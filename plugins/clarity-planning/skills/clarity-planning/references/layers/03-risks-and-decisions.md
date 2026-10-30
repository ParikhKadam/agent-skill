# Layer 3: Risks, unknowns and decisions

**Answers:** Which assumption, if wrong, breaks the design? Which decisions belong to someone else, and what do we do while waiting?
**Prevents:** Spending weeks on the safe parts and discovering the fatal assumption last. Teams usually spike the technical risk ("does the framework work?") and skip the knowledge risk ("can we ever identify the right record?").
**Output:** `20-risks-and-decisions/risks.md`, `spikes/S-nnn-*.md`, `decisions/D-nnn-*.md`, `open-questions.md`.
**Read first:** Brief, cases, facts register (`wsctl.py read-set <ws> review`).

## How to generate

1. **List the assumptions the design rests on.** Pull from `unknown` and `inferred` facts, from steps in the cases that rely on a judgment (matching, ranking, interpreting), from things you plan to depend on (another team, an API, a model).
2. **Score each:** impact (1-3: how much breaks if wrong) times uncertainty (1-3: 3 means we are guessing). Sort. Look at two kinds especially: **knowledge risks** (can we know X at all?) and **technical risks** (can the tool do X?). Do not let technical ones crowd out knowledge ones.
3. **Plan for the top one to three.** `spike` (test it), `accept` (cheap to be wrong; say why), or `mitigate` (reduce impact; say how).
4. **Write each spike** with a question that has a yes/no/number answer, a **bar set before looking** (what result means what, and what we do then), method and data, and a fallback design if it fails. Run it on real data where you can; report numbers first and say what the sample does not cover.
5. **Record decisions** one per file: choice, alternatives, why, evidence, **what would change this**, and confidence (`decided`, `hypothesis`, `unknown`, `measured`). Mark guesses as `hypothesis`; most early decisions are.
6. **Decisions that belong to others** go in `open-questions.md` with an owner and your recommended default. Proceed on the default and set a tripwire on dependent decisions.
7. **Surface scope and who decides.** If an answer might expand scope, apply "what breaks if we leave it out?" and put the rest in Deferred (layer 10).

## Standard practice

When there is no code to learn from, bring in established patterns as **alternatives** (see `standard-practices.md`). For each decision, name the pattern, say why it fits or not against the facts recorded so far, set `basis: standard-practice` and keep `confidence: hypothesis` until a spike or the owner confirms. A common pattern is a reason to try it first, not evidence that it fits. For payments, authentication, personal data and regulated areas, check current guidance from a primary source and cite it.

## Starter questions

- "It is six months later and this failed. What is the most likely reason?"
- "Which single step, if wrong, makes the rest worthless?"
- "What are we assuming about the data or the other system that we have not looked at?"
- "Who decides this, and what if they do not answer by Friday?"
- "If we choose wrong, how hard is it to undo?" (cheap to reverse: pick and go.)
- "What result would make us confident? Can we get it in a day?"

## Gate (layer 3 passed when)

- [ ] Assumptions are ranked; the top one to three each have a measured answer or an accepted fallback.
- [ ] Every spike had its bar set before the result, and its result is recorded with sample and date.
- [ ] Every open decision has an owner and a recommended default; dependent decisions carry a tripwire.
- [ ] Every decision states confidence honestly and what would change it.
- [ ] A knowledge risk was tested, not only technical ones.

## Depth

small: name the top risk in the brief. medium: rank, one spike. large: rank, spike every top risk with a bar, owner list, and a second round once spikes return.

## When it goes sideways

- **Cannot run the spike** (no access, no time). Keep the spike doc `pending`, record the risk with a high score, take the fallback design, pass the gate with conditions if the user agrees, and make the spike the first task of the plan.
- **The spike returns an ambiguous result.** Say what it does settle, what it does not, and what one more cheap test would close it. Do not stretch the result.
- **The spike kills the design.** Good: it was cheap. Reopen layer 1 or 4 (the user flow may need to rely on a person for that step), log it, continue.
- **Two options remain after the spike.** Pick the simpler and reversible one; set the tripwire.
- **The owner is unreachable.** Proceed on the default; mark `hypothesis`; add a tripwire; tell the user which decisions are on borrowed time.
- **Everything scores high.** You are guessing too broadly. Narrow: which is the single assumption the others depend on?

## Hands off to

Layer 4: with the world and the riskiest assumption understood, flows are worth drawing up.
