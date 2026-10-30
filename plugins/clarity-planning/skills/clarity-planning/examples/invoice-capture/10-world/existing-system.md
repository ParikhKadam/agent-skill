---
id: EXISTING
title: Existing system inventory
layer: 2
kind: world
status: agreed
version: 1
updated: 2026-10-20
summary: What the finance app already has that invoice capture reuses, and the surprises found
depends_on: [BRIEF@1]
read_sets: [review, build-component]
---

# Existing system inventory

## In plain words

Suppliers, purchase orders, receipts, roles and an ERP payments connector already exist, so invoice capture adds an invoice concept and approval rather than a new platform. The surprises are mostly about the ERP and about approvals living in a config file.

| Area | What exists | Where (file, service or doc) | Reuse, extend or avoid | Surprise |
|---|---|---|---|---|
| Data and models | Suppliers, POs with lines, goods-received records | finance-app database | Reuse | PO status can be stale (closed POs still billed) |
| Permissions and tenancy | Roles per company; tenant id on every row | auth module | Reuse; extend with delegation | Approval limits are hard-coded in config, not in the database |
| Integrations and tools | ERP connector that posts payments | `erp_connector` service | Extend to post invoices | No idempotency key; duplicates accepted (F-05) |
| Tracing, logging, config | Request tracing, structured logs | shared logging library | Reuse | Logs may contain supplier names; must not hold bank details |
| UI patterns | List-detail screens, a confirm dialog | web app | Reuse | None |
| Tests and fixtures | PO and supplier fixtures | `tests/fixtures` | Extend with invoice fixtures | None |

## Things that behave differently from what the docs say

- The connector docs say "post is idempotent". In a test environment, posting the same payload twice created two entries (S-002).
