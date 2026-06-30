---
type: visual-truth-note
status: in-review
owner: design-system
surfaces: [Orbit, Client Connected Platform]
platform: orbit-client-connected-platform
source: user-provided
last_reviewed: 2026-06-15
maturity_score: 65
tags: [orbit, design-brain, visual-truth, client-connected-platform]
---

# Orbit / Client Connected Platform Visual Truth

This note extracts working design guidance from the current Orbit / Client Connected
Platform screenshot manifest. The screenshots are in-review and restricted until
design-system owners approve sanitization, but they are still useful as directional
platform evidence.

Primary screenshot manifest:
`design-brain/examples/screenshots/orbit-client-connected-platform/manifest.md`

## What Orbit / Client Connected Platform Is

Orbit / Client Connected Platform is the external client-facing surface. It is for
client procurement, category, sourcing, legal, and stakeholder teams using Efficio
workflows.

The visual tone should feel guided, trustworthy, polished, and client-safe while still
supporting enterprise density. It should explain context and next steps more clearly
than internal Connected Platform screens.

## Screenshot Evidence

Use these as in-review visual truth candidates:

- `orbit-client-home-ai-tools-dashboard.png`
- `orbit-client-sourcing-execution-tool-hub.png`
- `orbit-client-marketiq-intro-get-started.png`
- `orbit-client-marketiq-select-initiative.png`
- `orbit-client-marketiq-select-initiative-modal.png`
- `orbit-client-marketiq-research-parameters-generate.png`
- `orbit-client-marketiq-research-output-next-actions.png`
- `orbit-client-delivery-engine-initiative-detail-tool-coverage.png`

Reference-only:

- `orbit-client-procurement-technology-landscape-diagram.png`

## Shell And Navigation

- Use the current client shell as the visual precedent: persistent navigation, clear
  product area, and a focused work surface.
- The shell can remain dense, but the page content should provide more guidance than
  internal Connected Platform screens.
- Active product areas and selected work should be obvious without exposing unnecessary
  internal process detail.
- Avoid copying Connected Platform-only operational shortcuts unless the screenshot or
  source proves clients see them.

## Density

- Preserve enterprise density, especially in tool hubs, initiative lists, and detail
  views.
- Give client-facing workflows more breathing room around explanation, selected context,
  and primary actions than internal CP screens.
- Use compact density for tables and modals when the data requires it, but avoid making
  client-facing screens feel like internal admin tools.
- Keep page width and central content columns purposeful in guided tool flows.

## Card Usage

- Cards should guide a user through tools, selected initiative context, generated output,
  next actions, and initiative tool coverage.
- Client-facing cards should make purpose and next action explicit.
- Use summary cards to explain what a tool does before asking the user to act.
- Avoid generic SaaS feature cards. Cards should map to real products, initiatives,
  reports, next actions, or evidence.
- A card grid is acceptable when it helps compare tools or next actions, but each card
  needs a concrete action or status.

## Table And List Behavior

- Client-facing tables and lists should keep row identity, search, tabs, ownership, and
  selection clear.
- In modal tables, keep the table focused on the decision the user is making. Search and
  tabs should reduce choice, not add ceremony.
- Use client-safe metadata labels. Avoid exposing internal-only process language unless
  it is present in the client platform.
- Selected initiative context should remain visible after the user leaves the modal.
- Row actions should be explicit; avoid hidden affordances that require internal
  training.

## Modal And Workflow Behavior

- Client modals should have clear titles, close/cancel paths, and focused table/list
  content.
- Guided workflows should show selected context, research parameters, generated states,
  download/report actions, and next actions.
- Success and completion states should be visible and reassuring without pretending work
  completed instantly.
- Use toasts and generated-state labels only when they clarify real state.

## Dashboard And Tool Treatment

- The client home dashboard should foreground available tools, performance summary, and
  initiative summary without becoming a marketing landing page.
- Tool hubs should present real product choices: MarketIQ, RFP Builder, RFP Analytics,
  ClauseIQ, or other source-backed tools.
- Tool detail screens should explain what the tool does, what context is selected, and
  what the user can do next.
- Initiative detail pages may use tabs, status controls, key tool coverage cards, and
  actions, but should stay client-safe and review-oriented.

## Copy Tone

- Use client-safe language. Do not expose internal shorthand unless it is visibly present
  in product source.
- Explain state and next steps plainly: selected initiative, research parameters,
  generated report, save/download, run again, update milestone.
- Permission and RBAC copy should say what the user can do and who can help without
  revealing internal operations.
- Avoid vague AI hype. Tie AI or generated outputs to concrete procurement tasks and
  evidence.

## Do

- Identify the platform as Orbit / Client Connected Platform before designing.
- Use the Orbit screenshot manifest before inventing client shell, tool hub, guided
  workflow, or results patterns.
- Keep client next actions explicit and understandable.
- Preserve selected context across workflow steps.
- Use client-safe copy and visible status.

## Do Not

- Do not import Connected Platform operational density without client guidance.
- Do not expose internal-only labels, controls, or process shortcuts unless product
  source proves clients see them.
- Do not use benchmark/docs screenshots as Orbit visual precedent.
- Do not use the procurement technology landscape diagram as UI layout precedent.
- Do not turn client tool screens into generic landing pages or promotional feature
  grids.

## Current Gaps

- Screenshots still need sanitization and approval.
- Client-facing form validation, error, empty, loading, and permission-denied states are
  still underrepresented.
- RFP Analytics and KPI/dashboard examples need stronger production references.
- Platform-specific pattern contracts still need links back to this visual truth note.
