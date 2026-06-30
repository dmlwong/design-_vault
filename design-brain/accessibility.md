---
type: foundation
status: stable
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-06-15
maturity_score: 88
tags: [orbit, design-brain, accessibility]
---

# accessibility.md — WCAG 2.2 AA baseline

AA is the floor for every interactive element. This file is the shared a11y contract;
each component contract references the slices it touches.

## Always
- **Contrast:** text and meaningful UI meet WCAG 2.2 AA (4.5:1 body, 3:1 large text and
  non-text UI). Verify in both themes.
- **Keyboard:** every interactive element is reachable and operable by keyboard with a
  logical tab order. No keyboard traps.
- **Focus visible:** a clear focus indicator using the `focus-ring` token. Never remove
  the outline without an equivalent.
- **Semantics:** prefer native elements; add ARIA only to fill gaps, correctly.
- **Labels:** all controls have accessible names; icon-only controls have `aria-label`.
- **Not colour alone:** pair colour with text or icon for status/intent.
- **Targets:** interactive targets meet minimum size guidance, especially in compact density.

## Patterns to get right
- Forms: programmatic label association, inline errors linked via `aria-describedby`,
  error summary on submit.
- Dialogs/drawers: focus trap while open, return focus on close, `Esc` to dismiss.
- Tables/grids: header associations; manage focus for sortable/selectable rows.
  Repeated row-local actions need row identity in their accessible names.
- Compact abbreviations: initials, badges, and shorthand values need full text in the
  same cell or region; do not rely on `aria-label` on static generic wrappers.
- Loading previews: skeletons should mirror final layout shape, active density, and
  current columns so the state does not change scanning context. Keep skeleton tables
  and charts out of live-region text; announce concise loading status separately.
- Live regions: announce async results (loaded, saved, error) politely.

## Reduced motion
Honour `prefers-reduced-motion`; see `motion.md`.

## Check before done
- [ ] Keyboard-only pass completes the task
- [ ] Visible focus on every stop
- [ ] AA contrast in `efficio` and `orbit`
- [ ] Status conveyed without relying on colour
- [ ] Benchmark routes have a generated artifact from `npm run bench:a11y`
- [ ] Benchmark routes have a browser visual artifact with screenshots, focus-ring
      evidence, rendered contrast samples, and theme/density coverage
- [ ] Benchmark routes have a separate screen-reader artifact with PASS/FAIL/NEEDS
      HUMAN CONFIRMATION

## Benchmark Artifact
Benchmark routes must include three distinct accessibility artifacts under
`design-brain/_benchmarks/results/`:

1. Generated semantic artifact from `npm run bench:a11y`.
2. Browser visual artifact with screenshots, rendered contrast samples, real-browser
   focus-ring evidence, theme/density coverage, and fixes made.
3. Screen-reader artifact with PASS/FAIL/NEEDS HUMAN CONFIRMATION, assistive
   technology used, spoken-output checklist, issues found, and human-only checks
   remaining.

The generated artifact uses the existing Vitest, Testing Library, jsdom, and
`dom-accessibility-api` stack to check landmarks, duplicate IDs, broken ARIA references,
accessible names, role values, hidden focus traps, and sequential Tab reachability.

Generated and browser visual artifacts do not replace screen-reader testing. Do not mark
the screen-reader artifact PASS unless VoiceOver, NVDA, JAWS, or another agreed
assistive technology was actually used to confirm announcements, timing, dialog context,
tab context, table navigation, and live-region quality. If only DOM/accessibility-tree
evidence is available, mark the screen-reader result **NEEDS HUMAN CONFIRMATION**.
