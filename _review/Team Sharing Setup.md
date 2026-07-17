---
type: governance
status: in-review
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-07-06
maturity_score: 70
tags: [orbit, design-brain, sharing, onboarding, governance]
---

# Team Sharing Setup & Onboarding

The live guide for sharing this vault across teams and getting a new person (or a new
consuming repo) productive. Supersedes the archived Obsidian-Sync-only draft in
`_archive/usage-guides-2026-06/Team Sharing Setup.md`.

## How the vault is shared today

**The git repository is the canonical distribution** — `github.com/dmlwong/design-_vault`
(see `_review/STATE.md`). Obsidian is the authoring UI on top of a local checkout; git is
how changes travel, get reviewed, and pass CI (`.github/workflows/vault-integrity.yml`
runs the link checker and export self-check on every push/PR).

Two roles, two paths:

| Role | Gets the brain via | Edits? |
| ---- | ------------------ | ------ |
| **Authors** (design / product / PO) | clone of this repo, opened as an Obsidian vault | yes — in the vault, per governance |
| **Consumers** (engineers, Codex, Claude Code, Lovable) | the generated export inside their product repo | never — exported copies are read-only |

> **Open decision (owner):** whether to also offer **Obsidian Sync** for authors who
> won't touch git. It needs a paid Sync plan and an owner-managed invite list, and it
> bypasses PR review — if adopted, keep git as canonical and treat Sync as a
> convenience mirror. Until decided, authors use git.

## Onboarding a new author (≈30 minutes)

1. **Get access** — ask a design-system owner for access to the repo, then clone it.
2. **Open it in Obsidian** — "Open folder as vault" on the checkout. Personal session
   state (`.obsidian/workspace.json`) is gitignored; shared config is tracked — don't
   force-add personal state. Obsidian's graph view works via the generated "Vault
   graph" footer in each note (`tools/gen_graph_links.py`); the back-ticked paths in
   the body are the canonical references and stay as they are.
3. **Read, in order:**
   - `README.md` — what the vault is, structure, team workflow.
   - `AGENTS.md` — the 9 non-negotiable rules, the routing table (§3), Definition of Done (§5).
   - `_review/STATE.md` — where things stand right now (the single state narrative).
   - Then on demand via the routing table: `design-brain/tokens.md`, `defaults.md`,
     `interaction-defaults.md`, your platform's profile in `design-brain/platforms/`.
4. **Know the edit rules:**
   - Low-risk notes: edit directly, commit with a clear message.
   - **Governed files** (tokens, component/pattern contracts, `defaults.md`, `AGENTS.md`,
     tool projections): propose via `_review/Change Request Template.md`; a design-system
     owner approves (`_review/Governance.md`).
   - Frontmatter matters: keep `status`, `last_reviewed`, and `owner` honest when you edit.
5. **The one rule:** edit the **vault**, never an exported product-repo copy. If an AI
   tool gets Orbit wrong, fix the vault file so the correction persists (`AGENTS.md` §6).

## Onboarding a consuming team / product repo

1. **Export the brain into the repo** (run from the vault checkout):
   ```bash
   python3 tools/export_brain.py --target <path-to-repo> --profile all --dry-run   # preview
   python3 tools/export_brain.py --target <path-to-repo> --profile all             # apply
   ```
   Profiles: `all` (Codex + Claude), `codex`, `claude`, `lovable`. Details in
   `_exports/README.md`.
2. **Restricted content stays home by default** — platform screenshots and private
   `_review` WIP files are excluded from export. `--include-restricted` re-enables them
   only after the sanitization decision is approved (audit finding A3).
3. **Commit the export** in the product repo so teammates get it via `git pull`. Never
   hand-edit it — it carries a generated-export notice and is overwritten on re-export.
4. **Wire the drift-check into the product repo's CI**:
   `python3 tools/export_brain.py --target . --profile all --check` exits `1` when the
   copy differs from the vault. (Not yet wired for `efficio-orbit` — see
   `_review/Maintenance Workflow.md`, automation status.)
5. **Verify the brain loaded** — in the product repo, ask the AI tool:
   *"Before writing code, summarise the Orbit constraints you'll follow."* It should
   name tokens-only, platform-first, and the Definition of Done. If not, `AGENTS.md`
   isn't being read (wrong folder, or export missing).
6. **Lovable is the exception** — it can't read repos; paste the
   `design-brain/lovable/` projections into its knowledge base and re-sync after brain
   changes.

## Keeping it in sync

The change loop, cadence, and drift-prevention mechanics live in
`_review/Maintenance Workflow.md` — this doc doesn't duplicate them. Short version:
authors edit the vault → owners approve governed changes → re-export to every consuming
repo → CI catches drift.

## Related

- `_review/STATE.md` — current state; where the vault lives.
- `_review/Maintenance Workflow.md` — the sync/maintenance loop.
- `_review/Governance.md` + `_review/Change Request Template.md` — who approves what, how.
- `_exports/README.md` — exporter flags (check / self-check / include-restricted).
- `_archive/usage-guides-2026-06/Using the Design Brain — Step by Step.md` — the fuller
  archived walkthrough (case A/B build flows); paths in it are pre-git and stale.

<!-- graph-links:start — generated by tools/gen_graph_links.py; do not hand-edit -->
## Vault graph
[[AGENTS|AGENTS]] · [[README|design-_vault README]] · [[_archive/usage-guides-2026-06/Team Sharing Setup|Team Sharing Setup]] · [[_exports/README|_exports README]] · [[_review/Change Request Template|Change Request Template]] · [[_review/Governance|Governance]] · [[_review/Maintenance Workflow|Maintenance Workflow]] · [[_review/STATE|STATE]] · [[design-brain/defaults|defaults]] · [[design-brain/interaction-defaults|interaction-defaults]] · [[design-brain/tokens|tokens]]
<!-- graph-links:end -->
