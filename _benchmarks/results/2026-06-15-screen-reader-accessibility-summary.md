---
type: benchmark-screen-reader-accessibility-summary
status: stable
owner: design-system
surfaces: [docs, benchmarks]
source: manual-prep
last_reviewed: 2026-06-15
tags: [orbit, accessibility, benchmark, screen-reader, summary]
---

# Screen-Reader Accessibility Pass Summary

Detailed artifact:
`design-brain/_benchmarks/results/2026-06-15-screen-reader-accessibility.md`

Overall verdict: **NEEDS HUMAN CONFIRMATION after fixes**

## Scope

Routes reviewed:

- `/design-system/benchmarks/clauseiq-results`
- `/design-system/benchmarks/form-validation`
- `/design-system/benchmarks/analytics-dashboard`
- `/design-system/benchmarks/lovable-port`

## What Was Completed

- Prepared a repeatable screen-reader checklist for all four benchmark routes.
- Attempted macOS VoiceOver availability; VoiceOver was installed but not running, and
  this process did not have macOS Accessibility control permission.
- Used rendered Chrome/CDP checks as supporting evidence for live regions, alerts,
  dialogs, focus return, tab semantics, table labels, sort state, and row/action names.
- Fixed code-level announcement and semantics issues found during the pass.
- Updated the Design Brain so screen-reader checks are tracked separately from generated
  and browser visual accessibility artifacts.

## Route Results

| Route | Result |
| ----- | ------ |
| ClauseIQ results | NEEDS HUMAN CONFIRMATION; semantic checks pass after fixes. |
| Form validation | NEEDS HUMAN CONFIRMATION; semantic checks pass after fixes. |
| Analytics dashboard | NEEDS HUMAN CONFIRMATION; semantic checks pass after fixes. |
| Lovable port | NEEDS HUMAN CONFIRMATION; semantic checks pass after fixes. |

## Fixes Made

- Added concise live-region announcements for benchmark state changes.
- Reduced duplicate form validation announcements.
- Kept inline field errors linked through `aria-describedby`.
- Removed duplicate form saved/loading announcements.
- Added ClauseIQ error alert semantics.
- Added `aria-sort` to active table headers.
- Changed table sort labels to full direction words.
- Added accessible count naming for badge tabs.
- Added MarketIQ retry/refresh announcements.
- Added Lovable selected-row and stage-change announcements.
- Hid loading skeleton tables/charts from live-region text.

## Verification

Commands passed:

```bash
npm run bench:a11y
npm run audit:design-system
npm run lint
npm run build:docs
```

## Remaining Human Checks

- Run VoiceOver, NVDA, or JAWS on all four routes.
- Confirm exact spoken output for validation, save, error recovery, loading, retry,
  refresh, stale, selected-detail, and stage-change states.
- Confirm ClauseIQ dialog title, modal context, close behavior, and focus return.
- Confirm Lovable tab selected state, badge count, and panel context announcements.
- Confirm dense table navigation verbosity and row-local action names in screen-reader
  table navigation.
