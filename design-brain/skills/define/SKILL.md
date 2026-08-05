---
name: define
description: Turn a Ready concept into agreed behaviour before anyone builds — a scenario & behaviour matrix (green paths, edge paths, the rules they rely on, and the open questions with named owners) authored in Excel with the tool owner and data team, kept canonical as markdown in the vault, and projected into an interactive journey-flows page. Use AFTER a brief passes the gate and its explore prototype has shown the value, and BEFORE the build team commits a sprint. Triggers on: "define the behaviour for <concept>", "build the scenario matrix", "we need the journey flows", "what happens when <edge case>", "turn the gap report into a definition pack". This is the converge-on-behaviour capability — it does not design UI and does not use Orbit components; when the goal is to build the screens, use `build-screen` / `port-to-orbit` instead.
---

# Define — agreed behaviour before anyone builds

This skill produces the **Definition Pack**: the second stage of the pack chain, run only
for concepts whose verdict is Ready. Explore asked *is this worth building?* Define asks
*exactly what does it do — including when things go wrong, and who decides what we don't
yet know?* It is the last cheap moment to discover that two teams meant different things.

| | This skill (Define / converge on behaviour) | explore (diverge) | build-screen, port-to-orbit (build) |
| - | - | - | - |
| Stage | After the gate, before the sprint | Before the gate | After definition |
| Question | *What does it do, exactly?* | *Is this worth building?* | *How does it look and ship?* |
| Output | Matrix + journey flows | A clickable concept | On-system screens |
| Audience | Tool owner, data team, build team | Stakeholder | Build team |
| Done when | Every scenario has an outcome and every unknown has an owner | The bet is testable | It matches the design system |

## The method (five steps — do them in order)

### 1. Seed from the gap report — never re-discover
The Concept Pack's typed gap report already did this work. Convert it, don't repeat it:
- every **edge case** becomes an E-row (that is what the type is for);
- every **open question** becomes a C-item, carrying its named owner across;
- every **risk** you cannot close becomes a C-item too, not a silent assumption.
Read the source brief and its gap report first. If a gap arrives with no owner, get one
before you write it down — an unowned question is a question nobody is answering.

### 2. Author in Excel — meet the people who decide
The tool owner and data team live in spreadsheets, and agreement happens where they work.
Start a blank workbook, or take an existing matrix out for editing:

```
python3 tools/matrix_xlsx.py template -o <concept>.xlsx        # new
python3 tools/matrix_xlsx.py export <matrix>.md -o <name>.xlsx # existing, for a round of edits
```

Tabs: **Meta** (identity + frontmatter), **Rules** (R-items every journey relies on),
**Clarifications** (C-items, each with an Owner), **Green Path** (G-rows) and **Edge Paths**
(E-rows). Every scenario row carries the same nine fields — subtitle, the rules it relies on,
starting state, user actions, backend, front-end result, next action, expected outcome, and
a **worked example with real-shaped numbers**. The worked example is not decoration: it is
where the disagreement surfaces.

### 3. Import — markdown is the canonical copy
```
python3 tools/matrix_xlsx.py import <name>.xlsx -o discovery/definition/<slug>.md
```
Set `**Source Concept Pack:**` to the Ready brief's path in backticks — that link is what
lights the concept's *Defined* stage on Vault Health, and what the link checker validates.
The importer refuses a C-item with no owner and a scenario missing any of its nine fields:
an incomplete matrix should fail loudly here, not quietly in a sprint.

### 4. Generate the journey flows
```
python3 tools/build_journey_flows.py discovery/definition/<slug>.md -o artifacts/<slug>-journey-flows.html
```
This page is a **projection** — never hand-edit it; edit the matrix and regenerate. CI fails
the build if the two drift apart.

### 5. Walk the C-items with their owners
Take every open clarification to the person named on it and come back with a decision or a
date. C-items block **build**, not definition: a matrix that ships with six honest open
questions is finished work; one that ships with six silently-resolved guesses is not.

## Non-negotiables
- **Markdown is canonical, Excel is a working surface.** Round-trip through the importer;
  never hand-edit a generated flows page.
- **Every open question carries a named owner.** No owner, no C-item.
- **Every scenario states its outcome and the rule that guarantees it.** "It works" is not
  an expected outcome.
- **Edge paths are not optional.** A definition with only green paths has defined the demo,
  not the product.
- **Record what is still open, honestly.** Mark a scenario `(open)` when it hangs on an
  unconfirmed C-item rather than writing a confident guess.

## Scope
Define decides **behaviour**, not visual design: no components, no tokens, no layouts. Those
attach at `build-screen` / `port-to-orbit`, where the Orbit Definition of Done applies. A
reviewer reading a matrix judges completeness and honesty, nothing else.

## Handoff
- The build team, via `build-screen` — they receive agreed rules, every edge case, and the
  open questions that still gate them.
- Worked example to follow: `discovery/definition/clauseiq-supplier-rounds.md` with its
  committed workbook beside it (14 rules · 18 scenarios · 6 owned clarifications).

## Invocation
`/define <the Ready brief>`. If the brief is not Ready, say so and stop — defining behaviour
for a concept that has not proven its value is the expensive mistake this pipeline exists
to prevent.

<!-- graph-links:start — generated by tools/gen_graph_links.py; do not hand-edit -->
## Vault graph
[[discovery/definition/clauseiq-supplier-rounds|clauseiq-supplier-rounds]]
<!-- graph-links:end -->
