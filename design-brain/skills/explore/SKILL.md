---
name: explore
description: Turn a stakeholder concept pack, problem statement, or discovery brief into an explorable, interactive concept prototype a design/product team can test and iterate on — fast, and NOT bound to the Orbit design system. Use at the START of a delivery cycle (the Concept Commitment gate), when the input is a *problem to explore* rather than a component or screen to build to spec. Triggers on: "explore this concept pack", "prototype a feature from this brief", "turn this problem statement into something we can test", "concept for <initiative>". This is the divergence capability — it deliberately does not use Orbit components and does not enforce design-system fidelity. When the goal is instead to make something Orbit-correct or production-leaning, use `port-to-orbit` / `component-contract` instead.
---

# Explore — concept packs into testable interactive prototypes

This skill produces a **fast, explorable, interactive concept** from a problem — the upstream
half of the design funnel. It is the opposite of the vault's port/govern skills:

| | This skill (Explore / diverge) | port-to-orbit, component-contract (Port / converge) |
| - | - | - |
| Stage | Early — Concept Commitment | Late — Build Readiness |
| Goal | *Is this the right feature?* | *Make it real and on-system* |
| Components | **Whatever serves the idea (not Orbit)** | Orbit only, tokens-only |
| Success | It's clickable and tests the bet | It matches the design system |
| Delivery | A running, clickable prototype | Production-leaning code |

A winning concept from this skill later flows *into* the Port funnel to become real. Do not
try to do both at once — Orbit fidelity is a distraction while exploring.

## The method (four steps — do them in order)

### 1. Frame first — never jump to screens
The failure mode is composing screens before deciding what the feature *is*. So:
- Read the concept pack **and** whatever Efficio context exists (platform profiles, personas,
  principles, prior discovery packs, product surfaces). Pull it; don't invent it.
- Produce a **concept brief**, short and sharp:
  - **User** — one primary user, one situation.
  - **The one bet** — the single core flow to prototype. **Pick the highest-*evidence* bet,
    not the most demo-able one.** A concept pack usually lists many journeys; choose one.
  - **Value hypothesis** — the "if… then…" this concept tests.
  - **Deliberately out of scope** — name what you are *not* building and why.
  - **Flagged assumptions** — everything you had to assume, *especially where Efficio context
    is missing* (product vision, tech reality/feasibility, real personas, what the system
    records today). These are as important as the concept.
- **Present the brief and let the human steer before you build.** The human owns the bet.
  Do not silently resolve a fork the pack itself leaves open.

### 2. Generate a genuinely interactive prototype
- Build a **self-contained, fully interactive artifact**: HTML + inline CSS + vanilla JS with
  real state. No external/CDN dependencies (CSP-safe), no framework runtime required.
- **Interactivity is the definition of done.** Primary CTAs must *do things*: add flows into a
  list, filters filter, a status change lands in an audit trail, a generated view composes
  from live state. Build one coherent end-to-end flow with a clear "aha" moment.
- **Not Orbit-bound.** Choose the palette, type, and layout that best serve *this* idea and the
  Efficio domain (procurement, B2B, dense, professional). Real content throughout — no lorem.
  Design light and dark. (Follow the `artifact-design` skill for craft.)
- **Deliver it running, as an Artifact.** Never deliver screenshots as the artifact — a
  designer must be able to click it. A snapshot is a fallback, never the goal.

### 3. Verify it actually works
- Drive the prototype headless (Playwright against the local file) before delivering: confirm
  the primary CTAs do what they claim, the core flow completes, and the console is clean.
- Interactivity and flow-completion are what you verify — not visual conformance.

### 4. Critique it — a blind, adversarial product pass
- Pressure-test the *concept*, not the code. Ideally in a **fresh context** (a concept-critic
  should not grade its own framing). Attack: the value hypothesis, each assumption, workflow
  fit, whether the chosen bet is really the highest-value one, edge cases, adoption risk.
- Order findings by what could **kill** it. End with the 2–3 things a real user session must
  answer, and the assumptions that need validation.

### 5. Archive it durably — delivery is not evidence
- **Copy the exact delivered file** to `discovery/prototypes/<slug>/prototype.html`, and write
  a record beside it from `discovery/prototypes/_TEMPLATE-record.md` — its `brief:` key points
  at the brief this came from, which is what lights the concept's *Explored* stage on Vault
  Health. Then regenerate the graph links with `tools/gen_graph_links.py`.
- Record the **provenance** honestly (original build, or a labelled reconstruction) and what
  you actually verified in step 3 — including anything you skipped.
- This exists because it was learned the hard way: the 2026-07-21 status-prep prototype was
  delivered as a session-private Artifact and is unrecoverable. A link expires; the record
  does not. The `.html` stays vault-only (withheld from product-repo export); the record travels.

## Report — and feed the context gaps back
Deliver, together: the **brief**, the **running prototype link**, the **critique**, and a list
of the **context gaps** that forced assumptions. Those gaps are the highest-value output — they
are the backlog for the *Efficio context pack* that makes the next concept sharper.
**Optionally, emit a Lovable seed prompt** — the grounded brief plus platform/domain context
distilled into a prompt a stakeholder can paste into Lovable to keep iterating there from
grounded context instead of a blank canvas. It is a *projection* of the brief, not a second
source of truth (same relationship as `design-brain/lovable/knowledge-base.md`). Then offer:
iterate the bet, re-frame around a different bet, or hand a winner to the Port funnel.

## Non-negotiables
- **Frame before you build.** A concept brief precedes any prototype.
- **Interactive, delivered running.** Screenshots are never the deliverable.
- **Archived, not just delivered.** An Artifact link with no `discovery/prototypes/` record is
  an incomplete run — the prototype is a Concept Pack deliverable, and deliverables are files.
- **Not Orbit-bound.** Speed and explorability beat fidelity at this stage.
- **The human steers the bet.** Do not auto-decide the concept is "done" — present, and let a
  person choose, redirect, or kill it.
- **Flag every assumption and context gap.** Honesty about what you invented is part of the output.

## Scope — deliberately outside the Orbit Definition of Done
An explore prototype is a **throwaway concept, not a generated Orbit prototype**: the
`AGENTS.md` §5 checklist — including the §2.8 `<OrbitInspector />` mount — does not
apply to it and must not be scored against it. Those rules attach at the port, when the
concept enters the Orbit funnel. A reviewer asked to look at an explore artifact judges
the *concept and its interactivity*, nothing else.

"Throwaway" means *with respect to the design system* — the code is never ported as code. It
is never throwaway as **evidence**: step 5 archives it because it is the Concept Pack
deliverable that proves the concept's value.

## Handoff
- A concept the team wants to take forward → the **Port/Govern** funnel (`port-to-orbit` /
  `component-contract`) to become Orbit-correct and production-leaning. Tell the porter
  what it is receiving: **plain HTML/CSS/vanilla-JS with no framework** — the port maps
  behaviour and layout intent onto Orbit components, not markup onto markup
  (`design-brain/skills/port-to-orbit/SKILL.md`, workflow step 0).
- Context gaps surfaced → the Efficio context pack / vault backlog.

## Invocation
`/explore <concept-pack or problem statement>`. If no Efficio context is attached, say what
context you're missing and proceed on flagged assumptions rather than stalling.

<!-- graph-links:start — generated by tools/gen_graph_links.py; do not hand-edit -->
## Vault graph
[[AGENTS|AGENTS]] · [[design-brain/lovable/knowledge-base|knowledge-base]] · [[design-brain/skills/port-to-orbit/SKILL|port-to-orbit SKILL]] · [[discovery/prototypes/_TEMPLATE-record|_TEMPLATE-record]]
<!-- graph-links:end -->
