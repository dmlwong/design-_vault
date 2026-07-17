---
type: review
status: draft
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-07-17
maturity_score: 0
tags: [orbit, design-brain, orchestration, dry-run, trial]
---

# Orchestration Dry Run — 2026-07-17

First execution of the orchestration layer (proposal implemented in commit `d57248a`)
against a real task, run inside the vault (the full build-pipeline trial awaits the
product repo). **Task under trial:** `design-review` of
`design-brain/examples/orbit-client-marketiq-research-output-flow.tsx`.

Pipeline slice exercised: `context-scout` (haiku) → `design-reviewer` (opus-class,
fresh context). Not exercised: builder step, 2-loop escalation, handover check.

## Pre-registered expectations (written BEFORE any agent ran)

### Scout (context-scout, haiku)
- [ ] E1. Picks task key `design-review` from `routing.json`.
- [ ] E2. Resolves platform to `orbit-client-connected-platform` (stated in the
      example's frontmatter/companion `.md` — should not need to ask).
- [ ] E3. LOAD list matches the manifest's `design-review.load` (AGENTS.md, involved
      component/pattern contracts, tokens, accessibility, anti-patterns, motion, ux-copy).
- [ ] E4. Resolves `<involved>` placeholders by consulting the example's companion
      `.md`, and flags contract-less components (`PageHeader`/`HeaderPresets`,
      `Spinner`) under MISSING.
- [ ] E5. Output uses the exact packet format from its definition
      (TASK KEY / PLATFORM / AGENT / SKILL / LOAD / MISSING / THEN).
- [ ] E6. Offers no design opinions; assigns `design-reviewer (model: opus)`.

### Reviewer (design-reviewer, opus-class, fresh context)
- [ ] E7. Receives ONLY: its definition + the scout's packet + the artifact path.
      No orchestrator commentary, no scout conversation.
- [ ] E8. Output uses the exact `VERDICT / BLOCKERS / MAJOR / MINOR / CONTRACT GAPS`
      format; findings cite `file:line`.
- [ ] E9. Does NOT raise the missing `<OrbitInspector />` as a blocker — the example's
      gap report documents it's a self-contained reference, not a prototype root
      (doctrine-nuance trap).
- [ ] E10. CONTRACT GAPS names at least the known contract-less components.
- [ ] E11. Verdict is defensible: findings that are already documented in the example's
      gap report may appear, but genuinely new false positives count against the run.

## Run log

### Step 1 — context-scout (haiku) · ran 2026-07-17, ~42s, 9 tool uses
Emitted a format-perfect packet: task key `design-review`, platform
`orbit-client-connected-platform`, agent `design-reviewer (model: opus)`, skill none,
THEN none. Resolved the involved components by actually reading the example's
companion note — listed all six contracted components (button, card-panel,
status-indicator, badge-status, data-table, select-combobox). Added four files beyond
the manifest's load list (interaction-defaults, both platform files, visual truth) —
all apt for a screen-level review. MISSING flagged the absent tool-run-flow *pattern
contract* (true, valuable) but **not** the contract-less *components* the example's gap
report names (`PageHeader`/`HeaderPresets`, `Spinner`). No design opinions offered.

Scorecard: E1 ✓ · E2 ✓ · E3 ✓ (and exceeded — see D1) · E4 partial (components
resolved ✓, contract-less not flagged ✗ — see D2) · E5 ✓ · E6 ✓

## Deviations & classification

- **D1 · Manifest defect** — `routing.json` `design-review.load` omits
  `interaction-defaults.md` and the platform profile + visual truth, which a
  screen-level review plainly needs (the reviewer checklist cites composition and
  platform fit). The haiku scout compensated on its own judgment — good instinct, but
  routing correctness shouldn't depend on the clerk's initiative. Fix: add the three
  paths to the manifest's `design-review.load`.
- **D2 · Agent-definition defect** — `context-scout.md` says MISSING holds
  "contracts/files the manifest expects but don't exist"; the scout read that as
  manifest-level only and did not flag components used by the artifact that have no
  contract (`PageHeader`/`HeaderPresets`, `Spinner` — named in the example's own gap
  report). Fix: sharpen the MISSING rule to "any component the artifact uses that has
  no contract in `components/`".

*(reviewer deviations pending)*

## Fixes applied

*(with re-run confirmation where applicable)*

## Recommendation

*(promote orchestration files to stable — yes / not yet, and why)*
