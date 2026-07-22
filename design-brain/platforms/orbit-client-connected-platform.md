---
type: platform-profile
status: in-review
owner: design-system
surfaces: [Orbit, Client Connected Platform]
platform: orbit-client-connected-platform
source: specified
last_reviewed: 2026-06-15
maturity_score: 60
context_tier: task-core
load_when: [build-component, build-screen, port-prototype, platform-question]
tags: [orbit, design-brain, platform, client-connected-platform]
---

# Platform Profile: Orbit / Client Connected Platform

## Audience

External client users: procurement, category, sourcing, legal, and stakeholder teams
using client-facing Efficio workflows.

## Product Intent

Orbit / Client Connected Platform should feel client-safe, guided, trustworthy, and
polished while preserving enterprise density. It needs clearer context, safer copy, and
more explicit permission/review states than internal-only tooling.

## Visual Truth

User-provided screenshots are now listed in the manifest and are the first Orbit /
Client Connected Platform visual truth candidates. Treat them as restricted until
design-system owners confirm sanitization and approval. Do not treat docs benchmark
screenshots as Orbit / Client Connected Platform visual precedent.

Screenshot manifest:
`design-brain/examples/screenshots/orbit-client-connected-platform/manifest.md`

Visual truth extraction note:
`design-brain/platforms/orbit-client-connected-platform-visual-truth.md`

When designing or reviewing an Orbit / Client Connected Platform screen, read the visual
truth note before applying page-level layout, density, shell, table/list, modal,
dashboard, tool-hub, workflow, or copy patterns.

## Copy Rules

- Use client-safe language. Avoid internal Efficio shorthand unless product source
  proves the client sees it.
- Explain state, next action, and recovery clearly.
- Permission/RBAC copy should be respectful and action-oriented, not operationally
  revealing.

## Pattern Preferences

- Shell/navigation: use current client platform screenshots or source before composing
  new shell patterns.
- Density: keep tables and dashboards scannable, but favor clearer grouping and guidance
  than internal CP screens.
- Tables/list-detail: preserve context and review confidence; row actions must be
  explicit and client-safe.
- Dashboards/KPIs: pair summary metrics with accessible explanation and underlying rows.
- RBAC/permissions: state what the user can do and who can help without leaking internal
  operations.

## Golden Examples

Read the nearest platform-matched example before creating or reviewing an Orbit / Client
Connected Platform screen:

- `design-brain/examples/orbit-client-home-ai-tools-dashboard.md`
- `design-brain/examples/orbit-client-sourcing-execution-tool-hub.md`
- `design-brain/examples/orbit-client-marketiq-guided-workflow.md`
- `design-brain/examples/orbit-client-marketiq-research-output-next-actions.md`
- `design-brain/examples/orbit-client-delivery-engine-initiative-detail.md`

## Relevant Pattern Contracts

- Home/dashboard surfaces: `design-brain/patterns/home-dashboard.md`
- Tool selection hubs: `design-brain/patterns/tool-hub.md`
- Guided AI-assisted workflows: `design-brain/patterns/guided-conversational-workflow.md`
- Initiative detail/workspace screens: `design-brain/patterns/list-detail.md`
- Analytics/KPI views: `design-brain/patterns/analytics-dashboard.md`
- Generated output and next actions: `design-brain/patterns/review-and-approve-workflow.md`

## Difference From Connected Platform

- Orbit / Client Connected Platform needs clearer guidance, safer copy, and more visible
  selected context than internal CP.
- Orbit should not inherit CP's internal shorthand, operational shortcuts, or dense
  controls unless source proves clients see them.
- Orbit screens may still be data-dense, but they should preserve client confidence,
  review clarity, and explicit next actions.

## Audience & Personas

Read before designing. Write each persona as **trait → design consequence**. If a line
does not end in a design consequence, cut it. These are external client users.

> **Provisional drafts `[CONFIRM]`** — inferred from the audience definition in `AGENTS.md`
> and the Orbit / Client Connected Platform screenshot pack. Replace with real research;
> correct names, roles, and traits before promoting to `stable`.

- **Client Category / Procurement Manager** `[CONFIRM]`
  - Less familiar with Efficio internal process → clearer guidance, explicit next actions,
    client-safe copy; avoid internal shorthand.
  - Acts on AI-generated research/outputs → explainable results next to underlying data,
    visible parameters, save/download actions close to the output.
- **Client Stakeholder / Approver** `[CONFIRM]`
  - Reviews and signs off high-stakes outputs occasionally → visible state, review
    confidence, clear approve/reject with audit trail, minimal operational jargon.
  - Drops in between long gaps → preserved selected context, obvious "where am I / what's
    next", no assumption of prior-session memory.

## Known Gaps

- Screenshot sanitization and design-system approval are still needed.
- Client-facing form/error examples are still needed.
- Platform-specific pattern contracts still need to be connected to the approved visual
  truth set.

<!-- graph-links:start — generated by tools/gen_graph_links.py; do not hand-edit -->
## Vault graph
[[AGENTS|AGENTS]] · [[design-brain/examples/orbit-client-delivery-engine-initiative-detail|orbit-client-delivery-engine-initiative-detail]] · [[design-brain/examples/orbit-client-home-ai-tools-dashboard|orbit-client-home-ai-tools-dashboard]] · [[design-brain/examples/orbit-client-marketiq-guided-workflow|orbit-client-marketiq-guided-workflow]] · [[design-brain/examples/orbit-client-marketiq-research-output-next-actions|orbit-client-marketiq-research-output-next-actions]] · [[design-brain/examples/orbit-client-sourcing-execution-tool-hub|orbit-client-sourcing-execution-tool-hub]] · [[design-brain/examples/screenshots/orbit-client-connected-platform/manifest|orbit-client-connected-platform manifest]] · [[design-brain/patterns/analytics-dashboard|analytics-dashboard]] · [[design-brain/patterns/guided-conversational-workflow|guided-conversational-workflow]] · [[design-brain/patterns/home-dashboard|home-dashboard]] · [[design-brain/patterns/list-detail|list-detail]] · [[design-brain/patterns/review-and-approve-workflow|review-and-approve-workflow]] · [[design-brain/patterns/tool-hub|tool-hub]] · [[design-brain/platforms/orbit-client-connected-platform-visual-truth|orbit-client-connected-platform-visual-truth]]
<!-- graph-links:end -->
