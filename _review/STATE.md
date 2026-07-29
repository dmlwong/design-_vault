---
type: review
status: in-review
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-07-28
maturity_score: 0
tags: [orbit, design-brain, state, resume, handoff]
---

# STATE — Orbit Design Brain (single source of "where we are")

> The one place to resume from. Supersedes the older resume/snapshot docs
> (`Pick Up Here — 2026-06-25`, `State of the Design Brain — 2026-06-24`,
> `Action Plan`, `Session Change Log`), now in `_archive/state-snapshots-2026-06/`.
> Keep this current; don't spawn new dated snapshots.

## Where the vault lives
- **Canonical (edit here):** the git repository `github.com/dmlwong/design-_vault` — the
  "Orbit Design Brain" Obsidian vault. Clone it (or open a synced copy in Obsidian) to
  author; every local copy is a working copy of this repo, not a source of truth.
- **Ignore (stale copies):** any pre-git local folder (e.g. old `Codex/Design_Brain`
  copies or former OneDrive paths). If it isn't this repo, don't edit it.
- **Governs:** the `efficio-orbit` coded design-system repo. Author in the vault, then
  export with `tools/export_brain.py`. **The one rule: edit the vault, never the
  exported copy — then re-export.**

## ⏭️ Active work (both threads blocked on the owner)
1. **Cycle-2 craft heuristics** — `cycle2-craft-WIP.md`. Adds output-content craft heuristics
   **#9–#13** + rubric **Part B (/10)** as a new axis. **Re-measure done & validated 2026-06-29**
   (blind A/B: craft **0→10**, structure 16/16 and compliance 15/18 held). **Next action:** owner
   **red-lines Section 1 (the 5 heuristics)** → then record result to `_benchmarks/results/`,
   flip status pending→validated, upgrade the MarketIQ golden flow
   (`examples/orbit-client-marketiq-research-output-flow.{md,tsx}`) to embody #9–#13, promote to
   canonical (`interaction-defaults.md`, `ux-scorecard-template.md`), and export. WIP self-deletes on promotion.
2. **Connected Platform personas** — `cp-personas-WIP.md`. **2 / 4 confirmed** (Delivery Project
   Lead; Hands-On Senior Consultant). **Paused** — nothing writes to
   `platforms/connected-platform.md` until all 4 are in. **Next action:** owner **pastes Persona 3**.

## 📋 Outstanding (beyond the two active threads)
- [ ] **Work the full-vault audit** — `_review/2026-07-03-full-vault-audit.md`. Remaining
      owner decisions: sanitization of the 18 platform screenshots, real names for the
      placeholder repo/prototype references, cycle-2 red-line, personas 3–4, and
      whether to offer Obsidian Sync alongside git. Mechanical fixes (export
      drift-check, restricted-export exclusions, vault CI, link checker,
      contradiction/stale-index cleanup) applied 2026-07-03; live team-sharing +
      onboarding guide added 2026-07-06 (`_review/Team Sharing Setup.md`) — see the
      audit's "Fixes applied" section.
- [ ] **Promote `in-review` → `stable`** — ~71 files are `in-review` vs ~32 `stable`; needs owner sign-off
      (the bulk governance item).
- [ ] **Run the export** into `efficio-orbit` so Codex/Claude consume the current brain.
- [ ] **Confirm/correct personas** with real research (CP personas 3–4 pending; Orbit-client provisional).
- [ ] **Verify the two Discovery distillations** in `discovery/` against their source Word docs.
- [ ] **Parked (Phase 2):** platform shell templates; motion/data-viz tokens; drawer decision;
      screenshot sanitization; human VoiceOver/NVDA/JAWS confirmation. See `Parked Items.md`.

## 🧭 Snapshot of the brain
- **Always-on:** `AGENTS.md` (9 rules, routing table, Definition of Done) ← `CLAUDE.md` imports it.
- **Reference layer** (`design-brain/`): 12 component contracts, 11 page patterns, golden examples
  with real code, 2 platform profiles + visual-truth notes, 5 skills, lovable projections.
- **Orchestration layer** (added 2026-07-17, in-review): `orchestration.md` doctrine,
  11-agent roster in `agents/` with per-agent model tiers (incl. the 2026-07-21 intake pair and 2026-07-28 story-author), machine-readable
  `routing.json` (CI-checked), `lessons/INBOX.md` correction capture, frontmatter lint
  + weekly staleness CI. See `_review/2026-07-17-orchestration-and-optimisation-proposal.md`.
  **Dry run passed 2026-07-17** (`_review/2026-07-17-orchestration-dry-run.md`):
  scout→reviewer slice validated, 2 fixes applied + re-verified, and the reviewer found
   2 real (source-verified) blockers in the MarketIQ golden flow that the original A/B
  missed.
  **Full build-pipeline trial passed 2026-07-17** (`_review/2026-07-17-build-pipeline-trial.md`):
  ran `context-scout → component-builder → design-reviewer` against real code in the
  `efficio-orbit` repo (fixed a `filter:brightness` tokens-only violation on Button/
  IconButton, tokenised via owner-approved interim values). First loop, reviewer PASS.
  Storybook was wired into the component repo the same day (branch
  `claude/storybook-setup`) and the `extract-contract` upstream stream was proven blind.
  **Promoted `in-review → stable`:** `orchestration.md`, `context-scout`,
  `component-builder`, `contract-extractor` (design-reviewer already stable).
  **Still `in-review`:** `screen-builder` (exercised 2026-07-17 on the Commentary
  prototype — see `Parked Items.md`), `porter`, `benchmark-judge`, `vault-librarian`.
  **2026-07-28 addendum (see git log for detail):** Storybook merged to the component
  repo's `main` with its first CI + published GitHub Pages instance; vault health now
  reports build status + story coverage (1/52); intake pipeline piloted 2026-07-21;
  agents/skills hardened from the three-audit review (render-verify, write-stories
  task, reviewer severity classes).
- **Judgment layer:** `interaction-defaults.md` #1–#8 (structure) validated; #9–#13 (craft) in cycle-2 above.
- **Maturity:** ~82–88/100.

## 📚 Where the durable detail lives (kept in `_review/`)
- `Governance.md`, `Maintenance Workflow.md` — how the brain is governed and kept in sync.
- `Change Request Template.md`, `Platform Visual Truth Review Checklist.md` — reusable process.
- `Maturity Scorecard.md` — progress tracker. `Parked Items.md` — deferred work. `Source Inventory.md` — code provenance.
- Archived (recoverable, not deleted): point-in-time snapshots → `_archive/state-snapshots-2026-06/`;
  old-era HTML usage guides + onboarding → `_archive/usage-guides-2026-06/`.

<!-- graph-links:start — generated by tools/gen_graph_links.py; do not hand-edit -->
## Vault graph
[[AGENTS|AGENTS]] · [[CLAUDE|CLAUDE]] · [[_benchmarks/ux-scorecard-template|ux-scorecard-template]] · [[_review/2026-07-03-full-vault-audit|2026-07-03-full-vault-audit]] · [[_review/2026-07-17-build-pipeline-trial|2026-07-17-build-pipeline-trial]] · [[_review/2026-07-17-orchestration-and-optimisation-proposal|2026-07-17-orchestration-and-optimisation-proposal]] · [[_review/2026-07-17-orchestration-dry-run|2026-07-17-orchestration-dry-run]] · [[_review/Change Request Template|Change Request Template]] · [[_review/Governance|Governance]] · [[_review/Maintenance Workflow|Maintenance Workflow]] · [[_review/Maturity Scorecard|Maturity Scorecard]] · [[_review/Parked Items|Parked Items]] · [[_review/Platform Visual Truth Review Checklist|Platform Visual Truth Review Checklist]] · [[_review/Source Inventory|Source Inventory]] · [[_review/Team Sharing Setup|Team Sharing Setup]] · [[_review/cp-personas-WIP|cp-personas-WIP]] · [[_review/cycle2-craft-WIP|cycle2-craft-WIP]] · [[design-brain/interaction-defaults|interaction-defaults]] · [[design-brain/lessons/INBOX|lessons INBOX]] · [[design-brain/orchestration|orchestration]] · [[design-brain/platforms/connected-platform|connected-platform]]
<!-- graph-links:end -->
