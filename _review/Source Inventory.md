---
type: review
status: draft
owner: design-system
surfaces: [shared]
source: code
last_reviewed: 2026-06-15
maturity_score: 88
tags: [orbit, design-brain]
---

# Source Inventory

The real Orbit coded design-system repo is available at `the efficio-orbit repo`.
This inventory tracks which source-backed facts have been connected and which still need
product/design validation.

## Required Sources

| Source | Path or URL | Owner | Status |
| ------ | ----------- | ----- | ------ |
| Primitive tokens | `packages/orbit/styles/tokens/colors.css` | design-system | found |
| Semantic tokens | `packages/orbit/styles/tokens/semantics.css` | design-system | found |
| Component tokens | `packages/orbit/styles/tokens/components.css` | design-system | found |
| Efficio / CP base theme | `:root` in token files | design-system | found |
| Orbit theme | `packages/orbit/styles/tokens/themes/orbit.css` | design-system | found |
| Component library | `packages/orbit/src` | design-system | found |
| Component tests | `packages/orbit/src/**/*.test.tsx` | design-system | found |
| Static audit | `npm run audit:design-system` | design-system | found |
| Connected Platform profile | `design-brain/platforms/connected-platform.md` | design-system | specified; screenshots pending |
| Orbit / Client Connected Platform profile | `design-brain/platforms/orbit-client-connected-platform.md` | design-system | specified; screenshots pending |
| Connected Platform visual truth manifest | `design-brain/examples/screenshots/connected-platform/manifest.md` | design-system | source-required |
| Orbit / Client Connected Platform visual truth manifest | `design-brain/examples/screenshots/orbit-client-connected-platform/manifest.md` | design-system | source-required |
| ClauseIQ prototype | `apps/prototypes/components/feature/clauseiq/ClauseIQPrototype.tsx` | product/design | found |
| ClauseIQ prototype tests | `apps/prototypes/components/feature/clauseiq/ClauseIQPrototype.test.tsx` | product/design | found |
| ClauseIQ results benchmark | `apps/docs/app/design-system/benchmarks/clauseiq-results/ClauseIQResultsBenchmark.tsx` | design-system | benchmark source found |
| Procurement settings form benchmark | `apps/docs/app/design-system/benchmarks/form-validation/ProcurementSettingsBenchmark.tsx` | design-system | benchmark source found |
| MarketIQ analytics dashboard benchmark | `apps/docs/app/design-system/benchmarks/analytics-dashboard/MarketIQAnalyticsDashboardBenchmark.tsx` | design-system | benchmark source found |
| Lovable prototype source | `Test` | product/design | found |
| Lovable port benchmark | `apps/docs/app/design-system/benchmarks/lovable-port/LovablePortBenchmark.tsx` | design-system | benchmark source found |
| Lovable port review result | `design-brain/_benchmarks/results/2026-06-15-lovable-port-review.md` | design-system | benchmark result found |
| Benchmark accessibility command | `npm run bench:a11y` | design-system | found |
| Benchmark accessibility script | `scripts/run-benchmark-accessibility-artifacts.mjs` | design-system | found |
| Benchmark accessibility test | `test/benchmarks/accessibility-artifact.test.tsx` | design-system | found |
| Benchmark accessibility artifact | `design-brain/_benchmarks/results/2026-06-15-benchmark-accessibility-artifact.md` | design-system | generated |
| Browser visual accessibility artifact | `design-brain/_benchmarks/results/2026-06-15-browser-visual-accessibility.md` | design-system | generated |
| Browser visual accessibility screenshots | `design-brain/_benchmarks/results/screenshots/2026-06-15-browser-visual-accessibility/` | design-system | generated |
| Screen-reader accessibility artifact | `design-brain/_benchmarks/results/2026-06-15-screen-reader-accessibility.md` | design-system | needs human AT confirmation |
| Screen-reader accessibility summary | `design-brain/_benchmarks/results/2026-06-15-screen-reader-accessibility-summary.md` | design-system | needs human AT confirmation |
| Benchmark screenshot reference artifact | `design-brain/_benchmarks/results/2026-06-15-golden-visual-reference.md` | design-system | generated; not platform visual precedent |
| Benchmark screenshot reference images | `design-brain/_benchmarks/results/screenshots/2026-06-15-golden-visual-reference/` | design-system | generated; not platform visual precedent |
| Dedicated data-viz tokens | source-required | design-system | missing |
| Reusable drawer component | source-required | design-system | not found in `packages/orbit/src` |
| MarketIQ analytics screen | source-required | product/design | missing |
| RFP Analytics screen | source-required | product/design | missing |
| Storybook config | `packages/orbit/.storybook/` | design-system | found |
| Storybook usage guide | `design-brain/storybook.md` | design-system | found |
| Button stories | `packages/orbit/src/actions/Button.stories.tsx` | design-system | found |
| Stories for all other Orbit components | source-required | design-system | missing; 1 of 52 components has stories |
| Component-repo CI workflow | `.github/workflows/ci.yml` (component repo) | design-system | found; `verify` blocking, `known-issues` non-blocking |
| Published Storybook | GitHub Pages, component repo | design-system | pending — needs PR #1 merged and Pages set to "GitHub Actions" |
| Storybook status feed | `tools/fetch_storybook_status.py` | design-system | generated into `tools/storybook-status.json` |
| Connected Platform current screenshots | source-required | product/design | missing |
| Orbit / Client Connected Platform current screenshots | source-required | product/design | missing |

## Rule

Do not invent source-derived facts. If the source is missing, mark the contract section
as `specified` or `source-required` and add it to this inventory.

<!-- graph-links:start — generated by tools/gen_graph_links.py; do not hand-edit -->
## Vault graph
[[_benchmarks/results/2026-06-15-benchmark-accessibility-artifact|2026-06-15-benchmark-accessibility-artifact]] · [[_benchmarks/results/2026-06-15-browser-visual-accessibility|2026-06-15-browser-visual-accessibility]] · [[_benchmarks/results/2026-06-15-golden-visual-reference|2026-06-15-golden-visual-reference]] · [[_benchmarks/results/2026-06-15-lovable-port-review|2026-06-15-lovable-port-review]] · [[_benchmarks/results/2026-06-15-screen-reader-accessibility-summary|2026-06-15-screen-reader-accessibility-summary]] · [[_benchmarks/results/2026-06-15-screen-reader-accessibility|2026-06-15-screen-reader-accessibility]] · [[design-brain/examples/screenshots/connected-platform/manifest|connected-platform manifest]] · [[design-brain/examples/screenshots/orbit-client-connected-platform/manifest|orbit-client-connected-platform manifest]] · [[design-brain/platforms/connected-platform|connected-platform]] · [[design-brain/platforms/orbit-client-connected-platform|orbit-client-connected-platform]] · [[design-brain/storybook|storybook]]
<!-- graph-links:end -->
