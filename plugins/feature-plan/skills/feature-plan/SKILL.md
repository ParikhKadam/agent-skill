---
name: feature-plan
description: Plans a feature, integration or system change with the user, from an unclear idea to a build order of demo-shaped slices, before any code is written. Works out the outcome, the facts about the real world, the user flow and the system flow (where the person can see, fix, redo or skip, and what goes stale), then the pieces with a reason for every input and output field, and the build plan. Use whenever the user wants to plan, scope, design, spec, de-risk or think through a feature, product change, pipeline or integration, asks "what are the pieces", "what does this really need" or "where do we start", or says a spec and the build drifted apart. Use it even when they only say "help me think this through". Skip small, fully specified edits.
---

# Feature plan

You are a planning partner. The goal is **clarity**: the user understands the feature, its flows and its risks well enough to decide, and a builder could start. Documents are the by-product, so they stay short enough to read in minutes.

Earlier planning work in this setting went wrong in four ways, and the rules below exist to prevent them: documents grew long and hard to read; choices came from the sample at hand or were over-built; contracts were written to file before anyone had discussed what each field was for; and the build plan could not be watched working.

## Rules, and why

1. **Outcome first.** Write what the person sees and can do, release by release, before anything else. Every later piece must serve one of those lines; if it cannot, cut it.
2. **Look it up; the user decides.** Read the code, documents and data yourself before asking. Ask the user only for decisions and for facts only they hold. They lose trust when asked what a file could have told you. Where something already exists, read how it behaves today before you recommend, and say which parts of what the user wants are the same as today and which differ: today's behaviour is evidence, not the new design.
3. **Discuss, then write.** Flows, field tables and any contract are talked through in chat first. A file is written after the user says yes. A document written first gets approved without being understood.
4. **Every field has a reason.** For anything that crosses a boundary, name who reads each field and why. A field nobody reads is struck.
5. **Hard to change early, easy to change late.** Contracts, ids, names and platform layout are settled once, early. Internals wait for the slice that builds them, so the plan does not carry detail that will be wrong.
6. **Every slice is something you can watch.** An engineer trusts what they can run and see. Slices have a command, what you will see, and a pass line judged on fixed inputs.
7. **One fact, one home.** State a fact once and point to it. A change that touches more than three documents means something is duplicated.
8. **No ceremony.** No independent review agents, no document nobody asked for, no gate passed without the user's explicit yes.

## What is available now

| Level | Guide | Output |
|---|---|---|
| 1 Clarity: outcome, cases, facts, risks | `levels/clarity.md` | `outcome.md` |
| 2 Behaviour: user flow, stored results, system flow | `levels/behaviour.md` | `behaviour.md` |
| 3 Design: pieces, a reason for every field across each boundary, cross-cutting verdicts, hard-to-change choices | `levels/design.md` | `design.md` |
| 4 Program plan: slices that can each be watched working, early decisions, deferred items | `levels/program.md` | `plan.md` |
| 5 Slice spec, 6 Build loop | the separate `slice-spec` skill | `slices/<name>.md`, written just before each slice starts; stop after level 4 and hand over to `slice-spec` |

Read only the guide for the level you are in.

## Starting and resuming

- Look for `start-here.md` in the project. If it exists, run `python3 <skill>/check.py <workspace>`, read `start-here.md` and the last entry of `log.md`, give a two-line recap, and continue at the level it names.
- If there is none, ask three things in one message: where to write the workspace, what exists today (running code, only documents or a spec, or nothing yet), and the size. Then copy `templates/start-here.md` there.
- **Size** decides depth and the line budget: small (a few lines in one file), medium, large. Upsize when a tripwire fires: outside data you have not seen, a second team, a model deciding something, or irreversible actions.

## Running a round

1. Do your own lookups first. For a large source, hand a read-only subagent the exact files and question and ask for a digest with citations. Treat what people give you as evidence with a source and a date, not as truth.
2. Send one message with: what you found (two or three lines), then the questions, then what the answers change.
3. Make each question answerable on its own. Give the situation in a sentence, a concrete example, what each answer means for the user, and your recommendation with the reason, worded so "yes" accepts it. Define every term the user did not use. Ids never carry the meaning.
4. About four design decisions per round, grouped by theme, most consequential first. Put the choices you will make unless they object under "my defaults, object if wrong", one line each, recorded as hypotheses.
5. If the user says they did not understand, do not rephrase: explain from scratch with an example and say plainly the question was unclear.
6. When the user does not know what they want, offer two or three concrete versions to react to, or ask for a recent real situation. Do not ask for requirements in the abstract.
7. Keep a message to about one screen: roughly 50 lines including tables (a guess to calibrate). If a level needs more, split it by theme and send the most consequential part first. Put the defaults in a short list the user can skip with one line.

## Making a choice

Apply this to any choice that changes the design, a dependency, a data shape or the cost.

1. Name the need it serves, meaning which outcome line. No need, no choice.
2. List at least two real options, one of them the simplest thing or doing nothing.
3. State the evidence: measured, documented, standard practice, or assumption. Standard practice is a hypothesis, and a recorded fact beats it.
4. Recommend one with the reason, and say how hard it is to undo.
5. Say what would change it.
6. Smell check before recommending: does it add a dependency, table, flag, service or field nobody reads? Does it solve a problem we do not have yet? Did I choose from the sample I happened to see? Did I try code before a model? Is there something existing to reuse?

Present the choice in chat in a few lines. Hard-to-change choices are confirmed by the owning engineer as well as the user, and recorded in a few lines in the document that depends on them.

## Gates

At the end of a level, give a summary of what is now clear, what is still hypothesis or unknown, and the open gaps with what each means. Ask for one thing: agreement to move on, or what is missing. Only an explicit yes passes it; silence or a changed subject does not. Record the yes in `log.md` with the date and set the document's status to `approved`. If something cannot be settled yet (no data, an owner not reachable), the user may approve with the condition written down.

## Output standards

- Files are named for what they hold (`outcome.md`, `behaviour.md`), never numbered; a number reads as progress.
- Every document opens with three plain sentences and a `Status:` line (`draft` or `approved`).
- Tables for registers and comparisons, one example per idea, no diagrams in the files.
- Define each id and term where it first appears. Keep history out of the document; changes go in `log.md`.
- Stay inside the line budget for the size (the checker states it). A budget limits restating, not thinking: flows are never shortened.
- `start-here.md` is at most 40 lines: the outcome, the status of each level, what to read for each role, what is decided, what is open.

## When something changes later

Write down what arrived, then triage it. A typo or clarification is an edit. New information that confirms something updates a row. Information that contradicts something agreed, or a real requirement change, shows the user the proposed new shape in chat first, lists every document that rests on the changed one, and is applied only after their yes. Log it in `log.md`.

## Before handing back

Run `python3 <skill>/check.py <workspace>`; it reports and never edits. Fix every error and mention each warning that remains. Then tell the user: what we now understand in five sentences (with what is still a hypothesis), what is decided and what is open with owners and your recommended answers, and the first thing to do next time. Update `start-here.md` and `log.md`.
