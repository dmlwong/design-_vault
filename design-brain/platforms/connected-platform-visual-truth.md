---
type: visual-truth-note
status: in-review
owner: design-system
surfaces: [Connected Platform]
platform: connected-platform
source: user-provided
last_reviewed: 2026-06-15
maturity_score: 65
tags: [orbit, design-brain, visual-truth, connected-platform]
---

# Connected Platform Visual Truth

This note extracts working design guidance from the current Connected Platform
screenshot manifest. The screenshots are in-review and restricted until design-system
owners approve sanitization, but they are still useful as directional platform evidence.

Primary screenshot manifest:
`design-brain/examples/screenshots/connected-platform/manifest.md`

## What Connected Platform Is

Connected Platform is the internal Efficio operating surface. It is for consultants,
operators, delivery teams, and administrators who need speed, density, and direct access
to operational controls.

The visual tone should feel practical, compact, and work-focused. It may expose more
metadata, controls, and internal process language than external Orbit screens.

## Screenshot Evidence

Use these as in-review visual truth candidates:

- `connected-platform-home-shell-dashboard.png`
- `connected-platform-project-actions-workspace.png`
- `connected-platform-projects-initiatives-client-overview.png`
- `connected-platform-initiative-list-team-view.png`
- `connected-platform-initiative-workspace-timeline-detail.png`
- `connected-platform-clauseiq-contract-wizard-modal.png`
- `connected-platform-supplier-discovery-cards.png`
- `connected-platform-supplier-tracker-table.png`

Supporting reference only:

- `connected-platform-home-shell-dashboard-dock-visible.png`

## Shell And Navigation

- Use a persistent left navigation shell with compact labels, section grouping, and
  quick access to active work.
- Keep navigation dense enough for internal power users; avoid oversized marketing-style
  nav blocks.
- Active sections should be visibly anchored without overpowering the work surface.
- The work area should prioritize task content, not empty page framing.
- Do not copy browser chrome, OS dock, or screenshot capture artifacts into design
  guidance.

## Density

- Default to comfortable density, but keep internal pages closer to compact enterprise
  rhythm than client-facing Orbit.
- Tables, lists, project cards, tracker views, and dashboard regions should support high
  scan density.
- Use whitespace to separate regions, not to create a sparse consumer SaaS feel.
- Favor stable row heights, compact metadata, and grouped controls over large empty
  panels.

## Card Usage

- Cards are functional containers for work units: project summaries, milestones,
  suppliers, pinned content, tool coverage, and insight modules.
- Card content can be metadata-heavy when it supports operational scanning.
- Card headers should make the object clear: project, initiative, supplier, milestone,
  tool, or insight.
- Avoid decorative card grids that do not expose status, owner, next action, or evidence.
- Right-side support regions, such as AI insight rails, should assist the primary
  workflow rather than becoming promotional panels.

## Table And List Behavior

- Internal lists may carry many controls: tabs, filters, search, bulk import, row status,
  owners, avatars, and row-level actions.
- Preserve row identity and status at a glance. Status controls should remain close to
  the row or object they affect.
- Use pagination or stable list controls when the dataset is long.
- Dense internal tables should still keep keyboard focus, visible focus rings, readable
  hit targets, and non-color-only status indicators.
- Do not replace table/list contracts with custom clickable div rows when Orbit table
  components cover the use case.

## Modal And Wizard Behavior

- Internal modals may be large when the task requires multi-step setup or document
  upload.
- Use direct labels, clear step indicators, and explicit primary/secondary actions.
- Preserve cancel/close escape routes.
- Keep wizard progress visible and concrete; do not turn an internal task modal into a
  marketing-style explainer.

## Dashboard And Workspace Treatment

- Home and workspace views should show current work, actions, milestones, useful links,
  and operational signals.
- Dashboard cards should answer "what needs attention?" and "what can I do next?"
  before decorative summary.
- Initiative detail pages can combine tabs, summary metadata, timeline cards,
  accordions, and insight panels.
- Operational dashboards should favor drill-down and recovery paths over client-facing
  reassurance.

## Copy Tone

- Internal Efficio terminology is allowed when it matches the product source.
- Labels should be short and operational: `Project Actions`, `Bulk Import`, `Status`,
  `Owner`, `My Supplier Tracker`.
- Permission and error copy may reference internal roles or process state when safe.
- Avoid client-safe over-explanation when the internal user needs speed.

## Do

- Identify the platform as Connected Platform before designing.
- Use the Connected Platform manifest before inventing shell, workspace, list, or modal
  patterns.
- Keep controls and metadata close to the object they affect.
- Support compact density for internal queues, trackers, and tables.
- Preserve internal workflow language when source proves it is real.

## Do Not

- Do not borrow Orbit / Client Connected Platform polish when it hides internal controls.
- Do not simplify dense internal workflows into sparse landing-page layouts.
- Do not use benchmark/docs screenshots as Connected Platform visual precedent.
- Do not use the dock-visible screenshot as primary precedent.
- Do not invent client-facing copy for internal operational views.

## Current Gaps

- Screenshots still need sanitization and approval.
- Settings/admin screens are still missing.
- Error, empty, loading, and permission-denied states are still underrepresented.
- Platform-specific pattern contracts still need links back to this visual truth note.
