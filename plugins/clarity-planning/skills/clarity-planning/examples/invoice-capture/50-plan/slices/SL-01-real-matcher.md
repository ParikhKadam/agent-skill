---
id: SL-01
title: Real matcher
layer: 10
kind: slice
status: agreed
version: 1
updated: 2026-10-28
summary: Replace the stub matcher with the rule-based one and prove 35 of 50 match with none wrong
depends_on: [PLAN@1, C-matcher@1]
read_sets: [build-component]
---

# SL-01: Real matcher

## In plain words

The stub matcher returns a fixed PO. This slice replaces it with the real rules (exact PO number, else one PO within 5% of the total) and the candidate list for the rest.

## Proves

Rules alone match at least 35 of 50 past invoices with no wrong automatic match, and the awkward cases (short receipt, no PO number) produce a flag or a candidate list instead of a guess.

## Exit check

On the 50 stored invoices from S-001: at least 35 matched, 0 wrong. On CASE-02: the "3 of 10 lines not received" flag appears. On CASE-03: three candidates are listed and none is chosen. Anyone can run `match` over the fixture folder and compare to the stored true POs.

## Flag or rollback

`invoice_match`. Off: the clerk always picks the PO from a list.

## Notes during the work

(empty at the start; record surprises here, and reopen layer 2 if the data differs from the register.)
