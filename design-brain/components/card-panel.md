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

# Component Contract: `card-panel`

## Purpose
Use `Card` to group related content or controls when a bordered surface improves
scanning. Orbit cards are structural surfaces, not marketing tiles; they should make
dense operational content easier to understand.

## Source Links
- Component source:
  `packages/orbit/src/layout/Card.tsx`
- Styles:
  `packages/orbit/src/layout/Card.module.css`
- Tests:
  `packages/orbit/src/layout/Card.test.tsx`
- ClauseIQ flow-card usage:
  `apps/prototypes/components/feature/clauseiq/ClauseIQPrototype.tsx`

## Anatomy
Card surface, optional left status rail, children content, padding class, token-backed
background and border. Header, title, action, and footer structure are supplied by
children; they are not built into `Card`.

## Composition
`Card` has no header/footer/action slots, so to compose a titled content/work card
(header + status + metadata + actions + states) follow the **`work-card`** pattern —
`design-brain/patterns/work-card.md` — instead of inventing a structure per screen.

## Public API

| Prop | Type | Default | Required | Source |
| ---- | ---- | ------- | -------- | ------ |
| `state` | `'Default' \| 'Hover' \| 'Accent' \| 'Highlight' \| 'Feature' \| 'Information' \| 'Success' \| 'Warning' \| 'Error' \| 'Disabled'` | `'Default'` | no | code |
| `type` | `'Static' \| 'Dynamic'` | `'Dynamic'` | no | code |
| `padding` | `'Base' \| 'Medium' \| 'Small'` | `'Base'` | no | code |
| `indicator` | `boolean` | state-derived | no | code |
| `children` | `React.ReactNode` | none | yes | code |
| `style` | `React.CSSProperties` | none | no | code |

## Variants
- Dynamic card: default, shadowed, raises shadow on hover.
- Static card: no shadow.
- Padding: `Base`, `Medium`, `Small`.
- Status states: `Highlight`, `Feature`, `Information`, `Success`, `Warning`,
  and `Error` show the left indicator rail by default.
- Non-rail states: `Default`, `Hover`, and `Accent` do not show the rail unless
  `indicator` is passed.
- Disabled card: removes shadow, sets `aria-disabled`, and never shows a rail.

## States
- Default: `state="Default"`.
- Hover preview: `state="Hover"` adds preview-hover styling for design previews.
- Accent and highlight states use card background/border token families.
- Information/success/warning/error states use matching status card tokens and rail.
- Disabled: `state="Disabled"`, `aria-disabled="true"`, no rail.
- Loading, empty, and error content states are composed inside `children`, not owned
  by the `Card` primitive.

## Density
Use `padding="Small"` for dense tables, dashboard cells, and compact workflow cards.
Use `padding="Base"` for ordinary grouped content. Use `padding="Medium"` only when
the content genuinely needs more reading space. Do not nest cards inside cards.

## Themes
Works in `efficio` and `orbit` through token values only. The component maps `state`
to token suffixes, then sets internal custom properties:
`--_bg`, `--_border-color`, and `--_indicator`.

## RBAC / Permissions
Permission-gated actions inside a card follow the relevant action contract. If an
entire card is unavailable, use `state="Disabled"` only when the user is allowed to
know the content exists.

## Tokens Used
- `--orbit-color-card-bg-default`
- `--orbit-color-card-bg-accent`
- `--orbit-color-card-bg-highlight`
- `--orbit-color-card-bg-feature`
- `--orbit-color-card-bg-information`
- `--orbit-color-card-bg-success`
- `--orbit-color-card-bg-warning`
- `--orbit-color-card-bg-error`
- `--orbit-color-card-bg-disabled`
- `--orbit-color-card-border-*`
- `--orbit-color-card-indicator-*`
- `--orbit-card-indicator-width`
- `--orbit-radius-md`
- `--orbit-shadow-none`
- `--orbit-shadow-sm`
- `--orbit-shadow-md`
- `--orbit-space-base`
- `--orbit-space-m`
- `--orbit-space-s`

## Accessibility
`Card` is a non-interactive `div`. Do not make the card itself clickable unless it is
converted to a native interactive element or given a complete keyboard and role model.
`aria-disabled` is present only for `state="Disabled"`.

## Motion
Current source uses shadow and border transitions of `0.2s ease` for dynamic cards.
Do not add entrance animation. Reduced-motion handling is a foundation gap tracked in
`design-brain/motion.md`.

## Content / Copy
Card titles should describe the grouped task or data. Avoid promotional headings and
oversized hero language inside operational product screens.

## Do / Don't
- Do use card states to communicate actual product status.
- Do keep structured children simple and scannable.
- Do use `padding="Small"` for dense operational contexts.
- Don't nest cards inside cards.
- Don't create one-off surface colours with inline literal values.
- Don't use cards to replace tables for dense comparative data.

## Golden Example
`design-brain/examples/clauseiq-focus-mode-results.md`

## Gap Report
- No built-in header, footer, action, loading, or empty slots exist — compose via the
  `work-card` pattern (`design-brain/patterns/work-card.md`).
- The component exposes a generic `style` escape hatch; reviewers should ensure it
  only passes token-backed values.
- Reduced-motion rules are not implemented in source.
