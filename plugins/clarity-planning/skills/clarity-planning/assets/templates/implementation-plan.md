---
id: PLAN
title: Implementation plan
layer: 10
kind: plan
status: draft
version: 1
updated: {{DATE}}
summary: TODO the build order: a thin end-to-end skeleton first, then slices in risk order, each with its own exit check
read_sets: [onboard, review]
---

# Implementation plan

## In plain words

TODO Say in three sentences how we get from nothing to a working feature, and why in that order.

## The walking skeleton

The dumbest version of every step (stubs, hard-coded values, plain code) that runs end to end on the hand-written cases and produces the real output. Every stored result exists and every component can run alone.

- Skeleton exit check: TODO (which cases run end to end, and what output proves it)

## How the work is organised

TODO Who builds what: one track per team or agent (for example backend, AI service, frontend), each building against stubs and shared fixtures, and a join slice per phase that proves the tracks fit together.

- Tracks: TODO
- Join slices: TODO
- What cannot be added later (versions of outputs, audit rows, ids, schema/logic versions): TODO

## Slices, in risk order

Replace one stub at a time, riskiest first. A slice is done when its exit check passes on stored inputs, not when the code merges.

| ID | Track | Slice | Proves | Exit check | Flag or rollback | Owner | Rests on | Status |
|---|---|---|---|---|---|---|---|---|
| SL-01 | TODO | TODO | TODO | TODO | TODO | TODO | TODO | planned |

## Contracts to freeze first

Boundaries with other people or systems are agreed before the inside is built. Link the contract docs.

- TODO

## Deferred

What we are not building now, why it is safe to wait, and what would make us revisit it.

| Item | Why it can wait | Revisit when |
|---|---|---|
| TODO | TODO | TODO |

## Test strategy

TODO How each slice is judged (fixed inputs, recorded real data, hand-written cases), and what is judged by a person.

## Rollout

TODO Flags, who sees it first, how we notice trouble, how we turn it off.

## How a change is handled

TODO Changes during the build are routine updates, not rework. Say which things are hard to change (contracts, ids, names) and which are easy (tables, JSON contents, screens), how a database change goes (add, then switch, then drop), and that each change is a slice with an exit check.
