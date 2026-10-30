# Level 3: Design

**Resolves:** what the pieces are, what exactly crosses each boundary and why, which cross-cutting rules apply, and which hard-to-change choices must be settled now. **Output:** `design.md`. **Needs:** `outcome.md` and `behaviour.md` approved.

The failure this level prevents is a contract written to a file and approved before anyone knew what each field was for, and a design that cannot be built piece by piece. Nothing here is written until it has been talked through.

## Steps

1. **Find the pieces.** Start from the stored results and start points in `behaviour.md`. Each stored result gets one producer. Keep a piece separate only if one split test holds: the person can see, fix or redo its output; it needs its own quality bar and test set; its inputs go stale at a different rate; or it has a different owner, cost or failure mode. Otherwise merge it into a neighbour. Too many pieces is its own failure.
2. **Read what exists, per piece.** Where code or a system exists, read how each piece behaves today before deciding. List each piece as *reused*, *changed* or *new*. Look especially for places where today's code contradicts the behaviour you agreed (a step that reads an input the new design says it should not, a limit the design assumes is gone). Report each to the user as a finding.
3. **Discuss the inputs and outputs, boundary by boundary, in chat.** A boundary is wherever two people, teams or systems meet: requests, callbacks, shared stored results, files, screen-to-service calls. Design each from the behaviour already agreed, not from how the existing interface happens to work today. Keep today's interface only where it fits, and say so. For each boundary, show a table with a row per field: *Field | Read by | Why it exists | Where it comes from*. Add one real happy-path example and at least one failure example as text. Ask the user, and the owning engineer for the other side, to keep, change or strike each row. A field with no reason is not written. A field nobody on your side reads is a candidate to strike, but before striking one that the other side's code might read, ask its owner; until they answer, mark it *struck, pending*. Do not create a contract file or a component file until the table is approved.
4. **Decide who decides inside each piece:** code, a model or a person. Start at code. A model is justified only where code measurably fails; record what the code step achieved and what is left over. Mark the choice a hypothesis until measured. For model-backed pieces say how output is validated and what happens when it is invalid.
5. **State the quality bar and how each piece runs alone.** For each piece: what counts as correct, the number, the fixed test set, and the command or harness that runs it from stored input. If it cannot run without the rest of the flow, the boundary is wrong.
6. **List failure modes and cost per piece:** what it returns when it fails, what the person then sees, time and money per run.
7. **Give every cross-cutting concern a verdict with a reason:** who may do what, isolation between users, audit, sensitive data and encryption, retention and deletion, observability, cost, rollout and rollback, risks from model output or untrusted content, privacy and compliance. Each is *applies*, *defer* (with an owner and a trigger) or *not applicable* (with why). Derive permissions from who acts on which stored result, not from habit. For payments, authentication or personal data, check current guidance from a primary source.
8. **Record the hard-to-change choices** (names, ids, message formats, storage layout, queue or platform layout, anything other teams will build against). Use the choice protocol in `SKILL.md`. Each gets a few lines: the need, the options (one of them the simplest), the evidence, the choice, how hard it is to undo, what would change it. The owning engineer confirms each; the user confirms the ones that change scope or cost. Easy-to-change choices wait for the slice that builds them.
9. **Check the design against the behaviour.** Every start point in `behaviour.md` runs through the pieces; every stored result has a producer; every line of each case's ideal result maps to a field. A gap that changes agreed behaviour goes back to level 2, not around it.

## Discuss, then write

Send the tables in chat, a boundary at a time, with your recommended answer for every row the user might doubt. Keep each message to about one screen. Write `design.md` after the yes, and write the examples then too.

## Gate: the user and the owning engineers agree that

- every stored result has a producer and every piece passes a split test;
- every boundary table has been discussed; every field has a reader and a reason; no field is still *struck, pending* an answer from the other side (or the approval carries that as a condition);
- each piece has a quality bar, a way to run alone, and a failure outcome;
- every cross-cutting concern has a verdict;
- every hard-to-change choice is recorded and confirmed by its owning engineer;
- the design runs every start point and every case.

If an owning engineer is not reachable, the user may approve with the condition written down: the choice stays a hypothesis and the program plan makes confirming it an early slice.

## Depth

Small: skip, or one table of pieces. Medium: one line per piece, a table per boundary, verdicts in a short table. Large: everything above in full.

## `design.md` contains

The pieces (reused, changed or new); one table per boundary with *Read by* and *Why*, and its examples; who decides inside, quality bar and how it runs alone, for each piece; failure and cost; the cross-cutting verdicts; the decision records. Use `templates/design.md`.
