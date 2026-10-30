---
id: FLOW-SYSTEM
title: System flow
layer: 7
kind: flow
status: draft
version: 1
updated: {{DATE}}
summary: TODO how the components run in order from any starting artifact, and what happens when something fails
depends_on: [ARTIFACTS@1]
read_sets: [review, build-component]
---

# System flow

## In plain words

TODO The whole run in three sentences. Then the detail. This flow is components run in dependency order **from a chosen starting artifact**: a full run starts at the input, a re-run starts at a stored artifact.

## A full run

For each step name the component, the artifacts it reads, the artifact it writes, and **who decides inside** (code, model or person).

1. TODO

## Start points

| Start from | Used when | Runs these components | Skips |
|---|---|---|---|
| TODO | TODO | TODO | TODO |

## What happens when a step fails

| Step | Failure | What the user sees | Retry or idempotency |
|---|---|---|---|
| TODO | TODO | TODO | TODO |

## Duplicates, retries and concurrency

TODO The same request twice. Two people at once. A retry after a timeout. A partial failure halfway through.
