---
id: CONSTRAINTS
title: Constraints
layer: 2
kind: world
status: agreed
version: 1
updated: 2026-10-23
summary: What cannot change (the ERP) versus what we chose and may redesign (approval limits, where approval lives)
depends_on: [BRIEF@1]
read_sets: [review, change-request]
---

# Constraints

## In plain words

Only the first two rows bound the design. The others were choices someone made earlier, and we may change them if the evidence says so.

| ID | Constraint | Imposed or chosen | Who can change it | Source or evidence |
|---|---|---|---|---|
| X-01 | The ERP cannot record a partial receipt | imposed | ERP vendor | ERP documentation; confirmed in S-002 |
| X-02 | The ERP post has no idempotency key | imposed | ERP vendor | S-002 |
| X-03 | Approval limits live in a config file | chosen | Finance and engineering | F-06 |
| X-04 | Approvals are done in the ERP today | chosen | Finance controller | Current process; revisit in D-003 |
