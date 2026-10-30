# Layer 9: Contracts

**Answers:** What exactly crosses each boundary between teams or systems, including the stored artifacts others read? Who owns each side and what must they agree?
**Prevents:** Integration surprises: fields added mid-build, a callback nobody planned, a required name that the other side does not send, formats that differ by one detail.
**Output:** `40-design/contracts/K-*.md` (one per boundary), plus stubs.
**Read first:** System flow, artifacts, cross-cutting (`wsctl.py read-set <ws> contract`).

## How to generate

1. **List the boundaries.** Wherever two people, teams or systems meet: requests and callbacks, shared stored artifacts, events, files, UI-to-API calls. Each gets a contract.
2. **Write real examples, not descriptions.** For each: one **happy-path** message and at least one **failure** message, as actual payloads. A reader should see exactly what the other side must send and handle.
3. **State the rules around the examples:** required and optional fields, limits, idempotency key, ordering and retries, what is echoed back, what a missing field means, version and how it may change without breaking the other side.
4. **Name owners.** Who sends, who receives, who must agree before it is frozen. If the other owner is not in the conversation, write their question into `open-questions.md` with your recommended default.
5. **Write a stub for each side.** A tiny fake of the other party that returns the examples, so both teams build in parallel and you can run your component against the contract today. Include stubs in the plan's skeleton.
6. **Check the examples against the flows.** Does the payload carry what the flow needs? Anything missing (the owner's name, a stable id) is a finding that should surface now, not in week two.
7. **Freeze early, interior late.** Boundaries are agreed before building; internals stay free to change. Mark the contract `agreed` only when the other side has seen the examples.

## Standard practice

Apply the usual integration patterns deliberately: an adapter around the outside system, idempotency keys or check-before-act, explicit versioning, timeouts with backoff, tolerant readers that ignore unknown fields, and recorded-response tests. Verify the other side's real behavior by probing; do not trust its documentation for the details. Choose by what the other side actually supports and record the pattern and why. See `standard-practices.md`.

## Starter questions

- "Who sends this and who receives it? Who else reads it?"
- "What does the receiver need that the sender does not have yet?"
- "What if the same message arrives twice? What if it never arrives?"
- "How will this change in a year without breaking the other side?"
- "Can we both run against a fake of the other side tomorrow?"

## Gate (layer 9 passed when)

- [ ] Every boundary has a contract with happy-path and failure examples.
- [ ] Rules (required fields, idempotency, versioning) are written.
- [ ] Owners on both sides are named and the other side has seen the examples.
- [ ] Stubs exist or are planned in the skeleton, and each side can run against the other's stub.
- [ ] Missing fields found while checking against the flows are resolved or queued with owners.

## Depth

small: only if a boundary exists. medium: examples for each boundary. large: examples, rules, versioning, stubs for both sides, and a compatibility plan.

## When it goes sideways

- **The other team will not commit yet.** Write your side as a proposal with examples; use your stub; mark `draft`; set a date to revisit.
- **The other side's real behavior differs from its docs.** Probe it, record observed behavior, and write the contract to the observed behavior with a note.
- **You cannot see the other side.** Write it as a `PROPOSAL`: realistic example messages labelled `invented`, a question for the other owner, and a stub built from your proposal. Set the contract's status to `pending` until they have seen it; the gate can pass with the condition "owner reviews K-...".
- **A contract needs a new field mid-build.** Add it as an optional field first, version it, tell the other owner; log the change.
- **Too many contracts.** Merge boundaries that always change together; keep one per owner pair.
- **Contracts duplicate rules in two codebases** (checkers on both sides). Share fixtures: one set of example files both test against, owned by one side.

## Hands off to

Layer 10: the plan builds against frozen boundaries.
