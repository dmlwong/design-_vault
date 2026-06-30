---
type: review
status: in-review
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-06-24
maturity_score: 0
tags: [orbit, design-brain, status, summary, handoff]
---

# State of the Design Brain — 2026-06-24

A full summary of where the brain stands: what we built, what's outstanding, and what to
review next to make it better. Companion to `_review/Action Plan.md` (the running TODO) and
`_review/Session Change Log.md` (every file changed + sign-off checklist).

## 0. Orientation — where it lives now
- **Canonical vault (edit here):** `~/Library/CloudStorage/OneDrive-Efficio/Orbit Design Brain` (company OneDrive, opened in Obsidian).
- **Old local copy:** `~/Documents/Codex/Design_Brain` — **stale; delete it** once OneDrive opens cleanly in Obsidian.
- **Safety backup:** `~/Design_Brain_backup_2026-06-24` — delete when confident.
- **Portable:** all `/Users/...` paths converted to repo-relative; safe to share to any machine.
- **Product repo (consumer):** `efficio-orbit` — the brain is **NOT yet exported** with the
  current content (it has a stale older export). Exporting is the next real step.

---

## 1. What we've done

**Mapped & understood** the whole brain (foundations, 10+ component contracts, 10 pattern
contracts, examples, skills, governance).

**Built the `defaults.md` layer** — the "when unsure, use these" decisions (spacing, buttons,
density, cards, icons, status), sourced from real Orbit code + the platform screenshots.

**Added personas** (provisional) to both platform profiles — *trait → design consequence*.

**Built the Discovery system** — a 4D-aligned, tuned template + README + lifecycle, and **two
distilled packs** from your real Word docs (MarketIQ n8n; Research Agent in Initiatives).

**Decided & documented the sync model + maintenance workflow** — vault canonical, repo gets a
generated copy, "edit the vault, never the copy."

**Built a stress-test harness and ran two A/B tests** (baseline vs brain):
- Codex run: brain clearly beat baseline (manual ~17 vs ~11; the AI reviewer was invalid —
  harness since fixed).
- Claude run: **brain 17/18 vs baseline 13/18** (valid, independently verified).
- **Rendered the output in both Efficio + Orbit themes** — visually confirmed the brain card
  is denser, has one clear primary action, and switches themes via tokens alone.

**Closed every gap the tests surfaced:** canonical icon system (`FaIcon`, never lucide),
approved status mappings, a new `StatusIndicator` contract, a new `Chip` contract, the
`work-card` composition pattern, and a border-width default. **Settled 2 `[CONFIRM]`
decisions** (Shared-by-client → Information; Failed → Error).

**Promoted the first golden example with real reference code** —
`examples/work-card-research-primer` (.tsx + .md + both-theme screenshots).

**Made it portable and moved it off local** to company OneDrive (shareable).

**Created usage & onboarding artifacts** — `how-to-use-the-design-brain.html`,
`using-the-design-brain.html` (+ `.md`), `team-sharing-flow.html`, and the
`Session Change Log`.

---

## 2. What's outstanding (to finish / decide)

- [ ] **Export the current brain into `efficio-orbit`** — *the* step that makes Codex/Claude
      actually use this version. See `_review/Using the Design Brain — Step by Step.md`.
- [ ] **Team-share the OneDrive folder** — right-click → Share, or move to a SharePoint library.
- [ ] **Delete the stale local copy** (`~/Documents/Codex/Design_Brain`) after Obsidian opens
      the OneDrive vault cleanly; delete the backup when confident.
- [ ] **Owner sign-off** — promote `in-review` files to `stable` (use the checklist in
      `_review/Session Change Log.md`).
- [ ] **Confirm/correct the personas** with real user research (currently provisional — the
      one place I put words in your mouth about your users).
- [ ] **Resolve the remaining `[CONFIRM]`s** in `defaults.md` (Orbit-client outer page padding)
      and approve the `[SCREENSHOT]` platform-delta rows (pending screenshot sanitization).
- [ ] **Verify the two Discovery distillations** against the source Word docs.

---

## 3. What to review next to make it better (improvement backlog)

**Infrastructure / trust**
- Build the **export automation** — auto re-export + a **CI drift-check** (sync model is
  decided, not built). Turns "edit the vault, never the copy" into a guarantee.
- Add a **code→contract drift check** — flag when `efficio-orbit` changes a component API but
  its contract doesn't.
- **Tighten enforcement** — extend the audit to catch tokenized-but-wrong + border-width, and
  a Claude Code hook nudging contract-reading.

**Coverage / validation**
- **Breadth testing** — run the A/B on *other* task types (a form, an analytics view, an
  Orbit-client screen) and do a **real Codex confirmation run** (this session validated mostly
  with Claude).
- **Adoption test** — hand the brain to one teammate on real work and measure; the truest test.

**Content gaps (pre-existing)**
- Motion tokens; data-viz tokens; the drawer decision; production MarketIQ / RFP Analytics
  examples; human VoiceOver/NVDA/JAWS screen-reader confirmation (parked).
- Screenshot **sanitization & approval** of the visual-truth manifests → promote to `stable`.
- **More golden examples** — few-shot precedent is the highest-leverage quality lever; the
  `work-card` one is the first with real code.
- Lovable: re-sync projections or connect the Enterprise design system.

**Strategy reminders (decided this session)**
- **No external/competitor UI as "inspiration"** in the brain — it widens the model back out;
  the brain's value is constraint. Keep external refs in the human design process, upstream.

---

## 4. Key references
- `_review/Action Plan.md` — the running TODO list (most detailed).
- `_review/Session Change Log.md` — every file changed + decisions + owner sign-off checklist.
- `_review/Maintenance Workflow.md` — how to keep vault ↔ repo in sync.
- `_review/Using the Design Brain — Step by Step.md` (+ `.html`) — how to use it with Codex.
- `_benchmarks/results/2026-06-23-claude-stress-test-cp-research-card.md` — the validation result.
- `_review/how-to-use-the-design-brain.html` / `team-sharing-flow.html` — visual overviews.

## 5. The one rule
**Edit the vault, never the exported copy — then re-export.** Everything downstream flows
from that.
