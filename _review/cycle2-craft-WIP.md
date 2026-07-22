---
type: review
status: draft
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-06-29
maturity_score: 0
tags: [orbit, design-brain, interaction-defaults, judgment-layer, craft, cycle-2, wip, review]
---

# Cycle-2 craft heuristics — working file (WIP)

The cycle-1 judgment layer fixed *structure* (flow shape / IA / interaction model): an A/B moved
UX **7/16 → 15/16**, compliance held 18/18. But the 15/16 arm **still had craft gaps** you flagged
("better, still not optimal, still breaking UX best practice"). That means the **rubric is blind to
craft** — exactly as the compliance rubric was blind to UX in cycle-1. So cycle-2 adds a **new
measurement axis (Craft)** instead of inflating the old one, encodes the heuristics, upgrades the
golden flow to exemplify them, then **re-measures** before promoting.

**Altitude map (so cycle-2 doesn't collide with existing files):**
- `tokens.md` / `defaults.md` → *material* (which token / component).
- `interaction-defaults.md` #1–#8 → *structure* (flow shape / IA / interaction model — the screen).
- `data-viz.md` → *chart/KPI craft* (a single chart or KPI tile).
- **Cycle-2 #9–#13 (this file) → *output-content craft* (how the deliverable's findings are composed).** ← the gap.

**Loop:** draft → your red-line → re-measure (Arm J vs Arm J2 on the full score) → promote to
canonical + export → delete this WIP.
**Promotes to:** `interaction-defaults.md` (#9–#13), `_benchmarks/ux-scorecard-template.md` (Part B),
`examples/orbit-client-marketiq-research-output-flow.{md,tsx}` (craft upgrade).

Progress: **#9–#13 + rubric Part B written (flagged pending).** **RE-MEASURE DONE 2026-06-29 —
VALIDATED** (craft 0→10, structure & compliance held; see result below). Remaining (awaiting user
go): record result to `_benchmarks/results/` → flip status pending→validated → upgrade golden flow
to embody #9–#13 → export to repo.

## Re-measure result — 2026-06-29 (blind A/B, adversarial reviewer, file:line cited)
Arm J (baseline, structure-only) vs Arm J2 (structure + craft #9–#13), same ContractIQ tool, the
only variable = craft. Anonymized (candidate-1 = Arm J, candidate-2 = Arm J2) + blind sanitized rubric.

| Axis | Arm J (baseline) | Arm J2 (craft) |
| ---- | ---------------- | -------------- |
| Structure /16  | 16 | 16 |
| Craft /10      | **0** (blockers: prose findings, insight-with-no-action) | **10** |
| Compliance /18 | 15 | 15 |
| Verdict        | FAIL | **PASS** |

- **Outcome:** craft **0→10**, structure & compliance **held** → hypothesis validated.
- **What it proves:** #9–#13 are implementable without regression, and Part B discriminates (blind).
- **What it does NOT prove:** independent user outcome — builder applied / reviewer scored the same
  axis. The persona-driven harness (parked) tests real-user effectiveness later.
- **Shared defect (both arms, inherited from cycle-1 arm-j):** inert `SourcePicker` Dropdown
  (`options={[]}`, no-op `onChange`, unused `query`) — violates #8; avoid in the golden-flow upgrade.
- **Artifacts:** `~/brain-stress-test/cycle2-remeasure/{candidate-1,candidate-2,rubric-blind,review}.md`
  + `_private/{arm-j2.tsx,arm-j2-plan.md}`.

---

## Section 1 — The 5 craft heuristics (DRAFT, for red-line)

> Same format as #1–#8: **Signal → Default → Why → Escape**. These operate *after* the structural
> decisions, on the content of the deliverable itself. They slot in as #9–#13 under a new
> "Information design (output craft)" divider.

### 9. Lead with the signal, not the vanity metric
- **Signal:** an output has several numbers, but only some carry the decision (savings at risk, worst supplier score, count overdue) while others are vanity (e.g. "12 suppliers analysed").
- **Default:** lead with the decision-driving metric and order tiles/sections by decision-weight — riskiest / most-actionable first. The tool does the prioritising, not the reader.
- **Why:** `data-viz.md` "the number first"; users come for the decision. A row of equal-weight tiles offloads triage back onto the user.
- **Escape:** a genuinely flat dataset where no metric dominates — group logically and say so.

### 10. Summaries are drillable — no dead-end numbers
- **Signal:** a summary number, score, or status that stands in for underlying rows/evidence.
- **Default:** every summary is a path to its evidence — the tile/score/status links to or expands the rows behind it (the table, the clauses, the suppliers). No number is a dead end.
- **Why:** `data-viz.md` "tables are a feature"; trust requires verifiability; procurement users want the rows.
- **Escape:** a figure with genuinely no breakdown — then it's a fact; label it as one, don't fake a drill.

### 11. Findings are structured, not prose
- **Signal:** the output contains findings / risks / recommendations.
- **Default:** render them as scannable structured units (ranked rows, cards mapped to real evidence, a severity-tagged list) — one finding = one unit with its own severity / owner / evidence. Not paragraphs to read end-to-end.
- **Why:** scannability over reading; `anti-patterns.md` "cards must map to real tools / reports / evidence"; the consultant asks "what do I do?", not "read me a report."
- **Escape:** a genuine narrative deliverable (exec summary) where prose *is* the artifact — keep it short, put structured detail beneath it.

### 12. Each finding links insight → evidence → action
- **Signal:** a finding / risk / recommendation is shown.
- **Default:** one unit carries all three — the **insight** (what's true), its **evidence** (why we believe it, shown or linked), and the **next action** (what to do). Not an insight with no evidence, nor evidence with no "so what."
- **Why:** trust through verifiability + the user needs the next action (Persona 2: "what's my next step?"). This is what turns a report into a workspace.
- **Escape:** purely informational context with no action — omit the action, don't manufacture one.

### 13. Collapse spent configuration
- **Signal:** configuration that has already produced the current output (the params bar after Generate).
- **Default:** once an output exists, collapse spent config to a compact summary line (e.g. "Indirect • EU+UK • 18 suppliers — Adjust") and give the deliverable the reclaimed space. Re-expand on demand.
- **Why:** heuristic #2 (deliverable-is-the-hero) at the *post-generation* altitude — the config has done its job; the output is now the focus.
- **Escape:** rapid-iteration tools where the user re-runs constantly — keep config one action away (the "Adjust" affordance already provides this).

---

## Section 2 — Rubric: Part B — Information-design craft (/10) (DRAFT proposal)

Mirrors the cycle-1 move: a **new axis with its own subtotal**, so craft can rise without
regressing structure or compliance — and so a 15/16-structure-but-craft-poor output can't hide.
`ux-scorecard-template.md` becomes two parts in one file:
- **Part A — Structure (/16)** = the existing 8 categories (unchanged).
- **Part B — Craft (/10)** = 5 new categories below, each **0 / 1 / 2**, one per heuristic #9–#13.

| # | Craft category (heuristic) | 0 | 1 | 2 |
| - | -------------------------- | - | - | - |
| 9  | Signal over vanity (#9)        | leads with a vanity count; tiles equal-weight | leads right but no ordering by decision-weight | decision-driving metric leads; tiles ordered by weight |
| 10 | Drillable summaries (#10)      | dead-end numbers | some drill, some dead-ends | every summary reaches its evidence |
| 11 | Structured findings (#11)      | prose blob | mixed prose + some structure | findings are scannable structured units |
| 12 | Insight→evidence→action (#12)  | insight only, or evidence with no "so what" | two of three present | all three in each finding unit |
| 13 | Collapse spent config (#13)    | full config persists beside output | partial / manual collapse | spent config auto-collapses to a summary line |

- **Part B PASS bar (proposed):** **≥ 7 / 10**, *and* no `0` in category **11 or 12** (a prose blob
  or an insight with no action makes the deliverable un-actionable — the craft equivalent of a blocker). ← red-line this bar.
- **Combined UX = Part A /16 + Part B /10 = /26.** Record alongside Compliance /18 as before.

---

## Section 3 — Re-measure plan (the validation gate)

Same harness as cycle-1, three arms so the new axis is provable:
- **Arm J** — the current structure-only golden flow (cycle-1 winner). Expected: high Part A, **low Part B**.
- **Arm J2** — same tool, same structure, **+ the 5 craft heuristics applied**. Expected: Part A held, **Part B up**.
- Score both on the full **/26 + Compliance /18** with an adversarial blind reviewer citing file:line.
- **Success = Part B rises materially (J2 ≫ J) with no Part A or Compliance regression.** Only then promote.
- If J2 validates, its craft moves are folded into the **golden flow** (`.tsx` + `.md` Scope section
  flips from "v1 structure" to "v2 craft"), and #9–#13 + Part B promote to canonical.
- Reuse scratch `~/brain-stress-test/`; subagents read-only on repo/vault except that scratch dir;
  no installs / build / lint / git writes; restore repo to pristine `git status` after any render.

---

## Status
draft · awaiting red-line of Section 1 (heuristics) first — Sections 2–3 derive from it.

<!-- graph-links:start — generated by tools/gen_graph_links.py; do not hand-edit -->
## Vault graph
[[_benchmarks/ux-scorecard-template|ux-scorecard-template]] · [[design-brain/anti-patterns|anti-patterns]] · [[design-brain/data-viz|data-viz]] · [[design-brain/defaults|defaults]] · [[design-brain/interaction-defaults|interaction-defaults]] · [[design-brain/tokens|tokens]]
<!-- graph-links:end -->
