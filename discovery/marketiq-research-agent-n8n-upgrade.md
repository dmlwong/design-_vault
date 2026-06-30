---
type: discovery-pack
status: draft            # draft → active → shipped → archived
owner: Research Team / CP Team
platform: both
initiative: MarketIQ Research Agent — n8n upgrade
epic: https://efficio.atlassian.net/browse/CP-11165
ai_designs: N/A
sprint: 2026-03-18
surfaces: [MarketIQ]
source: product
last_reviewed: 2026-06-17
linked_patterns: [guided-conversational-workflow, review-and-approve-workflow]
linked_components: [card-panel, button]
tags: [orbit, discovery]
---

# Discovery: MarketIQ Research Agent — n8n upgrade

> Distilled from the 4D Concept Discovery Pack (`2026-03-18_Research Agent n8n upgrade_1.
> Discover.docx`). Word doc remains the human source of truth. Stakeholder list,
> recommended-tools, and disclaimer intentionally dropped.

## Design surface — read first
- **Platform(s):** CP **and** CCP — **prioritise CCP** (per open-question resolution).
- **Front-end in scope:** **Limited.** Output formatting restructured closer to the
  Efficio format, plus accommodating (a slot for) chatbot functionality. This sprint is
  mostly a **backend migration**, not a UI build.
- **Out of UI scope:** commodity data, charts, or graph-heavy outputs; the interactive
  co-pilot/chatbot itself.
- **States to design:** for any front-end change, cover loading/empty/error/success of the
  generated primer; most interactive states are **not applicable** this sprint (chatbot is
  accommodated, not built).

## Reference designs & visual truth
- **N/A this sprint** — no AI designs/prototype or current-state screenshots in the source
  doc (it noted "AI Designs: N/A"). Mostly a backend migration.

## Executive summary
- **What:** Move the MarketIQ research agent to an n8n agent. It currently needs manual
  intervention for any upgrade.
- **Why:** Manual upgrades create tech debt; n8n lets the primer reports be updated
  without CP development effort.
- **How (near-term):** Migrate the knowledge layer from a static vector store to a
  knowledge graph; connect via an n8n workflow/webhook; reconnect CP/CCP so defined
  initiative inputs are sent and a generated primer is returned.
- **Success:** Update and upgrade primer reports without needing CP development effort.
- **Constraints:** Scope may exceed one sprint; front-end effort is deliberately limited
  this sprint.

## Problem statements
- Users need external market insights at category, commodity, sector, country and client-
  industry levels to support sourcing/procurement decisions.
- The current experience is largely report/primer-led; the team wants a more dynamic,
  interactive experience.
- The static/vector knowledge base creates maintenance and dependency constraints; the
  proposed direction is a knowledge graph.
- CP/CCP integration needs defined initiative inputs and a connector/webhook approach
  rather than direct agent-code integration.
- Scope may exceed one sprint, so sizing and prioritisation are needed.

## Goals & success criteria (by priority)
**In scope**
- Migrate research agent from vector store to knowledge graph — **Success:** MarketIQ
  reads from the knowledge graph, reducing dependency on CP backend changes.
- Enable CP/CCP integration via n8n agent/webhook — **Success:** CP/CCP sends defined
  inputs; n8n runs, generates the primer, and returns it to the platform.
- Expand initiative inputs — **Success:** at minimum ingest client industry and support
  multi-country input; review other available parameters.
- Improve/prepare the front-end — **Success:** output restructured closer to the Efficio
  format; UI changes limited apart from accommodating chatbot functionality.

**Out of scope** *(do NOT build this sprint)*
- Phase 1 research co-pilot/chatbot capability (answer questions from the knowledge graph).
- Phase 2 expanded chatbot (consolidate supplier-finder + commodity-price-watch use cases).

## User journeys
**In scope**
- **Journey A — n8n integration:** As the Research team, we want to update the research
  agent without depending on the CP dev team.

**Out of scope**
- **Journey B — Interactive report:** As a user, I want to interrogate the report (ask for
  summaries or more detail on areas).
- **Journey C — Feedback widget:** As a user, I want to give feedback on the report.

## Prior decisions & rejected alternatives
- **Decided:** knowledge graph over the static vector store — *why:* the vector store
  creates maintenance and dependency constraints.
- **Decided:** n8n connector/webhook over direct agent-code integration — *why:* lets the
  agent be updated without CP backend changes.
- **Decided:** prioritise CCP over CP.
- **Ruled out (this sprint):** building the Phase 1 chatbot — *only accommodating* its
  future inclusion, not implementing it.
- **Ruled out (this sprint):** commodity data and charts — not required for the
  knowledge-base change; can be handled by the n8n agent later.

## Concept summary table
| Goal | Metric / target | Owner | Target date | Status |
| ---- | --------------- | ----- | ----------- | ------ |
| Migrate KB to knowledge graph | No longer reads from current vector DB | Research Team | Jul 8 | Priority discussed |
| Integrate via n8n / webhook | CP/CCP sends inputs; n8n generates & returns primer | CP Team | Jul 22 | To be sized |
| Add initiative inputs | Client industry + multi-country; review other params | CP Team | Jul 22 | To be planned |
| Front-end formatting | Output closer to Efficio format | Research Team | Jul 22 | Scheduled pre-July sprint |

## Linked design (bridge to the brain)
- **Platform profile + personas:** `design-brain/platforms/orbit-client-connected-platform.md`
  (CCP priority) and `design-brain/platforms/connected-platform.md`.
- **Pattern(s):** `design-brain/patterns/guided-conversational-workflow.md`,
  `design-brain/patterns/review-and-approve-workflow.md` (generated output + next actions).
  `[CONFIRM]` once the front-end scope is firmed up.
- **Component(s):** `design-brain/components/card-panel.md`, `button.md`.
- **Defaults:** `design-brain/defaults.md`.

## Delivery context (pre-fills the HAND OVER package — Part D)
- **Assumptions:** front-end changes are limited this sprint; the chatbot is accommodated,
  not built; output reformatting toward the Efficio format is the main visible change.
- **Dependencies & technical constraints:** migration to the knowledge graph; n8n
  always-running workflow + webhook; CP/CCP must send defined initiative inputs and receive
  the generated primer; significant research-side code changes expected for new params;
  handover/output format undefined (PDF / HTML / JSON); review how the knowledge navigator
  interacts with n8n as a precedent; commodity pricing = third-party processing, not
  internal benchmarking data.
- **Risks:** implementing the integration for both CP and CCP may consume the full sprint;
  sizing still unknown.
- **Open questions / outstanding decisions:**
  - What fits the July sprint vs. needs another sprint? → **OPEN** (sizing).
  - Which input params beyond client industry + multi-country? → **OPEN.**
  - CP/CCP integration effort? → no front-end changes; backend effort **OPEN.**
  - Prioritise CP or CCP? → **CCP.**
  - Handover/output format? → **OPEN** (PDF / HTML / JSON).
  - Front-end improvement target date? → **8 July.**
  - Success metric? → no CP dev required to update the research agent in future.

## Future vision (context only — do not build)
- MarketIQ evolves from static primer into a dynamic product with an interactive research
  co-pilot over the knowledge graph; insights augment Strategy Reviewer / Advisor /
  Builder; later phases may consolidate Supplier Finder + Commodity Price Watch chatbots.

## Status & owner
- **Status:** draft
- **Owner:** Research Team / CP Team
- **Last reviewed:** 2026-06-17
