---
type: benchmark
status: in-review
owner: design-system
surfaces: [shared]
source: code
last_reviewed: 2026-06-16
maturity_score: 88
tags: [orbit, design-brain, benchmark]
---

# Agent Benchmark Tasks

Run these tasks after exporting the brain into a product repo. Score each task with the
rubric below. The brain reaches 85-90 only when agents pass with minimal correction.

## Run History

| Date | Task | Repo | Result | Notes |
| ---- | ---- | ---- | ------ | ----- |
| 2026-06-14 | Task 1 — Data-Heavy Results Table | `the efficio-orbit repo` | 91/100 — PASS | See `results/2026-06-14-clauseiq-results-table.md`. |
| 2026-06-15 | Task 2 — Form With Validation | `the efficio-orbit repo` | 17/18 — PASS | See `results/2026-06-15-procurement-settings-form.md`. |
| 2026-06-15 | Task 3 — Dashboard KPI / Chart View | `the efficio-orbit repo` | 18/18 — PASS | See `results/2026-06-15-marketiq-analytics-dashboard.md`. |
| 2026-06-15 | Task 4 — Port Lovable Prototype Into Orbit | `the efficio-orbit repo` | 18/18 — PASS | See `results/2026-06-15-lovable-port.md`. |
| 2026-06-15 | Task 5 — Review Finished Multi-Component Screen | `the efficio-orbit repo` | 18/18 — PASS after fixes | See `results/2026-06-15-lovable-port-review.md`. |
| 2026-06-15 | Accessibility artifact pass — benchmark routes | `the efficio-orbit repo` | PASS | See `results/2026-06-15-benchmark-accessibility-artifact.md`. |
| 2026-06-15 | Browser visual accessibility pass — benchmark routes | `the efficio-orbit repo` | PASS after fixes | See `results/2026-06-15-browser-visual-accessibility.md`. |
| 2026-06-15 | Screen-reader accessibility pass — benchmark routes | `the efficio-orbit repo` | NEEDS HUMAN CONFIRMATION after fixes; parked | See `results/2026-06-15-screen-reader-accessibility.md` and `parked-items.md`. |
| 2026-06-15 | Benchmark screenshot reference pack — benchmark routes | `the efficio-orbit repo` | BENCHMARK EVIDENCE ONLY | See `results/2026-06-15-golden-visual-reference.md`; not platform visual precedent. |
| 2026-06-16 | Platform Separation — Connected Platform vs Orbit / Client Connected Platform | `the efficio-orbit repo` | 18/18 + 18/18 — PASS | See `results/2026-06-16-platform-separation-benchmark.md`; confirms agents can apply separate platform profiles, visual truth notes, golden examples, and patterns. |
| 2026-06-16 | Platform Separation accessibility artifact | `the efficio-orbit repo` | PASS | See `results/2026-06-16-platform-separation-accessibility-artifact.md`; screen-reader quality still needs human confirmation. |

## Scoring Rubric

Score each category 0-2:

| Category | 0 | 1 | 2 |
| -------- | - | - | - |
| Tokens only | hardcoded values | mixed | all semantic/component tokens |
| Theme support | one theme only | partial | `efficio` and `orbit` |
| Full states | happy path only | some states | all required states |
| Accessibility | broken | partial | keyboard, focus, AA, non-colour signals |
| Density | spacious/generic | partial | comfortable and compact |
| Contract match | ignores contract | partial | contract-complete |
| Pattern match | generic layout | partial | pattern-complete |
| Copy and motion | vague/decorative | partial | Orbit voice and functional motion |
| Orbit feel | generic SaaS | mixed | dense, restrained, procurement-first |

Passing target: 16/18 or higher with no blocker.

## Required Accessibility Artifact

Every benchmark route review must include a generated accessibility artifact before the
benchmark can be marked PASS. Run `npm run bench:a11y` from the repo root and link the
markdown output under `design-brain/_benchmarks/results/`.

The artifact must report PASS/FAIL per benchmark route, the automated checks run,
tooling availability for Playwright/axe/jest-axe or the equivalent existing stack, any
violations found, and remaining manual checks. If axe or browser automation is not
already available in the repo, use the existing stack rather than adding a dependency
only for this benchmark gate.

Every benchmark route review must also include a browser visual accessibility pass before
PASS: screenshots for supported theme/density states, real-browser focus-ring evidence
from Tab traversal through key controls, and rendered CSS contrast sampling for key
text, status, and control states.

Every benchmark route review must also include a separate screen-reader artifact before
PASS. Browser DOM, accessibility-tree, or CDP checks can support this artifact, but they
do not count as a completed screen-reader pass. Mark the result **NEEDS HUMAN
CONFIRMATION** unless VoiceOver, NVDA, or JAWS was actually used to confirm spoken
output, timing, dialog context, tab context, table navigation, and live-region quality.

## Task 1 — Data-Heavy Results Table

Prompt: "Using the Orbit Design Brain, build a data-heavy results table with filters,
sorting, row selection, loading, empty, and error states."

Expected references: `AGENTS.md`, `tokens.md`, `components/data-table.md`,
`examples/data-table-dense.md`.

## Task 2 — Form With Validation

Prompt: "Build a procurement settings form with text input, select/combobox, help text,
validation, disabled permission state, loading, and error recovery."

Expected references: `components/input.md`, `components/select-combobox.md`,
`examples/form-field-validation.md`, `ux-copy.md`, `accessibility.md`.

## Task 3 — Dashboard KPI / Chart View

Prompt: "Build a MarketIQ analytics dashboard with KPI blocks, one trend chart, one
category comparison, underlying table access, loading, insufficient-data, and stale states."

Expected references: `data-viz.md`, `patterns/analytics-dashboard.md`,
`examples/analytics-kpi-chart.md`.

## Task 4 — Port Lovable Prototype Into Orbit

Prompt: "Port this external/Lovable prototype into Orbit components and tokens. Report
component mapping, token translation, missing states, accessibility fixes, and deviations."

Expected references: `skills/port-to-orbit/SKILL.md`, `tokens.md`,
`components/README.md`, `anti-patterns.md`.

Latest source prototype: `Test`.

## Task 5 — Review Finished Multi-Component Screen

Prompt: "Review this finished screen against the Orbit Design Brain. Give PASS/FAIL,
blockers, major issues, minor issues, and contract gaps."

Expected references: `agents/design-reviewer.md`, `AGENTS.md`, relevant component and
pattern contracts.

## Task 6 — Platform Separation

Prompt: "Build or refactor one Connected Platform internal screen and one Orbit / Client
Connected Platform client-facing screen. Before implementing, state which platform
profile, visual truth note, golden examples, and pattern contracts were loaded. After
implementation, score both screens and report whether platform rules were kept separate."

Expected references:
- Connected Platform: `platforms/connected-platform.md`,
  `platforms/connected-platform-visual-truth.md`,
  `examples/connected-platform-initiative-list-table.md`,
  `patterns/list-detail.md`.
- Orbit / Client Connected Platform:
  `platforms/orbit-client-connected-platform.md`,
  `platforms/orbit-client-connected-platform-visual-truth.md`,
  `examples/orbit-client-marketiq-guided-workflow.md`,
  `patterns/guided-conversational-workflow.md`.

<!-- graph-links:start — generated by tools/gen_graph_links.py; do not hand-edit -->
## Vault graph
[[AGENTS|AGENTS]] · [[_benchmarks/parked-items|parked-items]] · [[_benchmarks/results/2026-06-14-clauseiq-results-table|2026-06-14-clauseiq-results-table]] · [[_benchmarks/results/2026-06-15-benchmark-accessibility-artifact|2026-06-15-benchmark-accessibility-artifact]] · [[_benchmarks/results/2026-06-15-browser-visual-accessibility|2026-06-15-browser-visual-accessibility]] · [[_benchmarks/results/2026-06-15-golden-visual-reference|2026-06-15-golden-visual-reference]] · [[_benchmarks/results/2026-06-15-lovable-port-review|2026-06-15-lovable-port-review]] · [[_benchmarks/results/2026-06-15-lovable-port|2026-06-15-lovable-port]] · [[_benchmarks/results/2026-06-15-marketiq-analytics-dashboard|2026-06-15-marketiq-analytics-dashboard]] · [[_benchmarks/results/2026-06-15-procurement-settings-form|2026-06-15-procurement-settings-form]] · [[_benchmarks/results/2026-06-15-screen-reader-accessibility|2026-06-15-screen-reader-accessibility]] · [[_benchmarks/results/2026-06-16-platform-separation-accessibility-artifact|2026-06-16-platform-separation-accessibility-artifact]] · [[_benchmarks/results/2026-06-16-platform-separation-benchmark|2026-06-16-platform-separation-benchmark]] · [[design-brain/accessibility|accessibility]] · [[design-brain/agents/design-reviewer|design-reviewer]] · [[design-brain/anti-patterns|anti-patterns]] · [[design-brain/components/README|components README]] · [[design-brain/components/data-table|data-table]] · [[design-brain/components/input|input]] · [[design-brain/components/select-combobox|select-combobox]] · [[design-brain/data-viz|data-viz]] · [[design-brain/examples/analytics-kpi-chart|analytics-kpi-chart]] · [[design-brain/examples/connected-platform-initiative-list-table|connected-platform-initiative-list-table]] · [[design-brain/examples/data-table-dense|data-table-dense]] · [[design-brain/examples/form-field-validation|form-field-validation]] · [[design-brain/examples/orbit-client-marketiq-guided-workflow|orbit-client-marketiq-guided-workflow]] · [[design-brain/patterns/analytics-dashboard|analytics-dashboard]] · [[design-brain/patterns/guided-conversational-workflow|guided-conversational-workflow]] · [[design-brain/patterns/list-detail|list-detail]] · [[design-brain/platforms/connected-platform-visual-truth|connected-platform-visual-truth]] · [[design-brain/platforms/connected-platform|connected-platform]] · [[design-brain/platforms/orbit-client-connected-platform-visual-truth|orbit-client-connected-platform-visual-truth]] · [[design-brain/platforms/orbit-client-connected-platform|orbit-client-connected-platform]] · [[design-brain/skills/port-to-orbit/SKILL|port-to-orbit SKILL]] · [[design-brain/tokens|tokens]] · [[design-brain/ux-copy|ux-copy]]
<!-- graph-links:end -->
