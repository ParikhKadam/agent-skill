---
id: ARTIFACTS
title: Artifacts and what goes stale
layer: 5
kind: artifact
status: agreed
version: 2
updated: 2026-10-28
summary: Five stored results, what the clerk can do to each, and what makes each stale; the table exposed the void-on-change rule
depends_on: [FLOW-USER@2, D-004@2]
read_sets: [review, change-request, build-component]
---

# Artifacts and what goes stale

## In plain words

Each row is a result the clerk can look at, fix or redo, so each is stored on the invoice record. The important columns are *Depends on* and *Goes stale when*: filling them in showed what happens if the clerk fixes the amount after approval (D-004).

| ID | Artifact | Produced by | User can | Depends on | Goes stale when | When stale | Stored where |
|---|---|---|---|---|---|---|---|
| ART-01 | Extracted fields | C-extractor | See, correct, re-read | The PDF | The PDF is replaced | Mark ART-02 to ART-04 stale and ask the clerk | Invoice record |
| ART-02 | Match (supplier and PO lines, with reasons) | C-matcher | See, pick by hand, re-match, skip | ART-01; live POs and receipts | ART-01 changes, or the PO closes or changes | Mark stale and ask the clerk to confirm | Invoice record |
| ART-03 | Coding proposal | C-coder | See, edit, regenerate | ART-02; coding rules | ART-02 changes | Regenerate automatically (rules, cheap); keep the clerk's edits marked | Invoice record |
| ART-04 | Approval | Manager or delegate (person) | Approve, reject | ART-01, ART-02, ART-03 as they were when approved | Any of them changes after approval | Approval void; invoice returns to the clerk (D-004) | Approval record |
| ART-05 | Posting record (ERP reference) | C-poster | See, retry | ART-04 | Never; it is final | Not applicable | Invoice record |

## Decisions found by filling in this table

- D-004: what happens to an approval when the clerk corrects something afterwards. Nobody had raised it before the "goes stale when" cell for ART-04 was filled in.
- The match depends on **live** PO and receipt data that can change under it, so ART-02 ages: it is re-checked when the invoice is opened and again just before posting.
