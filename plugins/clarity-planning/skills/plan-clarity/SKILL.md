---
name: plan-clarity
description: Stage 1 of clarity-first planning. Gets clarity on a feature before any design, covering the outcome, hand-written real cases, facts about the real world and existing system, constraints, ranked risks with spikes, and decisions with owners. Writes the brief, glossary, cases, facts register, risks, decisions and open questions into the planning workspace. Use when the user wants to start planning a feature, understand what a feature really needs, de-risk it, check assumptions, or says "first let's get clarity", even if they don't name the stage. Also use in rescue mode, when a spec or build exists and nobody can explain it plainly. Part of the clarity-planning family; the shared tools and guides live in the clarity-planning skill.
---

# Stage: Clarity (layers 0-3)

This stage answers: **what is this, for whom, what is true about the world it lives in, and which assumption would break it?** It comes first because flows and components built on unchecked facts are wasted.

Read `../clarity-planning/references/stage-protocol.md` first (relative to this skill's folder) and follow its steps: find the workspace, check readiness, load only what this stage needs, work each layer, get explicit approval at each gate, and close the stage. This file adds only what is specific to clarity.

## Starting a workspace (this stage owns intake)

Intake belongs to this stage alone; the hub and other stages hand over to it. Check first with `wsctl.py find <project root>`. If no workspace exists:
1. Find the mode (`<hub>/references/entry-modes.md`): new, brownfield, rescue, change, tiny.
2. **Read the project before asking anything**: code, docs, tickets, history.
3. Confirm the location with the user (default `docs/planning/<feature-slug>/`), choose the size (`<hub>/references/depth-sizing.md`), and run `wsctl.py init <path> --name "<Feature>" --size <s> --mode <m>`.
4. Restate the outcome in one sentence with the size, and get a yes. That is gate 0.

## The four layers and what matters most

Guide paths below are under `../clarity-planning/references/` (written `<hub>/references/` elsewhere).

| Layer | Guide | The heart of it |
|---|---|---|
| 0 Intake and sizing | `layers/00-intake-and-sizing.md` | Restate the outcome, size it, inventory what exists |
| 1 Outcome and value | `layers/01-outcome-and-value.md` | **Hand-write the ideal result for 2-3 real cases** with the user; find which part carries the value; list every fact each case reached for |
| 2 World and facts | `layers/02-world-and-facts.md` | One row per fact: where it lives, who writes it and when, reliability, how we read it, status. **Check real data yourself** where you can. Separate imposed from chosen constraints. In rescue mode, fill `10-world/divergence.md` |
| 3 Risks and decisions | `layers/03-risks-and-decisions.md` | Rank assumptions; spike the top ones with a bar set before looking; test a **knowledge** risk, not only technical ones; decisions with confidence, basis and a tripwire; open questions with owners and defaults |

## Produces (what the next stages read)

`00-start/brief.md`, `glossary.md`, `cases/`; `10-world/facts-register.md`, `existing-system.md`, `constraints.md` (and `divergence.md` in rescue mode); `20-risks-and-decisions/risks.md`, `spikes/`, `decisions/`, `open-questions.md`.

## Close

When layers 0-3 are passed or skipped, close per the stage protocol and ask whether to continue with **services and components** (`plan-components`).
