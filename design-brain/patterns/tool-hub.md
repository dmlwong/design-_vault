---
type: pattern-contract
status: in-review
owner: design-system
surfaces: [Orbit, Client Connected Platform]
platform: orbit-client-connected-platform
source: user-provided
last_reviewed: 2026-06-15
maturity_score: 66
tags: [orbit, design-brain, pattern-contract, visual-truth, tool-hub]
---

# Pattern Contract: `tool-hub`

## Purpose & Precedent
Help external client users choose among major workflow tools without turning the page
into generic feature marketing.

Current screenshot-backed precedent:
`design-brain/examples/orbit-client-sourcing-execution-tool-hub.md`

The example is in-review and restricted until design-system owners approve sanitization.

## When To Use / When Not To
Use when the user needs to choose among major products or workflow tools, such as
MarketIQ, RFP Builder, RFP Analytics, and ClauseIQ.

Do not use for:

- A normal home dashboard. Use `home-dashboard`.
- A sequential tool flow after the user has chosen a tool. Use
  `guided-conversational-workflow` or a product-specific pattern.
- Dense comparison of records or suppliers. Use table/list patterns.

## Regions & Composition
Required regions:

- Platform shell/navigation.
- Product-area header.
- Tool cards with product name, short purpose, availability/status, and entry action.
- Optional grouping by lifecycle stage or procurement journey.
- Optional recently used/current work region if source-backed.

Component contracts commonly used:
`card-panel`, `button`, `badge-status`, and `toast-notification` for transient launch or
availability feedback.

## Hierarchy & Density
The tool name and purpose lead. Entry action follows. Availability/status should be
visible without becoming the primary message unless the tool is unavailable.

Cards may be more spacious than internal CP operational cards, but must still feel like
enterprise product navigation, not a promotional website.

## Page-Level States
Initial skeleton, no available tools, partial availability, permission-limited tool,
coming soon/unavailable tool, launch failure, and stale tool availability.

## Navigation & Focus Behaviour
Keyboard order follows page heading, tool cards, then secondary regions. Each card's
primary action must include the tool name in its accessible name. Disabled tools need a
visible reason.

## Responsive Behaviour
Tool cards stack or reflow without losing product names, status, or primary actions.
Avoid truncating product names on narrow screens.

## Data & Performance Notes
Tool availability should come from product permissions or feature flags, not static
copy. Do not show a launch action before the destination is available.

## Anti-Patterns
- Generic SaaS feature-card grids detached from real products.
- Repeating the same CTA on every card without explaining each tool's purpose.
- Internal CP operational labels exposed to client users.
- Decorative tool icons used as the main differentiator.
- A marketing hero replacing the actual tool choices.

## Golden Example
`design-brain/examples/orbit-client-sourcing-execution-tool-hub.md`

## Gap Report
- Screenshot sanitization and design-system approval are still needed.
- Tool unavailable, permission-limited, launch failure, and loading states need
  source-backed examples.
- Tool-card availability/status behavior may need a dedicated component contract.
