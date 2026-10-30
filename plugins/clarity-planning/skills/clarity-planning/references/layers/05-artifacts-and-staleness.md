# Layer 5: Artifacts and staleness

**Answers:** Which intermediate results exist? Who makes each? What can the user do to it? What does it depend on? What makes it stale, and what happens then? Where is it stored?
**Prevents:** One-shot builds. If intermediate results are not stored, objects the user can act on, nothing can run alone, partial redo is impossible, and individual pieces cannot be built, tested or refined separately. This layer is where the product's real shape appears.
**Output:** `30-behavior/artifacts.md`.
**Read first:** The user flow, especially the re-entry table (`wsctl.py read-set <ws> review`).

## How to generate

1. **One row per result a re-entry point touches.** Start from the re-entry table. Add results the system itself needs to reuse (a computed pack, a resolved list) even if the user never sees them.
2. **Fill each column honestly.** Produced by (a component, or a person or outside system), user can (view, edit, pick, regenerate, skip), depends on (other artifacts, plus outside data that changes), goes stale when (precisely: which input changing), what happens when stale, stored where.
3. **Walk the staleness rules like a user.** For each artifact ask: if the user edits it, what built on it is now wrong? If an upstream artifact is regenerated, which downstream ones must be too? If outside data changes, which artifact quietly goes out of date?
4. **Look for hidden decisions.** Cells that are hard to fill are the point. Examples: "if the user corrects the amount after approval, is the approval void?"; "if the summary is regenerated, are insights computed from the old summary still valid?". Each is a decision; open a decision doc and note it under "Decisions found by this table".
5. **Count the logic as an input.** An artifact made by rules, a prompt or a model also goes stale when that logic changes (a new rule set, prompt or model version). Record the version each artifact was made with, and say whether a logic change re-runs old artifacts or only new ones.
6. **Decide stale behavior per rule:** regenerate automatically, mark stale and ask, or leave alone (and say why that is safe). A stale rule with no decided behavior is a bug waiting.
7. **Decide where each is stored and who owns it.** If the system is stateless between runs, every user-actionable artifact must be stored by something that persists, and sent back with the next request. Say which system, and what is kept (do not store sensitive content you do not need).
8. **Avoid false dependencies.** If an artifact depends on a sibling only out of habit (a writer reading a draft it does not need), cut the dependency so one part can be regenerated without invalidating the other.

## Starter questions

- "If you fix this, what else should change? What should stay?"
- "If we regenerate just this part, do we want the downstream parts regenerated too?"
- "Does this result age? How quickly does the data behind it change?"
- "Does it matter if someone sees yesterday's version?"
- "Who may change this, and does their change need to be remembered?"

## Gate (layer 5 passed when)

- [ ] Every re-entry in layer 4 maps to an artifact.
- [ ] Every artifact has a producer, a "user can", its dependencies and its stale rule filled.
- [ ] Every stale rule has a decided behavior.
- [ ] Hidden decisions the table exposed are written up as decisions.
- [ ] Storage and ownership of every user-actionable artifact is named.

## Depth

small: skip. medium: a table of the user-actionable artifacts with stale rules. large: every artifact, including internal ones, with stored-where and ownership, and a pass for false dependencies.

## When it goes sideways

- **Too many artifacts.** Keep only what a user acts on, a component needs to run alone, or staleness depends on. Merge the rest.
- **Too few** (everything is "the result"). Ask the four re-entry questions again for the weakest step.
- **A stale rule cannot be decided** (needs a policy). Open a question for the owner with your recommended behavior; default to "mark stale and ask".
- **Outside data changes under you** (live records, time-based). Mark the artifact "ages"; add an age limit or a refresh trigger; say what the user sees when it is old.
- **The artifact would hold sensitive data.** Decide what must be stored versus recomputed; store hashes or ids where you can.
- **The existing system stores nothing between steps.** That is a finding: adding storage is part of the plan (layer 10).

## Hands off to

Layer 6: one component per artifact, runnable alone.
