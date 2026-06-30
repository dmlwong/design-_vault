---
type: foundation
status: in-review
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-06-29
maturity_score: 72
tags: [orbit, design-brain, interaction-defaults, judgment-layer]
---

# interaction-defaults.md — How a screen is structured, and how its output is composed

The **judgment layer**. `tokens.md` and `defaults.md` govern the *material* layer (which token,
which component — closed, checkable, enforced). This file governs the *judgment* decisions that
actually determine UX, at two altitudes: **structure** (#1–#8 — flow shape, information
architecture, interaction model: how the *screen* is organised) and **output craft** (#9–#13 — how
the *deliverable's content* is composed). Read it whenever you choose how a screen is organised or
how its output reads — not just what it's built from. It complements `principles.md` (the values),
`data-viz.md` (single-chart / KPI craft), and `anti-patterns.md` (the don'ts).

Without it, agents fill the structural vacuum with their training prior — the generic,
Orbit-skinned configuration wizard (the Contract Analysis failure, 2026-06-25).

> **Validated (2026-06-29).** In an A/B build of the same tool, applying these heuristics moved an
> adversarial UX score from **7/16 → 15/16 with zero compliance regression** — the wizard
> collapsed into a single content-first surface. The **structural** heuristics (#1–#8) are the
> proven layer. The **output-craft** heuristics (#9–#13) were added 2026-06-29 and are **pending
> their own re-measure** (cycle-2 A/B: Arm J vs Arm J2) before they carry the same validated
> status — see `_review/cycle2-craft-WIP.md`.

> Format: **Signal → Default → Why → Escape hatch.** These are defaults with
> override-for-a-reason — not laws. The escape hatch keeps us from trading a generic wizard for a
> generic dense form. Always state the reason when you take an escape.

---

## 1. Flow shape — form, not wizard, by default
- **Signal:** expert / repeat user · ≤ ~8 inputs · no hard step dependency.
- **Default:** one dense surface (single form or scroll). **Not** a multi-step wizard.
- **Why:** Hick's law + "density over whitespace" + minimize friction for repetitive expert work.
- **Escape:** use a stepper only when later steps genuinely depend on earlier outputs, the
  inputs exceed one legible surface, or the audience is novice / one-time.

## 2. The deliverable is the hero (content-first IA)
- **Signal:** the tool produces an output (report, deck, analysis, dataset).
- **Default:** the output (or a live preview) is the primary surface; configuration is a
  side rail / collapsible panel / compact top bar. Never an all-config screen with the
  result hidden behind a button.
- **Why:** content-first IA; anti-pattern "cards must map to real tools / reports / evidence,
  not config."
- **Escape:** genuine setup-only tasks with no viewable artifact.

## 3. Restraint in status color
- **Signal:** you want to show a container's status.
- **Default:** use the `Card` indicator rail or a `StatusIndicator` / `Badge` — not a
  full-container background color.
- **Why:** "trust through restraint," scannability. Colored containers everywhere read as
  consumer celebration styling, not high-stakes procurement.
- **Escape:** a single, genuinely blocking error may color its own container.

## 4. Don't proceduralize a selection that can be inline
- **Signal:** a step exists only to pick something (e.g. a "Documents" step = a table +
  checkboxes).
- **Default:** inline it into the main surface, not its own wizard step.
- **Why:** collapses steps; density.
- **Escape:** the selection is large/complex enough to warrant its own focused surface
  (e.g. a searchable modal table, per the MarketIQ select-initiative example).

## 5. Minimize steps-to-goal; cut ceremony
- **Signal:** any task with a clear primary goal.
- **Default:** remove intro cards, confirmation steps, and "Next, you can…" filler that
  don't reduce error or risk. Count clicks/screens from entry to goal and shorten.
- **Why:** power-user efficiency; predictability.
- **Escape:** high-stakes / irreversible actions get one explicit confirm step (error prevention).

## 6. Match the platform's existing interaction model (Jakob's law)
- **Signal:** the platform already has a convention (how tools launch, how results show,
  the shell, where context lives).
- **Default:** reuse it. Don't invent a new interaction pattern; precedent wins ties.
- **Why:** "predictability over novelty"; lower learning cost across a long session.
- **Escape:** the existing convention is itself a known anti-pattern (cite it).

## 7. Progressive disclosure + smart defaults
- **Signal:** many optional inputs / lots of configurable depth.
- **Default:** show essentials with sensible pre-fills so the common path is ~one action;
  tuck advanced options behind disclosure (expand / drawer / "advanced").
- **Why:** reduce first-view cognitive load; speed the common case.
- **Escape:** regulated/auditable flows where every option must be explicit up front.

## 8. Demo / prototype affordances are dev-only
- **Signal:** state-preview togglers, "show error" buttons, mock-data switches.
- **Default:** behind a dev flag or omitted. Never shipped UI, never styled `Primary`. No dead or placeholder controls — a control that renders but does nothing (empty options, no-op handler) is a defect, not a stub. Wire it or remove it.
- **Why:** they read as product chrome and steal the primary-action slot.

---

## Information design (output craft)

> #1–#8 decide the *screen*; #9–#13 decide the *deliverable's content* — what the output leads with,
> how findings are composed, what the user can do next. They apply once structure is settled and a
> tool produces an analytical output, and they sit at the output-composition altitude between
> `data-viz.md` (a single chart / KPI) and the structural heuristics above.
> **Status: added 2026-06-29, pending the cycle-2 re-measure** (Arm J vs Arm J2) — these five do
> **not** yet carry the validated status of #1–#8. See `_review/cycle2-craft-WIP.md`.

## 9. Lead with the signal, not the vanity metric
- **Signal:** an output has several numbers, but only some carry the decision (savings at risk,
  worst supplier score, count overdue) while others are vanity (e.g. "12 suppliers analysed").
- **Default:** lead with the decision-driving metric and order tiles / sections by decision-weight
  — riskiest / most-actionable first. The tool does the triage, not the reader.
- **Why:** `data-viz.md` "the number first"; users come for the decision. A row of equal-weight
  tiles offloads triage back onto the user.
- **Escape:** a genuinely flat dataset where no metric dominates — group logically and say so.

## 10. Summaries are drillable — no dead-end numbers
- **Signal:** a summary number, score, or status that stands in for underlying rows / evidence.
- **Default:** every summary is a path to its evidence — the tile / score / status links to or
  expands the rows behind it (the table, the clauses, the suppliers). No number is a dead end.
- **Why:** `data-viz.md` "tables are a feature"; trust requires verifiability; procurement users
  want the rows.
- **Escape:** a figure with genuinely no breakdown — then it's a fact; label it as one, don't fake
  a drill.

## 11. Findings are structured, not prose
- **Signal:** the output contains findings / risks / recommendations.
- **Default:** render them as scannable structured units (ranked rows, cards mapped to real
  evidence, a severity-tagged list) — one finding = one unit with its own severity / owner /
  evidence. Not paragraphs to read end-to-end.
- **Why:** scannability over reading; `anti-patterns.md` "cards must map to real tools / reports /
  evidence"; the consultant asks "what do I do?", not "read me a report."
- **Escape:** a genuine narrative deliverable (exec summary) where prose *is* the artifact — keep it
  short, put structured detail beneath it.

## 12. Each finding links insight → evidence → action
- **Signal:** a finding / risk / recommendation is shown.
- **Default:** one unit carries all three — the **insight** (what's true), its **evidence** (why we
  believe it, shown or linked), and the **next action** (what to do). Not an insight with no
  evidence, nor evidence with no "so what."
- **Why:** trust through verifiability + the user needs the next action (Persona 2: "what's my next
  step?"). This is what turns a report into a workspace.
- **Escape:** purely informational context with no action — omit the action, don't manufacture one.

## 13. Collapse spent configuration
- **Signal:** configuration that has already produced the current output (the params bar after Generate).
- **Default:** once an output exists, collapse spent config to a compact summary line (e.g.
  "Indirect • EU+UK • 18 suppliers — Adjust") and give the deliverable the reclaimed space.
  Re-expand on demand.
- **Why:** heuristic #2 (deliverable-is-the-hero) at the *post-generation* altitude — the config
  has done its job; the output is now the focus.
- **Escape:** rapid-iteration tools where the user re-runs constantly — keep config one action away
  (the "Adjust" affordance already provides this).

---

## Golden reference
`design-brain/examples/orbit-client-marketiq-research-output-flow.md` (+ `.tsx`) — the code-backed
flow that embodies the **structural** heuristics (#1–#8). The **output-craft** heuristics (#9–#13)
are a pending upgrade to it (cycle-2). Anchor on it when building any tool that configures →
generates → shows a deliverable.

## Status
in-review · Structural heuristics #1–#8 promoted & validated 2026-06-29 · Output-craft heuristics
#9–#13 drafted 2026-06-29, pending cycle-2 re-measure · Owner: design-system
