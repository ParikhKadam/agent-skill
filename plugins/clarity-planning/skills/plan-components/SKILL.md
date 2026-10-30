---
name: plan-components
description: Stage 2 of clarity-first planning, covering services and components. Starts from the user flow and asks at every step where the user can see, fix, regenerate or skip. Turns each of those points into a stored intermediate result (artifact) with dependencies and staleness rules, then gives each artifact one component that runs alone, with who decides inside (code, model or person) and a quality bar. Use when the user wants to define services or components, split a pipeline into independently buildable and testable parts, support partial regeneration or manual overrides, or asks "what are the pieces?" for a feature whose clarity stage is done (or explicitly wants to start here). Part of the clarity-planning family; shared tools and guides live in the clarity-planning skill.
---

# Stage: Services and components (layers 4-6)

This stage answers: **what does the user do, where can they step in, which intermediate results must therefore exist, and what produces each one?** Components are decided by what the user can see, fix or redo, not by technical tidiness. That is what lets each piece be built, tested and refined on its own.

Read `../clarity-planning/references/stage-protocol.md` first (relative to this skill's folder) and follow it: find the workspace, run `wsctl.py stage <ws> components`, handle "not ready" by offering to go back or proceed with recorded assumptions, load only what this stage needs, get explicit approval at each gate, close the stage.

## Rests on (from the clarity stage)

The brief and cases (the ideal results are the test for every flow), the facts register and constraints (no component may assume a fact marked unknown without saying so), risks and decisions (the riskiest assumption shapes the component boundaries).

## The three layers and what matters most

Guide paths below are under `../clarity-planning/references/` (written `<hub>/references/` elsewhere).

| Layer | Guide | The heart of it |
|---|---|---|
| 4 User flow and re-entry | `layers/04-user-flow.md` | Walk a real case as a story. At **every** step ask the four questions: can the user see it, correct it, regenerate it alone, skip it? Each yes needs a stored result; list the ones ruled out |
| 5 Artifacts and staleness | `layers/05-artifacts-and-staleness.md` | One row per artifact: produced by, user can, depends on, goes stale when, what happens then, stored where. **The hard cells are the point**: they expose decisions nobody asked (if the user fixes X after Y was approved...). Cut false dependencies so one part can be redone without staling another |
| 6 Components | `layers/06-components.md` | One producer per artifact. Keep a component only if a split test holds. Each one **runs alone from stored inputs**, states who decides inside (start with code, see `ai-components.md`), and has a quality bar and test set set before building. Name the established pattern where one fits (`standard-practices.md`) as a hypothesis |

## Produces (what the next stages read)

`30-behavior/user-flow.md`, `30-behavior/artifacts.md`, `40-design/components/C-*.md` (via `wsctl.py new <ws> component "<title>"`), plus decisions the staleness table exposed.

## Close

When layers 4-6 are passed or skipped, close per the stage protocol and ask whether to continue with **flows and contracts** (`plan-flows`).
