---
type: benchmark-result
status: in-review
owner: design-system
surfaces: [RFP Builder, shared]
source: code
last_reviewed: 2026-06-15
maturity_score: 78
tags: [orbit, design-brain, benchmark, forms, validation]
---

# Benchmark Result: Procurement Settings Form

## Task
Task 2: build a procurement settings form with text input, select/combobox, help text,
validation, disabled permission state, loading, and error recovery using the Orbit Design
Brain.

## Product Repo
`the efficio-orbit repo`

## Required References Read
- `design-brain/components/input.md`
- `design-brain/components/select-combobox.md`
- `design-brain/examples/form-field-validation.md`
- `design-brain/ux-copy.md`
- `design-brain/accessibility.md`
- `design-brain/tokens.md`
- `design-brain/_benchmarks/agent-benchmark-tasks.md`

## Implementation
- Route:
  `apps/docs/app/design-system/benchmarks/form-validation/page.tsx`
- Component:
  `apps/docs/app/design-system/benchmarks/form-validation/ProcurementSettingsBenchmark.tsx`
- Styles:
  `apps/docs/app/design-system/benchmarks/form-validation/ProcurementSettingsBenchmark.module.css`
- Docs index link:
  `apps/docs/app/design-system/page.tsx`
- Supporting component API change:
  `packages/orbit/src/inputs/Input.tsx`
- Supporting component test:
  `packages/orbit/src/inputs/Input.test.tsx`
- Verified URL:
  `http://localhost:3001/design-system/benchmarks/form-validation`

Port `3001` was used for verification because port `3000` was already running an older
docs server that returned `404` for the new route.

## Result
Reported benchmark score: **17/18 - PASS**.

| Category | Score | Notes |
| -------- | ----- | ----- |
| Tokens only | 2 | New route styles use Orbit CSS custom properties for spacing, type, color, border, radius, and layout sizing. |
| Theme support | 2 | Browser verified the route under the docs shell Efficio base theme and `[data-theme="orbit"]` toggle. |
| Full states | 2 | Includes ready, loading, validation error, disabled permission, save error, retry recovery, and success states. |
| Accessibility | 2 | Controls have accessible names, validation uses non-colour icon/text signals, `Input` now links help/error text through `aria-describedby`, loading uses `role="status"`, and errors use `role="alert"`. |
| Density | 1 | Comfortable and compact composition states are present, but `Input` and `Dropdown` do not yet expose native density props. |
| Contract match | 2 | Uses real Orbit `Input` and `Dropdown` contracts, plus `Button`, `Card`, `Spinner`, `Toggle`, `Text`, and `Headings`. |
| Pattern match | 2 | Matches the golden form validation example shape: visible labels, help text, inline error copy, summary error, and recovery action. |
| Copy and motion | 2 | Copy is specific, calm, recovery-oriented, and procurement-contextual. No decorative motion was introduced. |
| Orbit feel | 2 | Dense, restrained, work-focused RFP Builder settings UI rather than a marketing or generic SaaS form. |

Total: `17/18`

## Verification Reported By Implementation Thread
- `npm run test:components -- Input FieldNaming` passed with 8 files and 26 tests.
- `npm run lint` passed.
- `npm run audit:design-system` passed with 27 checks.
- `npm run build:docs` passed and prerendered `/design-system/benchmarks/form-validation`.
- Browser verification passed for:
  - ready state
  - loading state with labelled status
  - validation state with `aria-invalid` fields
  - `Input` help/error linkage through `aria-describedby`
  - disabled permission state for input, dropdown, and save action
  - save error with recovery copy and retry action
  - Efficio and Orbit theme toggle
  - no desktop horizontal overflow
  - no clipped controls after retry button polish
  - no browser console warnings or errors

## What Worked
- The Design Brain was specific enough to steer the implementation toward real Orbit
  components instead of custom form controls.
- The `Input` contract exposed a genuine accessibility gap: the docs and accessibility
  baseline expected `aria-describedby`, but `Input` did not support it. The benchmark
  prompted a small component API addition and a focused test.
- The `Dropdown` contract handled labelled select behavior and inline message state
  without custom select logic.
- State preview controls made the benchmark easy to validate without navigating hidden
  app conditions.
- The result stayed procurement-first with RFP Builder settings, approval routing, role
  restrictions, and workspace context.

## Deductions
- Density is only partially contract-complete. The benchmark composition supports compact
  spacing, but `Input` and `Dropdown` still have no density prop.
- No formal axe scan or automated contrast report was run. Contrast confidence comes from
  Orbit tokens, theme verification, and the design-system audit.
- The route is a docs benchmark implementation, not a production RFP Builder settings
  screen.

## Brain Updates Applied
- `design-brain/components/input.md` now documents the new `ariaDescribedBy` prop and
  helper/error linkage expectation.
- `design-brain/examples/form-field-validation.md` now links the procurement settings
  benchmark.
- `design-brain/patterns/settings-form-validation.md` captures the form composition,
  states, accessibility behavior, and remaining gaps.
- `_benchmarks/agent-benchmark-tasks.md` now records the Task 2 pass.
- `_benchmarks/scorecard-template.md` now records implementation, verification, and
  follow-up sections.

## Open Brain Updates
- Decide whether Orbit should add a first-class `FormField` wrapper component.
- Define form-control density behavior at component level, layout level, or both.
- Link a production RFP Builder settings screen before marking the pattern stable.
- Add formal axe/contrast checks to future benchmark verification.

## Suggested Validation Questions
- Should `ariaDescribedBy` remain the public prop name, or should the API align exactly
  with React's native `aria-describedby` naming?
- Should `Input` remain a standalone primitive, or should Orbit introduce a first-class
  `FormField` wrapper for label, help text, required state, and error copy?
- Should compact density be solved at component level, layout level, or both?
- Should every benchmark route get a captured screenshot and formal axe report before
  contributing to the global maturity score?
