---
type: benchmark-summary
status: stable
owner: design-system
surfaces: [docs, benchmarks]
source: specified
last_reviewed: 2026-06-15
tags: [orbit, accessibility, benchmark, summary]
---

# Benchmark Accessibility Pass Summary

Date: 2026-06-15

Artifact: `design-brain/_benchmarks/results/2026-06-15-benchmark-accessibility-artifact.md`

## Scope

Reviewed the benchmark routes:

- `/design-system/benchmarks/clauseiq-results`
- `/design-system/benchmarks/form-validation`
- `/design-system/benchmarks/analytics-dashboard`
- `/design-system/benchmarks/lovable-port`

## Process Added

Created a repeatable accessibility artifact command:

```bash
npm run bench:a11y
```

The process uses the existing repo stack:

- Vitest
- Testing Library
- jsdom
- `dom-accessibility-api`

No new accessibility dependency was added. Playwright, axe, jest-axe, and
`@axe-core/playwright` were not installed as project dependencies.

## Automated Checks

The artifact pass checks:

- One `main` landmark and at least one level-one page heading
- Duplicate IDs
- Broken ARIA ID references
- Computed accessible names for controls, tables, tab panels, and meaningful images
- Known ARIA role values
- No tabbable descendants inside `aria-hidden` content
- Sequential keyboard Tab reachability for every tabbable element in the rendered route

## Route Verdicts

| Route | Verdict | Violations |
| ----- | ------- | ---------- |
| `/design-system/benchmarks/clauseiq-results` | PASS | 0 |
| `/design-system/benchmarks/form-validation` | PASS | 0 |
| `/design-system/benchmarks/analytics-dashboard` | PASS | 0 |
| `/design-system/benchmarks/lovable-port` | PASS | 0 |

## Issue Found And Fixed

Initial run found broken `aria-controls` references in the Lovable port benchmark.
Inactive tabs pointed to panel IDs that were not mounted in the DOM.

Fix:

- Mounted hidden tab panels for inactive Lovable benchmark tabs.
- Preserved the active tab panel content and visual behavior.
- Verified the route with the generated artifact and a browser smoke check.

## Design Brain Updates

Updated the benchmark and reviewer guidance so future benchmark reviews require the
formal accessibility artifact:

- `design-brain/_benchmarks/agent-benchmark-tasks.md`
- `design-brain/_benchmarks/scorecard-template.md`
- `design-brain/agents/design-reviewer.md`

## Commands Run

```bash
npm run bench:a11y -- --artifact design-brain/_benchmarks/results/2026-06-15-benchmark-accessibility-artifact.md
npm run audit:design-system
npm run lint
npm run build:docs
```

All commands passed.

## Remaining Manual Checks

- Verify visible focus ring styling in a real browser for every keyboard stop.
- Verify WCAG 2.2 AA contrast in both `efficio` and `orbit` themes with rendered CSS.
- Verify compact and comfortable density target sizes visually.
- Verify screen reader announcement quality for async status, alerts, dialogs, and tab changes.
- Run axe or Playwright checks if that stack is intentionally added to the project.
