---
type: review
status: draft
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-07-17
maturity_score: 0
tags: [orbit, design-brain, orchestration, build-pipeline, trial]
---

# Build-Pipeline Trial — 2026-07-17

The first run of the **full** orchestration build pipeline against real product code,
in the `efficio-orbit` component repo (`github.com/dmlwong/efficio-design-system`). The
in-vault dry run (`_review/2026-07-17-orchestration-dry-run.md`) only exercised
`context-scout → design-reviewer`; this trial adds the **builder** step and closes the
loop the whole orchestration effort was built to prove.

**Prerequisite unlocked the same day:** Storybook was wired into the component repo
(branch `claude/storybook-setup`), which (a) gave the upstream `extract-contract` stream
real stories to read and (b) gave the reviewer/verifier a way to render components.

## Task under trial

`build-component`: fix a tokens-only violation in `Button` —
`packages/orbit/src/actions/Button.module.css` used `filter: brightness(0.92)` for the
Positive/Destructive hover states (a hardcoded visual value, AGENTS.md §2.1). Chosen
because it was a **real defect surfaced by the extract-contract stream test**, and
because it turned out to require a *governed* change (a new token), so it exercised the
escalation path rather than a trivial edit.

## Pipeline exercised

`context-scout` (haiku) → `component-builder` (sonnet) → *(render-verify in Storybook)* →
`design-reviewer` (opus, fresh context). First loop, no rework.

## Run log

### Step 1 — context-scout (haiku)
Emitted a format-perfect packet: task key `build-component`, platform `shared` (correctly
loaded **both** platform profiles for a shared component), agent `component-builder
(sonnet)`, skill `component-contract`, `THEN: design-review`. MISSING: none (Button
contract exists). No design opinions. ✓

### Step 2 — component-builder (sonnet)
Read the Button contract + `tokens.md`, discovered **no hover token existed** for
Positive/Destructive (the reason the code reached for `brightness()`), and did the
correct tokens-only fix: added `--orbit-color-btn-primary-bg-positive-hover` (`#009b5a`)
and `-destructive-hover` (`#ce0030`) — each an exact 8% darken of its base, preserving
the prior look — and replaced the four `filter` rules with `background-color: var(...)`.
It verified `themes/orbit.css` has no Positive/Destructive override (so a single `:root`
value is correct for both themes), ran `npm run audit:design-system` before/after, and
**flagged the new tokens as a governed change needing owner sign-off** rather than
silently shipping them. It did not self-certify. ✓

### Step 3 — render-verify (Storybook, headless)
Rendered the Positive/Destructive stories in a real browser and asserted computed styles:
hover resolves to `rgb(0,155,90)` / `rgb(206,0,48)` with `filter: none`. The
`brightness()` filter is gone and hover is token-driven. ✓

### Step 4 — design-reviewer (opus, fresh context, blind)
Received only its definition + the review packet + the diff. **VERDICT: PASS, zero
blockers.** Independently confirmed the both-themes handling, verified the hex derivation
byte-for-byte, and added value the other stages missed:
- **Behavioral catch:** the old `filter` dimmed the whole button incl. the white label;
  the token darkens only the background → *better* hover label contrast. A real change,
  not a pure refactor — worth a PR note.
- **MAJOR (governance):** the two new tokens need owner sign-off before merge (values
  defensible as interim because they exactly reproduce prior behavior).
- **Pre-existing (not scored):** Positive base `#00a962` + white label ≈ 3:1 — under AA
  for normal text; flagged for separate owner tracking.
- **Contract gaps:** `button.md` never stated Positive/Destructive are unthemed and
  didn't enumerate hover tokens — the silence that made "both themes" ambiguous.

## Outcome & follow-through

- **Fix committed** to `claude/button-tokens-fix` (Button + the identical `IconButton`
  twin the reviewer flagged). Owner **approved the interim token values 2026-07-17**;
  the token comment records it.
- **Contract updated** (`components/button.md`): Positive/Destructive documented as
  intentionally unthemed; new hover tokens enumerated — the two contract gaps closed.
- **Pre-existing Positive-contrast concern** left for separate owner tracking (not caused
  by this change).

## Promotion decision

The orchestration doctrine set one condition for the builder agents: *a real
product-repo build through the full pipeline*. That is now met. Promoted `in-review →
stable` on the strength of this trial (build pipeline) and the same-day extract-contract
stream test:

- **`context-scout`** — exercised in the dry run **and** this trial.
- **`component-builder`** — exercised here; clean first-loop PASS.
- **`contract-extractor`** — exercised in the extract-contract stream test (blind
  extraction matched the contract and caught extra real defects).
- **`orchestration.md`** — the pipeline it describes is now proven end-to-end.

**Kept `in-review`** (not yet exercised by any real run): `screen-builder`, `porter`,
`benchmark-judge`, `vault-librarian`. `design-reviewer` was already `stable`.

## Owner follow-ups still open

- The two hover tokens are **interim** — re-source from a Figma hover ramp if/when defined.
- Positive base contrast (`#00a962` + white ≈ 3:1) — decide separately.
- `IconButton` fix rides the same branch; both land when `claude/button-tokens-fix` merges.

<!-- graph-links:start — generated by tools/gen_graph_links.py; do not hand-edit -->
## Vault graph
[[_review/2026-07-17-orchestration-dry-run|2026-07-17-orchestration-dry-run]] · [[design-brain/components/button|button]] · [[design-brain/orchestration|orchestration]] · [[design-brain/tokens|tokens]]
<!-- graph-links:end -->
