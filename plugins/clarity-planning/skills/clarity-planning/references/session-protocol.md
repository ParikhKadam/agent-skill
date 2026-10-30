# Session protocol

How a planning session actually runs: what a round looks like, how to talk, how to record, how to resume.

## Tone and level

Plain language, pitched a little above the user's own vocabulary. Be clear and concise; lead with what matters. If you must use a term the user may not know ("idempotent", "tenant", "SLA"), give a short definition the first time. Match their vocabulary for their own domain. Prefer plain names for the steps ("the facts step", "the pieces", "the build plan") over "layer 2" or "gate"; naming the step is fine when telling the user what is open. Never quote this skill at them; talk about what you are trying to find out.

## Anatomy of a round

A round is one message to the user containing:

1. **What I found** (only if relevant, two or three lines): facts you looked up that bear on the questions.
2. **What I changed in the docs since last time** (one line).
3. **The questions**: numbered, each with a title, a short body, and a recommended answer, and each understandable without opening any doc (see "Make every question answerable on its own").
4. **What the answers will change** (a sentence), so the user sees why.

**Round size follows the frontier, not a fixed number.** Ask every question that is unblocked now, meaning none depends on the answer to another in the same round. For a real layer that is usually around ten (a few more or fewer is normal). A question that depends on another waits for the next round. Ten answers in one go beat five rounds of two: the user answers in one sitting and you spend fewer turns.

Make a long round easy to answer:

- **Group by theme** under short headings (for example "Users", "Data", "Failure"), most consequential theme first, so the user can answer one theme and come back for the rest.
- **Put the recommended answer on every question** so most replies are "yes" or a one-word correction. Accept replies like "1-6 yes, 7 no because...".
- **Mark the ones that matter most** (a star) so a busy user answers those first and you proceed on the defaults for the rest, recording them as hypotheses.
- **Above about twelve questions**, star the ones that truly need the user's decision and move the rest under "my defaults, object if wrong".
- **Past about fifteen**, you are probably mixing layers or asking things you could look up. Cut what you can find yourself, then split what remains into two themed rounds.
- **If the user answers only some**, record the rest as open questions with your default and continue; do not re-ask them next round unless the answer would change the next layer.

### Two parts: what needs them, and your defaults

Most of a round should not need the user. Split it:

1. **Needs your decision:** only questions whose answer changes the design and that only the user (or someone they can ask) knows. Each has your recommendation.
2. **My defaults, object if wrong:** a compact list of the choices you will make unless they say otherwise ("I'll treat a no-show as a missed appointment with no cancellation"). One line each. Silence on this list means accepted, recorded as `hypothesis`.

Questions you could answer by looking something up never appear in either part: look them up. A "does this match?" question is not a round question; it is the gate, asked once when the layer is done. When a gate and the next round are both due, put them in one message so a single reply can approve and answer.

### Format

```
Found: the product already has suppliers and purchase orders, but no invoice concept.
Updated: added two facts to the register (F-03, F-04).

Q1. Matching: when an invoice has no PO number, what do clerks do today?
   My guess: they search by supplier and amount, then pick the PO by eye.
   -> If that's right, matching can be rule-based first, with a person picking the leftovers.

Q2. Approval: who may approve their own team's invoices?
   My guess: nobody; the uploader can never approve their own.
   -> Reply "yes" to accept.

These decide whether matching needs a fallback and how approval rights are modelled.
```

Word each question so "yes" accepts your recommendation. If you have no recommendation, say what you would need to form one.

### Make every question answerable on its own

A question that only makes sense to someone who has read your docs will not be answered, or will be answered wrongly. Before you send a round, **re-read each question as a person who has not opened any workspace doc** and fix it until it passes:

- **Define every term that lives only in the docs** (a part's name, "flag", "retention", "fingerprint", "context pack", "paged") in one plain line the first time, or replace it with plain words. Ids (Q-26, D-007, ART-09) may follow in brackets for the record but never carry the meaning.
- **Give each question four things:** the situation in one sentence, a concrete example, what each answer means for the user (what they will see or have to do), and your recommendation with the reason. "Default: yes" without the thing defined is not a question.
- **Be most careful with infrastructure, policy, security and data questions** (queues, retention, access, tracing, rollout, alerting). Say who normally decides, why you are asking now, and that "not sure, decide later" is fine, with what happens meanwhile.
- **Limit technical-decision questions to about four per round** unless the user asks for more, and group by decision, not by layer. A round of eight bare design questions reads as a wall.
- **Check the user's own words.** If they described the design differently from your question (their idea was a shared queue, your question assumed HTTP), ask in their frame first and present your alternative as an alternative.
- **If the user says they did not understand,** do not rephrase with the same words: explain each question from scratch with an example, say plainly that the question was unclear, and log it in the skill-monitor or session notes so it can be improved.

Bad: "Q28: the context pack lives only in Landi's Redis for 2 hours. Agree?"
Good: "Q28: To write insights, Landi reads live facts from Bullhorn about the people on the call (status, last notes, open submissions). Should we keep that bundle after it is used? If yes, regenerating insights could reuse stale data and we would store a second copy of CRM data; if no, every regenerate reads Bullhorn fresh. I recommend no, because it is always cheap to refetch and nothing sensitive is stored. Reply yes (do not keep it) or no."

## Delegating large reads

When a source is large (tens of KB or more) or a lookup is self-contained, hand it to a read-only subagent: name the exact files or question, say it must not edit anything, and ask for a digest with citations (file and section). Record what it returned as facts with status `doc`. Subagents obey the same source allow-list as you; list the allowed sources in their prompt.

## Rules for asking

- **Look up before asking.** Facts in code, docs or data are your job.
- **Open before closed.** Early on, let them describe in their own words; their phrasing carries intent that your options cannot. Offer a short menu only when they are stuck.
- **When they say "just guess" or "what do you think?"**, propose something concrete and move on. Mark it `hypothesis`.
- **Offer reconnaissance.** When looking further would help (deeper in code, their data, the web), say what you would look for and let them decide.
- **Never ask the user to produce a document.** You write; they correct.
- **Do not interrogate.** If the user seems tired or is giving short answers, summarize, record what is open, and stop at a clean point.

## Recording as you go

- Each new fact goes in the facts register the moment you learn it, with a status.
- Each choice goes in a decision doc, with confidence set honestly. Reversible small choices may share one decision doc ("small choices").
- Each question you cannot answer goes in `open-questions.md` with an owner and your recommended answer.
- Anything the user said that does not fit a doc yet goes in `90-log/sessions.md` so it is not lost.
- Bump `version:` in a doc's front matter when its meaning changes (not for typos), and update `updated:`.

## Presenting a finished layer (the gate)

When you believe a gate is met:

1. Summarize in plain words what is now clear (three to six lines).
2. Say what is still a hypothesis or unknown and what you will do about each.
3. Point at the evidence for each gate item.
4. Ask for one thing: agreement to move on, or what is missing.

Then mark it in `90-log/gates.md`. If the user wants to move on before a gate is met, see the "skip ahead" case in the uncertainty playbook.

## Reopening a layer

When something you learn contradicts a recorded layer:

1. Say so plainly: "This breaks something we agreed in the user flow."
2. Run `wsctl.py impact <workspace> <id>` on the doc that changes.
3. Edit the earliest affected doc, bump its version, then reconcile the docs that rest on it and update their pins.
4. Add a row to `90-log/change-log.md`. Set the gate of the earliest layer touched back to `in-progress`.

## Resuming

At the start of every later session: run `wsctl.py status`, read the last entry of `90-log/sessions.md`, and open with a two-line recap ("Last time we settled X; we were waiting on Y") before asking anything. If the user brings new information, add it to `sessions.md` first, then decide which layer it touches.

## Unattended runs (no human available)

Sometimes you are asked to plan when nobody can answer: a batch job, or the user says "I can't chat, use what I gave you". The method still applies, with these rules:

- **Use what the user provided; do not invent answers.** For everything else, record an open question with an owner and your recommended answer, proceed on it, and mark dependent decisions `hypothesis`.
- **Never mark a layer `passed`.** A gate needs the user's agreement or measured evidence, and unattended you have neither. Leave gates `in-progress` and write in the notes what each one is waiting for (`wsctl.py gate <ws> <layer> in-progress --notes "..."`).
- **Never mark a doc `agreed`.** Leave docs `draft`.
- **Label everything you could not verify**: facts `doc` or `unknown`, invented examples `invented`, contracts `PROPOSAL`.
- **Do the cheapest useful depth.** Thin docs are fine where nothing is verified; the point is a clear record of what is known, what is assumed and what to ask first.
- **End with a hand-off** in `90-log/sessions.md`: the assumptions you proceeded on, the questions to ask first, and the first step when the person returns.

## Pacing

- A small feature may finish in one session. A large one takes several; end each at a clean gate or with a clearly recorded next step.
- Do not spend a whole session polishing one layer. Reach a good-enough gate, move on, and let later layers tell you what needed more care.
- Offer a break point whenever a spike or an external answer is needed.

## Working with other people's input

If the user has limited the sources, that limit comes first: do not read or search outside the Sources list in the brief, even to be helpful. When they authorise one extra lookup, do it, then add it under Sources as an exception with the date and purpose.

The user may bring in teammates' notes, tickets, screenshots or specs. Treat them as evidence with a source and a date, not as truth. Add them to the facts register with status `doc` until checked. If the material is long, summarize what it settles and what it leaves open, and cite it from the docs instead of copying it.
