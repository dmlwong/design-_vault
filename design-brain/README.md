---
type: reference-index
status: stable
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-07-17
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
| `defaults.md` | Default choices when unsure — spacing, padding, component picks (material layer). |
| `interaction-defaults.md` | The judgment layer: flow shape, IA, interaction model, output craft (#1–#13). |
| `anti-patterns.md` | The "never do this" list — highest-leverage quality lever. |
| `accessibility.md` | WCAG 2.2 AA baseline. |
| `motion.md` | Interaction & motion rules. |
| `ux-copy.md` | Voice & microcopy. |
| `data-viz.md` | Charts, KPIs, and analytics views (MarketIQ / RFP Analytics). |
| `platforms/README.md` | Platform split: Connected Platform vs Orbit / Client Connected Platform. |
| `platforms/<platform>-visual-truth.md` | Screenshot-derived visual guidance per platform (in-review). |
| `orchestration.md` | Multi-agent doctrine: the roster, the build pipeline, model routing. |
| `routing.json` | Machine-readable routing manifest (task → context packet → agent → model); CI-checked. |
| `lessons/INBOX.md` | Mid-task correction capture; triaged weekly into brain edits. |
| `SETUP.md` | How the brain was set up, phase by phase — the scaling method. |

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
| `patterns/README.md` | How patterns work + the index (11 pattern contracts). |

### Skills (on-demand workflows)
| File | Role |
| ---- | ---- |
| `skills/component-contract/SKILL.md` | Build/refactor a component to its contract. |
| `skills/extract-contract/SKILL.md` | Generate a contract from existing source — the populate-the-brain workflow. |
| `skills/write-stories/SKILL.md` | Write a complete Storybook story set for a component. |
| `skills/port-to-orbit/SKILL.md` | Bring an external/Lovable prototype onto Orbit. |
| `skills/explore/SKILL.md` | Turn a gated brief into an interactive throwaway concept prototype. |

### Agents (the roster — see `orchestration.md`)
| File | Model | Role |
| ---- | ----- | ---- |
| `agents/context-scout.md` | haiku | Assembles the context packet for a task from `routing.json`. |
| `agents/vault-librarian.md` | haiku | Vault hygiene: checks, lint, staleness, lessons-inbox triage. |
| `agents/contract-extractor.md` | sonnet | Contract drafts from real source (extract-contract skill). |
| `agents/component-builder.md` | sonnet | Builds one component to its contract (component-contract skill). |
| `agents/screen-builder.md` | sonnet | Composes full screens from patterns + contracted components. |
| `agents/porter.md` | sonnet | Ports external/Lovable prototypes onto Orbit (port-to-orbit skill). |
| `agents/story-author.md` | sonnet | Writes a component's Storybook story set (write-stories skill). |
| `agents/design-reviewer.md` | opus | Audits finished work against the Definition of Done. |
| `agents/benchmark-judge.md` | opus | Blind scorer for benchmarks/A-B tests (fresh context, always). |
| `agents/brief-coach.md` | opus | Helps a stakeholder write a strong brief (never judges it). |
| `agents/brief-reviewer.md` | opus | Reviews a concept brief at intake against the brief contract. |

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
- `agents/*` → exported into `.claude/agents/` (the whole roster; `model:` frontmatter
  selects the tier per agent).
- `lovable/*` → pasted into Lovable or replaced by an Enterprise Design System link.

## Maintenance
When an agent gets Orbit wrong and you correct it, update the relevant canonical file —
or, mid-task, drop the correction into `lessons/INBOX.md` for the weekly triage — then
re-project (re-paste the Lovable files; the CLI tools pick up the edit automatically).
Treat the brain as living memory.

The "Vault graph" footer in each note is **generated** from the back-ticked references
by `tools/gen_graph_links.py` (it's what lights up Obsidian's graph view). Don't
hand-edit it — after adding or removing references, re-run the script; CI fails if the
footers go stale.

<!-- graph-links:start — generated by tools/gen_graph_links.py; do not hand-edit -->
## Vault graph
[[AGENTS|AGENTS]] · [[CLAUDE|CLAUDE]] · [[README|design-_vault README]] · [[design-brain/SETUP|SETUP]] · [[design-brain/accessibility|accessibility]] · [[design-brain/agents/benchmark-judge|benchmark-judge]] · [[design-brain/agents/brief-coach|brief-coach]] · [[design-brain/agents/brief-reviewer|brief-reviewer]] · [[design-brain/agents/component-builder|component-builder]] · [[design-brain/agents/context-scout|context-scout]] · [[design-brain/agents/contract-extractor|contract-extractor]] · [[design-brain/agents/design-reviewer|design-reviewer]] · [[design-brain/agents/porter|porter]] · [[design-brain/agents/screen-builder|screen-builder]] · [[design-brain/agents/story-author|story-author]] · [[design-brain/agents/vault-librarian|vault-librarian]] · [[design-brain/anti-patterns|anti-patterns]] · [[design-brain/components/README|components README]] · [[design-brain/components/_TEMPLATE|components _TEMPLATE]] · [[design-brain/data-viz|data-viz]] · [[design-brain/defaults|defaults]] · [[design-brain/examples/README|examples README]] · [[design-brain/interaction-defaults|interaction-defaults]] · [[design-brain/lessons/INBOX|lessons INBOX]] · [[design-brain/lovable/knowledge-base|knowledge-base]] · [[design-brain/lovable/workspace-knowledge|workspace-knowledge]] · [[design-brain/motion|motion]] · [[design-brain/orchestration|orchestration]] · [[design-brain/patterns/README|patterns README]] · [[design-brain/patterns/_TEMPLATE|patterns _TEMPLATE]] · [[design-brain/platforms/README|platforms README]] · [[design-brain/principles|principles]] · [[design-brain/skills/component-contract/SKILL|component-contract SKILL]] · [[design-brain/skills/explore/SKILL|explore SKILL]] · [[design-brain/skills/extract-contract/SKILL|extract-contract SKILL]] · [[design-brain/skills/port-to-orbit/SKILL|port-to-orbit SKILL]] · [[design-brain/skills/write-stories/SKILL|write-stories SKILL]] · [[design-brain/tokens|tokens]] · [[design-brain/ux-copy|ux-copy]]
<!-- graph-links:end -->
