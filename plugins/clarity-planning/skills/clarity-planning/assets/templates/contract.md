---
id: {{ID}}
title: {{TITLE}}
layer: 9
kind: contract
status: draft
version: 1
updated: {{DATE}}
summary: TODO the boundary, who is on each side, and the exact messages that cross it
depends_on: []
read_sets: [contract, review]
---

# {{ID}}: {{TITLE}}

Status: keep this doc `pending` until the owner on the other side has seen the examples; then `agreed`.

## In plain words

TODO What crosses this boundary, in which direction, and why it must be agreed before building.

## Parties and owners

- Sends: TODO (owner TODO)
- Receives: TODO (owner TODO)
- Who must agree before it is frozen: TODO

## Example: happy path

```json
TODO a real example payload
```

## Example: a failure

```json
TODO the error the receiver returns, with the code the sender must handle
```

## Rules

TODO Required and optional fields, limits, idempotency key, ordering, what is echoed back, versioning and how it may change without breaking the other side.

## Stub

TODO How each side can run against a stub of the other, so both can build in parallel.
