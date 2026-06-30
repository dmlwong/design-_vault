---
type: pattern-index
status: in-review
owner: design-system
surfaces: [shared]
platform: shared
source: code
last_reviewed: 2026-06-15
maturity_score: 78
tags: [orbit, design-brain, patterns]
---

# patterns/ — Page-Level Pattern Contracts

Component contracts cover the bricks; pattern contracts cover the buildings. A pattern is
a reusable *composition* — how components assemble into a screen or flow with a defined
behaviour. This is the layer that stops agents producing screens that use correct
components but compose them generically.

## When to write a pattern contract
- A composition recurs across surfaces (results dashboards, config wizards, list+detail).
- A screen sets precedent that future screens must follow.
- An agent keeps composing pages "correctly but wrong" — right bricks, wrong building.

## How agents use this
Building a full page or multi-component view → check this index for a matching pattern
**before** inventing a layout. Components defer to their contracts; the page defers to
the pattern.

Before applying any pattern, identify the platform profile:
`design-brain/platforms/connected-platform.md` for internal Efficio workflows or
`design-brain/platforms/orbit-client-connected-platform.md` for external client-facing
workflows.

## Index
| Pattern | Platform | Surfaces | Status |
| ------- | -------- | -------- | ------ |
| `home-dashboard` | shared | Connected Platform, Orbit / Client Connected Platform | in-review — platform screenshot-backed; sanitization approval needed |
| `tool-hub` | orbit-client-connected-platform | Sourcing Execution, client tool selection | in-review — screenshot-backed by Orbit Sourcing Execution |
| `focus-mode-results` | orbit-client-connected-platform | ClauseIQ, shared results views | in-review — benchmark evidence; production source still needed |
| `guided-conversational-workflow` | orbit-client-connected-platform | ClauseIQ, MarketIQ card-based flows | in-review — ClauseIQ source-backed, MarketIQ screenshot-backed |
| `settings-form-validation` | shared | RFP Builder, shared settings forms | in-review — benchmark evidence; production source still needed |
| `list-detail` | shared | Connected Platform, Orbit / Client Connected Platform | in-review — platform screenshot-backed; drawer/detail source still needed |
| `config-wizard` | connected-platform | ClauseIQ, Platform Config, RFP Builder | in-review — CP ClauseIQ wizard screenshot-backed |
| `analytics-dashboard` | orbit-client-connected-platform | MarketIQ, RFP Analytics | in-review — benchmark evidence plus adjacent Orbit dashboard screenshot; production source and data-viz tokens still needed |
| `lovable-port` | shared | shared prototype migration | in-review — benchmark evidence from `Test` |
| `review-and-approve-workflow` | shared | ClauseIQ, RFP Builder, MarketIQ | in-review — MarketIQ generated-output precedent; full approval source still needed |
| `work-card` | shared | any card-based surface | in-review — composition pattern; golden example: `work-card-research-primer.md` |

ClauseIQ now provides a source-backed precedent for `guided-conversational-workflow`.
MarketIQ now provides Orbit / Client Connected Platform screenshot-backed precedent for
guided workflow and generated-output next actions. Connected Platform screenshots now
provide in-review precedent for list/table and wizard patterns. `focus-mode-results`
still needs a production product screen with persistent filters, results, and detail
review before it can become stable.

## Golden Example Mapping

| Pattern | Golden examples |
| ------- | --------------- |
| `home-dashboard` | `connected-platform-home-shell-dashboard.md`, `orbit-client-home-ai-tools-dashboard.md` |
| `tool-hub` | `orbit-client-sourcing-execution-tool-hub.md` |
| `guided-conversational-workflow` | `clauseiq-focus-mode-results.md`, `orbit-client-marketiq-guided-workflow.md` |
| `list-detail` | `connected-platform-initiative-list-table.md`, `connected-platform-supplier-tracker-table.md`, `orbit-client-delivery-engine-initiative-detail.md` |
| `config-wizard` | `connected-platform-clauseiq-contract-wizard-modal.md` |
| `analytics-dashboard` | `analytics-kpi-chart.md`, `orbit-client-home-ai-tools-dashboard.md` |
| `review-and-approve-workflow` | `orbit-client-marketiq-research-output-next-actions.md` |
| `work-card` | `work-card-research-primer.md` (reference .tsx + both-theme screenshots) |
