---
type: proposal
status: draft
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-07-17
maturity_score: 0
tags: [orbit, design-brain, context-pack, explore, product-context, proposal]
---

# Proposal: The Efficio Context Pack

> The thing that blocked every concept-exploration attempt on 2026-07-17. The vault is rich
> in *how Orbit should look and behave* and poor in *who it's for, where it's going, and
> what's technically real* — and concept work needs the second far more than the first. This
> defines the missing layer, its shape, its sources, and how it connects to Claude.

## Why this exists

When we ran the `explore` method against the Commentary Enhancements concept pack, the
prototype only got good after we supplied — by hand — a persona, a product direction, a
domain, and a feasibility assumption. Every pressure-test then landed on the *same* missing
foundation: *what is CP becoming? who exactly is the PM? what does the platform record today?*
The **`explore` skill, the concept-critic, and connecting the vault to Claude are all blocked
by the same gap.** The Context Pack fills it.

**One-line definition:** a curated, standing bundle of Efficio **product** context that grounds
concept exploration (and any AI generation) so the output feels like a real Efficio feature,
not a generic demo.

## Where it sits — a second layer, not a rewrite

The vault becomes the single source of truth for **two** kinds of knowledge, projected to
different consumers:

```
                        THE VAULT (single source of truth)
      ┌──────────────────────────────┬──────────────────────────────┐
      │  Design-system layer (today)  │  Product-context layer (NEW)  │
      │  tokens · components ·        │  vision · personas · domain · │
      │  patterns · platform truth    │  tech reality · process       │
      └───────────────┬──────────────┴───────────────┬──────────────┘
                      │ projects                       │ projects
                      ▼                                ▼
             PORT / GOVERN (converge)          EXPLORE (diverge)
        port-to-orbit, component-contract       the /explore skill,
        → Orbit-correct, on-system              concept-critic → testable concepts
```

The context pack is **product context, not design rules.** It does not enforce Orbit fidelity
(Explore is deliberately not Orbit-bound). It lives in its own namespace — proposed
`context/` at the vault root — kept clearly separate from `design-brain/` so the two layers
never blur.

## What it holds (the sections)

Ordered by how load-bearing each was in the 2026-07-17 exploration. **Current state** is how
much of it already exists in the vault.

| # | Section | What it holds | Primary source | Current state |
|---|---------|---------------|----------------|---------------|
| 1 | **Product vision & strategy** | What CP and Orbit/CCP are *becoming* (e.g. "CP as the live governance source of truth"); near-term priorities; explicit non-directions | Leadership, roadmap, strategy | **Absent** — the biggest gap |
| 2 | **Users & personas** | Real personas: goals, context of use, what makes them anxious, a day in their work — PM, consultant, admin, external client | User research, interviews | **Partial** — 2/4 CP confirmed; Orbit provisional (`cp-personas-WIP.md`) |
| 3 | **Tech & data reality** | What the platform can/can't feasibly do; **what the system records today**; data available; integrations (Sigma, n8n); RBAC/security; scale | Engineering / architecture / specialist workstreams | **Absent** at product level — only component/token tech exists |
| 4 | **Domain & vocabulary** | Procurement/sourcing language and workflows: initiative, RAID, sourcing wave, category, baseline, savings, RFP, supplier; the initiative lifecycle | Domain experts, discovery packs | **Thin** — scattered in examples/discovery |
| 5 | **Product & surfaces** | What CP vs Orbit/CCP are; the surfaces (ClauseIQ, MarketIQ, RFP Analytics/Builder) and how they relate | Platform profiles, product docs | **Decent** — `platforms/*` profiles exist |
| 6 | **Process & governance** | The delivery gates (Concept Commitment, Build Readiness), sprint model, who decides; **client-visibility governance** (internal vs client-safe, approval) | The concept-pack process doc, governance | **Partial** — process implied, client-governance unmodelled |
| 7 | **Product decisions & non-goals** | Settled product decisions and deliberate non-goals ("no X because…") so concepts don't relitigate or drift out of bounds | Decision log | **Absent** at product level |

**Load-bearing four:** #1 Vision, #2 Personas, #3 Tech reality, #4 Domain. Their absence is
what hurt on 2026-07-17. #5–#7 are supporting.

## Design principles (so it stays useful, not a doc-dump)

- **Provenance + confidence on every item.** Each fact is tagged `confirmed` / `provisional` /
  `assumed`, with its source. `explore` uses this to know what's solid vs. what to flag.
- **An explicit "Known gaps" register.** Where a section is thin, say so — that is what lets
  Explore be honest about its assumptions instead of inventing silently.
- **Concise and high-signal.** It loads into an AI context window; budget matters. Curated
  summaries, not raw research dumps.
- **Living and owned.** Versioned in the vault, owned by product + design, updated as research
  lands. Same governance discipline as the rest of the vault.
- **Product context, never design rules.** If it starts specifying components or tokens, it has
  drifted into the wrong layer.

## How it connects to Claude

Same "author here, project everywhere" mechanic the design-system layer already uses:

- **Claude Project knowledge** — fastest path for designers in claude.ai / Artifacts running
  `/explore`: the pack (or a projection of it) is the project's knowledge base.
- **MCP** — a live connection for Claude Code and connector-enabled surfaces, so the pack is
  queried in real time rather than copy-pasted.
- **Read by `/explore`** at its Frame step; read by `critique-concept`; available to any
  generation that should feel Efficio-shaped.
- Projected like the existing `lovable/` knowledge base — one authored source, projected to
  each consumption surface.

## How it gets built and maintained

- **`distill-context` skill** (proposed, not yet built) turns raw inputs — research,
  interviews, product/architecture docs, discovery packs, a Word concept pack — into these
  structured sections with provenance tags.
- **Every concept pack feeds it.** The gaps `explore` flags on each run are the backlog for the
  pack — a self-improving loop: explore → surfaces gaps → distill fills them → next explore is
  sharper.
- **Build from real inputs, not speculation** (the session's discipline). Start with the
  load-bearing four, populated from real research; leave the rest as honest gaps.

## Phased plan

1. **Define the shape** (this doc) — agree the sections and principles. *(you are here)*
2. **Stand up `context/`** with section templates + the provenance/gaps convention.
3. **Populate the load-bearing four** from real inputs — Vision (leadership), Personas (finish
   the 2 pending + Orbit-client research), Tech reality (engineering), Domain (domain experts).
   Do **not** fabricate these; where input is missing, record it as a known gap.
4. **Build `distill-context`** once there are real inputs to run it on and validate against.
5. **Connect to Claude** (Project knowledge first, MCP later) and re-run `/explore` on the
   Commentary pack to measure how much sharper it gets with real context vs. today's assumptions.

## What this is not

- Not a design-system change — no tokens, components, or platform-truth edits.
- Not orchestration — it is *content* the Explore capability consumes.
- Not a replacement for human judgment — it grounds framing; a person still owns the bet.

<!-- graph-links:start — generated by tools/gen_graph_links.py; do not hand-edit -->
## Vault graph
[[_review/cp-personas-WIP|cp-personas-WIP]]
<!-- graph-links:end -->
