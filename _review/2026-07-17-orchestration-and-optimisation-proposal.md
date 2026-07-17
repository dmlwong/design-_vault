---
type: proposal
status: draft
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-07-17
maturity_score: 0
tags: [orbit, design-brain, orchestration, agents, model-routing, proposal]
---

# Proposal: Vault Optimisation, Agent Orchestration & Model Routing

> Research output, 2026-07-17. Three connected upgrades: (A) make the vault cheaper and
> more precise for agents to consume, (B) split vault-driven work across specialist
> agents with defined handoffs, (C) encode which AI model tier each task deserves so
> orchestrators pick automatically. Nothing here changes design content — it changes how
> the content is *executed*.

## Why this, why now

The vault's content layer is validated (benchmarks: compliance 17/18, UX 15/16 vs 7/16,
craft 0→10). Its remaining inefficiency is operational:

1. **One generalist context does everything.** Build, review, extraction, and audit all
   run in the same conversation today. The vault itself says the builder "should never
   grade its own homework" (`agents/design-reviewer.md`) — but nothing else is separated
   either, so context fills with mixed concerns and quality drifts on long sessions.
2. **Routing is prose.** `AGENTS.md` §3 is a human-readable table; an agent must *decide*
   to obey it. There is no machine-checkable statement of "task X ⇒ load files Y, Z".
3. **Every task pays the same model cost.** Link checking and design review are billed
   the same way. Mechanical work overpays; judgment work sometimes underpays (a fast
   model reviewing craft misses what the craft heuristics exist to catch).

## A. Vault optimisations (consumption layer)

### A1. Machine-readable routing manifest
Add `design-brain/routing.json` compiled from (and CI-checked against) `AGENTS.md` §3:

```json
{
  "tasks": {
    "build-component": {
      "load": ["components/<name>.md", "tokens.md", "defaults.md",
                "platforms/<platform>.md", "examples/<nearest>.md"],
      "skill": "component-contract",
      "agent": "component-builder",
      "then": ["design-review"]
    },
    "design-review": {
      "load": ["AGENTS.md", "components/*", "patterns/*", "anti-patterns.md",
                "accessibility.md"],
      "agent": "design-reviewer"
    }
  }
}
```

Prose stays canonical for humans; the manifest makes it executable. The link checker
gains a rule: every manifest path must exist (no drift).

### A2. `load_when` frontmatter
Each reference file declares its own triggers, so routing can be *computed* per task:

```yaml
load_when: [component-build, component-review, token-question]
context_tier: task-core   # always-on | task-core | reference | archive
```

Tiers give any orchestrator a budget rule: always-on is loaded every session (today:
`AGENTS.md` only, ~160 lines — correctly thin); task-core loads when the manifest says
so; reference loads on demand; archive never auto-loads.

### A3. Lessons inbox (feedback loop, friction removed)
Rule §6 says "update the brain file when corrected" — mid-task, that's heavyweight, so it
gets skipped. Add a lessons inbox (proposed new note `INBOX` in a new
`design-brain/lessons/` folder): any agent that gets corrected appends
a structured entry (date, task, wrong assumption, correction, proposed target file). The
vault-librarian agent (below) turns approved entries into edits weekly. Low friction in
the moment, governed promotion afterward.

### A4. Heavy-asset lazy rules
The `.tsx` golden examples and screenshots are the vault's largest items. Codify: load a
reference implementation **only** when building its component family; never load
screenshots into agent context (they are human/visual-truth evidence).

### A5. Decision log as agent context
The stakeholder-requested `decisions/` log doubles as agent guidance ("no Drawer — use
Overlay; rejected because…"). Prevents agents relitigating settled questions exactly the
way it prevents humans doing so. Mark it `context_tier: task-core` for build tasks.

### A6. Vault CI, next tier
Extend `.github/workflows/vault-integrity.yml`: frontmatter lint (required keys, valid
status values, `last_reviewed` not in the future), routing-manifest check (A1), and a
staleness report (files not reviewed in 90 days) posted as a PR comment, not a failure.

## B. Agent orchestration (execution layer)

### B1. The roster
Specialist definitions live in `design-brain/agents/` (exported to `.claude/agents/`,
usable as prompts in any other tool). Each declares scope, inputs, outputs, and model.

| Agent | Does | Model | Why that tier |
| ----- | ---- | ----- | ------------- |
| `context-scout` | Reads routing manifest + task, returns the context packet (files, platform, contract list) | **haiku** | Deterministic lookup, no judgment |
| `vault-librarian` | Link check, frontmatter lint, stale sweep, lessons-inbox triage | **haiku** | Mechanical, high-volume |
| `contract-extractor` | Runs `extract-contract` against source/Storybook | **sonnet** | Structured transformation of real code |
| `component-builder` | Runs `component-contract` to build/refactor one component | **sonnet** | Constrained by an explicit contract — the contract does the judgment |
| `screen-builder` | Multi-component/pattern composition | **sonnet**, opus when no pattern contract exists | Ambiguity rises when there's no written pattern |
| `porter` | Runs `port-to-orbit` on external/Lovable prototypes | **sonnet** | Mapping task with explicit target system |
| `design-reviewer` | Audits finished work vs the brain (exists today) | **opus / top tier** | Judgment-dense; the last line of defence |
| `benchmark-judge` | Blind A/B scoring for the benchmark process | **opus / top tier**, fresh context, never sees builder chat | Scoring integrity |

**The key inversion:** put the *strongest* model on review, not on build. The vault's own
evidence supports it — compliance came from contracts constraining the builder; what
slipped through (craft, flow shape) was caught by judgment. Rework costs more than review.

### B2. The standard build pipeline

```
task ──> context-scout ──> builder (component/screen/porter)
              │                     │
              └── context packet ───┘
                                    ▼
                          design-reviewer (fresh context)
                             │ PASS          │ FAIL (any blocker)
                             ▼               ▼
                     handover check    back to builder with the
                     (OrbitInspector,  blocker list — max 2 loops,
                      artifacts)       then escalate to a human
```

Rules: the reviewer never edits; the builder never self-certifies; two failed
review loops = stop and ask (prevents infinite churn on a contract gap — which is
itself the signal to fix the contract, per Phase 9).

### B3. Fan-out patterns (when to parallelise)
- **Contract backlog:** the known gaps (`PageHeader`/`HeaderPresets`, `Spinner`, `Table`
  variants) are independent — run `contract-extractor` on each in parallel, human-review
  the drafts as one batch.
- **Multi-dimension review:** for full screens, run the reviewer's checklist dimensions
  (tokens / states / a11y / density / composition) as parallel focused passes and merge —
  each pass is small and misses less than one long pass.
- **Never parallelise** edits to the same contract or governed file; those serialize
  through the change-request path.

### B4. Scheduled maintenance
A weekly `vault-librarian` run (CI cron or a scheduled agent session): link check,
frontmatter lint, staleness report, lessons-inbox triage into proposed edits. Output is a
single PR the owner reviews — the maintenance loop (Phase 9) stops depending on memory.

## C. Model routing (the decision rule)

One principle, stated once and encoded in every agent definition:

> **The more the task is constrained by something written, the cheaper the model.
> The more it depends on judgment the vault can't fully write down, the stronger the model.**

| Constraint level | Examples | Tier |
| ---------------- | -------- | ---- |
| Fully specified (a checklist or script could almost do it) | link check, token scan, frontmatter lint, context assembly | haiku |
| Contract-constrained generation | build to an existing contract, extract a contract from source, port with a mapping | sonnet |
| Judgment under written heuristics | design review, benchmark judging, writing a *new* contract or pattern, distilling discovery packs | opus / top tier |

Mechanics per tool:
- **Claude Code:** `model:` frontmatter in each `.claude/agents/*.md` (`haiku` /
  `sonnet` / `opus` / `inherit`); the orchestrating session stays on the session model.
- **Codex / other tools:** the agent files carry the same `model:` metadata; the doctrine
  file tells the operator to map tiers to that tool's equivalents.
- **Fallback:** unknown task → inherit the session model; never silently downgrade a
  review/judging task.

## Implementation plan (on approval)

1. A new orchestration doctrine file under `design-brain/` — the roster, pipeline,
   fan-out rules, model-routing table (source of truth for B & C). Add it to the
   `AGENTS.md` §3 routing table.
2. Seven new agent definitions in `design-brain/agents/` (design-reviewer already
   exists; add `model:`+`context packet` sections to it too).
3. `design-brain/routing.json` + `load_when`/`context_tier` frontmatter across the
   reference layer; extend `tools/check_links.py` to validate the manifest.
4. Exporter: copy all agents to `.claude/agents/`; include `routing.json`; update
   `REQUIRED_FILES`.
5. CI: frontmatter lint + manifest check; wire the weekly librarian job.
6. The lessons inbox note (A3) + a short section in `AGENTS.md` §6 pointing agents at it.

Estimated effort: one working session for 1–4; CI/cron (5) depends on where the runner
lives; 6 is minutes.

## What this does NOT change
- No design content, tokens, contracts, or platform truth changes.
- Governance is unchanged — agents propose, owners approve; governed files still ride
  change requests.
- The always-on layer stays thin; this proposal *reduces* average context per task.

## Status
draft · for design-system owner review · implementation gated on approval
