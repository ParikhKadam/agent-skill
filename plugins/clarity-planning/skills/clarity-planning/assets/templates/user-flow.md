---
id: FLOW-USER
title: User flow
layer: 4
kind: flow
status: draft
version: 1
updated: {{DATE}}
summary: TODO what the user sees and does from start to finish, and where they can step in, fix or redo
depends_on: [BRIEF@1]
read_sets: [onboard, understand, review]
---

# User flow

## In plain words

TODO One short paragraph: the whole journey as a story, walked with one case from the cases folder.

## The story, step by step

Walk one real case. Each step says what the user sees, what they do, and what they get back.

1. TODO

## Other paths

- **Alternate paths** (a different but valid way through): TODO
- **What differs by role or permission:** TODO
- **When something fails, and how the user recovers:** TODO
- **When the user leaves halfway and comes back:** TODO

## Re-entry points

At every step, ask four questions: can the user **see** the intermediate result, **correct** it, **regenerate it alone**, or **skip** the step because they already know the answer? Each yes needs a stored result to act on: name it in the Artifact column (an `ART-nn` from `artifacts.md`).

| Step | User can see | User can correct | Regenerate alone | Skip | Artifact |
|---|---|---|---|---|---|
| TODO | TODO | TODO | TODO | TODO | TODO |

## Re-entries ruled out

List the ones we considered and decided against, with the reason, so nobody reopens them by accident.

- TODO
