---
type: example-index
status: in-review
owner: design-system
surfaces: [shared]
platform: shared
source: code
last_reviewed: 2026-06-15
maturity_score: 70
tags: [orbit, design-brain, examples]
---

# examples/ — Golden Examples

Canonical, copy-able reference implementations. Few-shot exemplars move design quality
more than any amount of prose, so this folder is high-leverage.

Every example must declare `platform` in frontmatter:
`connected-platform`, `orbit-client-connected-platform`, `shared`, or `unknown`.

## What goes here
- 2–3 reference components per family, implemented to contract and to the brain.
- Ideally the real, current Orbit implementations — not idealised mockups.
- A short header in each file: what it demonstrates and which contract it satisfies.

## Suggested first set
- A data-dense table row (comfortable + compact)
- The primary button in all states
- A form field with label, help, and error
- The ClauseIQ focus-mode results pattern (your precedent-setting full-page pattern)

## Required First Set
| Example | File | Source status |
| ------- | ---- | ------------- |
| Data table with dense rows and compact mode | `data-table-dense.md` | source-backed; compact product example still needed |
| Primary button in all states | `button-states.md` | source-backed; loading state missing |
| Form field with help and error | `form-field-validation.md` | source-backed; field wrapper missing |
| Dialog or drawer keyboard behavior | `dialog-keyboard.md` | source-backed for dialog; drawer missing |
| ClauseIQ guided results workflow | `clauseiq-focus-mode-results.md` | source-backed by prototype |
| MarketIQ / RFP Analytics KPI chart view | `analytics-kpi-chart.md` | benchmark-backed; product source still needed |
| Lovable initiatives prototype port | `lovable-initiatives-port.md` | benchmark-backed |
| Work card — CP research primer (incl. reference `.tsx`) | `work-card-research-primer.md` | benchmark-backed; reference code + both-theme screenshots included |
| Tool-run flow — MarketIQ research output (code-backed) | `orbit-client-marketiq-research-output-flow.md` | synthesised + judgment-layer-validated (UX 15/16); reference `.tsx` |

## Platform Golden Examples

These examples are extracted from user-provided platform screenshots. They are useful as
visual truth candidates, but remain `in-review` and restricted until design-system owners
approve sanitization.

| Platform | Example | File | Source status |
| -------- | ------- | ---- | ------------- |
| Connected Platform | Home shell dashboard | `connected-platform-home-shell-dashboard.md` | screenshot-backed; in-review |
| Connected Platform | Initiative list/table | `connected-platform-initiative-list-table.md` | screenshot-backed; in-review |
| Connected Platform | ClauseIQ contract wizard modal | `connected-platform-clauseiq-contract-wizard-modal.md` | screenshot-backed; in-review |
| Connected Platform | Supplier tracker table | `connected-platform-supplier-tracker-table.md` | screenshot-backed; in-review |
| Orbit / Client Connected Platform | Home AI tools dashboard | `orbit-client-home-ai-tools-dashboard.md` | screenshot-backed; in-review |
| Orbit / Client Connected Platform | Sourcing execution tool hub | `orbit-client-sourcing-execution-tool-hub.md` | screenshot-backed; in-review |
| Orbit / Client Connected Platform | MarketIQ guided workflow | `orbit-client-marketiq-guided-workflow.md` | screenshot-backed; in-review |
| Orbit / Client Connected Platform | MarketIQ research output and next actions | `orbit-client-marketiq-research-output-next-actions.md` | screenshot-backed; in-review |
| Orbit / Client Connected Platform | Delivery Engine initiative detail | `orbit-client-delivery-engine-initiative-detail.md` | screenshot-backed; in-review |

## Benchmark Screenshot Reference Pack
Use the dated screenshot pack as benchmark-route evidence across themes and density
modes. Do **not** treat it as canonical platform visual precedent if it conflicts with
current product screens, Storybook, or design-system owner guidance:

- Artifact:
  `design-brain/_benchmarks/results/2026-06-15-golden-visual-reference.md`
- Screenshot directory:
  `design-brain/_benchmarks/results/screenshots/2026-06-15-golden-visual-reference/`

## Platform Visual Truth

Authoritative visual screenshots live under:

- Connected Platform:
  `design-brain/examples/screenshots/connected-platform/manifest.md`
- Orbit / Client Connected Platform:
  `design-brain/examples/screenshots/orbit-client-connected-platform/manifest.md`

## How agents use this
Skills and contracts point here. When output drifts toward a generic look, the agent
re-anchors on the nearest platform-matched example before continuing.
