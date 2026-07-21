---
type: proposal
status: draft
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-07-21
maturity_score: 0
tags: [orbit, design-brain, intake, brief, explore, governance, proposal]
---

# Proposal: Context-First Intake — form, brief rubric, and the review gate

> Lovable prototypes arrive with no record of the concept behind them, so teams
> reverse-engineer intent from pixels. This captures intent at intake with a structured
> form, gates it against a written rubric before generation, and feeds a **Ready** brief
> to the existing `explore` skill. It is the front door the divergence funnel was missing.
> **Draft** — everything ships behind `status: draft`, piloted below, promoted only by the
> owner after a live run.

## Why this exists

The vault already solved the *converge* problem (port/govern a prototype onto Orbit). It
lacked the *diverge* front door: a way to turn a stakeholder's problem into a testable
concept without losing the context that makes it feel like real Efficio. `explore` exists
for that — but was unwired and had no disciplined input. A brief with no standard produces
a *convincing* prototype on the wrong premise, which costs more downstream than a rejected
brief. The gate catches that at the cheapest point.

## The pipeline

```
intake form ─▶ 2a completeness (rule) ─▶ 2b brief-review (agent) ─▶ ground ─▶ explore ─▶ human steers ─▶ port
 (capture)      deterministic, free        opus, fresh context,       vault +    concept,     keep /        winner
                                           vs brief-contract          context    not Orbit    redirect /    becomes
                                           → Ready/Needs work/Blocked             -bound       kill          on-system
```

Colour of the funnel: `explore` diverges (throwaway, not Orbit-bound); `port-prototype`
converges. One seam, never one pass doing both. Doctrine lives in
`design-brain/orchestration.md`; the machine-readable wiring is `design-brain/routing.json`
(new tasks `brief-review` and `explore` — the latter registers a skill that existed on disk
but was absent from the manifest).

## Decisions locked (with the user)

1. **Lovable:** the vault generates the prototype via `explore` (primary) **and** optionally
   emits a context-rich **Lovable seed prompt** for stakeholders who iterate in Lovable —
   a projection of the brief, not a second source of truth.
2. **Form:** a self-contained HTML file in `tools/` with in-browser Layer-1 validation and
   an import/resubmit round-trip; committed briefs land in `discovery/briefs/`. Pages
   hosting later (reuses the health-dashboard path).
3. **Scope:** build everything now as `draft`; pilot the rubric before any promotion
   (vault discipline: manual → proven → encoded).

## The form → `explore` mapping

The intake form (`tools/intake-form.html`) has an **About** group (title, requester, team,
date — for identity, the gate log, and the filename) plus the concept fields, each mapping
to a `brief-contract` criterion / `explore` brief element:

| Field | Feeds |
| ----- | ----- |
| Platform · Surface | loads the right platform profile + patterns (criterion 8) |
| Problem statement · Why now | criterion 1 (problem-not-solution) · 5 (evidence) |
| Primary user + situation | criterion 2 (one user & moment) |
| Key journey / tasks | criterion 3 (one testable bet) |
| Key outcomes | criterion 4 (falsifiable outcome) |
| Out of scope | criterion 6 (fenced scope) |
| Known constraints | criterion 7 (feasibility) |
| Existing material · Open questions | context to read · flagged assumptions |

## Governance principles

- **The rubric is written down** (`design-brain/brief-contract.md`) — reviews are
  consistent and auditable, not vibes.
- **Human override, logged.** A verdict is advice with authority; the product or
  design-system owner may override, with the reason recorded in the brief's `## Gate log`.
- **Manual → proven → encoded.** The reviewer runs by hand first (this proposal), encoded
  as an agent but held at `draft` until a live pilot earns promotion.
- **Feasibility is capped by the Context Pack.** Criterion 7 can only judge *whether*
  feasibility was considered until tech reality lands in the vault; the reviewer says so
  rather than guessing buildability.

## Pilot — a dry run of the rubric (2026-07-21)

Three briefs, expected verdicts **pre-registered** before scoring, then scored by hand
against the eight criteria in `brief-contract.md`.

| # | Brief | Pre-registered | Actual | Match |
| - | ----- | -------------- | ------ | ----- |
| 1 | `discovery/marketiq-research-agent-n8n-upgrade.md` (as a brief) | Blocked | **Blocked** | ✓ |
| 2 | `discovery/research-agent-in-initiatives-cp-orbit.md` (as a brief) | Needs work | **Needs work** | ✓ |
| 3 | Form-generated Commentary brief (fill → generate → import → regenerate) | Ready | **Ready** | ✓ |

Per-criterion detail:

- **Brief 1 — MarketIQ n8n upgrade → BLOCKED.** FAIL on 1 (a backend/tech-debt goal, not a
  user problem), 2 (actor is an internal team doing maintenance, no situated moment), 3
  (no single UI flow — the sprint is a migration), 4 (engineering outcome, not
  prototype-testable). PASS on 5, 6, 7, 8. It is not an `explore` candidate at all — the
  right pipeline is build/discovery. The gate correctly refused it.
- **Brief 2 — Research Agent unify → NEEDS WORK.** A real, rich concept, but FAIL on 2 and
  3 (three journeys + re-run card + share + coverage-card states bundled together) and 4
  (success is mostly engineering). PASS on 1, 5, 6, 7, 8. The fix is to **narrow to one
  bet** (e.g. the re-run + who/when workspace card) — exactly what the reviewer output says.
- **Brief 3 — Commentary at-a-glance → READY.** All eight PASS: one consultant in one
  moment, a single scan-and-act flow, a falsifiable 30-second outcome, evidence (two
  escalations), a fenced scope, feasibility named (existing commentary/audit store). One
  honest flag under 7: the reviewer can PASS "feasibility acknowledged" but cannot *verify*
  last-review timestamps are exposed — noted, not invented.

**Pilot result:** all three verdicts matched pre-registration; every verdict is explainable
per criterion; **no new criteria were invented and no criterion needed rewriting** (pass
bar met). Key finding worth keeping: **a discovery pack is not a brief** — packs are
downstream, multi-journey, and solution-decided, so scoring one as a brief almost always
fails criterion 3 by design. That is the right signal: a winning brief *graduates into* a
pack, not the reverse. Criterion 3 (one testable bet) proved the sharpest filter.

## Live pilot — real stakeholder brief (2026-07-21)

The first genuinely real run: the **Commentary / RAID Enhancements Sponsor Intake pack**
(Sprint 83), taken through the whole loop — filled into `tools/intake-form.html`, then
reviewed by the `brief-reviewer` agent in a **fresh context** (it read the contract and CP
profile itself, never saw this conversation). Both briefs are committed under
`discovery/briefs/`.

- **Round 1 — as first submitted (broad) → NEEDS WORK.** PASS on 1, 5, 6, 7; FAIL on 2, 3,
  4, 8. The reviewer caught four bundled bets (capture / review / bulk / Sigma reuse),
  an unfalsifiable outcome, and an unresolved surface — and named the single
  highest-evidence bet to keep. This matched pre-registration and mirrors the pack's own
  ask ("recommend the highest-ROI one-sprint improvement").
- **Round 2 — narrowed per the reviewer's guidance → READY.** All eight pass. Criterion 7
  flagged the load-bearing dependency honestly (does who/when metadata exist on current CP
  updates?) as **CANNOT VERIFY**, routed to the Context Pack backlog rather than assumed.

**What the live run proves:** the gate is a *coach*, not just a filter — one fresh-context
review turned a broad, un-buildable intake into a Ready, testable brief, and it produced
exactly the Context Pack backlog the feasibility ceiling predicts. Two real context gaps
surfaced (the RAID/commentary data model has no vault spec; CP visual truth for the
initiative surface is still restricted). It also surfaced a **product finding in the form**:
the Surface list has no option for CP initiative / project-governance, forcing "Other /
shared", which the reviewer correctly flagged — logged to `design-brain/lessons/INBOX.md`.

## Follow-ups (named, not silent)

- **Success metrics** for the initiative — % of briefs Ready on first pass, rework cycles —
  defined once ≥5 real briefs exist; the `## Gate log` data is the raw material, and
  `vault_health.py` can later count briefs by gate status.
- **A committed-brief linter** (`tools/lint_briefs`) in CI to lint briefs in the repo
  (Layer 1 for the repo, not just the form).
- **Publish the form** to the Pages repo for a shareable URL (owner action, same path as
  the health dashboard).
- **AGENTS.md routing-table row** (governed): add "Reviewing a concept brief →
  `design-brain/brief-contract.md`" — proposed here for owner sign-off, not applied.
- **Promotion** of `brief-reviewer` and `brief-contract` to `stable` — owner decision after
  a live pilot on real stakeholder briefs.

## What this is not

- Not a Context Pack (separate initiative — it lifts criterion 7's ceiling, not built here).
- Not orchestration change beyond registering the intake stage the manifest already needed.
- Not a replacement for judgment — the human owns the bet; the gate protects the cheapest
  decision point, it does not make the decision.

<!-- graph-links:start — generated by tools/gen_graph_links.py; do not hand-edit -->
## Vault graph
[[design-brain/brief-contract|brief-contract]] · [[design-brain/lessons/INBOX|lessons INBOX]] · [[design-brain/orchestration|orchestration]] · [[discovery/marketiq-research-agent-n8n-upgrade|marketiq-research-agent-n8n-upgrade]] · [[discovery/research-agent-in-initiatives-cp-orbit|research-agent-in-initiatives-cp-orbit]]
<!-- graph-links:end -->
