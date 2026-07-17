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

### Step 2 — design-reviewer (opus-class, fresh context) · ~4m13s, 18 tool uses
Prompt contained only: its definition + the scout's packet + the artifact path (E7 ✓).
Returned the exact output format with `file:line` citations (E8 ✓). Verdict: **FAIL,
2 blockers** — and both were **verified genuine against the source** by the
orchestrator before acceptance:
1. *Nested cards* — the ready-state output-header `Card` wraps `MetricTiles`, which
   renders a `Card` per tile (violates `card-panel.md` Don't / AGENTS.md §4).
2. *Row identity* — `InitiativePicker` renders an identical "Select" button per row
   with no initiative identity in the accessible name (violates `accessibility.md`).
Plus 4 verified majors (result never announced to AT; skeleton doesn't mirror final
layout; two Primary buttons in the empty view; `density` not propagated to tables) and
a strong CONTRACT GAPS section: named the contract-less components (E10 ✓), spotted
`card-panel.md` drift vs the deprecated `type` prop the example works around, noted the
craft heuristics #9–#13 are unmet-but-out-of-scope per the example's own v1 scoping.
**Passed the doctrine-nuance trap** (E9 ✓): the missing `OrbitInspector` was cited as a
disclosed non-blocker, not a violation. No new false positives found on verification
(E11 ✓).

### Step 3 — scout re-run after D2 fix (haiku) · ~48s
MISSING now lists every contract-less component the artifact uses (PageHeader, Spinner,
Headings, Text, Overlay-to-verify) — E4 ✓ on re-run. The D1 manifest fix is also live:
the packet now carries interaction-defaults + both platform files from `routing.json`
itself rather than from the scout's initiative. One cosmetic deviation: output slightly
more verbose than the format spec (inline NOTE lines) — acceptable, not re-tuned.

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

- **Reviewer deviations: none material.** One judgment call worth recording: it flagged
  the disclosed dead `InitiativePicker` control as a MAJOR despite the gap-report
  disclosure, citing interaction-defaults #8 ("a defect, not a stub"). Defensible —
  disclosure documents a defect, it doesn't waive it. Definition left unchanged.
- **Genuine findings (verified in source):** 2 blockers + 4 majors recorded in the
  example's gap report
  (`examples/orbit-client-marketiq-research-output-flow.md`). Notable: the dry run
  found real defects in a benchmark-validated golden example that the original
  15/16 A/B scoring missed — the reviewer-gets-the-strongest-model doctrine earning
  its keep on day one.
- **Proposal (governed file — not applied):** `components/card-panel.md` is out of
  sync with source behaviour the example relies on (`type` deprecation, `hasShadow`).
  Needs a contract re-extraction pass (owner approval → `contract-extractor`).

## Fixes applied

- **D1** — `design-brain/routing.json`: `design-review.load` gained
  `interaction-defaults.md`, `platforms/<platform>.md`,
  `platforms/<platform>-visual-truth.md`. Confirmed live in the scout re-run.
- **D2** — `design-brain/agents/context-scout.md`: MISSING rule sharpened to
  explicitly include artifact-used components with no contract. Confirmed by re-run
  (one re-run, per the pipeline's own loop discipline).
- **Genuine findings** — recorded in the golden example's gap report; the `.tsx` was
  deliberately **not** rewritten (it is cited by recorded benchmark results). Fixing
  it is the natural first `build-component`/`build-screen` task for the product-repo
  trial.

## Recommendation

**Promote now:** `orchestration.md`, `routing.json`, `context-scout.md` — exercised,
tuned, re-verified. (`design-reviewer.md` is already stable and performed at spec.)

**Keep `in-review`:** the four builder agents (`component-builder`, `screen-builder`,
`porter`, `contract-extractor`) and `benchmark-judge`, `vault-librarian` — none were
exercised by this dry run. Promote after the product-repo trial runs a real build
through the full pipeline (candidate task: fix this dry run's two verified blockers in
the MarketIQ golden flow).

**Owner follow-ups surfaced:** card-panel contract re-extraction (drift vs source);
icon-size token gap (raw pixel `FaIcon` sizes have no token to use); the golden-flow
defects themselves.

<!-- graph-links:start — generated by tools/gen_graph_links.py; do not hand-edit -->
## Vault graph
[[design-brain/accessibility|accessibility]] · [[design-brain/agents/context-scout|context-scout]] · [[design-brain/agents/design-reviewer|design-reviewer]] · [[design-brain/components/card-panel|card-panel]] · [[design-brain/examples/orbit-client-marketiq-research-output-flow|orbit-client-marketiq-research-output-flow]] · [[design-brain/interaction-defaults|interaction-defaults]] · [[design-brain/orchestration|orchestration]]
<!-- graph-links:end -->
