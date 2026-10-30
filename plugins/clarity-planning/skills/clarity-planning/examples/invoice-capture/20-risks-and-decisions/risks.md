---
id: RISKS
title: Risks and unknowns
layer: 3
kind: risk
status: agreed
version: 2
updated: 2026-10-24
summary: Three ranked assumptions; matching by rules and duplicate posting were tested, scan quality is accepted
depends_on: [FACTS@2]
read_sets: [review]
---

# Risks and unknowns

## In plain words

The design rests on three assumptions. The two that scored highest were tested first: whether simple rules can match invoices to POs, and whether the ERP protects against duplicate posts. Scan quality was accepted as a known, cheap-to-handle limit.

| ID | Assumption that could break the design | Impact | Uncertainty | Score | Plan | Status |
|---|---|---|---|---|---|---|
| R-1 | Rules alone can match enough invoices to POs without wrong matches | 3 | 3 | 9 | spike S-001 | tested |
| R-2 | The ERP will not accept the same invoice twice | 3 | 2 | 6 | spike S-002, then mitigate with D-002 | tested |
| R-3 | Scanned PDFs can be read well enough | 2 | 2 | 4 | accept: a scan falls to manual entry; the clerk sees "could not read" | accepted |
