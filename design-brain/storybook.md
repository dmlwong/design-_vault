---
type: tooling-guide
status: draft
owner: design-system
surfaces: [shared]
source: code
last_reviewed: 2026-07-28
maturity_score: 0
context_tier: reference
load_when: [extract-contract, build-component]
tags: [orbit, design-brain, storybook, tooling]
---

# Storybook — how Orbit uses it

Storybook is the component workbench for `packages/orbit`. It renders every component in
isolation, against the real token stylesheet, in both themes.

The vault has referenced Storybook as an assumed input for a long time — "read current
product screenshots, Storybook, the platform profile" (`AGENTS.md` §2.3), "its Storybook
stories, if any" (`skills/extract-contract/SKILL.md`) — without ever saying what it is,
where it lives, or what a usable story looks like. This file closes that gap.

## Why the vault cares

Storybook is **upstream of `extract-contract`**. The `contract-extractor` agent reads
source *and* stories to draft a component contract; stories are where variants, sizes,
and states are already enumerated as running code.

The consequence is direct:

> A component with no stories gets a contract assembled from prop types and guesswork.
> A component with complete stories gets a contract extracted from observed behaviour.

Both produce a document. Only one of them is true. This is the same drift the vault
exists to prevent — so treat "does this component have stories?" as a precondition of
contract work, not a nice-to-have.

It also carries the second half of the Definition of Done that is hardest to check by
reading code: **"renders correctly in both `efficio` and `orbit` themes"**. The Theme
toolbar makes that a two-click check per story.

## Where it lives and how to run it

Config sits beside the component source, in the Orbit package:

- `packages/orbit/.storybook/main.ts` — framework and story discovery
- `packages/orbit/.storybook/preview.tsx` — global styles, theme toolbar, a11y panel
  (referred to below as *the preview file*)

Stories live next to the components they document, as
`packages/orbit/src/**/*.stories.tsx`.

Run from the design-system repo root:

| Command | What it does |
| ------- | ------------ |
| `npm run dev:storybook` | Dev server on port 6006, no auto-open |
| `npm run build:storybook` | Static build — use this in CI to prove stories still compile |

Both are root-level workspace scripts that delegate to `@efficio/orbit`.

Two addons are enabled and both matter here:

- **`@storybook/addon-essentials`** — controls, actions, viewport, docs. `tags: ['autodocs']`
  on a story's `meta` generates a docs page from the TypeScript types and JSDoc comments.
- **`@storybook/addon-a11y`** — runs axe against the rendered story and reports violations
  in a panel. It is a floor check, not a substitute for the accessibility contract in
  `design-brain/accessibility.md`; it cannot see focus order, keyboard operability, or
  whether a label is *meaningful*.

The preview file imports the package's full stylesheet — `packages/orbit/styles.css`, the same
entry a consuming app gets as `@efficio/orbit/styles.css` — so stories resolve real
tokens exactly as a consuming app does. A story that looks right in Storybook is looking at
the same cascade the product sees — which is why a hardcoded value shows up here as a value
that doesn't move when you flip themes.

## The Theme toolbar

Orbit ships two themes **through tokens, not component logic** (see `design-brain/tokens.md`):
the Efficio / Connected Platform base lives on `:root`, and the Orbit / Client theme lives
under `[data-theme="orbit"]`.

The **Theme** control in the top toolbar sets or removes `data-theme="orbit"` on the root
element. That is the whole mechanism — the same one the token layer uses in production.
Nothing about the component changes.

This gives you a cheap, direct test of rule 4 of the token contract: if a component needs
theme-conditional *logic* to look right, flipping the toolbar will expose it, because the
attribute is all that changed.

For a side-by-side comparison in a single frame, wrap a subtree in `data-theme="orbit"`
inside the story's `render` — see the `Themes` story in
`packages/orbit/src/actions/Button.stories.tsx`.

## How to write an extractable story

A story set written for a human demo and a story set written for contract extraction are
different documents. Orbit wants the second.

**Enumerate the surface, don't demo the happy path.**

1. **One story per variant.** Every value of `variant`, named as the story. If the contract
   says five variants exist, there are five stories.
2. **One story per size / density.** Including the compact case — Orbit lives in dense
   tables and forms.
3. **Every state.** `disabled`, `loading`, `error`, `empty`, and any state prop the
   component takes. A state with no story is a state nobody has verified.
4. **Every slot.** Leading icon, trailing icon, icon-only, long label, no label. Slots are
   where layout breaks.
5. **Name stories in the contract's vocabulary.** `Secondary`, not `Story2`. The extractor
   maps story names onto contract sections; matching names make that lossless, mismatched
   names make it a guess.
6. **Keep one all-variants story.** A single frame showing the intent hierarchy side by
   side. This is what visual diffing and design review actually look at, and it catches
   "each variant is fine alone but the hierarchy is wrong" — which per-variant stories
   structurally cannot.
7. **Write the JSDoc.** Comments above `meta` and each story become the autodocs page. One
   sentence stating *when to reach for this variant* is worth more than a paragraph
   describing what it looks like.

`packages/orbit/src/actions/Button.stories.tsx` is the reference implementation of all
seven. Read it before writing a new story file.

**Set `argTypes` explicitly.** Constraining `variant` to a `select` of the real options and
disabling controls for `ReactNode` slots keeps the controls panel honest — an unconstrained
control invites a reviewer to produce a state the component does not actually support.

## What `extract-contract` does with them

The skill's rule is **derive, don't transcribe**. Running against a component it will:

- read the source for the public API, then read the stories for the variants and states
  those props are actually exercised in;
- mark anything present in code or story as `from source`;
- mark anything the contract *prescribes* but the code does not do as `specified`;
- end with a gap report, ordered by severity.

The hard rule is worth restating because stories are what make it enforceable: **no
invented behaviour.** Anything not observed in code or stated by the user is marked
`specified` — never passed off as existing. Complete stories are how "observed" gets to be
a large set. Full workflow in `design-brain/skills/extract-contract/SKILL.md`.

## Known constraints

**Storybook 8 caps Vite at major 6.** `vite ^6` is pinned in the root `devDependencies`
alongside `storybook ^8.6`. Bumping Vite to 7 without moving Storybook first will fail to
install.

**Do not resolve install conflicts with `legacy-peer-deps`.** This is worth spelling out
because it looked like it worked:

> Setting `legacy-peer-deps=true` in `.npmrc` to clear a Storybook peer conflict disables
> automatic peer-dependency installation **for the entire repo**. It silently dropped
> `@testing-library/dom` — a transitive peer of `@testing-library/react` — and every one of
> the 33 test files failed to import, so **0 tests ran**. Storybook itself still built
> cleanly, and the Storybook work was genuinely fine; only the test suite was destroyed,
> and only a full `test:components` run revealed it.

The correct fix is to **declare the missing peer explicitly** in `devDependencies` and leave
npm's peer resolution on. If a conflict genuinely cannot be resolved, narrow it with an
`overrides` entry for the one offending package rather than changing repo-wide install
behaviour.

The general lesson, which is not specific to npm: a flag that makes an error message go away
is not the same as a flag that fixes the problem, and a green build of the thing you were
working on does not tell you about the thing you weren't.

**Coverage is partial.** `Button` has a full story set. Most Orbit components do not yet have
stories — see `_review/Source Inventory.md` for what is source-backed today. Until a
component has stories, its contract's variant and state sections rest on source reading
alone, and the gap report should say so.

## Related

- `design-brain/skills/extract-contract/SKILL.md` — the flow that consumes stories
- `design-brain/agents/contract-extractor.md` — the agent that runs it
- `design-brain/tokens.md` — the theme mechanism the toolbar exercises
- `design-brain/accessibility.md` — what the a11y addon does *not* cover
- `design-brain/components/_TEMPLATE.md` — the contract shape stories feed

<!-- graph-links:start — generated by tools/gen_graph_links.py; do not hand-edit -->
## Vault graph
[[AGENTS|AGENTS]] · [[_review/Source Inventory|Source Inventory]] · [[design-brain/accessibility|accessibility]] · [[design-brain/agents/contract-extractor|contract-extractor]] · [[design-brain/components/_TEMPLATE|components _TEMPLATE]] · [[design-brain/skills/extract-contract/SKILL|extract-contract SKILL]] · [[design-brain/tokens|tokens]]
<!-- graph-links:end -->
