---
id: CHANGELOG
title: Change log
layer: 11
kind: log
status: agreed
version: 1
updated: 2026-10-28
summary: Every requirement change, which layers it reopened and what came of it
read_sets: [change-request]
---

# Change log

## In plain words

One entry per change. The second row shows the protocol: a change touched one decision, `wsctl.py impact D-004` listed the three docs resting on it, and only those were reopened.

| Date | What changed and why | Earliest layer touched | Docs reopened | Outcome |
|---|---|---|---|---|
| 2026-10-20 | Workspace created | 0 | | |
| 2026-10-28 | Controller: a cost centre change must also void an approval (money moves between budgets) | 3 | D-004 (v1 to v2), ARTIFACTS (v1 to v2), CROSSCUT (pin updated) | Approval covers ART-01 to ART-03 including the cost centre; audit records the void; the other decisions untouched |
