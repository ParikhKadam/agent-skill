---
id: CASE-01
title: Case clean match
layer: 1
kind: case
status: agreed
version: 1
updated: 2026-10-21
summary: A straightforward invoice with a PO number, where the clerk spends most of the time on matching and coding
read_sets: [onboard, understand]
---

# Case: clean match

## Where it came from

Source: invented for this example, modelled on a typical clerk session (replace with a real one in a real project).

## The situation

A supplier sends an invoice for 10 items against PO 4471. The PO number is printed on the invoice. All 10 items were received.

## What the user does today

The clerk types supplier, invoice number, date, total and lines (about one minute). Searches POs for the supplier, opens PO 4471 and compares lines (about three minutes). Picks accounts and a cost centre from memory (about three minutes). Sends to the manager.

## The ideal result, written by hand

Supplier: Northwind Fasteners (id S-208). Invoice INV-9034, dated 2026-10-02, total 1,284.00. Matched to PO 4471, all 10 lines, all received. Proposed coding: account 5100 for lines 1-8, account 5120 for lines 9-10, cost centre 310. Nothing flagged. The clerk confirms and sends.

## What was hard or surprising

The clerk always checks the bank details printed on the invoice against the supplier record "just in case". It never came up in the original request.

## Facts we reached for

- F-01 invoice fields readable from the PDF
- F-02 supplier master record, including bank details
- F-03 PO lines and their status
- F-04 goods-received records
