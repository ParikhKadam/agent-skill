# Standard practices

When there is no code to read, you still have a large body of established design patterns. Use them: they are the cheapest source of good alternatives and of failure cases nobody thought of. But a pattern is a **starting guess about the design**, not a fact about this product. This file says how to use patterns responsibly and lists the common ones by problem type.

## How to use a pattern

For each design problem (in layers 3 and 6-9):

1. **Name the problem in plain words**, then the established pattern or two that usually answer it.
2. **Say why it fits or does not**, against the facts recorded so far (the facts register, constraints, cases). A pattern that needs something a recorded fact rules out (for example "use the outside system's idempotency key" when it has none) does not fit, and the fact wins.
3. **Tag it in the decision** as `basis: standard-practice` and keep `confidence: hypothesis` until it has been tested against this product's data or a spike. Say what would show it does not fit.
4. **Do not copy a pattern's full machinery** when the feature is small. Take the smallest version that handles the failure you actually care about; say what you left out.
5. **Check currency for high-stakes items.** For payments, authentication, personal data, regulated domains, cryptography and anything irreversible, practice moves and rules change. If you can search the web, look up current guidance from a primary source (the standard, the regulator, the vendor's docs), cite it in the decision doc, and note the date. If you cannot, say that the guidance is from memory and mark it `[T]` (needs a check by someone who knows).
6. **Prefer the existing system's way** when one exists (see `existing-system.md`); a second pattern for the same problem is a cost.

Never present a pattern as settled because it is common. "Everyone does it this way" is a reason to try it first, not evidence that it fits.

## Catalog by problem type

Format: **Problem** | patterns | fits when | does not fit / watch out.

### Duplicates and retries
- **Idempotency key**: the caller sends a stable key; the receiver returns the first result for a repeated key. *Fits* when you control or can influence the receiver. *Watch out:* the receiver may not support it; keys must be stable across retries and scoped to the operation.
- **Check-before-act with a natural key** (look up, then act): *fits* when the other side offers a lookup but no key. *Watch out:* a small race between check and act; add a lock or a unique constraint on your side.
- **Unique constraint on your own store** (for example one record per owner and date): the cheapest duplicate guard you control.
- **Outbox**: write the intent to your own database in the same transaction, send it later and mark it sent. *Fits* when "saved but not sent" or "sent but not saved" would be harmful. *Watch out:* needs a reliable sender and a way to retry safely.

### Lifecycles and states
- **Explicit state machine**: list states, allowed transitions, who or what triggers each. *Fits* whenever an object has a status that more than one actor changes. *Watch out:* name the "stuck" states (waiting, failed, partial) and how each resolves; add a timeout or a manual way out.
- **Derived versus stored status**: store the facts, derive the label, when the label can be computed. Avoid two statuses that can disagree.

### Background and scheduled work
- **Queue plus workers**: for work that is slow, retryable or bursty. Decide ordering, concurrency, retry limit, and a dead-letter place for what keeps failing.
- **Scheduled job (generate ahead of a deadline)**: *fits* recurring work with a cut-off; run it with margin before the cut-off, make it safe to run twice, and report outcomes per item, not only "job ran".
- **Reconciliation report**: a periodic check that what should have happened did. Cheap insurance against silent failure.
- **Long-running work**: give the user progress or a notification; survive restarts; recover lost jobs.

### Who may do what
- **Role-based access (RBAC)**: roles map to permissions. *Fits* when rules follow job titles. *Watch out:* role explosion; delegation and "not on your own item" rules are not roles.
- **Attribute or relationship checks (ABAC and relationship-based)**: rules depend on the resource or the relationship (owner, same team, amount under a limit). *Fits* when "may approve up to X" or "only their own" appear in the cases.
- **Central permission check**: one place that decides, called everywhere. Avoid scattering checks.
- **Delegation**: a time-bound grant recorded with who delegated to whom; the audit trail must show the delegate and the delegator.
- Derive the rules from actors, artifacts and actions in the layer 4-5 docs; the pattern is only a way to implement them.

### Audit, history and data lifecycle
- **Append-only audit log** of who changed what, when, before and after; separate from the data and hard to alter. Decide which events qualify (corrections, overrides, approvals, deletions).
- **Soft delete versus hard delete versus retention schedule**: decide by legal and business need, and by what derived data depends on the deleted record.
- **Versioned records** when users need "what did it say then".

### Multi-tenancy and data isolation
- **Tenant id on every row and every cache key**, enforced in one layer (query filters or row-level security). Watch caches, search indexes, logs, traces and model prompts: leaks happen there first.

### Integrations with outside systems
- **Adapter plus stub**: wrap the outside system behind your own interface so you can test against a fake and survive its changes.
- **Contract examples plus a recorded-response test** for the real one.
- **Timeouts, retry with backoff and jitter, circuit breaker or a kill switch** for an unreliable or rate-limited partner. Decide what the user sees when it is down.
- **Anti-corruption mapping**: translate their names and codes to yours at the edge.
- Verify actual behavior by probing; documentation of other systems is often wrong in the details.

### Input, files and parsing
- **Validate at the boundary, keep the original**: store the uploaded file untouched, and the parsed result as a separate, correctable artifact.
- **Fall back to manual entry** when automatic reading fails; never block the user.
- **Size, type and malware limits** on uploads; keep sensitive content out of logs.

### Notifications and user trust
- **Tell the user before and after** anything automatic that affects them (reminders before a cut-off, a record of what happened). Silent automatic actions are the commonest source of lost trust.
- **Digest versus immediate**: choose by urgency and volume.

### Rollout and change safety
- **Feature flag per step** with a way back to the manual path.
- **Pilot with a few users first**; shadow mode (compute but do not act) when you want to compare before switching on.
- **Expand-and-contract migrations** for data shape changes: add, backfill, switch, remove.

### Observability
- **One trace per unit of work** with ids, timings, cost and the decision reason; metrics per component; alerts on user-visible failure states ("approved, not posted for over an hour"), not only on errors.
- Keep sensitive values out of traces and logs.

### Language-model and agentic steps
Details and reasoning are in `ai-components.md`; the patterns in short:
- **Autonomy ladder:** code first; one model call; one round of requested reads; tools in a loop last, each rung justified by measurement.
- **Structured output validation:** the model returns a fixed structure; code validates it (types, allowed values, totals add up) and rejects or repairs before anything acts on it.
- **Untrusted-input handling:** outsider-written content is data, never instructions; kept separate in the prompt; cannot widen tools.
- **Tool least-privilege:** an allow-list per agent; irreversible actions executed by code or confirmed by a person.
- **Model gateway:** one place that calls models, applies masking, logs inputs and versions, enforces budgets, and can switch provider or region.
- **Eval-gated release:** prompt, model or rule changes ship only after passing the fixed evaluation set; provider model updates trigger a re-run.
- **Masking before model calls:** remove or tokenize personal and sensitive fields the step does not need.
- **Decision trace:** per item, the inputs, versions, proposal, rule checks and final decider, stored as the audit record.
- **Grounding and partial repair:** check each claim against its source; redo only the failing items.

### Finance and approvals
- **Maker-checker (separation of duties):** the person or system that prepares an action cannot approve it; record both.
- **Tolerance matching:** match amounts and quantities within an agreed tolerance (absolute and percentage), with anything outside it going to a person; the tolerance is a decision with an owner.
- **Bank-detail change verification:** a change to payee bank details is verified out of band (a call to a known contact) and blocks payment until verified; a classic fraud path.
- **Duplicate-payment guard:** a unique key on supplier, invoice number and amount, checked on upload and again before posting.
- **Approval limits and delegation:** limits by amount and cost centre as data, not code; time-bound delegation recorded with both names.

### Search, ranking and matching
- **Exact rules first, fuzzy or learned matching only on the leftovers**, with a policy for wrong versus unhelpful. **Rank and offer; do not auto-link** when a wrong link is costly.

## Where this plugs into the layers

| Layer | Use |
|---|---|
| 3 Risks and decisions | Name the pattern as an alternative in each decision; tag `basis` |
| 6 Components | The pattern that shapes who decides inside, failure behavior, tool permissions for agents |
| 7 System flow | Retries, duplicates, states, background work, reconciliation |
| 8 Cross-cutting | Permission model, audit, tenancy, retention, observability |
| 9 Contracts | Idempotency keys, versioning, stubs, adapter |
| 10 Plan | Flags, pilot, shadow mode, expand-and-contract |

## What to record

In the decision doc: the problem, the pattern(s) considered, `basis: standard-practice`, why it fits or not against which facts, what you left out of the pattern, the source for any high-stakes guidance with its date, and what would show it does not fit. Confidence stays `hypothesis` until a spike, a test on real data or the owner's agreement says otherwise.
