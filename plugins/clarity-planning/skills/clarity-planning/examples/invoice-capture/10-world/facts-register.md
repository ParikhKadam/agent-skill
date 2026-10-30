---
id: FACTS
title: Facts register
layer: 2
kind: fact
status: agreed
version: 2
updated: 2026-10-23
summary: Seven facts the cases needed, with source, reliability and how we read each; one still unknown
depends_on: [BRIEF@1, CASE-01@1, CASE-02@1, CASE-03@1]
read_sets: [review, change-request, build-component]
---

# Facts register

## In plain words

Each row is a fact the hand-written cases needed. Numbers marked **[M]** were measured on a sample of past records (invented for this example). The two rows that changed the design are F-05 (the ERP cannot detect duplicate posts) and F-04 (goods-received records exist for only 70% of deliveries).

| ID | Fact needed | Where it lives | Who writes it, and when | Reliability | How we read it | Status | Notes |
|---|---|---|---|---|---|---|---|
| F-01 | Supplier, number, date, total and lines from the PDF | The PDF itself | The supplier, at invoicing | Total clearly readable on 47 of 50 sampled PDFs (94%) [M]; the 3 misses were scans | Extractor reads the PDF; clerk confirms | measured | Scans are the weak case |
| F-02 | Supplier master record, incl. bank details | Suppliers table (existing) | Finance, when a supplier is onboarded | Bank details on the invoice differed from the record on 6 of 200 sampled [M] | Existing supplier lookup by id or name | measured | A mismatch is a fraud signal, see Q-2 |
| F-03 | PO lines and PO status | POs table (existing) | Buyers, at ordering | 12% of POs were already closed when their invoice arrived [M] | Existing PO query by supplier and number | measured | Closed POs still need matching |
| F-04 | Goods received against a PO | Goods-received records (existing) | Warehouse, at delivery | Present for about 70% of deliveries [M] | Existing receipts query | measured | Missing receipt is not the same as nothing received |
| F-05 | Does the ERP reject a second post of the same invoice? | ERP posting API | The ERP | No: posting the same payload twice created two entries (S-002) [M] | ERP lookup by invoice number and supplier | measured | Drives D-002 |
| F-06 | Who may approve, up to what amount, and delegation | Approval limits config | Finance, hard-coded in config | Rules exist; delegation is not modelled | Read config; delegation needs a new record | doc | Chosen, not imposed (X-03) |
| F-07 | How long invoice PDFs must be kept | Finance policy | Finance controller | Unknown | Ask the owner | unknown | Q-1 |
