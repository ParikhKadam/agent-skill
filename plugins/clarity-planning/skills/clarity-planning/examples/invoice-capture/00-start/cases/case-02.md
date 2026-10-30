---
id: CASE-02
title: Case partial delivery
layer: 1
kind: case
status: agreed
version: 1
updated: 2026-10-21
summary: An invoice for 10 items when only 7 arrived, and the manager who is on leave
read_sets: [onboard, understand]
---

# Case: partial delivery, approver away

## Where it came from

Source: invented for this example.

## The situation

An invoice bills 10 items against a PO, but the goods-received record shows only 7 arrived. The manager who normally approves is on leave for two weeks.

## What the user does today

The clerk notices the mismatch by comparing the invoice to the goods-received note, emails the supplier, and holds the invoice. For approval, the clerk walks it to whoever is covering. There is no system record of who covers whom.

## The ideal result, written by hand

The invoice is matched to the PO with a clear flag: "3 of 10 lines not yet received". It cannot be sent for approval until the clerk records a decision (hold, or approve as billed with a reason). The approval goes to the manager's delegate for those two weeks, and the delegate's name appears in the record.

## What was hard or surprising

Delegation. Nobody had mentioned it until the manager was away. It changes who may approve and what the audit trail must say.

## Facts we reached for

- F-03 PO lines and their status
- F-04 goods-received records
- F-06 approval limits and who may approve
