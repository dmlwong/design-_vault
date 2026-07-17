---
type: token-contract
status: in-review
owner: design-system
surfaces: [shared]
source: code
last_reviewed: 2026-06-15
maturity_score: 82
context_tier: task-core
load_when: [build-component, build-screen, port-prototype, extract-contract, design-review, token-question]
tags: [orbit, design-brain, tokens]
---

# tokens.md — Token Contract

This file records how Orbit tokens are used and where their real source lives. Values are
not copied here as the source of truth; they live in the coded design system.

## Source Of Truth

Design-system repo: `the efficio-orbit repo` (source paths below are relative to its repo root).

| Tier | Real source |
| ---- | ----------- |
| Bundle imported by consumers | `packages/orbit/tokens.css` |
| Primitive colours and swatches | `packages/orbit/styles/tokens/colors.css` |
| Semantic text/border/background colours | `packages/orbit/styles/tokens/semantics.css` |
| Component tokens | `packages/orbit/styles/tokens/components.css` |
| Spacing scale | `packages/orbit/styles/tokens/spacing.css` |
| Typography | `packages/orbit/styles/tokens/typography.css` |
| Radius, elevation, z-index, focus | `packages/orbit/styles/tokens/elevation.css` |
| Orbit theme override | `packages/orbit/styles/tokens/themes/orbit.css` |

Validation command:

```bash
cd <path-to-efficio-orbit>
npm run audit:design-system
```

The static audit checks reusable Orbit components for raw hex colours, button typing,
accessible naming, overlay focus restoration, token use, and related design-system rules.

## Three Tiers

1. **Primitives.** Raw palette, swatch, spacing, typography, radius, shadow, and z-index
   values. Components do not consume primitive colour values directly unless the source
   component has not yet been token-normalized.
2. **Semantic tokens.** Purpose-named text, border, background, status, and interaction
   tokens. Components should consume this tier by default.
3. **Component tokens.** Component-scoped aliases for buttons, cards, chips, overlays,
   dropdowns, tabs, side navigation, badges, toasts, and CP workspace surfaces.

## Themes

- **Efficio / Connected Platform base:** defined on `:root` across the token files.
- **Orbit:** activated with `[data-theme="orbit"]` in `themes/orbit.css`.
- Components must switch themes through CSS custom property values, not through
  component-level `if theme === ...` branches.

## Semantic Token Families

Use these real semantic families from `semantics.css`:

- Text: `--orbit-color-text-primary`, `--orbit-color-text-secondary`,
  `--orbit-color-text-disabled`, `--orbit-color-text-inverse`,
  `--orbit-color-text-error`, `--orbit-color-text-info`,
  `--orbit-color-text-success`, `--orbit-color-text-warning`,
  `--orbit-color-text-heading`.
- Borders: `--orbit-color-border-default`, `--orbit-color-border-accent`,
  `--orbit-color-border-selected`, `--orbit-color-border-highlight`,
  `--orbit-color-border-hover`, `--orbit-color-border-disabled`,
  `--orbit-color-border-focused`, `--orbit-color-border-error`,
  `--orbit-color-border-style1`.
- Backgrounds: `--orbit-color-bg-default`, `--orbit-color-bg-accent`,
  `--orbit-color-bg-hover`, `--orbit-color-bg-selected`,
  `--orbit-color-bg-disabled`, `--orbit-color-bg-style1`,
  `--orbit-color-bg-canvas`, `--orbit-color-bg-canvas-grid`.
- Connected Platform: `--orbit-color-cp-border`,
  `--orbit-color-cp-border-strong`, `--orbit-color-cp-surface-muted`,
  `--orbit-color-cp-nav-bg`, `--orbit-color-cp-nav-active-fg`,
  `--orbit-color-cp-date-text`, `--orbit-color-cp-timeline-highlight-bg`,
  `--orbit-color-cp-step-complete`, `--orbit-color-cp-step-active`.

## Component Token Families

Use real component token families from `components.css`:

- Button: `--orbit-color-btn-primary-*`, `--orbit-color-btn-secondary-*`,
  `--orbit-color-btn-tertiary-*`, `--orbit-btn-height-*`, `--orbit-btn-icon-size`.
- IconButton: `--orbit-icon-btn-small`, `--orbit-icon-btn-medium`,
  `--orbit-icon-btn-large`.
- Card: `--orbit-color-card-bg-*`, `--orbit-color-card-border-*`,
  `--orbit-color-card-indicator-*`, `--orbit-card-indicator-width`.
- ToggleCard: `--orbit-color-togglecard-*`.
- Badge / chip / status: `--orbit-badge-radius`, `--orbit-color-chip-*`,
  `--orbit-color-status-high-*`, `--orbit-color-status-low-*`.
- Checkbox / toggle: `--orbit-color-checkbox-*`, `--orbit-color-toggle-*`,
  `--orbit-toggle-*`.
- Dropdown: `--orbit-dropdown-trigger-height`, `--orbit-dropdown-option-height`,
  `--orbit-dropdown-chevron-size`.
- Tabs: `--orbit-tab-height`, `--orbit-tab-inner-height`,
  `--orbit-tab-underline-height`.
- Overlay / toast: `--orbit-color-overlay-backdrop`, `--orbit-overlay-width-medium`,
  `--orbit-overlay-width-large`, `--orbit-overlay-height-default`,
  `--orbit-toast-max-width`.
- Sidenav and CP shell: `--orbit-sidenav-*`, `--orbit-cp-*`.

## Spacing, Type, Radius, Shadow, Z-Index

- Spacing: `--orbit-space-none`, `--orbit-space-0`, `--orbit-space-px` (1px hairline —
  never a raw `1px`), `--orbit-space-micro`, `--orbit-space-xxs`,
  `--orbit-space-xs`, `--orbit-space-s`, `--orbit-space-base`,
  `--orbit-space-m`, `--orbit-space-l`, `--orbit-space-xl`, `--orbit-space-xxl`,
  `--orbit-space-mega`.
- Typography: `--orbit-font-family-sans`, `--orbit-font-family-brand`,
  `--orbit-text-xs` through `--orbit-text-3xl`, `--orbit-text-body-*`,
  `--orbit-text-button-*`, `--orbit-font-weight-*`, `--orbit-leading-*`.
- Radius: `--orbit-radius-none`, `--orbit-radius-sm`, `--orbit-radius-md`,
  `--orbit-radius-lg`, plus component-specific radius tokens.
- Shadow: `--orbit-shadow-none`, `--orbit-shadow-sm`, `--orbit-shadow-md`,
  `--orbit-shadow-lg`.
- Z-index: `--orbit-z-dropdown`, `--orbit-z-sticky`, `--orbit-z-tooltip`,
  `--orbit-z-overlay`, `--orbit-z-toast`.
- Focus: `--orbit-color-focus-ring` and `--orbit-color-border-focused`.

## Contrast-Sensitive Token Notes

The 2026-06-15 browser visual accessibility pass confirmed AA contrast across benchmark
routes after tuning:
- Efficio `--orbit-color-text-success` and `--orbit-color-text-warning` for small
  KPI/table deltas.
- Orbit `--orbit-color-text-success` for success deltas on information-tinted cards.
- Efficio `--orbit-color-sidenav-muted` for docs-shell navigation text.

Do not lighten these tokens for visual softness without rerunning rendered contrast
checks in both themes.

## Rules

- No hardcoded colours, spacing, radii, font sizes, line heights, shadows, or z-index in
  reusable Orbit components.
- Components consume semantic or component tokens; primitives stay behind aliases.
- If a source component currently uses a literal for motion or sizing, note it as a gap
  in that component contract rather than copying the literal into new UI.
- Theme differences must live in token overrides.
- Any new token must be added to the coded design system first, then referenced here.

## Known Gaps

- Dedicated motion tokens are not present in the current source. See `motion.md`.
- Dedicated data-viz tokens are not present in the current source. Analytics benchmarks
  currently use existing semantic/status tokens; see `data-viz.md`.
- Some source files still include component-local CSS variables such as `--_bg` and
  `--_border-color`; these should resolve to Orbit tokens, as `Card` and `Toast` do.
- `Table` consumes the primitive `--orbit-color-silver` directly (see
  `components/data-table.md` gap report). Primitives should stay behind semantic
  aliases; a semantic alias is needed before this can be called contract-clean.
