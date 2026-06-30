---
type: benchmark
status: in-review
owner: design-system
surfaces: [Connected Platform]
platform: connected-platform
source: code
last_reviewed: 2026-06-23
maturity_score: 70
tags: [orbit, design-brain, stress-test, claude, result]
---

# Stress Test Result — CP Research Card (Claude A/B, 2026-06-23)

- **Task:** CP workspace research-primer card (`discovery/research-agent-in-initiatives-cp-orbit.md`)
- **Tool:** Claude (subagents) — tool-agnostic: brain arm read `AGENTS.md` + `design-brain/`
  markdown only (what Codex reads), no `CLAUDE.md` / Claude skills.
- **Outputs:** `~/brain-stress-test/claude/{baseline,brain,review}.tsx|md`

> **Reviewer VALID this time** (verified file existence + proof-of-input; the harness fix
> held). Independently spot-checked: file sizes match, no lucide import (only a comment),
> both `1px` borders real, baseline density absent, Chip-vs-Badge divergence real.

## Scorecard

| File | Total | Verdict | ICON | STATUS map | WORK-CARD |
| ---- | ----- | ------- | ---- | ---------- | --------- |
| baseline (no brain) | **13/18** | FAIL | PASS | FAIL (Chip not Badge) | PARTIAL (no Primary in card) |
| brain | **17/18** | PASS | PASS | PASS | PASS |

Brain won the categories it most directly governs: **Full states** (2 vs 1), **Density**
(2 vs 0), **Contract match** (2 vs 1). Brain's only ding: a raw `1px` border width.

## Recent fixes verified landing
- **Icon (`FaIcon`)** — both arms PASS. (Note: Claude's baseline found `FaIcon` on its own;
  the lucide defect was Codex-specific and did NOT recur here.)
- **Status mappings** — brain used Completed→Success, Running→Information, and flagged
  "Shared by client"→Information as `[CONFIRM]`. Baseline got the values but used `Chip`.
- **work-card composition** — brain followed it (one Primary, correct anatomy); baseline
  had no Primary in the card body.

## Codex vs Claude (honest)
Claude's baseline (13) is stronger than Codex's (~11) because Claude explored the library
and independently used `FaIcon`/`StatusIndicator`. Confirms: the brain's *marginal* value
differs per agent; some gaps (lucide) are agent-specific. Brain wins on both. A Codex
confirmation run is still worth doing when access returns.

## NEW BRAIN GAPS (agent-agnostic — port to Codex too)

- [x] **`Chip` is undocumented.** *(FIXED 2026-06-24 — `components/chip.md`.)* Both arms needed a card-level status chip; baseline used
      `Chip`, brain used `Badge`. No `Chip` contract exists, and `badge-status.md` doesn't
      say which primitive carries a card-level status chip. → add a `chip` contract + state
      "card-level status chip = `Badge`".
- [~] **Card-level state model under-constrained.** *(demonstrated by the golden example's 5-state union.)* `work-card.md` lists states but binds
      none to a generated-output card's data model → coverage ranged baseline-near-zero to
      brain-5-states. → give the pattern (or the discovery pack) a concrete state model.
- [~] **Density has no mechanism for a standalone card.** *(demonstrated: `density` prop in the golden example.)* Mandated but no "how" → baseline
      skipped it (Density=0), brain invented a `density` prop. → defaults.md/work-card.md
      should say HOW one card exposes compact.
- [x] **No border-width token guidance.** *(FIXED 2026-06-24 — `defaults.md` border-width default.)* BOTH arms hardcoded `1px` borders (even the brain).
      `--orbit-space-px` (=1px) exists but the brain never names it for hairline borders. →
      add a border-width default in defaults.md/tokens.md.
- [ ] Minor: auto-generated author glyph unspecified (robot vs smile divergence).

## Settled / promoted (2026-06-24)
- `[CONFIRM]` decisions settled: "Shared by client" → Information; "Failed" → Error.
- Validated brain card promoted to the canonical golden example:
  `examples/work-card-research-primer.md` (+ reference `.tsx` + both-theme screenshots).
