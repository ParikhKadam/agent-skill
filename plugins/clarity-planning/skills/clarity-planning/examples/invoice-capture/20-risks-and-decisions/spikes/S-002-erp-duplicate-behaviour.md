---
id: S-002
title: ERP duplicate-post behaviour
layer: 3
kind: spike
status: agreed
version: 1
updated: 2026-10-24
summary: The ERP accepted the same invoice twice; a lookup by invoice number and supplier does find an earlier post
depends_on: [FACTS@2]
read_sets: [review]
---

# S-002: ERP duplicate-post behaviour

## The question

Does the ERP reject a second post of the same invoice, and if not, can we detect an earlier one first?

## Why it matters

Risk R-2. Posting an invoice twice is the second thing clerks said would end their trust.

## The bar, set before we look

| Result | Means | We then |
|---|---|---|
| Second post is rejected | The ERP protects us | Rely on it, plus a log |
| Second post accepted, but an earlier post can be found by lookup | We must check before posting | Check-before-post (D-002) |
| Accepted and not findable | We cannot post safely | Stop and raise with the ERP owner |

## Method and data

Posted one test invoice twice to the ERP test environment, then queried it by supplier and invoice number. Test environment only.

## Result

Two entries were created. The lookup by supplier and invoice number returned both. The docs claiming idempotency were wrong for this endpoint.

## What we do now

Check-before-post using the lookup, with our own stable key (supplier id plus invoice number), recorded in D-002. Raise the documentation error with the ERP owner.
