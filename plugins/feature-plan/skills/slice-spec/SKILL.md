---
name: slice-spec
description: Turns one planned slice into an engineering spec a coding agent can build without making a significant engineering decision itself, then runs the build loop for it. Use when the user is about to build, start, implement or hand over the next slice of a plan, asks "what exactly changes in the code for this slice", "write the implementation details", "is this slice ready to build", or wants a slice built by an agent, even if they never say "spec". Reads the plan, the design and the real code first, writes a short spec with the files to change, the smallest implementation and the non-goals, checks it is ready, and then builds with strict rules against over-engineering. Companion to feature-plan, which produces the plan. Skip one-line fixes.
---

# Slice spec and build loop

A plan decides what is hard to change and in what order to build. It deliberately does not say which files change or how: that detail goes stale if it is written weeks early. This skill writes it **just before a slice starts**, from the real code, so that whoever builds (a person or a coding agent) is not forced to invent engineering decisions.

## When the slice is ready to specify

Open the workspace (`start-here.md`) and find the slice in `plan.md`. Check, before anything else:

- every slice and decision it **needs** has passed or is confirmed by its owning engineer;
- the boundary rows it touches in `design.md` are approved;
- the access, data and fixtures it needs exist.

If something is missing, say exactly what and who owns it, and stop. Do not fill a gap in the plan yourself: a hard-to-change decision made silently inside a spec is the failure this skill exists to prevent. Route it back through `feature-plan` (its change handling), and carry on only after the owner's answer.

## Level 5: write the spec

1. **Investigate read-only.** Find how the code does today what this slice touches: the files and functions, the patterns and helpers to reuse, the existing tests, how to run them, the conventions. For a large repository hand a read-only subagent the exact question and ask for a digest with file references. Record what is reused, changed and new.
2. **Write the spec** from `templates/slice.md`, in at most 80 lines. It points to the plan and design instead of restating them. How to choose what goes in, and what counts as a significant decision: `spec-guide.md`.
3. **Run the ready test.** For each decision a builder would otherwise have to make (data shape, interface, dependency, error handling, concurrency, configuration, tests), the spec either makes it in one line or points to a confirmed decision record. A decision that is hard to change and not yet recorded is not made here: it goes back to the owner. The test passes when an agent can build the slice without choosing anything significant itself.
4. **Get the owning engineer's yes** on the spec and mark it approved in the workspace. Engineering decisions are confirmed by the engineer who owns that part, not by the planner.

## Level 6: build loop

Give the builder the spec and `build-rules.md`, which every slice follows. In short: plan small, build, run the demo, review the design as its own step, simplify, rerun, report, and stop to ask when a significant assumption proves wrong. Do not commit or deploy unless the user has authorised it.

When the build shows that the plan or design is wrong (a field nobody can supply, an interface that cannot work), stop and report it. That is a change to an approved document, handled through `feature-plan`, not an edit made in passing.

A finished slice has a completion report in its spec file: what changed, why the design is appropriate, which abstractions were added and why, the tests and checks run, and remaining concerns. The slice is done when its demo's pass line holds, not when the code merges.

## Before handing back

Run `python3 <feature-plan>/check.py <workspace>`; it checks that a spec has its files list, non-goals and ready check, and that a finished slice has its report. Then tell the user: whether the slice is ready, the decisions that remain with owners, and the first command to run.
