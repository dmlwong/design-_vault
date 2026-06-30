---
type: component-contract
status: in-review
owner: design-system
surfaces: [shared]
source: code
last_reviewed: 2026-06-19
maturity_score: 72
tags: [orbit, design-brain, component-contract]
---

# Component Contract: `status-indicator`

## Purpose
Use `StatusIndicator` for compact inline status shown as a coloured dot with an optional
text label — e.g. a row's state in a list, a tool-coverage item, or a queue entry. It is
presentational and non-interactive. For a filled status/classification chip, use
`badge-status` instead (see "Badge vs StatusIndicator" in that contract).

## Source Links
- Component source:
  `packages/orbit/src/indicators/StatusIndicator.tsx`
- Styles:
  `packages/orbit/src/indicators/StatusIndicator.module.css`
- (No dedicated test file in source.)

## Anatomy
Inline `span` container, a coloured dot (`aria-hidden`), and an optional text label.

## Public API

| Prop | Type | Default | Required | Source |
| ---- | ---- | ------- | -------- | ------ |
| `status` | `'Success' \| 'Warning' \| 'Information' \| 'Error' \| 'No Status'` | none | yes | code |
| `size` | `'Small' \| 'Default'` | `'Default'` | no | code |
| `label` | `string` | none | no | code |
| `ariaLabel` | `string` | none | no | code |

Note: the status set is a **subset** of `Badge` — there is no Green/Red/Gray. Map product
statuses with the approved mappings in `badge-status.md`.

## Variants
- Status: `Success`, `Warning`, `Information`, `Error`, `No Status`.
- Size: `Default` (dot = `--orbit-space-base`), `Small` (dot = `--orbit-space-s`).
- Labelled (dot + text) or dot-only (relies on `ariaLabel`).

## States
No hover, focus, disabled, loading, or selected state — it is not interactive. Loading and
empty are owned by the surrounding row/list, not the indicator.

## Density
Token-driven: container gap and padding `--orbit-space-xs`; label `--orbit-text-sm`. Use
`Small` in dense tables/lists; `Default` otherwise.

## Themes
Works in `efficio` and `orbit` through token values only; the dot colour resolves through
`--orbit-color-status-high-bg-*` tokens.

## RBAC / Permissions
Do not expose restricted workflow state. If a user may not see a status, omit the indicator.

## Tokens Used
- `--orbit-space-xs`
- `--orbit-space-s`
- `--orbit-space-base`
- `--orbit-text-sm`
- `--orbit-text-body-leading`
- `--orbit-font-weight-medium`
- `--orbit-font-family-sans`
- `--orbit-color-text-primary`
- `--orbit-color-status-high-bg-success`
- `--orbit-color-status-high-bg-information`
- `--orbit-color-status-high-bg-warning`
- `--orbit-color-status-high-bg-error`
- `--orbit-color-status-high-bg-no-status`

## Accessibility
Never rely on the dot's colour alone. Always provide a `label` (preferred — visible text)
or an `ariaLabel`. With a `label`, the text carries the meaning; with no label, the
component exposes `role="img"` and an accessible name of `ariaLabel` (falling back to the
status word). In repeated rows, include row identity in the accessible name where the bare
status would be ambiguous.

## Motion
No motion in source; add none.

## Content / Copy
Short status words (e.g. "Completed", "Running"). Use the approved workflow mappings in
`badge-status.md`; define new product statuses in the relevant `discovery/` pack.

## Do / Don't
- Do pass a `label` (or `ariaLabel`) so status is never colour-only.
- Do use `Small` in dense lists/tables.
- Do use the approved status→value mappings in `badge-status.md`.
- Don't use `StatusIndicator` as a clickable control.
- Don't invent statuses outside the five supported values.

## Golden Example
`design-brain/examples/data-table-dense.md` (row/list status). A dedicated example is a gap.

## Status
in-review · Last updated: 2026-06-19 · Owner: design-system

## Gap Report
- No dedicated test file in source.
- No dedicated golden example yet.
