---
type: pattern-contract
status: in-review
owner: design-system
surfaces: [ClauseIQ, RFP Builder, MarketIQ]
platform: shared
source: user-provided
last_reviewed: 2026-06-15
maturity_score: 64
tags: [orbit, design-brain, pattern-contract, visual-truth]
---

# Pattern Contract: `review-and-approve-workflow`

## Purpose & Precedent
Support high-stakes review, approval, rejection, and audit decisions with clear state
and recoverable actions.

Current screenshot-backed adjacent precedent:
`design-brain/examples/orbit-client-marketiq-research-output-next-actions.md`

This MarketIQ example covers generated output review, report actions, and next actions.
It is not yet a full approval/rejection source. Keep approval-specific behavior in
review until ClauseIQ or RFP Builder source is linked.

## When To Use / When Not To
Use when decisions need traceability, role awareness, and status transitions. Do not use
for casual one-click actions with no workflow state. For generated-output review without
an approval decision, use only the output/next-action subset of this pattern.

## Regions & Composition
Work item summary, evidence/detail panel, status badge, comments or rationale field when
approval is required, approve/reject actions, audit trail, output actions, and next-step
cards.

Component contracts: `badge-status`, `button`, `input`, `card-panel`, `dialog`,
`toast-notification`.

## Hierarchy & Density
Decision or output status and required action first, evidence second, next actions or
audit history third. Client-facing output screens must keep generated parameters and
result actions close together.

## Page-Level States
Loading, awaiting review, generated output ready, approved, rejected, needs changes,
permission-limited, conflict/stale item, failed transition, download/save failure, and
partial generated output.

## Navigation & Focus Behaviour
Critical actions require clear focus order and confirmation where destructive or
irreversible. Failed actions return focus to the recovery control. Save/download actions
must be keyboard reachable and named by the output they affect.

## Responsive Behaviour
Evidence and audit trail may collapse behind tabs on narrow screens; primary decision or
output state remains visible. Next action cards stack without hiding their action labels.

## Data & Performance Notes
Prevent stale approvals by checking item version before final transition. Generated
output actions must reflect real state; do not mark reports saved, downloaded, or final
before persistence succeeds.

## Anti-Patterns
- Approving silently without showing saved state.
- Colour-only status.
- Hiding why a user cannot approve.
- Treating generated output as final approval.
- Vague next-action cards that do not say what happens next.
- Save/download controls far away from the output they affect.

## Golden Example
`design-brain/examples/orbit-client-marketiq-research-output-next-actions.md`

## Gap Report
- Screenshot sanitization and design-system approval are still needed.
- Full approval/rejection workflow source is still required before marking stable.
- ClauseIQ and RFP Builder approval-specific examples are still missing.
