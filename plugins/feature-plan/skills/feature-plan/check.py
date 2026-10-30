#!/usr/bin/env python3
"""Checker for a feature-plan workspace. Reports; never edits.

Usage: python3 check.py <workspace>
Exit code 1 if there is any error.
"""
import re
import sys
from pathlib import Path

CORE = ["outcome.md", "behaviour.md", "design.md", "plan.md"]
BUDGET = {"small": 60, "medium": 120, "large": 200}  # lines per core file
SLICE_BUDGET = 80
DESIGN_EXTRA = 100  # field tables may run longer
ID = re.compile(r"\b((?:[A-Z]{1,6})-\d{1,3})\b")
DEF_ROW = re.compile(r"^\|\s*\**((?:[A-Z]{1,6})-\d{1,3})\**\s*\|")
DEF_HEAD = re.compile(r"^#{1,6}\s+((?:[A-Z]{1,6})-\d{1,3})\b")
SLICE_NEEDS = ["Run", "You see", "Pass when", "Owner"]
SLICE_SPEC_NEEDS = ["Files to change", "Non-goals", "Ready"]

errors, warnings = [], []


def err(f, msg):
    errors.append(f"ERROR   {f}: {msg}")


def warn(f, msg):
    warnings.append(f"warning {f}: {msg}")


def read(p):
    return p.read_text(encoding="utf-8").splitlines()


def status_of(lines):
    for l in lines[:12]:
        m = re.match(r"^Status:\s*(\w+)", l)
        if m:
            return m.group(1).lower()
    return None


def main(ws):
    ws = Path(ws)
    start = ws / "start-here.md"
    if not start.exists():
        err("start-here.md", "missing")
        return report()
    sl = read(start)
    size = "medium"
    for l in sl:
        m = re.match(r"^Size:\s*(\w+)", l)
        if m:
            size = m.group(1).lower()
    if size not in BUDGET:
        err("start-here.md", f"size '{size}' is not small, medium or large")
        size = "medium"
    if len(sl) > 40:
        err("start-here.md", f"{len(sl)} lines; limit is 40")

    docs = [ws / c for c in CORE if (ws / c).exists()]
    core_limit = 1 if size == "small" else 4
    if len(docs) > core_limit:
        err("workspace", f"{len(docs)} core documents; limit for {size} is {core_limit}")

    for p in ws.rglob("*.md"):
        if re.match(r"^\d", p.name):
            err(p.name, "file name starts with a number; name files for what they hold")

    log_text = (ws / "log.md").read_text(encoding="utf-8") if (ws / "log.md").exists() else ""
    defined, used_in = {}, {}

    for p in docs + sorted((ws / "slices").glob("*.md") if (ws / "slices").exists() else []):
        lines = read(p)
        name = str(p.relative_to(ws))
        is_slice = p.parent.name == "slices"
        limit = SLICE_BUDGET if is_slice else BUDGET[size] + (DESIGN_EXTRA if p.name == "design.md" and size == "large" else 0)
        if len(lines) > limit:
            err(name, f"{len(lines)} lines; budget is {limit}")
        st = status_of(lines)
        if st not in ("draft", "approved", "done"):
            err(name, "missing 'Status: draft', 'approved' or 'done' near the top")
        if st == "done" and not is_slice:
            err(name, "only a slice can be Status: done")
        if not any(l.startswith("In plain words:") for l in lines[:10]):
            err(name, "missing the 'In plain words:' opener near the top")
        text = "\n".join(lines)
        if st in ("approved", "done"):
            if re.search(r"TODO|\{\{", text):
                err(name, "approved or done but contains TODO or an unfilled {{placeholder}}")
            if name not in log_text and p.name not in log_text:
                err(name, "approved but log.md records no yes for it")
        elif re.search(r"\{\{", text):
            warn(name, "has unfilled {{placeholders}}")

        for i, l in enumerate(lines):
            m = DEF_ROW.match(l) or DEF_HEAD.match(l)
            if m:
                defined.setdefault(m.group(1), []).append(name)
        for m in ID.finditer(text):
            used_in.setdefault(m.group(1), set()).add(name)

        # tables that list who reads a field must also say why
        for i, l in enumerate(lines):
            if l.startswith("|") and "Read by" in l and "Why" not in l:
                err(name, f"line {i+1}: table has 'Read by' but no 'Why' column")
            if l.startswith("|") and "Why" in l and i + 2 < len(lines):
                cols = [c.strip() for c in l.strip("|").split("|")]
                wi = next((k for k, c in enumerate(cols) if c.startswith("Why")), None)
                if wi is not None:
                    j = i + 2
                    while j < len(lines) and lines[j].startswith("|"):
                        cells = [c.strip() for c in lines[j].strip("|").split("|")]
                        if len(cells) > wi and not cells[wi]:
                            err(name, f"line {j+1}: field row has an empty Why")
                        j += 1

        if p.name == "plan.md":
            for need in SLICE_NEEDS:
                if need not in text:
                    err(name, f"no slice states '{need}'")
        if is_slice:
            for need in SLICE_SPEC_NEEDS:
                if need not in text:
                    err(name, f"slice spec lacks '{need}'")
            if st == "done":
                rep = text.split("## Completion report", 1)[-1] if "## Completion report" in text else ""
                if not rep or "Not built yet" in rep:
                    err(name, "Status: done but the completion report is missing or not filled in")
                elif not re.search(r"(?i)remaining concerns", rep):
                    err(name, "completion report lacks 'Remaining concerns'")

    for i, files in defined.items():
        if len(set(files)) > 1 or len(files) > 1:
            err(i, f"id defined more than once ({', '.join(files)})")
    for i in used_in:
        if i not in defined and not re.match(r"^(CASE|SL)-\d", i):
            warn(i, f"id used in {', '.join(sorted(used_in[i]))} but never defined in a table row or heading")
    report()


def report():
    for l in errors + warnings:
        print(l)
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1])
