---
id: {{ID}}
title: {{TITLE}}
layer: 6
kind: component
status: draft
version: 1
updated: {{DATE}}
summary: TODO what this component takes in, what it produces, and who decides inside
depends_on: [ARTIFACTS@1]
read_sets: [build-component, review]
---

# {{ID}}: {{TITLE}}

## In plain words

TODO One paragraph: what job this component does for the user.

## Inputs and output

- Reads (artifact ids): TODO
- Writes (one artifact id): TODO

## Who decides inside

Choose per step: **code**, **model** or **person**. Start with code. A model is justified only where code measurably fails; say what the code rung achieved and what is left over. If a model is used, see the AI components guide.

TODO

## Runs alone

How this component runs from stored inputs without the rest of the flow (a command, an endpoint, a test harness). If it cannot, the boundary is wrong.

TODO

## Quality bar and test set

What "good" means for this component alone, the number that says so, and the fixed inputs (cases, recorded real data) used to judge it.

TODO

## Failure modes

TODO What can go wrong, what the component returns when it does, and what the user then sees.

## Cost, latency and owner

TODO
