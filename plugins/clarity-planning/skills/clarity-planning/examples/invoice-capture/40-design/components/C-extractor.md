---
id: C-extractor
title: Extractor
layer: 6
kind: component
status: agreed
version: 1
updated: 2026-10-26
summary: Reads the PDF and produces the extracted fields (ART-01); a model, judged against hand-checked invoices
depends_on: [ARTIFACTS@2]
read_sets: [build-component, review]
---

# C-extractor: Extractor

## In plain words

Reads a supplier invoice PDF and returns supplier, invoice number, date, total and line items. It is the one place a language model is justified: layouts vary too much for rules.

## Inputs and output

- Reads: the PDF (an input, not an artifact).
- Writes: ART-01 (extracted fields).

## Who decides inside

A model (rung 2: one call, no tools). Rungs 0-1 were considered: templates per supplier do not scale. Output is validated by code (the total must equal the sum of lines; dates must parse). The model never sees bank details.

## Runs alone

`extract <pdf-path>` returns ART-01 as JSON with no database access, so it can be run on a folder of PDFs.

## Quality bar and test set

At least 95% of sampled invoices have supplier, number, date and total all correct; zero cases where a wrong value is presented as confident. Test set: 50 hand-checked invoices, mixed layouts, including 5 scans. Run each three times to check variance.

## Failure modes

Unreadable scan, wrong total (caught by the sum check), model timeout. It returns "could not read" with the reason; the clerk enters the fields by hand.

## Cost, latency and owner

Target under 10 seconds and a few cents per invoice. Owner: the AI engineer.
