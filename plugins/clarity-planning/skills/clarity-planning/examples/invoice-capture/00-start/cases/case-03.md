---
id: CASE-03
title: Case no PO number
layer: 1
kind: case
status: agreed
version: 1
updated: 2026-10-21
summary: An invoice with no PO number, where the clerk finds the PO by supplier and amount
read_sets: [onboard, understand]
---

# Case: no PO number

## Where it came from

Source: invented for this example.

## The situation

A supplier sends an invoice with no PO number printed. The supplier has three open POs, two of them for similar amounts.

## What the user does today

The clerk searches by supplier, compares amounts and descriptions, and sometimes phones the buyer. This takes about ten minutes.

## The ideal result, written by hand

The system lists the three candidate POs with the reason each is likely or unlikely ("amount differs by 12", "same items") and does **not** pick one on its own. The clerk picks one, or marks "no PO", and the rest of the flow continues from that pick.

## What was hard or surprising

The clerk said they would rather pick by hand than risk a wrong automatic match. That is the distrust point in the brief.

## Facts we reached for

- F-03 PO lines and their status
- F-01 invoice fields readable from the PDF (the amount and item descriptions matter here)
