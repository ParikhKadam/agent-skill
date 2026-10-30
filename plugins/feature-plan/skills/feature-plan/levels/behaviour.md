# Level 2: Behaviour

**Resolves:** how the person moves through the feature, which intermediate results must therefore exist, and how the system runs from any starting point. **Output:** `behaviour.md`.

This is where an unclear flow becomes clear, so never shorten it to save lines. Cut repetition, not thinking. The failure it prevents is a design whose pieces cannot be redone one at a time, and decisions nobody asked about (what happens if the person fixes X after Y was approved?) discovered during the build.

## Part A: the user flow

1. **Walk a real case as a story,** step by step, in the order the person experiences it. Use the cases from level 1. Where something exists today, mark each step *same as today*, *new* or *changed*, so today's behaviour is not mistaken for the intended one.
2. **At every step ask four questions:** can they see it? can they correct it? can they redo it alone? can they skip it? Each yes means a result has to be stored so the step can be seen, kept, redone or left alone. Write the answers in a table: step, see, correct, redo alone, skip, stored result.
3. **List the re-entries you ruled out** (editing the AI's text by hand, automatic regeneration) with why, so they are not reopened by accident.
4. **Cover the other paths:** accept everything and only read; fail halfway; return later; leave halfway; two tabs; the same request twice; a role that may only view.

## Part B: stored results and what goes stale

One row per stored result: what makes it, what the user can do with it, what it depends on, when it goes stale, what happens then (leave it, mark it, redo it), where it is stored.

**The hard cells are the point.** Fill them in on purpose, because they expose decisions nobody asked:

- the user fixes X after Y was already produced from it;
- the user changes something while a run is in progress;
- time passes and only some results age (usually only the ones that read live outside data);
- the user's choice and the system's proposal disagree on the next run;
- a result is redone and something built on it is not;
- a step needs the output of an earlier one: who triggers it? Does the side that started the work wait for the output and then request the next step, or does it make one request and let the other side order the steps? Waiting and chaining across a boundary adds coupling and a place to fail; say which you chose and why;
- a result uses data fetched from outside (another system, a live source): is that data kept with the result or fetched again each time? Kept data can go stale and may be sensitive; fetched data costs time and can differ between runs;
- the person is also in the data they act on (they appear among the records, participants or recipients): are they a subject like the others, or excluded? Without a rule they get matched, notified or counted as someone else.

Cut false dependencies so one part can be redone without staling another. Keep the system's proposals and the user's choices as separate results: a redo may replace a proposal, never a choice. Say what is safe to leave alone and why.

## Part C: the system flow

1. **Who does what.** Split the work between systems or teams in one table. Say who decides inside each step (code, a model, or a person), starting at code.
2. **A full run, numbered,** from the first trigger to what the person sees.
3. **Every start point.** Each re-entry from Part A is a start point: what runs, what is skipped and why. A skipped step is a visible rule with a reason, not an accident.
4. **Failure table.** For each step: what fails, what the person sees, whether a retry is safe. A failure is never reused as a result, and the last good result stays visible.
5. **Duplicates and concurrency.** Same request twice, two devices, an edit during a run, a stuck job and how it is noticed.
6. **Check the flow against every case,** including the awkward one, and say which step covers which line of the ideal result. A gap is a finding to resolve now.

Use established patterns where they fit (a state machine for a lifecycle, check-before-act or an idempotency key for duplicates, a scheduled sweep for stuck work). Name the pattern, say why it fits against the recorded facts, and keep it a hypothesis until tested. A recorded fact always beats a pattern.

## Discuss, then write

Walk the flow in chat first, one case at a time, and show the table that results. Ask the hard-cell questions explicitly, with your recommended answer for each. Write `behaviour.md` after the user's yes.

## Gate: the user agrees that

- each case runs through with no gap;
- every re-entry is either supported by a stored result or ruled out;
- every stale rule has a decided behaviour, including the hard cells;
- every start point and every failure has a visible outcome.

## Depth

Small: the story and one table. Medium: all three parts, short. Large: all three parts in full, with every start point and the failure table.

## `behaviour.md` contains

The story; the see / correct / redo / skip table; ruled-out re-entries; stored results with stale rules and the decisions the hard cells exposed; who does what; the full run; start points; failures; duplicates; the check against the cases. Use `templates/behaviour.md`.
