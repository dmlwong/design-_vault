---
type: benchmark-summary
status: stable
owner: design-system
surfaces: [docs, benchmarks]
source: browser
last_reviewed: 2026-06-15
maturity_score: 88
tags: [orbit, accessibility, benchmark, browser-visual]
---

# Browser Visual Accessibility Pass Summary

Date: 2026-06-15

Full artifact:
`design-brain/_benchmarks/results/2026-06-15-browser-visual-accessibility.md`

Screenshot directory:
`design-brain/_benchmarks/results/screenshots/2026-06-15-browser-visual-accessibility/`

Overall result: **PASS after fixes**

## Scope

Routes checked:

- `/design-system/benchmarks/clauseiq-results`
- `/design-system/benchmarks/form-validation`
- `/design-system/benchmarks/analytics-dashboard`
- `/design-system/benchmarks/lovable-port`

Each route was checked in Efficio and Orbit themes, plus default/comfortable and compact
density states where supported.

## Results

| Route | Verdict | Focus rings | Contrast | Theme / density |
| ----- | ------- | ----------- | -------- | --------------- |
| ClauseIQ results | PASS | 14 main stops per theme; no missing rings | Min 4.57:1 Efficio, 4.58:1 Orbit | Verified |
| Form validation | PASS | 11 main stops per theme; no missing rings | Min 5.69:1 Efficio, 4.58:1 Orbit | Verified |
| Analytics dashboard | PASS | 14 main stops per theme; no missing rings | Min 4.60:1 Efficio, 4.58:1 Orbit | Verified |
| Lovable port | PASS | 14 main stops per theme; no missing rings | Min 4.82:1 Efficio, 4.58:1 Orbit | Verified |

## Issues Fixed

- Filled `Badge` foreground contrast for green, success, red, and gray variants.
- Efficio success and warning text tokens for small KPI/table delta text.
- Orbit success text token for analytics KPI deltas.
- Efficio sidenav muted text contrast.
- Docs shell `:focus-visible` styling for links, buttons, and inputs.

## Design Brain Updates

- Browser visual accessibility pass is now part of benchmark acceptance.
- Badge status contract now documents filled badge contrast behavior.
- Analytics dashboard pattern now requires AA contrast for KPI deltas and movement
  values.
- Token guidance now flags contrast-sensitive text and sidenav tokens.

## Verification Commands

All passed:

- `npm run bench:a11y`
- `npm run audit:design-system`
- `npm run lint`
- `npm run build:docs`

## Remaining Manual Checks

Manual screen-reader checks were not performed. Remaining checks include announcement
quality for validation/errors/status, ClauseIQ dialog behavior, Lovable tabs, table
navigation verbosity, and live-region timing.
