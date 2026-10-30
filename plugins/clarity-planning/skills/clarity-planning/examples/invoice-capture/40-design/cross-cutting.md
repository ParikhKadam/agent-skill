---
id: CROSSCUT
title: Cross-cutting concerns
layer: 8
kind: crosscut
status: agreed
version: 1
updated: 2026-10-28
summary: A verdict and a consequence for each of 13 concerns; approval rights, audit of overrides, bank-detail handling and retention matter most
depends_on: [ARTIFACTS@2, D-004@2]
read_sets: [review]
---

# Cross-cutting concerns

## In plain words

Permissions were derived from who does what to which artifact (the matrix below), not from a generic list. Audit and bank-detail handling are the concerns that changed the design.

### Who may do what

| Actor | ART-01 to ART-03 | ART-04 approval | ART-05 post |
|---|---|---|---|
| Clerk | See, correct, regenerate | Cannot approve; sends for approval | See; retry |
| Manager | See | Approve or reject within limit | See |
| Delegate | See | Approve within the delegator's limit; recorded as delegate | See |
| Uploader of this invoice | As clerk | Never approves their own | See |

### Verdicts

| Concern | Verdict | Why | What it means for the design |
|---|---|---|---|
| Who may do what (authorization) | applies | Money movement | The matrix above; the limit check lives in one place |
| Tenant or customer isolation | applies | Several companies | Every artifact carries a tenant id; coding history is per tenant |
| Audit trail | applies | Finance requirement | Record every correction, override, match pick, approval, void and post with who and when |
| Sensitive data and encryption | applies | Bank details and amounts | Encrypt PDFs at rest; never send bank details to the model; keep them out of logs |
| Retention and deletion | defer | Policy unknown (Q-1) | Make retention configurable; default seven years |
| Idempotency and duplicates | applies | Anti-goal in the brief | Hash on upload; check-before-post (D-002) |
| Observability | applies | Need to find failures | Trace each component with invoice id, time, cost; no invoice content |
| Cost and latency budget | applies | A model reads PDFs | Under 10 seconds and a few cents per invoice; cap per day |
| Privacy and compliance | applies | Supplier data | Data stays in region; PDFs are not used to train anything |
| Migration and backfill | does not apply | New concept, no old data | None |
| Rollout, flags and rollback | applies | Money | One flag per slice; start with one company; switch off returns to manual entry |
| Support and operations | applies | Posting failures | Alert when "approved, not posted" lasts over one hour |
| Accessibility and languages | defer | English only in version 1 | Revisit with the pilot |
