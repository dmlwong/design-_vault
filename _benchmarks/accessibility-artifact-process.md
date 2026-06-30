---
type: benchmark
status: stable
owner: design-system
surfaces: [docs, benchmarks]
source: code
last_reviewed: 2026-06-15
maturity_score: 88
tags: [orbit, design-brain, accessibility, benchmark]
---

# Benchmark Accessibility Artifact Process

Run this process before accepting a benchmark route as PASS.

## Command
From `the efficio-orbit repo`:

```bash
npm run bench:a11y
```

To write a named artifact:

```bash
npm run bench:a11y -- --artifact design-brain/_benchmarks/results/YYYY-MM-DD-benchmark-accessibility-artifact.md
```

## Browser Visual Accessibility Pass
Generated benchmark artifacts are necessary but not sufficient for acceptance. Before a
benchmark route can be marked PASS, also run a real-browser visual pass and save a dated
markdown artifact:

```bash
design-brain/_benchmarks/results/YYYY-MM-DD-browser-visual-accessibility.md
```

The browser pass must cover each benchmark route in both docs-shell themes where
supported and in comfortable/default plus compact density where available. Capture
screenshots, verify theme and density state before each capture, tab through key
controls in a real browser, inspect rendered focus-ring styles, and sample rendered CSS
contrast for key text, status, and control states.

## Manual Screen-Reader Accessibility Pass
Generated and browser visual artifacts do not complete the screen-reader gate. Before a
benchmark route can be marked fully PASS, save a separate dated markdown artifact:

```bash
design-brain/_benchmarks/results/YYYY-MM-DD-screen-reader-accessibility.md
```

Record one of these outcomes:

- **PASS:** VoiceOver, NVDA, JAWS, or another agreed screen reader was actually used and
  the spoken output passed the checklist.
- **FAIL:** assistive-technology testing found a blocker or major issue.
- **NEEDS HUMAN CONFIRMATION:** browser DOM, accessibility-tree, CDP, or automated
  checks passed, but no real screen-reader session confirmed the spoken output.

The screen-reader artifact should cover validation announcements, saved/error recovery,
dialogs, tabs, dense-table navigation, row-local action names, and live-region timing
for loading, retry, refresh, stale, selected-detail, and state-preview changes.

## Current Implementation
The command uses the existing repo stack:
- Vitest.
- Testing Library.
- jsdom.
- `dom-accessibility-api`.

No Playwright, axe, jest-axe, or `@axe-core/playwright` dependency is required for the
current gate.

Source files:
- `scripts/run-benchmark-accessibility-artifacts.mjs`
- `test/benchmarks/accessibility-artifact.test.tsx`
- `vitest.benchmark-a11y.config.ts`

## Automated Checks
The current artifact verifies:
- One `main` landmark and at least one level-one page heading.
- Duplicate IDs.
- Broken ARIA ID references.
- Computed accessible names for controls, tables, tab panels, and meaningful images.
- Known ARIA role values.
- No tabbable descendants inside `aria-hidden` content.
- Sequential keyboard Tab reachability for every tabbable element in the rendered route.

## Required Artifact Content
The generated markdown must include:
- PASS/FAIL per benchmark route.
- Tooling inventory, including whether Playwright or axe-family tools are available.
- Automated checks run.
- Violations found.
- Remaining manual checks.

## Manual Checks Still Required
The artifact is not a complete browser accessibility audit. Still verify:
- Visible focus ring styling in a real browser for every keyboard stop.
- WCAG 2.2 AA contrast in both `efficio` and `orbit` themes with rendered CSS.
- Compact and comfortable density target sizes visually.
- axe/Playwright results if that stack is intentionally added later.

If the browser visual pass finds real issues, fix the source component, token, pattern,
or benchmark route before acceptance. Record manual screen-reader checks separately; do
not mark them done unless they were actually performed with assistive technology.
