---
type: component-contract
status: in-review
owner: design-system
surfaces: [shared]
source: code
last_reviewed: 2026-06-19
maturity_score: 80
tags: [orbit, design-brain, component-contract]
---

# Component Contract: `badge-status`

## Purpose
Use badges for short inline status, count, or classification labels. Orbit's source
component is `Badge`; it is presentational and non-interactive.

## Source Links
- Component source:
  `packages/orbit/src/indicators/Badge.tsx`
- Styles:
  `packages/orbit/src/indicators/Badge.module.css`
- Tests:
  `packages/orbit/src/indicators/Badge.test.tsx`
- Page-header usage:
  `packages/orbit/src/navigation/PageHeader.tsx`

## Anatomy
Inline `span`, text label, background token, foreground token, optional accessible
label. The current badge has no icon slot and no count-specific variant; counts are
rendered by passing the count as `label`.

## Public API

| Prop | Type | Default | Required | Source |
| ---- | ---- | ------- | -------- | ------ |
| `label` | `string` | none | yes | code |
| `status` | `'Green' \| 'Red' \| 'Gray' \| 'Information' \| 'Warning' \| 'Success' \| 'Error' \| 'No Status'` | `'Green'` | no | code |
| `ariaLabel` | `string` | none | no | code |

## Variants
- `Green`
- `Red`
- `Gray`
- `Information`
- `Warning`
- `Success`
- `Error`
- `No Status`

The test suite explicitly covers `Information`, `Warning`, and `No Status`.

## States
Badge has no hover, focus, disabled, loading, or selected state because it is not
interactive. If a status action is needed, wrap the behavior in an appropriate
interactive component and keep the badge itself presentational.

## Density
Badge density is token-driven: `--orbit-space-xxs` vertical padding,
`--orbit-space-s` horizontal padding, `--orbit-text-xs`, and line-height `1`.
Do not shrink below the current text size in dense tables.

## Themes
Works in `efficio` and `orbit` through token values only. Status backgrounds and
foregrounds are CSS custom properties; do not replace them with literal colours.

## RBAC / Permissions
Do not expose restricted workflow state through a badge. If a user cannot see a
status, omit the badge or use approved neutral copy.

## Tokens Used
- `--orbit-badge-radius`
- `--orbit-space-xxs`
- `--orbit-space-s`
- `--orbit-text-xs`
- `--orbit-font-weight-regular`
- `--orbit-font-family-sans`
- `--orbit-color-bright-green`
- `--orbit-color-bright-orange`
- `--orbit-color-mid-gray`
- `--orbit-color-status-high-bg-success`
- `--orbit-color-status-high-bg-information`
- `--orbit-color-status-high-bg-warning`
- `--orbit-color-status-high-bg-error`
- `--orbit-color-status-high-bg-no-status`
- `--orbit-color-white`
- `--orbit-color-text-primary`

## Accessibility
Badge text must carry the meaning; never rely on colour alone. Use `ariaLabel` only
when the visible label is abbreviated or numeric and needs more context, such as
`ariaLabel="3 overdue items"`.

Green, red, gray, and success filled badges use `--orbit-color-text-primary` rather
than inverse white text where the rendered fills do not meet AA contrast with white.

## Motion
No motion is present in source and none should be added for ordinary badges.

## Content / Copy
Use stable product terms and short labels. Current implementation supports generic
status names, but product-specific workflow terms still need owner approval before
being treated as canonical.

## Badge vs StatusIndicator

Orbit has two status primitives — choose deliberately:

- **`Badge`** — a filled label pill. Use for a status/classification *chip* with text
  (tab counts, record classifications). Statuses: Green, Red, Gray, Information, Warning,
  Success, Error, No Status.
- **`StatusIndicator`** — a coloured **dot + optional label**. Use for compact inline
  row/list status (e.g. a tool-coverage row). Statuses: Success, Warning, Information,
  Error, No Status; sizes Small/Default. Source:
  `packages/orbit/src/indicators/StatusIndicator.tsx`.

- **`Chip`** — a tag / filter / scope label (selectable or removable), **not** a status. Use
  it for category / country / filter tags. See `components/chip.md`.

Both must pair colour with text — give `StatusIndicator` a `label` (or `ariaLabel`), never
a bare dot.

## Approved workflow status mappings

Use these for recurring product workflow statuses instead of inventing one per screen (the
2026-06-19 stress test showed agents diverge here):

| Workflow status | Status value | Marker |
| --------------- | ------------ | ------ |
| Completed | `Success` | `[SOURCED]` both stress-test arms agreed |
| Running / In progress | `Information` | `[SOURCED]` both arms agreed |
| Failed / Needs action | `Error` | settled 2026-06-24 |
| Shared by client | `Information` (Badge) | settled 2026-06-24 (was `[CONFIRM]`; owner-approved) |

Define any other product-specific status in the relevant `discovery/` pack, not ad hoc.

## Do / Don't
- Do pass semantic status variants instead of hand-styling.
- Do keep labels short enough for table cells and tab headers.
- Do use `ariaLabel` for ambiguous numeric badges.
- Don't invent product status names without a source.
- Don't make badges clickable; use a button/link around the relevant action instead.

## Golden Example
`design-brain/examples/data-table-dense.md`

## Gap Report
- Product-specific status taxonomy: core mappings approved above (incl. `Shared by client`
  → Information and `Failed` → Error, settled 2026-06-24); new product states still need
  owner confirmation as they arise.
- `StatusIndicator` now has its own contract: `design-brain/components/status-indicator.md`.
- No icon badge or count-specific component exists in source.
