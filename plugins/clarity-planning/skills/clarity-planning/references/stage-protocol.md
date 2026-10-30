# Stage protocol (shared by every stage skill)

The planning method is split into stage skills that can be invoked on their own and depend on each other through the **workspace**: the docs one stage writes are the inputs the next one reads, and the layer gates in `90-log/gates.md` record what is settled.

| Stage | Skill | Layers | Needs done (passed, passed with conditions, or skipped) |
|---|---|---|---|
| Clarity | `plan-clarity` | 0 Intake, 1 Outcome and value, 2 World and facts, 3 Risks and decisions | nothing |
| Services and components | `plan-components` | 4 User flow and re-entry, 5 Artifacts and staleness, 6 Components | 0-3 |
| Flows and contracts | `plan-flows` | 7 System flow, 8 Cross-cutting, 9 Contracts | 4-6 |
| Build plan | `plan-build` | 10 Implementation plan | 7-9 |
| Change | `plan-change` | 11 Change protocol | nothing; any time |
| Review | `plan-review` | none | nothing; any time |

`<hub>` below means the `clarity-planning` skill folder, which sits next to every stage skill's folder (`<this skill's folder>/../clarity-planning`). Its scripts, templates and guides are shared by all stages. Run the tool as `python3 <hub>/scripts/wsctl.py`.

## Every stage runs these steps

### 1. Find the workspace
Run `wsctl.py find <project root>` (it lists every folder with `90-log/gates.md`), or use the path the user gives.

- **Found:** use it. Do not start a second workspace for the same feature.
- **None, and this is `plan-clarity`:** it creates the workspace (intake is owned by `plan-clarity` alone; see its skill).
- **None, and this is a later stage:** tell the user no plan exists and offer to start with `plan-clarity`. If they decline ("we know the domain, just do components"), this stage creates a minimal workspace itself:
  1. Ask once for the location, the size and the mode, then run `wsctl.py init <path> --name "<Feature>" --size <s> --mode <m>`.
  2. Write a short brief marked as hypotheses (outcome in a sentence, who acts) and one case labelled `invented` (layer 4 needs a case to walk).
  3. Mark layers 0-3 `in-progress` with the note "declined by user; proceeding on hypotheses" (`wsctl.py gate <ws> <layer> in-progress --notes "..."`). Never mark them `skipped`: `skipped` means the size does not need a layer, and it would hide that the facts were never checked.
  4. `wsctl.py stage` then reports "proceeding on hypotheses" instead of pointing back at clarity.

`init` always comes before `stage`: the stage command reads the workspace.

### 2. Check readiness and create this stage's docs
Run `wsctl.py stage <ws> <stage>`. It lists the layers this stage needs, their gate status, any conditions carried from earlier gates, the layers it owns, and the docs from earlier stages. If it says this stage's docs are not created yet, run `wsctl.py init-stage <ws> <stage>`.

- **READY:** continue. Read any conditions it lists; they are open items this stage must respect.
- **PROCEEDING ON HYPOTHESES:** the user declined earlier layers. Continue, recording every assumption about them as a `hypothesis` decision or open question.
- **NOT READY:** tell the user plainly which earlier steps are open and what that risks (for example: "components designed before the facts are checked may rest on fields that do not exist"). Offer two choices and let them pick:
  1. **Go back:** run the earlier stage first (invoke its skill).
  2. **Proceed anyway:** continue, record every assumption as above, and add to this stage's gates the note "started before layer N passed". When the earlier stage later passes, run `plan-change` to reconcile.

  If nobody can answer (unattended), proceed anyway with the notes.

### 3. Load only what this stage needs
- Once per session (skip if already read in this session): `<hub>/references/session-protocol.md` (rounds and gates) and `<hub>/references/next-question-engine.md` (what to ask next).
- The layer guides for this stage's layers: `<hub>/references/layers/NN-*.md`.
- The earlier-stage docs this stage rests on, from the `stage` output. Read their **summaries** first; open a doc fully only when a question touches it. `wsctl.py read-set <ws> <id>` lists one doc (or table row such as `ART-02`) and what it rests on.
- Other shared guides only when a situation calls for them: `uncertainty-playbook.md`, `standard-practices.md`, `ai-components.md`, `doc-writing-guide.md`, `depth-sizing.md`, `workspace-structure.md`.

Do not re-ask what earlier stages settled. If something they settled looks wrong, say so and use `plan-change`, rather than silently overriding it.

### 4. Work each layer in order
For each layer this stage owns: mark it in progress (`wsctl.py gate <ws> <layer> in-progress`), run rounds (see the session protocol: "needs your decision" questions plus "my defaults, object if wrong"), write what is learned into the docs with statuses, and when the layer guide's gate checklist is met, present the gate.

### 5. Gates: the user decides, explicitly
A gate has three honest outcomes:

| Outcome | When | Command |
|---|---|---|
| **passed** | Every checklist item is met, and the user explicitly agrees | `wsctl.py gate <ws> <layer> passed --evidence "<doc ids; who agreed>"` |
| **passed with conditions** | The user agrees, but some items cannot be met yet (no access to real data, the other team unreachable, a spike that cannot run before building) | `wsctl.py gate <ws> <layer> passed-with-conditions --evidence "..." --notes "<each condition>"` |
| **in progress** | The user does not agree, or items are open that could be closed now | leave it; say what is missing |

- **Only the user's explicit yes passes a gate.** Silence, a change of subject, or a yes with an open concern is not agreement: ask once more, briefly.
- **Before presenting a gate** for contracts, flows, components or the build plan, the stage may offer `plan-review` (a cold read by reviewers with no context) and apply its findings first. The user may skip it. A review is advice, not agreement.
- **Conditions are not forgotten.** Later stages see them in `wsctl.py stage`, and `plan-build` turns each into an early slice (often slice zero).
- **Passing promotes the layer's docs** from `draft` to `agreed` (the `gate` command does it). Docs that wait on someone else should be `pending` instead of agreed: a spike not yet run, a contract the other side has not seen. Set those to `pending` BEFORE running the gate command, including invented cases (`invented: true` or a `Source:` line saying invented): the command leaves such docs as `draft` and names them, but it is on you to mark them `pending`.
- **The user rejects a gate** on a layer that is still in progress: fix the doc in place and re-ask with a one-line summary of what changed. No change-log entry and no version bump, unless other docs already pin this one (then `bump` and reconcile them).
- A layer the size does not need is marked `skipped` with the reason, after telling the user.
- Unattended runs never pass a gate: gates stay `in-progress` with notes on what each waits for.

### 6. Close the stage
When every layer of the stage is passed, passed with conditions, or skipped:
1. Run `wsctl.py check <ws>` and fix errors; mention any warnings that remain and why.
2. Run `wsctl.py index <ws>`. When HTML is wanted, run `wsctl.py html <ws>` then `wsctl.py html <ws> --check`.
3. Give the stage summary: what is now understood (five sentences), what was decided and with what confidence, the conditions carried forward, what is open with owners and defaults, and what the next stage will rest on. Also tell the user which files this stage wrote (folder and name) and which two or three to read first, and say which folders later stages will fill, so an empty folder is not mistaken for something hidden.
4. **Ask whether to start the next stage**, naming it in plain words ("Next is the pieces: the user flow, what gets stored, and the components. Shall I start?"). You may put the next stage's first round in the same message, so one reply can approve and answer. Only on a yes, invoke the next stage skill. If the user stops, write the next step in `90-log/sessions.md`.

If the stage ends early (the session runs out, the user stops), write `90-log/sessions.md`: covered, waiting on, first thing next time.

## When a stage discovers an earlier stage was wrong

This is expected. Stop, tell the user which earlier doc is affected and why, and run `plan-change`. Do not patch the current stage around a known error upstream.

## Calling stages from the hub

When the user asks generally ("plan this feature", "where are we?"), the hub runs `wsctl.py find` and `wsctl.py stage <ws>` and invokes the next stage skill (or `plan-clarity` when there is no workspace). After each stage closes with the user's yes, it invokes the next. The user can also call any stage directly by name.
