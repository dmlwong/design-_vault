---
type: pattern-contract
status: in-review
owner: design-system
surfaces: [ClauseIQ, MarketIQ]
platform: orbit-client-connected-platform
source: code
last_reviewed: 2026-06-15
maturity_score: 80
tags: [orbit, design-brain, pattern-contract]
---

# Pattern Contract: `guided-conversational-workflow`

## Purpose & Precedent
Guide users through structured, AI-assisted or card-based decisions while keeping
progress, selected context, parameters, and reviewable outputs visible. ClauseIQ is the
current code-backed precedent. MarketIQ now adds screenshot-backed Orbit / Client
Connected Platform visual truth.

## Source Links
- ClauseIQ prototype:
  `apps/prototypes/components/feature/clauseiq/ClauseIQPrototype.tsx`
- ClauseIQ reducer:
  `apps/prototypes/components/feature/clauseiq/state.ts`
- ClauseIQ tests:
  `apps/prototypes/components/feature/clauseiq/ClauseIQPrototype.test.tsx`
- Golden example:
  `design-brain/examples/clauseiq-focus-mode-results.md`
- Orbit / Client Connected Platform golden example:
  `design-brain/examples/orbit-client-marketiq-guided-workflow.md`

## When To Use / When Not To
Use when the workflow is sequential, AI-assisted, and auditable: users choose context,
provide input or parameters, wait for processing, then review output and take next
actions. Do not use for simple forms, static dashboards, tool-selection hubs, or dense
review pages where a persistent table/detail layout is the primary experience.

## Regions & Composition
Required regions:
- Product shell and page header.
- A vertical stack of workflow cards.
- Completed-context cards that remain visible but become lower emphasis or disabled.
- Current active card.
- Modal or controlled picker for large selection tasks.
- Selected-context summary after picker close.
- Parameter summary before generation.
- Processing card with honest progress copy.
- Results card.
- Next-step action card.

Component contracts used by ClauseIQ:
`card-panel`, `button`, `dialog`, `data-table`, `input`, `select-combobox`,
`badge-status`, `tabs`-adjacent grouped controls, `toast-notification` when feedback is
needed.

## Hierarchy & Density
Current task first, selected/completed context second, result evidence third. Cards stay
compact and operational. Orbit client flows may use slightly more explanation than
internal CP, but must avoid consumer chat bubbles, oversized decorative panels, or
marketing hero copy.

## Page-Level States
Source-backed ClauseIQ states:
- welcome.
- select initiative.
- initiative selected.
- select parameters.
- parameter selected.
- upload contract.
- upload validation error.
- processing.
- results.
- run another analysis with previous result retained.

Screenshot-backed MarketIQ states:
- tool intro/get started.
- select initiative.
- initiative picker modal with search and ownership tabs.
- initiative selected.
- research parameters confirmed.
- generate action ready.

## Navigation & Focus Behaviour
- Newly active cards scroll into view.
- Initiative selection opens a named `Overlay`.
- Initiative rows are keyboard selectable through table row-selection buttons.
- Ownership switching uses a grouped button control, not ARIA tabs.
- Processing locks earlier edit controls.
- Running another analysis preserves previous output above the new upload step.
- After a picker closes, focus should return to the control or selected-context card that
  launched it.

## Responsive Behaviour
Keep the layout as a single readable workflow column on narrow screens. Do not hide the
current required action behind secondary navigation. Modal tables should remain usable
on narrow screens without clipping search, tabs, or cancel/close controls.

## Data & Performance Notes
Long-running AI actions must show honest progress and must not fake instant success.
ClauseIQ uses a reducer and a configurable processing delay; production should connect
this to real task state.

## Anti-Patterns
- Decorative chat UI that hides structured procurement data.
- Re-running entrance animations on every generated response.
- Removing completed context when it is still needed for auditability.
- Generic assistant copy without recovery paths.
- Letting users edit locked context while processing or after results without a clear
  restart path.
- Hiding selected initiative/context after the modal closes.
- Using generic AI assistant language instead of source-backed procurement actions.

## Golden Examples
`design-brain/examples/clauseiq-focus-mode-results.md`
`design-brain/examples/orbit-client-marketiq-guided-workflow.md`

## Gap Report
- MarketIQ screenshots are in-review and still need sanitization approval.
- Responsive checks still need to be captured against production screens.
- ClauseIQ uses mock data; production data/performance constraints need product source.
- The pattern name is broader than ClauseIQ and should be validated against another
  AI-assisted workflow in production before marking stable.
