---
type: example
status: in-review
owner: design-system
surfaces: [Orbit, Client Connected Platform, Delivery Engine]
platform: orbit-client-connected-platform
source: user-provided
last_reviewed: 2026-06-15
maturity_score: 65
tags: [orbit, design-brain, example, visual-truth, client-connected-platform, delivery-engine]
---

# Golden Example: Orbit Client Delivery Engine Initiative Detail

## Demonstrates
- Client-facing initiative detail page.
- Tabs, status controls, initiative metadata, and tool coverage cards.
- Bridge between initiative management and tool workflows.

## Screenshot Evidence
- Primary screenshot:
  [orbit-client-delivery-engine-initiative-detail-tool-coverage.png](screenshots/orbit-client-connected-platform/orbit-client-delivery-engine-initiative-detail-tool-coverage.png)

Screenshot is in-review and restricted until design-system owners approve sanitization.

## Pattern Represented
Client initiative detail / project workspace.

Use this when creating or reviewing initiative detail screens, project workspaces, or
tool coverage summaries for external users.

## Components Visible
- Persistent shell/navigation.
- Page tabs.
- Initiative summary card.
- Status controls.
- Timeline/spend summary regions.
- Tool coverage cards.
- Content search region.
- Primary and secondary actions.

## Layout Guidance
- Keep initiative identity, status, and key metadata visible near the top.
- Use tabs to separate detail regions without losing page context.
- Tool coverage cards should show which tools are available, used, blocked, or ready to
  run.
- Keep client actions explicit and close to the relevant tool or region.

## Density Guidance
- Maintain enterprise density while keeping client review confidence.
- Cards can be dense if they expose status, usage, date, owner, and action.
- Avoid hiding tool availability behind abstract summaries.

## Copy Guidance
- Use client-safe initiative labels and action wording.
- Status copy should clarify what the client can do next.
- Avoid exposing internal-only operational terms unless visible in the source screen.

## Imitate
- Initiative metadata hierarchy.
- Tabbed detail organization.
- Tool coverage cards with concrete actions.
- Client-safe status and action labels.

## Do Not Imitate
- Internal CP admin tone.
- Tool cards without availability or next action.
- Losing selected initiative context.
- Overly sparse project pages that hide operational state.

## Review Questions
- Which initiative statuses are approved for client-facing display?
- Which tool coverage states need contracts?
- What are the permission-denied states for run, edit, upload, and close actions?
