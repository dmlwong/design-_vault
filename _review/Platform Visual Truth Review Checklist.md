---
type: review
status: in-review
owner: design-system
surfaces: [Connected Platform, Orbit, Client Connected Platform]
source: specified
last_reviewed: 2026-06-16
maturity_score: 88
tags: [orbit, design-brain, review, visual-truth, platform-separation]
---

# Platform Visual Truth Review Checklist

Use this checklist to review the screenshot-backed platform guidance before promoting
anything from `in-review` to `stable`.

Do not approve a file just because the benchmark passed. Approve it only if it matches
the real platform direction and is safe for the Design Brain to treat as precedent.

## Review Decisions

For each file, choose one:

- `[ ] Approved` — accurate enough to become stable.
- `[ ] Needs edits` — mostly right, but wording or interpretation needs correction.
- `[ ] Replace source` — screenshot or source is misleading, outdated, sensitive, or not
  representative.
- `[ ] Keep restricted` — useful internally, but not safe to share broadly.

## 1. Screenshot Manifests — Review First

These decide which screenshots are allowed to influence the Design Brain.

| Review | File | What to check |
| ------ | ---- | ------------- |
| [ ] | `design-brain/examples/screenshots/connected-platform/manifest.md` | Are the Connected Platform screenshot names, surfaces, states, and "what agents should learn" notes accurate? Which screenshots can move from `restricted until approved` to `approved` or `sanitized`? |
| [ ] | `design-brain/examples/screenshots/orbit-client-connected-platform/manifest.md` | Are the Orbit / Client Connected Platform screenshot names, surfaces, states, and learning notes accurate? Confirm the landscape diagram stays `reference-only`, not UI precedent. |

## 2. Platform Profiles — Review Second

These are the top-level platform rules agents will load before designing.

| Review | File | What to check |
| ------ | ---- | ------------- |
| [ ] | `design-brain/platforms/connected-platform.md` | Does it correctly describe CP as internal, operational, dense, and power-user focused? Are the listed examples and pattern contracts the right ones? |
| [ ] | `design-brain/platforms/orbit-client-connected-platform.md` | Does it correctly describe Orbit / Client Connected Platform as external, client-safe, guided, and polished while still enterprise-dense? |
| [ ] | `design-brain/platforms/README.md` | Does the platform split and "ask if unclear" rule feel clear enough for agents and team members? |

## 3. Visual Truth Notes — Review Third

These convert screenshots into written visual rules.

| Review | File | What to check |
| ------ | ---- | ------------- |
| [ ] | `design-brain/platforms/connected-platform-visual-truth.md` | Are the CP rules for shell/navigation, density, cards, tables/lists, modal/wizard behavior, dashboard treatment, and copy tone correct? |
| [ ] | `design-brain/platforms/orbit-client-connected-platform-visual-truth.md` | Are the Orbit rules for shell/navigation, density, cards, tables/lists, modal/workflow behavior, dashboard/tool treatment, and copy tone correct? |

## 4. Golden Examples — Connected Platform

These are the most likely files agents will copy from when building CP screens.

| Review | File | What to check |
| ------ | ---- | ------------- |
| [ ] | `design-brain/examples/connected-platform-home-shell-dashboard.md` | Does the interpretation of CP home shell/dashboard match the real internal platform? |
| [ ] | `design-brain/examples/connected-platform-initiative-list-table.md` | Does the interpretation of dense initiative lists, filters, owner metadata, and row actions match CP? |
| [ ] | `design-brain/examples/connected-platform-clauseiq-contract-wizard-modal.md` | Does the modal/wizard guidance match the actual ClauseIQ internal workflow? |
| [ ] | `design-brain/examples/connected-platform-supplier-tracker-table.md` | Does the supplier tracker/discovery guidance match real supplier workflows? |

## 5. Golden Examples — Orbit / Client Connected Platform

These are the most likely files agents will copy from when building client-facing Orbit
screens.

| Review | File | What to check |
| ------ | ---- | ------------- |
| [ ] | `design-brain/examples/orbit-client-home-ai-tools-dashboard.md` | Does the home/dashboard guidance match the real client platform tone and hierarchy? |
| [ ] | `design-brain/examples/orbit-client-sourcing-execution-tool-hub.md` | Does the tool hub guidance describe real tool selection without becoming marketing-style? |
| [ ] | `design-brain/examples/orbit-client-marketiq-guided-workflow.md` | Does the MarketIQ flow guidance correctly describe initiative selection, parameter confirmation, and generation? |
| [ ] | `design-brain/examples/orbit-client-marketiq-research-output-next-actions.md` | Does the generated output/next-actions guidance match client expectations and product behavior? |
| [ ] | `design-brain/examples/orbit-client-delivery-engine-initiative-detail.md` | Does the initiative detail/tool coverage guidance match the real client-facing Delivery Engine screen? |

## 6. Pattern Contracts — Review After Examples

Review these after the screenshot and example notes. The question is whether the pattern
contracts point to the right examples and describe the right screen shape.

| Review | File | What to check |
| ------ | ---- | ------------- |
| [ ] | `design-brain/patterns/home-dashboard.md` | Does this correctly cover both CP and Orbit home/dashboard pages without blending the two? |
| [ ] | `design-brain/patterns/tool-hub.md` | Does this correctly describe Orbit client-facing tool selection? |
| [ ] | `design-brain/patterns/guided-conversational-workflow.md` | Does this correctly cover ClauseIQ/MarketIQ guided workflows? |
| [ ] | `design-brain/patterns/list-detail.md` | Does this correctly separate CP dense list/detail behavior from Orbit client initiative detail behavior? |
| [ ] | `design-brain/patterns/config-wizard.md` | Does this correctly describe the CP ClauseIQ modal/wizard precedent? |
| [ ] | `design-brain/patterns/review-and-approve-workflow.md` | Is the MarketIQ output example only an adjacent review/output precedent, not a full approval workflow? |
| [ ] | `design-brain/patterns/analytics-dashboard.md` | Is the Orbit home dashboard correctly marked as adjacent visual precedent, not a deep analytics source? |
| [ ] | `design-brain/patterns/README.md` | Is the pattern-to-example mapping clear and accurate? |

## 7. Guardrails — Review Last

These files prevent future agents from mixing the two platforms.

| Review | File | What to check |
| ------ | ---- | ------------- |
| [ ] | `AGENTS.md` | Does the platform-first rule force agents to identify CP vs Orbit before designing? |
| [ ] | `design-brain/anti-patterns.md` | Are the platform-mixing anti-patterns strong enough and accurate? |
| [ ] | `design-brain/examples/README.md` | Are the platform golden examples discoverable enough? |

## Approval Notes

Use this area while reviewing.

### Approved Files

- 

### Needs Edits

- 

### Replace Source

- 

### Keep Restricted

- 

## After Review

When review is complete:

1. Update each approved file from `status: in-review` to `status: stable`.
2. Update screenshot manifest rows from `restricted until approved` to the correct
   sensitivity status: `sanitized`, `approved`, or `restricted`.
3. Keep any uncertain files as `in-review`.
4. Export the Design Brain to `the efficio-orbit repo`.
5. Run a dry-run export and confirm `No export changes`.

<!-- graph-links:start — generated by tools/gen_graph_links.py; do not hand-edit -->
## Vault graph
[[AGENTS|AGENTS]] · [[design-brain/anti-patterns|anti-patterns]] · [[design-brain/examples/README|examples README]] · [[design-brain/examples/connected-platform-clauseiq-contract-wizard-modal|connected-platform-clauseiq-contract-wizard-modal]] · [[design-brain/examples/connected-platform-home-shell-dashboard|connected-platform-home-shell-dashboard]] · [[design-brain/examples/connected-platform-initiative-list-table|connected-platform-initiative-list-table]] · [[design-brain/examples/connected-platform-supplier-tracker-table|connected-platform-supplier-tracker-table]] · [[design-brain/examples/orbit-client-delivery-engine-initiative-detail|orbit-client-delivery-engine-initiative-detail]] · [[design-brain/examples/orbit-client-home-ai-tools-dashboard|orbit-client-home-ai-tools-dashboard]] · [[design-brain/examples/orbit-client-marketiq-guided-workflow|orbit-client-marketiq-guided-workflow]] · [[design-brain/examples/orbit-client-marketiq-research-output-next-actions|orbit-client-marketiq-research-output-next-actions]] · [[design-brain/examples/orbit-client-sourcing-execution-tool-hub|orbit-client-sourcing-execution-tool-hub]] · [[design-brain/examples/screenshots/connected-platform/manifest|connected-platform manifest]] · [[design-brain/examples/screenshots/orbit-client-connected-platform/manifest|orbit-client-connected-platform manifest]] · [[design-brain/patterns/README|patterns README]] · [[design-brain/patterns/analytics-dashboard|analytics-dashboard]] · [[design-brain/patterns/config-wizard|config-wizard]] · [[design-brain/patterns/guided-conversational-workflow|guided-conversational-workflow]] · [[design-brain/patterns/home-dashboard|home-dashboard]] · [[design-brain/patterns/list-detail|list-detail]] · [[design-brain/patterns/review-and-approve-workflow|review-and-approve-workflow]] · [[design-brain/patterns/tool-hub|tool-hub]] · [[design-brain/platforms/README|platforms README]] · [[design-brain/platforms/connected-platform-visual-truth|connected-platform-visual-truth]] · [[design-brain/platforms/connected-platform|connected-platform]] · [[design-brain/platforms/orbit-client-connected-platform-visual-truth|orbit-client-connected-platform-visual-truth]] · [[design-brain/platforms/orbit-client-connected-platform|orbit-client-connected-platform]]
<!-- graph-links:end -->
