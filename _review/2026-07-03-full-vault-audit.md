---
type: review
status: draft
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-07-03
maturity_score: 0
tags: [orbit, design-brain, audit, review, gaps]
---

# Full Vault Audit — 2026-07-03

> Scope: every active file in the vault (root docs, `design-brain/` incl. components,
> patterns, platforms, examples, skills, agents, lovable; `discovery/`; `_review/`;
> `_benchmarks/`; `_bases/`; `_canvases/`; `_exports/`; `tools/export_brain.py`).
> Goal assessed against: **a strong vault that can be shared across multiple teams as a
> single source of truth.**
>
> Verdict up front: the *content architecture* is genuinely strong — layered
> (material → structure → craft), source-backed, benchmark-validated, honest about its
> own gaps. What blocks cross-team sharing is not content quality; it is that the vault
> is still **wired for one person**, its **automation is documented but does not
> exist**, and its **status story contradicts itself across files**. Those are fixable
> in days, not months.

---

## A. CRITICAL — blocks "shared across teams" (fix before sharing)

### A1. The vault is single-user by construction
- `_review/STATE.md` anchors the canonical home to one machine:
  `~/Documents/Orbit Design Brain`, governs `~/efficio-orbit`, and lists personal stale
  copies to ignore. None of that is actionable for a second person.
- `.obsidian/workspace.json` (personal session state) is committed; it will churn and
  conflict the moment two people open the vault.
- The Obsidian Sync setup doc (`Team Sharing Setup.md`) was archived to
  `_archive/usage-guides-2026-06/` — yet `_review/Maintenance Workflow.md` still links
  it at `_review/Team Sharing Setup.md` (broken). There is currently **no live
  instruction for how a teammate gets, opens, and syncs the vault**.
- **Fix:** replace machine paths with the git remote + a clone/Sync instruction; restore
  (or rewrite) the team-sharing setup doc as an active file; gitignore
  `.obsidian/workspace.json` (keep shared config only).

### A2. The maintenance "robot" does not exist
`_review/Maintenance Workflow.md` presents auto-export, Obsidian-Sync distribution, and
a **CI drift-check** as the operating model ("CI fails loudly if the repo copy ≠ the
vault", "out of sync cannot happen silently"). In reality:
- There is **no `.github/`, no CI config, no scheduled job** anywhere in the vault.
- `tools/export_brain.py --dry-run` **always exits 0**, even when drift is found
  (`apply_ops` returns a count that `main()` ignores) — so the documented CI gate
  *cannot* fail a build even if someone wires it up.
- `_review/STATE.md` confirms even the manual export is still an outstanding task.
Drift protection is currently discipline, not structure — the exact failure mode the
workflow doc says is "structurally impossible."
- **Fix:** (1) make `--dry-run` exit non-zero when changes are found (or add
  `--check`); (2) add a real CI job (vault repo Action running the dry-run against the
  product repo, or in the product repo); (3) until then, reword the workflow doc to
  describe the *target* state, not the current one.

### A3. Restricted assets flow out unconditionally
- Both screenshot manifests mark all 18 platform screenshots **"restricted until
  design-system owners approve sanitization"** — but the PNGs are committed to the repo,
  and `export_brain.py` copies the entire `design-brain/` tree (including
  `examples/screenshots/**/*.png`) **and all of `_review/`** (STATE with personal paths,
  WIP files with internal test detail) into any target repo, on every profile except
  `lovable`.
- Policy and pipeline directly contradict each other; sharing the vault to more teams
  multiplies exposure before sanitization ever happened.
- **Fix:** decide sanitization (it has been pending since 2026-06-15); add an export
  exclusion list (screenshots-until-approved, `_review/` WIP/STATE); write a one-page
  access policy for the vault itself (who may see restricted assets, what "restricted"
  means once the vault is multi-team).

### A4. Placeholder names break resolvability
- The design-system repo is referred to as the literal string **`the efficio-orbit
  repo`** in **19 files** — including `CLAUDE.md`'s "Design-system source repo: `the
  efficio-orbit repo`", which is circular. A new team or agent cannot resolve it.
- The Lovable source prototype is literally **`Test`** in 8 files
  (`patterns/lovable-port.md` "Original source prototype: `Test`",
  `agent-benchmark-tasks.md` "Latest source prototype: `Test`", etc.) — meaningless to
  anyone who wasn't there.
- **Fix:** one canonical "Repositories & sources" note (real URL/path per environment),
  referenced everywhere; restore the prototype's real name/link or describe it.

### A5. No live onboarding for human audiences
The old usage guides (how to use the brain, building with Codex, running the export,
team sharing) were all archived as "old-era" with no replacement. `README.md` explains
structure; `AGENTS.md` addresses agents. **Nothing current tells a designer, PM, or
engineer what their workflow with the vault is.** For a multi-team SSOT this is the
front door.
- **Fix:** one `USING-THE-BRAIN.md` (or revived guide set) with per-role quickstarts:
  author (Obsidian), consumer-engineer (repo copy), PM (discovery packs), agent
  (AGENTS.md) — plus the governance path for proposing changes.

---

## B. MAJOR — trust & integrity defects

### B1. The vault contradicts itself about cycle-2 status
Three files, three different states for heuristics #9–#13:
- `design-brain/interaction-defaults.md` (canonical, exported): "**pending their own
  re-measure**".
- `_review/cycle2-craft-WIP.md`: "**RE-MEASURE DONE 2026-06-29 — VALIDATED**".
- `_review/STATE.md`: validated, awaiting owner red-line.
An agent reading only the canonical file gets stale facts. The promotion pipeline
stalled mid-flight and left the brain inconsistent.
- **Fix:** finish the promotion checklist in STATE (or at minimum update the note in
  `interaction-defaults.md` to "re-measure passed 2026-06-29; awaiting owner red-line").

### B2. Three parallel "current state" narratives
`README.md §Current Maturity` (frozen 2026-06-16, score 88), `_review/Maturity
Scorecard.md` (88, different exit criteria), and `_review/STATE.md` (2026-07-01,
"~82–88") all narrate progress and disagree. STATE also miscounts its own inventory:
"**14 component contracts, 10 page patterns**" — actual: **12** contracts, **11**
patterns.
- **Fix:** STATE.md is the right single narrative; cut README's maturity essay to two
  lines + a pointer, fold the scorecard's exit criteria into STATE, correct the counts.

### B3. Link/path convention chaos (~180 machine-unresolvable references)
Three conventions coexist, all as plain back-ticked strings (never Obsidian wikilinks
or markdown links):
1. vault-root-relative (`design-brain/tokens.md`),
2. **export-relative** (`design-brain/_benchmarks/...` — a path that does not exist in
   the vault, since `_benchmarks/` is at root; used by `accessibility.md`,
   `examples/README.md`, most benchmark results),
3. bare sibling names (`tokens.md`, `badge-status.md`).
Consequences: Obsidian backlinks/graph (a stated reason for using Obsidian) don't work;
no automated link check is possible; some references are genuinely broken
(`_review/Team Sharing Setup.md`; `AGENTS.md` cites the Lovable projection at
`lovable/knowledge-base.md` instead of `design-brain/lovable/…`).
- **Fix:** pick one convention (vault-root-relative), state it in `AGENTS.md`, convert
  high-traffic files, and add a tiny link-checker script to `tools/` (run in the same CI
  as A2).

### B4. Non-negotiable rule 8 (OrbitInspector) exists nowhere but the rule
`AGENTS.md` §2.8 and the Definition of Done require every generated prototype to mount
`<OrbitInspector />` — but **no other file in the vault mentions it**: no contract, no
pattern, no skill workflow, no design-reviewer checklist item, and **neither golden
`.tsx` reference mounts it**. The vault's own canonical examples violate its own
non-negotiable, and the reviewer can't catch it.
- **Fix:** add it to the two golden `.tsx` files (or scope rule 8 to product-repo
  prototypes explicitly), add a checklist line to `agents/design-reviewer.md`, and a
  short "inspector" note the routing table can point to.

### B5. Governance is written but not executable
- `Governance.md` requires a **named owner** for `stable`; every file's owner is the
  generic `design-system`. No CODEOWNERS/approval mechanics exist in the repo.
- The Change Request template has no filed examples; the forums (weekly WG, fortnightly
  council) have no records; the bulk item "promote ~71 `in-review` → `stable`" (STATE)
  has no owner or date.
- Contract↔code drift is undetectable: source-backed contracts don't record **which
  commit/version of `efficio-orbit` they were extracted from**, so nobody can tell when
  the code moves under them.
- **Fix:** name real owners in frontmatter for stable files; add a `source_commit:` (or
  `extracted_from:`) field to source-backed contracts; keep one lightweight
  decision-log; CODEOWNERS on `design-brain/` + `AGENTS.md` once multi-team.

### B6. tokens.md is out of sync with its own consumers
- Spacing family omits tokens the brain itself relies on: `--orbit-space-px`
  (the hairline default in `defaults.md`), `--orbit-space-xl` and `--orbit-space-0`
  (consumed in `data-table.md` / `button.md` token lists).
- `data-table.md` lists **`--orbit-color-silver`** — a primitive — with no gap flag,
  while the rules say "primitives stay behind aliases" (and `anti-patterns.md` bans
  reaching past semantic tokens).
- **Fix:** complete the family lists; flag the `Table` silver usage as a gap in the
  contract (and upstream, in the audit rule if possible).

---

## C. MAJOR — content gaps (what's missing for coverage)

### C1. Component contracts: 12 of ~38, and the golden examples outrun them
Missing contracts for components the vault itself already uses or names:
- **Used by golden examples/patterns now:** `PageHeader`/`HeaderPresets` (only
  partially covered inside `tabs.md`), `FaIcon`, `Spinner`, `Text`/`Headings`,
  the shells (`CpWorkspaceShell`, `OrbitAppShell` — the parked "shell template" gap).
  `orbit-client-marketiq-research-output-flow.md` flags this itself.
- **In the input family but uncontracted:** `Searchbox`, `TextArea`, `DateInput`,
  `CurrencyInput`, `Checkbox`, `Toggle`, `ToggleCard`, `Dropzone`, `MultiStateButton`.
- **Flagged repeatedly, still open:** `Drawer` (draft since 2026-06-14; named the #1
  gap in 6+ files), Avatar/resource-stack, menu/checkbox-list (column visibility),
  virtualized table.
- **Fix:** rank by traffic (Phase 5 method) and contract the next ~8; decide Drawer —
  it is the single most-cited blocker in the vault.

### C2. Missing foundations
- **Layout/grid/breakpoints:** every pattern says "narrow screens" with no shared
  breakpoint spec or tokens — responsive behaviour is unspecifiable and unreviewable.
- **Motion tokens** and **data-viz tokens**: known, documented gaps — still open.
- **Iconography:** one row in `defaults.md`; no reference for sizing, pairing, or the
  `FA` constant set.
- **Localisation/i18n:** one line in `ux-copy.md` ("locale-aware") for a product with
  currency/date-heavy data and (per personas) KSA vs ROW deployments.
- **Forms:** no `FormField` wrapper contract (flagged in `settings-form-validation.md`)
  — help/error wiring is re-composed per screen.
- **Elevation usage** beyond token names; **empty-state copy library**.

### C3. ux-copy.md is the thinnest file for a copy-critical product (42 lines)
Its own "Don't" — inconsistent terms across ClauseIQ/MarketIQ/RFP surfaces — is
unpreventable without a **terminology glossary**. Also missing: number/date/currency
format spec (the personas are procurement professionals), error-message templates,
product naming rules (the vault itself alternates "Orbit", "Orbit / Client Connected
Platform", "CCP", "Orbit-client").

### C4. Accessibility specifics
- Target size has no number (WCAG 2.2 ⇒ 24×24 CSS px minimum); no zoom/reflow (400%)
  requirement; `prefers-reduced-motion` is promised in `defaults.md` but **no source
  component implements it** (motion.md confirms); human screen-reader confirmation
  parked (fine — but it gates any "AA verified" claim to teams).

### C5. Evidence gaps both platforms flag about themselves
Error, empty, loading, and permission-denied states are "underrepresented" in both
visual-truth notes; CP settings/admin screens missing; Orbit client form/error examples
missing; **RFP Builder and RFP Analytics — 2 of the 4 named surfaces — have no
examples and no production source at all** (Source Inventory: missing).

### C6. Personas stalled in a worse-is-live state
`platforms/connected-platform.md` still ships 3 provisional `[CONFIRM]` personas while
2 **confirmed, materially richer** personas (with design consequences like AI
Green/Amber/Red visibility at point of use) sit in `cp-personas-WIP.md`, which no
routing points to. Waiting for all 4 before writing anything means agents design
against the weakest version for weeks.
- **Fix:** either promote the 2 confirmed now (marked confirmed, 2 pending) or add a
  pointer from the profile to the WIP. Orbit-client personas remain fully provisional —
  schedule the research.

### C7. Discovery layer hasn't started operating
2 packs, both `draft (example)`, both carrying "verify against the source Word doc"
caveats. The per-sprint loop (distil → active → shipped → archived) has no live
instance. For cross-team adoption this is the layer PMs touch first.

---

## D. MINOR / HYGIENE

1. **Export manifest drift:** `REQUIRED_FILES` in `export_brain.py` omits
   `patterns/work-card.md`, `patterns/settings-form-validation.md`,
   `patterns/lovable-port.md` (copied anyway via tree copy, but the guard won't notice
   their deletion — the manifest silently rotted as patterns were added).
2. **Duplicate parked-items:** `_review/Parked Items.md` and
   `_benchmarks/parked-items.md` track the same item in two places.
3. **Stale indices:** root `README.md` structure diagram omits `discovery/`;
   `design-brain/README.md` file table omits `defaults.md`,
   `interaction-defaults.md`, `SETUP.md`, the visual-truth notes, and lists patterns as
   "seed: focus-mode-results, guided workflow" (there are 11). AGENTS.md §3 routing has
   no row for golden `examples/` (agents reach them only via contracts).
4. **Frontmatter inconsistencies:** `maturity_score` scale is defined nowhere;
   status vocab drifts (`in review` in template footers vs `in-review` in frontmatter;
   one `in-progress`); `badge-status.md` content updated 2026-06-24 but
   `last_reviewed: 2026-06-19`; component contracts carry no `platform:` key so the
   `_bases` views can't slice them by platform.
5. **File naming:** spaces in `_review/*.md` filenames break xargs/URLs/some tooling
   (this audit hit it); vault folder `design-_vault` vs canonical name "Orbit Design
   Brain".
6. **Canvas stale:** `Orbit Brain Map.canvas` has 7 nodes — missing platforms,
   defaults, interaction-defaults, discovery, skills.
7. **Example gaps (self-flagged, listed for the backlog):** no dedicated chip or
   status-indicator example; button loading state missing; no compact-density
   production table example.
8. **External URLs in discovery packs** (Jira, public figma.site) — confirm intended
   once the audience widens.
9. **Empty `.obsidian/app.json` / `appearance.json`** committed; decide the shared
   Obsidian config set deliberately.

---

## E. What is genuinely strong (keep, and say so to new teams)

- **Layered architecture with honest altitudes:** material (`tokens.md`/`defaults.md`)
  → structure (`interaction-defaults.md` #1–#8, validated 7/16→15/16) → craft (#9–#13,
  measured 0→10) → per-initiative (`discovery/`). The altitude map in
  `cycle2-craft-WIP.md` is better articulated than most commercial design systems.
- **Derive-don't-transcribe discipline:** contracts cite real source files and tests;
  invented facts are marked `specified`/`source-required`; gap reports are ordered and
  honest. The `[SOURCED]/[SCREENSHOT]/[CONFIRM]` marker system in `defaults.md` is
  excellent epistemic hygiene.
- **Measured, not asserted:** A/B stress tests with blind adversarial scoring, separate
  compliance/structure/craft axes, results filed. The disambiguation content
  (Badge vs StatusIndicator vs Chip, approved status mappings) was *earned* from
  observed agent divergence — exactly the feedback loop working.
- **Platform separation** is enforced at every layer (rules, profiles, visual truth,
  examples, anti-patterns, benchmark Task 6).

---

## F. Recommended sequence (to "shareable, trusted SSOT")

**Phase 1 — Shareability (days):** A1 personal-path removal + team setup doc; A3
sanitization decision + export exclusions + access policy; A4 placeholder resolution;
A5 role-based onboarding; gitignore workspace.json.

**Phase 2 — Trust (days):** A2 CI drift-check (fix exit code, add Action, run first
real export); B1 finish cycle-2 promotion; B2 single state narrative + correct counts;
B3 one link convention + checker; B4 OrbitInspector enforcement; B5 named owners +
`source_commit` pinning; B6 token list sync. Then run the stalled bulk promotion
(`in-review` → `stable`) with owners.

**Phase 3 — Coverage (weeks, by traffic):** Drawer decision; shell templates;
next ~8 component contracts (C1); breakpoints + iconography + glossary + FormField
(C2/C3); promote confirmed personas + finish 3–4 (C6); RFP Builder/Analytics sources
(C5); error/empty visual truth.

**Phase 4 — Operate:** first real `active` discovery pack through the full lifecycle;
quarterly health-check actually run once; benchmark re-runs pinned to design-system
releases.

---

## Status
draft · produced by full-vault audit 2026-07-03 · for design-system owner review
