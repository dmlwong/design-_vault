---
type: benchmark-screenshot-reference
status: in-review
owner: design-system
surfaces: [docs, benchmarks]
platform: shared
source: browser
last_reviewed: 2026-06-15
maturity_score: 78
tags: [orbit, design-brain, benchmark, screenshot-reference, screenshots]
---

# Benchmark Screenshot Reference Pack

Generated: 2026-06-15

Local target: `http://localhost:3001`

Screenshot directory:
`design-brain/_benchmarks/results/screenshots/2026-06-15-golden-visual-reference/`

Overall verdict: **suitable as benchmark evidence only; not platform visual precedent**

## Reclassification Note

These screenshots are useful because they document the benchmark routes, theme switching,
density controls, and component compositions in a repeatable browser capture. They are
not canonical visual precedent for the current platform. Do not use them to decide the
final Orbit product look if they conflict with live product screens, current Storybook,
or design-system owner guidance.

## Capture Method

- Started the docs app with `npm run dev -w @efficio/orbit-docs -- -p 3001`
  because port `3000` was already occupied by another local server.
- Used the in-app Browser for route inspection and control verification.
- Replaced the in-app screenshot output with headless Chrome DevTools Protocol capture
  after the in-app screenshot API tiled sticky shell regions.
- Captured clean viewport screenshots at `1440x900` CSS pixels with
  `devicePixelRatio: 1`, `captureBeyondViewport: false`, and `Page.captureScreenshot`.
- Before each screenshot, the script navigated fresh to the route, waited for the route
  heading and fonts, clicked the requested theme, clicked the density control, then
  verified the rendered `data-theme`, switch/button pressed state, and any
  `data-density` attributes.

## Screenshot Inventory

| Route | Theme | Density | Screenshot | Suitable |
| ----- | ----- | ------- | ---------- | -------- |
| `/design-system/benchmarks/clauseiq-results` | Efficio | Default rows | `clauseiq-results-efficio-default.png` | Yes |
| `/design-system/benchmarks/clauseiq-results` | Efficio | Compact rows | `clauseiq-results-efficio-compact.png` | Yes |
| `/design-system/benchmarks/clauseiq-results` | Orbit | Default rows | `clauseiq-results-orbit-default.png` | Yes |
| `/design-system/benchmarks/clauseiq-results` | Orbit | Compact rows | `clauseiq-results-orbit-compact.png` | Yes |
| `/design-system/benchmarks/form-validation` | Efficio | Default / comfortable | `form-validation-efficio-default.png` | Yes |
| `/design-system/benchmarks/form-validation` | Efficio | Compact | `form-validation-efficio-compact.png` | Yes |
| `/design-system/benchmarks/form-validation` | Orbit | Default / comfortable | `form-validation-orbit-default.png` | Yes |
| `/design-system/benchmarks/form-validation` | Orbit | Compact | `form-validation-orbit-compact.png` | Yes |
| `/design-system/benchmarks/analytics-dashboard` | Efficio | Default / comfortable | `analytics-dashboard-efficio-default.png` | Yes |
| `/design-system/benchmarks/analytics-dashboard` | Efficio | Compact | `analytics-dashboard-efficio-compact.png` | Yes |
| `/design-system/benchmarks/analytics-dashboard` | Orbit | Default / comfortable | `analytics-dashboard-orbit-default.png` | Yes |
| `/design-system/benchmarks/analytics-dashboard` | Orbit | Compact | `analytics-dashboard-orbit-compact.png` | Yes |
| `/design-system/benchmarks/lovable-port` | Efficio | Default / comfortable | `lovable-port-efficio-default.png` | Yes |
| `/design-system/benchmarks/lovable-port` | Efficio | Compact | `lovable-port-efficio-compact.png` | Yes |
| `/design-system/benchmarks/lovable-port` | Orbit | Default / comfortable | `lovable-port-orbit-default.png` | Yes |
| `/design-system/benchmarks/lovable-port` | Orbit | Compact | `lovable-port-orbit-compact.png` | Yes |

## Coverage Notes

All four benchmark routes support both docs-shell themes:

- Efficio base theme through `:root`.
- Orbit theme through `[data-theme="orbit"]`.

All four routes expose density controls:

- ClauseIQ results: `Compact rows` switch maps to Orbit `Table` density.
- Form validation: `Compact density` switch maps to compact form composition.
- Analytics dashboard: `Compact density` switch maps to compact KPI/chart layout and
  Orbit `Table` density.
- Lovable port: `Table density` button group maps to comfortable/compact Orbit `Table`
  density.

## Visual Defects Noticed

- **Non-blocking:** wide table routes expose horizontal overflow at a `1440px` viewport.
  This is expected for dense benchmark tables and is visible as a bottom horizontal
  scrollbar in the first-viewport screenshots. The screenshots remain suitable for
  theme, density, layout rhythm, and component precedent, but they are not full-table
  captures.
- **Capture tooling issue, resolved:** the in-app Browser screenshot output tiled sticky
  shell regions. Those files were overwritten with clean headless Chrome CDP captures.

No product behavior changes were made from this pass.

## Benchmark Suitability

These screenshots are suitable as benchmark evidence for future agents because they show:

- real benchmark routes rather than idealized mockups;
- Efficio and Orbit theme token differences from the same component logic;
- comfortable/default and compact density variants;
- dense enterprise procurement layouts with state controls visible in the first
  viewport;
- token-backed Orbit components in page-level compositions.

Use the linked example files in `design-brain/examples/` for route-specific benchmark
guidance only. For visual direction, prefer current platform screenshots or
Storybook-equivalent references once they are available.
