---
type: agent-entrypoint
status: stable
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-06-30
maturity_score: 82
tags: [orbit, design-brain, agent-context]
---

# AGENTS.md — Orbit Design Brain

> Canonical, always-on design context for any AI coding agent working on Orbit.
> This file is the single source of truth. Claude Code imports it via `@AGENTS.md`
> in `CLAUDE.md`. Codex reads it directly. Lovable consumes the compiled projection
> in `design-brain/lovable/knowledge-base.md`. Edit here, project everywhere — never the reverse.

> Canonical home: this file lives in the shared **Orbit Design Brain** Obsidian vault.
> Product-repo copies are generated exports. Do not hand-edit exported copies.

---

## 1. Who you are building for

You are generating UI for Efficio procurement platforms:

- **Connected Platform** — internal Efficio users.
- **Orbit / Client Connected Platform** — external client users.

Surfaces include **ClauseIQ**, **MarketIQ**, **RFP Analytics**, and **RFP Builder**.
The audience is procurement and category professionals doing dense, high-stakes,
repetitive work inside long sessions.

This is **B2B enterprise software**, not a consumer app and not a marketing site.
That single fact governs almost every decision below: information density over
whitespace, scannability over delight, predictability over novelty.

## 2. Non-negotiable rules (apply to every output, every time)

1. **Tokens only.** Never hardcode a colour, spacing, radius, font size, shadow, or
   z-index value. Every visual value resolves through the token system. A hardcoded
   value is a defect, not a style choice. See `design-brain/tokens.md`.
2. **Identify the platform first.** Before designing a screen, identify whether it is
   for Connected Platform or Orbit / Client Connected Platform. Read the matching
   platform profile and visual truth note in `design-brain/platforms/`. If the platform
   is unclear, ask before creating UI.
3. **Match the right platform, not the default.** Do **not** ship the generic ShadCN / Tailwind
   default look. The model's untouched aesthetic is the single biggest quality risk.
   When unsure what the platform looks like, read current product screenshots,
   Storybook, the relevant platform profile, or a source-backed golden example before
   inventing. Benchmark screenshots are useful for behavior, state, theme, and density
   evidence, but they are not canonical platform visual precedent unless design-system
   owners mark them as such.
4. **WCAG 2.2 AA is the floor, not the goal.** Contrast, focus order, keyboard
   operability, and visible focus rings are required on every interactive element.
   See `design-brain/accessibility.md`.
5. **Density is a first-class concern.** Default to the comfortable density mode;
   support compact. Tables, lists, and forms are where Orbit lives — they must stay
   legible at high row counts. See `design-brain/principles.md`.
6. **Use the contract, not your imagination.** Before building any component that
   exists in the system, read its contract in `design-brain/components/`. If no contract exists,
   propose one using `design-brain/components/_TEMPLATE.md` before writing code.
7. **Respect state and role.** Every component must define loading, empty, error,
   and disabled states, plus any RBAC-driven variations, before it is considered done.
8. **Prototype handover inspector.** Every generated prototype must mount the Orbit
   design-spec inspector exactly once at the root: import
   `OrbitInspector` from `@efficio/orbit/inspector` and render
   `<OrbitInspector />` as the final child of the root layout after all app content,
   with no props and no conditional wrapper.
9. **Stop and ask** when a request conflicts with these rules rather than silently
   resolving the conflict.

## 3. How to load the rest of the brain (progressive disclosure)

Keep this file lean. Pull the detailed layer in only when the task needs it:

All paths are relative to the repo root.

| When the task involves…            | Read first                                        |
| ---------------------------------- | ------------------------------------------------- |
| Any screen/page design             | `design-brain/platforms/<platform>.md` (audience, personas, visual truth) |
| Any visual value                   | `design-brain/tokens.md`                          |
| Choosing spacing, padding, a button, or any default | `design-brain/defaults.md`       |
| Choosing a flow shape, IA, or interaction model | `design-brain/interaction-defaults.md` |
| Building a specific assigned feature/initiative | the linked `discovery/<initiative>.md` business pack |
| The intent / feel of a screen      | `design-brain/principles.md`                      |
| Building or editing a component    | `design-brain/components/<name>.md` (its contract)|
| A component with no contract yet   | `design-brain/components/_TEMPLATE.md`            |
| A full page / multi-component view | `design-brain/patterns/<name>.md` (page patterns) |
| Charts, KPIs, analytics views      | `design-brain/data-viz.md`                        |
| Animation, transitions, micro-int. | `design-brain/motion.md`                          |
| Any text shown to a user           | `design-brain/ux-copy.md`                         |
| Anything interactive               | `design-brain/accessibility.md`                   |
| "Why does the output look generic" | `design-brain/anti-patterns.md`                   |
| Porting a Lovable/external proto   | `design-brain/skills/port-to-orbit/SKILL.md`      |
| Writing a contract from source     | `design-brain/skills/extract-contract/SKILL.md`   |
| Reviewing finished UI work         | `design-brain/agents/design-reviewer.md`          |
| Multi-agent work / choosing a model | `design-brain/orchestration.md` (+ machine-readable `design-brain/routing.json`) |
| Recording a correction mid-task    | `design-brain/lessons/INBOX.md`                   |

## 4. Token contract (summary — full detail in `design-brain/tokens.md`)

Three tiers, two themes:

- **Tier 1 — Primitives**: raw palette/scale values in
  `packages/orbit/styles/tokens/`.
- **Tier 2 — Semantic**: real families such as `--orbit-color-text-primary`,
  `--orbit-color-border-focused`, and `--orbit-color-bg-hover`.
- **Tier 3 — Component**: component-scoped tokens such as
  `--orbit-color-btn-primary-*`, `--orbit-color-card-bg-*`,
  `--orbit-dropdown-trigger-height`, and `--orbit-tab-height`.
- **Themes**: `efficio` / Connected Platform base on `:root`; `orbit` through
  `[data-theme="orbit"]` in `themes/orbit.css`. Components must switch through token
  values, not theme-conditional component logic.

Use `npm run audit:design-system` in `the efficio-orbit repo` to catch
hardcoded visual values and other design-system rule violations.

### Default choices (when unsure)

Do not invent spacing, padding, or component choices. When the task does not specify one,
use the Orbit default. Full table in `design-brain/defaults.md`; the always-on minimum:

- Primary action: `Button` Primary, Medium — one primary per view.
- Tabular data: Orbit `Table` (never div rows); density `Default`, `Compact` for dense lists.
- Modal/drawer: `Overlay`, size `Default` (no reusable `Drawer` exists — use `Overlay`).
- Cards: type `Dynamic`, padding `Base` (`Small` for dense surfaces); never nest cards.
- Radius: `--orbit-radius-md` cards, `--orbit-radius-sm` controls, `--orbit-radius-lg` overlays.
- Density default is comfortable; support compact. The audit can't catch a
  tokenized-but-wrong choice — the default is the choice.

## 5. Definition of done for any UI work

A component or screen is done only when **all** are true:

- [ ] Zero hardcoded visual values; everything via tokens
- [ ] Used the Orbit defaults for spacing, density, and component choice — no invented values (see `design-brain/defaults.md`)
- [ ] Platform identified and matching platform profile followed
- [ ] Renders correctly in both `efficio` and `orbit` themes
- [ ] All states present: default, hover, focus, active, disabled, loading, empty, error
- [ ] Keyboard-operable with a visible focus ring; meets WCAG 2.2 AA contrast
- [ ] Benchmark routes include generated accessibility, browser visual, and
      screen-reader artifacts
- [ ] Works at comfortable **and** compact density
- [ ] Copy follows `design-brain/ux-copy.md`; motion follows `design-brain/motion.md`
- [ ] Matches the component contract (or a new contract was written first)
- [ ] Generated prototypes mount `<OrbitInspector />` exactly once at the root for
      handover inspection
- [ ] No `design-brain/anti-patterns.md` violations

## 6. Feedback loop

When you make an incorrect assumption about Orbit and the user corrects you, **update
the relevant brain file so the fix persists**, then continue. Treat this file and its
references as living memory, not static docs. Propose the edit; let the user approve.

Mid-task, if stopping to edit the brain would derail the work, append the correction to
`design-brain/lessons/INBOX.md` instead (template inside) and continue — the
vault-librarian triages entries into proposed edits weekly. Either way, the correction
must land somewhere durable before the task is called done.

## 7. Governance

Design system owners approve changes to this file, `design-brain/tokens.md`,
component contracts, pattern contracts, and tool projections. Product and design team
members may propose changes using `_review/Change Request Template.md`.
