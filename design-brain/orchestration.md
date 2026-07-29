---
type: orchestration
status: stable
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
| Judgment under written heuristics | design review, benchmark judging, reviewing a concept brief at intake, authoring a *new* contract or pattern, distilling discovery packs | `opus`-class (top tier) |

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
| `story-author` | Writes a component's Storybook story set (`write-stories` skill) | sonnet | Contract-constrained enumeration of the source |
| `design-reviewer` | Audits finished work against the brain | opus-class | Judgment-dense, last line of defence |
| `benchmark-judge` | Blind A/B scoring for benchmarks | opus-class | Scoring integrity |
| `brief-coach` | Helps a stakeholder write a strong brief (Socratic, draws it out) | opus-class | Judgment-dense authoring help |
| `brief-reviewer` | Reviews a concept brief at intake against the brief contract | opus-class | Judgment on intent, at the cheapest gate |

## The standard build pipeline

```
task ──> context-scout ──> builder (component / screen / porter)
              │                        │
              └── context packet ──────┘
                                       ▼
                       render-verify (builder pre-flight: Storybook
                       both themes + densities, a11y panel, audit
                       script — proven in the 2026-07-17 build trial)
                                       ▼
                       write-stories (new/story-less components —
                       story-author, then extract-contract)
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

## The intake & explore pipeline (upstream of the build)

Before the build pipeline there is a divergence pipeline that turns a stakeholder's
concept into a testable prototype. It fixes context-free Lovable hand-offs by capturing
intent at intake and gating it before generation.

```
(brief-coach) ──> intake form ──> brief-review ──> explore ──> (human steers) ──> port-prototype
 optional,        (Layer 1:        brief-reviewer   explore skill                  the winner
 draws a strong   in-browser       opus, FRESH      (concept, NOT                  becomes
 brief OUT of     completeness)    context,         Orbit-bound)                   Orbit-correct
 the stakeholder                   vs brief-contract
 (Socratic)                        → Ready / Needs work / Blocked
```

Hard rules:
- **Coach ≠ reviewer (a firewall).** `brief-coach` helps a stakeholder *write* a strong brief
  (Socratic, draws it out, never fabricates, never gives a verdict). `brief-reviewer` then
  *judges* it blind, in a fresh context. The same agent must never both coach and judge the
  same brief — it would pass what it authored. Two roles, one contract.
- **Two funnels, one seam.** `explore` diverges (fast, throwaway, not Orbit-bound);
  `port-prototype` converges (on-system). Never ask one pass to do both — that is the
  "correctness engine doing a creation job" failure.
- **The gate is a fresh context.** `brief-reviewer` judges the brief as written against
  `design-brain/brief-contract.md`, not the requester's conversation — same blindness
  rule as `design-reviewer`.
- **The human owns the bet.** `explore` presents; a person keeps, redirects, or kills.
- **Manual trigger only.** `brief-review` runs in a Claude session (no API secrets in CI),
  same rule as lessons-inbox triage.
- **Feasibility is capped by context.** Brief-contract criterion 7 (and thus this whole
  pipeline's output quality) is bounded by the Efficio Context Pack; the reviewer says so
  honestly rather than guessing buildability.

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

- **Vault CI (automated, no AI):** on every push — export self-check, link check
  (including the routing manifest and `then:` chains), frontmatter lint, graph-links
  check, the Storybook status-parser self-test, and an informational staleness report.
  A **daily** 06:00 UTC run additionally regenerates the health report, commits the
  trend, raises/clears a `vault-health` GitHub issue on drift, and republishes the
  stakeholder site (`.github/workflows/vault-integrity.yml`).
- **Component-repo CI (automated, no AI):** the design-system repo's `verify` job
  blocks on typecheck, lint, the full component test suite, and a Storybook build;
  Pages publishes only from a green `verify` (`design-brain/storybook.md`). **A red
  `verify` on the commit under review blocks a design-review PASS** — a reviewer must
  not pass work the repo's own gate rejects. Remember the recorded failure shape: a
  green Storybook build over a dead test suite; the steps gate separately for a reason.
- **Lessons-inbox triage (manual, needs judgment):** run the `vault-librarian` agent in
  a normal session on the entries in `design-brain/lessons/INBOX.md`; it proposes edits,
  the owner approves. Deliberately not wired to CI — no API secrets in the pipeline
  until the owner decides it's worth it. The inbox must trend toward empty; an entry
  older than two weeks is itself a health smell, and the private dashboard now counts
  open entries so a stalled queue stops being invisible.

  A triaged lesson has **two** possible homes, and forgetting the second is why the
  builders carried no accumulated knowledge until 2026-07-29:
  1. **A canonical brain file**, when the lesson changes a rule, a default, or a contract.
  2. **A trap on the agent that made the mistake**, when it is a recurring mechanical
     error rather than a rule change — stated inline next to the instruction it modifies
     and dated to the incident, as in `design-brain/agents/design-reviewer.md` and
     `design-brain/agents/component-builder.md`.

  Traps are evidence-backed or they are not written. Each cites the benchmark result or
  recorded correction it came from; the `Source-Required Follow-Up` section on each
  builder names where the next one goes.

  An entry is deleted only once its fix is **verified in place** — not when it is agreed.
  Both entries closed on 2026-07-29 had been applied days earlier and left sitting, which
  made a real backlog indistinguishable from a finished one.

## Vault-describing artifacts are generated projections

Any artifact that *describes the vault* — counts, rosters, maturity, status mixes, CI
claims — must be **generated from the vault at build time**, never hand-written. Three
separate artifacts have gone stale the other way ("8 agents" when there were 10, "97
documents", an invented maturity gauge). The pattern that works: pull live numbers from
the health data, and fail the build when a banned stale claim survives
(`tools/build_about_page.py` implements both). Hand-written prose *about* the vault is a
drift defect by default.

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
- `design-brain/storybook.md` — the component workbench, its CI, and the story rules
  the `write-stories` task enforces.
- `design-brain/lessons/INBOX.md` — mid-task correction capture (see `AGENTS.md` §6).
- `_review/2026-07-17-orchestration-and-optimisation-proposal.md` — the approved design.

<!-- graph-links:start — generated by tools/gen_graph_links.py; do not hand-edit -->
## Vault graph
[[AGENTS|AGENTS]] · [[_review/2026-07-17-orchestration-and-optimisation-proposal|2026-07-17-orchestration-and-optimisation-proposal]] · [[design-brain/agents/component-builder|component-builder]] · [[design-brain/agents/design-reviewer|design-reviewer]] · [[design-brain/brief-contract|brief-contract]] · [[design-brain/lessons/INBOX|lessons INBOX]] · [[design-brain/lovable/knowledge-base|knowledge-base]] · [[design-brain/storybook|storybook]]
<!-- graph-links:end -->
