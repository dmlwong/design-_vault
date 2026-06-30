---
type: example
status: in-review
owner: design-system
surfaces: [ClauseIQ, RFP Builder, shared]
platform: shared
source: code
last_reviewed: 2026-06-15
maturity_score: 74
tags: [orbit, design-brain, example]
---

# Golden Example: Form Field With Help And Error

## Demonstrates
- `input` contract from the real `Input` component.
- `select-combobox` contract from the real `Dropdown` component.
- Accessible labels through visible labels, `ariaLabel`, or `ariaLabelledBy`.
- `invalid`, `required`, and `aria-invalid` behavior.
- Recoverable validation copy from the ClauseIQ upload flow.
- `aria-describedby` linkage through `Input`'s `ariaDescribedBy` prop.
- RFP Builder procurement settings form states from Benchmark Task 2.

## Real Source Links
- Input source:
  `packages/orbit/src/inputs/Input.tsx`
- Dropdown source:
  `packages/orbit/src/inputs/Dropdown.tsx`
- MultiSelectDropdown source:
  `packages/orbit/src/inputs/MultiSelectDropdown.tsx`
- Field naming helpers:
  `packages/orbit/src/inputs/naming.ts`
- ClauseIQ upload validation:
  `apps/prototypes/components/feature/clauseiq/upload.ts`
- ClauseIQ validation tests:
  `apps/prototypes/components/feature/clauseiq/ClauseIQPrototype.test.tsx`
- Procurement settings benchmark:
  `apps/docs/app/design-system/benchmarks/form-validation/ProcurementSettingsBenchmark.tsx`
- Benchmark result:
  `_benchmarks/results/2026-06-15-procurement-settings-form.md`
- Benchmark screenshot reference pack:
  `_benchmarks/results/2026-06-15-golden-visual-reference.md`

## Benchmark Screenshot Evidence
Use these screenshots for benchmark-route evidence of form validation composition, state
toolbar placement, permission-aware actions, and compact form density. Do not treat them
as canonical platform visual precedent until current product screenshots are linked:

- `_benchmarks/results/screenshots/2026-06-15-golden-visual-reference/form-validation-efficio-default.png`
- `_benchmarks/results/screenshots/2026-06-15-golden-visual-reference/form-validation-efficio-compact.png`
- `_benchmarks/results/screenshots/2026-06-15-golden-visual-reference/form-validation-orbit-default.png`
- `_benchmarks/results/screenshots/2026-06-15-golden-visual-reference/form-validation-orbit-compact.png`

## Source-Backed Shape
Use `Input` for standalone text entry and always provide `ariaLabel` or
`ariaLabelledBy`. When helper or error copy exists, pass the helper/error ids through
`ariaDescribedBy`. Use `Dropdown` when users must choose one known option; it supports
visible `label`, `message`, `required`, `invalid`, keyboard navigation, and listbox
semantics.

ClauseIQ upload validation gives the clearest real error-copy precedent:
- Unsupported files: `This file type isn't supported. Please upload a PDF file.`
- Oversized PDFs: `This file is too large. Maximum upload size is 100 MB.`

The tests confirm these errors are exposed through role `alert`.

The procurement settings benchmark adds a richer form precedent: visible label,
required marker, helper copy, inline error copy, validation summary, disabled permission
state, save-error recovery, success state, loading state, and compact composition mode.

## Acceptance Notes
Errors must explain what happened and how to recover. Status must not rely on colour
alone. Do not build custom form styling when `Input`, `Dropdown`, or
`MultiSelectDropdown` covers the behavior.

## Known Limits
- `Input` does not include a built-in label, help text, or error message wrapper.
- `Dropdown` has `message` support; `Input` needs external field composition.
- No Storybook source was found in the repo scan.
- A canonical field-wrapper component should be added if forms become common.
- Compact form density is currently handled by parent composition; `Input` and
  `Dropdown` do not expose density props.
