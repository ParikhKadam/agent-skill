---
id: K-erp-post
title: ERP posting and lookup
layer: 9
kind: contract
status: agreed
version: 1
updated: 2026-10-27
summary: The post and lookup calls between the finance app and the ERP connector, with happy-path and duplicate examples
depends_on: [FLOW-SYSTEM@1, S-002@1]
read_sets: [contract, review]
---

# K-erp-post: ERP posting and lookup

## In plain words

Two calls cross this boundary: look up whether an invoice is already in the ERP, and post it. The ERP does not reject duplicates, so the lookup is ours to call first.

## Parties and owners

- Sends: the finance app (owner: backend engineer).
- Receives: the ERP connector (owner: the ERP integration team).
- Who must agree before it is frozen: both owners, and finance for the field mapping.

## Example: happy path

```json
POST /erp/invoices
{
  "supplier_id": "S-208",
  "invoice_number": "INV-9034",
  "invoice_date": "2026-10-02",
  "total": "1284.00",
  "currency": "USD",
  "po_number": "4471",
  "lines": [{"account": "5100", "cost_centre": "310", "amount": "1000.00"}],
  "request_key": "S-208:INV-9034"
}
-> 201 {"erp_reference": "AP-55012", "status": "created"}
```

## Example: a failure

```json
GET /erp/invoices?supplier_id=S-208&invoice_number=INV-9034
-> 200 {"items": [{"erp_reference": "AP-55012", "status": "posted"}]}
```
An existing item means: do not post; record the existing reference. A timeout on `POST` means: look up before any retry.

## Rules

`request_key` is ours (supplier id plus invoice number) and is echoed back by the connector once it supports it; until then the lookup is the guard. Amounts are decimal strings. The connector may add response fields; we ignore unknown ones. Changes are versioned in the path (`/v1`).

## Stub

The finance app tests against a stub that stores posts in memory and returns the two examples above, including a stub that returns "201" twice for the same key to prove the lookup guards it.
