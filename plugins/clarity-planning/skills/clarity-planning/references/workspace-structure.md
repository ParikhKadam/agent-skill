# Workspace structure

A feature's planning lives in one folder of many small docs, grouped by **what a reader wants to know**, not by when it was written. Nobody should read everything; the structure, the reading paths and the index exist so a reader opens only what they need.

Default location: `docs/planning/<feature-slug>/` in the project repo (versioned with the code). If the team keeps design docs elsewhere, use that and record the path in the brief.

## The tree

```
<feature-slug>/
├── INDEX.md                         generated: every doc, summary, status, what it rests on
├── html/                            generated: start-here.html, story, system, contracts, decisions-and-risks, build-plan, everything
├── html-src/authored.json           authored data for the html pages (diagram data, glosses); see share-pages.md
├── 00-start/                        START HERE: what and why, in plain words
│   ├── brief.md                     outcome, who acts, distrust, valuable part, non-goals, size
│   ├── glossary.md                  the users' words and what they mean
│   └── cases/case-01.md ...         hand-written real cases with the ideal result
├── 10-world/                        THE WORLD: what is true outside our design
│   ├── facts-register.md            each fact: where it lives, who writes it, reliability, access
│   ├── existing-system.md           what exists, reuse, surprises
│   ├── constraints.md               imposed versus chosen
│   └── divergence.md                rescue mode only: spec versus build, and how to decide
├── 20-risks-and-decisions/          RISKS AND DECISIONS
│   ├── risks.md                     ranked assumptions with the plan for each
│   ├── open-questions.md            who must answer what, with our recommended answer
│   ├── spikes/S-001-*.md            one test, its bar and its result
│   └── decisions/D-001-*.md         one decision per file, with alternatives and tripwire
├── 30-behavior/                     BEHAVIOR: what users and the system do
│   ├── user-flow.md                 the story, paths, re-entry points
│   ├── artifacts.md                 stored intermediate results and what goes stale
│   └── system-flow.md               how components run from any start point, and failure rules
├── 40-design/                       DESIGN
│   ├── components/C-*.md            one component per file: inputs, output, who decides, bar
│   ├── cross-cutting.md             verdict per concern (or one file per concern if large)
│   └── contracts/K-*.md             one boundary per file, with real example messages
├── 50-plan/                         PLAN
│   ├── implementation-plan.md       skeleton, slices in risk order, deferred, rollout
│   └── slices/SL-01-*.md            one file per slice once it starts
└── 90-log/                          LOG
    ├── gates.md                     layer gates with evidence
    ├── change-log.md                every requirement change and what it reopened
    └── sessions.md                  what each session covered and the next step
```

Folders group docs by purpose. Layer numbers (0-11) describe the order work happens. A doc declares both: its folder is where it lives; its `layer:` says when it is worked on. Folder 30 holds layers 4, 5 and 7 because a reader wants all the behavior together.

`init` creates the logs and the clarity stage's docs only; each later stage creates its own with `wsctl.py init-stage <ws> <stage>`, so unstarted layers do not fill the workspace with templates. Add the rest with `wsctl.py new <ws> <decision|spike|component|contract|case|slice> "<title>"`.

## Front matter (required on every doc)

```yaml
---
id: C-matcher
title: Matcher
layer: 6
kind: component
status: draft
version: 2
updated: 2026-10-28
summary: Picks the supplier and purchase order for an invoice; code first, a person for the leftovers
depends_on: [ART-02@1, D-003@2]
read_sets: [build-component, review]
---
```

| Field | Rule |
|---|---|
| `id` | Unique and stable. Never reuse or renumber. Conventions: `BRIEF`, `CASE-nn`, `GLOSSARY`, `FACTS`, `EXISTING`, `CONSTRAINTS`, `RISKS`, `QUESTIONS`, `S-nnn`, `D-nnn`, `FLOW-USER`, `ARTIFACTS`, `FLOW-SYSTEM`, `C-<slug>`, `CROSSCUT`, `K-<slug>`, `PLAN`, `SL-nn`, `GATES`, `CHANGELOG`, `SESSIONS`. Rows inside docs use `F-nn` (facts), `X-nn` (constraints), `R-n` (risks), `Q-n` (questions), `ART-nn` (artifacts) |
| `layer` | 0-11, the layer this doc belongs to |
| `kind` | `brief`, `case`, `glossary`, `fact`, `world`, `risk`, `question`, `spike`, `decision`, `flow`, `artifact`, `component`, `crosscut`, `contract`, `plan`, `slice`, `gates`, `log`. The checker uses it |
| `status` | `draft`, `agreed`, `pending` (waits on someone: an unrun spike, a contract the other side has not seen), `stale`, `superseded`, `parked`. Passing a gate promotes the layer's `draft` docs to `agreed` |
| `version` | Integer. Bump when the **meaning** changes, not for typos |
| `summary` | One line a reader can use to decide whether to open the doc. This is what the index shows, so write it for a stranger |
| `depends_on` | Doc ids or table-row ids (`ART-02`, `F-07`) this one rests on, pinned to the version it was written against (`ID@n`; a row is pinned to its doc's version). Prefer row ids: they make `impact` lists short. Add with `wsctl.py dep` |
| `read_sets` | Reading paths it belongs to: `onboard`, `understand`, `review`, `build-component`, `contract`, `change-request` (or your own) |
| `confidence` | Decisions only: `decided`, `hypothesis`, `unknown`, `measured` |

Keep the front matter plain: one `key: value` per line, lists in square brackets, no comments, no nested structures (the tool reads a simple subset).

## Staleness by pins

`depends_on: [D-003@2]` says "I was written when D-003 was at version 2". When someone edits D-003 and bumps it to 3, `wsctl.py check` reports every doc pinned to the old version as **possibly stale**. A person (or you) then reads the dependent doc, decides if it still holds, edits if needed, and updates the pin. That is how a changed requirement finds the docs it touches without rereading everything.

Pin to what the doc **actually relies on**: a component rests on the artifacts it reads and the decisions that shaped it, not on everything.

## Commands

```
python3 <skill>/scripts/wsctl.py init <path> --name "<Feature>" --size small|medium|large --mode new|brownfield|rescue|change|tiny
python3 <skill>/scripts/wsctl.py find [<folder>]                       # list planning workspaces
python3 <skill>/scripts/wsctl.py init-stage <ws> components|flows|build  # create a stage's docs
python3 <skill>/scripts/wsctl.py new <ws> decision|spike|component|contract|case|slice "<title>" [--id SL-00] [--layer 5]
python3 <skill>/scripts/wsctl.py dep <ws> <id> <dep-id>                 # add a pinned dependency (doc or row id)
python3 <skill>/scripts/wsctl.py set <ws> <id> [--summary T] [--status S] [--confidence C] [--field k=v ...]   # edit front matter only; sets updated, never version
python3 <skill>/scripts/wsctl.py section <ws> <id> "<heading>" --file FILE|-   # replace (or append) the body under one ## heading; rest untouched
python3 <skill>/scripts/wsctl.py status <ws>             # layer gates, open items, possibly-stale docs
python3 <skill>/scripts/wsctl.py check <ws> [-v]         # lint: broken links, missing owners, unmet gates
python3 <skill>/scripts/wsctl.py index <ws>              # write INDEX.md
python3 <skill>/scripts/wsctl.py read-set <ws> <set|id> [--deep] [--paths]
python3 <skill>/scripts/wsctl.py impact <ws> <id> [--deep] # docs that rest on or mention a doc or row (ART-02, F-07, Q-1)
python3 <skill>/scripts/wsctl.py stage <ws> [<stage>]     # which stage is next; is a stage ready
python3 <skill>/scripts/wsctl.py gate <ws> <layer> <status> [--evidence ...] [--notes ...]   # passed needs evidence; skipped needs a reason
python3 <skill>/scripts/wsctl.py bump <ws> <id>          # its meaning changed: version + 1, lists dependents
python3 <skill>/scripts/wsctl.py pin <ws> <id>           # after reading it against the change: update its pins
python3 <skill>/scripts/wsctl.py html <ws> [--check|--classic]   # the share pages (--check validates; --classic: old overview, flows, plan)
```

Run `check`, `index` and `html` at the end of a session. `check` exits non-zero only for errors (broken ids, bad status), not for warnings.

## What the checker catches (so you can see them early)

- A re-entry point with no artifact, or naming an artifact that does not exist.
- An artifact with no producer, or whose "user can", "depends on" or "goes stale when" is empty.
- A component with an empty "who decides", "quality bar" or "runs alone".
- A contract without both a happy-path and a failure example.
- A slice without an exit check.
- A fact with no source or no status; an open question with no owner.
- A decision with no confidence or no "what would change this".
- A layer marked passed with no evidence, or with docs still in draft.
- A doc `agreed` with TODO markers left in it.
- A doc written against an older version of something it rests on.

## The index and the html pages

`INDEX.md` is generated: status by layer, reading paths, every doc with summary and dependencies, decisions by confidence, open questions with owners, unknown facts, and a health list. Never edit it by hand.

`html/` holds the shareable pages built from the docs (self-contained, light and dark themes, diagrams generated from the docs or authored in `html-src/authored.json`): `start-here.html` first, then `story`, `system`, `contracts`, `decisions-and-risks`, `build-plan`, and `everything` on one page. What each holds, the authored data and the check: `share-pages.md`.

They are for people who will not open markdown. They are not published anywhere unless the user asks; do not publish them as artifacts or upload them.

## When to split, merge, or rename

- **Split a doc** when different readers need different parts or it passes roughly 150 lines. Move detail into child docs, leave a summary and links, assign reading paths.
- **Merge** when two docs are always read together and neither stands alone.
- **One decision per file**, so each has its own history and tripwire. Tiny reversible choices may share one "small choices" decision.
- **Never rename an id.** Rename the title and file freely; ids are what pins and links rest on. If a doc dies, set `superseded` and point to the replacement in its body.
- For a large feature, cross-cutting concerns may become a folder with one file per concern; keep `CROSSCUT` as the summary doc.

## Per-project overrides

If the project already has a docs convention (an ADR folder, a specs directory), keep the workspace folder as the home for this method and **link** to the existing docs from `existing-system.md` and the facts register rather than moving them. Do not reorganize a team's existing documentation unasked.
