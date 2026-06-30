---
type: benchmark
status: in-review
owner: design-system
surfaces: [Connected Platform]
platform: connected-platform
source: code
last_reviewed: 2026-06-19
maturity_score: 60
tags: [orbit, design-brain, stress-test, codex, result]
---

# Stress Test Result — CP Research Card (Codex, A/B)

- **Task:** CP workspace "research" card (from `discovery/research-agent-in-initiatives-cp-orbit.md`)
- **Tool:** Codex · **Date run:** 2026-06-19
- **Outputs:** `~/brain-stress-test/baseline.tsx`, `brain.tsx`, `review.md`

> **The AI reviewer (`review.md`) is INVALID** — it could not access `~/brain-stress-test/`
> (sandbox), saw an empty folder, and scored both files `0/18 FAIL` as "missing". Scores
> below are a **manual review of the actual code**. Guide updated so the reviewer verifies
> the files exist first and runs with access to the scratch folder.

## A/B scorecard (manual; approximate — code not compiled/rendered)

| Category | Baseline (no brain) | Brain |
| -------- | ------------------- | ----- |
| Tokens only | 2 — Orbit tokens via a raw `<style>` block | 2 — inline token styles, real tokens (verified) |
| Theme support | 2 | 2 |
| Full states | 1 — ~1 card state; running/empty only at tool-coverage level | 2 — completed/running/empty/error/disabled, all demoed |
| Accessibility | 1 — some aria; raw `<button>`, no dialog close | 2 — aria-live, IconButton close, required/invalid wiring |
| Density | 1 — hardcoded `Small`, no toggle | 2 — `Default`/`Compact` prop |
| Contract match | 1 — raw `<button>` for Cancel (violation) | 2 — Orbit `Button`/`IconButton`, Card non-interactive |
| Pattern match | 1 — invented composition | 1.5 — invented but contract-aligned |
| Copy & motion | 1 — minimal copy | 2 — designed state/error/empty copy |
| Orbit feel | 1–2 | 2 |
| **Total (approx)** | **~11/18** | **~17/18** |

- **Verdict:** Brain clearly wins (~6 points). The brain did NOT rescue a generic output —
  the baseline found the real Orbit components/tokens on its own. The brain's value showed
  up as **completeness & discipline**: all states, both densities, contract fidelity,
  deeper a11y, and designed copy — the DoD items an unguided agent skips.

## Best gap signal: where the two arms DIVERGED

(Where baseline and brain made *different* choices = where the brain failed to constrain.)

## BRAIN GAPS (backlog → feed back into the vault)

- [x] **Status taxonomy is unconstrained.** *(FIXED 2026-06-19 — `badge-status.md` mappings.)* "Shared by client": baseline → `No Status`,
      brain → `Information`. "Completed/Running": baseline → `StatusIndicator`, brain →
      `Badge`. `badge-status.md` says the taxonomy "is not canonical" → agents invent
      mappings. **Fix:** approved status→token mappings for recurring workflow statuses, or a
      rule to define them in the discovery pack.
- [x] **Icon system unspecified.** *(FIXED 2026-06-19 — `FaIcon` canonical in `defaults.md`/`anti-patterns.md`.)* Baseline used `FaIcon` (Font Awesome Pro unicode); brain
      used `lucide-react`. The brain says nothing about icons → divergence + license risk.
      **Fix:** state the canonical icon approach in `defaults.md`.
- [x] **`StatusIndicator` is undocumented.** *(FIXED 2026-06-19 — `components/status-indicator.md`.)* Baseline used a real `StatusIndicator`
      component with no contract / no Badge-vs-StatusIndicator guidance. **Fix:** add a
      contract or a "when to use which" note.
- [x] **No composition/pattern for this card.** *(FIXED 2026-06-19 — `patterns/work-card.md`.)* Both arms invented different compositions
      (`Card` has no header/footer/action slots). **Fix:** a card composition note in the
      pattern layer or the discovery pack.

## Notes

- Baseline was genuinely brain-free (used its own judgment + the repo), so the A/B is valid.
- Brain typography tokens verified real (`--orbit-text-h5-size` etc. exist in typography.css).
