---
type: reference-index
status: stable
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-06-14
maturity_score: 72
tags: [orbit, design-brain, index]
---

# design-brain/ — Reference Layer

This folder holds the detailed reference layer for the Orbit Design Brain. The canonical
Obsidian vault root contains `AGENTS.md`, `CLAUDE.md`, and `README.md`; this folder holds
the files those entry points route agents into.

The reference layer has one shared foundation plus two platform profiles:
Connected Platform for internal Efficio users, and Orbit / Client Connected Platform for
external client users.

**Author in the Obsidian vault. Export into product repos. Never hand-edit generated
exports.**

## How it fits together

```
                 ┌─────────────────────────────┐
                 │   CANONICAL (edit here)      │
                 │   AGENTS.md  +  references    │
                 │   principles / tokens /       │
                 │   anti-patterns / a11y /      │
                 │   motion / ux-copy /          │
                 │   components/ / examples/      │
                 └──────────────┬──────────────┘
                                │ project into
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                        ▼
  Claude Code              Codex                     Lovable
  CLAUDE.md  ──@imports──► AGENTS.md (read directly)  lovable/knowledge-base.md
  + skills/               + skills/                   + lovable/workspace-knowledge.md
                                                      (or Enterprise Design System)
```

- **Claude Code** auto-loads `CLAUDE.md`, which `@imports` `AGENTS.md`.
- **Codex** reads `AGENTS.md` directly (it's the open AGENTS.md standard).
- **Lovable** can't read the repo, so paste the projections in `lovable/` into its
  Knowledge Base / Workspace Knowledge — or, on Enterprise, connect a Design System project.
- The detailed reference files load on demand via the routing table in `AGENTS.md` §3.

## The files

### Always-on / entry points
| File | Role |
| ---- | ---- |
| `AGENTS.md` | **Canonical brain.** Identity, hard rules, routing, Definition of Done. The master. |
| `CLAUDE.md` | Thin Claude Code entry point; `@imports AGENTS.md` + Claude-specific notes. |

### Reference layer (loaded on demand)
| File | Role |
| ---- | ---- |
| `principles.md` | How Orbit should *feel* — the intent layer. |
| `tokens.md` | Token contract / governance with real source paths. |
| `anti-patterns.md` | The "never do this" list — highest-leverage quality lever. |
| `accessibility.md` | WCAG 2.2 AA baseline. |
| `motion.md` | Interaction & motion rules. |
| `ux-copy.md` | Voice & microcopy. |
| `data-viz.md` | Charts, KPIs, and analytics views (MarketIQ / RFP Analytics). |
| `platforms/README.md` | Platform split: Connected Platform vs Orbit / Client Connected Platform. |

### Components & examples
| File | Role |
| ---- | ---- |
| `components/_TEMPLATE.md` | The contract template — copy per component. |
| `components/README.md` | How contracts work + the component index. |
| `components/<name>.md` | One source-backed or specified contract per component. |
| `examples/README.md` | What golden examples are and current source status. |
| `examples/<files>` | Source-linked reference implementations and known gaps. |
| `examples/screenshots/<platform>/manifest.md` | Visual truth intake manifests for real platform screenshots. |
| `patterns/_TEMPLATE.md` | Page-level pattern contract template (compositions, not bricks). |
| `patterns/README.md` | How patterns work + index (seed: focus-mode-results, guided workflow). |

### Skills (on-demand workflows)
| File | Role |
| ---- | ---- |
| `skills/component-contract/SKILL.md` | Build/refactor a component to its contract. |
| `skills/extract-contract/SKILL.md` | Generate a contract from existing source — the populate-the-brain workflow. |
| `skills/port-to-orbit/SKILL.md` | Bring an external/Lovable prototype onto Orbit. |
| `agents/design-reviewer.md` | Reviewer subagent definition — audits work against the Definition of Done. |

### Lovable projections
| File | Role |
| ---- | ---- |
| `lovable/knowledge-base.md` | Project-level Knowledge Base text. |
| `lovable/workspace-knowledge.md` | Workspace-wide rules. |

## What Still Needs Real Source
1. Add real sanitized screenshots to the platform visual truth manifests.
2. Decide whether drawer becomes a reusable Orbit component; no canonical source was found.
3. Link MarketIQ / RFP Analytics KPI and dashboard source.
4. Validate the remaining page patterns against real product screens.
5. Run future benchmark tasks after exporting into a product repo.
6. Add dedicated motion duration/easing tokens to the coded design system if approved.

## Where This Lives
- `AGENTS.md`, `CLAUDE.md` → vault root and generated product repo root.
- `skills/*` → exported into `.claude/skills/` for Claude Code.
- `agents/design-reviewer.md` → exported into `.claude/agents/`.
- `lovable/*` → pasted into Lovable or replaced by an Enterprise Design System link.

## Maintenance
When an agent gets Orbit wrong and you correct it, update the relevant canonical file,
then re-project (re-paste the Lovable files; the CLI tools pick up the edit automatically).
Treat the brain as living memory.
