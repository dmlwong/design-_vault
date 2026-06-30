---
type: benchmark-accessibility-artifact
status: stable
owner: design-system
surfaces: [docs, benchmarks]
source: generated
last_reviewed: 2026-06-15
tags: [orbit, accessibility, benchmark]
---

# Benchmark Accessibility Artifact

Generated: 2026-06-15T12:47:52.057Z

Command: `npm run bench:a11y -- --artifact design-brain/_benchmarks/results/2026-06-15-benchmark-accessibility-artifact.md`

Overall verdict: **PASS**

## Tooling Inventory

| Tool | Available | Used | Notes |
| ---- | --------- | ---- | ----- |
| Vitest + Testing Library + jsdom | yes | yes | Existing repo test stack. |
| dom-accessibility-api | yes | yes | Used for computed accessible names. |
| Playwright | no | no | Not a project dependency for this pass. |
| axe / jest-axe / @axe-core/playwright | no | no | Not installed; no new dependency added. |

## Automated Checks

- One main landmark and at least one level-one page heading.
- Duplicate IDs and broken ARIA ID references.
- Computed accessible names for controls, tables, tab panels, and meaningful images.
- Known role attribute values.
- No tabbable descendants inside `aria-hidden` content.
- Sequential keyboard Tab pass reaches every tabbable element in the rendered route.

## Route Results

| Route | Verdict | Keyboard stops | Named elements | ARIA refs | Roles | Tables | Violations |
| ----- | ------- | -------------- | -------------- | --------- | ----- | ------ | ---------- |
| /design-system/benchmarks/clauseiq-results | PASS | 27/27 | 31 | 2 | 5 | 1 | 0 |
| /design-system/benchmarks/form-validation | PASS | 11/11 | 11 | 6 | 3 | 0 | 0 |
| /design-system/benchmarks/analytics-dashboard | PASS | 20/20 | 23 | 4 | 14 | 1 | 0 |
| /design-system/benchmarks/lovable-port | PASS | 83/83 | 98 | 21 | 20 | 1 | 0 |

## Violations

### ClauseIQ results table

Route: `/design-system/benchmarks/clauseiq-results`

No automated violations found.

### Procurement settings form

Route: `/design-system/benchmarks/form-validation`

No automated violations found.

### MarketIQ analytics dashboard

Route: `/design-system/benchmarks/analytics-dashboard`

No automated violations found.

### Lovable initiatives port

Route: `/design-system/benchmarks/lovable-port`

No automated violations found.

## Remaining Manual Checks

- Verify visible focus ring styling in a real browser for every keyboard stop.
- Verify WCAG 2.2 AA contrast in both `efficio` and `orbit` themes with rendered CSS.
- Verify compact and comfortable density target sizes visually.
- Verify screen reader announcement quality for async status, alerts, dialogs, and tab changes.
- Run axe/Playwright when that stack becomes a project dependency or the benchmark gate is expanded.

