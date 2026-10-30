---
id: D-004
title: An approval is void if what it covered changes
layer: 3
kind: decision
status: agreed
version: 2
updated: 2026-10-28
confidence: decided
basis: preference
summary: If the amount, supplier, PO match, coding or cost centre changes after approval, the approval is void and the invoice returns to the clerk
depends_on: [FLOW-USER@2]
read_sets: [review, change-request]
---

# D-004: An approval is void if what it covered changes

## Choice

An approval covers the extracted fields, the match and the coding as they were when approved. If any of them changes afterwards, the approval is void and the invoice returns to the clerk for re-approval.

## In plain words

Filling in the staleness table forced this question: what if the clerk corrects the amount after the manager approved? Without this rule a manager could approve one amount and the ERP receive another. Version 2 added the cost centre to what the approval covers, after the controller pointed out that a cost centre change moves money between budgets.

## Alternatives considered

| Option | For | Against |
|---|---|---|
| Void on any covered change | Safe; simple to explain | The manager approves again for small fixes |
| Void only on amount or supplier | Fewer re-approvals | Misses cost centre and coding changes |
| Allow edits with a notification | Fast | The manager may not notice |

## Why this one

The finance controller decided (version 2): safety over speed for money movements.

## What would change this

If re-approvals become a burden (more than 10% of invoices), allow minor coding edits within the same account without voiding.

## What it reopens or affects

Artifact ART-04's stale rule, cross-cutting audit (a void is a recorded event), the system flow's approval step.
