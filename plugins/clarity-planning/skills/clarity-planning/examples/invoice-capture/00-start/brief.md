---
id: BRIEF
title: Invoice capture
layer: 1
kind: brief
status: agreed
version: 1
updated: 2026-10-20
summary: Clerks turn a supplier invoice PDF into an approved, posted ERP entry with as few corrections as possible
size: large
mode: brownfield
read_sets: [onboard, understand, review, change-request]
---

# Invoice capture

> This is a worked example. The product, people and numbers are invented, so you can see what the docs look like without any real company's data.

## In plain words

Accounts-payable clerks receive supplier invoices as PDFs. Today they retype the fields into the finance app, find the matching purchase order by eye, pick accounting codes from memory, and send the invoice to a manager for approval. After approval someone posts it to the ERP. This feature reads the invoice, proposes the supplier, purchase order and codes, and lets the clerk fix anything before it goes to the manager. Approved invoices post to the ERP without retyping.

## Outcome in one sentence

Clerks get approved invoices into the ERP without retyping, and no invoice ever posts to the wrong place.

## Who acts on the result, and what they do next

The **clerk** checks the proposed match and codes, fixes what is wrong and sends for approval. The **manager** approves or rejects. Nobody acts on the extracted fields alone; they only matter if the match and codes are right.

## What would make them distrust it

One invoice posted to the wrong supplier or posted twice. Clerks said a single wrong posting would make them re-check everything by hand, which removes the benefit.

## The valuable part

The **match and the coding**, not reading the fields. In CASE-01 the clerk typed the fields in under a minute but spent six minutes finding the purchase order and choosing codes.

## Non-goals and anti-goals

- Non-goal: invoices arriving by email (parked, see the plan's deferred list).
- Non-goal: more than one currency.
- Anti-goal: an invoice posted twice, even if every other step works.

## What success looks like

- Hypothesis (to measure): at least 70% of invoices need only a confirm click from the clerk.
- Zero wrong postings and zero duplicate postings in the pilot month.

## Size and depth

Size: large. Why: money is irreversible once posted, a language model reads the PDFs, and the ERP is another team's system. All layers run in full.

## What already exists

Suppliers, purchase orders (POs) and roles exist in the finance app, and an ERP connector already handles payments. There is no invoice concept. Details in `10-world/existing-system.md`.
