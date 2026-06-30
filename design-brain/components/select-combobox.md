---
type: component-contract
status: in-review
owner: design-system
surfaces: [shared]
source: code
last_reviewed: 2026-06-14
maturity_score: 76
tags: [orbit, design-brain, component-contract]
---

# Component Contract: `select-combobox`

Real components: `Dropdown` and `MultiSelectDropdown` from `@efficio/orbit`.

Source:
- `packages/orbit/src/inputs/Dropdown.tsx`
- `packages/orbit/src/inputs/Dropdown.module.css`
- `packages/orbit/src/inputs/Dropdown.test.tsx`
- `packages/orbit/src/inputs/MultiSelectDropdown.tsx`
- `packages/orbit/src/inputs/MultiSelectDropdown.test.tsx`

## Purpose
Let users choose from controlled option sets, including single-select and multi-select
procurement filters/statuses.

## Public API

`DropdownOption`: `{ label: string; value: string }`

`DropdownProps = BaseDropdownProps & FieldNamingProps`.

| Prop | Type | Default | Required | Notes |
| ---- | ---- | ------- | -------- | ----- |
| `options` | `DropdownOption[]` | none | yes | Available options. |
| `onChange` | `(value: string) => void` | none | yes | Receives selected value. |
| `value` | `string` | undefined | no | Selected value. |
| `message` | `string` | undefined | no | Help/error message. |
| `placeholder` | `string` | `'Please Select...'` | no | Empty trigger value. |
| `required` | `boolean` | `false` | no | Sets required semantics. |
| `disabled` | `boolean` | `false` | no | Disables trigger. |
| `invalid` | `boolean` | `false` | no | Error trigger/message state. |
| `previewState` | `'hover' \| 'focus'` | undefined | no | Docs/prototype preview. |
| `label` | `string` | undefined | conditional | Visible label. |
| `ariaLabel` | `string` | undefined | conditional | Standalone accessible name. |
| `ariaLabelledBy` | `string` | undefined | conditional | External accessible name. |

`MultiSelectDropdown` uses `value: string[]` and `onChange(values: string[])`, supports
removable selected chips, and exposes a `role="combobox"` trigger.

## Variants
- Single select via `Dropdown`.
- Multi select via `MultiSelectDropdown`.
- Labelled, externally labelled, or aria-labelled.
- Required, disabled, invalid.
- Preview hover/focus on `Dropdown`.

## States
- Default, hover, focus/open, disabled, invalid, selected, active option.
- Empty options: current source renders an empty listbox; product wrappers should provide
  empty guidance if needed.
- Loading/error fetching options: not built into these components.

## Density
Uses component sizing tokens: trigger height, option height, spacing. No explicit density
prop.

## Themes
Works in base Efficio/CP and `[data-theme="orbit"]` through tokens.

## Tokens Used
`--orbit-dropdown-trigger-height`, `--orbit-dropdown-option-height`,
`--orbit-dropdown-chevron-size`, `--orbit-z-dropdown`, `--orbit-shadow-lg`,
`--orbit-radius-sm`, `--orbit-space-xs`, `--orbit-space-s`,
`--orbit-space-base`, `--orbit-color-btn-secondary-bg`,
`--orbit-color-btn-secondary-border`, `--orbit-color-btn-secondary-bg-hover`,
`--orbit-color-btn-secondary-bg-disabled`,
`--orbit-color-btn-secondary-border-disabled`,
`--orbit-color-btn-secondary-icon`, `--orbit-color-btn-secondary-icon-disabled`,
`--orbit-color-bg-hover`, `--orbit-color-border-focused`,
`--orbit-color-border-error`, `--orbit-color-text-primary`,
`--orbit-color-text-secondary`, `--orbit-color-text-disabled`,
`--orbit-color-text-error`.

## Accessibility
- `Dropdown` trigger is a native button with `aria-haspopup="listbox"`,
  `aria-expanded`, `aria-controls`, `aria-activedescendant`, and accessible naming.
- `Dropdown` supports ArrowUp/ArrowDown, Home/End, Enter/Space, Escape.
- `MultiSelectDropdown` exposes `role="combobox"` and `aria-multiselectable`.
- Tests cover visible label linkage, keyboard option selection, active option exposure,
  multi-select chip removal, and keyboard toggling.

## Motion
No menu animation in source.

## Content / Copy
Use specific labels. Empty/no-result copy must be supplied by product composition when
options are dynamic.

## Do / Don't
- Do use `label`, `ariaLabel`, or `ariaLabelledBy`.
- Do use `MultiSelectDropdown` for multi-value filters.
- Don't use this as a searchable combobox; current `Dropdown` does not filter/search.

## Golden Example
`design-brain/examples/form-field-validation.md`

## Gap Report
- Major: no built-in async loading/error/empty option states.
- Major: no search filtering in `Dropdown`; ClauseIQ implements custom parameter search.
- Major: no density prop.
