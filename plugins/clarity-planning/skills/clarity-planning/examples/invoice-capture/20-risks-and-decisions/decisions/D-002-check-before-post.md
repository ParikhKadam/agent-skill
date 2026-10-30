---
id: D-002
title: Check before posting, using our own key
layer: 3
kind: decision
status: agreed
version: 1
updated: 2026-10-24
confidence: hypothesis
basis: standard-practice
summary: Before each post, look up supplier plus invoice number in the ERP and refuse a second post
depends_on: [S-002@1, FACTS@2]
read_sets: [review, change-request]
---

# D-002: Check before posting, using our own key

## Choice

Before posting, look up the supplier and invoice number in the ERP. If an entry exists, do not post; record the existing entry instead. Our key is supplier id plus invoice number.

## In plain words

The ERP does not protect us from double posting (S-002), so we do. A post that times out is retried safely: the retry first looks, and finds it.

## Alternatives considered

| Option | For | Against |
|---|---|---|
| Check-before-post with our key | Works with what the ERP offers | Two calls per post; a tiny window between check and post |
| Ask the ERP team to add an idempotency key | The real fix | Not available soon; outside our control |
| Do nothing and reconcile later | No work now | The anti-goal in the brief |

## Why this one

Check-before-act with a natural key is the usual pattern when the other side offers a lookup but no idempotency key (basis: standard practice). It fits because S-002 showed the lookup works and the post does not protect us. We left out a distributed lock for now; the small window between check and post is covered by a unique key on our own record.

## What would change this

If the ERP adds an idempotency key, use it and keep the lookup as a backstop. If the window between check and post shows duplicates in the pilot, add a per-key lock. Confidence is a hypothesis because it was tested only in the ERP test environment.

## What it reopens or affects

Component C-poster, contract K-erp-post, the failure table in the system flow.
