---
type: example
status: in-review
owner: design-system
surfaces: [MarketIQ, RFP Analytics]
platform: orbit-client-connected-platform
source: code
last_reviewed: 2026-06-15
maturity_score: 72
tags: [orbit, design-brain, example, data-viz, benchmark]
---

# Golden Example: Analytics KPI And Chart View

## Demonstrates
- `analytics-dashboard` pattern.
- KPI hierarchy, chart choice, semantic/status token fallback, and access to underlying
  rows.

## Real Source Links
- Benchmark route:
  `apps/docs/app/design-system/benchmarks/analytics-dashboard/page.tsx`
- Benchmark component:
  `apps/docs/app/design-system/benchmarks/analytics-dashboard/MarketIQAnalyticsDashboardBenchmark.tsx`
- Benchmark styles:
  `apps/docs/app/design-system/benchmarks/analytics-dashboard/MarketIQAnalyticsDashboardBenchmark.module.css`
- Benchmark result:
  `_benchmarks/results/2026-06-15-marketiq-analytics-dashboard.md`
- Benchmark screenshot reference pack:
  `_benchmarks/results/2026-06-15-golden-visual-reference.md`
- Product screen: source-required

## Benchmark Screenshot Evidence
Use these screenshots for benchmark-route evidence of KPI density, chart/table pairing,
status tone, and theme/density mechanics. Do not treat them as canonical platform visual
precedent until production MarketIQ/RFP Analytics screens are linked:

- `_benchmarks/results/screenshots/2026-06-15-golden-visual-reference/analytics-dashboard-efficio-default.png`
- `_benchmarks/results/screenshots/2026-06-15-golden-visual-reference/analytics-dashboard-efficio-compact.png`
- `_benchmarks/results/screenshots/2026-06-15-golden-visual-reference/analytics-dashboard-orbit-default.png`
- `_benchmarks/results/screenshots/2026-06-15-golden-visual-reference/analytics-dashboard-orbit-compact.png`

## Acceptance Notes
The number leads, the chart supports, and the underlying table remains available.
Charts must have an accessible description and table/text equivalent. Stale,
insufficient-data, loading, and failure states must be explicit.

## Known Limits
- This is benchmark evidence, not yet a production MarketIQ or RFP Analytics screen.
- Dedicated data-viz tokens do not exist yet; the benchmark uses existing semantic/status
  tokens as an interim path.
- Browser visual screenshots and rendered contrast evidence exist in benchmark artifacts;
  a production screenshot is still source-required.
