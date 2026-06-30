---
type: benchmark-browser-visual-accessibility-artifact
status: stable
owner: design-system
surfaces: [docs, benchmarks]
platform: shared
source: browser
last_reviewed: 2026-06-15
tags: [orbit, accessibility, benchmark, browser-visual]
---

# Browser Visual Accessibility Pass

Generated: 2026-06-15T12:35:05+01:00

Local target: `http://localhost:3001`

Overall verdict: **PASS after fixes**

## Tooling Inventory

| Tool | Used | Notes |
| ---- | ---- | ----- |
| Docs dev server | yes | `npm run dev -w @efficio/orbit-docs -- --port 3001` |
| In-app Browser | yes | Used for initial route inspection; screenshot capture fell back to CDP because sticky regions tiled in the in-app screenshot output. |
| Chrome DevTools Protocol | yes | Used for clean 1440x900 viewport screenshots and real `Tab` focus traversal. |
| Rendered CSS contrast sampler | yes | Sampled computed foreground/background pairs for key text, status, control, table, chart, and shell states. |
| axe / jest-axe / Playwright package | no | Not installed in the repo; no dependency added for this pass. |

## Route Results

| Route | Verdict | Theme / density | Focus-ring findings | Contrast findings |
| ----- | ------- | --------------- | ------------------- | ----------------- |
| `/design-system/benchmarks/clauseiq-results` | PASS | Efficio + Orbit; default + compact table rows verified | 14 main stops sampled per theme; no missing rings | Min 4.57:1 Efficio, 4.58:1 Orbit; 0 failures |
| `/design-system/benchmarks/form-validation` | PASS | Efficio + Orbit; comfortable + compact form density verified | 11 main stops sampled per theme; no missing rings | Min 5.69:1 Efficio, 4.58:1 Orbit; 0 failures |
| `/design-system/benchmarks/analytics-dashboard` | PASS | Efficio + Orbit; comfortable + compact dashboard/table density verified | 14 main stops sampled per theme; no missing rings | Min 4.60:1 Efficio, 4.58:1 Orbit; 0 failures |
| `/design-system/benchmarks/lovable-port` | PASS | Efficio + Orbit; comfortable + compact table density verified | 14 main stops sampled per theme; no missing rings | Min 4.82:1 Efficio, 4.58:1 Orbit; 0 failures |

## Screenshot Evidence

Directory:
`design-brain/_benchmarks/results/screenshots/2026-06-15-browser-visual-accessibility/`

| Route | Efficio default | Efficio compact | Orbit default | Orbit compact |
| ----- | --------------- | --------------- | ------------- | ------------- |
| ClauseIQ results | `clauseiq-results-efficio-default.png` | `clauseiq-results-efficio-compact.png` | `clauseiq-results-orbit-default.png` | `clauseiq-results-orbit-compact.png` |
| Form validation | `form-validation-efficio-default.png` | `form-validation-efficio-compact.png` | `form-validation-orbit-default.png` | `form-validation-orbit-compact.png` |
| Analytics dashboard | `analytics-dashboard-efficio-default.png` | `analytics-dashboard-efficio-compact.png` | `analytics-dashboard-orbit-default.png` | `analytics-dashboard-orbit-compact.png` |
| Lovable port | `lovable-port-efficio-default.png` | `lovable-port-efficio-compact.png` | `lovable-port-orbit-default.png` | `lovable-port-orbit-compact.png` |

Each screenshot was captured after verifying the expected `data-theme`, density switch,
`data-density`, pressed density button, or compact table class for that route.

## Focus-Ring Findings

Chrome CDP dispatched real `Tab` key events through the rendered pages. The focus sampler
checked the active element plus common visual proxies such as switch tracks.

- ClauseIQ: export, state buttons, search input, filter buttons, compact rows switch,
  sortable headers, row action, and pagination stops showed visible 2px Orbit focus rings.
- Form validation: compact density switch, reset/state buttons, text input, dropdown
  trigger, save action, and recovery controls showed visible 2px Orbit focus rings.
- Analytics dashboard: compact switch, export/refresh, state buttons, filter buttons,
  sortable table controls, and pagination showed visible 2px Orbit focus rings.
- Lovable port: export/add, tab, state/scope/density buttons, search/filter controls,
  table row actions, and pagination showed visible 2px Orbit focus rings.
- Docs shell navigation links sampled during traversal showed the shell-level Orbit focus
  ring after the focus-visible fix.

## Contrast Findings

Rendered CSS sampling checked both themes and both density states. Disabled controls were
excluded from AA failure counts.

- ClauseIQ: lowest sampled ratio after fixes was 4.57:1 in Efficio and 4.58:1 in Orbit.
- Form validation: lowest sampled ratio after fixes was 5.69:1 in Efficio and 4.58:1 in Orbit.
- Analytics dashboard: lowest sampled ratio after fixes was 4.60:1 in Efficio and 4.58:1 in Orbit.
- Lovable port: lowest sampled ratio after fixes was 4.82:1 in Efficio and 4.58:1 in Orbit.

## Issues Fixed

- Filled green/success/red/gray `Badge` foregrounds now use `--orbit-color-text-primary`
  where inverse white text failed AA on rendered fills.
- Efficio `--orbit-color-text-success` and `--orbit-color-text-warning` were darkened for
  small KPI/table delta text.
- Orbit `--orbit-color-text-success` was darkened so success deltas pass on Orbit
  information-tinted KPI cards.
- Efficio `--orbit-color-sidenav-muted` was raised from 3.56:1 to AA-compliant contrast
  against the sidenav background.
- The docs shell now applies a tokenized `:focus-visible` rule to links, buttons, and
  inputs, including the search input that previously removed the native outline.

## Design Brain Updates

- `design-brain/_benchmarks/accessibility-artifact-process.md` now requires a browser
  visual accessibility pass before benchmark acceptance.
- `design-brain/_benchmarks/agent-benchmark-tasks.md` records this browser pass and adds
  browser visual evidence to the required benchmark acceptance criteria.
- `design-brain/accessibility.md` now names the dated browser visual artifact as part of
  benchmark acceptance.
- `design-brain/components/badge-status.md` records the filled badge foreground contrast
  rule.
- `design-brain/patterns/analytics-dashboard.md` records AA requirements for KPI deltas
  and movement values.

## Remaining Manual Screen-Reader Checks

These checks were **not** performed and remain manual:

- Screen-reader announcement quality for validation summary, inline field errors, saved
  status, save error recovery, stale data, insufficient data, and load-failure states.
- Dialog announcement and focus return for ClauseIQ row detail.
- Tab announcement quality for the Lovable port tab interface.
- Table navigation verbosity and row/action announcements in a screen reader.
- Live-region timing for async save, refresh, retry, and state-preview changes.
