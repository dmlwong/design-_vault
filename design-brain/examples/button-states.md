---
type: example
status: in-review
owner: design-system
surfaces: [ClauseIQ, shared]
platform: shared
source: code
last_reviewed: 2026-06-14
maturity_score: 68
tags: [orbit, design-brain, example]
---

# Golden Example: Button In All States

## Demonstrates
- `button` contract from the real `Button` and `IconButton` components.
- Primary and secondary actions in ClauseIQ.
- Tertiary edit/change actions.
- Icon-only close action inside a modal.
- Disabled handling through `state="Disabled"` or `disabled`.

## Real Source Links
- Button source:
  `packages/orbit/src/actions/Button.tsx`
- Button styles:
  `packages/orbit/src/actions/Button.module.css`
- Button tests:
  `packages/orbit/src/actions/Button.test.tsx`
- IconButton source:
  `packages/orbit/src/actions/IconButton.tsx`
- ClauseIQ usage:
  `apps/prototypes/components/feature/clauseiq/ClauseIQPrototype.tsx`

## Source-Backed Shape
Use:
- `variant="Primary"` for the next primary action, such as `View Result`.
- `variant="Secondary"` for sibling actions, such as `Run Another Analysis` and
  `Download Report`.
- `variant="Tertiary"` for lower-emphasis contextual edits, such as `Change Playbook`.
- `IconButton` with an accessible `ariaLabel` for icon-only actions, such as closing
  the initiative modal.

The button test confirms that `Button` defaults to `type="button"` and blocks click
activation when disabled by state.

## Acceptance Notes
Generated buttons should use Orbit variants and token-backed icons. Avoid generic
utility-class button output. Button labels must be concrete verbs and should reflect
the workflow state.

## Known Limits
- No built-in loading state exists.
- No Storybook source was found in the repo scan.
- Focus-visible behavior is in CSS, but no specific focus test exists for `Button`.
