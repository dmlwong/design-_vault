---
type: pattern-contract
status: in-review
owner: design-system
surfaces: [Connected Platform, Orbit, Client Connected Platform]
platform: shared
source: user-provided
last_reviewed: 2026-06-15
maturity_score: 66
tags: [orbit, design-brain, pattern-contract, visual-truth]
---

# Pattern Contract: `list-detail`

## Purpose & Precedent
Let users scan many entities and inspect or edit one item without losing list context.

Screenshot-backed precedent now exists for:

- Connected Platform initiative list:
  `design-brain/examples/connected-platform-initiative-list-table.md`
- Connected Platform supplier tracker:
  `design-brain/examples/connected-platform-supplier-tracker-table.md`
- Orbit / Client Connected Platform initiative detail:
  `design-brain/examples/orbit-client-delivery-engine-initiative-detail.md`

These examples are in-review and restricted until design-system owners approve
sanitization.

## When To Use / When Not To
Use for entities like initiatives, suppliers, clauses, projects, requests, or analyses
where the user needs to move between a collection and an item or workspace.

Do not use when the primary task is pure bulk comparison with no selected-item detail,
or when the user is choosing a tool rather than inspecting entities.

## Regions & Composition
List/table region, filters/search, tabs where source-backed, selected-state detail
drawer/panel or detail page, row actions, status controls, global actions, and optional
tool coverage or related-content cards.

Component contracts: `data-table`, future `drawer` or existing `dialog` where detail is
modal, `button`, `badge-status`, `tabs`, `card-panel`, `select-combobox`, `input`.

Connected Platform examples favor dense list/table controls: filters, tabs, bulk import,
status controls, owner metadata, and row actions.

Orbit / Client Connected Platform examples favor selected initiative context, tabs,
status controls, and tool coverage cards with explicit client-safe actions.

## Hierarchy & Density
List first, selected entity detail second. Compact density is required for long lists.
Connected Platform may expose more controls and metadata in the list. Orbit should keep
client-facing selected context and next actions clear.

## Page-Level States
Initial skeleton, no items, no selected item, selected item loading, detail error, stale
list, permission-limited actions, empty filter result, partial tool coverage, and failed
row action.

## Navigation & Focus Behaviour
Selecting a row updates detail or navigates to the detail page. Closing a detail panel or
dialog returns focus to the selected row. If selection navigates to a detail page, the
page heading must identify the selected entity and preserve a route back to the list.

## Responsive Behaviour
Detail becomes a full-screen or stacked region on narrow screens. Tables may scroll
inside their own region, but filters, tabs, search, and primary actions must not clip.

## Data & Performance Notes
Use stable selection identity across refreshes. Avoid clearing selected state on minor
data updates unless the entity disappears. Use pagination or server-side filtering for
large datasets unless a virtual-table contract exists.

## Anti-Patterns
- Losing list position after editing.
- Opening every detail in a modal that blocks comparison.
- Replacing dense internal CP tables with decorative cards.
- Exposing CP internal labels in Orbit client list/detail screens.
- Hiding status or owner metadata when it drives the next action.
- Clearing selected context after refresh.

## Golden Examples
- `design-brain/examples/connected-platform-initiative-list-table.md`
- `design-brain/examples/connected-platform-supplier-tracker-table.md`
- `design-brain/examples/orbit-client-delivery-engine-initiative-detail.md`

## Gap Report
- Screenshot sanitization and design-system approval are still needed.
- A reusable drawer/detail-panel source is still missing.
- Empty, loading, error, and permission states need platform screenshots.
