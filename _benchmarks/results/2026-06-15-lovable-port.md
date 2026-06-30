---
type: benchmark-result
status: in-review
owner: design-system
surfaces: [shared]
source: code
last_reviewed: 2026-06-15
maturity_score: 82
tags: [orbit, design-brain, benchmark, lovable-port, migration]
---

# Benchmark Result: Lovable Prototype Port

## Task
Task 4: port an external Lovable prototype into Orbit components and tokens. Report
component mapping, token translation, missing states, accessibility fixes, deviations,
and whether the result passes the benchmark rubric.

## Product Repo
`the efficio-orbit repo`

## Prototype Source
`Test`

Main prototype files inspected:
- `Test/src/components/initiatives-table.tsx`
- `Test/src/components/initiatives-table-simple.tsx`
- `Test/src/styles.css`
- `Test/src/routes/index.tsx`

## Required References Read
- `AGENTS.md`
- `design-brain/skills/port-to-orbit/SKILL.md`
- `design-brain/tokens.md`
- `design-brain/components/README.md`
- `design-brain/anti-patterns.md`
- `design-brain/accessibility.md`
- `design-brain/ux-copy.md`
- `design-brain/_benchmarks/agent-benchmark-tasks.md`
- `design-brain/components/data-table.md`
- `design-brain/components/button.md`
- `design-brain/components/input.md`
- `design-brain/components/select-combobox.md`
- `design-brain/components/tabs.md`
- `design-brain/components/badge-status.md`
- `design-brain/components/card-panel.md`

## Implementation
- Route:
  `apps/docs/app/design-system/benchmarks/lovable-port/page.tsx`
- Component:
  `apps/docs/app/design-system/benchmarks/lovable-port/LovablePortBenchmark.tsx`
- Styles:
  `apps/docs/app/design-system/benchmarks/lovable-port/LovablePortBenchmark.module.css`
- Docs index link:
  `apps/docs/app/design-system/page.tsx`
- Verified URL:
  `http://localhost:3000/design-system/benchmarks/lovable-port`

## Result
Reported benchmark score: **18/18 - PASS**.

| Category | Score | Notes |
| -------- | ----- | ----- |
| Tokens only | 2 | New route styles use Orbit CSS custom properties for spacing, type, color, border, radius, and layout sizing. A targeted scan found no raw hex, px, rem, rgba, or OKLCH values in the new route. |
| Theme support | 2 | Browser verified Efficio base theme and `[data-theme="orbit"]`; the table remained visible and token-driven in both modes. |
| Full states | 2 | Includes data, loading skeleton, empty, error, no-permission, active filters, search, sorting, pagination, column presets, comfortable density, and compact density. |
| Accessibility | 2 | Uses Orbit keyboard-operable controls, native table semantics, named search/table/row actions, `aria-pressed` state toggles, `role="status"` loading, `role="alert"` error, and visible status/stage labels. |
| Density | 2 | Comfortable and compact density are implemented through Orbit `Table` density and token-backed page controls. |
| Contract match | 2 | Uses real Orbit `PageHeader`, `Table`, `Searchbox`, `Dropdown`, `Button`, `Badge`, `Card`, `Text`, `Headings`, and `FaIcon` APIs. |
| Pattern match | 2 | Preserves the useful Lovable information architecture while converting it to a dense procurement workflow with Orbit states and controls. |
| Copy and motion | 2 | Copy is clear, calm, procurement-oriented, and recovery-focused. No decorative animation or entrance motion was introduced. |
| Orbit feel | 2 | Replaces generic ShadCN/Tailwind styling with restrained Orbit components, high information density, token-backed states, and enterprise procurement context. |

Total: `18/18`

## Component Mapping
| Lovable / ShadCN element | Orbit mapping | Status |
| ------------------------ | ------------- | ------ |
| Full-screen Tailwind shell | Docs benchmark page section with CSS module and Orbit tokens | Ported |
| Project title/header and top navigation | Orbit `PageHeader` with tabs, actions, and initiative pill | Ported |
| ShadCN `Button` actions | Orbit `Button` with `Primary`, `Secondary`, and `Tertiary` variants | Ported |
| Lucide action icons | Orbit `FaIcon` inside Orbit buttons | Ported |
| Search input | Orbit `Searchbox` with explicit accessible name | Ported |
| ShadCN dropdown menu checkbox column toggles | Orbit `Dropdown` as controlled column-set presets | Ported with deviation |
| Mine / Team / Triage segmented control | Orbit `Button` group with `aria-pressed` | Ported |
| Comfortable / compact density control | Orbit `Button` group controlling Orbit `Table` density | Ported |
| Tailwind / ShadCN virtualized table | Orbit `Table` with sortable headers, pagination, row selection, empty state | Ported with scope adjustment |
| Status pills | Orbit `Badge` variants | Ported |
| Stage button with colored dot | Orbit `Button` plus `Badge`; no colour-only status | Ported |
| Avatar fallback stack | Page-local token-backed initials stack with accessible resource label | Ported locally |
| Row detail | Page-level `Card` detail panel | Added |
| Missing loading/error/empty/permission states | Page-level `Card`, `Table`, and live-region compositions | Added |

## Token Translation
| Prototype style source | Orbit translation | Status |
| ---------------------- | ----------------- | ------ |
| Tailwind background utilities | `--orbit-color-bg-default`, `--orbit-color-card-bg-default`, `--orbit-color-bg-hover`, `--orbit-color-bg-selected` | Ported |
| Tailwind text utilities | `--orbit-color-text-primary`, `--orbit-color-text-secondary` | Ported |
| Tailwind border utilities | `--orbit-color-border-default`, `--orbit-color-border-selected`, `--orbit-space-px` | Ported |
| Tailwind status colors | Orbit `Badge` statuses: `Information`, `Success`, `Warning`, `Error`, `No Status` | Ported |
| Tailwind spacing/type/radius utilities | `--orbit-space-*`, `--orbit-text-*`, `--orbit-radius-*` and Orbit typography components | Ported |
| Inline column pixel widths | Token expressions such as `calc(var(--orbit-space-mega) * 4)` | Ported |
| Hardcoded icon sizes | Orbit `FaIcon` and component icon sizing | Ported |
| ShadCN dark theme overrides | Theme-neutral Orbit semantic/component tokens | Ported |

## Missing States Added
- Loading: labelled status region with skeleton table rows matching the final table
  shape.
- Empty: table empty state with recovery guidance for search/filter conditions.
- Error: `Card state="Error"` with plain-language explanation and retry action.
- Disabled / permission: no-permission state disables add, edit, and stage-change
  controls and explains role restrictions.
- Active filters: visible filter summary and clear action.
- Row detail: selected initiative panel confirms row selection behavior.
- Density: comfortable and compact modes wired to Orbit `Table`.
- Theme: Efficio base and Orbit theme use the same component logic.

## Accessibility Fixes
- Replaced click-only table header divs with Orbit sortable header buttons.
- Replaced custom pseudo-table row structure with native Orbit table semantics.
- Added accessible names for search, table, row selection, and stage-change controls.
- Added `aria-pressed` to state, scope, and density toggle groups.
- Added `role="status"` with live text for loading state.
- Added `role="alert"` for the error state.
- Kept status and stage labels visible so color is never the only signal.
- Used disabled native buttons for permission-restricted actions.
- Fixed a duplicate React key warning in the resource initials stack found during
  browser verification.

## Verification Reported By Implementation Thread
- `npm run audit:design-system` passed with 27 checks.
- `npm run lint` passed.
- `npm run build:docs` passed and prerendered
  `/design-system/benchmarks/lovable-port`.
- Targeted raw visual-value scan of the new route found no raw `hex`, `px`, `rem`,
  `rgba`, or `oklch` usage.
- Browser verification passed for render, search/filter, compact density, loading,
  empty, error, no-permission, row detail, Efficio/Orbit theme visibility, mobile-width
  sanity, and fresh reload without console errors.

## What Worked
- The `port-to-orbit` skill gave an effective sequence: inventory, component mapping,
  token translation, state/a11y completion, theme/density, and validation.
- The `data-table` contract made the biggest quality difference by replacing custom div
  rows with native table semantics, row selection, sorting, and pagination.
- The PageHeader tab composition preserved the Lovable page structure while adding
  keyboard tab-list behavior.
- State preview buttons made validation simple and exposed states that the Lovable
  prototype omitted.
- Token-only CSS modules were sufficient to preserve the dense operational layout
  without importing Tailwind or ShadCN styling.

## Deviations / Residual Risk
- Orbit has no contracted dropdown-menu checkbox component, so the port uses controlled
  column presets through Orbit `Dropdown`.
- Orbit `Table` currently provides pagination, not virtualization, so the benchmark uses
  a deterministic 72-row dataset with 12-row pages rather than the prototype's 623-row
  virtualized table.
- Avatar/resource fallback stacks are implemented locally because no Avatar contract
  exists in the Design Brain.
- No formal axe or automated contrast artifact was generated. Accessibility confidence
  comes from semantic markup, Orbit components, token use, design-system audit, and
  browser interaction checks.
- This is a docs benchmark route, not a production AUT01 initiatives screen.

## Brain Updates Applied
- Added `patterns/lovable-port.md` as an in-review prototype migration pattern.
- Added `examples/lovable-initiatives-port.md` as the golden example for this run.
- Updated `skills/port-to-orbit/SKILL.md` with benchmark-proven porting rules.
- Updated `components/data-table.md` with virtualization and pagination guidance.
- Updated `anti-patterns.md` with Lovable/ShadCN import and pseudo-table warnings.
- Updated `_benchmarks/agent-benchmark-tasks.md` run history with Task 4.
- Updated `_review/Maturity Scorecard.md` and `README.md` to reflect the 85/100 score.

## Open Brain Updates
- Decide whether Orbit needs a contracted menu/checkbox-list pattern for granular column
  visibility.
- Decide whether resource avatar stacks belong in an Avatar contract, table pattern, or
  product-specific composition.
- Decide whether future large-table benchmarks require virtualization or whether
  pagination/server-side pagination is sufficient for scoring.
- Add formal axe/contrast capture expectations to benchmark verification artifacts.

## Suggested Validation Questions
- Is the column preset substitution acceptable for ports from ShadCN dropdown checkbox
  menus, or should future ports require granular column toggles?
- Should Avatar/resource stacks be formalized before more procurement table ports?
- Should Task 4 deduct for replacing virtualization with pagination, or is that aligned
  with the current Orbit `Table` contract?
- Should a formal accessibility scan be required for a full 18/18 score?
