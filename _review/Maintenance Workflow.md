---
type: governance
status: stable
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-06-18
maturity_score: 75
tags: [orbit, design-brain, maintenance, workflow, governance]
---

# Maintenance Workflow — Orbit Design Brain

> **Automation status (2026-07-03):** this file describes the target operating model.
> What exists today: the exporter with a real CI drift-check flag
> (`tools/export_brain.py --check`, exits 1 on drift) and vault-integrity CI
> (`.github/workflows/vault-integrity.yml`: link check + required-files check).
> **Not yet wired:** the scheduled auto re-export into `efficio-orbit` and a drift-check
> job running against the product repo. Until those exist, re-export manually after
> vault changes. See `_review/2026-07-03-full-vault-audit.md`, finding A2.

How the Design Brain is kept current and in sync over time. The model has **two
audiences using two tools**, bridged by automation:

- **Authors** (design / product / PO) edit the **vault** in Obsidian (via Obsidian Sync).
  No git, no clone. **The vault is the single source of truth.**
- **Consumers** (Codex, Claude Code, engineers) read the brain inside the **product repo**
  (`the efficio-orbit repo`) via git — a **generated copy**, never hand-edited.

```
 AUTHORS (design/PM/PO)        ROBOT (automation)          CONSUMERS
 edit in Obsidian  ──Sync──>   vault  ──auto-export──>    efficio-orbit  ──>  Codex / Claude
        ▲                              (+ CI drift-check)                          │
        └──────────── correction when the AI gets it wrong ◄───────────────────────┘
```

## The one rule

**Edit the vault. Never edit the copy.** If that rule holds, drift is structurally
impossible. The repo copy is disposable — always reproducible from the vault by the
exporter (`tools/export_brain.py`).

## 1. Everyday change loop

1. An author edits the **vault** in Obsidian — a token note, component/pattern contract,
   persona, default, or anti-pattern.
2. **Governed files** (tokens, component/pattern contracts, `design-brain/defaults.md`,
   `AGENTS.md`, tool projections) go through a **Change Request**
   (`_review/Change Request Template.md`) → design-system owner approves. Low-risk notes
   can be edited directly.
3. The **robot re-exports** the vault into `efficio-orbit`; **CI fails loudly if the repo
   copy ≠ the vault** (drift-check). Nobody hand-edits the copy.
4. AI tools in the repo now read the updated brain. Done.

## 2. Per-sprint Discovery loop

1. PM/PO writes the sprint brief in **Word** (the 4D Concept Discovery Pack).
2. **Distil it into the template** → one `discovery/<initiative>.md` (see
   `discovery/_TEMPLATE.md`; an AI agent can do the distillation). Set `status: active`;
   set `platform`, `linked_patterns`, `linked_components`.
3. It rides the same export to the repo. The AI **pulls the pack at START** and its
   **Part D delivery context feeds the handover**.
4. Sprint ends → mark the pack `shipped` → `archived`. Promote any reusable learning **up**
   into the brain (a new pattern, default, or anti-pattern).

## 3. Automated vs. manual

| The robot does (no upkeep) | Humans do (lightweight, periodic) |
| -------------------------- | --------------------------------- |
| Re-export vault → repo | Approve governed changes (owner) |
| Fail CI if the copy drifts | Distil each sprint's Word doc into a pack |
| Distribute the vault (Obsidian Sync) | Confirm `[CONFIRM]` / `[SCREENSHOT]` items → `stable` |
| | Archive shipped Discovery packs |
| | Re-sync **Lovable** projections after token/brain changes (the one manual projection, unless on the Enterprise design-system connection) |

## 4. The feedback loop (what makes it compound)

When an AI gets Orbit wrong and a human corrects it, **fix the vault file, not just the
output** (`AGENTS.md` §6 / the "FEED BACK" stage of the operating model). The robot
re-exports and the fix becomes true for everyone, permanently. Skipping this is how the
brain rots; doing it is how it sharpens every sprint.

## 5. Governance rhythm

From `_review/Governance.md` and the operating model's forums:

- **Product Design Working Group** (weekly) — ways of working, tooling, knowledge mgmt.
- **Design System Council** (fortnightly) — token/component/pattern governance, drift.
- **Delivery Excellence Forum** (monthly) — delivery metrics, lessons learned, adoption.
- **Quarterly health check** — promote `draft → stable`, retire dead components, sweep the
  Discovery index for stale packs, confirm lingering `[CONFIRM]` items.

## 6. Sync mechanics (how drift is prevented, not just detected)

1. **Auto re-export** — a scheduled job or git hook regenerates the repo copy from the
   vault, so it is never "someone forgot."
2. **CI drift-check** — `python3 tools/export_brain.py --target <repo> --profile all
   --check` is run in CI; it exits `1` when the repo copy differs from the vault, failing
   the build. (`--dry-run` only prints; use `--check` for gating.) "Out of sync" cannot
   happen silently once this job is wired into the product repo's CI.
3. **One-way discipline** — the repo copy carries the generated-export notice and is never
   hand-edited.

## Related

- `_review/Governance.md` — approval rules and review cadence.
- `_review/Change Request Template.md` — how authors propose governed changes.
- `_archive/usage-guides-2026-06/Team Sharing Setup.md` — Obsidian Sync setup for
  authors (archived; revive as a live doc before sharing the vault to more teams —
  see `_review/2026-07-03-full-vault-audit.md`, findings A1/A5).
- `discovery/README.md` — Discovery pack lifecycle and index.
- `tools/export_brain.py` — the exporter that generates the repo copy.
- `AGENTS.md` §6 — the feedback loop rule.
