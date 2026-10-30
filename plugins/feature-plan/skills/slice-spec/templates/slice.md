# {{Slice name}}

Status: draft

In plain words: {{what becomes real in this slice, and what the user can do after it that they could not before}}

Plan entry: `plan.md`, slice {{name}}. Design rows used: {{boundary and decision names}}. Owner: {{engineer}}.

## Demo

Run: {{command}}

You see: {{what appears}}

Pass when: {{the number, on fixed inputs}}

## Findings from the code

{{what exists today for this slice: reused, changed, new}}

## Files to inspect

{{path: why}}

## Files to change

| File | Change | Why |
|---|---|---|

## Smallest implementation

{{a few sentences: what is added, what is reused, what is left alone}}

## Configuration and migrations

{{each setting with its default; each schema change as add, switch, drop with the way back and its test; hard or easy to change}}

## Tests and verification

{{unit and integration tests, fixtures, and how to run the demo}}

## Non-goals

{{what this slice must not do}}

## Decisions made here

{{one line each}}

## Questions for the owner

| Question | My recommended answer |
|---|---|

## Ready

- [ ] Every slice and decision this slice needs has passed or is confirmed by its owner.
- [ ] No significant decision is left for the builder (data shape, interface, dependency, errors, concurrency, security, configuration, deployment, tests).
- [ ] Files to change and non-goals are listed.
- [ ] The owning engineer has approved this spec.

## Completion report

Not built yet. When the slice is built, set Status: done and write here: what changed; why the design is appropriate; which abstractions were added and why; the tests and checks run; remaining concerns.
