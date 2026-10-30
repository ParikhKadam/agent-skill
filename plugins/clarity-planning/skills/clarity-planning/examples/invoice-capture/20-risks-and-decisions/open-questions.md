---
id: QUESTIONS
title: Open questions
layer: 3
kind: question
status: agreed
version: 1
updated: 2026-10-24
summary: Policy questions only the finance controller can answer, each with our recommended default
read_sets: [review, change-request]
---

# Open questions

## In plain words

Three questions belong to the finance controller. We proceed on the recommended defaults and mark dependent decisions as hypotheses.

| ID | Question | Why it matters | Owner | Recommended answer | Status | Needed by layer |
|---|---|---|---|---|---|---|
| Q-1 | How long must invoice PDFs be kept? | Decides storage and deletion rules | Finance controller | Seven years; make it configurable | open | 8 |
| Q-2 | When bank details differ from the supplier record, block or only warn? | A mismatch is a fraud signal | Finance controller | Block until a manager confirms | open | 8 |
| Q-3 | May invoices under a threshold auto-approve? | Changes the approval flow | Finance controller | Not in version 1; revisit after the pilot | answered | 4 |
