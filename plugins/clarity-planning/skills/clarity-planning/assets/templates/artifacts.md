---
id: ARTIFACTS
title: Artifacts and what goes stale
layer: 5
kind: artifact
status: draft
version: 1
updated: {{DATE}}
summary: TODO every intermediate result, who makes it, what the user can do to it and what makes it stale
depends_on: [FLOW-USER@1]
read_sets: [review, change-request, build-component]
---

# Artifacts and what goes stale

## In plain words

An **artifact** is an intermediate result that exists in its own right: stored, nameable, and something a user (or another step) can look at, fix, redo or skip. Every re-entry point in the user flow needs one. If a result is not stored, the user cannot act on it and the step cannot run alone.

The columns that matter most are *Depends on* and *Goes stale when*. Filling them in is how hidden design decisions surface (for example: if the user fixes this, what happens to everything built on it?). For each stale rule, state the behavior: regenerate automatically, mark and ask, or leave alone. If rules, a prompt or a model produce an artifact, their version is an input too: say which version made it and whether a new version re-runs it.

| ID | Artifact | Produced by | User can | Depends on | Goes stale when | When stale | Stored where |
|---|---|---|---|---|---|---|---|
| ART-01 | TODO | C-TODO | TODO | TODO | TODO | TODO | TODO |

## Decisions found by filling in this table

Each time a "goes stale" cell forced a question nobody had asked, record it here and open a decision doc.

- TODO
