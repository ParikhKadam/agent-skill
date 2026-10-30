#!/usr/bin/env python3
"""wsctl: manage a clarity-planning workspace (a folder of small markdown docs).

Standard library only. Run `python3 wsctl.py -h` for the command list.

  init     create a workspace (logs and the clarity stage's docs)
  init-stage  add a later stage's template docs
  find     list planning workspaces under a folder
  new      add a decision, spike, component, contract, case or slice from a template
  status   where are we, what is open at the current layer, what may be stale
  check    lint the workspace (broken links between docs, missing owners, unmet gates)
  index    write INDEX.md, the detailed index of every doc
  read-set list the few docs needed for one purpose (or one doc and what it rests on)
  impact   docs that name or rest on a doc or table row (what to reread after a change)
  stage    which stage is next, and whether a stage's prerequisites are met
  gate     set a layer's gate status, evidence and notes
  bump     record that a doc's meaning changed (version + 1, today's date)
  dep      add a pinned dependency to a doc
  set      edit a doc's front matter (summary, status, confidence, other fields); body untouched
  section  replace (or append) the body under one `##` heading from a file or stdin
  pin      after checking a doc still holds, point its dependency pins at current versions
  html     write the shareable pages (start-here, story, system, contracts, decisions-and-risks, build-plan, everything)
           into <workspace>/html/; --check validates them; --classic writes the old three flat pages instead
"""
import argparse
import datetime
import html as htmllib
import os
import re
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATES = SKILL_DIR / "assets" / "templates"

LAYERS = {
    0: "Intake and sizing",
    1: "Outcome and value",
    2: "World and facts",
    3: "Risks, unknowns and decisions",
    4: "User flow and re-entry points",
    5: "Artifacts and staleness",
    6: "Components",
    7: "System flow",
    8: "Cross-cutting concerns",
    9: "Contracts",
    10: "Implementation plan",
    11: "Change protocol",
}
# Stage skills: which layers each settles and which gates it needs first.
STAGES = {
    "clarity": {"skill": "plan-clarity", "layers": [0, 1, 2, 3], "needs": []},
    "components": {"skill": "plan-components", "layers": [4, 5, 6], "needs": [0, 1, 2, 3]},
    "flows": {"skill": "plan-flows", "layers": [7, 8, 9], "needs": [4, 5, 6]},
    "build": {"skill": "plan-build", "layers": [10], "needs": [7, 8, 9]},
    "change": {"skill": "plan-change", "layers": [11], "needs": []},
    "review": {"skill": "plan-review", "layers": [], "needs": []},
}
FOLDERS = {
    "00-start": "Start here: what and why",
    "10-world": "The world: facts, existing system, constraints",
    "20-risks-and-decisions": "Risks, decisions, open questions",
    "30-behavior": "Behavior: what users and the system do",
    "40-design": "Design: components, cross-cutting, contracts",
    "50-plan": "Plan: how we build it",
    "90-log": "Log: gates, changes, sessions",
}
READ_SET_PURPOSE = {
    "onboard": "A newcomer's first read (about 10 minutes)",
    "understand": "Understand the feature in plain words",
    "review": "Review the plan before building",
    "build-component": "Build or change one component",
    "contract": "Work on a boundary with another team",
    "change-request": "A requirement changed: find what to reopen",
}
STATUSES = {"draft", "agreed", "pending", "stale", "superseded", "parked"}
CONFIDENCE = {"decided", "hypothesis", "unknown", "measured"}
BASIS = {"evidence", "standard-practice", "preference"}
GATE_STATUSES = {"not-started", "in-progress", "passed", "passed-with-conditions", "skipped"}
PASSED = ("passed", "passed-with-conditions")
DONE = PASSED + ("skipped",)
ROW_ID = re.compile(r"^(ART|F|Q|R|X|V)-[\w-]+$")
REQUIRED = ["id", "title", "layer", "kind", "status", "version", "summary"]

# Templates each stage creates: (template, destination, smallest size that needs it).
# `init` creates the log docs and the clarity stage; later stages run `init-stage`.
LOG_DOCS = [
    ("gates.md", "90-log/gates.md"),
    ("change-log.md", "90-log/change-log.md"),
    ("sessions.md", "90-log/sessions.md"),
]
STAGE_DOCS = {
    "clarity": [
        ("brief.md", "00-start/brief.md", "small"),
        ("glossary.md", "00-start/glossary.md", "small"),
        ("case.md", "00-start/cases/case-01.md", "small"),
        ("open-questions.md", "20-risks-and-decisions/open-questions.md", "small"),
        ("facts-register.md", "10-world/facts-register.md", "medium"),
        ("existing-system.md", "10-world/existing-system.md", "medium"),
        ("constraints.md", "10-world/constraints.md", "medium"),
        ("risks.md", "20-risks-and-decisions/risks.md", "medium"),
    ],
    "components": [
        ("user-flow.md", "30-behavior/user-flow.md", "small"),
        ("artifacts.md", "30-behavior/artifacts.md", "medium"),
    ],
    "flows": [
        ("system-flow.md", "30-behavior/system-flow.md", "medium"),
        ("cross-cutting.md", "40-design/cross-cutting.md", "medium"),
    ],
    "build": [
        ("implementation-plan.md", "50-plan/implementation-plan.md", "small"),
    ],
    "change": [],
}
SIZE_RANK = {"small": 0, "medium": 1, "large": 2}
NEW_KINDS = {
    # kind: (template, folder, id prefix, filename pattern)
    "decision": ("decision.md", "20-risks-and-decisions/decisions", "D-", "{id}-{slug}.md"),
    "spike": ("spike.md", "20-risks-and-decisions/spikes", "S-", "{id}-{slug}.md"),
    "component": ("component.md", "40-design/components", "C-", "{id}.md"),
    "contract": ("contract.md", "40-design/contracts", "K-", "{id}.md"),
    "case": ("case.md", "00-start/cases", "CASE-", "case-{num}.md"),
    "slice": ("slice.md", "50-plan/slices", "SL-", "{id}-{slug}.md"),
}


# ---------------------------------------------------------------- parsing

FM = re.compile(r"\A---\n(.*?)\n---\n?", re.S)


def parse_value(v):
    v = v.strip()
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        return [x.strip().strip("'\"") for x in inner.split(",") if x.strip()]
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    return v.strip("'\"")


def split_doc(text):
    m = FM.match(text)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = parse_value(v)
    return meta, text[m.end():]


class Doc:
    def __init__(self, rel, meta, body):
        self.rel = rel
        self.meta = meta
        self.body = body

    @property
    def id(self):
        return str(self.meta.get("id", ""))

    @property
    def title(self):
        return str(self.meta.get("title", self.rel.stem))

    @property
    def layer(self):
        v = self.meta.get("layer")
        return v if isinstance(v, int) else None

    @property
    def kind(self):
        return str(self.meta.get("kind", ""))

    @property
    def status(self):
        return str(self.meta.get("status", ""))

    @property
    def version(self):
        v = self.meta.get("version", 1)
        return v if isinstance(v, int) else 1

    @property
    def summary(self):
        return str(self.meta.get("summary", ""))

    @property
    def read_sets(self):
        v = self.meta.get("read_sets", [])
        return v if isinstance(v, list) else [v]

    @property
    def deps(self):
        v = self.meta.get("depends_on", [])
        v = v if isinstance(v, list) else [v]
        out = []
        for item in v:
            if "@" in item:
                i, n = item.split("@", 1)
                out.append((i.strip(), int(n) if n.strip().isdigit() else None))
            elif item:
                out.append((item.strip(), None))
        return out

    @property
    def folder(self):
        return self.rel.parts[0] if len(self.rel.parts) > 1 else ""


def load_docs(root):
    docs, stray = [], []
    for p in sorted(root.rglob("*.md")):
        rel = p.relative_to(root)
        if rel.name == "INDEX.md" and len(rel.parts) == 1:
            continue
        if any(part.startswith(".") or part in ("html", "html-src") for part in rel.parts):
            continue
        meta, body = split_doc(p.read_text(encoding="utf-8"))
        if not meta:
            stray.append(rel)
            continue
        docs.append(Doc(rel, meta, body))
    return docs, stray


def split_row(line):
    line = line.strip().replace("\\|", "\x00")
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip().replace("\x00", "|") for c in line.split("|")]


def tables(body):
    """Return [(nearest heading, [row dicts keyed by lowercased header])]."""
    lines = body.splitlines()
    out, heading, i = [], "", 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
        if (line.lstrip().startswith("|") and i + 1 < len(lines)
                and re.match(r"^\s*\|[\s:|\-]+\|\s*$", lines[i + 1]) and "-" in lines[i + 1]):
            header = [h.lower() for h in split_row(line)]
            rows, j = [], i + 2
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                cells = split_row(lines[j])
                cells += [""] * (len(header) - len(cells))
                rows.append(dict(zip(header, cells)))
                j += 1
            out.append((heading, rows))
            i = j
            continue
        i += 1
    return out


def is_blank(cell):
    c = (cell or "").strip()
    return (not c or c.upper().startswith("TODO") or re.fullmatch(r"<[^>]*>", c) is not None
            or c in {"?", "-", "…", "..."})


def section_blank(text):
    """A section is blank if empty, or any line still starts with TODO."""
    return (not text.strip()) or re.search(r"^\s*TODO\b", text, re.M) is not None


def section(body, heading):
    """Text under the first heading whose title starts with `heading` (case-insensitive)."""
    lines = body.splitlines()
    start, level = None, 0
    for i, line in enumerate(lines):
        m = re.match(r"^(#+)\s+(.*)$", line)
        if not m:
            continue
        if start is None:
            if m.group(2).strip().lower().startswith(heading.lower()):
                start, level = i + 1, len(m.group(1))
        elif len(m.group(1)) <= level:
            return "\n".join(lines[start:i]).strip()
    return "\n".join(lines[start:]).strip() if start is not None else ""


def read_gates(docs):
    gates = {}
    for d in docs:
        if d.id == "GATES":
            for _, rows in tables(d.body):
                for r in rows:
                    m = re.match(r"^\d+$", r.get("layer", "").strip())
                    if m:
                        gates[int(m.group(0))] = (r.get("status", "").strip().lower(), r)
    return gates


def find_root(arg):
    p = Path(arg).resolve()
    if not p.is_dir():
        sys.exit(f"not a directory: {p}")
    return p


# ---------------------------------------------------------------- templates

def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:48] or "item"


def id_slug(s, limit=24):
    """A slug for a permanent id: whole words only, at most `limit` characters."""
    out = ""
    for w in slugify(s).split("-"):
        if len(out) + len(w) + (1 if out else 0) > limit:
            break
        out = f"{out}-{w}" if out else w
    return out or slugify(s)[:limit]


def row_index(docs):
    """Map table-row ids (ART-01, F-07, Q-1, R-2, X-03, V-1) to the doc that holds them."""
    rows = {}
    for d in docs:
        for _, rs in tables(d.body):
            for r in rs:
                rid = r.get("id", r.get("#", "")).strip()
                if ROW_ID.match(rid):
                    rows.setdefault(rid, d)
    return rows


def mentions(docs, target, exclude=None):
    pat = re.compile(rf"(?<![\w-]){re.escape(target)}(?![\w-])")
    return [d for d in docs if d is not exclude and d.id != target and pat.search(d.body)]


def render_template(name, **subs):
    text = (TEMPLATES / name).read_text(encoding="utf-8")
    for k, v in subs.items():
        text = text.replace("{{" + k.upper() + "}}", str(v))
    return text


def _write_stage_docs(root, stage, subs, size, mode):
    made = []
    plan = [(t, dst) for t, dst, need in STAGE_DOCS[stage] if SIZE_RANK[size] >= SIZE_RANK[need]]
    if stage == "clarity" and mode == "rescue":
        plan.append(("divergence.md", "10-world/divergence.md"))
    for tpl, dest in plan:
        out = root / dest
        if out.exists():
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_template(tpl, **subs), encoding="utf-8")
        made.append(dest)
    return made


def cmd_init(a):
    root = Path(a.path).resolve()
    if (root / "90-log" / "gates.md").exists() or (root / "00-start").exists():
        sys.exit(f"workspace already exists at {root}")
    today = datetime.date.today().isoformat()
    subs = dict(feature=a.name, slug=slugify(a.name), date=today, size=a.size, mode=a.mode,
                id="CASE-01", title="first case")
    for tpl, dest in LOG_DOCS:
        out = root / dest
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_template(tpl, **subs), encoding="utf-8")
    made = _write_stage_docs(root, "clarity", subs, a.size, a.mode)
    for d in FOLDERS:
        (root / d).mkdir(parents=True, exist_ok=True)
    print(f"created {a.size} workspace at {root} ({len(made) + len(LOG_DOCS)} docs: the clarity stage and the logs)")
    print("Later stages add their own docs with `wsctl.py init-stage <ws> <stage>`.")
    cmd_index(argparse.Namespace(path=str(root), quiet=True))


def cmd_init_stage(a):
    """Create a stage's template docs if they do not exist yet."""
    root = find_root(a.path)
    if a.stage not in STAGE_DOCS:
        sys.exit(f"unknown stage {a.stage}; one of {', '.join(STAGE_DOCS)}")
    docs, _ = load_docs(root)
    brief = next((d for d in docs if d.id == "BRIEF"), None)
    size = str(brief.meta.get("size", "medium")) if brief else "medium"
    size = size if size in SIZE_RANK else "medium"
    mode = str(brief.meta.get("mode", "brownfield")) if brief else "brownfield"
    today = datetime.date.today().isoformat()
    subs = dict(feature=brief.title if brief else root.name, slug=slugify(root.name), date=today,
                size=size, mode=mode, id="CASE-01", title="first case")
    made = _write_stage_docs(root, a.stage, subs, size, mode)
    print(f"stage {a.stage}: " + (f"created {', '.join(made)}" if made else "all its docs already exist"))


def cmd_new(a):
    root = find_root(a.path)
    tpl, folder, prefix, pattern = NEW_KINDS[a.kind]
    docs, _ = load_docs(root)
    slug = slugify(a.title)
    num = ""
    if a.id:
        new_id = a.id if a.id.startswith(prefix) else prefix + a.id
        m = re.match(re.escape(prefix) + r"(\d+)$", new_id)
        num = m.group(1) if m else id_slug(a.id)
    elif a.kind in ("component", "contract"):
        new_id = prefix + id_slug(a.title)
    else:
        nums = [int(m.group(1)) for d in docs
                for m in [re.match(re.escape(prefix) + r"(\d+)$", d.id)] if m]
        n = max(nums or [0]) + 1
        width = 2 if a.kind in ("case", "slice") else 3
        num = str(n).zfill(width)
        new_id = prefix + num
    if any(d.id == new_id for d in docs):
        sys.exit(f"id {new_id} already exists")
    dest = root / folder / pattern.format(id=new_id, slug=id_slug(a.title, 40), num=num)
    dest.parent.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    text = render_template(tpl, id=new_id, title=a.title, date=today, slug=slug)
    if a.layer is not None:
        text = re.sub(r"(?m)^layer: \d+$", f"layer: {a.layer}", text, count=1)
    known = {d.id for d in docs} | set(row_index(docs))
    m = re.search(r"(?m)^depends_on: \[(.*)\]$", text)
    dropped = []
    if m:
        keep = []
        for item in [x.strip() for x in m.group(1).split(",") if x.strip()]:
            (keep if item.split("@")[0] in known else dropped).append(item.split("@")[0] if item.split("@")[0] in known else item)
        vers = {d.id: d.version for d in docs}
        keep = [f"{k}@{vers[k]}" if k in vers else k for k in keep]
        text = text[:m.start()] + "depends_on: [" + ", ".join(keep) + "]" + text[m.end():]
    dest.write_text(text, encoding="utf-8")
    print(f"created {dest.relative_to(root)} (id {new_id})")
    if dropped:
        print(f"  left out dependencies that do not exist yet: {', '.join(dropped)} (add later with `wsctl.py dep`)")


# ---------------------------------------------------------------- checks

def run_checks(root):
    docs, stray = load_docs(root)
    F = []  # (level, where, message)
    by_id = {}
    for d in docs:
        for k in REQUIRED:
            if k not in d.meta or d.meta[k] in ("", None):
                F.append(("ERROR", str(d.rel), f"front matter is missing '{k}'"))
        if d.status and d.status not in STATUSES:
            F.append(("ERROR", str(d.rel), f"status '{d.status}' is not one of {sorted(STATUSES)}"))
        if d.id in by_id:
            F.append(("ERROR", str(d.rel), f"duplicate id {d.id} (also {by_id[d.id].rel})"))
        by_id[d.id] = d
    for r in stray:
        F.append(("WARN", str(r), "no front matter, so the index ignores it"))

    rows = row_index(docs)
    gates = read_gates(docs)
    gst = lambda l: gates.get(l, ("not-started", {}))[0] if l is not None else "in-progress"
    # Docs of layers whose gate has not started are still templates: skip their content checks.
    quiet = lambda d: bool(gates) and gst(d.layer) == "not-started"
    for d in docs:
        for dep, pin in d.deps:
            t = by_id.get(dep) or rows.get(dep)
            if not t:
                F.append(("ERROR", str(d.rel), f"depends on unknown id {dep} (no doc or table row has it)"))
                continue
            if pin is not None and pin > t.version:
                F.append(("ERROR", str(d.rel), f"pins {dep}@{pin}, but {t.id} is only at version {t.version}"))
            elif pin is not None and t.version > pin:
                F.append(("WARN", str(d.rel),
                          f"possibly stale: written against {dep}@{pin}, which is now @{t.version}. "
                          f"Reconcile, then update the pin"))
            if t.status == "superseded" and d.status != "superseded":
                F.append(("WARN", str(d.rel), f"rests on superseded doc {dep}"))
        if d.status == "agreed":
            n = len(re.findall(r"\bTODO\b|\{\{", d.body))
            if n:
                F.append(("WARN", str(d.rel), f"agreed but still has {n} TODO marker(s)"))
        if d.kind == "decision" and not quiet(d):
            if d.meta.get("confidence") not in CONFIDENCE:
                F.append(("WARN", str(d.rel), f"decision needs confidence: one of {sorted(CONFIDENCE)}"))
            elif d.meta.get("confidence") == "unknown" and d.status == "agreed":
                F.append(("WARN", str(d.rel), "agreed decision whose confidence is 'unknown'"))
            if d.meta.get("basis") not in BASIS:
                F.append(("WARN", str(d.rel), f"decision needs basis: one of {sorted(BASIS)}"))
            elif d.meta.get("basis") == "standard-practice" and d.meta.get("confidence") in ("decided", "measured") \
                    and "source" not in d.body.lower() and "tested" not in d.body.lower() and "measured" not in d.body.lower():
                F.append(("INFO", str(d.rel), "standard-practice decision marked firm: say what tested it or cite a source"))
            if section_blank(section(d.body, "What would change this")):
                F.append(("WARN", str(d.rel), "decision does not say what would change it"))

    for layer, (st, row) in gates.items():
        if st not in GATE_STATUSES:
            F.append(("ERROR", "90-log/gates.md", f"layer {layer} has status '{st}'"))
        if st == "skipped" and is_blank(row.get("notes", "")):
            F.append(("WARN", "90-log/gates.md", f"layer {layer} skipped without a reason in notes"))
        if st == "passed-with-conditions" and is_blank(row.get("notes", "")):
            F.append(("WARN", "90-log/gates.md", f"layer {layer} passed with conditions but the conditions are not in notes"))
        if st in PASSED:
            ld = [d for d in docs if d.layer == layer and d.kind != "gates"]
            if not ld:
                F.append(("WARN", "90-log/gates.md", f"layer {layer} passed but no doc is tagged layer {layer}"))
            for d in ld:
                if d.status == "draft" and d.kind != "log":
                    F.append(("WARN", str(d.rel), f"layer {layer} gate passed but this doc is still draft "
                              f"(agreed, or pending if it waits on someone)"))
            ev = row.get("evidence", "")
            if is_blank(ev):
                F.append(("WARN", "90-log/gates.md", f"layer {layer} passed with no evidence listed"))
            gate_date = row.get("date", "").strip()
            for tok in re.findall(r"[A-Z][A-Z0-9]*-[\w-]+|[A-Z]{3,}", ev):
                t = by_id.get(tok)
                if t and gate_date and str(t.meta.get("updated", "")) > gate_date:
                    F.append(("WARN", "90-log/gates.md", f"layer {layer} evidence {tok} changed on "
                              f"{t.meta.get('updated')} after the gate passed on {gate_date}: re-confirm or reopen"))

    # cross-layer consistency
    artifact_ids, artifact_rows = set(), []
    for d in docs:
        if d.kind == "artifact":
            for _, rows in tables(d.body):
                for r in rows:
                    if re.match(r"^ART-", r.get("id", "").strip()):
                        artifact_ids.add(r["id"].strip())
                        artifact_rows.append((d, r))
    comp_ids = {d.id for d in docs if d.kind == "component"}
    for d, r in artifact_rows:
        if quiet(d):
            continue
        for col in ("user can", "depends on", "goes stale when"):
            if col in r and is_blank(r[col]):
                F.append(("WARN", str(d.rel), f"{r['id']}: column '{col}' is empty. This table is where hidden decisions surface"))
        pb = r.get("produced by", "")
        if is_blank(pb):
            F.append(("WARN", str(d.rel), f"{r['id']}: no producer named"))
        else:
            for tok in re.findall(r"\bC-[\w-]+", pb):
                if "TODO" in tok.upper():
                    continue
                if comp_ids and tok not in comp_ids:
                    F.append(("ERROR", str(d.rel), f"{r['id']}: producer {tok} has no component doc"))
    art_settled = gst(5) in PASSED
    for d in docs:
        if quiet(d):
            continue
        if d.kind == "flow":
            for heading, rows in tables(d.body):
                if rows and "artifact" in rows[0] and "re-entr" in heading.lower():
                    for r in rows:
                        cell = r.get("artifact", "")
                        step = r.get("step", "?")
                        toks = re.findall(r"\bART-[\w-]+", cell)
                        if is_blank(cell):
                            F.append(("WARN", str(d.rel), f"re-entry '{step}': name the artifact or list it as ruled out"))
                        for t in toks:
                            if t not in artifact_ids:
                                lvl = "ERROR" if art_settled else "WARN"
                                F.append((lvl, str(d.rel), f"re-entry '{step}' names {t}, which is not in the artifact register"
                                          + ("" if art_settled else " yet (define it in layer 5)")))
        if d.kind == "component":
            for sec in ("Who decides", "Quality bar", "Runs alone"):
                if section_blank(section(d.body, sec)):
                    F.append(("WARN", str(d.rel), f"component section '{sec}' is empty"))
        if d.kind == "contract" and d.status != "pending":
            if d.body.count("```") < 4:
                F.append(("WARN", str(d.rel), "contract needs at least two examples (happy path and a failure) in code blocks"))
        if d.kind == "plan":
            for heading, rows in tables(d.body):
                if rows and "exit check" in rows[0]:
                    for r in rows:
                        if is_blank(r.get("id", "")) or r.get("id", "").lower() in ("skeleton",):
                            pass
                        if is_blank(r.get("exit check", "")):
                            F.append(("WARN", str(d.rel), f"slice '{r.get('slice', r.get('id', '?'))}' has no exit check"))
                        if "flag or rollback" in r and is_blank(r["flag or rollback"]):
                            F.append(("INFO", str(d.rel), f"slice '{r.get('slice', r.get('id', '?'))}' has no flag or rollback"))
        if d.kind == "fact":
            for _, rows in tables(d.body):
                for r in rows:
                    if re.match(r"^F-", r.get("id", "").strip()):
                        if is_blank(r.get("where it lives", "")):
                            F.append(("WARN", str(d.rel), f"{r['id']}: no source for this fact"))
                        if is_blank(r.get("status", "")):
                            F.append(("WARN", str(d.rel), f"{r['id']}: no status (measured, doc, inferred or unknown)"))
        if d.kind == "question":
            for _, rows in tables(d.body):
                for r in rows:
                    if re.match(r"^Q-", r.get("id", "").strip()) and r.get("status", "").lower() == "open":
                        if is_blank(r.get("owner", "")):
                            F.append(("WARN", str(d.rel), f"{r['id']}: open question with no owner"))
    index = root / "INDEX.md"
    newest = max((root / d.rel).stat().st_mtime for d in docs) if docs else 0
    if not index.exists() or index.stat().st_mtime < newest:
        F.append(("INFO", "INDEX.md", "out of date: run `wsctl.py index`"))
    return docs, F


def cmd_check(a):
    root = find_root(a.path)
    _, F = run_checks(root)
    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    for lvl, where, msg in sorted(F, key=lambda f: (order[f[0]], f[1])):
        if lvl == "INFO" and not a.verbose:
            continue
        print(f"{lvl:5} {where}: {msg}")
    errs = sum(1 for f in F if f[0] == "ERROR")
    warns = sum(1 for f in F if f[0] == "WARN")
    print(f"\n{errs} error(s), {warns} warning(s)")
    sys.exit(1 if errs else 0)


# ---------------------------------------------------------------- status

def current_layer(gates):
    """The layer to work on now, or None when layers 0-10 are all done."""
    if all(gates.get(l, ("not-started",))[0] in DONE for l in range(0, 11)):
        return None
    for layer in range(0, 11):
        if gates.get(layer, ("not-started",))[0] == "in-progress":
            return layer
    for layer in range(0, 11):
        if gates.get(layer, ("not-started",))[0] not in DONE:
            return layer
    return None


def open_items(docs):
    out = {"questions": [], "unknown_facts": [], "risks": []}
    for d in docs:
        for _, rows in tables(d.body):
            for r in rows:
                rid = r.get("id", "").strip()
                if d.kind == "question" and rid.startswith("Q-") and r.get("status", "").lower() == "open":
                    out["questions"].append(r)
                if d.kind == "fact" and rid.startswith("F-") and r.get("status", "").lower() in ("unknown", ""):
                    out["unknown_facts"].append(r)
                if d.kind == "risk" and rid.startswith("R-") and r.get("status", "").lower() in ("open", ""):
                    out["risks"].append(r)
        if d.kind == "spike" and d.status in ("draft", "pending") and \
                section_blank(section(d.body, "Result")):
            out["risks"].append({"id": d.id, "assumption that could break the design": f"spike not run: {d.title}"})
    return out


def cmd_status(a):
    root = find_root(a.path)
    docs, F = run_checks(root)
    gates = read_gates(docs)
    brief = next((d for d in docs if d.id == "BRIEF"), None)
    print(f"{brief.title if brief else root.name}  size={brief.meta.get('size','?') if brief else '?'}"
          f"  mode={brief.meta.get('mode','?') if brief else '?'}")
    cur = current_layer(gates)
    print("\nLayer gates")
    for layer, name in LAYERS.items():
        st = gates.get(layer, ("not-started",))[0]
        n = sum(1 for d in docs if d.layer == layer and d.kind != "gates")
        mark = "<-- current" if layer == cur else ""
        print(f"  {layer:>2} {name:<32} {st:<23} {n} doc(s) {mark}")
    oi = open_items(docs)
    print(f"\nOpen: {len(oi['questions'])} question(s), {len(oi['unknown_facts'])} unknown fact(s), {len(oi['risks'])} open risk(s)")
    for q in oi["questions"][:8]:
        print(f"  {q.get('id')}: {q.get('question', '')[:90]}  [owner: {q.get('owner', '?')}]")
    stale = [f for f in F if "possibly stale" in f[2]]
    if stale:
        print(f"\nPossibly stale ({len(stale)}):")
        for _, where, msg in stale[:8]:
            print(f"  {where}: {msg}")
    conds = [(l, r.get("notes", "")) for l, (st_, r) in sorted(gates.items()) if st_ == "passed-with-conditions"]
    if conds:
        print("\nConditions carried from gates passed with conditions:")
        for l, n in conds:
            print(f"  layer {l}: {n}")
    if cur is None:
        print("\nPlan complete: layers 0-10 are done. Use plan-change when something changes.")
        return
    owner = next((n for n, s in STAGES.items() if cur in s["layers"]), "?")
    print(f"\nLayer {cur} ({LAYERS[cur]}) belongs to stage '{owner}' ({STAGES.get(owner, {}).get('skill', '?')}). "
          f"Read references/layers/{cur:02d}-*.md, then ask the next round.")
    print("When the user agrees the gate is met: wsctl.py gate <ws> <layer> passed --evidence \"...\"")


# ---------------------------------------------------------------- index

def cell(s):
    return str(s).replace("|", "/").replace("\n", " ").strip()


def cmd_index(a):
    root = find_root(a.path)
    docs, F = run_checks(root)
    gates = read_gates(docs)
    brief = next((d for d in docs if d.id == "BRIEF"), None)
    name = brief.title if brief else root.name
    today = datetime.date.today().isoformat()
    L = [f"# {name}: planning index", "",
         f"Generated by `wsctl.py index` on {today}. Do not edit by hand; edit the docs and re-run.", "",
         "## How to use this index", "",
         "- To understand the feature, open the **understand** reading path below. You do not need the rest.",
         "- To work on one thing, use `wsctl.py read-set <workspace> <id>` to list just the docs it rests on.",
         "- After a change, `wsctl.py impact <workspace> <id>` lists every doc to reopen.", "",
         "## Status by layer", "", "| Layer | Name | Gate | Docs |", "|---|---|---|---|"]
    for layer, nm in LAYERS.items():
        st = gates.get(layer, ("not-started",))[0]
        n = sum(1 for d in docs if d.layer == layer and d.kind != "gates")
        L.append(f"| {layer} | {nm} | {st} | {n} |")
    sets = {}
    for d in docs:
        for s in d.read_sets:
            sets.setdefault(s, []).append(d)
    L += ["", "## Reading paths", ""]
    for s in sorted(sets, key=lambda x: list(READ_SET_PURPOSE).index(x) if x in READ_SET_PURPOSE else 99):
        L.append(f"### {s}: {READ_SET_PURPOSE.get(s, 'custom reading path')}")
        L.append("")
        for d in sorted(sets[s], key=lambda d: (d.layer if d.layer is not None else 99, str(d.rel))):
            L.append(f"- [{d.title}]({d.rel.as_posix()}): {d.summary}")
        L.append("")
    L += ["## Every document", ""]
    folders = {}
    for d in docs:
        folders.setdefault(d.folder, []).append(d)
    for f in sorted(folders):
        L += [f"### {f or 'root'}: {FOLDERS.get(f, '')}", "",
              "| ID | Title | Layer | Status | v | Summary | Rests on |", "|---|---|---|---|---|---|---|"]
        for d in sorted(folders[f], key=lambda d: str(d.rel)):
            deps = ", ".join(f"{i}@{p}" if p else i for i, p in d.deps)
            L.append(f"| {d.id} | [{cell(d.title)}]({d.rel.as_posix()}) | {d.layer} | {d.status} | {d.version} | {cell(d.summary)} | {deps} |")
        L.append("")
    dec = [d for d in docs if d.kind == "decision"]
    if dec:
        L += ["## Decisions", "", "| ID | Decision | Confidence | Status | Summary |", "|---|---|---|---|---|"]
        for d in sorted(dec, key=lambda d: d.id):
            L.append(f"| {d.id} | [{cell(d.title)}]({d.rel.as_posix()}) | {d.meta.get('confidence', '?')} | {d.status} | {cell(d.summary)} |")
        L.append("")
    oi = open_items(docs)
    if oi["questions"]:
        L += ["## Open questions", "", "| ID | Question | Owner | Recommended answer |", "|---|---|---|---|"]
        for q in oi["questions"]:
            L.append(f"| {q.get('id')} | {cell(q.get('question', ''))} | {cell(q.get('owner', ''))} | {cell(q.get('recommended answer', ''))} |")
        L.append("")
    if oi["unknown_facts"]:
        L += ["## Facts still unknown", "", "| ID | Fact | Where it might live |", "|---|---|---|"]
        for r in oi["unknown_facts"]:
            L.append(f"| {r.get('id')} | {cell(r.get('fact needed', ''))} | {cell(r.get('where it lives', ''))} |")
        L.append("")
    issues = [f for f in F if f[0] in ("ERROR", "WARN")]
    L += ["## Health", ""]
    if issues:
        for lvl, where, msg in issues:
            L.append(f"- {lvl} `{where}`: {msg}")
    else:
        L.append("No errors or warnings.")
    (root / "INDEX.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    if not getattr(a, "quiet", False):
        print(f"wrote {root / 'INDEX.md'} ({len(docs)} docs, {len(issues)} issue(s))")


# ---------------------------------------------------------------- read-set / impact

def cmd_read_set(a):
    root = find_root(a.path)
    docs, _ = load_docs(root)
    by_id = {d.id: d for d in docs}
    rows = row_index(docs)
    target = a.target
    if target in rows and target not in by_id:
        target = rows[target].id  # a table row: read the doc that holds it
    if target in by_id:
        seen, order = set(), []

        def walk(i, depth):
            i = rows[i].id if i in rows and i not in by_id else i
            if i in seen or i not in by_id:
                return
            seen.add(i)
            order.append(by_id[i])
            if depth:
                for dep, _ in by_id[i].deps:
                    walk(dep, depth - 1)
        walk(target, 99 if a.deep else 1)
        picked = order
    else:
        picked = [d for d in docs if a.target in d.read_sets]
        if not picked:
            sets = sorted({s for d in docs for s in d.read_sets})
            sys.exit(f"no doc, row or reading path named '{a.target}'. Reading paths: {', '.join(sets) or 'none'}")
        picked.sort(key=lambda d: (d.layer if d.layer is not None else 99, str(d.rel)))
    for d in picked:
        print(d.rel.as_posix() if a.paths else f"{d.rel.as_posix()}  [{d.id} v{d.version} {d.status}]  {d.summary}")


def cmd_impact(a):
    """What to reread after `target` changes: docs that name it in depends_on or mention it in their text.
    Direct only by default; --deep follows whole-doc dependencies further (usually too broad)."""
    root = find_root(a.path)
    docs, _ = load_docs(root)
    by_id = {d.id: d for d in docs}
    rows = row_index(docs)
    if a.target not in by_id and a.target not in rows:
        sys.exit(f"unknown id {a.target} (no doc or table row has it)")
    owner = by_id.get(a.target) or rows[a.target]
    found = {}
    for d in docs:
        if d is owner:
            continue
        if any(dep == a.target for dep, _ in d.deps):
            found[d.id] = (d, "depends on it")
    for d in mentions(docs, a.target, exclude=owner):
        found.setdefault(d.id, (d, "mentions it"))
    if a.deep and a.target in by_id:
        rev = {}
        for d in docs:
            for dep, _ in d.deps:
                rev.setdefault(dep, []).append(d)
        queue = list(found)
        while queue:
            cur = queue.pop(0)
            for d in rev.get(cur, []):
                if d.id not in found and d is not owner:
                    found[d.id] = (d, f"via {cur}")
                    queue.append(d.id)
    where = f" (row in {owner.rel.as_posix()})" if a.target not in by_id else ""
    if not found:
        print(f"nothing names or rests on {a.target}{where}")
        return
    print(f"Reread these after {a.target}{where} changes:")
    for d, why in sorted(found.values(), key=lambda x: (x[0].layer if x[0].layer is not None else 99, str(x[0].rel))):
        print(f"  layer {d.layer}: {d.rel.as_posix()}  [{d.id}]  {why}")
    layers = sorted({d.layer for d, _ in found.values() if d.layer is not None})
    print(f"\nLayers to recheck: {', '.join(map(str, layers))}. Reopen only the layers whose docs you actually change;"
          f" log it in 90-log/change-log.md.")


def _find(root, target):
    docs, _ = load_docs(root)
    by_id = {d.id: d for d in docs}
    if target not in by_id:
        sys.exit(f"unknown id {target}")
    return by_id[target], by_id


def _set_front_matter(path, key, value):
    text = path.read_text(encoding="utf-8")
    m = FM.match(text)
    if not m:
        sys.exit(f"{path} has no front matter")
    block, n = re.subn(rf"(?m)^{re.escape(key)}:.*$", f"{key}: {value}", m.group(1), count=1)
    if n == 0:
        block = block + f"\n{key}: {value}"
    path.write_text("---\n" + block + "\n---\n" + text[m.end():], encoding="utf-8")


def cmd_bump(a):
    """Record that a doc's meaning changed: version + 1 and today's date."""
    root = find_root(a.path)
    d, _ = _find(root, a.target)
    new = d.version + 1
    _set_front_matter(root / d.rel, "version", new)
    _set_front_matter(root / d.rel, "updated", datetime.date.today().isoformat())
    rev = [x for x in load_docs(root)[0]
           if any(i == d.id and (p is None or p < new) for i, p in x.deps)]
    print(f"{d.id} is now v{new}.")
    if not rev:
        print("No doc pins it, so nothing shows as possibly stale. Run `wsctl.py impact` to find docs that mention it.")
        return
    print("These rest on it and now show as possibly stale:")
    for x in rev:
        print(f"  {x.rel.as_posix()}  [{x.id}]")
    print("Read each one, edit if it no longer holds, then run `wsctl.py pin <ws> <its id>`.")


def cmd_pin(a):
    """After checking a doc still holds, point its depends_on at the current versions."""
    root = find_root(a.path)
    d, by_id = _find(root, a.target)
    rows = row_index(load_docs(root)[0])
    new, changed = [], []
    for dep, pin in d.deps:
        t = by_id.get(dep) or rows.get(dep)
        if not t:
            sys.exit(f"{d.id} depends on unknown id {dep}")
        new.append(f"{dep}@{t.version}")
        if pin != t.version:
            changed.append(f"{dep}: {pin if pin is not None else 'unpinned'} -> {t.version}")
    _set_front_matter(root / d.rel, "depends_on", "[" + ", ".join(new) + "]")
    print(f"{d.id}: " + ("; ".join(changed) if changed else "pins already current"))
    print("Only pin after you have read the doc against what changed. Pinning without reading hides staleness.")


def cmd_dep(a):
    """Add a pinned dependency to a doc (a doc id or a table-row id such as ART-02)."""
    root = find_root(a.path)
    d, by_id = _find(root, a.target)
    rows = row_index(load_docs(root)[0])
    t = by_id.get(a.dep) or rows.get(a.dep)
    if not t:
        sys.exit(f"unknown id {a.dep} (no doc or table row has it)")
    deps = [f"{i}@{p}" if p is not None else i for i, p in d.deps if i != a.dep]
    deps.append(f"{a.dep}@{t.version}")
    _set_front_matter(root / d.rel, "depends_on", "[" + ", ".join(deps) + "]")
    print(f"{d.id} now rests on {a.dep}@{t.version}")


PROTECTED_FIELDS = {"id": "never change an id", "version": "use `wsctl.py bump`",
                    "updated": "set automatically", "depends_on": "use `wsctl.py dep` / `pin`"}


def _fm_value(v):
    """Render a value as plain one-line front matter (lists pass through; risky text is quoted)."""
    v = v.strip()
    if "\n" in v:
        sys.exit("front matter values must be one line")
    if v.startswith("[") and v.endswith("]"):
        return v
    if re.search(r": |\s#", v) or v[:1] in "\"'[{&*!|>%@`" or v.endswith(":"):
        if '"' not in v:
            return f'"{v}"'
        if "'" not in v:
            return f"'{v}'"
        sys.exit("value has both quote kinds and a risky character; reword it")
    return v


def cmd_set(a):
    """Edit only a doc's front matter; the body and other keys stay byte-for-byte."""
    root = find_root(a.path)
    d, _ = _find(root, a.target)
    edits = []
    if a.summary is not None:
        edits.append(("summary", a.summary))
    if a.status:
        edits.append(("status", a.status))
    if a.confidence:
        edits.append(("confidence", a.confidence))
    for f in a.field or []:
        if "=" not in f:
            sys.exit(f"--field needs key=value, got {f!r}")
        k, v = f.split("=", 1)
        edits.append((k.strip(), v))
    if not edits:
        sys.exit("nothing to set: give --summary, --status, --confidence or --field key=value")
    for k, v in edits:
        if k in PROTECTED_FIELDS:
            sys.exit(f"{k} cannot be set here: {PROTECTED_FIELDS[k]}")
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_-]*", k):
            sys.exit(f"bad field name {k!r}")
        if k == "status" and v not in STATUSES:
            sys.exit(f"status must be one of {sorted(STATUSES)}")
        if k == "confidence" and v not in CONFIDENCE:
            sys.exit(f"confidence must be one of {sorted(CONFIDENCE)}")
    for k, v in edits:
        _set_front_matter(root / d.rel, k, _fm_value(v))
    _set_front_matter(root / d.rel, "updated", datetime.date.today().isoformat())
    print(f"{d.id}: set " + ", ".join(k for k, _ in edits) + " (version unchanged)")


def cmd_section(a):
    """Replace the body under one `##` heading (append it if missing); the rest stays intact."""
    root = find_root(a.path)
    d, _ = _find(root, a.target)
    path = root / d.rel
    src = sys.stdin.read() if a.file == "-" else Path(a.file).read_text(encoding="utf-8")
    new = src.strip("\n")
    if not new.strip():
        sys.exit("section text is empty")
    heading = a.heading.strip().lstrip("#").strip()
    text = path.read_text(encoding="utf-8")
    m = FM.match(text)
    head, body = (text[:m.end()], text[m.end():]) if m else ("", text)
    lines = body.splitlines(keepends=True)
    start = end = None
    heads, fence = [], False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        hm = None if fence else re.match(r"^(#+)\s+(.*?)\s*$", line)
        if not hm:
            continue
        if len(hm.group(1)) == 2:
            heads.append((i, hm.group(2).lower()))
    heads.append((len(lines), None))
    want = heading.lower()
    hit = next((k for k, (_, t) in enumerate(heads[:-1]) if t == want), None)
    if hit is None:  # like `section()`: a title that starts with the given words
        hit = next((k for k, (_, t) in enumerate(heads[:-1]) if t.startswith(want)), None)
    if hit is not None:
        start, end = heads[hit][0], heads[hit + 1][0]
    if start is None:
        pre = body if not body or body.endswith("\n") else body + "\n"
        body2 = pre + ("\n" if pre.strip() else "") + f"## {heading}\n\n{new}\n"
        verb = "appended"
    else:
        title = lines[start].rstrip("\n")
        block = f"{title}\n\n{new}\n" + ("\n" if end < len(lines) else "")
        body2 = "".join(lines[:start]) + block + "".join(lines[end:])
        verb = "replaced"
    path.write_text(head + body2, encoding="utf-8")
    _set_front_matter(path, "updated", datetime.date.today().isoformat())
    print(f"{d.id}: {verb} section '{heading}' (version unchanged)")


def cmd_find(a):
    """List planning workspaces under a folder (any folder with 90-log/gates.md)."""
    base = Path(a.path).resolve()
    hits = sorted(p.parent.parent for p in base.rglob("90-log/gates.md")
                  if not any(part.startswith(".") or part == "node_modules" for part in p.parts))
    if not hits:
        print(f"no planning workspace under {base}")
    for h in hits:
        print(h)


def _is_unverified(d):
    """True for a doc that waits on real evidence: front matter `invented: true`, or a filled-in Source line saying invented."""
    if str(d.meta.get("invented", "")).strip().lower() in ("true", "yes"):
        return True
    return any(re.match(r"^\s*(?:[-*]\s*)?\**Source:?\**:?\s*invented\b", l, re.I) and "TODO" not in l
               for l in d.body.splitlines())


def cmd_gate(a):
    """Set a layer's gate status (and evidence, notes) in 90-log/gates.md. Passing promotes the layer's draft docs."""
    root = find_root(a.path)
    if a.status not in GATE_STATUSES:
        sys.exit(f"status must be one of {sorted(GATE_STATUSES)}")
    f = root / "90-log" / "gates.md"
    if not f.exists():
        sys.exit("90-log/gates.md not found")
    lines = f.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^\|\s*(\d+)\s*\|", line)
        if m and int(m.group(1)) == a.layer:
            c = split_row(line)
            c += [""] * (6 - len(c))
            changing = c[2].strip() != a.status
            evidence = a.evidence if a.evidence is not None else c[3]
            notes = a.notes if a.notes is not None else c[5]
            if a.status == "skipped" and is_blank(notes):
                sys.exit("a skipped layer needs --notes with the reason")
            if a.status in PASSED and is_blank(evidence):
                sys.exit("a passed layer needs --evidence (doc ids, a measurement, who agreed)")
            if a.status == "passed-with-conditions" and is_blank(notes):
                sys.exit("passed-with-conditions needs --notes listing the conditions (they carry into the build plan)")
            c[2], c[3], c[5] = a.status, evidence, notes
            if changing or a.evidence is not None:
                c[4] = datetime.date.today().isoformat()
            lines[i] = "| " + " | ".join(c[:6]) + " |"
            f.write_text("\n".join(lines) + "\n", encoding="utf-8")
            print(f"layer {a.layer} ({LAYERS.get(a.layer, '?')}): {a.status}")
            if a.status in PASSED and changing and not a.no_promote:
                docs, _ = load_docs(root)
                promoted, kept = [], []
                for d in docs:
                    if d.layer == a.layer and d.status == "draft" and d.kind not in ("log", "gates"):
                        if _is_unverified(d):
                            kept.append(d.id)
                            continue
                        _set_front_matter(root / d.rel, "status", "agreed")
                        promoted.append(d.id)
                if promoted:
                    print(f"promoted to agreed: {', '.join(promoted)} (docs waiting on someone should be 'pending' instead)")
                if kept:
                    print(f"left as draft (invented/unverified, set them to pending): {', '.join(kept)}")
            return
    sys.exit(f"layer {a.layer} not found in gates.md")


def cmd_stage(a):
    """Show a stage's prerequisites and readiness, or (no name) every stage and which comes next."""
    root = find_root(a.path)
    docs, _ = load_docs(root)
    gates = read_gates(docs)
    st = lambda l: gates.get(l, ("not-started", {}))[0]
    notes = lambda l: gates.get(l, ("", {}))[1].get("notes", "") if l in gates else ""
    done = lambda l: st(l) in DONE
    declined = lambda l: not done(l) and "declined" in notes(l).lower()

    def stage_status(ls):
        if all(done(l) for l in ls):
            return "done"
        if all(done(l) or declined(l) for l in ls):
            return "declined"
        return "in progress" if any(st(l) != "not-started" for l in ls) else "not started"

    if not a.name:
        nxt = None
        print("Stage         Skill            Layers     Status")
        for name, s in STAGES.items():
            if name in ("change", "review"):
                continue
            status = stage_status(s["layers"])
            if nxt is None and status not in ("done", "declined"):
                nxt = name
            print(f"{name:<13} {s['skill']:<16} {','.join(map(str, s['layers'])):<10} {status}")
        print("change        plan-change      11         any time a fact or requirement changes")
        print("review        plan-review      -          any time, before a gate or on request (cold read, no layer)")
        if nxt:
            ready = all(done(l) for l in STAGES[nxt]["needs"])
            print(f"\nNext: {nxt} ({STAGES[nxt]['skill']})" + ("" if ready else "  [some prerequisites open: run `stage <ws> " + nxt + "`]"))
        else:
            print("\nAll stages done. Use plan-change when something changes.")
        return
    if a.name not in STAGES:
        sys.exit(f"unknown stage {a.name}; one of {', '.join(STAGES)}")
    s = STAGES[a.name]
    print(f"Stage {a.name} ({s['skill']}): layers {', '.join(f'{l} {LAYERS[l]}' for l in s['layers'])}")
    for l in s["needs"]:
        print(f"  needs layer {l:>2} {LAYERS[l]:<32} {st(l)}" + ("  (declined by user)" if declined(l) else ""))
    for l in s["layers"]:
        print(f"  owns  layer {l:>2} {LAYERS[l]:<32} {st(l)}")
    missing = [l for l in s["needs"] if not done(l)]
    if not missing:
        print("\nREADY")
    elif all(declined(l) for l in missing):
        print(f"\nPROCEEDING ON HYPOTHESES: the user declined layers {', '.join(map(str, missing))}; "
              f"record assumptions as hypotheses and reconcile with plan-change later")
    else:
        print(f"\nNOT READY: layers {', '.join(map(str, missing))} not passed or skipped")
    conds = [(l, notes(l)) for l in s["needs"] if st(l) == "passed-with-conditions"]
    for l, n in conds:
        print(f"  condition from layer {l}: {n}")
    missing_docs = [dst for t, dst, need in STAGE_DOCS.get(a.name, []) if not (root / dst).exists()]
    if missing_docs:
        print(f"\nThis stage's docs are not created yet: run `wsctl.py init-stage <ws> {a.name}`")
    prior = sorted((d for d in docs if d.layer in s["needs"] and d.kind not in ("gates", "log")),
                   key=lambda d: (d.layer, str(d.rel)))
    if prior:
        print("\nInputs from earlier stages (read the summaries; open a doc only when a question touches it):")
        for d in prior:
            print(f"  {d.rel.as_posix()}  [{d.id} {d.status}]  {d.summary}")


# ---------------------------------------------------------------- markdown to html

def esc(s):
    return htmllib.escape(s, quote=False)


def inline(s, link_fix=None):
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![*\w])\*([^*\n]+)\*(?!\w)", r"<em>\1</em>", s)

    def lk(m):
        href = m.group(2)
        if link_fix and not re.match(r"^(https?:|#|mailto:)", href):
            href = link_fix(href)
        return f'<a href="{href}">{m.group(1)}</a>'
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lk, s)


def md_to_html(md, link_fix=None):
    lines = md.splitlines()
    out, i = [], 0
    para = []

    def flush():
        if para:
            out.append("<p>" + inline(" ".join(para), link_fix) + "</p>")
            para.clear()

    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            flush()
            j, code = i + 1, []
            while j < len(lines) and not lines[j].startswith("```"):
                code.append(lines[j])
                j += 1
            out.append("<pre><code>" + esc("\n".join(code)) + "</code></pre>")
            i = j + 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            flush()
            lvl = min(len(m.group(1)) + 1, 6)  # page title owns h1
            out.append(f"<h{lvl}>{inline(m.group(2), link_fix)}</h{lvl}>")
            i += 1
            continue
        if (line.lstrip().startswith("|") and i + 1 < len(lines)
                and re.match(r"^\s*\|[\s:|\-]+\|\s*$", lines[i + 1])):
            flush()
            head = split_row(line)
            j, rows = i + 2, []
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                rows.append(split_row(lines[j]))
                j += 1
            t = ["<div class='tw'><table><thead><tr>" + "".join(f"<th>{inline(h, link_fix)}</th>" for h in head) + "</tr></thead><tbody>"]
            for r in rows:
                t.append("<tr>" + "".join(f"<td>{inline(c, link_fix)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table></div>")
            out.append("".join(t))
            i = j
            continue
        if re.match(r"^\s*([-*]|\d+\.)\s+", line):
            flush()
            stack, buf = [], []
            while i < len(lines) and re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]):
                mm = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", lines[i])
                indent = len(mm.group(1)) // 2
                tag = "ol" if mm.group(2)[0].isdigit() else "ul"
                while len(stack) > indent + 1:
                    buf.append(f"</li></{stack.pop()}>")
                if len(stack) == indent + 1:
                    buf.append("</li>")
                else:
                    while len(stack) < indent + 1:
                        buf.append(f"<{tag}>")
                        stack.append(tag)
                buf.append("<li>" + inline(mm.group(3), link_fix))
                i += 1
            while stack:
                buf.append(f"</li></{stack.pop()}>")
            out.append("".join(buf))
            continue
        if line.startswith(">"):
            flush()
            q = []
            while i < len(lines) and lines[i].startswith(">"):
                q.append(lines[i].lstrip("> "))
                i += 1
            out.append("<blockquote>" + inline(" ".join(q), link_fix) + "</blockquote>")
            continue
        if re.match(r"^---+\s*$", line):
            flush()
            out.append("<hr>")
            i += 1
            continue
        if not line.strip():
            flush()
        else:
            para.append(line.strip())
        i += 1
    flush()
    return "\n".join(out)


CSS = """
:root{--bg:#fbfaf7;--fg:#1f2328;--mut:#59636e;--card:#fff;--line:#d9d6cc;--acc:#1b5e8a;--chip:#eef3f7;--warn:#9a5b00}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#15181c;--fg:#e6e8ea;--mut:#9aa4ae;--card:#1d2127;--line:#323941;--acc:#6db3e0;--chip:#25303a;--warn:#e0a85a}}
:root[data-theme=dark]{--bg:#15181c;--fg:#e6e8ea;--mut:#9aa4ae;--card:#1d2127;--line:#323941;--acc:#6db3e0;--chip:#25303a;--warn:#e0a85a}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 system-ui,-apple-system,Segoe UI,sans-serif}
main{max-width:980px;margin:0 auto;padding:24px 16px 64px}
nav{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 20px}nav a{padding:6px 12px;border:1px solid var(--line);border-radius:999px;color:var(--fg);text-decoration:none;font-size:14px}
nav a.on{background:var(--acc);border-color:var(--acc);color:#fff}
h1{font-size:28px;margin:0 0 4px}h2{font-size:21px;margin:36px 0 8px;padding-top:8px;border-top:1px solid var(--line)}h3{font-size:17px;margin:22px 0 6px}h4,h5{margin:16px 0 4px}
.sub{color:var(--mut);margin:0 0 16px}a{color:var(--acc)}
.tw{overflow-x:auto;margin:10px 0}table{border-collapse:collapse;width:100%;font-size:14px}th,td{border:1px solid var(--line);padding:6px 9px;text-align:left;vertical-align:top}th{background:var(--chip)}
code{background:var(--chip);padding:1px 5px;border-radius:4px;font-size:.9em}pre{background:var(--chip);padding:12px;border-radius:8px;overflow-x:auto}pre code{background:none;padding:0}
blockquote{margin:10px 0;padding:6px 14px;border-left:4px solid var(--acc);background:var(--chip);border-radius:0 6px 6px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 16px;margin:10px 0}.card h3{margin:0 0 4px}
.chip{display:inline-block;padding:1px 9px;border-radius:999px;background:var(--chip);font-size:12px;margin-right:4px}
.missing{color:var(--warn);font-style:italic}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:10px}
"""

PAGES = [("overview.html", "Overview"), ("flows.html", "Flows and components"), ("plan.html", "Plan and risks")]


def render_page(title, sub, active, body):
    nav = "".join(f'<a href="{f}" class="{"on" if f == active else ""}">{n}</a>' for f, n in PAGES)
    return (f"<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            f"<meta name='viewport' content='width=device-width,initial-scale=1'><title>{esc(title)}</title>"
            f"<style>{CSS}</style></head><body><main><nav>{nav}</nav><h1>{esc(title)}</h1>"
            f"<p class='sub'>{esc(sub)}</p>{body}</main></body></html>")


def cmd_html(a):
    """Default: the share pages (scripts/share/). --check: validate them. --classic: the old three-page generator."""
    if a.classic:
        return cmd_html_classic(a)
    root = find_root(a.path)
    script = SKILL_DIR / "scripts" / "share" / ("validate_share.py" if a.check else "build_share.py")
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, str(script), str(root)], env=env)
    if r.returncode:
        sys.exit(r.returncode)
    if not a.check:
        print(f"wrote the pages into {root / 'html'} (start-here.html first); add --check to validate them")


def cmd_html_classic(a):
    root = find_root(a.path)
    docs, F = run_checks(root)
    by_id = {d.id: d for d in docs}
    gates = read_gates(docs)
    outdir = root / "html"
    outdir.mkdir(exist_ok=True)
    brief = by_id.get("BRIEF")
    name = brief.title if brief else root.name
    today = datetime.date.today().isoformat()

    def fix_for(d):
        def fx(href):
            base = (root / d.rel).parent
            tgt = os.path.normpath(base / href.split("#")[0])
            frag = "#" + href.split("#")[1] if "#" in href else ""
            return os.path.relpath(tgt, outdir).replace(os.sep, "/") + frag
        return fx

    def body_of(did, empty="Not written yet."):
        d = by_id.get(did)
        if not d:
            return f"<p class='missing'>{esc(empty)}</p>"
        body = re.sub(r"\A\s*# .*\n", "", d.body)  # the page section supplies the title
        return md_to_html(body, fix_for(d))

    def doc_section(did, title, empty="Not written yet."):
        d = by_id.get(did)
        meta = f"<span class='chip'>{d.status}</span><span class='chip'>v{d.version}</span>" if d else ""
        return f"<h2>{esc(title)} {meta}</h2>" + body_of(did, empty)

    def cards(kind, empty):
        ds = sorted((d for d in docs if d.kind == kind), key=lambda d: d.id)
        if not ds:
            return f"<p class='missing'>{esc(empty)}</p>"
        parts = []
        for d in ds:
            href = os.path.relpath(root / d.rel, outdir).replace(os.sep, "/")
            extra = ""
            for sec in ("Who decides", "Quality bar", "Result", "Choice"):
                t = section(d.body, sec)
                if t and not is_blank(t):
                    extra += f"<p><strong>{sec}:</strong> {inline(t.splitlines()[0])}</p>"
                    break
            conf = f"<span class='chip'>{d.meta.get('confidence')}</span>" if d.meta.get("confidence") else ""
            parts.append(f"<div class='card'><h3><a href='{href}'>{esc(d.title)}</a></h3>"
                         f"<span class='chip'>{d.id}</span><span class='chip'>{d.status}</span>{conf}"
                         f"<p>{inline(d.summary)}</p>{extra}</div>")
        return "<div class='grid'>" + "".join(parts) + "</div>"

    # ---- overview
    ov = ["<h2>Status by layer</h2><div class='tw'><table><thead><tr><th>Layer</th><th>Name</th><th>Gate</th><th>Docs</th></tr></thead><tbody>"]
    for layer, nm in LAYERS.items():
        st = gates.get(layer, ("not-started",))[0]
        n = sum(1 for d in docs if d.layer == layer and d.kind != "gates")
        ov.append(f"<tr><td>{layer}</td><td>{nm}</td><td>{st}</td><td>{n}</td></tr>")
    ov.append("</tbody></table></div>")
    ov.append(doc_section("BRIEF", "The feature in plain words"))
    ov.append("<h2>Worked cases</h2>" + cards("case", "No cases yet. Hand-write 2-3 real ones first."))
    ov.append(doc_section("GLOSSARY", "Words we use"))
    ov.append("<h2>Decisions</h2>" + cards("decision", "No decisions recorded yet."))
    oi = open_items(docs)
    ov.append("<h2>Open questions</h2>")
    if oi["questions"]:
        ov.append("<div class='tw'><table><thead><tr><th>ID</th><th>Question</th><th>Owner</th><th>Recommended answer</th></tr></thead><tbody>")
        for q in oi["questions"]:
            ov.append(f"<tr><td>{esc(q.get('id',''))}</td><td>{inline(q.get('question',''))}</td><td>{inline(q.get('owner',''))}</td><td>{inline(q.get('recommended answer',''))}</td></tr>")
        ov.append("</tbody></table></div>")
    else:
        ov.append("<p>None open.</p>")
    sets = {}
    for d in docs:
        for s in d.read_sets:
            sets.setdefault(s, []).append(d)
    ov.append("<h2>Reading paths</h2><p class='sub'>Open only the path that matches what you are doing.</p>")
    for s in sorted(sets, key=lambda x: list(READ_SET_PURPOSE).index(x) if x in READ_SET_PURPOSE else 99):
        ov.append(f"<h3>{esc(s)}: {esc(READ_SET_PURPOSE.get(s, 'custom'))}</h3><ul>")
        for d in sorted(sets[s], key=lambda d: (d.layer if d.layer is not None else 99, str(d.rel))):
            href = os.path.relpath(root / d.rel, outdir).replace(os.sep, "/")
            ov.append(f"<li><a href='{href}'>{esc(d.title)}</a>: {inline(d.summary)}</li>")
        ov.append("</ul>")
    ov.append("<h2>Every document</h2><div class='tw'><table><thead><tr><th>ID</th><th>Title</th><th>Layer</th><th>Status</th><th>Summary</th></tr></thead><tbody>")
    for d in sorted(docs, key=lambda d: str(d.rel)):
        href = os.path.relpath(root / d.rel, outdir).replace(os.sep, "/")
        ov.append(f"<tr><td>{d.id}</td><td><a href='{href}'>{esc(d.title)}</a></td><td>{d.layer}</td><td>{d.status}</td><td>{inline(d.summary)}</td></tr>")
    ov.append("</tbody></table></div>")
    sub = f"Generated {today} from the markdown docs. Edit the docs, not this page."
    (outdir / "overview.html").write_text(render_page(name, sub, "overview.html", "\n".join(ov)), encoding="utf-8")

    # ---- flows
    fl = [doc_section("FLOW-USER", "User flow, with re-entry points"),
          doc_section("ARTIFACTS", "Artifacts and what goes stale"),
          doc_section("FLOW-SYSTEM", "System flow"),
          "<h2>Components</h2>" + cards("component", "No components yet (layer 6)."),
          doc_section("CROSSCUT", "Cross-cutting concerns")]
    (outdir / "flows.html").write_text(render_page(name + ": flows and components", sub, "flows.html", "\n".join(fl)), encoding="utf-8")

    # ---- plan
    pl = [doc_section("RISKS", "Risks and unknowns"),
          "<h2>Spikes</h2>" + cards("spike", "No spikes yet."),
          "<h2>Contracts</h2>" + cards("contract", "No contracts yet (layer 9)."),
          doc_section("PLAN", "Implementation plan"),
          "<h2>Slices</h2>" + cards("slice", "No slices started."),
          doc_section("CHANGELOG", "Change log")]
    (outdir / "plan.html").write_text(render_page(name + ": plan and risks", sub, "plan.html", "\n".join(pl)), encoding="utf-8")
    print(f"wrote {', '.join(f for f, _ in PAGES)} in {outdir}")


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init", help="create a workspace")
    p.add_argument("path")
    p.add_argument("--name", required=True, help="feature name")
    p.add_argument("--size", choices=["small", "medium", "large"], default="medium")
    p.add_argument("--mode", choices=["new", "brownfield", "rescue", "change", "tiny"], default="brownfield")
    p.set_defaults(fn=cmd_init)
    p = sub.add_parser("new", help="add a doc from a template")
    p.add_argument("path")
    p.add_argument("kind", choices=sorted(NEW_KINDS))
    p.add_argument("title")
    p.add_argument("--id", help="choose the id (for example SL-00 or K-billing)")
    p.add_argument("--layer", type=int, help="the layer this doc belongs to (decisions default to 3)")
    p.set_defaults(fn=cmd_new)
    p = sub.add_parser("init-stage", help="create a stage's template docs if missing")
    p.add_argument("path")
    p.add_argument("stage", choices=sorted(STAGE_DOCS))
    p.set_defaults(fn=cmd_init_stage)
    p = sub.add_parser("find", help="list planning workspaces under a folder")
    p.add_argument("path", nargs="?", default=".")
    p.set_defaults(fn=cmd_find)
    p = sub.add_parser("dep", help="add a pinned dependency to a doc")
    p.add_argument("path")
    p.add_argument("target", help="the doc that depends")
    p.add_argument("dep", help="the doc or table-row id it rests on")
    p.set_defaults(fn=cmd_dep)
    p = sub.add_parser("set", help="edit a doc's front matter (not id, version, depends_on)")
    p.add_argument("path")
    p.add_argument("target", help="the doc id")
    p.add_argument("--summary")
    p.add_argument("--status", help="/".join(sorted(STATUSES)))
    p.add_argument("--confidence", help="/".join(sorted(CONFIDENCE)))
    p.add_argument("--field", action="append", metavar="KEY=VALUE", help="any other key; lists as [a, b]; repeatable")
    p.set_defaults(fn=cmd_set)
    p = sub.add_parser("section", help="replace (or append) the body under one ## heading")
    p.add_argument("path")
    p.add_argument("target", help="the doc id")
    p.add_argument("heading", help="the ## heading title, without the ##")
    p.add_argument("--file", required=True, help="file with the new text, or - for stdin")
    p.set_defaults(fn=cmd_section)
    for nm, fn, h in (("status", cmd_status, "where are we"), ("index", cmd_index, "write INDEX.md")):
        p = sub.add_parser(nm, help=h)
        p.add_argument("path")
        p.set_defaults(fn=fn)
    p = sub.add_parser("html", help="write the shareable HTML pages into <ws>/html/ (see references/share-pages.md)")
    p.add_argument("path")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--check", action="store_true", help="validate the generated pages and print the report; exit 1 on FAIL")
    g.add_argument("--classic", action="store_true", help="write the old three flat pages (overview, flows, plan) instead")
    p.set_defaults(fn=cmd_html)
    p = sub.add_parser("check", help="lint the workspace")
    p.add_argument("path")
    p.add_argument("-v", "--verbose", action="store_true")
    p.set_defaults(fn=cmd_check)
    p = sub.add_parser("read-set", help="docs for one purpose, or one doc and what it rests on")
    p.add_argument("path")
    p.add_argument("target", help="a reading path name or a doc id")
    p.add_argument("--deep", action="store_true", help="follow dependencies all the way down")
    p.add_argument("--paths", action="store_true", help="print paths only")
    p.set_defaults(fn=cmd_read_set)
    p = sub.add_parser("bump", help="record that a doc's meaning changed (version + 1)")
    p.add_argument("path")
    p.add_argument("target")
    p.set_defaults(fn=cmd_bump)
    p = sub.add_parser("pin", help="after checking a doc still holds, update its dependency pins")
    p.add_argument("path")
    p.add_argument("target")
    p.set_defaults(fn=cmd_pin)
    p = sub.add_parser("stage", help="stage readiness, or every stage and which is next")
    p.add_argument("path")
    p.add_argument("name", nargs="?")
    p.set_defaults(fn=cmd_stage)
    p = sub.add_parser("gate", help="set a layer's gate status in gates.md")
    p.add_argument("path")
    p.add_argument("layer", type=int)
    p.add_argument("status", choices=sorted(GATE_STATUSES))
    p.add_argument("--evidence")
    p.add_argument("--notes")
    p.add_argument("--no-promote", action="store_true", help="do not mark the layer's draft docs agreed")
    p.set_defaults(fn=cmd_gate)
    p = sub.add_parser("impact", help="docs that name or rest on a doc or table row")
    p.add_argument("path")
    p.add_argument("target")
    p.add_argument("--deep", action="store_true", help="also follow whole-doc dependencies further (broad)")
    p.set_defaults(fn=cmd_impact)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
