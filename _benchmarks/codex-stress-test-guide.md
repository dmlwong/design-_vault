---
type: benchmark
status: stable
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-06-18
maturity_score: 70
tags: [orbit, design-brain, stress-test, codex, benchmark]
---

# Codex Stress-Test Guide (Option A — code + scorecard)

Validate that the Design Brain **measurably improves** AI UI output before investing in
automation. This is an **A/B test**: build the same screen twice — once **without** the
brain (baseline) and once **with** it — then have an adversarial reviewer score both.
Nothing is exported; Codex reads the vault directly.

> Output of this test = **real Orbit component code** + a **scorecard**, not rendered
> pixels. (To see rendered UI, use Option B — render as a benchmark route.)

## Paths

- **Vault (the brain):** `the Design Brain vault`
- **Product repo (real components/tokens):** `the efficio-orbit repo`
- **Scratch output (keeps the repo untouched):** `~/brain-stress-test/`  (`mkdir -p ~/brain-stress-test`)
- **Final scorecard:** save into `_benchmarks/results/` (date-named, per convention).

## The one trap: keep the baseline clean

`efficio-orbit/AGENTS.md` auto-loads a (stale) brain for Codex. If the baseline reads it,
the A/B is contaminated. So the **baseline prompt explicitly tells Codex to ignore all
brain/AGENTS guidance** and build from its own judgment + the component library only. Both
arms get the **same functional task**; only the brain arm gets the brain's *design
guidance*.

## Safety — do not touch the design system (applies to every run)

The build runs use `efficio-orbit` only as a **read-only reference**. Guard it three ways:

1. **In the prompt** (baked into each run below) — read-only in `efficio-orbit`, write only
   to `~/brain-stress-test/`, no installs, no build/test/lint, no git writes.
2. **In Codex** — run in your **read-only / approval** mode so any write or command is
   surfaced for you to approve, not auto-applied. The prompt reduces risk; the approval mode
   is the real guarantee.
3. **Verify after each run** — `efficio-orbit` is a git repo, so run `git status` in it; it
   should show **no changes**. If anything was touched, revert it (`git restore <file>`)
   before continuing.

---

## The task under test (worked example)

**CP workspace "research" card** (from `discovery/research-agent-in-initiatives-cp-orbit.md`).
Functional requirements (the *what* — identical for both arms):

- A card in the **Connected Platform** workspace showing a generated research primer.
- Remove the summarised body text; show **3 buttons: Download, Re-run, Share**.
- **Re-run** opens a modal to select **Category / Countries** (like "add initiative"); sends
  a notification on re-run.
- **Share** = a paper-plane icon next to Download; shares to a CP share modal; status shows
  "Shared by client".
- Show a **timestamp + an icon for who generated it** (auto-generated → default to the
  initiative owner).
- The tool-coverage card has **exactly 2 states: Completed and Running** (no incomplete
  state — it's auto-triggered). Plus empty (no category selected → no pack).

---

> **Run order & access:** run 1 → 2 → 3 in that order. Run 3 (review) must be able to READ
> `~/brain-stress-test/` — if your Codex is sandboxed to its workspace, start the review
> session **from `~/brain-stress-test`** (or grant home-dir read), or it sees an empty folder
> and wrongly scores both files as missing.

## Run 1 — Baseline (no brain)

Start Codex in `efficio-orbit`. Paste:

```
Build a Connected Platform workspace "research primer" card as a React/TSX component.

SAFETY (do not damage the design system): you may READ the efficio-orbit repo to
learn its components and tokens, but do NOT create, edit, move, rename, or delete ANY file
inside it, do NOT install packages, and do NOT run build/test/lint/format or any
git-writing command. The ONLY file you write is ~/brain-stress-test/baseline.tsx (outside
the repo; it does NOT need to compile — it is a throwaway test artifact).

IMPORTANT: Do NOT read or follow AGENTS.md, CLAUDE.md, or anything under design-brain/.
Build from your own judgment plus whatever component library you find (read-only) in the repo.

Requirements:
- Card showing a generated research primer in the CP workspace.
- No summarised body text; 3 buttons: Download, Re-run, Share.
- Re-run opens a modal to pick Category / Countries; notify on re-run.
- Share = paper-plane icon next to Download; status shows "Shared by client".
- Timestamp + icon for who generated it (auto -> default to initiative owner).
- Tool-coverage card has 2 states only: Completed and Running. Plus an empty state.

Write the component to ~/brain-stress-test/baseline.tsx. At the top, in a comment, list
every colour/spacing/component choice you made and where each value came from.
```

## Run 2 — Brain

Start a **fresh** Codex session in `efficio-orbit`. Paste:

```
SAFETY (do not damage the design system): you may READ the efficio-orbit repo and
the vault, but do NOT create, edit, move, rename, or delete any file inside efficio-orbit,
do NOT install packages, and do NOT run build/test/lint or any git-writing command. The
ONLY file you write is ~/brain-stress-test/brain.tsx (outside the repo; it need not compile).

Before writing any code, read these files and follow them exactly:
- AGENTS.md
- design-brain/defaults.md
- design-brain/platforms/connected-platform.md  (incl. personas)
- discovery/research-agent-in-initiatives-cp-orbit.md
- the contracts: design-brain/components/card-panel.md, button.md, dialog.md, badge-status.md

Then build the SAME CP workspace "research primer" card (same requirements as the
discovery pack's Detailed UI / interaction notes). Honour the brain: Orbit tokens only,
Connected Platform profile + density, the defaults (button variant/size, card padding,
spacing tokens), all required states, and the discovery pack's UI notes.

Write the component to ~/brain-stress-test/brain.tsx. At the top, in a comment, list which
brain rules/contracts/defaults you applied.
```

## Run 3 — Adversarial review

Start a **fresh** Codex session. Paste:

```
SAFETY: read-only. Do NOT modify any file in efficio-orbit or the vault. The ONLY file you
write is ~/brain-stress-test/review.md.

FIRST verify both ~/brain-stress-test/baseline.tsx and ~/brain-stress-test/brain.tsx exist
and are non-empty (e.g. `ls -l ~/brain-stress-test`). If either is missing or unreadable,
STOP and write only: "RUN INCOMPLETE — baseline/brain artifact not found; rerun Runs 1-2."
Do NOT score a missing file as 0/18.

Begin review.md with a "## Proof of input" section, BEFORE any scoring, containing:
- the raw output of `ls -l ~/brain-stress-test`;
- for EACH of baseline.tsx and brain.tsx: its byte size, total line count, and the first 10
  lines pasted verbatim.
If either file is 0 bytes or its snippet is empty, STOP per the rule above. Every score you
give must cite the file:line you read it from.

Act as the Orbit design-reviewer. Read:
- design-brain/agents/design-reviewer.md
- AGENTS.md section 5 (Definition of Done)
- _benchmarks/scorecard-template.md

Then audit BOTH files:
- ~/brain-stress-test/baseline.tsx
- ~/brain-stress-test/brain.tsx

For EACH, score the 9 rubric categories 0-2 (Tokens only, Theme support, Full states,
Accessibility, Density, Contract match, Pattern match, Copy & motion, Orbit feel) for a
total /18, and give VERDICT: PASS/FAIL with BLOCKERS / MAJOR / MINOR (reviewer format).

Then add a "BRAIN GAPS" section: where the brain failed to prevent a problem, or was
silent/ambiguous and the agent had to guess. Be specific and cite file:line.

Write the full report to ~/brain-stress-test/review.md.
```

---

## Scoring rubric (0–2 each, target ≥ 16/18, no blocker)

Tokens only · Theme support (efficio + orbit) · Full states (default/hover/focus/active/
disabled/loading/empty/error) · Accessibility (keyboard, focus, AA, non-colour) · Density
(comfortable + compact) · Contract match · Pattern match · Copy & motion · Orbit feel
(dense/restrained/procurement-first, not generic SaaS).

## How to read the result

- **First, check the "Proof of input" block** at the top of `review.md` — non-zero file
  sizes and real code in the snippets. If it's empty or missing, the run is **invalid**
  regardless of the scores (this is exactly how the first run silently failed). Re-run
  before trusting anything below.
- **Brain should clearly beat baseline** and show: tokens only (no hex/px), CP platform
  correctness, all states present, defaults respected (e.g. `Button` Primary/Medium, card
  padding `Base`/`Small`, `--orbit-space-*` gaps), and an Orbit — not ShadCN — feel.
- **The baseline** shows the freelancing/generic gap the brain is meant to close.
- **The "BRAIN GAPS" section is the deliverable you asked for** — your prioritized backlog
  of what to improve in the brain. Feed each item back per `_review/Maintenance Workflow.md`
  (fix the vault file, not the output).
- **If the brain arm does NOT clearly win** → the brain needs work *before* automation.
  That's exactly the signal this test exists to give you.

## Re-running for other tasks

Swap the task + the linked files (platform profile, discovery pack, relevant contracts);
keep the three-run structure. Save each scorecard to `_benchmarks/results/` dated.

## Honest caveats

- Judges **code + the reviewer's assessment**, not rendered pixels (that's Option B).
- The reviewer is an AI — for anything high-stakes, a human spot-checks the scorecard.
- Keep the arms isolated: fresh Codex session per run; the baseline must genuinely not read
  the brain, or the comparison is meaningless.
