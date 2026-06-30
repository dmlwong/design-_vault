---
type: component-contract-template
status: stable
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-06-14
maturity_score: 70
tags: [orbit, design-brain, template]
---

# Component Contract: `<ComponentName>`

> Copy this file to `components/<component-name>.md` and fill every section.
> This is the single definition of "correct" for the component. Code matches the
> contract; the contract does not bend to the code without an explicit update.

## Purpose
One sentence: what problem this solves for the Orbit user. Where it appears
(ClauseIQ / MarketIQ / RFP Analytics / RFP Builder / shared).

## Anatomy
The named parts (e.g. container, label, icon slot, trailing action). A short list or
a reference to the golden example in `examples/`.

## Public API (props)
| Prop | Type | Default | Required | Notes |
| ---- | ---- | ------- | -------- | ----- |
| `…`  |      |         |          |       |

> The API is part of the contract. Changing it requires updating this file first.

## Variants
List every variant and when to use it (e.g. `primary` / `secondary` / `ghost` /
`danger`; `sm` / `md` / `lg`). One row per variant with usage guidance.

## States (all required unless N/A — justify any N/A)
- **Default**
- **Hover**
- **Focus-visible** — visible ring, token: `<semantic focus token>`
- **Active / pressed**
- **Disabled** — non-interactive, reduced emphasis, still AA-legible
- **Loading** — describe the indicator and whether layout shifts
- **Empty** — only if data-bearing; what the empty state shows (see `ux-copy.md`)
- **Error** — validation/error presentation
- **Selected / active-nav** — if applicable

## Density
- **Comfortable** (default): spacing/sizing tokens used
- **Compact**: which tokens change; what must stay legible at high row counts

## Themes
Confirm the component renders correctly in **both** `efficio` and `orbit` with no
theme-conditional logic. Note any token that intentionally differs by theme.

## RBAC / permissions
Any role-driven differences (hidden, read-only, disabled-with-reason). State the
default for an unauthorized user.

## Tokens used
List the Tier-2 semantic tokens this component consumes. No primitives, no literals.

## Accessibility
- Role / semantics (native element or ARIA role)
- Keyboard interaction model (Tab, Enter, Space, Arrow, Esc as relevant)
- Labelling (`aria-label` / `aria-labelledby` expectations)
- Contrast notes for non-obvious cases
- Reference: `accessibility.md`

## Motion
Entrance/exit, hover/press feedback, transitions — durations and easing by token.
Respect reduced-motion. Reference: `motion.md`.

## Content / copy
Default labels, truncation rules, max lengths, localisation notes. Reference: `ux-copy.md`.

## Do / Don't
- ✅ …
- ❌ … (pull relevant items from `anti-patterns.md`)

## Golden example
Link to the canonical implementation in `examples/`.

## Status
`draft` | `in review` | `stable` · Last updated: `<date>` · Owner: `<name>`
