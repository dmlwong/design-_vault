---
type: component-contract
status: draft
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-06-14
maturity_score: 42
tags: [orbit, design-brain, component-contract, gap]
---

# Component Contract: `drawer`

## Purpose
Use a drawer-like surface to reveal detail, edit forms, filters, or supporting context
without losing the parent view. This is currently a specified product need, not a
source-backed reusable Orbit component.

## Source Links
- Reusable drawer source: not found in
  `packages/orbit/src`
- Source-backed modal/dialog alternative:
  `packages/orbit/src/feedback/Overlay.tsx`
- Prototype drawer-like panels found in:
  `apps/prototypes/app/suppliers/page.tsx`
  `apps/prototypes/components/feature/FilterPanel.tsx`
  `apps/prototypes/components/feature/data-tracker/AddClausePanel.tsx`
  `apps/prototypes/components/feature/data-tracker/LargeOverlay.tsx`

## Anatomy
Required future anatomy: backdrop or edge surface, header, title, close control, body,
optional footer actions, and focus return to the trigger.

## Public API
No canonical reusable API exists yet. Until design-system owners create or approve
one, agents should not invent a production drawer API. Use `Overlay` for modal
dialog behavior when the product requirement is blocking interaction with the page.

| Prop | Type | Default | Required | Source |
| ---- | ---- | ------- | -------- | ------ |
| source-required reusable API | source-required | source-required | source-required | gap |

## Variants
Specified future variants:
- Detail drawer.
- Edit drawer.
- Filter drawer or side panel.
- Wide drawer for complex forms.

These variants need source or design approval before becoming stable contract.

## States
Specified future states: open, closed, focus-visible, loading body, empty body, error
body, submitting, disabled actions. Existing reusable `Overlay` already covers focus
trap, Escape close, backdrop close, body-scroll lock, and focus restoration for modal
dialog use cases.

## Density
Drawer bodies should support dense field groups and detail lists without becoming
marketing panels. Use Orbit spacing tokens and avoid nested card layouts.

## Themes
Future drawer implementation must resolve all visual values through `efficio` and
`orbit` theme tokens. Do not hardcode surface, border, shadow, overlay, or z-index
values.

## RBAC / Permissions
Read-only drawers should keep context visible while disabling restricted edit actions
with approved copy. If the existence of an object is restricted, do not open a drawer
for it.

## Tokens Used
Specified future token set:
- `--orbit-color-bg-default`
- `--orbit-color-border-default`
- `--orbit-shadow-lg`
- `--orbit-z-overlay`
- `--orbit-color-focus-ring` or `--orbit-color-border-focused`
- `--orbit-space-base`
- `--orbit-space-m`
- `--orbit-radius-md`

## Accessibility
If modal, match `Overlay` behavior: `role="dialog"`, accessible name, focus trap,
Escape close, body-scroll lock, and focus restoration. If non-modal, do not trap focus;
ensure the parent page remains reachable and screen-reader order is coherent.

## Motion
Slide motion is only acceptable when it helps spatial orientation and must support
reduced motion. Source currently has no shared motion token system, so this remains
a gap.

## Content / Copy
Header names the selected entity or task. Footer actions should use concrete verbs:
`Save`, `Apply filters`, `Cancel`, `Close`.

## Do / Don't
- Do use `Overlay` when source-backed modal behavior is required today.
- Do treat drawer as a design-system gap until a reusable component exists.
- Don't invent drawer props in product code without adding a source-backed contract.
- Don't hide required filters or primary navigation inside a drawer.
- Don't nest drawers or open a drawer from another modal.

## Golden Example
`design-brain/examples/dialog-keyboard.md`

## Gap Report
- No reusable `Drawer` component was found in `packages/orbit/src`.
- Prototype drawer-like panels exist but are not yet canonical design-system source.
- API, sizes, focus behavior, motion, and responsive behavior need owner approval.
