# Layer 0: Intake and sizing

**Answers:** What is the outcome in one sentence? How big is this? What already exists?
**Prevents:** Starting a deep process on a small change, a shallow one on a large one, and designing something the product already does.
**Output:** `00-start/brief.md` (partly), `10-world/existing-system.md` (medium and large), the workspace itself.
**Read first:** The user's request; the project's code and docs. No prior workspace docs unless resuming.

## How to generate

1. **Read before asking.** Skim the repo layout, README, relevant modules, recent git history, open tickets or docs the user points at. Keep reading until you can say how the relevant parts work today and what this change would touch. If the user named the sources to use, read only those (see "Source allow-list" below). If the baseline is large (tens of KB or more), have a read-only subagent digest it (see `session-protocol.md`).
2. **Find the mode** (`entry-modes.md`) and check for an existing workspace.
3. **Draft the one-sentence outcome** in the user's words: who does what, to get what. Not a solution ("add a queue"), an outcome ("clerks get approved invoices into the ERP without retyping").
4. **Size it** with the tripwires in `depth-sizing.md`. Say your size and the one or two reasons.
5. **Inventory what exists** (medium and large): data and models, permissions and tenancy, integrations and tools, tracing and logging, UI patterns, tests. For each, reuse, extend or avoid, and any surprise.
6. **Say back to the user**, in about 150 words: what they asked, who it is for and why as far as they said, what you found that bears on it, and anything that might change what they are asking for (a constraint, a conflict, a cheaper path). End with one line inviting correction, then one question about what the request leaves most open.
7. **Create the workspace** with `wsctl.py init`, fill the brief's outcome and size sections, set gate 0.

## Source allow-list

If the user limits the sources ("use only these two docs"), record them under Sources in the brief and stay inside them in every stage, including later sessions. Anything outside is an authorised exception only when the user says so; log it there with the date and what it was for. Need something else? Ask first, with what you would look up and why.

## Starter questions (only those the repo cannot answer)

- "Who will use this first, and what do they do today instead?"
- "Is there a deadline or an event this has to meet?"
- "Has anyone tried something like this before here? What happened?"
- "What is the one result that would make you say it worked?"

## Gate (layer 0 passed when)

- [ ] The user agreed with your one-sentence outcome (or corrected it and you restated).
- [ ] Size and mode are chosen with reasons, and recorded in the brief.
- [ ] You have read what exists well enough to say what the change touches.
- [ ] The workspace exists and `wsctl.py status` runs.

## Depth

small: the sentence and the size. medium: plus a half-page inventory. large: full inventory including who owns each neighbouring system.

## When it goes sideways

- **The request is a solution, not an outcome** ("add Redis"). Ask what problem it solves and for whom; record the solution as a `hypothesis` decision.
- **You cannot read the code or data** (no access, wrong environment). Record it as a risk and note which facts you cannot verify. See "no access" in the playbook.
- **The user arrives with a written brief or flows** (not open answers). Do not re-ask what it says. Extract outcome, users, steps and constraints into the docs, mark each statement `doc` and cite where it came from, then challenge it: gaps, contradictions with the allowed sources, unstated failure cases. The first round asks only about those, split into "needs your decision" and "my defaults". Their cases are likely `invented` until the user supplies real ones.
- **The user has a spec and wants it built.** Switch to rescue mode; treat the spec as a hypothesis. How to tell it from a written brief: a brief states requirements for something not yet built (extract and challenge, above); a spec of a design that has already drifted from a build, or that nobody can explain, is rescue.
- **Several features are bundled.** Split now; plan the first, park the others with the reason.
- **The scope is clearly tiny.** Use tiny mode and say what you are skipping.

## Hands off to

Layer 1: ask for two or three real situations.
