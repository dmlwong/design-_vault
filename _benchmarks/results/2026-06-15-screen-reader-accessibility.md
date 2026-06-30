---
type: benchmark-screen-reader-accessibility-artifact
status: stable
owner: design-system
surfaces: [docs, benchmarks]
source: manual-prep
last_reviewed: 2026-06-15
tags: [orbit, accessibility, benchmark, screen-reader]
---

# Manual Screen-Reader Accessibility Pass

Generated: 2026-06-15T13:44:15+01:00

Local target: `http://localhost:3002`

Overall screen-reader verdict: **NEEDS HUMAN CONFIRMATION after fixes**

This pass prepared and exercised the manual checklist, fixed code-level announcement
issues found through rendered-browser semantic checks, and documented the remaining
assistive-technology run. It was **not** completed with macOS VoiceOver, NVDA, or JAWS.

## Tooling Inventory

| Tool | Used | Notes |
| ---- | ---- | ----- |
| Docs dev server | yes | `npm run dev -w @efficio/orbit-docs -- --port 3002` |
| macOS VoiceOver | no | VoiceOver is installed but not running. `System Events` accessibility control returned `false`, so scripted VoiceOver/manual control was not available to this process. |
| In-app Browser | attempted | The Next route crashed in the in-app browser tab, so verification moved to local Chrome. |
| Local Chrome + CDP | yes | Used to exercise rendered controls and inspect live regions, alerts, dialogs, focus return, tab semantics, table labels, and row/action names. |
| Automated benchmark artifact | yes | `npm run bench:a11y -- --artifact design-brain/_benchmarks/results/2026-06-15-benchmark-accessibility-artifact.md` passed after fixes. |

## Route Verdicts

| Route | Screen-reader verdict | Supporting semantic result | Notes |
| ----- | --------------------- | -------------------------- | ----- |
| `/design-system/benchmarks/clauseiq-results` | NEEDS HUMAN CONFIRMATION | PASS after fixes | Dialog semantics, focus trap/return, row names, table sort state, loading/error live text verified in rendered Chrome. |
| `/design-system/benchmarks/form-validation` | NEEDS HUMAN CONFIRMATION | PASS after fixes | Validation summary, inline error references, saved status, save error alert, retry status, and loading status verified in rendered Chrome. |
| `/design-system/benchmarks/analytics-dashboard` | NEEDS HUMAN CONFIRMATION | PASS after fixes | Loading, retry, refresh, stale, failure, table sort state, and alert/status semantics verified in rendered Chrome. |
| `/design-system/benchmarks/lovable-port` | NEEDS HUMAN CONFIRMATION | PASS after fixes | Tab labels/panels, loading/error/retry, row action names, selected detail status, and stage-change status verified in rendered Chrome. |

## Checklist Results

| Check | Result | Evidence |
| ----- | ------ | -------- |
| Validation summary and inline errors | Semantic PASS; needs human announcement confirmation | Form validation state exposes one summary `role="alert"`, invalid input/dropdown controls, and `aria-describedby` links to field help/error text. Inline field errors no longer add separate assertive alerts. |
| Saved status and save error recovery | Semantic PASS; needs human timing confirmation | Successful save exposes a single polite status: `Settings saved for future RFPs.` Save error exposes alert copy and `Retry save`; retry returns `Procurement settings ready for editing.` |
| ClauseIQ dialog announcement and focus return | Semantic PASS; needs human announcement confirmation | Focused row activation opens `role="dialog"` with `aria-modal="true"` and title `Liability cap`; close returns focus to `Open finding CIQ-001, Liability cap, row 2`. |
| Lovable tab announcement quality | Semantic PASS; needs human announcement confirmation | Tabs expose `role="tab"`, `aria-selected`, `aria-controls`, mounted matching panels, and badge tab name `My QC tasks, 2 items`. |
| Table navigation verbosity and row/action announcements | Semantic PASS; needs human table-navigation confirmation | Tables expose names/labels; active sorted headers expose `aria-sort`; sort buttons use full direction words; row-local buttons include row identity such as `Open finding CIQ-001, Liability cap, row 2` and `Edit initiative AUT01-2000 AB test 1`. |
| Live-region timing for loading, retry, refresh, and state-preview changes | Semantic PASS; needs human timing confirmation | Route-level and state-level statuses now announce data, empty, loading, error, retry, refresh, stale, selected-detail, and stage-change states without wrapping whole skeleton tables in live regions. |

## Issues Found And Fixed

- Filled in missing route-level live-region announcements for benchmark state preview changes.
- Removed duplicate assertive validation noise by keeping the validation summary as the alert and leaving inline field errors as `aria-describedby` text.
- Removed duplicate saved-status announcement on the form benchmark.
- Added `role="alert"` to the ClauseIQ error recovery state.
- Added `aria-sort` to active table headers and changed sort button labels from abbreviated directions to full words.
- Improved PageHeader badge-tab naming so `My QC tasks` announces as `My QC tasks, 2 items`.
- Added MarketIQ refresh/retry completion announcements.
- Added Lovable selected-row and stage-change announcements.
- Hid loading skeleton tables/charts from live-region text and exposed concise loading statuses instead.

## Remaining Human-Only Checks

- Run macOS VoiceOver, NVDA, or JAWS on all four routes and confirm the exact spoken output.
- Confirm validation summary is announced once on submit and inline field errors are discoverable when each invalid field receives focus.
- Confirm saved, save error, retry, loading, refresh, stale, selected-detail, and stage-change announcements are neither dropped nor repeated excessively.
- Confirm ClauseIQ dialog title and modal context are spoken on open, Escape/close behavior is understandable, and focus return is spoken correctly.
- Confirm Lovable tab navigation announces selected state, badge count, and panel context naturally.
- Confirm table reading mode is not too verbose for dense rows and that row-local actions remain understandable in screen-reader table navigation.

## Design Brain Updates

- `design-brain/accessibility.md` now requires a separate screen-reader artifact for benchmark routes.
- `design-brain/_benchmarks/accessibility-artifact-process.md` now defines the manual screen-reader artifact and PASS/FAIL/NEEDS HUMAN CONFIRMATION outcomes.
- `design-brain/_benchmarks/agent-benchmark-tasks.md` now tracks the screen-reader pass separately from generated and browser visual artifacts.
- `design-brain/_benchmarks/scorecard-template.md` now includes a screen-reader artifact field.
- `design-brain/agents/design-reviewer.md` now requires the screen-reader artifact for benchmark route reviews.
- `design-brain/components/data-table.md` now records `aria-sort` and full direction sort labels.
- `design-brain/components/tabs.md` now records badge-count accessible naming.
