---
id: FLOW-SYSTEM
title: System flow
layer: 7
kind: flow
status: agreed
version: 1
updated: 2026-10-26
summary: How the four components run from the PDF or from any stored artifact, and how failure, duplicates and retries are handled
depends_on: [ARTIFACTS@2, D-002@1]
read_sets: [review, build-component]
---

# System flow

## In plain words

A full run reads the PDF, matches, proposes codes, waits for approval, then posts. Because every result is stored, a re-run starts from any of them, and posting always checks first for an earlier post.

## A full run

1. **C-extractor** reads the PDF and writes ART-01. Decides inside: a model, judged against hand-checked fields.
2. **C-matcher** reads ART-01 and live PO and receipt data and writes ART-02. Decides inside: code, with the clerk picking leftovers.
3. **C-coder** reads ART-02 and writes ART-03. Decides inside: rules from the supplier's coding history.
4. A manager approves (ART-04). Decides: a person. The invoice waits in "awaiting approval".
5. **C-poster** reads ART-04 and, in order: re-checks ART-02 against live data, looks up an earlier ERP post, then posts and writes ART-05. Decides inside: code.

Nothing runs in parallel in version 1: each step needs the artifact before it. Coding could run alongside the approval wait only if codes were not part of what the manager approves, and they are (D-004).

## Start points

| Start from | Used when | Runs these components | Skips |
|---|---|---|---|
| The PDF | New upload, or the PDF replaced | C-extractor, C-matcher, C-coder | Nothing |
| ART-01 | The clerk corrected the fields | C-matcher, C-coder | C-extractor |
| ART-02 | The clerk picked or changed the PO | C-coder | C-extractor, C-matcher |
| ART-03 | The clerk asked to re-propose codes | C-coder | C-extractor, C-matcher |
| ART-04 | Approved; time to post, or retry | C-poster | All earlier components |

## What happens when a step fails

| Step | Failure | What the user sees | Retry or idempotency |
|---|---|---|---|
| Read | Scan unreadable or model error | "Could not read this invoice; enter it by hand" | Manual entry; no automatic retry |
| Match | PO query fails | "Could not check POs; try again" | Retry on request; nothing stored |
| Post | ERP down or timeout | "Approved, not yet posted" | Retried with backoff; each retry looks up first (D-002) |
| Post | An earlier post is found | "Already posted" with the ERP reference | No second post; the existing entry is recorded |

## Duplicates, retries and concurrency

- The same upload twice: caught by a hash of supplier, invoice number and total; the clerk sees the earlier invoice.
- Two clerks open the same invoice: the first holds a lock; the second sees "being edited by X".
- A retry after a timeout: the lookup finds the earlier post, so no duplicate.
- A failed step never stores a partial result as if it were complete.
