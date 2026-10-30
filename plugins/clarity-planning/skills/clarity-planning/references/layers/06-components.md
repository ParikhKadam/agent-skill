# Layer 6: Components

**Answers:** What produces each artifact? Inside each, who decides: code, a model, or a person? What is each component's quality bar and how is it tested? Where two structurally different designs compete, which one and why?
**Prevents:** A single entangled pipeline that cannot be tested in pieces, and unmeasured autonomy decisions made in the first spec. Also boxes drawn for technical tidiness that match nothing the user does.
**Output:** `40-design/components/C-*.md` (one per component), decisions for any approach comparison.
**Read first:** Artifacts table, user flow, facts and risks (`wsctl.py read-set <ws> build-component` once a component exists; before that, `review`).

## How to generate

1. **One producer per artifact.** Start from the artifacts table; each artifact gets a component (or is produced by a person or outside system, which you note).
2. **Apply the four split tests.** Keep a component separate only if at least one holds: the user can see, edit, override or regenerate its output; it needs its own quality bar and test set; its inputs go stale at a different rate; it has a different owner, cost or failure mode. Otherwise merge it into a neighbour. Too many components is its own failure.
3. **State inputs and output** as artifact ids. A component reads artifacts and writes one.
4. **Decide who decides inside** (code, model, person) using the autonomy ladder in `ai-components.md`: start with code, record what the code rung achieved and what is left. Mark the choice `hypothesis` until measured.
5. **Make it run alone.** Say how: a command, an endpoint or a harness that takes stored inputs and produces the output. If it cannot run without the rest of the flow, the boundary is wrong.
6. **Set the quality bar before building**: what counts as correct, the number, the policy for wrong versus unhelpful, and the fixed test set (hand-written cases first, then recorded real inputs).
7. **List failure modes and cost:** what the component returns when it fails and what the user sees; time and money per run.
8. **Compare real alternatives** if the design could go two structurally different ways (for example, the model chooses what to read versus code reads fixed things). Lay out two or three, recommend one, and record a decision with what would change it. Where the spec and an existing build disagree, run both on the fixed set.
9. **Update pins.** Each component rests on the artifacts it reads and the decisions that shaped it; set `depends_on` accordingly.

## Standard practice

Before inventing a structure, ask what established pattern answers each design problem here (state machine for a lifecycle, adapter and stub for an outside system, queue and workers for slow work, a central permission check). Name it in the component doc under "Who decides inside" or "Failure modes", say why it fits against the facts, and keep it a `hypothesis` until tested. Take the smallest version that handles the failure you care about and note what you left out. See `standard-practices.md`.

## Starter questions

- "When this step is wrong, what does that cost? Is a person nearby to catch it?"
- "What can be done with a fixed rule? What is left over?"
- "If this component were replaced next month, what would the other parts need from it?"
- "Who owns this, and who gets paged when it fails?"
- "How would we know this component got better or worse?"

## Gate (layer 6 passed when)

- [ ] Every artifact has a producing component (or a named person or system).
- [ ] Every component can run alone from stored inputs; the way is written down.
- [ ] Every component has a "who decides inside" with the autonomy choice and its evidence.
- [ ] Every component has a quality bar and a named test set.
- [ ] No component exists without passing a split test.
- [ ] Competing designs were compared and the choice recorded with a tripwire.

## Depth

small: skip. medium: one line per component (inputs, output, who decides). large: a card per component with bar, test set, failure modes, cost and owner.

## When it goes sideways

- **A component keeps growing.** It is probably two: split along the artifact it could store midway.
- **Two components always change together.** Merge.
- **The quality bar cannot be defined.** Define "wrong" first (what is harmful?), then "good enough"; if still unclear, ask what the user would reject.
- **No test set exists.** Writing it is slice zero of the plan: hand-write ten cases from layer 1; add real inputs as they arrive.
- **The existing system already has a component like this.** Reuse it; read how it behaves; record any surprise.
- **A model step is justified only by taste.** Put it at the code rung first and let the measured leftovers justify the model.

## Hands off to

Layer 7: components run in dependency order from any start artifact.
