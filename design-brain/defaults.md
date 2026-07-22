---
type: foundation
status: in-review
owner: design-system
surfaces: [shared]
source: code
last_reviewed: 2026-06-19
maturity_score: 72
context_tier: task-core
load_when: [build-component, build-screen, port-prototype, default-choice]
tags: [orbit, design-brain, defaults]
---

# defaults.md — Default choices (when unsure, use these)

This file removes guesswork. When generating UI, do **not** invent spacing, padding, or
component choices. Pick the default below unless the component contract, a pattern
contract, or a `discovery/` pack says otherwise. The static audit
(`npm run audit:design-system`) catches hardcoded values, but it **cannot** catch a
tokenized-but-wrong choice — that is what this file is for.

How to read the markers:
- `[SOURCED]` — taken straight from a component/token contract; safe to apply now.
- `[SCREENSHOT]` — derived from real platform screenshots that are still `in-review`
  (restricted until design-system owners approve sanitization). Apply it, but it inherits
  that in-review status.
- `[CONFIRM]` — a recommended default that still needs design-system owner sign-off.
  Apply it provisionally, but flag it in your output until it is confirmed.

## Buttons & actions

| Decision                          | Default                                       | Source                      |
| --------------------------------- | --------------------------------------------- | --------------------------- |
| Primary page/section action       | `Button` variant `Primary`, size `Medium`     | `[SOURCED]` button contract |
| Secondary action                  | `Button` variant `Secondary`, size `Medium`   | `[SOURCED]`                 |
| Low-emphasis / inline action      | `Button` variant `Tertiary`                   | `[SOURCED]`                 |
| Confirm / positive action         | `Button` variant `Positive`                   | `[SOURCED]`                 |
| Destructive action                | `Button` variant `Destructive`                | `[SOURCED]`                 |
| Icon-only action                  | `IconButton`, size `Medium`, with `ariaLabel` | `[SOURCED]`                 |
| How many primary actions per view | Exactly one                                   | `[SOURCED]` ux-copy         |
| Button label style                | Verb-led, sentence case ("Save changes")      | `[SOURCED]` ux-copy         |

## Density

| Decision | Default | Source |
| -------- | ------- | ------ |
| Default density | Comfortable (`density="Default"`) | `[SOURCED]` principles |
| When to use Compact | Dense tables, queues, trackers, admin lists | `[SOURCED]` |
| Compact must still | Pass WCAG 2.2 AA and keep target sizes | `[SOURCED]` accessibility |

## Cards

| Decision | Default | Source |
| -------- | ------- | ------ |
| Card type | `Dynamic` | `[SOURCED]` card contract |
| Card padding | `Base` | `[SOURCED]` |
| Card padding for dense dashboards/tables | `Small` | `[SOURCED]` |
| Card padding `Medium` | Only when extra reading room is needed | `[SOURCED]` |
| Nesting cards | Don't | `[SOURCED]` |

## Tables

| Decision | Default | Source |
| -------- | ------- | ------ |
| Tabular data component | Orbit `Table` (never div rows) | `[SOURCED]` data-table contract |
| Table density | `Default`; `Compact` for high row counts | `[SOURCED]` |
| Large datasets | Pagination (no virtualization in contract yet) | `[SOURCED]` |
| Row key | Always provide `getRowKey` | `[SOURCED]` |

## Inputs & forms

| Decision | Default | Source |
| -------- | ------- | ------ |
| Text entry | `Input` | `[SOURCED]` input contract |
| Single choice | `Dropdown` (placeholder `Please Select...`) | `[SOURCED]` select contract |
| Multiple choice | `MultiSelectDropdown` | `[SOURCED]` |
| Field label | Visible label linked via `ariaLabelledBy` | `[SOURCED]` |
| Help / error text | Linked via `ariaDescribedBy`; pair colour with icon/text | `[SOURCED]` |
| Gap between fields | `--orbit-space-base` (16px); Compact `--orbit-space-xxs` | `[SOURCED]` settings form benchmark |
| Label → input gap (within a field) | `--orbit-space-xs` (4px) | `[SOURCED]` settings form benchmark |
| Form panel / group gap & padding | `--orbit-space-base` (16px) | `[SOURCED]` settings form benchmark |

## Dialogs & overlays

| Decision | Default | Source |
| -------- | ------- | ------ |
| Modal / blocking surface | `Overlay`, size `Default`, height `Viewport` | `[SOURCED]` dialog contract |
| Drawer / side panel | Use `Overlay` — no reusable `Drawer` exists yet | `[SOURCED]` drawer gap |

## Radius, elevation, focus, motion

| Decision | Default | Source |
| -------- | ------- | ------ |
| Card radius | `--orbit-radius-md` | `[SOURCED]` |
| Control radius (button, input, dropdown, tab, toast) | `--orbit-radius-sm` | `[SOURCED]` |
| Overlay radius | `--orbit-radius-lg` | `[SOURCED]` |
| Hairline / divider border width | `--orbit-space-px` (1px) — never a raw `1px` | `[SOURCED]` spacing.css |
| Dynamic card shadow | `--orbit-shadow-sm` (→ `md` on hover) | `[SOURCED]` |
| Overlay / toast shadow | `--orbit-shadow-lg` | `[SOURCED]` |
| Focus ring | `--orbit-color-focus-ring` / `--orbit-color-border-focused` | `[SOURCED]` |
| Hover/focus transition | Existing source convention (~`0.15s ease`); add no new animation | `[SOURCED]` motion |
| Reduced motion | Always honour `prefers-reduced-motion` | `[SOURCED]` |

## Icons

| Decision | Default | Source |
| -------- | ------- | ------ |
| Icon component | `FaIcon` (Orbit's Font Awesome 6 Pro primitive); use the `FA` constants (e.g. `FA.check`) or a unicode string | `[SOURCED]` FaIcon — 61 uses in source |
| Icon library | **Never** import `lucide-react`, `react-icons`, `@fortawesome/*`, or any other icon library — Orbit has none installed | `[SOURCED]` lucide = 0 uses, not a dependency |
| Icon accessibility | Icons are decorative by default (`ariaHidden`); put the accessible name on the control, not the icon | `[SOURCED]` FaIcon |

## Layout spacing (page-level)

Confirmed from the procurement settings form benchmark
(`apps/docs/app/design-system/benchmarks/form-validation/`) and the platform shells
(`CpWorkspaceShell`, `OrbitAppShell`), which use real Orbit tokens.

| Decision | Default | Source |
| -------- | ------- | ------ |
| Gap between sibling cards/blocks (content grid) | `--orbit-space-l` (32px); Compact `--orbit-space-base` | `[SOURCED]` settings form benchmark |
| Gap between major page sections | `--orbit-space-l` (32px) | `[SOURCED]` settings form benchmark |
| Panel / context-panel padding | `--orbit-space-base` (16px) | `[SOURCED]` settings form benchmark |
| Outer page content padding (CP) | `--orbit-cp-shell-content-padding` (the `CpWorkspaceShell` content token) | `[SOURCED]` CpWorkspaceShell |
| Outer page content padding (Orbit-client) | No shell default — `OrbitAppShell` sets none; each page sets its own (use `--orbit-space-l` for new pages) | `[SOURCED]` OrbitAppShell + `[CONFIRM]` for the new-page value |

## Platform deltas

The defaults above are shared. Where Connected Platform and Orbit / Client Connected
Platform diverge, the platform profile wins. Read
`design-brain/platforms/<platform>.md` first.

| Aspect            | Connected Platform (internal)                                                                                            | Orbit / Client Connected Platform (external)                                                                                                                                                                          |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Shell             | Light theme; icon-only collapsed left nav rail; tab bars for sub-navigation `[SCREENSHOT]`                               | Dark labelled left nav; light work canvas; teal/blue primary buttons `[SCREENSHOT]`                                                                                                                                   |
| Density bias      | Denser by default — dense quick-link grids, compact list/table rows, many items per viewport `[SCREENSHOT]`              | Comfortable in main content; reserve Compact for tables, modals, and the side rail. Detail/coverage screens carry real metadata (tabs, side-by-side summary cards, tool rows) but stay clearly grouped `[SCREENSHOT]` |
| Card padding bias | Tight — `Small` on operational tiles, list rows, and tables `[SCREENSHOT]`                                               | Roomy — `Base` for tool/KPI/summary cards (icon → title → description → action); `Small` only in dense tool-coverage rows/tables `[SCREENSHOT]`                                                                       |
| Spacing bias      | Tight, scan-first; maximise content per screen `[SCREENSHOT]`                                                            | Generous gaps between sections; guided flows use a constrained central content column with one prominent primary action (e.g. full-width `Generate`) `[SCREENSHOT]`                                                   |
| Copy              | Concise internal/operational labels ("Bulk Import", "Add Initiative", "Incumbent Status", "Disqualified") `[SCREENSHOT]` | Client-safe, benefit-led, explanatory ("AI-Powered Tools for Faster Initiative Delivery"); verb-led actions ("Launch Tool", "Generate") `[SCREENSHOT]`                                                                |

> Both columns are confirmed from the in-review screenshot packs in
> `design-brain/examples/screenshots/` — they inherit that in-review status until
> design-system owners approve sanitization. The spacing **scale** is confirmed real from
> `spacing.css` (`base`=16px, `m`=24px, `l`=32px, `xxl`=48px).

## Rule

If a default here conflicts with a component contract, pattern contract, platform
profile, or `discovery/` pack, **those win** — and update this file so the conflict does
not recur. If none of them answer the question, use the default here and do not invent a
new value.
