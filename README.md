---
type: vault-index
status: stable
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-06-16
maturity_score: 88
tags: [orbit, design-brain, obsidian]
---

# Orbit Design Brain

This vault is the canonical design operating system for Orbit by Efficio. It gives
design, product, and AI coding tools one shared source of truth for how Orbit UI should
look, behave, and be reviewed.

The vault has one shared foundation with two platform profiles:

- **Connected Platform** for internal Efficio users.
- **Orbit / Client Connected Platform** for external client users.

Author here first. Export into product repos second. Never hand-edit generated product
repo copies.

## How It Works

1. The shared Obsidian vault holds the canonical brain.
2. `AGENTS.md` gives Codex and other agents the always-on rules.
3. `CLAUDE.md` imports `AGENTS.md` for Claude Code.
4. `design-brain/` holds reference files, component contracts, pattern contracts,
   examples, skills, and Lovable projections.
5. `tools/export_brain.py` generates agent-ready packs into product repos.

## Vault Structure

```text
Orbit Design Brain/
  AGENTS.md
  CLAUDE.md
  README.md
  design-brain/
    platforms/
  _bases/
  _canvases/
  _review/
  _exports/
  _archive/
  _benchmarks/
  tools/
```

## Current Maturity

Estimated current score: **88/100** after the first real-source integration pass,
five passing agent benchmarks, a passing platform-separation benchmark, a passing
benchmark accessibility artifact pass, a passing browser visual accessibility pass, a
prepared screen-reader artifact, and a benchmark screenshot pack for the benchmark
routes. User-provided Connected Platform and Orbit / Client Connected Platform
screenshots are now filed in platform visual truth manifests with visual truth
extraction notes, and are pending sanitization and design-system approval. Platform
golden examples are now connected to page pattern contracts so agents can choose the
right screen shape before composing components.

The structure, governance, export path, token source paths, first top-10 component
contracts, platform profiles, ClauseIQ guided-workflow example, a passing ClauseIQ
results-table benchmark, a passing procurement settings form benchmark, a passing
MarketIQ analytics dashboard benchmark, a passing Lovable-to-Orbit port benchmark, and a
passing Design Brain review benchmark, a passing platform-separation benchmark, a
generated accessibility artifact pass for benchmark routes, and a browser visual
accessibility pass with screenshots, focus-ring evidence, and rendered contrast sampling
are now in place. A dated benchmark screenshot pack now documents the benchmark routes
across Efficio/Orbit themes and default/compact density, but those screenshots must
**not** be treated as canonical platform visual precedent because they do not yet match
the current live platform. Platform-specific visual truth notes now extract shell,
density, card, list/table, modal, dashboard, and copy guidance from the user-provided
screenshots, and the platform-separation benchmark confirms agents can apply CP and
Orbit rules separately in generated benchmark screens. The score reaches the top end of
**85-90** after the remaining source and validation gaps are closed:

- Drawer decision or reusable drawer source.
- Design-system approval of the user-provided platform screenshot manifests.
- MarketIQ / RFP Analytics examples.
- Dedicated data-viz tokens.
- Human review of the new screenshot-backed page pattern contracts.
- Human-confirmed VoiceOver/NVDA/JAWS screen-reader evidence, parked in
  `_review/Parked Items.md`.

## Team Workflow

1. Product or design team member proposes a change using
   `_review/Change Request Template.md`.
2. Design system owners approve changes to foundations, tokens, contracts, and patterns.
3. Canonical notes are updated in this vault.
4. Generated packs are exported into product repos.
5. Corrections from agent failures are fed back into this vault.

## First Real-Source Tasks

1. Decide whether drawer becomes a reusable Orbit component or remains pattern-specific.
2. Review, sanitize, and approve the new platform screenshot manifests.
3. Link production MarketIQ / RFP Analytics KPI and dashboard source.
4. Source and document the next page pattern contract.
5. Identify whether dedicated data-viz tokens exist or should be specified.

## Parked For Now

- Human-confirmed VoiceOver/NVDA/JAWS screen-reader checks for benchmark routes are
  parked in `_review/Parked Items.md`. Keep the current screen-reader result as
  **NEEDS HUMAN CONFIRMATION** until a real assistive-technology session is completed.
