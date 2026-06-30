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
- Chart palette: use the semantic data-viz tokens only (`<viz-cat-1..n>`, `<viz-pos>`,
  `<viz-neg>`, `<viz-neutral>` — fill with your real token names). Never raw hex.
- Positive/negative encodings pair colour with sign/icon (a11y: never colour alone).
- Number formatting per `ux-copy.md` (currency, %, dates unambiguous, locale-aware).
- Empty/insufficient-data state: designed, with a reason and next action — never a blank axis.
- Loading: skeleton in final layout; no spinner-induced reflow.
- Tooltips: keyboard-reachable; data must also be available outside hover (table/summary).

## Chart choice quick rules
- Trend over time → line. Compare categories → horizontal bar (labels stay legible).
- Part-of-whole → stacked bar; pies only ≤ ~4 slices and only when proportion is the point.
- Distribution → histogram/box. Correlation → scatter.
- Avoid dual axes, 3D, radar, and decorative gradients in functional charts.

## KPI / scorecard blocks
Value, label, delta (with direction + period), and optional sparkline — in that priority.
Density-mode aware. Click-through to the detailed view where one exists.

## Don't
- ❌ Default library colours or default tooltips left unstyled.
- ❌ Charts that can't be understood in grayscale.
- ❌ Animating chart entry on every data refresh.
