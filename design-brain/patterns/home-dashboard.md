---
type: pattern-contract
status: in-review
owner: design-system
surfaces: [Connected Platform, Orbit, Client Connected Platform]
platform: shared
source: user-provided
last_reviewed: 2026-06-15
maturity_score: 66
tags: [orbit, design-brain, pattern-contract, visual-truth, dashboard]
---

# Pattern Contract: `home-dashboard`

## Purpose & Precedent
Provide a platform home surface that helps users understand current work, available
tools, summary signals, and likely next actions without becoming a marketing page.

This pattern has platform-specific screenshot-backed precedent:

- Connected Platform:
  `design-brain/examples/connected-platform-home-shell-dashboard.md`
- Orbit / Client Connected Platform:
  `design-brain/examples/orbit-client-home-ai-tools-dashboard.md`

Both examples are in-review and restricted until design-system owners approve
sanitization.

## When To Use / When Not To
Use for platform home, landing, and dashboard-entry pages where the user needs a
summary of work and a route into common tasks.

Do not use for:

- Deep analytics views where chart/table comparison is primary. Use
  `analytics-dashboard`.
- Product selection among major tools. Use `tool-hub`.
- Dense queues or trackers. Use `list-detail` or `data-table`-backed patterns.

## Regions & Composition
Required regions:

- Platform shell/navigation.
- Page or product-area header.
- Work summary cards.
- Tool/action entry cards when relevant.
- Status/count indicators.
- Recent work, initiative, or performance summary regions.

Component contracts commonly used:
`card-panel`, `button`, `badge-status`, `tabs` where the home surface has grouped
sections, and `data-table` only when a compact list/table is genuinely needed.

## Platform Differences
Connected Platform:

- More operational metadata is acceptable.
- Cards can be denser and more direct.
- Internal labels may use Efficio operational terminology.
- Prioritize current work, internal actions, milestones, and operational signals.

Orbit / Client Connected Platform:

- Keep the shell and work surface client-safe.
- Use clearer descriptions and more explicit next actions.
- Avoid internal process shortcuts unless product source proves clients see them.
- Cards should guide the client toward tools, summaries, and reviewable next steps.

## Hierarchy & Density
Current work and next actions lead. Summary signals support. Tool or action cards must
map to real work, not decorative feature promotion.

Connected Platform can run denser. Orbit should preserve enterprise density while giving
client users more context and confidence.

## Page-Level States
Initial skeleton, empty/no assigned work, partial data, stale summary, failed summary
load, permission-limited cards, unavailable tool/action, and refreshed data.

## Navigation & Focus Behaviour
The shell comes first, then page heading, then summary/tool regions. Cards with actions
must be keyboard reachable and have explicit accessible names. Status/count indicators
must not be color-only.

## Responsive Behaviour
Cards stack predictably on narrow screens. The page must keep core status and next
actions visible before secondary summaries.

## Data & Performance Notes
Do not show stale counts without a visible stale/last-updated signal. Avoid layout jumps
when dashboard summaries load.

## Anti-Patterns
- Marketing hero layout as the first screen.
- Generic feature cards with no current-work or next-action signal.
- Mixing CP operational shortcuts into Orbit client screens.
- Hiding internal CP controls behind client-style explanatory copy.
- Benchmark/docs screenshots used as product visual precedent.

## Golden Examples
- `design-brain/examples/connected-platform-home-shell-dashboard.md`
- `design-brain/examples/orbit-client-home-ai-tools-dashboard.md`

## Gap Report
- Screenshot sanitization and design-system approval are still needed.
- Empty, loading, stale, and permission-limited home states need source-backed examples.
- Current home dashboard card contracts should be reviewed once component source is
  identified.
