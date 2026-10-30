---
name: plan-build
description: Stage 4 of clarity-first planning, the build plan. Turns the agreed design into a staged implementation plan. First a walking skeleton where every stored result exists and every component runs alone on stubs, end to end on the hand-written cases. Then slices in risk order, each replacing one stub, with an exit check on fixed inputs, a flag or rollback, and an owner. Contracts are frozen first, there is a deferred list with revisit triggers, and test sets are built early. Use when the user asks for an implementation plan, build order, phases, milestones, slices, tickets or rollout plan for a feature whose design is settled (or explicitly wants to start here), or wants to avoid a one-shot build. Part of the clarity-planning family; shared tools and guides live in the clarity-planning skill.
---

# Stage: Build plan (layer 10)

This stage answers: **in what order do we build, and how do we know each step works?** The aim is confidence at every stage: nothing lands as one untestable piece, and any disagreement between the design and the build is settled by a measurement on fixed inputs.

Read `../clarity-planning/references/stage-protocol.md` first (relative to this skill's folder) and follow it: find the workspace, run `wsctl.py stage <ws> build`, handle "not ready", load only what this stage needs, get explicit approval at the gate, close the stage.

## Rests on (from earlier stages)

Risks (slice order), components with their quality bars and test sets (exit checks), artifacts (what the skeleton must store), the system flow (start points the skeleton must run), contracts (frozen first, stubs in the skeleton), and the cases (what the skeleton runs end to end).

## Before planning: ask how they want the plan

Ask in ONE round, before drafting, so preferences are not discovered at review. Follow `../clarity-planning/references/session-protocol.md`, "Make every question answerable on its own": plain words, define terms, one example, what each answer changes, a recommended default. About five questions:

1. **Simple first or riskiest first?** A thin, useful version first (with evidence slices ahead of it), or the hardest part first. Changes the order of slices. Default: simple first, with evidence slices ahead, unless one unknown could make everything else worthless.
2. **Who builds what?** Teams or agents, and whether to split into tracks (for example backend, AI service, frontend) so slices run in parallel. Changes whether the plan has tracks and join slices. Default: one track per team that builds independently.
3. **How is change handled?** Is rework acceptable, or should changes be additive and made in small update steps? Do you expect the schema or contracts to change during the build? Default: additive changes and small update steps; expect the schema to change.
4. **Rollout style.** Flags, a pilot group, a cutover; what stays the default for everyone else. Default: behind a flag, pilot group first, old behaviour stays default.
5. **Tickets or not, and how big is a slice?** Example: one slice is about a few days of work with one exit check. Default: no tickets until asked; slices of a few days.

The answers go into the plan's first section and into a decision doc. Unanswered ones proceed on the defaults, marked hypothesis.

## What matters most (guide: `../clarity-planning/references/layers/10-implementation-plan.md`)

0. **Gate conditions first:** `wsctl.py status` lists conditions from gates passed with conditions; each becomes an early slice (usually `SL-00`, created with `wsctl.py new <ws> slice "..." --id SL-00`).
1. **Walking skeleton:** dumbest version of every step, real storage of every artifact, every component runnable alone, contracts exercised against stubs, end to end on the hand-written cases. Write its exit check.
2. **Slices in risk order:** each replaces one stub, proves one claim, and has an **exit check written before the work** (inputs, number, threshold), a flag or rollback, an owner, and what it rests on.
3. **Contracts first:** boundary agreements at the front.
4. **Test sets as slice zero:** hand-written cases first, recorded real inputs next.
5. **Deferred list:** each item with why it can wait and what would make us revisit it.
6. **Rollout:** flags, pilot users, how trouble is noticed, how to switch off.
7. **Tracks and joins:** one track per team, each builds against stubs and shared fixtures; a join slice per phase proves the tracks fit together.
8. **Start with what cannot be added later; defer what can:** versions of outputs, audit rows, ids and schema/logic versions exist from day one; the rest waits.
9. **Changes are updates:** classify hard-to-change (contracts, ids, names) versus easy-to-change (tables, JSON contents, screens). Database changes go add, then switch, then drop. Each change is a slice with an exit check; the plan is not reopened.

In rescue mode, the existing build is the skeleton: add stored artifacts and exit checks around it rather than starting over.

If the user wants tickets, convert slices one to one, with exit checks as acceptance criteria. Do not file them in a tracker unless asked.

## Produces

`50-plan/implementation-plan.md` and `50-plan/slices/SL-*.md` (via `wsctl.py new <ws> slice "<title>"`) for slices about to start.

## Close

When layer 10 is passed, close per the stage protocol. Point out that **`plan-change`** handles anything learned during the build that contradicts the plan.
