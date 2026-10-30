---
id: {{ID}}
title: {{TITLE}}
layer: 3
kind: decision
status: draft
version: 1
updated: {{DATE}}
confidence: hypothesis
basis: evidence
summary: TODO one line: the choice and the reason
depends_on: []
read_sets: [review, change-request]
---

# {{ID}}: {{TITLE}}

Confidence is `decided` (the owner agreed), `hypothesis` (our best bet, not yet tested), `unknown` (open) or `measured` (a test or real data backs it). Do not mark a guess as decided.

Basis is `evidence` (a spike, measured data or a case backs it), `standard-practice` (an established pattern we expect to fit; see the standard practices guide), or `preference` (the owner's call). A `standard-practice` basis stays `hypothesis` until tested here, and should cite a source for anything high-stakes (payments, auth, personal data, regulated areas).

## Choice

TODO The decision in one or two sentences.

## In plain words

TODO Why a reader should care and what would go differently without it.

## Alternatives considered

| Option | For | Against |
|---|---|---|
| TODO | TODO | TODO |

## Why this one

TODO Tie it to evidence: a fact id, a spike result, a case.

## What would change this

TODO The observation or result that would make us reverse it. A decision with no stated trigger is a belief, not a decision.

## What it reopens or affects

TODO Docs and layers that rest on this choice.
