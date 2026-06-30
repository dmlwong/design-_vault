---
type: benchmark
status: in-review
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-06-29
maturity_score: 72
tags: [orbit, design-brain, benchmark, ux-rubric, judgment-layer]
---

# UX Judgment Scorecard

> The **second** rubric, run *alongside* `_benchmarks/scorecard-template.md` (the /18
> **compliance** rubric). It exists because compliance and UX are different axes: the Contract
> Analysis prototype scored ~18/18 on compliance while being UX-poor. This rubric measures the
> thing the other one is blind to — **did we design the right thing for the user and task.**
>
> It has **two parts**: **Part A — Structure (/16)** (the screen: flow shape, IA, interaction
> model) and **Part B — Craft (/10)** (the deliverable's content: what it leads with, how findings
> read, what the user can do next). Combined **UX = /26**. Part B exists because a Part-A-clean
> output can still be craft-poor — the cycle-1 arm scored 15/16 on structure yet had real craft
> gaps; Part A was blind to them, exactly as compliance was blind to UX.

## What it measures (and why the axes are separate)
- The **/18 compliance rubric** = the *material layer* (tokens, components, states, a11y,
  theme). Mostly closed/checkable. The brain already governs this well.
- **Part A — Structure (/16)** = the *judgment layer, structure* (flow shape, IA, interaction
  model, restraint, ceremony). Categories 1–8 map 1:1 to heuristics **#1–#8** in `interaction-defaults.md`.
- **Part B — Craft (/10)** = the *judgment layer, output craft* (signal-first, drillable
  summaries, structured findings, insight→evidence→action, collapsed config). Categories 9–13
  map 1:1 to heuristics **#9–#13**.
- Run **all three axes** on every arm. A new layer must *raise its own axis without regressing the
  others* — you can only see that with separate scores.

## How to score
- Score each category **0 / 1 / 2**. Part A categories 1–8 → **/16**; Part B categories 9–13 →
  **/10**; combined **/26**.
- **Anchor on the references**, not taste:
  - Good: `examples/work-card-research-primer.tsx`, `examples/orbit-client-marketiq-research-output-flow.tsx`.
  - Bad: `apps/prototypes/components/feature/contract-analysis/ContractAnalysisPrototype.tsx`.
- **Cite file:line** for every score (what in the code earned it).
- **Blockers — a `0` in any of these fails the relevant axis regardless of total:**
  - Part A — **category 1 or 2** (wrong flow shape, or a buried deliverable: the screen is wrong even if clean).
  - Part B — **category 11 or 12** (a prose blob, or an insight with no action: the deliverable is un-actionable even if it scores elsewhere).

| Score | Meaning |
| ----- | ------- |
| **2** | Matches the heuristic's default (or takes its escape *with a stated reason*). |
| **1** | Partially; or follows it by luck without the supporting structure. |
| **0** | Violates it — defaults to the generic/training-prior choice. |

---

## Part A — Structure (/16) — categories 1–8

### 1. Flow-shape fit  *(heuristic #1 — form, not wizard)*
Is the structure right for the task and user (single surface / form vs multi-step wizard)?
- **2** — one surface for a ≤~8-input expert task; a stepper only where steps genuinely depend on each other.
- **1** — a stepper that could have been a form, but steps are at least coherent.
- **0** — a multi-step wizard imposed on a short, non-sequential expert task.

### 2. Deliverable foregrounded  *(heuristic #2 — content-first IA)*
Does the output own the screen, with configuration secondary?
- **2** — the deliverable (or its live preview / empty-state CTA) is the primary surface; config is a bar/rail/disclosure.
- **1** — output and config share the screen roughly equally.
- **0** — an all-configuration screen; the result is hidden behind a button or reduced to a list of titles.

### 3. Restraint & visual hierarchy  *(heuristic #3)*
Status and emphasis via the right primitives, scannable, not consumer-celebration.
- **2** — status via `StatusIndicator`/`Badge`/single error rail; calm, dense, one focal point per surface.
- **1** — mostly restrained but some decorative colour or competing emphasis.
- **0** — whole containers tinted by status as decoration; noisy / celebratory.

### 4. Selection at the right altitude  *(heuristic #4)*
Is each selection handled inline / focused-modal / needless-step appropriately?
- **2** — small selections inline; only a genuinely large one gets a focused modal.
- **1** — a defensible but heavier-than-needed treatment.
- **0** — a whole wizard step that is just a picker.

### 5. Steps-to-goal & ceremony  *(heuristic #5)*
Minimal path to the goal; one clear primary; no filler.
- **2** — common path is ~one action; no intro card / review step / generic "Next, you can…"; exactly one Primary per surface.
- **1** — some avoidable ceremony, or a second competing primary.
- **0** — intro + review + next-steps scaffolding around a simple task.

### 6. Platform & mental-model fit  *(heuristic #6 — Jakob's law)*
Correct platform; reuses existing platform conventions.
- **2** — right platform/shell; reuses established interaction patterns; context persisted.
- **1** — right platform but invents a local interaction where a convention existed.
- **0** — wrong platform/shell, or a novel interaction with no reason.

### 7. Progressive disclosure & smart defaults  *(heuristic #7)*
Essentials first, sensible pre-fills, depth on demand.
- **2** — first view is the essential decision; advanced options pre-filled and disclosed.
- **1** — some disclosure but weak defaults, or essentials buried among options.
- **0** — every parameter forced up front with no defaults.

### 8. Substance over scaffolding & honest states  *(heuristic #8 + principle "show state honestly")*
Real content/evidence; states designed honestly; no shipped demo affordances.
- **2** — shows real analytical substance; loading/empty/error designed inline; no demo togglers in shipped UI.
- **1** — thin substance or one faked/again-behind-modal state.
- **0** — config-only with no substance, faked success, or demo state-togglers baked into the UI.

---

## Part B — Craft (/10) — categories 9–13

> Categories 9–13 map 1:1 to heuristics #9–#13. They score the *deliverable's content*, not the
> screen. **Anchor note:** there is no code golden anchor for craft *yet* (the golden-flow craft
> upgrade is the cycle-2 deliverable). Until it lands, score Part B against the heuristic defaults
> in `interaction-defaults.md` #9–#13; Arm J2 becomes the first craft anchor if it validates.

### 9. Signal over vanity  *(heuristic #9 — lead with the signal)*
Does the output lead with the decision-driving metric, ordered by weight?
- **2** — the decision-driving metric (risk / savings / worst score) leads; tiles / sections ordered by decision-weight.
- **1** — leads with something relevant, but tiles are equal-weight / unordered.
- **0** — opens with a vanity count ("N analysed"); the user must triage for themselves.

### 10. Drillable summaries  *(heuristic #10)*
Can every summary number reach its evidence?
- **2** — every summary tile / score / status links to or expands the rows behind it.
- **1** — some drill down; some are dead ends.
- **0** — dead-end numbers; no path from summary to evidence.

### 11. Structured findings  *(heuristic #11 — BLOCKER if 0)*
Are findings scannable structured units, not prose?
- **2** — findings are discrete structured units (ranked rows / evidence-mapped cards / severity-tagged list), one finding per unit.
- **1** — mixed: some structure, some prose to read end-to-end.
- **0** — a prose blob the reader must mine to extract the findings.

### 12. Insight → evidence → action  *(heuristic #12 — BLOCKER if 0)*
Does each finding carry all three?
- **2** — each finding states the insight, shows / links its evidence, and offers the next action.
- **1** — two of the three (e.g. insight + evidence but no action).
- **0** — insight only, or evidence with no "so what" — nothing to act on.

### 13. Collapsed spent config  *(heuristic #13)*
Once output exists, does spent configuration get out of the way?
- **2** — spent config auto-collapses to a compact summary line; the deliverable gets the space; re-expand on demand.
- **1** — partial or manual collapse; config still competes with the output.
- **0** — full configuration persists beside the output after generation.

---

## Verdict
- **Part A — Structure:** ___ / 16 · **Part B — Craft:** ___ / 10 · **Combined UX:** ___ / 26
- **Blockers:** any `0` in category **1, 2, 11, or 12** → **FAIL** regardless of total
  (1 / 2 = wrong screen; 11 / 12 = un-actionable deliverable).
- **PASS bars:** Part A **≥ 12/16**, Part B **≥ 7/10**, and **no blocker**.
- Record the companion **compliance score** (/18) on the same output, so regression across any axis is visible.

## Experiment scoring block (copy per arm)
```
Arm: C (current brain) | J (structure only) | J2 (structure + craft)
Part A /16:    1:_ 2:_ 3:_ 4:_ 5:_ 6:_ 7:_ 8:_      = __/16
Part B /10:    9:_ 10:_ 11:_ 12:_ 13:_              = __/10
Combined UX:                                          __/26
Compliance/18: __/18 (from scorecard-template.md)
Blockers:      (list any 0 in cat 1, 2, 11, or 12)
Verdict:       PASS / FAIL
Evidence:      (file:line citations per score)
Human gut-check: "Which would you ship, and why?"
```

## Provenance
Created 2026-06-27; **Part A — Structure (/16)** validated in the 2026-06-29 judgment-layer A/B (it
correctly passed the single-surface arm at 15/16 and failed the 18/18-compliant wizard arm at 7/16
— the blind spot the compliance rubric alone misses). **Part B — Craft (/10)** added 2026-06-29
(cycle-2); it is **pending its first run** (the Arm J vs Arm J2 re-measure) before it carries the
same validated status. See `_review/cycle2-craft-WIP.md`.

## Status
in-review · Part A validated 2026-06-29 · Part B added 2026-06-29, pending cycle-2 re-measure ·
Owner: design-system
