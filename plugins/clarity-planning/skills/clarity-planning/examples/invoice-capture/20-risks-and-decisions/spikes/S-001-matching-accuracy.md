---
id: S-001
title: Matching accuracy with rules only
layer: 3
kind: spike
status: agreed
version: 1
updated: 2026-10-24
summary: On 50 past invoices, exact rules matched 41 correctly and 0 wrongly; 9 were left for a person
depends_on: [FACTS@2]
read_sets: [review]
---

# S-001: Matching accuracy with rules only

## The question

Can plain rules (PO number, then supplier plus amount) match an invoice to its PO with no wrong matches?

## Why it matters

Risk R-1. A wrong match posts money to the wrong place, the one failure the clerks said would end their trust.

## The bar, set before we look

| Result | Means | We then |
|---|---|---|
| 0 wrong, 35 or more right of 50 | Rules are enough for the common case | Rules first; a person picks the leftovers (D-001) |
| Any wrong match | Rules are unsafe | Never auto-pick; always show candidates |
| Fewer than 35 right, 0 wrong | Safe but too many manual picks | Consider a model for the leftovers |

## Method and data

Last quarter's approved invoices, 50 chosen at random (read-only), with the true PO known from the approved record. Rules: exact PO number; else single PO for that supplier within 5% of the total. Repeatable by re-running the script on the same sample. Invented sample for this example.

## Result

41 right, 0 wrong, 9 left to a person. Of the 9: 5 had no PO number and no single close amount, 4 had two equally good candidate POs. Not covered: scanned invoices, foreign suppliers.

## What we do now

Rules first, a person picks the leftovers, no model for matching in version 1 (D-001). Revisit if leftovers exceed 30% in the pilot.
