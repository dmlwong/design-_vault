---
type: benchmark-result
status: stable
owner: design-system
surfaces: [ClauseIQ, shared]
source: code
last_reviewed: 2026-06-14
maturity_score: 80
tags: [orbit, design-brain, benchmark, clauseiq]
---

# Benchmark Result: ClauseIQ Results Table

## Task
Task 1: build a data-heavy results table with filters, sorting, row selection, loading,
empty, and error states using the Orbit Design Brain.

## Product Repo
`the efficio-orbit repo`

## Implementation
- Route:
  `apps/docs/app/design-system/benchmarks/clauseiq-results/page.tsx`
- Component:
  `apps/docs/app/design-system/benchmarks/clauseiq-results/ClauseIQResultsBenchmark.tsx`
- Styles:
  `apps/docs/app/design-system/benchmarks/clauseiq-results/ClauseIQResultsBenchmark.module.css`
- URL:
  `http://localhost:3000/design-system/benchmarks/clauseiq-results`

## Result
Reported benchmark score: **91/100 — PASS**.

## Verification Reported By Implementation Thread
- `npm run audit:design-system` passed with 27 checks.
- `npm run build:docs` passed.
- `npm run test:components` passed with 31 files and 123 tests.
- Browser checked search/filter, compact density, loading/empty/error states,
  detail dialog, disabled RBAC approval, Efficio/Orbit theme toggle, mobile viewport,
  and console logs.

## What Worked
- The agent used real Orbit components: `Table`, `Button`, `Overlay`, `Card`, and `Badge`.
- Styles were tokenized through Orbit CSS custom properties.
- The view included explicit loading, empty, error, disabled, compact, and detail states.
- Row selection labels and dialog behavior followed the component contracts.
- The exported Design Brain was sufficient for a high-quality first benchmark result.

## Deductions
- `focus-mode-results` was still marked as a draft/source gap.
- No formal axe or contrast audit was run beyond token, theme, and browser checks.
- The route is a benchmark/docs implementation, not yet a validated production product
  screen.

## Brain Updates Applied
- Exporter updated to include benchmark task files in product repos so future prompts can reference
  `design-brain/_benchmarks`.
- Record the benchmark route as evidence in `focus-mode-results`, while keeping the
  production-screen gap open.
- Raise the Design Brain maturity estimate, but do not treat one benchmark pass as the
  full 85-90 target.
