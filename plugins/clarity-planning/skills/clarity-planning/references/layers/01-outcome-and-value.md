# Layer 1: Outcome and value

**Answers:** Who acts on the result and what do they do next? What would make them distrust it? Which part carries the value? What are the non-goals?
**Prevents:** Building the visible part (a polished summary) while the valuable part (the match, the next action) is under-served. A large share of wasted effort traces to optimizing the wrong output.
**Output:** `00-start/brief.md` (complete), `00-start/cases/case-nn.md`, `00-start/glossary.md`.
**Read first:** The brief so far; any real examples the user can show.

## How to generate: hand-write the result first

Before any design, **write the ideal result for two or three real cases yourself, with the user.** This is the single most clarifying step in the process.

1. **Get real cases.** Ask for situations that actually happened recently: "walk me through the last time". Pick them to differ: a clean one, an awkward one (missing information, an exception), one where the user hesitated.
2. **For each case**, ask: what did they have in hand, what did they do, what did they want at the end? Then **write the perfect result** as they would want to receive it, line by line.
3. **Note every fact you reached for.** Each time the ideal result needed a piece of information, write it down with the case. These become the facts register in layer 2.
4. **Notice the surprises.** Where the user said "it depends", paused, or corrected you: that is a hidden rule or exception.
5. **Find the value.** Ask which part of the ideal result they would miss most if it were gone, and which part they would barely read. The answer often contradicts the first brief.
6. **Write the brief** in plain words: who acts, what they do next, what would make them distrust it, the valuable part, non-goals and anti-goals, how success looks.
7. **Start the glossary.** Any term used in two senses, or that the team and users name differently, goes in now.

## Starter questions

- "Walk me through the last time this came up. What did you open first?"
- "If I handed you the perfect result, what is on it?"
- "What do you check by hand before you trust it?"
- "What would make you stop using this?"
- "Which part would you miss most? Which part would you never read?"
- "What is explicitly not part of this?"
- "What would count as a failure even if it technically works?"

## Gate (layer 1 passed when)

- [ ] Two to three cases (one for small) exist with hand-written ideal results.
- [ ] The user recognized each ideal result as right, or corrected it.
- [ ] The brief says who acts, what the valuable part is, what would cause distrust, and the non-goals.
- [ ] Each case lists the facts it reached for.
- [ ] Glossary has every term that was used two ways.

## Depth

small: one case, a short brief. medium: 2-3 cases. large: 3+ including an awkward case and one real example of each input kind.

## When it goes sideways

- **No real cases available** (a new product): write invented ones and label them `invented`; plan how to replace them (user interviews, a pilot). Lower confidence on everything built on them.
- **Only a written brief, no real transcripts, so the user cannot recognize real cases.** Do not hold the gate open. With the user's explicit yes, pass layer 1 as `passed-with-conditions`: `--evidence` names the brief and the invented cases the user reacted to; `--notes` says "cases are invented from the brief; replace with N real examples from <source/owner> before <milestone>". Keep each invented case `pending` (set before the gate command) with `invented: true` and a Source line saying how it will be replaced, and add the replacement as an open question with an owner. `plan-build` makes the replacement slice zero. Never mark invented cases `agreed`.
- **The user cannot say what "ideal" is.** Offer two candidate results and ask which is closer; iterate. Reaction is easier than invention.
- **The cases disagree on what matters.** Probably two user types. Name both in the glossary and decide which comes first; do not merge them.
- **The value is not where the team thought.** Say so plainly; it re-orders everything. Record as a decision and tell the owner.
- **The user wants to skip this.** Do it in ten minutes with one case; it is the cheapest insurance in the process.
- **Privacy forbids real examples.** Use anonymized ones with the same shape; keep ids and counts, drop names and content.

## Hands off to

Layer 2: every fact the cases reached for becomes a row to verify.
