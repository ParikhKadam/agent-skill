---
name: plan-flows
description: Stage 3 of clarity-first planning, covering flows and contracts. Defines the system flow as components running from any stored starting result (full runs and partial re-runs), failure, retry, duplicate and concurrency handling, a verdict for every cross-cutting concern (RBAC and permissions, tenancy, audit, encryption, retention, observability, cost, rollout), and contracts for every boundary with real happy-path and failure examples plus stubs. Use when the user asks for the system flow, sequence of steps, failure handling, idempotency, security or permissions model, audit trail, API or integration contracts, or callback formats for a feature whose components are defined (or explicitly wants to start here). Part of the clarity-planning family; shared tools and guides live in the clarity-planning skill.
---

# Stage: Flows and contracts (layers 7-9)

This stage answers: **how do the components run together from any starting point, what happens when things fail, which cross-cutting rules apply, and exactly what crosses each boundary with other teams or systems?**

Read `../clarity-planning/references/stage-protocol.md` first (relative to this skill's folder) and follow it: find the workspace, run `wsctl.py stage <ws> flows`, handle "not ready", load only what this stage needs, get explicit approval at each gate, close the stage.

## Rests on (from earlier stages)

The artifacts table and component docs (the flow is just components in dependency order from a chosen artifact), the user flow's re-entry points (each one is a start point), the facts register (what outside systems actually support: idempotency, lookups, limits), and decisions.

## The three layers and what matters most

Guide paths below are under `../clarity-planning/references/` (written `<hub>/references/` elsewhere).

| Layer | Guide | The heart of it |
|---|---|---|
| 7 System flow | `layers/07-system-flow.md` | Numbered full run, with who decides at each step. Then **every start point** from layer 4. Skips are visible gates with reason codes, and a failure is never reused as a result. Failure table, duplicates, concurrency, budgets |
| 8 Cross-cutting | `layers/08-cross-cutting.md` | Verdict for every concern. **Derive permissions** from actors × artifacts × actions. Audit what users correct or override. Keep sensitive data out of logs, traces and model inputs. Check current guidance from a primary source for payments, auth and personal data |
| 9 Contracts | `layers/09-contracts.md` | One doc per boundary with **real example messages**, one happy path and at least one failure. Rules, versioning, owners on both sides, and a stub for each side. If you cannot see the other side, write a `PROPOSAL` with invented examples labelled as such and status `pending`; the gate can pass with the condition that the owner reviews it |

Use `standard-practices.md` deliberately here: retries and duplicates, state machines, outbox, adapters and stubs, permission models, audit, tenancy. Each pattern is a hypothesis checked against the facts register.

## Produces (what the build stage reads)

`30-behavior/system-flow.md`, `40-design/cross-cutting.md`, `40-design/contracts/K-*.md` (via `wsctl.py new <ws> contract "<title>"`), plus decisions on failure behavior and permission rules. New artifacts or components discovered here (for example an audit record) go back into layers 5-6 through `plan-change`.

## Close

When layers 7-9 are passed or skipped, close per the stage protocol and ask whether to continue with the **build plan** (`plan-build`).
