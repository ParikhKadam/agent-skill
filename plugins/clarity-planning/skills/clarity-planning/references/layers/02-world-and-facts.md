# Layer 2: World and facts

**Answers:** For each fact the feature needs: where it lives, who writes it and when, how reliable it is, how we can read it. What exists already? Which limits are imposed and which are our own choices?
**Prevents:** Designing on facts nobody checked. The commonest cause of late rework is a world that differs from what the spec assumed: fields that do not exist or are half-filled, a stale environment, notes that cannot be searched the way the design needs.
**Output:** `10-world/facts-register.md`, `existing-system.md`, `constraints.md`, glossary updates.
**Read first:** The brief and cases (`wsctl.py read-set <ws> understand`).

## How to generate

1. **Start from the cases.** Every "facts we reached for" line becomes a row `F-nn`.
2. **For each fact, fill the row:** where it lives (system, table, field, person), who writes it and when (is it ever late or blank?), reliability (a rate and sample size, or `unknown`), how we read it (API, query, limits that matter), status (`measured`, `doc`, `inferred`, `unknown`).
3. **Check reality yourself where you can.** Sample real records read-only: fill rates, value ranges, how recent, how often wrong. Report numbers with the sample size and date. Compare the environment you can reach to the one users use (a test copy may lag by years).
4. **Probe the access path.** What can the interface do and not do (filters, search versus query, paging, rate limits, permissions)? A design that needs "filter by X" fails if X cannot be filtered.
5. **Complete the inventory** (`existing-system.md`): reuse, extend, avoid; list places where behavior differs from docs, with how you found out.
6. **Sort constraints into imposed versus chosen.** Imposed (an outside system, regulation, contract) bounds the design. Chosen (a past decision or coded rule) can be redesigned when evidence says so. Many "constraints" turn out to be chosen.
7. **Build the glossary further.** Terms users use, what record each leaves, what each is not.
8. **List the unknowns.** Every row you cannot verify now stays `unknown`, goes to layer 3.

## Starter questions

- "Where would I look to find that, and who puts it there?" / "When is it filled in?"
- "Out of ten, how many are filled in right?" (then sample)
- "Is this the same system and data that users actually use?"
- "Has anyone changed how that works recently?"
- "Which of these limits can we change, and who decides?"
- "Is it all right if I read real records, read-only? Which ones?"

## Gate (layer 2 passed when)

- [ ] Every fact the cases reached for has a row with a source and a status.
- [ ] No row is silently assumed: unknowns are `unknown` and have a plan.
- [ ] The access path and its limits are known for each outside system.
- [ ] Imposed and chosen constraints are separated.
- [ ] `existing-system.md` says what to reuse and what surprised us.
- [ ] You have checked reality (data or a probe) for the top facts, not only read docs.

## Depth

small: skip unless the change leans on data you have not seen. medium: register for what the cases reached for, a few sampled facts. large: full register, sampled real data, access limits, constraints sorted, a second pass after the first spike.

## When it goes sideways

- **No access to real data.** If the user is present and agrees, pass the gate with conditions (see the playbook) instead of blocking. Make access the first spike; mark dependents `unknown`; keep the design cheap to change. Do not proceed as if the docs were true.
- **Docs and data disagree.** Trust observation, note the date, record the discrepancy; do not edit the doc silently.
- **The data is sensitive.** Read minimally and read-only; keep names and content out of the docs (ids, counts, shapes); confirm permission once and record it.
- **The environment is stale or empty.** Say so; find the real one or mark every dependent fact `unknown`.
- **A fact depends on a person's memory.** Mark `doc` or `inferred`, name the person, and verify when you can.
- **The register explodes.** Keep only facts a case or flow actually uses. Park the rest.
- **You discover the world is very different from the brief.** That is the layer working. Reopen layer 1 and say so.

## Hands off to

Layer 3: unknowns and risky assumptions become ranked risks and spikes.
