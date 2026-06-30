---
type: benchmark-result
status: in-review
owner: design-system
surfaces: [shared]
source: code
last_reviewed: 2026-06-15
maturity_score: 84
tags: [orbit, design-brain, benchmark, review, lovable-port]
---

# Benchmark Result: Lovable Port Review

## Task
Task 5: review the finished Lovable port screen against the Orbit Design Brain. Give
PASS/FAIL, blockers, major issues, minor issues, contract gaps, benchmark rubric score,
and recommended Design Brain updates. If real issues are found, fix them, update the
relevant Design Brain files, and run the required validation commands.

## Product Repo
`the efficio-orbit repo`

## Reviewed Files
- `apps/docs/app/design-system/benchmarks/lovable-port/LovablePortBenchmark.tsx`
- `apps/docs/app/design-system/benchmarks/lovable-port/LovablePortBenchmark.module.css`
- `apps/docs/app/design-system/benchmarks/lovable-port/page.tsx`

## Required References Read
- `AGENTS.md`
- `design-brain/agents/design-reviewer.md`
- `design-brain/patterns/lovable-port.md`
- `design-brain/examples/lovable-initiatives-port.md`
- `design-brain/components/data-table.md`
- `design-brain/components/button.md`
- `design-brain/components/select-combobox.md`
- `design-brain/components/tabs.md`
- `design-brain/components/badge-status.md`
- `design-brain/components/card-panel.md`
- `design-brain/accessibility.md`
- `design-brain/tokens.md`
- `design-brain/anti-patterns.md`
- `design-brain/_benchmarks/agent-benchmark-tasks.md`

## Review Verdict
**PASS after fixes.**

Initial review found real accessibility and state-consistency issues, but none remained
as blockers after targeted fixes.

## Score
Final benchmark score: **18/18 - PASS**.

| Category | Score | Notes |
| -------- | ----- | ----- |
| Tokens only | 2 | Route uses Orbit CSS custom properties and Orbit component tokens. Targeted raw-value scan found no raw `hex`, `px`, `rem`, `rgba`, or `oklch` usage in the benchmark route. |
| Theme support | 2 | Implementation is token-driven and was previously checked in Efficio and Orbit theme modes. No theme-conditional component logic was found. |
| Full states | 2 | Data, loading, empty, error, no-permission, active filters, selected detail, comfortable density, and compact density are present. Loading now preserves active density. |
| Accessibility | 2 | Native table semantics, row-specific action labels, resource hidden text, `aria-pressed` groups, labelled loading status, alert error state, and visible text status/stage labels are present after fixes. |
| Density | 2 | Comfortable and compact density are supported by the visible table and loading skeleton table. |
| Contract match | 2 | Uses real Orbit `PageHeader`, `Table`, `Searchbox`, `Dropdown`, `Button`, `Badge`, `Card`, `Text`, `Headings`, and `FaIcon` APIs. |
| Pattern match | 2 | Matches `lovable-port` pattern after clarifying row action labels, resource initials, and loading density. |
| Copy and motion | 2 | Copy is clear and procurement-contextual. No decorative motion was introduced. |
| Orbit feel | 2 | Dense, restrained, procurement-first workflow. No generic ShadCN/Tailwind look remains. |

Total: `18/18`

## Blockers
None remaining.

## Major Issues Found And Fixed
1. Resource initials did not expose the full resource list robustly.
   - Original issue: resource initials relied on `aria-label` on a generic span, which
     is not a dependable accessible-name strategy for static table content.
   - Fix: moved the full resource list into visually hidden text inside the cell, while
     keeping visual initials `aria-hidden`.

2. Repeated row action buttons had generic accessible names.
   - Original issue: every row exposed visible `View` and `Edit` button text. For
     screen reader and keyboard users, repeated row actions need row identity.
   - Fix: added row-specific accessible labels, such as
     `View initiative AUT01-2000 AB test 1` and
     `Edit initiative AUT01-2000 AB test 1`.

## Minor Issues Found And Fixed
1. Loading state ignored active density.
   - Original issue: the loading table always rendered `density="Compact"`, even when
     the visible table was in comfortable density.
   - Fix: passed the active table density into the loading table so skeleton state
     preserves scanning context.

## Contract Gaps Noticed
- No contracted menu / checkbox-list pattern exists for granular column visibility.
- No Avatar or resource-stack contract exists for people/resource table cells.
- No virtualized table contract exists. The current Orbit `Table` contract supports
  pagination, not virtualization.
- No formal axe/contrast artifact is required by the benchmark template, so full
  accessibility evidence is still manual follow-up rather than a scored requirement.

## Design Brain Updates Applied
- `design-brain/patterns/lovable-port.md` now requires loading states to match final
  layout shape, current columns, and current density.
- `design-brain/patterns/lovable-port.md` now requires row-local actions like `View`
  and `Edit` to include row identity in accessible names.
- `design-brain/patterns/lovable-port.md` now requires compact people/resource
  abbreviations to include full hidden text in the same cell.
- `design-brain/examples/lovable-initiatives-port.md` now records those acceptance
  notes for future ports.
- `design-brain/accessibility.md` now captures these table/accessibility rules
  generically.
- `design-brain/agents/design-reviewer.md` now includes dense-table review traps.
- `_benchmarks/agent-benchmark-tasks.md` now records the Task 5 pass.
- `_review/Maturity Scorecard.md` and `README.md` now reflect the five-benchmark pass
  and current 86/100 estimate.

## Verification Reported By Implementation Thread
- `npm run audit:design-system` passed with 27 checks.
- `npm run lint` passed.
- `npm run build:docs` passed and prerendered
  `/design-system/benchmarks/lovable-port`.
- Browser verification on `http://localhost:3001/design-system/benchmarks/lovable-port`
  confirmed row-specific `View`/`Edit` accessible labels, resource full text in the
  table cell, compact density following into the loading table, and no fresh console
  errors.

Environment note: port `3000` was occupied by a stale Node server returning `404` for
the benchmark route during review, so verification used port `3001`.

## Open Brain Updates
- Decide whether to add a formal `menu-checkbox-list` or `column-visibility-menu`
  contract for granular table column controls.
- Decide whether resource initials belong in an Avatar contract, a table-cell pattern,
  or a procurement-specific composition.
- Decide whether future Lovable ports should score down when virtualization is replaced
  by pagination, or whether current `Table` contract alignment is sufficient.
- Add formal axe/contrast capture expectations to Task 5 or the scorecard template.

## Suggested Validation Questions
- Should row-local actions always require visible row identity nearby, or is an
  `aria-label` sufficient when the action sits inside a native table row?
- Should compact resource initials be allowed as page-local composition before an
  Avatar/resource-stack contract exists?
- Should loading states always mirror active density and column set for all table
  patterns, or only for ported external prototypes?
- Should a formal browser accessibility scan be required before any benchmark can score
  `Accessibility = 2`?
