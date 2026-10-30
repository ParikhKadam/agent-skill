---
id: C-matcher
title: Matcher
layer: 6
kind: component
status: agreed
version: 1
updated: 2026-10-26
summary: Finds the supplier and PO for an invoice (ART-02) with exact rules, and lists candidates when the rules cannot decide
depends_on: [ARTIFACTS@2, D-001@1, S-001@1]
read_sets: [build-component, review]
---

# C-matcher: Matcher

## In plain words

Finds which supplier sent the invoice and which PO lines it bills. It never picks between equally good candidates; it lists them with reasons and lets the clerk pick.

## Inputs and output

- Reads: ART-01, plus live supplier, PO and receipt data.
- Writes: ART-02 (match, or a candidate list with reasons).

## Who decides inside

Code (rung 0), by decision D-001. Rules in order: exact PO number; else one PO for that supplier within 5% of the total. Everything else becomes a candidate list for a person. A model for the leftovers was considered and deferred; the measured evidence (S-001) does not justify it yet.

## Runs alone

`match <invoice-id>` reads a stored ART-01 and writes ART-02; it can also run on a fixture file of invoices and POs.

## Quality bar and test set

Zero wrong automatic matches. At least 35 of 50 matched automatically. Test set: the 50 past invoices from S-001, plus CASE-02 and CASE-03 as awkward cases. Run on every change to the rules.

## Failure modes

PO query fails (returns "could not check POs"; stores nothing). A closed PO still matches but is flagged. A short receipt is flagged "3 of 10 lines not received".

## Cost, latency and owner

No model cost; under 2 seconds. Owner: the backend engineer.
