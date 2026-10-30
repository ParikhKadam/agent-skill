---
id: C-poster
title: Poster
layer: 6
kind: component
status: agreed
version: 1
updated: 2026-10-26
summary: Posts an approved invoice to the ERP once, checking first for an earlier post (ART-05)
depends_on: [ARTIFACTS@2, D-002@1, K-erp-post@1]
read_sets: [build-component, review]
---

# C-poster: Poster

## In plain words

Sends an approved invoice to the ERP exactly once. Before posting it re-checks the match against live data and looks for an earlier post, so retries never duplicate.

## Inputs and output

- Reads: ART-04 (approval), ART-01 to ART-03 as approved, and live PO data.
- Writes: ART-05 (the ERP reference).

## Who decides inside

Code (rung 0). Steps in order: confirm the approval is still valid (D-004); re-check the PO is still open and the receipt unchanged; look up supplier plus invoice number in the ERP; post only if none exists.

## Runs alone

`post <invoice-id>` runs against the ERP stub (K-erp-post), so it can be tested without the real ERP.

## Quality bar and test set

Zero duplicate posts and zero wrong-supplier posts across 100 simulated runs that include timeouts after a successful post, double clicks, and two workers racing. Test set: the stub's failure examples from K-erp-post.

## Failure modes

ERP down (state "approved, not posted", retried with backoff); an earlier post found (records it, no new post); the approval no longer valid (stops and returns the invoice to the clerk).

## Cost, latency and owner

Two ERP calls per post. Owner: the backend engineer.
