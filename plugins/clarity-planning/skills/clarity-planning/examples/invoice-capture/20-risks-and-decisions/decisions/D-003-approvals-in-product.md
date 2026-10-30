---
id: D-003
title: Approvals live in the product, not the ERP
layer: 3
kind: decision
status: agreed
version: 1
updated: 2026-10-24
confidence: hypothesis
basis: preference
summary: Managers approve inside the finance app so delegation while on leave can be expressed and audited
depends_on: [CASE-02@1, CONSTRAINTS@1]
read_sets: [review, change-request]
---

# D-003: Approvals live in the product, not the ERP

## Choice

Approval is a step in the finance app, with delegation, and only an approved invoice is posted to the ERP.

## In plain words

CASE-02 shows the real need: a manager on leave, a delegate approving, and the record saying who. The ERP's own workflow has no delegation, so building approval there would not meet the need.

## Alternatives considered

| Option | For | Against |
|---|---|---|
| Approval in the finance app | Supports delegation and our audit needs | We own approval rules and limits |
| Approval in the ERP (today) | No new work | No delegation; the clerk cannot see status |

## Why this one

Delegation is the most visible need in CASE-02.

## What would change this

If the finance controller mandates the ERP workflow, or the ERP adds delegation. Confidence is a hypothesis: not yet confirmed with the finance controller.

## What it reopens or affects

Artifact ART-04, the permission matrix in cross-cutting, the approval limits in X-03.
