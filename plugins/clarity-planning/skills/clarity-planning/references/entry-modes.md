# Entry modes

Pick the mode in the first minutes. It changes where you start, not what the layers are. If unsure, ask one question: "Is there anything written or built already?"

| Mode | When | Start at |
|---|---|---|
| **new** | A product or system from an idea; nothing exists | Layer 1 (cases), then 2 |
| **brownfield** | A feature inside an existing product (most common) | Layer 0 inventory, then 1 |
| **rescue** | A spec or partly built system exists and the team lacks clarity or the build drifted from the spec | Reconcile (below), then the layers the evidence shows are weak |
| **change** | A plan workspace exists and a requirement changed | Layer 11 (change protocol) |
| **tiny** | A small, well-understood edit | Layers 0, 1, 4 and 10 in a few lines |

Any mode: if the user pastes a written brief, flows or requirements, extract and challenge them instead of asking open questions (see "written brief" in `layers/00-intake-and-sizing.md`). If they limit the sources, record the allow-list in the brief and respect it in every mode.

## new

You have an idea and little else. Risk is mostly "is this the right thing, and what is the world like?".

1. Layer 1 first: ask for two or three real situations the product would serve. If none exist yet, write invented ones, label them `invented`, and plan how to replace them with real ones (a user interview, a pilot).
2. Layer 2 is mostly about **users and their environment**, not an existing system. Facts live in interviews, competitors, regulations, and the other systems you must integrate with.
3. Layer 3 will be dominated by "does anyone want this" and "can we get the data/access". Spike those first.
4. Be strict on non-goals; new work grows fastest.

## brownfield

A feature in an existing product. Risk is collision with what exists and facts about existing data.

1. Layer 0: read the code and docs for what exists, and write `existing-system.md` before asking questions. Look for reuse (permissions, tracing, tooling) and for behaviors that differ from docs.
2. Layer 1: cases drawn from real usage today. What do users do by hand now?
3. Layer 2: facts about **existing data** (fill rates, who writes it, when) matter most. Sample real records.
4. Respect existing conventions; list them as chosen constraints, and flag any you would break.

## rescue

A spec exists, or code exists, or both, and trust in them is low. Typical signs: the spec is long and detailed but nobody can explain the system plainly; the build changed shape; the team wrote explainer docs afterwards to understand it.

Do **not** start by rewriting the spec. Reconcile:

1. **Inventory what exists.** Specs, plans, branches, tickets, notes, explainer docs. List them with dates and who wrote them. Note which are specs (what we meant to build), which are descriptions (what is built), and which are findings (what we learned).
2. **Extract the real system**, from code and runs (if only an engineer's notes exist and you cannot read the code, extract it from the notes, label every statement `doc`, and make "read the real code against `existing-system.md`" the first task of the plan): the steps, what each reads and writes, where the model or a human decides. Write it in the artifacts and components format, even if it was never designed that way. This is the staleness table nobody wrote.
3. **Build a divergence table** in `10-world/divergence.md` (`init --mode rescue` creates it) (spec says, code does, evidence, which is better, what would change it). Mark each `unknown` until measured. Do not argue; measure on fixed inputs.
4. **Find the missing clarity.** Check each layer's gate against the existing material and see which fail. Typical gaps: no hand-written cases, facts about the world taken as given, no artifact boundaries (so partial re-runs are impossible), no per-component quality bars.
5. **Plan from here**, not from scratch: the thin end-to-end version is likely the code you have, with stored artifacts added; the slices are the components in risk order, each with an exit check on stored inputs.
6. **Keep findings, retire repeats.** Old docs that restate each other become `superseded` or are folded in; keep the evidence they hold (measurements, real-data findings) and link to it.

Treat the user's frustration as data: a pile of explainer docs written after the fact is a map of what was unclear. Ask which doc finally made it click, and why.

## change

A workspace exists and a requirement changed ("contractors can belong to several workspaces", "invoices also arrive by email").

1. Read `INDEX.md` and `90-log/sessions.md`.
2. State the change in one sentence and find the **earliest layer** it touches (usually layer 1, 4 or 5).
3. Run `wsctl.py impact <ws> <id>` on the doc that changes. That is your reopen list.
4. Rework from the earliest layer downward, bumping versions and pins. Leave unrelated decisions alone.
5. Log it in `90-log/change-log.md`; the gate of the earliest layer goes back to `in-progress`.
6. Check the staleness table first: it usually shows exactly which artifacts and components are affected, and which are untouched.

## tiny

Small, understood, reversible. One short brief (outcome, who, how we know it works), one case, the user flow in a few lines, and a plan with an exit check. No facts register unless the change relies on data you have not seen. Re-size at once if a tripwire fires (outside data, second team, a model deciding, irreversible actions, security-relevant).
