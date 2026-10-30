# Writing the docs

The test of a doc: **a competent newcomer reads it and understands what is going on and why, without asking anyone.** A doc that only lists what the system does does not pass. It must explain.

## State versus explain

A doc that **states** says "Actions are capped at 8." A doc that **explains** says "We cap suggested actions at 8, because in the three real cases recruiters acted on at most 5, and more than 8 buried the important ones. If recruiters start asking for more, this is a one-line change."

Explaining means giving, for each important point: the **why**, an **example**, the **evidence and its status**, and **what would change it**. Put the plain statement first, then the reasoning.

## The shape of a doc

1. **In plain words.** Two to five sentences, no jargon, written for a stranger. If you cannot write this, you do not understand the thing yet; go back and ask.
2. **The detail.** Tables for registers and comparisons, numbered prose for flows, real example payloads for contracts.
3. **Status and evidence.** What is decided, what is a hypothesis, what is unknown, and where each claim comes from.
4. **What would change this.** The observation that would make you revise it.

The template for each kind of doc already has these sections. Fill them in; do not delete them to look tidier.

## Voice and language

- Plain words. Say "the clerk uploads the invoice", not "the actor initiates document ingestion".
- Use the users' terms (from the glossary). If the team and users use different words, write the user word and note the team word once.
- Short sentences. One idea each. Active voice.
- Concrete before abstract: an example first, then the rule it illustrates.
- Numbers over adjectives: "filled in for 70% of 200 sampled records", not "usually filled in".
- No filler ("it is important to note that"). No hedging inflation: say "hypothesis" once, where it belongs.
- Name the person or system that acts: "the matcher returns", "the clerk confirms", not "it is determined".

## Status labels in text

When a claim is not obvious, tag it:

| Tag | Meaning |
|---|---|
| **[D]** | from a document someone wrote, not checked |
| **[M]** | measured by us on real data (say sample and date) |
| **[I]** | inferred by us (say from what) |
| **[T]** | needs a test before anyone relies on it |
| *invented* | made up as an example; replace with a real one |

Facts register rows use the status column; decisions use `confidence`. In prose, tag only what a reader might otherwise take as settled.

## Tables, prose and examples

- **Tables** for lists of like things (facts, artifacts, risks, slices, concerns). Keep cells short; put long text in prose under the table.
- **Prose** for reasoning: why, trade-offs, "what would change this".
- **Examples** for contracts and flows: a real message beats a description of a message.
- **Numbered steps** for flows and procedures.
- **Diagrams are welcome in the HTML pages, never in the markdown docs.** A diagram is either generated from the documents' tables or authored once into `html-src/authored.json` (`references/share-pages.md`), and each carries a caption saying what it was generated from. The markdown docs stay diagram-free: a table of "from, to, when" does the job there, and a diagram in a doc goes stale.

## Length

- One doc, one purpose. If you are writing "and also", you probably have two docs.
- Aim for under about 150 lines. Past that, split and link; the index keeps it findable.
- Do not copy source material into a doc. Summarize what it settles, cite it, and link.
- Do not repeat across docs. State a thing in one place and point to it; decisions are referenced by id.

## Keeping docs easy to change

- Stable ids; never renumber (pins and links rest on them).
- One decision per file; one component per file; one contract per file.
- Change meaning: bump `version`. Change a typo: do not.
- When something is replaced, mark the old doc `superseded` and leave it: the reasoning is history, not clutter.
- Record every requirement change in `change-log.md` with what it reopened.

## Good and bad, side by side

**Bad (states):**
> The matcher uses supplier name, amount and PO number to match invoices. Unmatched invoices go to manual review.

**Good (explains):**
> **In plain words:** The matcher finds the supplier and purchase order an invoice belongs to. It tries exact rules first and only asks a person when the rules cannot decide.
> On 50 past invoices, the rules alone got 41 right and 0 wrong; the other 9 had no PO number or two candidate POs, which is where a person helps. **[M]** (spike S-001, sample of last quarter).
> We chose "no wrong matches" over "fewest manual reviews" because a wrong match posts money to the wrong supplier, whereas a manual review costs a minute. **Would change if:** reviews exceed 30% of invoices, which would justify trying a model on the leftovers.

**Bad (a decision with no reasoning):**
> Decision: use approach B.

**Good:**
> **Choice:** Approvals live inside the product, not in the ERP. **Alternatives:** ERP workflow (simpler, but cannot express delegation while on leave). **Why:** delegation rules are the main user need (CASE-02). **Would change if:** the ERP adds delegation, or finance mandates its workflow. Confidence: hypothesis (not yet tested with finance).

## Before you mark a doc agreed

- Does "In plain words" make sense to someone who has never seen the feature?
- Is every claim either obvious or tagged?
- Is there an example where a stranger would ask "what does that look like?"
- Does it say what would change it?
- Are all TODOs gone? (`wsctl.py check` warns on agreed docs with TODOs.)
- Is the `summary:` good enough that the index alone tells a reader whether to open it?
