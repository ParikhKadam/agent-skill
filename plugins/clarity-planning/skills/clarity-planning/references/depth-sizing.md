# Depth and sizing

Process should shrink with the feature. A planning method that makes a one-field change take a week will be abandoned, and rightly. Size first, then spend depth where being wrong is expensive.

## Pick a size

| Size | Typical | Layers | Effort shape |
|---|---|---|---|
| **small** | One field, one screen, a small rule, a bug-sized change with a design question | 0, 1, 4, 10 in a few lines each | Minutes to an hour. One case, the flow, a plan with an exit check |
| **medium** | A feature in an existing product with a few steps and some data questions | All layers, short | A few sessions. One spike on the top risk |
| **large** | A new subsystem, anything with outside data or another team, anything where a model decides something, anything hard to undo | All layers in full | Several sessions. A spike per top risk, contracts with stubs, component quality bars |

## Tripwires: upsize when any is true

- You depend on data or a system you have not looked at.
- A second team must build or agree something.
- A language model or other judgment-by-software decides something users rely on.
- The action is irreversible or touches money, access or other people's data.
- Users will want to fix, redo or skip intermediate steps.
- The first guess at scope has already doubled.

One tripwire moves small to medium. Two or more, or any of the first three combined with irreversibility, means large.

## Depth by layer and size

| Layer | small | medium | large |
|---|---|---|---|
| 0 Intake | restate in a sentence | brief plus existing-system notes | full inventory of what exists |
| 1 Outcome | 1 case | 2-3 cases | 3+ cases, including an awkward one, and a real example of each kind of input |
| 2 World | skip unless data is unseen | facts register for what the cases reached for | full register, sampled real data, imposed versus chosen |
| 3 Risks | name the top risk in the brief | rank assumptions, one spike | rank, spike each top risk with a bar, decision owners |
| 4 User flow | story in a few lines | story, alternate paths, re-entry table | all roles, failures, leaving and returning |
| 5 Artifacts | skip | table, short | full table with stale behaviors decided |
| 6 Components | skip | one line per component | a card per component with bar and test set |
| 7 System flow | skip | numbered flow, failure table | plus every start point, duplicates, concurrency |
| 8 Cross-cutting | skip, but state anything sensitive | verdict per concern | each concern with its consequence, authorization derived from actors and artifacts |
| 9 Contracts | only if a boundary exists | examples for each boundary | examples, rules, versioning, stubs both sides |
| 10 Plan | one slice with an exit check | skeleton plus slices | skeleton, slices with flags, deferred list, rollout |
| 11 Change | skip | change log | change log plus `impact` practice |

## How to allocate depth within a size

Spend on **cost of being wrong times uncertainty**. A layer that is cheap to be wrong about (an obvious, reversible flow) gets a few lines. A layer where an error is found late and costs a rebuild (a fact about an outside system, who may see what, what is irreversible) gets the spike and the evidence.

## Thin is fine when nothing is verified

Large size means every layer runs, not that every doc is long. When you have no access to data, code or the other team, write the doc at the depth the evidence supports: a short register of what is assumed and how to check it, flagged `unknown` or `inferred`, beats a long doc of guesses. Say in the doc what would make it thicker (access, a spike, an owner's answer).

## Skipping a layer on purpose

Skipping is fine when the size says so. Mark the gate `skipped` in `90-log/gates.md` with a reason; for example "layer 5 skipped: no intermediate results the user can act on". A silent skip is the failure; a recorded skip is a decision.

## Right-sizing in practice

- Start small and let the tripwires pull you up. Most features are medium.
- Never skip layer 1 (cases) or layer 10 (an exit check per slice), even on a tiny change: those two are what keep a small change from becoming a surprise.
- If the user is time-pressed, say which layers you are compressing and what risk that leaves, once.
- If planning has stalled for more than a session on one layer, size down, record the open items, and move to the plan; the build will answer some of them.
