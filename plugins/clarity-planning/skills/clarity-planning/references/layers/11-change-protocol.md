# Layer 11: Change protocol

**Answers:** When a requirement changes (or something learned during the build contradicts a plan), what gets reopened, and how do the docs stay true?
**Prevents:** Rewriting everything, or worse, patching code while the docs rot; reopening decisions already settled; losing the reasoning behind a choice.
**Output:** `90-log/change-log.md`, updated docs with bumped versions and pins.
**Read first:** The change-request reading path (`wsctl.py read-set <ws> change-request`).

## First: triage the update

Not every update is a requirement change. New information, small tweaks and real changes need different amounts of work. Before touching anything, log it in `90-log/sessions.md` (so it is not lost), then decide which of these it is:

| Kind | Example | What to do |
|---|---|---|
| **A. Clarification or typo** | A name, a wrong number copied, a sentence unclear | Edit the doc. No version bump, no pins, no log entry |
| **B. New information that confirms or sharpens** | A measured rate replaces a guess | Update the row (status `measured`), `bump` it if its meaning got firmer. Nothing downstream changes |
| **B2. An open question is answered** | The owner answers Q-n | Close the row; update the decision it fed. If the answer matches the recommended default, update the docs that mention it (`wsctl.py impact <ws> Q-n`) from "default" to "decided" and stop. If it differs, it is C |
| **C. New information that contradicts** | A fact is not as recorded; a spike result flips a decision | Treat as a change: run `impact`, reopen the earliest layer it touches |
| **D. Small plan tweak** | A threshold, a slice's order, a flag name | Edit the plan doc or slice and `bump` it if the exit check or scope changed; check whether the slice's dependents care |
| **E. Requirement change** | A new user type, a new input, a dropped feature, a non-goal that becomes a goal | The full protocol below, starting at the brief (layer 1) when a non-goal or goal changes |
| **F. Scope or outcome change** | The valuable part is not what we thought | Back to layer 1; re-size; expect most layers to reopen |

When unsure between B and C, ask: "does this contradict something the design decided?" If it only replaces a default or a guess with the same answer, it is B; if a decision or a design element must change, it is C. When unsure between D and E, ask: "would a user notice?" If yes, it is E.

**Information that arrives during a conversation** (a remark, a screenshot, a new ticket) goes through the same triage. Say which kind you think it is and what you will touch; for C, E and F, get the user's agreement before reworking.

**Mechanics.** `wsctl.py bump <ws> <id>` records that a doc's meaning changed (version + 1) and lists the docs that rest on it. Each of those shows as *possibly stale* until you read it against the change, edit it if needed, and run `wsctl.py pin <ws> <its id>` to point its pins at the current versions. Never pin without reading; that hides staleness instead of resolving it.

**Reopen what actually changes.** Reopen every layer whose docs you edit, not only the earliest; leave untouched layers alone. Use `wsctl.py impact <ws> <id>` on the changed doc **or table row** (for example `ART-02`, `F-07`, `Q-1`): it lists docs that rest on it or mention it, which is a short, usable reread list. `--deep` follows whole-doc dependencies further and is usually too broad. After the rework, `wsctl.py check` warns about any passed gate whose evidence changed after it passed: re-confirm it with the user or reopen it.

## How to run a change

1. **State the change in one sentence** and the reason (new requirement, a spike result, a build surprise, a stakeholder decision).
2. **Find the earliest layer it touches.** A new user need usually touches layer 1 or 4; a data surprise, layer 2; a new input, layer 5; a new boundary, layer 9.
3. **Run `wsctl.py impact <ws> <id>`** on the doc that changes. That lists every doc resting on it, with layers.
4. **Use the staleness table** (artifacts) to see which artifacts and components are affected and which are untouched. Unrelated decisions are left alone.
5. **Rework from the earliest layer downward.** Edit the doc, bump its version and `updated`, then read each dependent doc, edit if needed, and update its pin to the new version. Docs you read and found still true get their pin updated too.
6. **Check the plan.** Which slices change? Which exit checks change? Which deferred items become needed?
7. **Record it** in `change-log.md`: date, what and why, earliest layer, docs reopened, outcome. Set the gate of the earliest layer touched to `in-progress` until reconciled.
8. **Run `wsctl.py check`** until no "possibly stale" remains, then `index` and `html`.

## Starter questions

- "What changed, and why now?"
- "Does this replace something we decided, or add to it?"
- "Is anything already built that this invalidates?"
- "Is this change big enough to resize the work?"

## Gate (layer 11 passed when)

- [ ] `wsctl.py impact` works on the docs (ids and pins are in place).
- [ ] The change log is in use; each change names what it reopened.
- [ ] No "possibly stale" warnings remain after a change.
- [ ] Superseded docs are marked `superseded` and point to their replacement.

## Handling common changes

| Change | Typical path |
|---|---|
| A new kind of user or role | Layer 1 case, layer 4 flow, layer 5 permissions in artifacts, layer 8 matrix |
| A new input channel (email as well as upload) | New input artifact and intake component (layers 5-6); matching onward is untouched |
| A policy changes (retention, limits) | Layer 8 consequence; check which artifacts store what |
| A spike shows a step cannot be code-only | Layer 6 component rung; decision with measured evidence; plan slice |
| An outside system changes its API | Layer 9 contract version; stub; slice for adapting |
| The user wants to drop a feature | Mark dependent docs `superseded` or `parked`; update deferred; keep the reasoning |
| The change doubles the scope | Re-size; split into slices; defer the rest with triggers |

## When it goes sideways

- **A change contradicts a decision someone fought for.** Do not hide it. Show the evidence, the tripwire that was recorded, and ask the owner. The decision doc's "what would change this" exists for this moment.
- **The change arrives as a verbal comment.** Put it in `sessions.md` first, then run the protocol so it does not vanish.
- **Docs and code have already diverged.** Switch to rescue mode and reconcile before applying the change.
- **Everything seems to be affected.** The dependencies are too coarse or too many. Narrow pins to what each doc really relies on; the earlier layers are probably the thing that changed.
- **Stale warnings multiply.** Do the earliest ones first; many clear themselves once the root doc is reconciled.
