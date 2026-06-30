---
type: component-contract
status: in-review
owner: design-system
surfaces: [shared, ClauseIQ, MarketIQ, RFP Analytics, RFP Builder]
source: code
last_reviewed: 2026-06-15
maturity_score: 84
tags: [orbit, design-brain, component-contract]
---

# Component Contract: `data-table`

Real component: `Table` from `@efficio/orbit`.

Source:
- `packages/orbit/src/layout/Table.tsx`
- `packages/orbit/src/layout/Table.module.css`
- `packages/orbit/src/layout/Table.test.tsx`
- ClauseIQ usage: `apps/prototypes/components/feature/clauseiq/ClauseIQPrototype.tsx`

## Purpose
Dense, scannable tabular display for procurement users comparing many rows, values,
statuses, and actions over long sessions.

## Public API

| Prop | Type | Default | Required | Notes |
| ---- | ---- | ------- | -------- | ----- |
| `columns` | `TableColumn<T>[]` | none | yes | Column definitions. |
| `rows` | `T[]` | none | yes | Data rows. |
| `getRowKey` | `(row: T) => React.Key` | none | yes | Stable row key. |
| `ariaLabel` | `string` | undefined | no | Used when `ariaLabelledBy` is absent. |
| `ariaLabelledBy` | `string` | undefined | no | Overrides `ariaLabel`. |
| `density` | `'Default' \| 'Compact'` | `'Default'` | no | Compact reduces cell vertical padding. |
| `variant` | `'Default' \| 'SeparatedRows'` | `'Default'` | no | Separated rows use row cards/spacing. |
| `emptyState` | `React.ReactNode` | `'No rows available.'` | no | Rendered in a full-width table row. |
| `onRowSelect` | `(row: T) => void` | undefined | no | Makes first cell content a row-selection button. |
| `getRowSelectionLabel` | `(row: T, index: number) => string` | `'Select row'` | no | Required for useful selectable-row names. |
| `pagination` | `TablePaginationProps` | undefined | no | Adds pagination nav. |

`TableColumn<T>`:

| Field | Type | Required | Notes |
| ----- | ---- | -------- | ----- |
| `id` | `string` | yes | Column id and fallback header label. |
| `header` | `React.ReactNode` | yes | Header content. |
| `render` | `(row: T) => React.ReactNode` | yes | Cell renderer. |
| `width` | `string` | no | Applied inline to `th`; use only when source/product requires explicit column sizing. |
| `sortable` | `boolean` | no | Renders sort button. |
| `sortDirection` | `'asc' \| 'desc'` | no | Controls sort icon. |
| `info` | `string` | no | Adds tooltip trigger beside header. |
| `onSortChange` | `(direction: 'asc' \| 'desc') => void` | no | Disabled sort button when absent. |

`TablePaginationProps`: `pageSize`, `page`, `totalRows`, `onPageChange`.

## Variants
- `Default`: bordered table container with collapsed rows.
- `SeparatedRows`: transparent wrapper, row spacing, each row reads as a separated surface.
- `Default` density: base cell padding.
- `Compact` density: tighter vertical padding.
- Selectable rows: enabled when `onRowSelect` is provided.
- Sortable columns: enabled per column with `sortable`.
- Paginated table: enabled when `pagination` is provided.

## States
- Default: renders headers and rows.
- Hover: selectable rows use `--orbit-color-bg-hover`.
- Focus-visible: sort buttons, info icon, row action, and pagination buttons use
  `--orbit-color-border-focused`.
- Disabled: sort buttons without `onSortChange`; pagination prev/next at limits.
- Empty: full-width empty row with `emptyState`.
- Error: not built into `Table`; page/pattern must provide error state around it.
- Loading: not built into `Table`; page/pattern must provide skeleton matching final columns.
- Selected: current source does not expose selected-row state.

## Density
`density="Compact"` reduces cell padding to `var(--orbit-space-s) var(--orbit-space-base)`.

## Themes
Works in base Efficio/CP and `[data-theme="orbit"]` through CSS custom properties.

## Large Data / Virtualization
The source-backed `Table` contract supports pagination, sorting, row selection, compact
density, and empty states. It does not currently expose row virtualization. When porting
external prototypes that use virtualized div rows, prefer Orbit `Table` with pagination
or server-side pagination unless a new virtual-table contract has been approved.

Do not recreate a pseudo-table with clickable div rows just to preserve prototype
virtualization. Native table semantics, keyboard row access, stable pagination, and
contracted Orbit styling are higher priority until a virtualized table primitive exists.

## Tokens Used
`--orbit-color-card-border-default`, `--orbit-radius-md`, `--orbit-color-card-bg-default`,
`--orbit-font-family-sans`, `--orbit-space-base`, `--orbit-space-s`,
`--orbit-space-xs`, `--orbit-space-xxl`, `--orbit-space-xl`,
`--orbit-color-text-primary`, `--orbit-color-text-secondary`,
`--orbit-color-text-disabled`, `--orbit-color-card-bg-accent`,
`--orbit-color-bg-hover`, `--orbit-color-bg-default`, `--orbit-color-silver`,
`--orbit-color-border-focused`, `--orbit-radius-sm`, `--orbit-font-weight-semibold`,
`--orbit-font-weight-medium`, `--orbit-leading-relaxed`, `--orbit-text-sm`,
`--orbit-text-base`.

## Accessibility
- Renders native `table`, `thead`, `tbody`, `th scope="col"`, and `td`.
- Table name comes from `ariaLabel` or `ariaLabelledBy`.
- Active sorted headers expose `aria-sort="ascending"` or `aria-sort="descending"`.
- Sortable headers use real buttons with full direction labels such as
  `Sort Name descending`; do not abbreviate directions in accessible names.
- Selectable rows expose row-contained buttons in the first cell.
- Tests cover accessible table names, selectable row buttons, keyboard row activation,
  sortable headers, header info labels, and pagination.

## Motion
No table animation in source. Preserve layout stability for loading/error wrappers.

## Content / Copy
Use specific table names and row-selection labels. Avoid generic `Select row` in product
usage when row identity is available.

## Do / Don't
- Do use `SeparatedRows` for ClauseIQ-style initiative selection.
- Do pass a meaningful `emptyState`.
- Do keep loading/error states at the page or pattern layer.
- Don't replace dense procurement comparison tables with card grids.

## Golden Example
`design-brain/examples/data-table-dense.md`

## Gap Report
- Major: no built-in loading, error, or selected-row state.
- Major: no source-backed virtualization contract; use pagination/server-side
  pagination for large datasets until approved.
- Major: `width` is an inline style escape hatch; use deliberately.
- Minor: default row-selection label is generic if `getRowSelectionLabel` is omitted.
