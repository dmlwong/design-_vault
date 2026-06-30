---
type: component-contract
status: in-review
owner: design-system
surfaces: [shared]
source: code
last_reviewed: 2026-06-24
maturity_score: 70
tags: [orbit, design-brain, component-contract]
---

# Component Contract: `chip`

## Purpose
Use `Chip` for tags, filters, and scope/category labels — including selectable (toggle) and
removable chips. It is the flexible tag primitive. **Not for status**: a card-level status
label is a `Badge`; an inline row status is a `StatusIndicator` (see "Chip vs Badge vs
StatusIndicator" below).

## Source Links
- Component source:
  `packages/orbit/src/indicators/Chip.tsx`
- Styles:
  `packages/orbit/src/indicators/Chip.module.css`

## Anatomy
Inline pill: background + optional border + label; removable chips add a trailing close
button (`FaIcon` xmark, `aria-label="Remove <label>"`). Interactive (toggle) chips render a
native `<button>`; static/removable render a `<span>` (+ a close `<button>` when removable).

## Public API

| Prop | Type | Default | Required | Source |
| ---- | ---- | ------- | -------- | ------ |
| `label` | `string` | none | yes | code |
| `variant` | `'Information' \| 'Success' \| 'Warning' \| 'Error' \| 'Style 1'..'Style 4' \| 'Additional' \| 'No Status' \| 'None' \| 'Outline' \| 'Disabled'` | `'Outline'` | no | code |
| `contrast` | `'High' \| 'Low'` | `'Low'` | no | code |
| `size` | `'Default' \| 'Mini' \| 'Small' \| 'Medium'` | `'Default'` | no | code |
| `selected` | `boolean` | `false` | no | code |
| `disabled` | `boolean` | `false` | no | code |
| `removable` | `true` | — | no | code (removable mode) |
| `onClick` | `() => void` | — | no | code (toggle mode) |
| `onRemove` | `() => void` | — | no | code (removable mode) |

`Chip` is a discriminated union: **static** (default), **toggle** (`onClick`), or
**removable** (`removable: true` + `onRemove`). Don't combine `onClick` with `removable`.

## Variants
- Status-coloured: Information, Success, Warning, Error.
- Neutral / categorical: Style 1–4, Additional, No Status, None, Outline.
- Contrast: `Low` (tinted + bordered, default) or `High` (solid fill).
- Sizes: Default, Medium, Small, Mini.

## States
Static (presentational); toggle (`aria-pressed` = `selected`); removable (close button);
selected; disabled (`aria-disabled` / native `disabled`). No loading state.

## Density
Use `Mini` / `Small` in dense filter bars and table cells; `Default` otherwise. Token-driven.

## Themes
`efficio` + `orbit` via token values only (chip + status tokens).

## RBAC / Permissions
Don't expose restricted state through a chip; disable or omit.

## Tokens Used
- `--orbit-color-chip-*` (style-1..4, additional, no-status, default-border, disabled-*,
  high-bg-*, high-fg*)
- `--orbit-color-status-low-bg-*`, `--orbit-color-status-low-border-*`
- `--orbit-color-text-info / success / warning / error / primary`, `--orbit-color-white`

## Accessibility
Toggle chips are real buttons with `aria-pressed`; removable close buttons have
`aria-label="Remove <label>"`. Never rely on chip colour alone — the label carries meaning.

## Chip vs Badge vs StatusIndicator
- **`Chip`** — tags, filters, scope/category labels; selectable (toggle) or removable.
- **`Badge`** — a card-level status/classification pill (e.g. "Shared by client", tab counts).
- **`StatusIndicator`** — a dot + label for inline row/list status (e.g. tool-coverage rows).

The 2026-06-23 stress test diverged exactly here: use **Badge** for a card-level *status*,
**Chip** for scope / category / filter tags.

## Motion
No motion in source; add none.

## Content / Copy
Short tag labels; sentence case. For removable filter chips, the label is the value.

## Do / Don't
- Do use `Chip` for filters, scope/category tags, and selectable / removable items.
- Do use `Badge` (not Chip) for a card-level *status*.
- Don't combine `onClick` (toggle) with `removable`.
- Don't invent variants outside the supported set.

## Golden Example
`design-brain/examples/lovable-initiatives-port.md` (filter / scope chips). Dedicated
example is a gap.

## Status
in-review · Last updated: 2026-06-24 · Owner: design-system

## Gap Report
- No dedicated golden example for chips yet.
