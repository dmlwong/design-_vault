# Archived vault explainers

Three hand-authored decks that each explained the vault from one angle. They were
**consolidated into a single generated page** — `artifacts/about-the-vault.html`,
built by `tools/build_about_page.py` from `tools/about-template.html` — and moved here.

| File | What it was | Its unique contribution (kept in the new page) |
| ---- | ----------- | ---------------------------------------------- |
| `systems-overview.html` | Internals deck | Agent roster + model tiers, tool-stack flow, structure |
| `one-source-of-truth.html` | Pitch deck | The AI-sameness argument, the experiment story, benchmark proof, per-audience value |
| `how-the-vault-is-shared.html` | Operations deck | Authors-vs-consumers split, travels/stays-home, onboarding |

## Why they were retired

They shared ~40% of their content (the "one brain, authored once" thesis and the
Author→Govern→Verify→Export→Build pipeline, drawn three times), and — more importantly
— they **drifted from the vault**: "eight specialist agents" (really 10), "97 documents"
(really 139), an invented "~85/100 maturity" gauge, and a CI "drift check" described as
live when it was commented out.

The replacement is a **generated projection** (like `DESIGN.md` and the health page): its
counts, agent roster, and status mix come from the vault at build time, and the generator
fails the build if a banned stale claim reappears — so this class of drift can't recur.
See `design-brain/lessons/INBOX.md` for the durable lesson.

`_archive/` is skipped by all vault linters; these files remain viewable by opening them
locally.
