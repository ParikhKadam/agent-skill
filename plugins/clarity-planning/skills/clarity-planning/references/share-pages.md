# Share pages: the HTML set for readers who will not open markdown

`wsctl.py html <ws>` turns the workspace into six self-contained pages and one combined page in `<ws>/html/`. Markdown stays the source and stays diagram-free; the pages add pictures, plain glosses and a reading order. Local files only: no site, no server, no external loads, nothing published unless the user asks.

## The pages and who reads which

| Page | Holds | Read first by |
|---|---|---|
| `start-here.html` | what and why, release panel, "needs you" box, status board, system picture, journey, decisions at a glance, blocking conditions, top risks, who reads what, FAQ | everyone; the product owner stops here |
| `story.html` | the worked cases, the user flow, the glossary | product owner, newcomers |
| `system.html` | stored results, components, system flow, state machine, re-entry matrix, cross-cutting rules, constraints, facts, existing system | lead engineer, component owners |
| `contracts.html` | every contract in full with examples, field tables, shared vocabulary | the teams on each side of a boundary |
| `decisions-and-risks.html` | decision cards, questions, risks with the risk grid, spikes | tech leads, product owner |
| `build-plan.html` | plan, timeline, slices, gate conditions, short change log | whoever builds, the product owner |
| `everything.html` | all of the above on one searchable, printable page | anyone who wants to search |

A page with no source documents is not written and its nav link disappears: no contract documents, no `contracts.html`; no cases, user flow or glossary, no `story.html`; and so on. A section with no source (no slices, no gates, no questions) is dropped from its page the same way. `start-here.html` always exists.

## Rules the pages follow

- Inline CSS and SVG, no external loads, readable without JavaScript. The buttons (expand all, light or dark, copy) are extras.
- Details are collapsed, not removed; "Expand all" opens them for searching.
- Every id (`Q-44`, `C-matcher`, `SL-01`) is a link that resolves; an id that is not defined in the workspace stays plain text.
- Plain glosses at the first use of a term on each page (authored list, below). Status chips for every status.
- Every diagram has a caption that says what it was generated from.
- Each page has a footer with the generation date and the documents it covers, with versions.
- No front matter, tool commands, session logs or absolute paths in the output. Built-in rewrites turn `` `wsctl.py ...` `` into "the workspace tool" and file names such as `open-questions.md` into the doc id; anything else goes in `rewrites` (below).

## Build and check

```
python3 <skill>/scripts/wsctl.py html <ws>             # build into <ws>/html/ (start-here.html first)
python3 <skill>/scripts/wsctl.py html <ws> --check     # validate; prints a report; exit 1 on FAIL
python3 <skill>/scripts/wsctl.py html <ws> --classic   # the old three flat pages (overview, flows, plan)
```

The check fails on: a page missing or out of date with the markdown, a document shown in no page or in two, a dangling link or duplicate anchor, an id mentioned without a link, banned content (paths, tool commands, front matter, external loads), a missing header, footer, print or dark CSS. It warns, but does not fail, for each authored diagram or item that is missing. A page with no source is reported as N/A. Fix FAILs in the markdown or the authored data, then build and check again.

Without `html-src/authored.json` the build still works: everything generated from the markdown tables is drawn (dependency map, timeline, status board, risk grid, permission grid, tables), and every authored diagram shows a dashed box saying `not authored yet: see references/share-pages.md`.

## Authored data

Some pictures cannot be generated from tables: the system context, the journey, sequences, the state machine, the failure tree, the wireframe. Their data, and the plain-words text around the pages, is authored once in `<ws>/html-src/authored.json`. It is **JSON, never code**: the builder reads data and never runs anything from a workspace. It lives only there; keep a copy nowhere else. The builder never edits it.

All keys are optional. Shortened examples are from the real transcript-summarization workspace.

| Key | What it is | Example |
|---|---|---|
| `brand` | name in the header and page titles; default is the brief's title | `"Transcript summarization v2"` |
| `id_key` | the "Id key" line in the header; default is built from the id prefixes found | `"D decision · Q question · R risk ..."` |
| `heroes` | per page: `h1` and `lede` for the top box; `{n_slices}` style counts are filled in | `{"story": {"h1": "Four worked calls ...", "lede": "..."}}` |
| `titles`, `nav`, `sowhat` | per section id (`st-risks`, `sys-flow`, `bp-log` ...): heading, short nav label, the one-line "so what" under it. Counts: `{n_open}`, `{n_slices}`, `{n_def}`, `{n_log}`, `{n_risks}`, `{n_top_score}`, `{top_score}` | `"dr-questions": "{n_open} questions are open ..."` |
| `texts` | named bits of prose around diagrams and tables (`statebar`, `picture_note`, `needs_intro`, `risk_note`, `status_note`, `conditions_text`, `full_run_heading`, `timeline_freeze`, `answers_recorded_title`, and a few more; the builder uses a plain default when one is missing) | `"statebar": "The build has not started. ..."` |
| `rewrites` | `[pattern, replacement]` regex pairs applied to markdown text before it is shown: remove references that only make sense in markdown, or name a role | `["Details: `10-world/existing-system\\.md`\\.", "Details: EXISTING."]` |
| `glosses` | `[key, regex, plain gloss, source]`; shown once per page after the first match | `["stub", "\\bstubs?\\b", "a stand-in for one side ...", "K-01 Stub"]` |
| `source_tag_prefixes`, `guess_title` | prefixes of grey source tags such as `[WG P4]`; the tooltip of the `(h)` guess chip | `["JG", "WG"]` |
| `home_override`, `order` | which page shows a doc when its `kind` is not enough; display order by kind (`component`, `slice`, `case`, `decision`, `spike`, `contract`) | `{"order": {"slice": ["SL-00", "SL-01"]}}` |
| `tracks`, `owner_tracks`, `join_slice_prefix` | tracks as `[letter, label, svg class nb/nl/nf]`; which owner prefix puts a component in which track (`""` matches anything); slices with this id prefix get the join lane | `[["B", "Backend (B)", "nb"]]`, `{"backend": "B"}`, `"SL-J"` |
| `start_chips`, `start_covers`, `worked_example` | status chips in the first box; extra documents named in the page footer; which case supplies the worked example (`case`, and `starts_with` to pick one bullet) | `[["pending", "admin rules pending"]]` |
| `release` | the release panel; parsed from the plan's section "Release 1, blockers and estimates" when it exists, and any of `contains`, `not_contains`, `estimates`, `blocking`, `blocked_by`, `title`, `tag` here overrides it | `{"blocked_by": "the owners must see K-01 ..."}` |
| `needs` | rows of the "needs you" box: `[what, item id, who decides, recommended answer, what it blocks]` | `["Start dates ...", "Q-44", "the owner", "start together", "blocks SL-00"]` |
| `tech_gloss`, `faq`, `condition_notes`, `where_we_are` | plain words for technical terms `[term, meaning]`; questions `[question, answer]`; notes under the conditions; the "where we are" bullets | `["Redis", "a fast in-memory store ..."]` |
| `readers` | the who-reads-what table: `who`, `people`, `pages` as `[page, id, note]`, `also` ids, `slices` | `{"who": "Backend", "pages": [["contracts", "K-01", "publish side"]], ...}` |
| `risk_top`, `risk_short`, `risk_plain`, `risk_r1` | the top risks on start-here; a short title per risk for the grid; one plain sentence of what happens if it comes true; ids that can stop release 1 | `{"R-1": "Live data is good enough"}` |
| `case_notes` | per case, one `[ids, note]` per bullet of the ideal result: how the system gets there | `"CASE-01": [[["C-topics", "ART-03"], "Part topics. ..."]]` |
| `art_part`, `dependency_edits`, `dependency_map` | which part each stored result belongs to; the "if X changes, these go stale" rows `[change, [outdated ...]]`; the dependency map's hub component, its label and its component order | `{"hub": "C-orchestrator", "hub_label": "the orchestrator"}` |
| `reentry` | the re-entry matrix: `cols`, `rows` as `[action, cells, note]` with one letter per column (`R` reruns, `O` outdated, `U` untouched, `o` outdated only if the effective set changed), `star_note` | `["Edit a topic selection", "UUOOO", "no Landi run"]` |
| `journey` | the journey strip: `steps` as `[title, what happens, re-entry or null]`, and a `note` | `["Check topics", "Pick from the 27", "pick, deselect"]` |
| `scope_map` | text of the scope map: `before`, `phase1_title`, `phase1` lines, `later` as `[phase number, title, text]`, `nongoals` | `{"later": [[2, "Phase 2: insights", "..."]]}` |
| `timeline_conditions`, `retired`, `permission_labels`, `permission_debug_actor` | bullets under the timeline; retired slices with why; short labels for permission grid cells (`[prefix, label]`, a prefix starting `~` matches anywhere); the actor row shown as "debug switch only" | `[["metadata only", "metadata only"]]` |
| `diagram_text` | per generated diagram letter (`B`, `E`, `G`, `I`, `J`, `K`, `L`, `M`): override `title`, `desc` (screen-reader text) or `caption` | `{"L": {"caption": "Generated from ... Short titles are authored."}}` |
| `diagrams` | drawings: `system_context`, `state_machine`, `failure_tree`, `wireframe` (see below) | |
| `sequences` | list of sequence diagrams: `key`, `title`, `desc`, `lifelines` `[id, [label lines], class]`, `steps`, `caption`, `width`, `size` (`full` for the big one, `small` for the grid) | `{"k": "msg", "from": "P", "to": "B", "t": "refresh"}` |
| `contracts` | per contract: `fields` (`required_until`, `conditional` notes for the field tables), `wire` (rows `[label, html]` for "on the wire"), `extra_example_sections`, `vocabulary` rows `[group, value, meaning, used in]`, `vocabulary_note`, `codes_from`, `codes_used_in`, `keys_html`, `inputs_html` (raw HTML for the keys and inputs sections; ids inside are linked) | `"codes_from": "K-02"` |

Step kinds in a sequence: `msg` (arrow `from` to `to`; flags `q` queue, `cb` callback, `ret` reply), `self` (a note box on lifeline `at`), `band` (a full-width label). `h` is the row height.

A drawing is a list of primitive operations, one `[op, [args]]` or `[op, [args], {kwargs}]` each, in drawing order, plus its size and texts:

```
"state_machine": {"w": 980, "h": 520, "title": "Part state machine", "desc": "...", "caption": "Generated from K-03 ...", "wide": 720,
  "ops": [["node", [30, 60, 200, 70, "ng", "not_started", ["nothing requested yet"]], {"tcls": "tt"}],
          ["poly", [[[230, 95], [370, 160]], "e", "a"]], ["label", [280, 110, "published", "tl"]]]}
```

Operations: `rect x y w h class rx`, `text x y string class anchor`, `node x y w h class title lines` (a titled box), `poly points class marker`, `label x y string class anchor` (text with a halo), `raw svg`. Classes come from the page CSS: boxes `nb` backend, `nl` second track, `nf` third track, `nx` outside system, `nq` queue, `ng` neutral, `na` attention, `nok`, `nbad`; arrows `e`, `eq`, `ecb`, `edash`, `ebad`. The `wireframe` drawing also carries `"case": "<case id>"`: it appears after that case on `story.html` and on `start-here.html`.

Use a small script or a careful editor to produce coordinates; there is no auto layout. Keep the JSON in version control with the workspace.

## Authoring the diagrams that cannot be generated

The rule: **draw only what a document says, and say which document**. A node, arrow, state or label that no sentence supports is an invention; leave it out and ask.

1. **System context** (`diagrams.system_context`): the parties and boundaries named in the system flow, the contracts, and the decisions about who talks to whom. One box per party or store, one arrow per message in the contracts, labelled with the contract id. Caption: "Generated from FLOW-SYSTEM, K-01 to K-03 and D-007".
2. **Journey** (`journey`): the numbered steps of the user flow, in order, one line of what the user sees each. Mark a step as a re-entry only where the user flow's re-entry table names it.
3. **Sequence diagrams** (`sequences`): the numbered "full run" steps of the system flow, and the rows of its start-points table for the small ones. Lifelines are the components or parties in those steps; message labels use the contract ids.
4. **State machine** (`diagrams.state_machine`): the status values and transitions in the contract that exposes them and the failure table of the system flow. Every arrow needs a row there.
5. **Failure tree** (`diagrams.failure_tree`): the failure table and the "duplicates, retries and concurrency" list of the system flow, one branch per row.
6. **Wireframe** (`diagrams.wireframe`): one screen of one case, at a stated step. Regions come from the case text and the artifact and part names; each region's note says which stored result it shows.
7. **Re-entry matrix** (`reentry`): one row per start point or user action in the system flow, one column per part; cells from the stale rules in the artifact table.
8. **Scope map** (`scope_map`): the phase tables and the Deferred table of the plan, and the non-goals of the brief; the phase 1 lines paraphrase the phase 1 slices.
9. **Release panel** (`release`): the plan's release section; write it here only where the plan lacks it.
10. **"Needs you" rows** (`needs`): the open questions and unmet conditions that block the start; the recommended answer is the one in the questions doc.
11. **Risk wording** (`risk_short`, `risk_plain`): short title and one plain sentence per top risk, paraphrasing the risks table without adding consequences it does not state.

After authoring, build, open the pages, and read each picture against its source section once. Then run `--check`.

## Review by two readers

After a build, have the pages read cold by the two reader roles in `cold-review.md`: the **Product-owner reader** (the one-minute questions, diagrams, jargon, progress, contradictions) and the **Lead-engineer reader** (diagrams against the text, buildability from contracts and slice cards, navigation, stale content). Give each only the `html/` folder. Apply their findings to the markdown or the authored data, never to the HTML, then build and check again.

## Known limits

- Section names in the markdown come from the stage templates ("In plain words", "The ideal result, written by hand", "Slices ...", "Deferred ..."). A renamed section is left out of the page, not guessed.
- The plan's slice tables need `ID` and `Slice` columns; phases come from `### Phase N: title` headings.
- Component tracks come from the card's "Owner:" line and `owner_tracks`; status chips know the common status words only.
- Diagrams are drawn from coordinates you write; the builder checks that they render, not that they are right. The reader roles check that.
- Counts and facts written into `texts`, `titles` and `sowhat` are authored: a change in the markdown does not update them. Use the `{n_open}` style placeholders where a count is available.
- `keys_html` and `inputs_html` are raw HTML fragments, and `wire` values may contain `<code>`; they are not checked against the contracts.
- English only; tested on two workspaces. Print uses the browser's print dialog.
