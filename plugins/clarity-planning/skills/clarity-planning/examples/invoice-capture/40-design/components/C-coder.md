---
id: C-coder
title: Coder
layer: 6
kind: component
status: agreed
version: 1
updated: 2026-10-26
summary: Proposes account and cost-centre codes for each invoice line (ART-03) from the supplier's coding history
depends_on: [ARTIFACTS@2]
read_sets: [build-component, review]
---

# C-coder: Coder

## In plain words

Proposes accounting codes for each line using how the same supplier's earlier invoices were coded. It is a suggestion; the clerk can change every code.

## Inputs and output

- Reads: ART-02 and the supplier's coding history.
- Writes: ART-03 (codes per line, each with the reason).

## Who decides inside

Code (rung 0): the most frequent codes for the same supplier and item description; the cost centre from the PO. A model is not used. If a supplier is new, the codes are left empty with "no history" for the clerk to fill.

## Runs alone

`propose-codes <invoice-id>` reads a stored ART-02 and writes ART-03. Regenerating keeps lines the clerk already edited and marks them.

## Quality bar and test set

At least 80% of lines get the code the clerk would have chosen, measured on the last 200 coded lines; no code is ever proposed from a different tenant's history.

## Failure modes

New supplier (empty codes, flagged); conflicting history (shows the top two codes).

## Cost, latency and owner

No model cost; under 1 second. Owner: the backend engineer.
