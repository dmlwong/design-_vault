---
type: benchmark-result
status: in-review
owner: design-system
surfaces: [MarketIQ, RFP Analytics, shared]
source: code
last_reviewed: 2026-06-15
maturity_score: 78
tags: [orbit, design-brain, benchmark, analytics, data-viz, marketiq]
---

# Benchmark Result: MarketIQ Analytics Dashboard

## Task
Task 3: build a MarketIQ analytics dashboard with KPI blocks, one trend chart, one
category comparison, underlying table access, loading, insufficient-data, and stale
states using the Orbit Design Brain.

## Product Repo
`the efficio-orbit repo`

## Required References Read
- `design-brain/data-viz.md`
- `design-brain/patterns/analytics-dashboard.md`
- `design-brain/examples/analytics-kpi-chart.md`
- `design-brain/components/card-panel.md`
- `design-brain/components/data-table.md`
- `design-brain/components/button.md`
- `design-brain/tokens.md`
- `design-brain/accessibility.md`
- `design-brain/ux-copy.md`
- `design-brain/_benchmarks/agent-benchmark-tasks.md`

## Implementation
- Route:
  `apps/docs/app/design-system/benchmarks/analytics-dashboard/page.tsx`
- Component:
  `apps/docs/app/design-system/benchmarks/analytics-dashboard/MarketIQAnalyticsDashboardBenchmark.tsx`
- Styles:
  `apps/docs/app/design-system/benchmarks/analytics-dashboard/MarketIQAnalyticsDashboardBenchmark.module.css`
- Docs index link:
  `apps/docs/app/design-system/page.tsx`
- Verified URL:
  `http://localhost:3000/design-system/benchmarks/analytics-dashboard`

## Result
Reported benchmark score: **18/18 - PASS**.

| Category | Score | Notes |
| -------- | ----- | ----- |
| Tokens only | 2 | New route styles use Orbit CSS custom properties for spacing, type, color, border, radius, sizing, and chart styling. A targeted raw `hex` / `rgb` / `px` scan returned no hardcoded visual values in the new benchmark files. |
| Theme support | 2 | The implementation uses Orbit semantic/component/status tokens, so it inherits Efficio base and `[data-theme="orbit"]` values through the docs shell. |
| Full states | 2 | Includes data, loading skeleton, insufficient-data, stale-data, load-failure, refreshed, permission-limited export, comfortable density, and compact density states. |
| Accessibility | 2 | State controls are keyboard buttons with `aria-pressed`; loading and stale states use live regions; chart has an accessible description and the same data is available in visible summaries/table rows; status is paired with text/icons, not colour alone. |
| Density | 2 | Comfortable and compact density are supported. Compact mode tightens dashboard gaps and switches the underlying Orbit table to `density="Compact"`. |
| Contract match | 2 | Uses real Orbit `Card`, `Table`, `Button`, `Badge`, `Toggle`, `Text`, `Headings`, and `FaIcon` APIs. Loading/error/empty states are composed at the page layer. |
| Pattern match | 2 | Matches `analytics-dashboard`: filter/state bar, KPI row, trend chart, category comparison, insight/status region, underlying table, export/refresh actions, and state previews. |
| Copy and motion | 2 | Copy is specific, calm, and procurement-contextual. No decorative chart animation or entrance motion was added. |
| Orbit feel | 2 | Dense, restrained MarketIQ workflow with spend, benchmark pressure, supplier coverage, category rows, role-limited export, and recommendation-oriented next actions. |

Total: `18/18`

## Verification Reported By Implementation Thread
- `npm run build:docs` passed and prerendered
  `/design-system/benchmarks/analytics-dashboard`.
- `npm run audit:design-system` passed with 27 checks.
- `npm run lint` passed.
- Browser verification passed for:
  - initial route render, page title, KPI summary, trend chart, category comparison,
    table region, and state controls
  - loading state with labelled status and skeletons in the final layout
  - insufficient-data state with reason and next action
  - stale-data state with non-colour warning signal and unique refresh action
  - load-failure state with recovery copy and retry action
  - refresh from stale back to data state
  - compact density switch applying compact Orbit table class
  - chart and category comparison render signals
  - underlying table row access
  - removal of an SVG nested `<title>` hydration mismatch found during browser QA

## What Worked
- The Design Brain references were sufficient to steer the agent toward a number-first
  dashboard rather than a decorative chart page.
- The analytics pattern clearly required underlying table access, which prevented the
  charts from becoming hover-only data displays.
- `Card` and `Table` contracts correctly pushed loading, empty, error, and stale states
  to the page/pattern layer instead of forcing new primitive APIs.
- State preview controls made validation straightforward without hidden product data
  conditions.
- Browser verification caught a real hydration issue in SVG point titles. Removing those
  titles kept chart data accessible through the chart description, visible summary, and
  table rows.

## Deductions / Residual Risk
- No formal axe scan or automated contrast report was run. Accessibility confidence
  comes from semantic markup, Orbit tokens, the design-system audit, and browser checks.
- The route is a docs benchmark implementation, not a validated production MarketIQ
  screen.
- Dedicated data-viz token names are still missing. The implementation therefore uses
  existing Orbit semantic/status tokens for chart marks instead of dedicated
  `viz-cat-*` tokens.
- `patterns/analytics-dashboard.md` and `examples/analytics-kpi-chart.md` still need a
  real MarketIQ/RFP Analytics production precedent before becoming stable.

## Brain Updates Applied
- `data-viz.md` now documents benchmark evidence, interim chart token usage, and
  required data-viz token families.
- `patterns/analytics-dashboard.md` now points to the benchmark route and records
  state, density, accessibility, and remaining production-source gaps.
- `examples/analytics-kpi-chart.md` now links the benchmark route as interim evidence.
- `_benchmarks/agent-benchmark-tasks.md` now records the Task 3 pass.
- `_review/Maturity Scorecard.md` now reflects three passing benchmarks.

## Open Brain Updates
- Decide and implement real data-viz token names for category series, positive,
  negative, neutral, grid, axis, and chart-fill semantics.
- Link a real MarketIQ or RFP Analytics production dashboard source before marking
  `analytics-dashboard` stable.
- Add formal axe/contrast artifacts for dashboard benchmarks.
- Decide whether Orbit needs a chart primitive or chart utility contract for accessible
  SVG labels, responsive chart dimensions, tooltips, legends, and table-backed data.

## Suggested Validation Questions
- Is using existing status tokens for chart marks acceptable until dedicated data-viz
  tokens exist, or should future benchmark scoring deduct under "Tokens only"?
- Should category comparison be part of the chart region or treated as a dense analytic
  list/table variant?
- Should stale data appear only as a page-level banner, or should stale status also
  propagate into each KPI/chart card?
- Should permission-limited export be required for analytics benchmark tasks?
- Should every dashboard benchmark include a downloadable data table/export simulation,
  or is visible table access sufficient?
