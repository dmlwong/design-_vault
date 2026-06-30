---
type: principle
status: stable
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-06-14
maturity_score: 75
tags: [orbit, design-brain, principles]
---

# principles.md — How Orbit should feel

The intent layer. Read this when a screen needs to *feel* right, not just be correct.

## The one-line philosophy
Engineering-first, density-respecting, predictable enterprise software for procurement
professionals doing serious work in long sessions. Calm, legible, and fast — never flashy.

## Operating principles
1. **Density over whitespace.** Orbit users compare, scan, and act on large data sets.
   Reach for compact, legible layouts before generous consumer-style spacing.
2. **Scannability over delight.** Hierarchy, alignment, and consistent rhythm do the
   work. Decorative flourishes that slow scanning are a cost, not a feature.
3. **Predictability over novelty.** Reuse established Orbit patterns. A new interaction
   pattern needs a reason; precedent wins ties.
4. **Show system state honestly.** Loading, empty, error, and stale states are designed,
   not afterthoughts. Never fake instant success.
5. **Progressive disclosure.** Default to the essential; reveal depth on demand
   (focus modes, expandable detail, drawers) rather than crowding the first view.
6. **Trust through restraint.** This is high-stakes procurement. Visual confidence
   comes from consistency and clarity, not saturation or motion.

## Density modes
- **Comfortable** — default. The baseline rhythm.
- **Compact** — denser rows/controls for power users and data-heavy views.
  Both must stay AA-legible. Components declare how they respond in their contract.

## What "good" looks like here
Reference the golden examples in `examples/`. When a generated screen feels like a
generic SaaS template, it has failed — re-anchor on the examples and `anti-patterns.md`.
