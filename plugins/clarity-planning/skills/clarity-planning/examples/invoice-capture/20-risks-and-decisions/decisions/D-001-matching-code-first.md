---
id: D-001
title: Matching is code first; a person picks the leftovers
layer: 3
kind: decision
status: agreed
version: 1
updated: 2026-10-24
confidence: measured
basis: evidence
summary: Match with exact rules and show candidates for the rest; do not use a model for matching in version 1
depends_on: [S-001@1, FACTS@2]
read_sets: [review, change-request]
---

# D-001: Matching is code first; a person picks the leftovers

## Choice

Match an invoice to a PO with exact rules. When the rules cannot decide, show the candidate POs with reasons and let the clerk pick. No model for matching in version 1.

## In plain words

Rules got 41 of 50 right with none wrong (S-001). The other 9 are exactly the cases where clerks would rather choose than trust a guess. Adding a model would add cost and a chance of a wrong match for little gain.

## Alternatives considered

| Option | For | Against |
|---|---|---|
| Rules, then a person | Safe; measured; cheap | 18% need a manual pick |
| Rules, then a model for the leftovers | Fewer manual picks | A wrong match is the failure users fear most; extra cost |
| Model for everything | Simplest to describe | Unmeasured; hardest to trust and test |

## Why this one

S-001: 41 right, 0 wrong. CASE-03: the clerk said they prefer picking over a risky automatic match.

## What would change this

If manual picks exceed 30% of invoices in the pilot, test a model on the leftovers with a zero-wrong bar on the same 50-invoice set.

## What it reopens or affects

Component C-matcher; artifact ART-02; the user flow's "skip the match" re-entry.
