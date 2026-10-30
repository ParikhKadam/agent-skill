# Design

Status: draft

In plain words: {{three sentences: the pieces, what crosses between them, and the choices that must be settled early}}

## The pieces

Each piece has one producer role. Mark each *reused*, *changed* or *new* where something exists today.

| Piece | Does | Reads | Writes | Decides inside | Runs alone with | Quality bar (number, test set) | Today |
|---|---|---|---|---|---|---|---|

Findings where today's code contradicts the agreed behaviour: {{each, or "none found"}}

## Boundary: {{name, for example: system A to system B}}

Parties and owners: {{sender, receiver, who must agree}}

| Field | Read by | Why it exists | Comes from |
|---|---|---|---|

Happy-path example:

```
{{a real example}}
```

Failure example:

```
{{the error and the code the sender must handle}}
```

Rules: {{required and optional fields, idempotency, ordering, versioning}}

## Failure and cost

| Piece | When it fails it returns | The person sees | Time and cost per run |
|---|---|---|---|

## Cross-cutting verdicts

| Concern | Verdict (applies, defer, not applicable) | Reason and what it means for the design |
|---|---|---|
| Who may do what | | |
| Isolation between users | | |
| Audit | | |
| Sensitive data and encryption | | |
| Retention and deletion | | |
| Observability | | |
| Cost | | |
| Rollout and rollback | | |
| Model and untrusted-content risks | | |
| Privacy and compliance | | |

## Hard-to-change choices

### {{short name}}

- Need it serves: {{outcome line}}
- Options: {{at least two, one the simplest}}
- Evidence: {{measured, documented, standard practice or assumption}}
- Choice and why: {{}}
- How hard to undo, and what would change it: {{}}
- Confirmed by: {{owning engineer, date}}
