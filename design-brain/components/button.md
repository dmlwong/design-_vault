---
type: component-contract
status: in-review
owner: design-system
surfaces: [shared]
source: code
last_reviewed: 2026-06-14
maturity_score: 78
tags: [orbit, design-brain, component-contract]
---

# Component Contract: `button`

Real components: `Button` and `IconButton` from `@efficio/orbit`.

Source:
- `packages/orbit/src/actions/Button.tsx`
- `packages/orbit/src/actions/Button.module.css`
- `packages/orbit/src/actions/Button.test.tsx`
- `packages/orbit/src/actions/IconButton.tsx`
- `packages/orbit/src/actions/IconButton.module.css`

## Purpose
Trigger explicit user actions with predictable hierarchy and accessible states.

## Public API

`ButtonProps` extends native button attributes except `disabled`.

| Prop | Type | Default | Required | Notes |
| ---- | ---- | ------- | -------- | ----- |
| `variant` | `'Primary' \| 'Secondary' \| 'Tertiary' \| 'Positive' \| 'Destructive'` | `'Primary'` | no | Visual/intent variant. |
| `size` | `'Small' \| 'Medium'` | `'Medium'` | no | Height/padding variant. |
| `state` | `'Default' \| 'Hover' \| 'Disabled'` | `'Default'` | no | `Hover` is a preview state for docs/prototypes. |
| `children` | `React.ReactNode` | none | yes | Visible label. |
| `icon` | `React.ReactNode` | undefined | no | Leading icon. |
| `iconRight` | `React.ReactNode` | undefined | no | Trailing icon. |
| `disabled` | `boolean` | `false` | no | Also disabled when `state="Disabled"`. |
| `type` | native button type | `'button'` | no | Defaults to non-submit. |

`IconButtonProps` uses the same variants, adds size `'Large'`, requires `icon` and
`ariaLabel`, and omits visible children.

## Variants
- `Primary`: main action.
- `Secondary`: neutral action with border.
- `Tertiary`: low-emphasis inline action.
- `Positive`: success/confirm action.
- `Destructive`: destructive action.
- Icon-only: use `IconButton`, not an empty `Button`.

## States
- Default, hover, focus-visible, disabled.
- `state="Hover"` exists for visual preview and should not be used for live state.
- No built-in loading state in `Button`; use `MultiStateButton` or product wrapper if
  loading is required.
- No built-in pressed/active styling beyond native button behavior and hover.

## Density
`Medium` height uses `--orbit-btn-height-medium`; `Small` uses
`--orbit-btn-height-small`.

## Themes
Works in base Efficio/CP and `[data-theme="orbit"]` through button tokens.

## Tokens Used
`--orbit-color-btn-primary-*`, `--orbit-color-btn-secondary-*`,
`--orbit-color-btn-tertiary-*`, `--orbit-btn-height-medium`,
`--orbit-btn-height-small`, `--orbit-btn-icon-size`, `--orbit-icon-btn-small`,
`--orbit-icon-btn-medium`, `--orbit-icon-btn-large`, `--orbit-space-s`,
`--orbit-space-base`, `--orbit-space-0`, `--orbit-radius-sm`,
`--orbit-text-button-size`, `--orbit-text-button-weight`,
`--orbit-text-button-leading`, `--orbit-font-family-sans`,
`--orbit-color-border-focused`.

## Accessibility
- Uses native `button`.
- Default `type="button"` prevents accidental form submission.
- Disabled state sets native `disabled` and `aria-disabled`.
- Icon-only buttons require `ariaLabel`.
- Tests cover default type and disabled activation blocking.

## Motion
Source uses `transition: all 0.15s ease`; motion tokens do not yet exist.

## Content / Copy
Use verb-led labels: "Save changes", "Run analysis", "Add clause". Avoid vague labels.

## Do / Don't
- Do use one primary action per view/section.
- Do use `IconButton` for icon-only actions.
- Don't use `Positive` or `Destructive` without clear product intent.

## Golden Example
`design-brain/examples/button-states.md`

## Gap Report
- Major: no built-in loading state on `Button`.
- Major: motion values are literals pending motion tokens.
