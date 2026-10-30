# Next-question engine

Use this when you (or the user) do not know what to ask next. The user usually cannot say which question matters, because they do not yet know what they do not know. You pick, using value of information: **ask the question whose answer would change the most downstream work.**

## Step 1: Scan the state (2 minutes)

Run `wsctl.py status <workspace>` and read the current layer's guide. List four things:

1. **Unknowns**: facts with status `unknown`, open questions, risks scored high and untested.
2. **Unmet gate items**: what the current layer's gate still lacks.
3. **Contradictions**: two docs, or a doc and a real example, that disagree.
4. **Things the user said that have no home** (in `90-log/sessions.md`).

If all four are empty, you are probably ready to pass the gate. If a list is long, the next question comes from it.

## Step 2: Choose by value of information

For each candidate unknown, ask three things and rank:

| Test | Question to yourself |
|---|---|
| Reach | How many docs, layers or components would change if the answer flipped? |
| Cost of being wrong | If we guess wrong, do we find out cheaply (a test fails) or late (users, money, a rebuild)? |
| Findability | Can I find it myself (code, data, docs) without the user? |

Order: **findable first (look it up, do not ask)**, then **high reach and late-to-find**, then the rest. Never spend the user's attention on something you could have read.

## Step 3: Generate the question from a probe

If no candidate comes to mind, run the probes below against what exists so far. Each probe turns something vague into a specific question. Pick the two or three that fit; do not read them out as a list.

### Make it concrete (use when the user speaks in abstractions)

- **Last time.** "Walk me through the last time this actually happened. What did you open first?"
- **Hand-made result.** "If I handed you the perfect result for that case, what would be on it?"
- **Show me the artifact.** "Can you show me a real one?" (a record, an email, a screenshot, a row)
- **What you do by hand.** "What do you check manually before trusting it?" The manual checks are the requirements nobody wrote down.

### Find hidden facts (use in layers 1-2)

- **Where does it live.** "Where would I look to find that out, and who puts it there?"
- **Who writes it, when.** "At what moment does that get filled in? Is it ever late, wrong or blank?"
- **How often is it right.** "Out of ten, how many times is that filled in correctly?" (then measure if you can)
- **Same word, two meanings.** "You said 'account' twice. Is it the same thing both times?"
- **What exists already.** "Has anyone built anything like this here? What happened to it?"

### Find the edges (use in layers 3-5)

- **Counterexample.** "Is there a case where that rule does not hold?"
- **Inversion.** "What would make you stop trusting this? What is the worst wrong answer it could give?"
- **Failure halfway.** "What if it stops at step three? What state is the user left in?"
- **Redo.** "If they fix that value after the fact, what else should change?"
- **Skip.** "Is there a user who already knows this and would want to bypass that step?"
- **Two at once.** "What if two people do this at the same moment?"
- **Same thing twice.** "What if the same request arrives twice?"
- **Who else touches it.** "Who else reads or changes this, and what do they expect?"

### Find the real scope (use when things grow)

- **What breaks if we leave it out?** "If this were missing at launch, what could the user not do?"
- **Smallest useful.** "What is the smallest version someone would actually use on Monday?"
- **Later, not never.** "Can this wait without blocking anything else?"

### Find the real decision-maker (use when stuck on a choice)

- **Whose call.** "Who decides this? Can we get an answer by Friday? What if not?"
- **Reversibility.** "If we choose wrong, how hard is it to undo?" (cheap to reverse: pick and move on)
- **Evidence that would settle it.** "What result would make us confident? Can we get it in a day?"

### Find the risk (use in layer 3 and any time something feels too smooth)

- **Pre-mortem.** "It is six months later and this failed. What is the most likely reason?"
- **Weakest link.** "Which single step, if it were wrong, makes the rest worthless?"
- **Assumed, not seen.** "What are we assuming about the data or the other system that we have not looked at?"

## Step 4: Shape the question

Every question you send must be:

- **Specific to this project**, built on their last answer or on something you found ("The invoice you showed has no PO number. Does that happen often?").
- **Followed by your recommendation**, worded so "yes" accepts it. A proposal they can correct beats an open question.
- **One idea per question.** If it has an "and", split it.
- **Honest about why**: say what the answer would change ("this decides whether matching needs a fallback").
- **Plain language**, pitched slightly above the user's own vocabulary. No process jargon; never quote this skill at them.

Bad: "What are your non-functional requirements?"
Good: "Will two clerks ever work on the same invoice at the same time? If so I'd lock it for whoever opens it first. Does that match how you work?"

## Step 5: Decide who answers

| The answer lives in | Do this |
|---|---|
| Code, config, docs, tickets, git history | Look it up. Do not ask. |
| Real data you can read | Read or sample it (read-only). Report numbers, not impressions. |
| A running system you can probe | Probe it carefully, read-only, and log what you did. |
| One person's head | Ask that person, with a recommended default. |
| Nobody yet | Record as `unknown`, plan a spike, proceed on a flagged default. |

## Step 6: Know when to stop asking

Stop and move to the next layer when:

- The gate items are met with evidence.
- Remaining unknowns are cheap to be wrong about, are recorded with a default, and cannot change the layers above.
- The user's answers have started to repeat what is already written.

Stop **and reopen an earlier layer** when an answer contradicts something recorded there.

## Question smells

- You are asking for something that is in the repo. (Read it.)
- The question has four parts. (Split it, ask the first.)
- The answer would not change any doc. (Do not ask.)
- You are asking the user to design. (Propose and let them react.)
- You asked the same thing in different words. (Check `sessions.md`; the answer is probably written.)
- The user keeps saying "it depends". (Ask for a real case and walk it.)
