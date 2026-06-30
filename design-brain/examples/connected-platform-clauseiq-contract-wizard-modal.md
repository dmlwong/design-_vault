---
type: example
status: in-review
owner: design-system
surfaces: [Connected Platform, ClauseIQ]
platform: connected-platform
source: user-provided
last_reviewed: 2026-06-15
maturity_score: 65
tags: [orbit, design-brain, example, visual-truth, connected-platform, clauseiq, modal]
---

# Golden Example: Connected Platform ClauseIQ Contract Wizard Modal

## Demonstrates
- Large internal modal/wizard behavior.
- Multi-step document workflow.
- ClauseIQ contract upload and setup treatment inside Connected Platform.

## Screenshot Evidence
- Primary screenshot:
  [connected-platform-clauseiq-contract-wizard-modal.png](screenshots/connected-platform/connected-platform-clauseiq-contract-wizard-modal.png)

Screenshot is in-review and restricted until design-system owners approve sanitization.

## Pattern Represented
Internal modal wizard for a document-heavy task.

Use this when creating or reviewing CP workflows that require setup, upload, step-by-step
progress, or a focused task overlay.

## Components Visible
- Dialog/modal.
- Wizard stepper.
- Upload/drop zone or file selection area.
- Primary and secondary actions.
- Close/cancel affordances.
- Supporting explanatory content.

## Layout Guidance
- Let the modal be large enough for the task; do not cram document setup into a tiny
  confirmation dialog.
- Keep step progress visible and concrete.
- Align the primary action with the current step's task.
- Preserve clear cancel and close paths.

## Density Guidance
- Modal content can be spacious enough for upload confidence, but should still feel
  operational.
- Avoid decorative whitespace that pushes the task below the fold.
- Keep step labels and form controls compact and readable.

## Copy Guidance
- Use direct internal workflow language.
- Explain upload/setup requirements only where they affect completion.
- Error and validation copy should be specific and recoverable.

## Imitate
- Focused modal task boundary.
- Visible wizard progress.
- Explicit upload/setup action.
- Clear escape routes.

## Do Not Imitate
- Generic onboarding wizard styling.
- Marketing copy inside task modals.
- Hidden validation requirements.
- Removing keyboard or focus management from the dialog.

## Review Questions
- Which wizard steps are canonical for ClauseIQ?
- Which upload states need screenshots: loading, invalid file, upload failure, success?
- Should this map to the existing dialog contract or a future wizard contract?
