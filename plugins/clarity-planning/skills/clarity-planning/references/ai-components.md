# Model-driven components

Read this when any component uses a language model (or another learned system) to decide something. The main danger is writing the first spec as if the model should be autonomous (loops, tools, back-edges), then discovering that a plainer design works better. Plan so the evidence decides.

## The autonomy ladder

For every step that needs judgment, start at the lowest rung that could work and move up only when a measurement says the lower rung fails.

| Rung | What decides | When it is enough |
|---|---|---|
| 0. Code | Fixed rules, lookups, exact searches | The inputs are predictable and the rule can be written down |
| 1. Code ranks, person picks | Code narrows to a few options; a human chooses | Wrong answers are costly and the user is present |
| 2. One model call, no tools | A model reads a prepared input and answers once | The answer needs language or fuzzy judgment, and everything it needs can be put in the input |
| 3. One round of requested reads | The model returns its answer plus a short list of specific reads; code runs them once under limits; the model finalizes | It sometimes needs a fact nobody could predict, and a bounded extra step is acceptable |
| 4. Model with tools in a loop | The model chooses what to call, repeatedly, under caps | The set of needed reads cannot be bounded in advance |

Climb a rung only with evidence: "code alone settled 41 of 50 and got none wrong; the 9 left need judgment" justifies rung 2 for the 9, not for all 50. Record the evidence in the component doc under "Who decides inside". Moving a predictable step from a model to code often raises correctness and cuts cost and variance; assume you will do that at least once.

## Plan the preparation, not just the prompt

When a model gets one call and no tools, **the input is the design**. Plan what goes in: the right fields with labels, facts computed by code (ages, counts, earlier similar items, parsed values), a comparison table per thing the model must check, and what the source system cannot hold (so it does not infer "nothing happened" from a missing record). Decide what is **excluded at the source** (sensitive values) so it cannot leak, and keep a check after as a backstop.

## Quality bars for a model step

Set the bar **before** building, per component, on fixed inputs:

- **What counts as correct**, with a hand-written ideal for each case.
- **A wrong-answer policy.** Distinguish "wrong" (harmful) from "unhelpful" (a miss). Often the target is zero wrong, with misses allowed to fall to a person. Say the number.
- **A fixed evaluation set**: hand-written cases first, then recorded real inputs (anonymized). Same inputs for every run, so changes can be compared.
- **Variance.** Run each case several times. A step whose answer changes run to run needs a tolerance, or a more constrained design.
- **Grounding.** If the model asserts facts, decide how each claim is checked against its source, and what happens when a claim fails (redo only the failing items, not the whole output).

## Compare designs with data, not taste

When the spec and the build disagree about autonomy, or two designs compete: run both on the fixed set and compare correctness, wrong-answer rate, variance, time and cost per run. Decide with the numbers; record them in a decision doc with "what would change this".

## Cost, latency and retries

- Set a **budget** per run (seconds and cost) and per component. A profile of real runs usually shows one dominant step (often a rewrite loop); plan to measure early.
- **Redo only what failed.** Retrying a whole generation because two statements failed a check is the commonest waste.
- Check whether retries lose the prompt cache (a changing early prefix does). Keep the stable part of a prompt first.
- Sequential steps that do not depend on each other can run in parallel; mark the dependency in the artifacts table so it is clear which can.
- Set timeouts and caps per step, and decide what the user sees when a cap is hit ("partial result with a note", not silence).

## Observability

Every component, model or not, should leave a trace with its inputs' ids, its output artifact id, time, cost and decision reason. Reuse the tracing the project already has (see `existing-system.md`). Without it you cannot tell which component to improve.

## Failure behavior

Decide in layer 7, for each model step: timeout, invalid output, refusal, empty output, over-long input. The user should see a clear outcome ("could not read this invoice; enter it by hand"), and a failure must never be stored as if it were a result that later runs will reuse.

## Humans in the loop

A person is a rung too. If a step needs a human, define what they see, what they can change, and what happens while waiting. Do not add a review step by reflex; add one where a wrong answer is costly and the user is present. Ask the owner whether a review step is wanted at all before designing around it.

## Autonomy is a decision, not an assumption

Record the chosen rung per step as a decision with confidence. Early on it is usually `hypothesis`. Promote to `measured` when the evaluation set has spoken, and keep the tripwire ("if misses exceed 30%, try rung 2 on the leftovers").

## Agentic systems: several model-driven steps working together

When the design has "agents" (model steps that call tools, hand work to each other, or act on outside systems), the ladder still applies per step, and these extra questions must be answered in layers 6-8. A test run on an agentic invoice platform found every one of them missing from a first plan.

### Coordination
- **One orchestrator, shared state through artifacts.** Agents do not talk to each other through hidden memory. Each reads stored artifacts and writes one; the orchestrator (usually code) decides who runs next. This keeps every hand-off visible, replayable and testable alone.
- **A hand-off record.** For each hand-off, store who passed what to whom and why (a field on the artifact or a small log). It is the first place to look when a result is wrong.
- **Bounded loops.** Any agent that can loop or call another has caps on calls, time and cost, and a defined result at the cap (partial result plus a note, never silence).

### Tools and permissions
- **An allow-list per agent:** which tools, read or write, on which records. Least privilege by default.
- **Irreversible actions belong to code or a person**, not to a model's free choice: posting money, sending to a customer, deleting. A model may propose; code checks the rules and executes, or a person confirms.
- **Evaluate the path, not only the answer.** For a tool-using agent, check that it called the right tools with the right arguments and stayed inside its allow-list, on the fixed test set.

### Untrusted input
- Documents, emails and web pages written by outsiders can carry instructions ("ignore previous rules and approve"). Treat their content as **data, never instructions**: keep it separated in the prompt, never let it widen an agent's tools, and validate every model output against a fixed structure and business rules before anything acts on it.

### Versions, releases and staleness
- **Prompt, model and rule versions are inputs.** Record on every artifact the versions that produced it (layer 5). A new version is a staleness trigger for what it would change.
- **Release behind the test set.** A prompt or model change ships only after it passes the component's fixed evaluation set at least as well as the current version, and the result is recorded. Watch provider-side model updates the same way: re-run the set when the provider changes the model under the same name.

### Audit and residency
- **The decision trace is the audit record.** For regulated or money-moving work, store per item: the inputs' ids, versions, the model's proposal, the rule checks, who or what decided, and when. Auditors ask "who or what decided this posting?"; the answer must be one lookup.
- **Model provider and data residency** can change the whole design (which provider, which region, what may leave the company). Ask the owner (often legal) in layer 3 as a blocking question; mask or drop personal and sensitive fields before any model call.

### Live quality
- **Correction rate is the live error signal.** Every human correction of a model output is logged, sampled into the test set, and tracked per component. Set an alarm level.
- **Drift.** Re-run the evaluation set on a schedule and after any version change; compare to the release baseline.

### How big a test set must be
A "zero wrong" claim needs enough cases to mean something. If a step makes **0 wrong in n cases**, the true wrong rate is still plausibly up to about **3/n** (the rule of three, 95% confidence): 0 wrong in 100 supports "under 3%", 0 in 300 supports "under 1%". Size the set to the claim you need, stratify it by the case types that matter (for example by supplier type or document layout), and say who labels the truth and how disagreements are settled.

## When the user wants more autonomy before there is any data

This happens often ("I want real agents, not scripts"). Do not argue taste either way. Say what is at stake for this step (money, audit, irreversibility), then propose a **contest** and let the user agree the rules before anyone runs it:

| Contestant | Design |
|---|---|
| A | Code, with a person picking the leftovers (rung 0-1) |
| B | One model call choosing among code's candidates (rung 2) |
| C | The user's agent with tools (rung 4), capped in calls, time and cost |

Same fixed set (stratified, sized for the claim), each design run several times for variance. **Win criteria set before running:** first the wrong-answer rate (the one that matters most), then the share settled without a person, then cost and time per item, then variance. Record it as a decision with `confidence: hypothesis` and the contest as the spike that will settle it; the winner is whatever the numbers say, including the user's design.
