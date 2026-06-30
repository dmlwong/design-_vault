---
type: governance
status: stable
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-06-14
maturity_score: 75
tags: [orbit, design-brain, governance]
---

# Governance

The Orbit Design Brain is shared memory for design, product, and AI agents. It should
change quickly when Orbit learns something, but not casually.

## Approval Rules

- Design system owners approve changes to foundations, tokens, component contracts,
  pattern contracts, skills, and tool projections.
- Product and design team members can propose changes using the change request template.
- Agent failures must feed back into the canonical vault, not only into generated UI.
- Source-derived facts from code take precedence over memory or preference.
- Product-specific exceptions must be written into the relevant contract or pattern.

## Review Cadence

- Weekly until the first vertical slice is stable.
- Monthly until the top 10 components and key patterns are stable.
- Quarterly after the brain reaches 85-90 maturity.

## Definition Of Stable

A note can be marked `stable` only when it has a named owner, real source links where
needed, current examples, and no unresolved `source-required` fields.
