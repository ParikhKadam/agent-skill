# Uncertainty playbook

Real planning is mostly uncertainty. This playbook lists the situations that stall sessions, how to recognize each, what to do, and what to record so the uncertainty stays visible instead of being forgotten. Find the heading that matches; if none does, use the general rule at the end.

Format: **Signal** (how you know), **Do**, **Record**.

## About the user and the request

### The user does not know what they want
**Signal:** "I'm not sure", "something like X", answers drift between sessions.
**Do:** Do not ask for requirements in the abstract. Ask for a recent real situation and walk it; or propose two or three concrete versions to react to ("version A does X, version B does Y"). Reaction is easier than invention.
**Record:** The cases as hand-written results; the chosen version as a `hypothesis` decision.

### The user wants a spec or code immediately
**Signal:** "Just write the spec", "just start building".
**Do:** Do the cheapest form of the skipped layers (often ten minutes each): one hand-written case, the top three facts, the riskiest assumption. Say what risk remains. If they still want to skip, agree it.
**Record:** The declined layers stay `in-progress` with the note "declined by user; proceeding on hypotheses" (use `skipped` only when the size makes a layer unnecessary, never to mean "not done"); the remaining risks in `risks.md`. See the stage protocol, step 1.

### The user gives contradictory answers
**Signal:** Today's answer conflicts with an earlier one or with a doc.
**Do:** Show both, side by side, without blame, and ask which holds now. Often the situations differ (two user types, two stages); that is a finding.
**Record:** Both statements and the resolution in a decision; add the distinction to the glossary.

### The user is not the real owner of the decision
**Signal:** "I think they want...", "I'd have to ask".
**Do:** Write the question for the owner with your recommended default; proceed on the default.
**Record:** Open question with owner; dependent decisions as `hypothesis` with a tripwire ("if X says otherwise, reopen D-005").

### Stakeholders disagree
**Signal:** Different people give incompatible goals.
**Do:** Do not pick a winner. Write the disagreement as an option comparison with the consequence of each, and list who decides. Look for a case both sides would accept as the test.
**Record:** Decision with confidence `unknown` and an owner; flag it as blocking or not.

### The feature is much bigger than first said
**Signal:** Every answer opens a new area.
**Do:** Re-size. Split into slices and decide the first slice's boundary with "what breaks if we leave it out?". Park the rest.
**Record:** New size in the brief; deferred items with revisit triggers in the plan.

## About facts and data

### No access to real data
**Signal:** Environments are down, empty, stale, or access is restricted.
**Do:** Make getting read-only access to the real thing the first spike. Until then, mark dependent facts `unknown` or `inferred` and keep the first design cheap to change. Check that the environment you can reach is the one users use (a test copy may be years old).
**Record:** A risk "we cannot see the real data", spike for access, and the lower confidence on everything downstream.

### A gate item cannot be met yet, but the user is here
**Signal:** Layer 2 wants checked real data, layer 3 a spike result, layer 9 the other side's agreement, and none is possible before building.
**Do:** Do not block the plan and do not pretend. Ask the user to pass the gate **with conditions**: list each unmet item as a condition. `plan-build` turns each into an early slice.
**Record:** `wsctl.py gate <ws> <layer> passed-with-conditions --notes "..."`; the waiting docs stay `pending`.

### The docs and the real system disagree
**Signal:** A field, endpoint or behavior is not as documented.
**Do:** Trust observation over documentation, and note the date. Do not "fix" the doc silently.
**Record:** A row in "Things that behave differently" (existing-system) and a fact with status `measured`.

### A fact is "usually" true
**Signal:** "Most of the time", "normally".
**Do:** Get a rate. Ask for the exception cases, or sample real records. The exception rate often drives the design (a field filled 70% of the time needs a fallback).
**Record:** Reliability column with the rate and sample size.

### You cannot tell how reliable something is
**Signal:** No way to measure yet.
**Do:** Say so. Set status `unknown`, design a spike with a bar, and treat the fact as a risk until measured.
**Record:** Fact row `unknown`; risk row; spike doc.

### The data is sensitive or read-only only
**Signal:** Production data, personal or financial content.
**Do:** Read only what you need, read-only, and keep names, emails and content out of the docs (anonymize; use ids and counts). Confirm with the owner that reading is allowed, once, and record it.
**Record:** A constraint (imposed) and a note on how data was handled.

### Nobody is available to answer
**Signal:** "I can't chat", a batch run, the owner is away for days.
**Do:** Follow the unattended rules in `session-protocol.md`: use only what was provided, record open questions with recommended answers, proceed on them, never mark a layer passed or a doc agreed.
**Record:** Assumptions and first questions in `90-log/sessions.md`; gates `in-progress` with notes on what each waits for.

### You cannot see the other side of a boundary
**Signal:** A contract with a team or system whose real messages you cannot observe.
**Do:** Write the contract as a **proposal** with realistic example messages, label every example `invented` and the doc title or summary `PROPOSAL`, and list the question for the other owner. Write the stub from your proposal so your side can still be built and tested.
**Record:** Open question for the other owner; contract stays `draft` until they have seen the examples.

## About the existing system

### A spec or a built system already exists
**Signal:** Docs of many pages, branches, tickets.
**Do:** Use rescue mode (`entry-modes.md`). Treat the spec as a hypothesis, the code as a second hypothesis, and decide with evidence.
**Record:** Divergence table; decisions with confidence; the staleness table reverse-engineered from the code.

### The spec and the implementation differ and nobody knows which is right
**Signal:** "The code does something else now."
**Do:** Do not argue. Define a fixed set of inputs and a measurable bar per component, run both, and compare. The spec is right only where it wins.
**Record:** Per divergence: spec says, code does, measured result, choice, and what would change it.

### Another team owns the part you need
**Signal:** An API, a table or a flow you do not control.
**Do:** Write the contract as example messages (layer 9) early. Run against a stub of their side so you are not blocked, and agree the examples with them.
**Record:** Contract doc; open question for their owner; stub noted.

### You do not understand the existing code well enough
**Signal:** You are guessing how it behaves.
**Do:** Say so. Read the relevant files, run it if possible, or ask the person who wrote it. Never design on a guess about existing behavior.
**Record:** `existing-system.md` rows with where you verified.

## About design

### Two approaches look equally good
**Signal:** Long debate, no winner.
**Do:** Find the assumption that would separate them and test it cheaply. If it is cheap to reverse, pick the simpler, record the tripwire, and move on.
**Record:** Decision with alternatives and "what would change this".

### A step needs judgment (a model, a human, a rule)
**Signal:** "It depends on the context."
**Do:** Apply the autonomy ladder (`ai-components.md`): start with code, measure, promote only where code fails. Ask what happens when the judgment is wrong.
**Record:** In the component doc, who decides and what the code rung achieved.

### You cannot decide where to split components
**Signal:** Too many or too few boxes.
**Do:** Use the four tests (user acts on it, own quality bar, stale at a different rate, different owner or failure mode). If none holds, merge.
**Record:** The reason each component exists, in its doc.

### A later layer shows an earlier one was wrong
**Signal:** The staleness table reveals a missing rule; a contract example does not fit the flow.
**Do:** Say so and reopen the earlier layer (`session-protocol.md`). This is the process working, not failing.
**Record:** Change log entry; bumped versions; updated pins.

### Everything seems important
**Signal:** No obvious cuts.
**Do:** Rank by "what breaks if left out" and by risk. The thin end-to-end version is the cut: whatever it does not need yet is deferred.
**Record:** Deferred list with revisit triggers.

## About process

### The user disappears mid-session
**Do:** Write `sessions.md` with what is settled, what is open, what you would do next, and your defaults. A later session resumes from there.

### A new person joins halfway
**Do:** Point them at `wsctl.py read-set <ws> onboard` and the overview page. Do not retell the history.

### Requirements change after the plan is agreed
**Do:** Layer 11: find the earliest layer touched, run `wsctl.py impact` on the changed doc, rework from there. Do not rewrite everything.

### The docs have grown unwieldy
**Do:** Split by purpose, not by length. Move detail down into child docs, leave a summary and a link, and update the reading paths. Run `wsctl.py index`.

### The user says "this is too much process"
**Do:** Listen. Drop to the small size, keep only brief, one case, user flow and plan. Say which risks that leaves, once. Process should shrink with the feature.

## The general rule

When a situation is not listed: say what you do not know, say how you would find out and how long that takes, give a default you would proceed with, and write all three down. Uncertainty that is written down is a plan; uncertainty that is silent becomes a surprise in week six.
