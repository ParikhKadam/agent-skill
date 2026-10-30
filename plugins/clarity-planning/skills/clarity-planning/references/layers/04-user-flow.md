# Layer 4: User flow and re-entry points

**Answers:** What does the user see and do from start to finish? What differs by role? What happens when things fail? And at every step: can the user **see** the intermediate result, **correct** it, **regenerate it alone**, or **skip** the step?
**Prevents:** Building a one-shot pipeline that cannot support the first thing users ask for: fix a wrong link, redo one part, bypass a step they already know. These needs look like polish and turn out to determine the architecture.
**Output:** `30-behavior/user-flow.md`.
**Read first:** Brief, cases, facts register, risks (`wsctl.py read-set <ws> understand`).

## How to generate

1. **Walk one real case end to end** (from the cases folder) as a story: what the user sees, does and gets back at each step. Keep it in plain language.
2. **Add the other paths:** alternate valid routes, what differs by role or permission, failure and recovery, leaving halfway and coming back, the same action twice.
3. **Run the four re-entry questions at every step.** For each step ask: see it? correct it? regenerate it alone? skip it? Write a row for each yes. These are not extras: each yes is a requirement that an intermediate result exists as a stored, nameable thing (layer 5).
4. **Ask who else touches it.** A second user, an approver, an admin, a downstream system. Their flow is part of this layer.
5. **List the re-entries you ruled out**, with the reason, so nobody reopens them by accident.
6. **Test against the cases.** Run each hand-written case through the story. Any gap is a finding.
7. **Name the artifact** for each re-entry row (use `ART-nn`; you will define them in layer 5). A re-entry with no stored result behind it is a design hole.

## Starter questions

- "After it shows the result, what would you want to change first?"
- "If it got this part wrong, how would you tell, and what would you do?"
- "Is there a step you would sometimes want to skip because you already know the answer?"
- "If you fixed that value, what else should change automatically?"
- "What if you leave halfway and return tomorrow?"
- "What do the other roles see here? Can someone without access still do this?"
- "What if two people do this at once? What if the same request comes twice?"

## Gate (layer 4 passed when)

- [ ] Each hand-written case runs through the story with no gap.
- [ ] Alternate paths, role differences, failures and recovery are covered at the depth the size needs.
- [ ] Every step has been asked the four re-entry questions; each yes is a row with an artifact named; each no that mattered is listed as ruled out.
- [ ] The user has read the story and recognizes it as how they would use it.

## Depth

small: the story in a few lines. medium: story plus alternate paths plus re-entry table. large: every role, every failure, leaving and returning, concurrency.

## When it goes sideways

- **The user describes the system, not the journey.** Pull back to a case: "start from when they open it".
- **Every step "might" be skipped or fixed.** Rank by how often; pick the two or three that matter; list the rest as ruled out or deferred.
- **Roles are unclear.** Draft a role table (who, what they can do, what they cannot) and ask for corrections.
- **The flow depends on a spike not yet run.** Write the branch both ways and mark it `hypothesis`; revisit when the spike returns.
- **The story contradicts a fact from layer 2.** Reopen layer 2; the story is not wrong because it is inconvenient.
- **Mobile, offline or multi-device matters.** Add the variant paths; do not assume the desktop story covers them.

## Hands off to

Layer 5: every row in the re-entry table needs an artifact behind it.
