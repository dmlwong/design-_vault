---
type: concept-brief
status: draft
owner: design-system
platform: connected-platform
surfaces: [Other / shared]
source: product
last_reviewed: 2026-07-31
tags: [orbit, discovery, concept-brief, reverse-brief]
---

# Concept brief (reverse): Initiatives tracker — extracted from the Lovable prototype

> **Produced by reverse-brief mode** (`design-brain/agents/brief-coach.md`): the brief was
> extracted *backwards* from an already-built prototype, and every question the prototype
> could not answer is recorded in the typed gap report below rather than guessed.
>
> **Honesty note:** this run was made against the archived prototype source
> (`design-brain/examples/lovable-initiatives-port.md` and its benchmark record) without the
> original owner in the room — it is the worked demonstration for the Concept Desk. Items
> only the owner can answer appear as gaps; nothing has been invented to fill them.

**Requester:** *(prototype owner — to be confirmed)* · **Team:** — · **Submitted:** 2026-07-31

## A · Which corner of Efficio
- **Platform:** Connected Platform (internal)
- **Surface / feature area:** Initiatives workflow (AUT01)

## B · The problem
- **Problem statement (extracted):** Consultants working a large initiatives portfolio
  (the prototype renders 623 rows) need to scan, filter, and act on initiatives in one
  working view instead of navigating them one at a time. *Extracted from what the
  prototype builds, not from the owner's own words — confirm with the owner.*
- **Why now / evidence:** **Not answerable from the prototype.** No ticket, request, or
  measure is encoded in a UI. → gap report, open question #1.

## C · Who and what they do
- **Primary user + situation (extracted):** An internal consultant or PM reviewing the
  AUT01 initiatives portfolio mid-engagement. *The prototype implies the user; it cannot
  name their moment — confirm.*
- **Key journey / tasks (extracted from the built UI, in order):**
  1. Scan the initiatives table (sortable columns, badges for status, stage, savings variance)
  2. Narrow it — search box, status/stage filters, column-set and density controls
  3. Inspect one initiative (selected-detail panel)
  4. Act on it (row actions: View / Edit)

## D · Success and edges
- **Key outcomes:** **Not answerable from the prototype** — a UI shows behaviour, not the
  measure of success. → gap report, open question #2.
- **Out of scope / non-goals:** **Not stated anywhere in the prototype.** → open question #3.
- **Known constraints (observed):** the prototype assumes a virtualized table for 623
  rows; Orbit `Table` has no virtualization contract (the port substituted pagination).
  Granular column checkboxes have no contracted Orbit pattern (the port substituted
  column-set presets).

## E · What already exists
- **Existing material:** the Lovable prototype (ShadCN/Tailwind), its full Orbit port, and
  a scored benchmark: `design-brain/examples/lovable-initiatives-port.md`,
  `_benchmarks/results/2026-06-15-lovable-port.md`.
- **Open questions / assumptions:** see the typed gap report — that list *is* the value of
  this exercise.

## Gap report (typed — this is what the prototype could not answer)
> Each gap is typed so it lands somewhere: **edge cases** seed the Definition Pack's
> scenario matrix as E-rows; **open questions** become C-items with owners; **risks** go to
> the verdict; **duplication** goes to the desk.

| # | Type | Gap | Suggested owner |
| - | ---- | --- | --------------- |
| 1 | open question | What prompted this — which ticket, client ask, or number? The UI encodes no evidence. | Prototype owner |
| 2 | open question | What does success look like — what would be counted or observed? | Prototype owner |
| 3 | open question | What is deliberately out of scope? Nothing in the UI says. | Prototype owner |
| 4 | open question | Savings-variance column: where does the number come from, who maintains the calculation? | Data team |
| 5 | open question | System of record for the initiatives rows — which source feeds this table? | Data team |
| 6 | risk | RBAC: the prototype shows every initiative and every value to everyone. Who must *not* see savings figures? | Prototype owner + platform |
| 7 | edge case | Empty, loading, and error states: absent from the prototype (the port had to add them). | Concept team |
| 8 | edge case | Scale: behaviour at 623+ rows — virtualization assumed, no Orbit contract exists; pagination substituted at port. | Build team |
| 9 | edge case | Repeated row actions ("View", "Edit") lacked row-specific accessible names. | Build team |
| 10 | duplication | The initiatives surface is also targeted by an in-flight concept: `discovery/research-agent-in-initiatives-cp-orbit.md`. Overlap unexamined. | Concept desk |

## Gate log
> Not yet submitted — reverse-brief output goes to the owner for confirmation of the
> extracted sections, then into `brief-review` like any other brief.

| Date | Verdict | By | Notes / gaps / override reason |
| ---- | ------- | -- | ------------------------------ |
| — | not yet submitted | — | Awaiting owner confirmation of extracted sections B–D |

## Graduation
- **Discovery pack:** not yet

<!-- graph-links:start — generated by tools/gen_graph_links.py; do not hand-edit -->
## Vault graph
[[_benchmarks/results/2026-06-15-lovable-port|2026-06-15-lovable-port]] · [[design-brain/agents/brief-coach|brief-coach]] · [[design-brain/examples/lovable-initiatives-port|lovable-initiatives-port]] · [[discovery/research-agent-in-initiatives-cp-orbit|research-agent-in-initiatives-cp-orbit]]
<!-- graph-links:end -->
