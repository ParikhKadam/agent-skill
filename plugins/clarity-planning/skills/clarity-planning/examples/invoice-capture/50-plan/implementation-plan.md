---
id: PLAN
title: Implementation plan
layer: 10
kind: plan
status: agreed
version: 1
updated: 2026-10-28
summary: A walking skeleton on the three cases, then four slices in risk order, each with an exit check on stored inputs
depends_on: [C-matcher@1, C-poster@1, K-erp-post@1, RISKS@2, FLOW-SYSTEM@1]
read_sets: [onboard, review]
---

# Implementation plan

## In plain words

First build the dumbest version of every step so one invoice runs end to end and every result is stored. Then replace one stub at a time, riskiest first: matching, then safe posting, then reading the PDF, then coding, then approval rules. Each slice is finished when its own check passes on stored inputs.

## The walking skeleton

Upload a PDF. A stub extractor returns fields typed from a lookup table; a stub matcher returns the PO from the same table; a stub coder returns fixed codes; a manager approves in the app; the poster posts to the ERP stub. Every artifact (ART-01 to ART-05) is stored, and each component runs alone.

- Skeleton exit check: CASE-01, CASE-02 and CASE-03 run end to end against the stubs and produce the ideal results written in the cases; the duplicate-post example from K-erp-post is refused.

## Slices, in risk order

| ID | Slice | Proves | Exit check | Flag or rollback | Owner | Rests on | Status |
|---|---|---|---|---|---|---|---|
| SL-01 | Real matcher | 35 or more of 50 invoices match with none wrong | S-001's 50-invoice set plus CASE-02 and CASE-03 pass | `invoice_match` flag; off shows candidates only | Backend engineer | C-matcher, D-001 | planned |
| SL-02 | Real poster with check-before-post | No duplicate or wrong post under failures | 100 simulated runs including timeouts and races: 0 duplicates | `invoice_post` flag; off keeps "approved, not posted" | Backend engineer | C-poster, K-erp-post, D-002 | planned |
| SL-03 | Real extractor | 95% of 50 hand-checked invoices read correctly | The 50-invoice set, three runs each, no confident wrong values | `invoice_read` flag; off means manual entry | AI engineer | C-extractor | planned |
| SL-04 | Real coder, approval rules and audit | 80% of lines coded as the clerk would; every override audited | Last 200 coded lines; audit trail complete for CASE-02 | `invoice_approval` flag | Backend engineer | C-coder, D-003, D-004 | planned |

## Contracts to freeze first

- K-erp-post: both owners see the examples and agree before SL-02 starts.

## Deferred

| Item | Why it can wait | Revisit when |
|---|---|---|
| Invoices by email | Upload covers the pilot | The pilot ends |
| More than one currency | One currency in the pilot company | A second currency is needed |
| A model for matching leftovers | S-001 shows rules are enough | Manual picks exceed 30% in the pilot |
| Auto-approval under a threshold | Controller said not in version 1 (Q-3) | After the pilot |

## Test strategy

Fixed sets judge each slice: the 50-invoice set for matching and reading, 200 coded lines for coding, simulated failures against the ERP stub for posting. A person judges the approval flow with the three cases. Each set is built as slice zero and kept in the repo's fixtures.

## Rollout

One flag per slice, enabled for one pilot company first. Alert when "approved, not posted" exceeds an hour. Switching a flag off returns that step to manual entry with no data loss.
