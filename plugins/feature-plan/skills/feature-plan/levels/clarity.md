# Level 1: Clarity

**Resolves:** what the person gets and when; what already exists; what is true in the real world; what could break the plan. **Output:** `outcome.md`.

The failure this level prevents is designing flows on a fact that turns out false, or building something nobody needed. Do it before any flow is polished, and keep it short.

## Steps

1. **Restate the outcome.** Read what the user gave you (notes, tickets, an existing spec) and say in one sentence what the person gets and who acts on it. Ask for agreement.
2. **Know what exists.** Find out which of three situations this is, because it decides what you may trust:
   - **Running code exists** (a first version, a legacy system). Read how it behaves today. For each thing the user wants, write whether it is *same as today*, *differs from today* or *unknown*. Today's behaviour is evidence about the world, not the new design: do not carry it over without asking, because a limit that was fine before may be what the user wants gone, and a behaviour the user did not mention may be one they rely on.
   - **Only documents or a spec exist.** Treat them as hypotheses with a date. Look for where they disagree with each other or with the user, and say which you believe and why.
   - **Nothing exists yet.** Say so. Every fact about the world then needs a source or a spike, and established design patterns are the only starting structure; label them hypotheses and keep a recorded fact above any pattern.
3. **Cut it into releases.** Say what the person sees and can do at each release, in their words ("I upload the file and see the totals; I fix a wrong line once"). Two or three is usual. A release is something that can ship and that the person can watch working. Anything out of scope, or promised only for later, is not a release: list it under not in scope. If you cannot describe a release in the person's words, it is not one. This is what the whole plan will be judged against.
4. **Write two or three real cases by hand.** A case is a concrete situation with the ideal result written out step by step. Use a real example if one exists; otherwise label it `invented` and ask for a real one. Include one awkward case (missing data, a wrong guess, a failure). If every case is the easy kind, or all come from one kind of source, say so: the plan will lean on a sample, and no rule may rest on it alone.
5. **List what would make the person distrust the result.** Each line becomes a check later.
6. **Record the facts the cases reach for.** One row each: the fact, where it lives, who writes it, how reliable, how we read it, and a status: `measured` (seen in code or data), `doc` (written somewhere or told to us), `unknown`. Look facts up before asking. Never present a guess as a fact; mark invented examples as invented.
7. **Separate constraints.** Mark each as *imposed* (someone outside the plan set it, and say who can change it) or *chosen* (the existing system decided and we may redesign). The user's own constraints are never changed silently; if a plan would challenge one, it becomes a decision for them.
8. **Rank the risks.** Score impact times uncertainty. The top ones are usually about knowing (can we read this fact at all?) not building. Give each top risk a spike: the smallest test that settles it, with a pass line. If the data for a spike is out of reach, write the spike and leave it pending.
9. **Note the decisions only the user can make**, each with your recommended answer.

## When you are stuck

- **No access to real data:** make getting access the first spike; mark every dependent fact `unknown`.
- **The person who knows is unavailable:** record the question with an owner and your recommended answer, proceed on it, and mark the dependent choice a hypothesis.
- **Two sources disagree:** do not average them. Data beats a document beats memory; record the conflict and a test.
- **The user wants to skip ahead:** do the cheapest version of this level (ten minutes), say what risk remains, and record the skip.
- **Scope keeps growing:** ask "what breaks if we leave this out?" and move the rest to a later release.

## Gate: the user agrees that

- the outcome and the releases are right, and every release can be watched working;
- you have said what exists today and what differs from it;
- the cases look like their world (or are marked invented, with a plan to replace them);
- every fact has a source and a status, or sits on the unknown list;
- the top risks have a spike or an accepted fallback.

## Depth

Small: the outcome and one case in a few lines. Medium: all steps, short, one spike for the top risk. Large: all steps in full, a spike per top risk.

## `outcome.md` contains

Outcome sentence; what exists today; releases in the person's words; who acts; distrust checks; not in scope; constraints (imposed or chosen); facts with status; top risks with their spikes; cases; decisions only the user can make. Use `templates/outcome.md`.
