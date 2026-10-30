---
id: FACTS
title: Facts register
layer: 2
kind: fact
status: draft
version: 1
updated: {{DATE}}
summary: Every fact the feature needs, where it lives, who writes it, how reliable it is and how we read it
depends_on: [BRIEF@1]
read_sets: [review, change-request, build-component]
---

# Facts register

## In plain words

Start from the hand-written cases: every time the ideal result needed a fact, it is a row here. A design built on a fact nobody checked is a guess, so each row says how we know. Status is `measured` (we checked real data), `doc` (someone wrote it down, unchecked), `inferred` (we reasoned it) or `unknown`.

Reliability is how often the fact is present and right (a fill rate, an error rate, or "unknown"). Access is how we can read it, with the limits that matter (rate, paging, permissions, what cannot be searched).

| ID | Fact needed | Where it lives | Who writes it, and when | Reliability | How we read it | Status | Notes |
|---|---|---|---|---|---|---|---|
| F-01 | TODO | TODO | TODO | TODO | TODO | unknown | |
