---
id: FLOW-USER
title: User flow
layer: 4
kind: flow
status: agreed
version: 2
updated: 2026-10-25
summary: From PDF upload to posted invoice for the clerk and the manager, with five re-entry points the clerk can use
depends_on: [BRIEF@1, CASE-01@1, CASE-02@1, CASE-03@1, RISKS@2]
read_sets: [onboard, understand, review]
---

# User flow

## In plain words

The clerk uploads an invoice and sees what the system read, which PO it matches and what codes it proposes. The clerk can fix any of those, redo one part, or pick the PO directly. When satisfied, the clerk sends it to a manager, who approves or rejects. Approved invoices post to the ERP.

## The story, step by step

Walked with CASE-02 (partial delivery, approver away).

1. The clerk uploads the PDF. The system shows the extracted fields beside the PDF.
2. The clerk fixes a misread total (a correction). The fields are saved.
3. The system proposes the PO and flags "3 of 10 lines not yet received". Because the receipt is short, the clerk must record a decision: hold, or approve as billed with a reason.
4. The system proposes accounting codes. The clerk changes one code.
5. The clerk sends for approval. The system routes it to the manager's delegate, because the manager is on leave.
6. The delegate approves. The record shows who approved, as delegate for whom.
7. The system posts to the ERP (after checking nothing was posted before) and shows "posted" with the ERP reference.

## Other paths

- **Alternate paths:** no PO number (CASE-03: candidates are listed and the clerk picks); the clerk already knows the PO and skips the automatic match.
- **What differs by role or permission:** clerks upload, fix and send; managers and delegates approve within their limit; nobody approves an invoice they uploaded.
- **When something fails, and how the user recovers:** an unreadable scan shows "could not read this invoice; enter it by hand". An ERP outage leaves the invoice "approved, not posted" and it retries.
- **When the user leaves halfway and comes back:** everything is saved at each step; the invoice reopens where it was.

## Re-entry points

| Step | User can see | User can correct | Regenerate alone | Skip | Artifact |
|---|---|---|---|---|---|
| Read the invoice | Yes, fields beside the PDF | Yes | Yes (re-read the PDF) | No | ART-01 |
| Match to a PO | Yes, with reasons | Yes (pick the PO) | Yes (re-match) | Yes (clerk picks directly) | ART-02 |
| Propose codes | Yes | Yes (edit lines) | Yes (re-propose) | No | ART-03 |
| Approval | Yes, with who and when | No (manager decides) | No | No | ART-04 |
| Post to the ERP | Yes, with the ERP reference | No | Yes (retry) | No | ART-05 |

## Re-entries ruled out

- Skipping the read step: the fields are needed for everything after; the clerk can correct them instead.
- Regenerating an approval: it is a person's decision, never generated.
- Editing a posted invoice: reversal is a separate ERP process, out of scope.
