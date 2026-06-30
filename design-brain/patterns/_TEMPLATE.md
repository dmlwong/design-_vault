---
type: pattern-contract-template
status: stable
owner: design-system
surfaces: [shared]
platform: unknown
source: specified
last_reviewed: 2026-06-14
maturity_score: 70
tags: [orbit, design-brain, template]
---

# Pattern Contract: `<pattern-name>`

> Copy to `patterns/<pattern-name>.md`. A pattern contract defines a reusable page-level
> composition: regions, the components in them, responsive behaviour, and state at the
> page level.

## Purpose & precedent
What user job this composition serves; which surfaces use it; whether it sets precedent
(i.e. new screens of this type MUST follow it).

## When to use / when not to
The decision rule. What problem qualifies; the nearest alternative pattern and why you'd
pick it instead.

## Regions & composition
Name each region (e.g. header bar, filter rail, results canvas, detail drawer) and the
component contracts that fill it. ASCII sketch or link to the golden example screen.

## Hierarchy & density
What the user scans first; what is progressive-disclosed (expandable detail, drawers,
focus mode); how the pattern behaves in comfortable vs compact.

## Page-level states
Initial load (skeleton layout), partial data, zero results, error, stale/refreshing,
long-running operation. These are page states, beyond per-component states.

## Navigation & focus behaviour
Entry points, in-pattern navigation (tabs, steps, drill-down), what Esc/back does, where
keyboard focus lands on entry and after major transitions.

## Responsive behaviour
What collapses, stacks, or hides at each breakpoint. What is non-negotiable at all sizes.

## Data & performance notes
Pagination/virtualisation expectations, acceptable initial payloads, optimistic updates.

## Anti-patterns for this composition
The specific wrong versions agents tend to produce (e.g. "filters in a modal instead of a
rail", "cards where a dense table is required").

## Golden example
Link to the real screen in `examples/` or the prototype.

## Status
`draft` | `in review` | `stable` · Last updated: `<date>` · Owner: `<name>`
