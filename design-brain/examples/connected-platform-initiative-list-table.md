---
type: example
status: in-review
owner: design-system
surfaces: [Connected Platform]
platform: connected-platform
source: user-provided
last_reviewed: 2026-06-15
maturity_score: 65
tags: [orbit, design-brain, example, visual-truth, connected-platform, table]
---

# Golden Example: Connected Platform Initiative List Table

## Demonstrates
- Dense internal list/table behavior.
- Filters, tabs, bulk action, status controls, owner metadata, and row actions.
- Connected Platform scan density for internal team workflows.

## Screenshot Evidence
- Primary screenshot:
  [connected-platform-initiative-list-team-view.png](screenshots/connected-platform/connected-platform-initiative-list-team-view.png)

Screenshot is in-review and restricted until design-system owners approve sanitization.

## Pattern Represented
Internal initiative list/table for Connected Platform.

Use this when creating or reviewing queues, initiative indexes, trackers, and internal
team lists where row identity, ownership, status, and actionability matter.

## Components Visible
- Table/list surface.
- Tabs.
- Filters and search.
- Bulk import/action entry point.
- Status controls.
- Owner avatars or initials.
- Row-level actions.

## Layout Guidance
- Place filtering and search close to the list they affect.
- Keep tabs, filters, and bulk actions visible without stealing space from row data.
- Preserve row identity: initiative name, category, owner, status, and next action should
  remain scannable together.
- Keep status controls near the affected row or object.

## Density Guidance
- Support compact mode for long lists.
- Use stable row heights and predictable column widths.
- Avoid large row cards when a true table/list is needed.

## Copy Guidance
- Internal labels may use operational team language.
- Keep button text short and action-led.
- Status labels should be specific enough for internal users to act without explanation.

## Imitate
- Dense row metadata.
- Tabs and filters close to the data.
- Ownership and status visibility.
- Recoverable row actions.

## Do Not Imitate
- Ad hoc clickable div rows when the Orbit `Table` contract applies.
- Client-facing over-explanation.
- Hidden row actions that require guesswork.
- Color-only status indicators.

## Review Questions
- Which list controls are source-backed component contracts versus screen-specific?
- Are status values and owner labels final?
- Which empty, loading, and permission states need additional screenshots?
