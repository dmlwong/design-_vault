---
type: vault-index
status: stable
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-07-03
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
  AGENTS.md            ← canonical brain (agents auto-load this)
  CLAUDE.md            ← thin Claude Code entry point (@imports AGENTS.md)
  README.md            ← this index
  design-brain/        ← reference layer: tokens, defaults, interaction-defaults,
    components/           component contracts
    patterns/             page-level pattern contracts
    platforms/            platform profiles + visual truth
    examples/             golden examples (+ screenshots/ manifests)
    skills/  agents/  lovable/
  discovery/           ← per-initiative business/requirements packs
  _bases/              ← Obsidian database views
  _canvases/           ← visual map
  _review/             ← governance, STATE, audits, WIP
  _exports/            ← export notice + how-to
  _archive/            ← superseded docs (recoverable)
  _benchmarks/         ← benchmark tasks, rubrics, results
  tools/               ← export_brain.py, check_links.py
```

## Current State

**`_review/STATE.md` is the single "where we are" narrative** — active threads,
outstanding work, and the maturity snapshot live there (this section used to duplicate
it and drift; it no longer does). For progress detail see
`_review/Maturity Scorecard.md`; for the latest gap analysis see
`_review/2026-07-03-full-vault-audit.md`.

## Team Workflow

1. Product or design team member proposes a change using
   `_review/Change Request Template.md`.
2. Design system owners approve changes to foundations, tokens, contracts, and patterns.
3. Canonical notes are updated in this vault.
4. Generated packs are exported into product repos.
5. Corrections from agent failures are fed back into this vault.

## Open Work & Parked Items

Tracked in one place each — don't re-list them here:

- Active/outstanding work: `_review/STATE.md`.
- Deferred work: `_review/Parked Items.md` (e.g. the human-confirmed
  VoiceOver/NVDA/JAWS screen-reader pass — keep the screen-reader result as
  **NEEDS HUMAN CONFIRMATION** until a real assistive-technology session runs).
