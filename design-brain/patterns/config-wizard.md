---
type: pattern-contract
status: in-review
owner: design-system
surfaces: [Connected Platform, ClauseIQ, Platform Config, RFP Builder]
platform: connected-platform
source: user-provided
last_reviewed: 2026-06-15
maturity_score: 66
tags: [orbit, design-brain, pattern-contract, visual-truth]
---

# Pattern Contract: `config-wizard`

## Purpose & Precedent
Guide users through setup or configuration where order, validation, and review matter.

Current screenshot-backed precedent:
`design-brain/examples/connected-platform-clauseiq-contract-wizard-modal.md`

The example is in-review and restricted until design-system owners approve sanitization.

## When To Use / When Not To
Use for multi-step setup, upload, or configuration with dependencies. Do not use for
independent settings that can be edited in any order, or for a single confirmation
dialog.

## Regions & Composition
Step navigation, current step content, upload or field input, validation summary,
contextual help, footer actions, review/submit step, and clear close/cancel paths.

Component contracts: `input`, `select-combobox`, `button`, `tabs`, `card-panel`,
`dialog`, `toast-notification`.

## Hierarchy & Density
Current required step first, supporting requirements second, footer actions last. Avoid
oversized empty space, but allow enough room for document upload confidence.

## Page-Level States
Initial load, step loading, upload required, upload validation error, invalid file,
saved draft, submitting, submission error, completed.

## Navigation & Focus Behaviour
Focus moves to the first invalid field or upload error after validation. Back/next
controls preserve entered values. Close/cancel remains reachable by keyboard and should
not discard work without a clear confirmation when data would be lost.

## Responsive Behaviour
Step navigation collapses to compact progress display on narrow screens. Large modals
must not clip footer actions or upload controls.

## Data & Performance Notes
Autosave or draft behavior must be explicit. Do not imply saved state before
persistence. Upload progress and failure must reflect real task state.

## Anti-Patterns
- Hiding validation until final submit when earlier recovery is possible.
- Using tabs for a required sequential flow without progress semantics.
- Treating a document setup wizard as a tiny confirmation dialog.
- Marketing-style wizard copy inside an internal operational workflow.
- Hiding cancel/close or keyboard escape paths.

## Golden Example
`design-brain/examples/connected-platform-clauseiq-contract-wizard-modal.md`

## Gap Report
- Screenshot sanitization and design-system approval are still needed.
- Actual Platform Config / New Playbook precedent has not been linked.
- Upload loading, invalid file, and failure states need source-backed screenshots.
