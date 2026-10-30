# Writing a good slice spec

The reader is a builder with the repository open and nothing else. The spec must let them start without asking, and must not tell them more than they need.

## What goes in

- **Files to inspect** and **files to change**, each change with a reason (one phrase). A file you cannot name yet is a gap in the investigation.
- **The smallest implementation** that meets the slice's demo, in a few sentences: what is added, what is reused, what is left alone.
- **Data and interfaces touched.** Point to the design rows and decision records; restate only what the builder must not get wrong.
- **Configuration and migrations.** Each new setting with its default; each schema change as add, then switch, then drop, with a working way back and a test. Classify each as hard or easy to change.
- **Tests and verification:** the demo command and pass line from the plan, plus the unit or integration tests that give the builder a fast loop. Name the fixtures.
- **Non-goals:** what this slice must not do, including tempting neighbours.
- **Decisions made here,** one line each, and **questions for the owner** with a recommended answer.
- **Ready check:** the list below, ticked.

## What stays out

The plan's reasoning, the design's tables, history, alternatives already decided, and anything the builder can read in the code in a minute.

## The ready test: significant decisions

A decision is *significant* if another piece, another team or a later slice will depend on it, or if reversing it later means rework. Walk this list; each item is made in one line, points to a confirmed record, or is not relevant:

- data shape and storage layout, including keys, ids, indexes and migrations;
- interface shape: names, fields, versions, status and error codes;
- new dependencies or services;
- error handling, retries, timeouts and idempotency;
- concurrency, ordering and locking;
- security and access checks, and what is logged;
- configuration and secrets;
- how it is deployed and switched on or off;
- how it is tested, and with what fixtures.

Small choices (names inside a function, local structure) are the builder's, and need no line.

## When the ready test fails

If a significant decision is unmade: if it is easy to change, make it in the spec and say so; if it is hard to change, stop and send it to its owner with your recommendation, via `feature-plan`'s change handling. Never choose it quietly. If the spec would pass 80 lines, the slice is too big: split it and say how.

## Spec size by kind of slice

A slice that adds a piece to an existing module: short, mostly files and tests. A slice that creates a new service or crosses a boundary: longer, but the boundary rows stay in the design; the spec holds the wiring, configuration and deployment.
