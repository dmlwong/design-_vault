---
type: example
status: in-review
owner: design-system
surfaces: [ClauseIQ, shared]
platform: shared
source: code
last_reviewed: 2026-06-14
maturity_score: 72
tags: [orbit, design-brain, example]
---

# Golden Example: Dialog Or Drawer Keyboard Behavior

## Demonstrates
- `dialog` contract from the real `Overlay` component.
- Focus trap, Escape handling, backdrop close, body-scroll lock, and focus return.
- Accessible dialog naming with `ariaLabelledBy`.
- Real modal composition in ClauseIQ's initiative selection flow.
- Drawer is documented as a gap, so this example uses `Overlay`.

## Real Source Links
- Overlay source:
  `packages/orbit/src/feedback/Overlay.tsx`
- Overlay styles:
  `packages/orbit/src/feedback/Overlay.module.css`
- Overlay tests:
  `packages/orbit/src/feedback/Overlay.test.tsx`
- ClauseIQ modal usage:
  `apps/prototypes/components/feature/clauseiq/ClauseIQPrototype.tsx`
- ClauseIQ flow tests:
  `apps/prototypes/components/feature/clauseiq/ClauseIQPrototype.test.tsx`

## Source-Backed Shape
ClauseIQ's initiative modal uses:
- `Overlay visible={open}`.
- `onClose={onClose}`.
- `ariaLabelledBy="clauseiq-initiative-modal-title"`.
- `size="Large"`.
- `height="Content"`.
- a heading inside the dialog title element.
- `IconButton` close action with `ariaLabel="Close initiative selection"`.
- a toolbar with ownership switcher and search.
- a selectable `Table`.
- a footer `Cancel` button.

The Overlay tests confirm dialog role/name, Escape close, backdrop close, focus trap,
body-scroll lock, and focus restoration.

## Acceptance Notes
Use this example to verify that modal surfaces are keyboard-operable and do not lose
the user's place in dense workflows. If the product asks for a drawer today, use this
source-backed modal behavior unless design-system owners approve a reusable drawer.

## Known Limits
- Reusable drawer source was not found in `packages/orbit/src`.
- `Overlay` has no built-in header/footer/action slots.
- No Storybook source was found in the repo scan.
