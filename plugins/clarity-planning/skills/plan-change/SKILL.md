---
name: plan-change
description: Change protocol for a clarity-first planning workspace. Use whenever new information arrives or plans change after planning has started. First triages the update (clarification, new information that confirms, new information that contradicts, a small plan tweak, a requirement change, or a change of outcome or scope). Then reworks only what is affected, by bumping the changed doc, listing everything that rests on it, reopening the earliest layer touched, reconciling dependents and logging the change. Use when the user says something changed, a stakeholder decided differently, a spike or the build contradicted the plan, a requirement was added or dropped, or asks "what does this change affect?", at any stage. Part of the clarity-planning family; shared tools and guides live in the clarity-planning skill.
---

# Stage: Change (layer 11, any time)

This skill keeps a plan true as things change, without rewriting everything and without silently patching. Any stage skill may hand off here when it finds that an earlier stage was wrong.

Read `../clarity-planning/references/stage-protocol.md` (relative to this skill's folder) for the shared rules, and `../clarity-planning/references/layers/11-change-protocol.md` for the full procedure. The essentials:

## 1. Log, then triage

Write what arrived in `90-log/sessions.md` first so it is not lost. Then decide which kind it is and tell the user what you will touch:

| Kind | What to do |
|---|---|
| Clarification or typo | Edit. Nothing else |
| New information that confirms or sharpens | Update the row (to `measured`), `bump` if its meaning got firmer. Nothing downstream changes |
| An open question is answered | Close it and update the decision it fed. Same as our recommended default: update the docs that mention it (`impact <ws> Q-n`) from default to decided. Different: treat as contradicting |
| New information that contradicts | Treat as a change (below) |
| Small plan tweak | Edit the plan or slice; `bump` if scope or exit check changed |
| Requirement change (including a non-goal that becomes a goal) | The full protocol below, from the brief if goals or non-goals change |
| Outcome or scope change | Back to `plan-clarity` (layer 1); re-size; expect most layers to reopen |

Unsure between "confirms" and "contradicts"? Ask: does it contradict something the design decided? Replacing a default or guess with the same answer confirms; anything that forces a decision or design element to change contradicts. Unsure between a tweak and a requirement change? Ask: would a user notice? If yes, it is a requirement change.

## 2. Rework only what is affected (for contradictions and requirement changes)

1. Get the user's agreement to rework. This reopens things they approved.
2. Edit the earliest affected doc, then `wsctl.py bump <ws> <id>`.
3. `wsctl.py impact <ws> <id>` lists the docs that rest on it or mention it; it also works on table rows (`ART-02`, `F-07`, `Q-1`), which gives the shortest list. The artifacts table shows which components are untouched.
4. Reopen every layer whose docs you will change (not only the earliest): `wsctl.py gate <ws> <layer> in-progress --notes "<change>"`.
5. Read each dependent against the change, edit it if needed, then `wsctl.py pin <ws> <id>`. Never pin without reading.
6. Re-pass the reopened gates with the user's explicit yes, as in the owning stage. If the change is large, hand over to that stage skill (`plan-clarity`, `plan-components`, `plan-flows` or `plan-build`) to redo its layers.
7. Add a row to `90-log/change-log.md`: what changed and why, earliest layer, docs reopened, outcome.
8. `wsctl.py check` until no "possibly stale" remains and no passed gate shows changed evidence (re-confirm those gates with the user or reopen them), then `index` and `html`.

Leave unrelated decisions alone. If a change contradicts a decision someone argued for, show its recorded "what would change this" and ask the owner. Do not override it quietly.
