# Layer 7: System flow

**Answers:** How do the components run in order from any starting artifact? What happens on failure, retry, duplicate and concurrent use?
**Prevents:** Failure behavior invented in production: duplicate posts, half-finished states, silent failures, the same job id twice, partial results stored as if complete.
**Output:** `30-behavior/system-flow.md`.
**Read first:** Artifacts, components, user flow (`wsctl.py read-set <ws> review`).

## How to generate

1. **Write the full run as numbered prose.** For each step: the component, the artifacts it reads, the artifact it writes, who decides inside, and what can run in parallel (steps with no dependency between them).
2. **Add the start points.** A full run starts at the input; each re-entry starts at a stored artifact. For each, list which components run and which are skipped. This is what makes "regenerate only X" ordinary instead of a new feature.
3. **Make skipping safe.** Where a stage can be skipped because nothing it depends on changed, define the **gate**: what is compared (a hash of the inputs and a logic version), what the decision is, and the reason code logged ("reused", "changed: transcript", "refresh requested"). A skipped stage must be visible, not silent, and a failure must never be reused as if it were a result.
4. **Failure table.** For each step: how it can fail (timeout, invalid output, outside system down, permission denied), what the user sees, whether it retries, and the idempotency rule. Decide what state the system is left in.
5. **Duplicates and concurrency.** The same request twice (same id returns the same job); two people at once (lock, last write wins, or reject); retries after a timeout; two runs started in the same second.
6. **Visibility.** What is traced, where a failure is reported, and who is told. A step that swallows an error and reports success is the worst case.
7. **Walk the cases and re-entries through it.** Every start point from layer 4 must run.

## Standard practice

Failure, retry and duplicate handling is where established patterns help most and where teams most often reinvent badly. Check the catalog in `standard-practices.md` for: idempotency keys or check-before-act, unique constraints you control, outbox, explicit state machines with named stuck states, scheduled jobs with margin and per-item outcomes, reconciliation reports, timeouts and backoff. Pick by what the outside systems in your facts register actually support, and record the pattern and why in the failure table or a decision.

## Starter questions

- "If this step fails after the earlier steps succeeded, what does the user see and what is saved?"
- "If the same request arrives twice, what should happen the second time?"
- "If an outside system is down, can the user continue without it?"
- "How long may a run take before we tell the user? What do we show while waiting?"
- "Who is told when something fails silently?"

## Gate (layer 7 passed when)

- [ ] The full run and every start point from layer 4 are written and traced through.
- [ ] Every step has a failure outcome the user can see and a retry or idempotency rule.
- [ ] Skip gates (if any) compare real inputs and log a reason code; failures are never reused.
- [ ] Duplicates, concurrency and partial failure are decided.
- [ ] Time and cost per run have budgets, and the flow says what happens at a cap.

## Depth

small: skip or two lines. medium: numbered flow plus failure table. large: plus every start point, skip gates, concurrency, budgets.

## When it goes sideways

- **A step's failure leaves a half state** (approved, not posted). Make that a named, visible state and decide how it resolves (retry, manual action, timeout).
- **Retries cannot be made safe** (the other system has no idempotency key). That is a risk: add a spike, or design a check-before-post using a stable key.
- **Parallel steps race on shared data.** Decide the owner of each write; make shared data an artifact written once.
- **The flow is a loop** (the model may go back). Cap trips, define what the node passes on at the cap, and ask whether a plain code path would do (see the ladder).
- **Long-running work.** Decide how the user waits (progress, notification), what survives a restart, and how a lost job is recovered.

## Hands off to

Layer 8: cross-cutting concerns attach to artifacts and steps now defined.
