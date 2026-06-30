---
type: example
status: in-review
owner: design-system
surfaces: [Orbit, Client Connected Platform, MarketIQ]
platform: orbit-client-connected-platform
source: user-provided
last_reviewed: 2026-06-15
maturity_score: 65
tags: [orbit, design-brain, example, visual-truth, client-connected-platform, marketiq, workflow]
---

# Golden Example: Orbit Client MarketIQ Guided Workflow

## Demonstrates
- Client-facing guided workflow from tool intro to initiative selection and generation.
- Selected initiative context.
- Modal table selection inside a guided MarketIQ flow.

## Screenshot Evidence
- Intro/start:
  [orbit-client-marketiq-intro-get-started.png](screenshots/orbit-client-connected-platform/orbit-client-marketiq-intro-get-started.png)
- Select initiative:
  [orbit-client-marketiq-select-initiative.png](screenshots/orbit-client-connected-platform/orbit-client-marketiq-select-initiative.png)
- Initiative selection modal:
  [orbit-client-marketiq-select-initiative-modal.png](screenshots/orbit-client-connected-platform/orbit-client-marketiq-select-initiative-modal.png)
- Research parameters and generate action:
  [orbit-client-marketiq-research-parameters-generate.png](screenshots/orbit-client-connected-platform/orbit-client-marketiq-research-parameters-generate.png)

Screenshots are in-review and restricted until design-system owners approve
sanitization.

## Pattern Represented
Guided conversational/tool workflow for an external client user.

Use this when creating or reviewing client-facing flows where a user selects context,
confirms parameters, and generates or requests an output.

## Components Visible
- Tool intro card.
- Primary start action.
- Selected initiative card.
- Modal table with search and tabs.
- Research parameter summary.
- Generate action.
- Toast/status feedback.

## Layout Guidance
- Keep the flow centered around the current task, not a broad marketing page.
- Preserve selected context after the user chooses an initiative.
- Use the modal table only for the selection decision; do not overload it with unrelated
  workflow steps.
- Keep the generate action close to the confirmed parameters.

## Density Guidance
- Give client users enough breathing room to understand context and next action.
- Keep modal tables dense enough to compare initiatives.
- Avoid turning the flow into a sparse stepper when the current screen can show selected
  context and parameters clearly.

## Copy Guidance
- Explain what MarketIQ does in client-safe language.
- Make next actions explicit: select initiative, run without initiative, generate,
  edit, cancel.
- Avoid internal shorthand unless visible in the product source.

## Imitate
- Selected context persistence.
- Clear primary action per step.
- Client-safe parameter summaries.
- Searchable modal table for initiative choice.

## Do Not Imitate
- Internal CP operational labels unless product source proves clients see them.
- Generic AI assistant framing.
- Hiding the selected initiative after modal close.
- Making generation look instant if real work is asynchronous.

## Review Questions
- Which MarketIQ copy is final client-facing copy?
- What are the loading, error, and permission states for generation?
- Should "run without an initiative" be available for all clients?
