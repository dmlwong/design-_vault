---
type: governance
status: in-review
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-06-24
maturity_score: 60
tags: [orbit, design-brain, usage, onboarding, codex]
---

# Using the Design Brain — Step by Step

How to actually build Orbit UI with an AI tool (Codex / Claude Code) using this brain,
together with the `efficio-orbit` design system. The visual overview is in
`_review/how-to-use-the-design-brain.html`; this is the detailed reference.

## The core principle (read this first)
There is **no plugin or integration.** An AI tool uses the brain when a file called
`AGENTS.md` is present in the folder it's working in — it reads it automatically. So
"using the brain" = **working in a folder that has the brain in it.**

- **You author** the brain in the **Obsidian vault** (this folder, on OneDrive).
- **AI tools consume** the brain in a **code repo** (`efficio-orbit`), where it's been
  exported.
- You run Codex / Claude Code **in the code repo, never in the vault.**

The brain *describes* Orbit's real components and tokens, which live in the
`@efficio/orbit` package inside `efficio-orbit`. So to build *real* Orbit UI, your project
must have that package available.

---

## Part 1 — One-time setup: get the brain INTO the codebase (the export)
*Do this once per repo, and re-run whenever the vault changes. Shared by both cases.*

1. **Open Terminal.**
2. **Dry-run first** (writes nothing — shows what would change):
   ```bash
   cd "~/Library/CloudStorage/OneDrive-Efficio/Orbit Design Brain"
   python3 tools/export_brain.py --target <path-to-efficio-orbit> --profile all --dry-run
   ```
   (`<path-to-efficio-orbit>` = your local checkout of the Orbit repo, e.g. `~/efficio-orbit`.)
3. **Run it for real** — drop `--dry-run`:
   ```bash
   python3 tools/export_brain.py --target <path-to-efficio-orbit> --profile all
   ```
4. **What it writes into the repo:** `AGENTS.md` + `CLAUDE.md` at the repo root;
   `design-brain/`, `_benchmarks/`, `_review/` under it; `.claude/skills` + the
   `design-reviewer` agent; and a `DESIGN_BRAIN_EXPORT.md` notice.
5. **Commit & push** in `efficio-orbit`, so every teammate gets the brain via `git pull`.
6. **Profiles:** `all` (Codex **and** Claude), `codex` (AGENTS.md + reference layer only),
   `claude` (adds CLAUDE.md + `.claude/`), `lovable` (just the projections).

> Re-export after any vault change — that's the maintenance loop (`_review/Maintenance
> Workflow.md`). Never hand-edit the exported copies; edit the vault and re-export.

---

## Part 2 — Case A: a new feature/screen in Orbit (the common case)
*You're adding to the existing Orbit codebase. No new repo.*

1. **Open `efficio-orbit` in your AI tool.**
   - Codex: run `codex` from inside the `efficio-orbit` folder in Terminal.
   - Claude Code: open the `efficio-orbit` folder.
2. **Confirm it loaded the brain.** Codex reads `AGENTS.md` automatically; Claude Code
   reads `CLAUDE.md` (which imports `AGENTS.md`). Sanity-check by asking:
   *"Before writing code, summarise the Orbit constraints you'll follow."* It should
   mention tokens-only, platform-first, the Definition of Done.
3. **Give it the task — and name the platform.** e.g. *"Build a Connected Platform
   workspace card for X."* If it's an assigned sprint feature, point it at the discovery
   pack: *"…following `discovery/<initiative>.md`."*
4. **Let it build to spec.** It reads the relevant `design-brain/` files (the routing table
   in `AGENTS.md §3` tells it which: the platform profile, `defaults.md`, the component /
   pattern contract). Tokens only, real Orbit components, the defaults, the pattern
   composition.
5. **Validate.** Check against the Definition of Done (`AGENTS.md §5`): all states, both
   themes, both densities, WCAG 2.2 AA, copy, motion, no anti-patterns. For a thorough
   pass, ask it to run the `design-reviewer` — *a blocker means not done.*
6. **Feed back.** If it gets Orbit wrong and you correct it, fix the **vault** file (in
   Obsidian) — not just the output, and not the exported copy — then **re-export** (Part 1).

---

## Part 3 — Case B: a brand-new, separate repo/app

1. **Create or clone the new repo.**
2. **Make Orbit available in it.** The brain references `@efficio/orbit`, so the project
   needs that package to build real Orbit UI:
   - install it (`npm install @efficio/orbit`) if it's published to a registry the team
     can reach, **or**
   - add it as a workspace / linked dependency from your `efficio-orbit` checkout.
   - *If Orbit isn't installable yet, the brain still guides structure/behaviour, but the
     component imports won't resolve — flag this to the design-system owner.*
3. **Export the brain into the new repo:**
   ```bash
   cd "~/Library/CloudStorage/OneDrive-Efficio/Orbit Design Brain"
   python3 tools/export_brain.py --target /path/to/new-repo --profile all
   ```
4. **Commit it** in the new repo.
5. **Open Codex / Claude in the new repo.** It auto-loads `AGENTS.md` → same usage as
   Case A, steps 2–5.
6. **Feed back to the VAULT, not the new repo's copy.** Corrections always go to the
   canonical vault, then re-export to **every** repo that uses the brain.

> You can put the brain in as many repos as you like — each is just another `--target`.

---

## Part 4 — Rules & gotchas (don't skip)
- **Edit the vault, never the exported copies.** The repo copies are generated; hand-edits
  get overwritten on the next export and cause drift.
- **Re-export after vault changes** — to *each* repo that uses the brain. (Automating this
  with a CI drift-check is on the roadmap — `_review/Maintenance Workflow.md`.)
- **Run AI tools in the repo, not the vault.** The vault is Obsidian-only.
- **The brain needs `@efficio/orbit`** to build real UI; without it you get guidance with
  nothing to import.
- **Verify the brain loaded** before trusting output — ask the AI to summarise the Orbit
  constraints. If it doesn't mention them, `AGENTS.md` isn't being read (wrong folder, or
  not exported).
- **Lovable is separate** — it can't read the repo; paste `design-brain/lovable/` into its
  knowledge base, or connect the Enterprise design system.

---

## Part 5 — Quick reference

```bash
# Export the brain into a repo (run from the vault)
cd "~/Library/CloudStorage/OneDrive-Efficio/Orbit Design Brain"
python3 tools/export_brain.py --target <repo> --profile all --dry-run   # preview
python3 tools/export_brain.py --target <repo> --profile all             # apply

# Then, in the repo:
git add -A && git commit -m "Update Orbit Design Brain export"          # share via git
codex            # or open the repo in Claude Code — it auto-loads AGENTS.md
```

| Where | What |
| ----- | ---- |
| Vault (OneDrive, Obsidian) | author the brain — the single source of truth |
| `efficio-orbit` (git) | build Orbit UI; the brain is exported here |
| A new repo | export the brain into it too (`--target`) + install `@efficio/orbit` |
| Lovable | paste `design-brain/lovable/` projections |
