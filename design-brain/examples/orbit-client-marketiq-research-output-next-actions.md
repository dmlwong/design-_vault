---
type: example
status: in-review
owner: design-system
surfaces: [Orbit, Client Connected Platform, MarketIQ]
platform: orbit-client-connected-platform
source: user-provided
last_reviewed: 2026-06-15
maturity_score: 65
tags: [orbit, design-brain, example, visual-truth, client-connected-platform, marketiq, results]
---

# Golden Example: Orbit Client MarketIQ Research Output And Next Actions

## Demonstrates
- Client-facing generated output state.
- Report download/save actions.
- Next action cards after completion.

## Screenshot Evidence
- Primary screenshot:
  [orbit-client-marketiq-research-output-next-actions.png](screenshots/orbit-client-connected-platform/orbit-client-marketiq-research-output-next-actions.png)

Screenshot is in-review and restricted until design-system owners approve sanitization.

## Pattern Represented
Generated report output and follow-on workflow for Orbit / Client Connected Platform.

Use this when creating or reviewing generated outputs, report result pages, completion
states, or next-step guidance for external users.

## Components Visible
- Output/result card.
- Research parameter summary.
- Generated status label.
- Save toggle.
- Download action.
- Secondary rerun action.
- Next action cards.

## Layout Guidance
- Keep the generated output and its parameters together so users know what produced the
  result.
- Place save/download actions near the output they affect.
- Use next action cards to continue the workflow, not as generic recommendations.
- Preserve the selected initiative context in the surrounding shell/work surface.

## Density Guidance
- Keep result metadata compact and easy to verify.
- Give primary output actions enough room to be obvious.
- Avoid excessive whitespace between output and next action options.

## Copy Guidance
- State generated status clearly.
- Use client-safe action labels such as download, save, run again, update milestone.
- Avoid implying final approval when the result is only generated or ready for review.

## Imitate
- Parameter traceability.
- Download/save proximity.
- Concrete next actions.
- Client-facing completion clarity.

## Do Not Imitate
- Fake finality for AI-generated output.
- Vague "continue" actions.
- Hidden report state.
- Internal process language unless it is visible to clients.

## Review Questions
- What is the approved language for generated reports?
- What happens when download fails or generation has partial data?
- Should "Ask Athena" have a dedicated contract or pattern rule?
