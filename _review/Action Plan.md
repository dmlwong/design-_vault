---
type: review
status: in-progress
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-06-17
maturity_score: 50
tags: [orbit, design-brain, action-plan, todo]
---

# Action Plan — Orbit Design Brain

Running to-do list for finishing the current additions (defaults, personas, Discovery)
and closing the structural and source gaps. Ordered by priority.

**Legend:** 🤝 = an AI agent can do this with/for you · 🧠 = only you (needs product
knowledge or owner authority).

> If you do nothing else, do Phases 1–3 — that loop delivers value and proves the system
> before investing in the rest. Phase 4 is what makes it a *team* foundation, not a
> personal one.

## Phase 1 — Finish what was just built
Goal: the three new additions are filled in.

- [x] 🤝 Confirm the `[CONFIRM]` rows in `design-brain/defaults.md` — DONE 2026-06-17:
      field/section gaps sourced from the settings form benchmark (corrected `-m`→`-l`);
      CP + Orbit-client platform deltas confirmed from screenshot packs; outer page
      padding sourced from `CpWorkspaceShell` / `OrbitAppShell`. `defaults.md` now
      `in-review` (maturity 70). Only judgement call left: the new-page padding value for
      Orbit-client (shell defines none) — needs owner sign-off.
- [~] 🧠 Fill personas in `design-brain/platforms/connected-platform.md` (internal) and
      `design-brain/platforms/orbit-client-connected-platform.md` (external) — 2–3 each,
      every line as *trait → design consequence*. **Provisional drafts written 2026-06-17,
      marked `[CONFIRM]`** (inferred from audience def + screenshots). YOU still need to
      correct names/roles/traits with real research before `stable`.
- [x] 🤝 Discovery template + first pack — DONE 2026-06-17: rebuilt `_TEMPLATE.md` to
      match the real **4D Concept Discovery Pack** structure, then **tuned it against the
      AI-Native Design-to-Delivery guides** — it now maps to the START first-session
      routine (added Prior decisions & rejected alternatives, delivery learnings, states-to-
      design) and pre-fills the HAND OVER Part D delivery context (assumptions / dependencies
      / risks / outstanding decisions + owner). Worked example distilled from the MarketIQ
      n8n Word doc; lifecycle convention + index row in `discovery/README.md`. Future packs:
      distil the Word doc into this template each sprint.
- [x] 🤝 Validation test (2nd real pack) — DONE 2026-06-17: ran a UI-heavy doc
      (`research-agent-in-initiatives-cp-orbit.md`) through the template. Held up well;
      surfaced 2 real gaps → added **Reference designs & visual truth** (Figma/AI-design link
      + annotated screenshots) and an optional **Detailed UI / interaction notes** section.
      Backfilled doc 1 with the new field (N/A). Template now validated against both a
      backend-heavy and a UI-heavy concept.
- [ ] 🧠 Promote `design-brain/defaults.md` from `status: draft` → `in-review` once
      confirmed.

## Phase 2 — Ship it to the tools
Goal: Codex and Claude Code actually see the new files.

- [ ] 🤝 Dry-run the export:
      `python3 tools/export_brain.py --target <path-to-efficio-orbit> --profile all --dry-run`
- [ ] 🤝 Run the real export (drop `--dry-run`).
- [ ] 🧠 Verify in Claude Code: open the repo, `/context` shows `CLAUDE.md` + `AGENTS.md`;
      ask "what's the default button and spacing?" — a correct answer means it works.

## Phase 3 — Prove it works (most important)
Goal: confirm the brain stops the padding/button freelancing.

- [x] 🤝 Run the AI on one real screen — DONE 2026-06-19 (CP research card, Codex A/B).
      **Result: brain clearly wins ~17/18 vs ~11/18** (manual scoring — the AI reviewer
      couldn't see the scratch files and was invalid; guide fixed). Full result:
      `_benchmarks/results/2026-06-18-codex-stress-test-cp-research-card.md`. 4 brain gaps
      found (status taxonomy, icon system, StatusIndicator, card composition) — see next item.
- [x] 🤝 Feed the 4 stress-test BRAIN GAPS back — ALL DONE 2026-06-19: (1) icon system →
      `defaults.md` Icons + `anti-patterns.md` (canonical `FaIcon`, never lucide — verified
      61 vs 0); (2) status taxonomy → `badge-status.md` Badge-vs-StatusIndicator + approved
      mappings; (3) `StatusIndicator` → new contract `components/status-indicator.md` (indexed);
      (4) card composition → new pattern `patterns/work-card.md` (indexed + cross-linked from
      `card-panel.md`). **`[CONFIRM]` decisions SETTLED 2026-06-24:** "Shared by client" →
      Information, "Failed" → Error (in `badge-status.md`).
- [x] 🤝 Tune the files where it falls short — fix the file, not just the output. DONE
      2026-06-23/24: closed all 4 Claude-run gaps; **promoted the validated brain card to the
      canonical golden example** `examples/work-card-research-primer.md` (+ reference `.tsx` +
      both-theme screenshots); settled the two `[CONFIRM]` status decisions. (Lever 1 of the
      optimisation plan — golden examples raise the floor for every future run.)
- [ ] 🧠 Re-run the same task until it passes without hand-holding. Only then scale to
      more personas / Discovery packs.

## Phase 4 — Team-readiness (structural gaps)
Goal: it survives leaving one machine and being used by someone else.

- [x] 🤝 **Portability — DONE 2026-06-24.** All `/Users/derekwong/...` absolute paths
      converted to repo-relative (source → `packages/orbit/...`; commands →
      `<path-to-efficio-orbit>`). 0 absolute paths remain.
- [x] 🤝 **Vault moved off local — DONE 2026-06-24.** Canonical home is now the company
      OneDrive: `~/Library/CloudStorage/OneDrive-Efficio/Orbit Design Brain`. Backup at
      `~/Design_Brain_backup_2026-06-24`. **Next: share the OneDrive folder with the team (or
      move to a SharePoint library); delete the stale local copy at `~/Documents/Codex/Design_Brain`.**
- [~] 🤝 **Sync model DECIDED (2026-06-18):** vault stays canonical (authors edit in
      Obsidian, no git); repo gets a generated copy kept in sync by automation, not by hand.
      Workflow recorded in `_review/Maintenance Workflow.md`. **Still to build:** (a) auto
      re-export job/hook, (b) CI drift-check (`export_brain.py --dry-run` fails the build if
      copy ≠ vault). The "one rule": edit the vault, never the copy.
- [ ] 🤝 Enforcement: add a CI / pre-commit check that runs `npm run audit:design-system`
      on PRs; optionally a Claude Code hook that nudges contract-reading before edits.
- [ ] 🧠 Adoption test: hand the brain to one teammate, give a real task, measure their AI
      output against the rubric. The only true test of "shared foundation."

## Phase 5 — Close the real source gaps (pre-existing)
Goal: the brain can keep its promise where it currently can't.

- [ ] 🧠 Motion tokens — decide whether to add `--orbit-motion-*` / `--orbit-ease-*` to the
      code, then mark `motion.md` stable.
- [ ] 🧠 Data-viz tokens — add `--orbit-color-viz-*` families; unblocks MarketIQ / RFP
      Analytics.
- [ ] 🧠 Drawer decision — reusable `Drawer` component, or keep using `Overlay`?
- [ ] 🧠 Screenshot sanitization & approval — work through
      `_review/Platform Visual Truth Review Checklist.md`; promote approved files
      `in-review` → `stable`.
- [ ] 🧠 Production MarketIQ / RFP Analytics examples — link real screens to the golden
      examples.
- [ ] 🧠 Human screen-reader pass — the parked VoiceOver/NVDA/JAWS session
      (`_review/Parked Items.md`).

## Phase 6 — Keep it alive (ongoing)

- [ ] 🤝 Drift detection — a job that re-extracts contracts and flags where source ≠
      contract.
- [ ] 🧠 Lovable — re-sync projections after token changes, or move to the Enterprise
      Design System connection (kills the manual-paste rot).
- [ ] 🧠 Review cadence — weekly → monthly → quarterly as the brain matures
      (`_review/Governance.md`).

## Parked for Phase 2 (deferred ideas)
Captured, not started — revisit after the brain is exported, shared, and adoption-tested.

- [ ] 🤝 **Platform shell templates (parked 2026-06-25).** Document the canonical app shell
      (left nav + header) per platform so the AI frames every *full screen* correctly — the
      shell is the biggest "platform identity" element. Mostly **documentation, not new
      code**: CP already has `packages/orbit/src/navigation/CpWorkspaceShell.tsx`
      (source-backed → add a `shell` pattern contract + golden example). Orbit-client's
      `OrbitAppShell` (in `apps/prototypes`) is thin/prototype-only — investigate whether it
      needs hardening into a shared component (design-system-owner decision). High-leverage
      golden-example candidate; pairs with the platform profiles + page patterns.
