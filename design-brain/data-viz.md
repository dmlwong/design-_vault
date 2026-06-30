---
type: foundation
status: in-review
owner: design-system
surfaces: [MarketIQ, RFP Analytics]
source: code
last_reviewed: 2026-06-15
maturity_score: 74
tags: [orbit, design-brain, data-viz, benchmark]
---

# data-viz.md — Charts, KPIs, and analytics views

MarketIQ and RFP Analytics live and die on data display. Generic chart defaults are as
damaging there as generic ShadCN components elsewhere. Read this before building any
chart, KPI, scorecard, or analytics view.

## Principles
- **The number first.** Users come for the value/decision, not the picture. Lead with the
  figure and its delta; the chart supports it.
- **One question per chart.** A chart answers a single comparison/trend/composition
  question. If it answers two, split it.
- **Tables are a feature.** Procurement users often want the underlying rows. Dense
  sortable tables are a first-class display, not a fallback — don't force charts.
- **Honest axes.** No truncated y-axes that exaggerate change without explicit flagging;
  consistent scales across compared charts.

## Defaults
- Chart palette: use dedicated semantic data-viz tokens once they exist. Until then,
  benchmark-backed charts may use existing Orbit semantic/status tokens such as
  `--orbit-color-status-high-bg-information`, `--orbit-color-status-high-bg-warning`,
  `--orbit-color-status-high-bg-error`, `--orbit-color-status-high-bg-success`,
  `--orbit-color-border-default`, and `--orbit-color-text-secondary`. Never raw hex.
- Positive/negative encodings pair colour with sign/icon (a11y: never colour alone).
- Number formatting per `ux-copy.md` (currency, %, dates unambiguous, locale-aware).
- Empty/insufficient-data state: designed, with a reason and next action — never a blank axis.
- Loading: skeleton in final layout; no spinner-induced reflow.
- Tooltips: keyboard-reachable; data must also be available outside hover (table/summary).

## Benchmark Evidence
- MarketIQ analytics dashboard benchmark:
  `apps/docs/app/design-system/benchmarks/analytics-dashboard/MarketIQAnalyticsDashboardBenchmark.tsx`
- Benchmark result:
  `_benchmarks/results/2026-06-15-marketiq-analytics-dashboard.md`

## Chart Accessibility Contract
- Each SVG chart has `role="img"` and a title/description relationship or equivalent
  accessible name and description.
- Do not rely on per-point `<title>` elements for critical data; browser QA found they
  can cause hydration issues in the benchmark route.
- Every charted value must also exist in visible text, a summary, or an underlying table.
- Legends use text labels plus token-backed swatches.
- Loading, insufficient data, stale data, and failure states are page/pattern states,
  not hidden chart-only states.

## Chart choice quick rules
- Trend over time → line. Compare categories → horizontal bar (labels stay legible).
- Part-of-whole → stacked bar; pies only ≤ ~4 slices and only when proportion is the point.
- Distribution → histogram/box. Correlation → scatter.
- Avoid dual axes, 3D, radar, and decorative gradients in functional charts.

## KPI / scorecard blocks
Value, label, delta (with direction + period), and optional sparkline — in that priority.
Density-mode aware. Click-through to the detailed view where one exists.

## Data-Viz Token Gap
Create real semantic data-viz tokens before marking analytics guidance stable. Required
families:
- category series: `--orbit-color-viz-category-1..n`
- positive / negative / neutral: `--orbit-color-viz-positive`,
  `--orbit-color-viz-negative`, `--orbit-color-viz-neutral`
- chart structure: `--orbit-color-viz-axis`, `--orbit-color-viz-grid`,
  `--orbit-color-viz-fill`
- stale / insufficient / forecast confidence, if product semantics need them

## Don't
- ❌ Default library colours or default tooltips left unstyled.
- ❌ Charts that can't be understood in grayscale.
- ❌ Animating chart entry on every data refresh.
- ❌ Hover-only charts with no table or text equivalent.
