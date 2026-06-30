---
type: pattern-contract
status: in-review
owner: design-system
surfaces: [RFP Builder, shared]
platform: shared
source: code
last_reviewed: 2026-06-15
maturity_score: 74
tags: [orbit, design-brain, pattern-contract, forms, validation]
---

# Pattern Contract: `settings-form-validation`

## Purpose & Precedent
Use this pattern for operational settings forms where users configure procurement
defaults, approval routes, or workspace policies and need clear validation, permission,
loading, save, and recovery states. The current precedent is the procurement settings
benchmark for RFP Builder.

## Source Links
- Benchmark component:
  `apps/docs/app/design-system/benchmarks/form-validation/ProcurementSettingsBenchmark.tsx`
- Benchmark styles:
  `apps/docs/app/design-system/benchmarks/form-validation/ProcurementSettingsBenchmark.module.css`
- Benchmark result:
  `_benchmarks/results/2026-06-15-procurement-settings-form.md`
- Related components:
  `design-brain/components/input.md`
  `design-brain/components/select-combobox.md`

## When To Use / When Not To
Use for settings, configuration, policy defaults, approval routing, and other forms
where a user is changing durable operational behavior. Do not use for simple one-field
search, wizard step navigation, or dense editable tables.

## Regions & Composition
Required regions:
- Header with form purpose and current benchmark/task context if in docs.
- State or mode controls when used as a benchmark/demo.
- Form panel with field groups.
- Context panel for workspace, role, scope, and last-reviewed information.
- Inline field help and error messages.
- Validation summary when multiple fields need attention.
- Permission notice when the user can view but not edit.
- Save error recovery panel with retry action.
- Success confirmation using a polite status region.

Core component contracts:
`input`, `select-combobox`, `button`, `card-panel`, `toast-notification` when transient
feedback is needed.

## Hierarchy & Density
Users should first understand what setting they are changing, then the required fields,
then the workspace/role context. Comfortable density is default. Compact density may
reduce parent spacing, but must not hide helper/error text or shrink touch targets below
the component contracts.

## Page-Level States
- Ready/editable.
- Loading with labelled `role="status"`.
- Validation error with inline field errors and a summary alert.
- Permission-limited/locked, where fields and primary actions are disabled and the
  reason is visible.
- Save error with recoverable copy and retry.
- Saved/success with polite status feedback.

## Navigation & Focus Behaviour
The form uses native form submission. Field labels must be visible. `Input` fields use
`ariaLabelledBy` for visible labels and `ariaDescribedBy` for helper/error ids.
Errors use non-colour signals. Validation summaries should appear before the field grid
and must not replace inline field errors.

## Responsive Behaviour
The form and context panel stack at narrow widths. The primary action row wraps without
clipping labels. The context panel remains after the form so users do not have to pass
metadata before reaching required fields.

## Data & Performance Notes
Do not fake saving. Loading and save errors need honest state and recovery paths. Avoid
destructive resets when switching preview states in production; the benchmark uses state
switches only for validation.

## Anti-Patterns
- Placeholder-only labels.
- Error colour without text or icon.
- Summary-only validation with no field-level messages.
- Disabled controls without a visible permission reason.
- Generic "Something went wrong" save errors.
- Custom select logic when `Dropdown` covers the behavior.

## Golden Example
`design-brain/examples/form-field-validation.md`

## Gap Report
- No first-class `FormField` wrapper exists yet.
- `Input` and `Dropdown` have no native density prop.
- No production RFP Builder settings screen has been linked yet.
