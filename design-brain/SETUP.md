---
type: setup-guide
status: stable
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-06-14
maturity_score: 72
tags: [orbit, design-brain, setup]
---

# SETUP.md — Setting up the Orbit Design Brain

A step-by-step guide to go from the Obsidian vault scaffold to a working design brain
that improves what Codex, Claude Code, and Lovable produce.

> **Read this first — the one rule that matters.** Do **not** build all 38 component
> contracts before testing. Get a single component working end to end, prove it changes
> agent output, *then* scale. The failure mode of this system is endless building. Phases
> 1–4 below are the minimum that delivers value; everything after is refinement.

---

## Phase 0 — Canonical home (done in this vault)

Canonical vault layout:

```
Orbit Design Brain/
├── AGENTS.md            ← canonical brain and Codex entry point
├── CLAUDE.md            ← thin; @imports ./AGENTS.md
├── README.md            ← vault index
├── design-brain/        ← reference layer
├── _bases/              ← Obsidian database-like views
├── _canvases/           ← visual map
├── _review/             ← governance and change requests
├── _exports/            ← generated export notices
├── _benchmarks/         ← agent benchmark tasks
└── tools/               ← export scripts
```

`AGENTS.md` and `CLAUDE.md` sit at the vault root so they are also copied to product
repo roots during export.

---

## Phase 1 — Wire the always-on layer (done in this vault)

**Goal:** the hard rules load on every session, and the agents can already read your
real tokens and components.

1. Keep `AGENTS.md` and `CLAUDE.md` at the vault root.
2. Keep detailed files in `design-brain/`.
3. Export into product repos with `tools/export_brain.py`.
4. Fill product-repo commands in exported `CLAUDE.md` once the real repo is available.

**Verify (Claude Code):** open the repo, run `/context` — you should see `CLAUDE.md` and
the imported `AGENTS.md` loaded. Run `/memory` to confirm there are no stale conflicting
rules.

**Verify (Codex):** with `AGENTS.md` at the repo root it is read automatically before the
agent acts. Put any personal, cross-repo preferences in `~/.codex/AGENTS.md`.

> At this point — before any contracts — output already improves, because "tokens only,
> match Orbit, full states, WCAG AA" is now always in context and the agents can read your
> token and component files directly.

---

## Phase 2 — Point `tokens.md` at the real source (done)

**Goal:** the token contract references your real files instead of duplicating values.

1. `design-brain/tokens.md` now points to
   `packages/orbit/tokens.css` and the real token source
   files under `packages/orbit/styles/tokens/`.
2. The token contract lists the real semantic and component token families agents may
   use.
3. The validation command is `npm run audit:design-system` from
   `the efficio-orbit repo`.
4. `motion.md` records a source-backed gap: dedicated motion tokens were not found, and
   current source uses literal transitions.

**Verify:** ask an agent "list the semantic tokens I'm allowed to use for colour and
spacing, and where they're defined." A correct answer means the contract and the source agree.

---

## Phase 3 — Build one vertical slice (first pass done)

**Goal:** one component, fully documented and exemplified, end to end.

1. **Pick the component.** Choose the highest-traffic one that appears in your prototype —
   usually the data table or the primary button. (Phase 5 explains how to rank the rest.)
2. **Extract, don't invent.** Run the `extract-contract` skill
   (`design-brain/skills/extract-contract/SKILL.md`): it reads the real source and
   stories, pulls the public API, variants, states, and tokens, and produces the filled
   contract plus a gap report of what the code is missing.
3. **Write the contract.** Copy `design-brain/components/_TEMPLATE.md` to
   `design-brain/components/<name>.md` and fill every section from the extracted facts.
   Where the code is missing states (loading / empty / error / disabled), the contract
   specifies them — that gap is the contract doing its job.
4. **Add the golden example.** Point an entry in `design-brain/examples/` at the real
   implementation (or its Storybook story). Don't write an idealised mockup — use the
   actual component.

**Verify:** the contract's API matches the code exactly; every state is either present or
explicitly marked and justified.

---

## Phase 4 — Test the brain, then tune it (≈1 hr, the most important phase)

**Goal:** confirm the brain actually changes output, and correct it where it doesn't.

1. Give an agent a real task against the slice, e.g.:
   *"Using the design brain, refactor `<component>` so every state in its contract is
   implemented and all values come from semantic tokens."*
   or
   *"Build a new `<small composed view>` using the Orbit design brain and the
   `<component>` contract."*
2. Judge the output against the **Definition of Done** in `AGENTS.md` §5 — tokens only,
   both themes, all states, AA, both densities, copy, motion, no anti-patterns.
3. Wherever it falls short, **fix the relevant brain file**, not just the output:
   - Generic look → strengthen `principles.md` / `anti-patterns.md`.
   - Missed states → tighten the contract.
   - Wrong values → fix the `tokens.md` pointers or names.
4. Re-run the same task until the output passes without hand-holding.

This loop is the whole point. Once one slice passes cleanly, you have evidence the system
works and a tuned set of principles — *now* it's worth scaling.

---

## Phase 5 — Scale by traffic (first top-10 pass done)

**Goal:** cover the components that actually matter, not all of them.

1. Rank components by how often they appear in your prototype (a rough count is fine —
   table, button, input, select, dialog, drawer, toast, tabs, badge, card usually lead).
2. Write contracts for the **top ~10** from the template, reusing the Phase 3 method.
   The current first pass source-backed nine of ten; `drawer` remains a documented gap.
3. Add a golden example for each as you go; update the index in `components/README.md`.
4. Stop when you stop hitting friction. Undocumented long-tail components can wait until
   something actually goes wrong with them.

---

## Phase 6 — Wire the skills into the tools (export-supported)

**Goal:** the on-demand workflows are discoverable.

1. Export the brain into a product repo:
   ```bash
   python3 tools/export_brain.py --target /path/to/orbit-product --profile all
   ```
2. The exporter copies skills into Claude Code's location:
   ```bash
   .claude/skills/component-contract
   .claude/skills/extract-contract
   .claude/skills/write-stories
   .claude/skills/port-to-orbit
   .claude/skills/explore
   .claude/agents/design-reviewer.md   (plus the rest of design-brain/agents/)
   ```
3. Place the same skills in your Codex skills location if you want them available as
   named Codex skills outside this vault.
4. Add real port-skill reference files when available: component mapping, token
   translation, and validation checklist.

**Verify (Claude Code):** `/skills` lists all five vault skills (`component-contract`, `extract-contract`, `write-stories`, `port-to-orbit`, `explore`).

---

## Phase 7 — Project into Lovable (≈30 min)

**Goal:** Lovable produces Orbit-correct UI even though it can't read your repo.

Pick the path that matches your plan:

- **Enterprise plan (preferred):** create your design system as a dedicated Lovable
  Design System project (your React components + knowledge files), then connect it to each
  project in Project settings → Design systems. Components, tokens, and updates flow in
  automatically. This is the closest Lovable equivalent to your port skill.
- **Otherwise:** paste `design-brain/lovable/knowledge-base.md` into the project's
  Knowledge Base and `workspace-knowledge.md` into Workspace Knowledge. Export your tokens
  into it — either paste the values or, in code mode, set them in `tailwind.config` and
  tell Lovable those are the source of truth.

Start each Lovable session with: *"Before writing code, review the Knowledge Base and
summarise the Orbit constraints you'll follow."*

> Lovable is the one projection that needs re-syncing by hand when the canonical tokens
> change (unless you're on the connected Enterprise design system). Note it in your routine.

---

## Phase 8 — Make it durable (optional, ≈20 min)

**Goal:** a single, low-friction place to author and maintain the brain.

- If you want Obsidian as the authoring surface, open the `design-brain/` folder as a vault
  (it's all plain Markdown — backlinks between principles and the contracts that embody
  them, a Base view of contracts by status, all work out of the box).
- Keep the repo as the source the tools read. If you author in Obsidian elsewhere, symlink
  or sync the folder into the repo so there's one true copy — never two you edit separately.

---

## Phase 9 — The maintenance loop (forever)

The brain is living memory, not documentation:

1. When an agent gets Orbit wrong and you correct it, update the relevant canonical file.
2. Re-project: the CLI tools pick up the edit automatically; re-paste the Lovable files
   (or rely on the connected design system).
3. Review the `components/` index quarterly — promote `draft` contracts to `stable`,
   retire components that no longer exist.

---

## Quick checklist

- [x] `AGENTS.md` + `CLAUDE.md` at vault root; paths point to `design-brain/`
- [x] Obsidian folders created: `_bases`, `_canvases`, `_review`, `_exports`, `_benchmarks`
- [x] Export script created: `tools/export_brain.py`
- [ ] `tokens.md` points at real token files; validation rule added
- [x] Top 10 starter component contracts created
- [ ] Top 10 component contracts extracted from real code
- [ ] One component: source-derived contract written + golden example linked
- [ ] Brain tested against a real task and tuned until it passes
- [x] First six pattern contract shells created
- [ ] Top ~10 component contracts extracted; first two pattern contracts source-validated
      (focus-mode-results, guided-conversational-workflow)
- [x] Exporter copies skills into `.claude/skills/`
- [ ] Lovable Knowledge Base / Design System connected
- [x] One canonical Obsidian vault structure; maintenance loop documented

<!-- graph-links:start — generated by tools/gen_graph_links.py; do not hand-edit -->
## Vault graph
[[AGENTS|AGENTS]] · [[CLAUDE|CLAUDE]] · [[design-brain/anti-patterns|anti-patterns]] · [[design-brain/components/README|components README]] · [[design-brain/components/_TEMPLATE|components _TEMPLATE]] · [[design-brain/lovable/knowledge-base|knowledge-base]] · [[design-brain/lovable/workspace-knowledge|workspace-knowledge]] · [[design-brain/motion|motion]] · [[design-brain/principles|principles]] · [[design-brain/skills/extract-contract/SKILL|extract-contract SKILL]] · [[design-brain/tokens|tokens]]
<!-- graph-links:end -->
