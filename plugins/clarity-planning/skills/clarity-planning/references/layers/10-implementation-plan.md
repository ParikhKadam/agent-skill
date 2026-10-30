# Layer 10: Implementation plan

**Answers:** In what order do we build, and how do we know each step works?
**Prevents:** One-shot implementation. If every part lands together, nothing can be judged until the end, and nobody can tell whether the spec or the build is better. A plan of a thin skeleton plus risk-ordered slices gives confidence at each stage.
**Output:** `50-plan/implementation-plan.md`, `slices/SL-nn-*.md` once a slice starts.
**Read first:** Components, system flow, contracts, risks, deferred items (`wsctl.py read-set <ws> review`).

## How to generate

1. **Define the walking skeleton.** The dumbest version of every step (stubs, hard-coded values, plain code) that runs **end to end on the hand-written cases** and produces the real output. Every artifact exists and is stored; every component runs alone from stored inputs; contracts are exercised against stubs. Write its exit check: which cases run, and what output proves it.
2. **Turn every gate condition into work.** Read the conditions (`wsctl.py status` lists them). Each becomes an early slice, usually slice zero (`wsctl.py new <ws> slice "..." --id SL-00`): get data access, run the pending spike, have the owner review the contract.
3. **List the slices in risk order.** Each replaces one stub with the real thing. Order by cost of being wrong times uncertainty (use layer 3): the riskiest first, plumbing last. Pair a slice with the component, the claim it proves ("matching gets 40 of 50 right with none wrong") and the artifact it fills.
4. **Write each slice's exit check before the work starts**: on stored inputs, with a number and a threshold, run by anyone. A slice is done when its check passes, not when the code merges.
5. **Give each slice a flag or rollback**, an owner, and what it rests on. Slices that depend on a boundary rest on its contract.
6. **Freeze contracts first.** Put the boundary agreements at the front of the plan.
7. **Write the Deferred list.** Each item: why it can wait, what would make us revisit it. This keeps scope visible.
8. **Test strategy.** What fixed inputs judge which slice; what is judged by a person; what the evaluation set is and who maintains it. The test set for each component is built early (slice zero).
9. **Rollout.** Flags, who sees it first, how trouble is noticed, how to turn it off, what happens to existing data.
10. **Sanity-check the order.** Could any slice be built and judged alone? If two must land together, merge them or add a stub between.
10a. **Split into tracks if more than one team builds.** One track per team or agent (for example backend, AI service, frontend). Each builds against stubs and shared fixtures from the contracts; add a join slice per phase that proves the tracks fit together.
10b. **Start with what cannot be added later; defer what can.** Versions of outputs, audit rows, ids and schema/logic versions exist from day one. Everything that can be added safely goes on the deferred list.
10c. **Plan for change.** Classify what is hard to change (contracts, ids, names) versus easy (tables, JSON contents, screens). For database changes use add, then switch, then drop. Each kind of change is a slice with an exit check. Write this as "How a change is handled".

## Starter questions

- "What is the smallest thing we could show end to end next week?"
- "Which part, if it fails, makes everything else worthless? Can we do that first?"
- "How will we know this slice works? Who runs the check?"
- "What can we turn off if this goes wrong?"
- "Who builds what, and who has to agree to what before they can start?"

## Gate (layer 10 passed when)

- [ ] The skeleton has an exit check and runs on the hand-written cases.
- [ ] Every slice has an exit check (inputs, number, threshold), an owner, a flag or rollback, and what it rests on.
- [ ] Slices are in risk order with the reasoning visible.
- [ ] Contracts are first; deferred items have revisit triggers.
- [ ] Test sets exist or are slice zero.
- [ ] Tracks and join slices exist if more than one team builds.
- [ ] A note on how changes are handled.
- [ ] The user agrees the order and the checks.

## Depth

small: one slice with an exit check. medium: skeleton plus slices. large: skeleton, slices with flags, deferred list with triggers, rollout, and slice docs as each starts.

## When it goes sideways

- **Slices cannot be judged alone.** The component boundary is wrong; return to layer 6.
- **The skeleton is too big.** Make steps dumber. A stub that returns a fixed answer is fine.
- **The riskiest slice is blocked** (data, access, another team). Put the unblocking task first and keep the skeleton moving.
- **The user wants the plan as tickets.** Convert slices into tickets one-to-one; keep the exit checks as the acceptance criteria. Do not file tickets in a tracker unless asked.
- **The build is already underway.** Use rescue mode: treat what exists as the skeleton and add stored artifacts and exit checks around it.
- **The shape keeps changing during the build.** It is expected: classify the change and use the update steps, do not reopen the whole plan.
- **Deadlines force cuts.** Cut by deferring slices, not by dropping exit checks.

## Hands off to

Building, and layer 11 when requirements move.
