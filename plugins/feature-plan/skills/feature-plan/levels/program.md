# Level 4: Program plan

**Resolves:** in what order to build so that something can be watched working at every step, which hard-to-change decisions must be settled first, and what is deliberately not built yet. **Output:** `plan.md`. **Needs:** `design.md` approved.

The failure this level prevents is a build that lands as one untestable piece, and a plan with the detail of a specification that is wrong by the time it is used. An engineer trusts what they can run and see, so every slice ends in a demo. Detail about how a slice is built waits until the slice is next (a slice spec, written later); this plan holds only what must be known now.

## Steps

1. **Start from the releases** in `outcome.md`. Each release is shippable and watchable. Slices serve a release; a slice that serves none is cut.
2. **Slice zero: fixed inputs and an answer key.** Before anything is built, collect real or recorded inputs and write down the right answers, by the user and an owner, not by the builder. Label invented inputs as invented. Every later pass line is judged on these. If real data is out of reach, make getting it slice zero.
3. **Cut slices and order them.** One slice builds one piece or proves one claim. Order by what is hardest to change first, then by risk:
   - **Settle the hard-to-change things first.** Interfaces, queues or platform layout, ids and versions come first, built as a thin end-to-end skeleton on stubs: each team's piece runs alone against stubs of the others, so nothing others depend on is reworked later. Changing it later costs the most, so it is not left to the end.
   - **Run the evidence slice beside the skeleton, not instead of it.** It needs nothing built: fixed inputs, an answer key, and the riskiest unknown.
   - **Then replace the stubs with real pieces one at a time,** riskiest first, each demonstrated on real or recorded data. Put real output as early as this order allows. Pieces that can run alone with no infrastructure are built that way.
   - Every outside source the design depends on is exercised from the start, not left to the end.
   - Keep the first release small and add complexity later; a depth feature that no release needs waits for a later release.
4. **Give every slice a demo,** in this form:
   - **Run:** the command or action.
   - **You see:** what appears, in plain words.
   - **Pass when:** a number on fixed inputs, run by anyone.
   - **Needs:** the slices, decisions, access or data it waits for.
   - **Switch:** a flag or a way to roll back.
   - **Owner:** a named person or team.
   Command names are proposals; the slice owner picks the real ones.
5. **Settle the early decisions.** List the hard-to-change choices from `design.md` that must be agreed before the first slice that depends on them, each with its owner. Name the slice that needs each. Anything easy to change waits.
6. **Tracks and joins,** if more than one team builds. One track per team; each builds against recorded or stub versions of the others, using fixtures recorded from real runs where possible. A release check at the end of each release connects the tracks for real and is judged on the fixed inputs.
7. **Deferred list.** Each item: why it can wait, and what would bring it back (a measured trigger, not a date).
8. **Rollout and rollback.** What is switched on first, who watches it, how trouble is noticed, how to switch it off, and what happens to existing data.
9. **How a change is handled.** Classify hard to change (interfaces, ids, names, formats) versus easy (tables, contents, screens). Hard ones change only by adding optional fields or a new version run beside the old. Easy ones change by update steps (a database change adds, then switches, then drops). Each change is a slice with a pass line; the plan is not reopened.
10. **What each slice lets the user tick.** A table from slice to the outcome item it completes, so any tracker the team uses can point at it. The plan itself knows nothing of trackers.
11. **Estimates.** None until slice zero and the first real slice have run.

## When it goes sideways

- A slice cannot be demonstrated alone: the boundary is wrong; return to level 3.
- The riskiest slice is blocked (data, access, another team): put the unblocking task first and keep the rest moving.
- Deadlines force cuts: cut by deferring slices, never by dropping pass lines.
- The build is already under way: treat what exists as the first slice and add the answer key and pass lines around it.

## Check coverage before the gate

Walk `design.md` against the slices. Every piece, every stored result, and every cross-cutting verdict marked *applies* (access rules, audit, deletion, support access, rollout and cutover, operations and recovery) must have a slice that builds it, or an item on the deferred list with its trigger. A tested behaviour that no slice builds is a gap. List the gaps and add the slices before asking for the gate.

## Gate: the user agrees that

- every piece, stored result and "applies" verdict has a slice or a deferred item;
- every slice has a demo, a pass line judged on fixed inputs, an owner and a switch;
- the order and the reasoning behind it are visible, and the first demo uses real output;
- the early decisions have owners and the slices that wait for them;
- the deferred list has triggers;
- the user can tell, release by release, what they will be able to watch.

## Depth

Small: one slice with a demo. Medium: releases and slices, short. Large: all of the above, with tracks, a deferred list and rollout.

## `plan.md` contains

Releases and slices (each with its demo); the early decisions with owners; tracks and release checks; deferred items with triggers; rollout and rollback; how a change is handled; what each slice lets the user tick. Use `templates/plan.md`. Slice specs are not written here.
