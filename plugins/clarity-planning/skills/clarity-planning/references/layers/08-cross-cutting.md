# Layer 8: Cross-cutting concerns

**Answers:** Which of the concerns that cut across every feature apply here (access control, tenancy, audit, encryption, retention, idempotency, observability, cost, privacy, migration, rollout, operations, accessibility), and what each means for this design?
**Prevents:** A generic security checklist glued on at the end that misses the real rules, and the late discovery that an audit or retention requirement changes what must be stored.
**Output:** `40-design/cross-cutting.md` (or one file per concern for a large feature).
**Read first:** Artifacts, user flow, system flow (`wsctl.py read-set <ws> review`).

## How to generate

1. **Derive, do not append.** Permissions come from actors × artifacts × actions in layers 4-5: who may see, edit, regenerate, approve, post? Build that matrix first; many rules fall out of it ("the uploader may not approve their own").
2. **Give each concern a verdict:** `applies` (with a concrete consequence), `does not apply` (one-line reason), or `defer` (who decides, by when). Use the table in the template; add concerns the product needs.
3. **Walk the concerns against the artifacts and steps:**
   - **Access:** per artifact and action; what happens when the user lacks access to part of the input.
   - **Tenancy:** can one customer's data ever appear in another's results, caches, traces or logs?
   - **Audit:** which changes need who, when, before and after? Corrections, overrides, approvals, deletions.
   - **Sensitive data and encryption:** which artifacts hold it, at rest and in transit, in logs and traces, in prompts sent to models.
   - **Retention and deletion:** how long each artifact lives, who can delete, and what deleting an input does to artifacts derived from it.
   - **Idempotency and duplicates:** keys, where checked.
   - **Observability:** traces, metrics and alerts per component; what is never logged.
   - **Cost and latency:** budgets per run and per user; what happens at the cap.
   - **Privacy and compliance:** regulations that apply; consent; what leaves the system.
   - **Migration and backfill:** existing data that must be converted; coexistence with the old path.
   - **Rollout:** flags, who sees it first, rollback, how we notice trouble.
   - **Operations:** who is paged, what the runbook says, how to reprocess.
   - **Accessibility and languages:** if users need them.
4. **Spot the interactions.** Retention versus audit; encryption versus searchability; tenancy versus shared caches; per-user permissions versus stored artifacts others may read.
5. **Feed back.** A concern that applies may add an artifact (an audit record), a component, a field or a flow step. Update layers 5-7 and bump versions.
6. **Ask the owner for the policy questions you cannot decide** (retention periods, approval limits) with your recommended default.

## Standard practice

Each concern has well-known approaches (role-based versus relationship-based access, a central permission check, delegation as a recorded time-bound grant, append-only audit, tenant id enforced in one layer, a retention schedule, shadow-mode rollout). Name the one you propose, tie it to this feature's actors and artifacts, and mark it `hypothesis` until the policy owner agrees. For security, privacy, payments and regulated data, check current guidance from a primary source (the standard, the regulator, vendor docs), cite it with the date, and if you cannot search say the guidance is from memory and needs a check. See `standard-practices.md`.

## Starter questions

- "Who must not be able to see or do this? What happens if they try?"
- "If someone changes this after the fact, who needs to know and what is the record?"
- "Is there any data here someone would be upset to see in a log or sent to another company?"
- "How long must this be kept? Is there a time it must be deleted?"
- "What does the old system do today that we must not lose?"
- "If this goes wrong in production, who finds out first?"

## Gate (layer 8 passed when)

- [ ] Every concern in the table has a verdict with a reason; none is blank.
- [ ] A permission matrix (actors × artifacts × actions) exists, or "applies: no" is justified.
- [ ] Concerns that apply have a consequence stated (and the affected artifacts, components or flows updated).
- [ ] Policy questions are with their owners, with defaults.
- [ ] Sensitive data handling is stated for stored artifacts, logs, traces and model inputs.

## Depth

small: skip, but state anything sensitive in the brief. medium: verdict per concern in a line each. large: each applicable concern with its consequence, a permission matrix, and checks of interactions.

## When it goes sideways

- **The user says "security is handled elsewhere".** Ask what exactly is handled and what this feature adds (new data, new actors, new outside calls). Record the boundary.
- **A policy is unknown** (retention, limits). Open a question with a default; design so the value is configurable.
- **A regulation may apply and nobody knows.** Raise to the owner as a blocking question; do not guess.
- **Tenancy is weak in the existing system.** Existing-system surprise and a risk; decide whether this feature depends on it.
- **A concern would double the scope.** Defer with an explicit trigger and say what risk that leaves.

## Hands off to

Layer 9: boundaries with other people and systems become contracts.
