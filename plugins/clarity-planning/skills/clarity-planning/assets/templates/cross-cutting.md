---
id: CROSSCUT
title: Cross-cutting concerns
layer: 8
kind: crosscut
status: draft
version: 1
updated: {{DATE}}
summary: A verdict for each concern that cuts across the feature: applies, does not, or deferred, and why
depends_on: [ARTIFACTS@1]
read_sets: [review]
---

# Cross-cutting concerns

## In plain words

Give every concern a verdict so none is skipped by accident. `applies` needs a concrete consequence. `does not apply` needs the reason in one line. `defer` needs who decides and by when. Derive permissions from actors, artifacts and actions (layers 4-5), not from a generic checklist.

| Concern | Verdict | Why | What it means for the design |
|---|---|---|---|
| Who may do what (authorization) | TODO | TODO | TODO |
| Tenant or customer isolation | TODO | TODO | TODO |
| Audit trail (who changed what, when) | TODO | TODO | TODO |
| Sensitive data and encryption | TODO | TODO | TODO |
| Retention and deletion | TODO | TODO | TODO |
| Idempotency and duplicates | TODO | TODO | TODO |
| Observability (traces, metrics, alerts) | TODO | TODO | TODO |
| Cost and latency budget | TODO | TODO | TODO |
| Privacy and compliance | TODO | TODO | TODO |
| Migration and backfill of existing data | TODO | TODO | TODO |
| Rollout, flags and rollback | TODO | TODO | TODO |
| Support and operations (who gets paged) | TODO | TODO | TODO |
| Accessibility and languages | TODO | TODO | TODO |
| Model and tool permissions (what each model step may read, write or trigger) | TODO | TODO | TODO |
| Untrusted content reaching a model (prompt injection) | TODO | TODO | TODO |
| Model provider and data residency (what may leave, to whom, where) | TODO | TODO | TODO |
| Prompt, model and rule versions (release gate, staleness) | TODO | TODO | TODO |
