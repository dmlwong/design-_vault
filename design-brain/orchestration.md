---
type: orchestration
status: in-review
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-07-17
maturity_score: 60
context_tier: task-core
load_when: [orchestration, model-choice, multi-agent-work]
tags: [orbit, design-brain, orchestration, agents, model-routing]
---

# Orchestration — agents, pipelines, and model routing

How vault-driven work is split across specialist agents, in what order they run, and
which AI model tier each task deserves. This file is doctrine: any orchestrator (a
Claude Code session, a Codex operator, a CI job, a human) follows the same rules.
The machine-readable companion is `design-brain/routing.json` — task → context packet
→ agent → model. Prose here is canonical; the manifest is CI-checked against reality.

## The one principle behind model routing

> **The more a task is constrained by something written, the cheaper the model.
> The more it depends on judgment the vault can't fully write down, the stronger the model.**

| Constraint level | Examples | Tier |
| ---------------- | -------- | ---- |
| Fully specified — a checklist or script could almost do it | link check, token scan, frontmatter lint, context assembly | `haiku` |
| Contract-constrained generation | build to an existing contract, extract a contract from source, port with a mapping | `sonnet` |
| Judgment under written heuristics | design review, benchmark judging, authoring a *new* contract or pattern, distilling discovery packs | `opus`-class (top tier) |

Rules:
- Tiers are **aliases**, never pinned model IDs — each tool maps them to what it has.
- Fallback: unknown task → inherit the session model.
- **Never silently downgrade a review or judging task.** If the top tier is unavailable,
  say so and let a human decide.
- The strongest model goes on the **reviewer**, not the builder. Contracts constrain the
  builder; what slips past contracts (flow shape, craft) is exactly what review exists to
  catch, and rework costs more than review.

## The roster

Definitions live in `design-brain/agents/` (exported to `.claude/agents/` for Claude
Code; other tools paste them as personas). Each declares `model:` in frontmatter.

| Agent | Does | Model | Why that tier |
| ----- | ---- | ----- | ------------- |
| `context-scout` | Assembles the context packet for a task from `routing.json` | haiku | Deterministic lookup |
| `vault-librarian` | Link check, frontmatter lint, staleness sweep, lessons-inbox triage | haiku | Mechanical, high-volume |
| `contract-extractor` | Contract drafts from real source/Storybook (`extract-contract` skill) | sonnet | Structured transformation |
| `component-builder` | Builds/refactors one component (`component-contract` skill) | sonnet | The contract does the judgment |
| `screen-builder` | Multi-component/pattern composition | sonnet → opus-class when no pattern contract exists | Ambiguity rises without a written pattern |
| `porter` | Ports external/Lovable prototypes (`port-to-orbit` skill) | sonnet | Mapping to an explicit target |
| `design-reviewer` | Audits finished work against the brain | opus-class | Judgment-dense, last line of defence |
| `benchmark-judge` | Blind A/B scoring for benchmarks | opus-class | Scoring integrity |

## The standard build pipeline

```
task ──> context-scout ──> builder (component / screen / porter)
              │                        │
              └── context packet ──────┘
                                       ▼
                          design-reviewer  (ALWAYS a fresh context)
                             │ PASS                │ FAIL (any blocker)
                             ▼                     ▼
                     handover check          back to the builder with the
                     (OrbitInspector,        blocker list — max 2 loops,
                      required artifacts)    then STOP and escalate to a human
```

Hard rules:
- The **reviewer never edits** and the **builder never self-certifies** (a blocker means
  not done — `AGENTS.md` §5).
- The reviewer and the benchmark-judge run in **fresh contexts**: they must not see the
  builder's conversation, only the produced artifact and the brain.
- **Two failed review loops = stop.** Repeated failure on the same blocker usually means
  the *contract* has a gap — that's a Phase 9 signal (fix the brain), not a
  keep-retrying signal.
- Every generated prototype passes the handover check before it's called done
  (inspector mounted once, benchmark artifacts present where required).

## Fan-out rules (when to parallelise)

- **Parallelise independent artifacts only**: e.g. the contract backlog
  (`PageHeader`/`HeaderPresets`, `Spinner`, `Table` variants) — one `contract-extractor`
  per component, human-review the drafts as a batch.
- **Multi-dimension review** for full screens: run the reviewer checklist dimensions
  (tokens / states / accessibility / density / composition) as parallel focused passes
  and merge the findings — small passes miss less than one long pass.
- **Never parallelise** edits to the same contract or governed file — those serialize
  through the change-request path (`AGENTS.md` §7).

## Scheduled maintenance

- **CI (automated, no AI):** link check + frontmatter lint on every push; weekly
  staleness report (`tools/lint_frontmatter.py --stale-report`, informational).
- **Lessons-inbox triage (manual, needs judgment):** run the `vault-librarian` agent in
  a normal session on the entries in `design-brain/lessons/INBOX.md`; it proposes edits,
  the owner approves. Deliberately not wired to CI — no API secrets in the pipeline
  until the owner decides it's worth it.

## Tool bindings

- **Claude Code:** the exporter copies every `design-brain/agents/*.md` to
  `.claude/agents/`; the `name`/`description`/`model` frontmatter keys make them native
  subagents (`model:` is honored per invocation). Skills already export to
  `.claude/skills/`.
- **Codex / other CLI agents:** no subagent runtime — use the agent files as pasted
  role prompts and follow this doctrine manually; the `model:` key maps to the tool's
  own tiers.
- **Lovable:** out of scope for orchestration (single-tool projection);
  `lovable/knowledge-base.md` remains the projection path.

## Related

- `design-brain/routing.json` — the machine-readable manifest (CI-checked).
- `design-brain/agents/` — the roster definitions.
- `design-brain/lessons/INBOX.md` — mid-task correction capture (see `AGENTS.md` §6).
- `_review/2026-07-17-orchestration-and-optimisation-proposal.md` — the approved design.
