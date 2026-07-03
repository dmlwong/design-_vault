---
type: example
status: in-review
owner: design-system
surfaces: [Orbit, Client Connected Platform, MarketIQ]
platform: orbit-client-connected-platform
source: specified
last_reviewed: 2026-06-29
maturity_score: 72
tags: [orbit, design-brain, example, golden, tool-run-flow, interaction-defaults]
---

# Golden Example: Orbit-Client MarketIQ Research Output (tool-run flow)

> The code-backed reference for the **tool-run flow** shape (configure → generate → deliverable)
> on the Orbit / Client Connected Platform. It embodies `interaction-defaults.md` (the 8
> heuristics). **Validated 2026-06-29** via the judgment-layer A/B: the arm built to this flow
> scored **UX 15/16 vs 7/16** for the wizard baseline, with compliance held at 18/18. Anchor on
> it when building any tool that configures → generates → shows a deliverable.

## Why this exists
The brain had **no code-backed golden flow** for the most common Orbit shape — *an AI tool
that produces a deliverable*. The only tool-run precedent was prose + restricted
screenshots, and one pattern (`config-wizard`) actively modelled a stepper. With nothing to
imitate, the model defaulted to its training prior (the generic configuration wizard) — the
Contract Analysis failure (2026-06-25). This is the **"what it should have been,"** built
for a *different* tool (MarketIQ) so it teaches the shape without being the test's answer key.

## What it demonstrates — the 8 interaction-defaults, made concrete
Each maps to a heuristic in `interaction-defaults.md` and **inverts a specific
Contract-Analysis failure**:

| # | Heuristic | In this flow | The failure it inverts |
| - | --------- | ------------ | ---------------------- |
| 1 | Form, not wizard | one surface: params bar + output | a 4-step wizard for ~8 fields |
| 2 | Deliverable is the hero | the research output owns the screen; config is a slim bar; the empty-state CTA lives in the output area | an all-config screen, result hidden behind a button |
| 3 | Restraint in status colour | `StatusIndicator`/`Badge`; only the genuine error card carries a rail | whole cards tinted Information/Success/Highlight as decoration |
| 4 | Don't proceduralise inline selection | category/regions inline; initiative picker is a focused modal (the sanctioned escape) | a whole "Documents" wizard step that was just a table |
| 5 | Minimise steps / cut ceremony | no intro card, no review step, no "Next, you can…"; one Primary = Generate/Re-run | intro card + review step + generic next-steps card |
| 6 | Match platform model | `OrbitAppShell` + `PageHeader(type="tool")` + initiative pill, context persisted | (shared with anti-example, but here the shell frames a real output) |
| 7 | Progressive disclosure + smart defaults | essentials inline; regions/scope pre-filled behind "Adjust parameters" | every parameter forced up front across steps |
| 8 | Demo affordances dev-only | states driven by the `state` prop, never a shipped toggler | a Ready/Loading/Empty/Error button group baked into the UI |

## Also correct (the material layer the brain already gets right)
- **Tokens only** — every value an `--orbit-*` token; theme-agnostic (efficio + orbit).
- **Real Orbit components**, APIs verified against source. Uses `Card` **without** the
  deprecated `type` prop (prefers default/`hasShadow`) — modelling the fix for a defect
  found in the anti-example.
- **No invented charts.** Orbit has no chart component and data-viz tokens are a known gap,
  so the output is **numeric metric tiles + a `Table`**, not a fabricated graph.

## Reference implementation
- Code: `design-brain/examples/orbit-client-marketiq-research-output-flow.tsx` (self-contained;
  `state` prop drives `empty` / `generating` / `ready` / `error`).

## States
`empty` (CTA in the output area) · `generating` (inline status + skeleton, no coloured card)
· `ready` (output header with save/download near the output, metric tiles, findings, supplier
table) · `error` (rail + retry, parameters preserved).

## Source status
**Synthesised** to embody `interaction-defaults.md`, then **validated 2026-06-29** by the
judgment-layer A/B (the arm built to this flow scored UX 15/16 vs 7/16 for the wizard baseline,
compliance held at 18/18). It is a **compositional / interaction-model** reference — not
canonical platform *visual* precedent until confirmed against a live MarketIQ product screen.

## Scope (v1 — structure)
This is the **structure-level** golden flow: it teaches flow shape, IA, restraint, and the
escapes. Finer **information-design craft** — leading with risk signal over vanity metrics,
drillable summaries, structured (not prose) findings, insight→evidence→action links, collapsing
spent config — is a tracked follow-on (to be added with measured evidence, then reflected here).

## Related
- Heuristics: `interaction-defaults.md`
- Anti-example: `apps/prototypes/components/feature/contract-analysis/ContractAnalysisPrototype.tsx`
- Adjacent precedent: `examples/orbit-client-marketiq-research-output-next-actions.md`,
  `examples/orbit-client-marketiq-guided-workflow.md`
- Patterns it touches: `guided-conversational-workflow.md`, `review-and-approve-workflow.md`,
  `tool-hub.md`, `config-wizard.md`
- House-style reference: `examples/work-card-research-primer.tsx`

## Gap Report
- The reference `.tsx` does not mount `<OrbitInspector />` (AGENTS.md §2.8) — it is a
  self-contained component, not a full prototype root. When composing it into a
  generated prototype, mount the inspector once at the root layout per rule 8.
- Not validated against a live MarketIQ screen (compositional reference only).
- `InitiativePicker` is wired with an empty list in the reference — a real build passes
  initiatives; shown to demonstrate the focused-modal escape (#4), not the data.
- Reuses the thin prototype `OrbitAppShell` (the parked shell-template gap).
- Several components it leans on still lack contracts (`PageHeader`/`HeaderPresets`,
  `Spinner`, `Table` variants) — see the component-contract backlog.
- v1 is structure-level; information-design craft is a tracked follow-on (see Scope).
