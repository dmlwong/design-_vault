---
type: foundation
status: draft
owner: design-system
surfaces: [shared]
source: code
last_reviewed: 2026-06-14
maturity_score: 55
tags: [orbit, design-brain, motion, gap]
---

# motion.md — Interaction & Motion Rules

Motion in Orbit is functional: it explains state change and guides attention. It is never
decoration that slows the user down.

## Source Status

The coded design system currently has **no dedicated motion token file** and no
`motion-*` / `ease-*` CSS custom property family.

Observed source patterns in `packages/orbit/src`:

- Common hover/focus transitions use `0.15s ease`.
- Card, ToggleCard, Dropzone, and Toggle use `0.2s ease`.
- Toast uses `toastSlideIn 0.3s ease`.
- Spinner uses `orbitSpin 1s linear infinite`.
- No reusable `prefers-reduced-motion` rule was found in the component CSS scan.

## Rules Until Motion Tokens Exist

- Do not introduce new decorative animation.
- Prefer existing source behavior for maintenance work.
- For new reusable components, ask design-system owners to add motion tokens before
  introducing new duration/easing values.
- Respect `prefers-reduced-motion` when adding any new movement.
- Loading states should prefer skeletons or inline progress that preserve layout.

## Recommended Token Gap

Add these to the coded design system before marking this file stable:

- `--orbit-motion-fast`
- `--orbit-motion-base`
- `--orbit-motion-slow`
- `--orbit-ease-standard`
- `--orbit-ease-emphasized`
- `--orbit-ease-exit`

## Defaults By Interaction

- Hover/press feedback: current source convention is short and quiet.
- Enter/exit of surfaces: current Toast uses a short slide/fade, but needs
  reduced-motion handling.
- Layout/expand: use restraint and avoid reflow jank.
- Loading: no spinner-only screen when final-layout skeletons are possible.

## Don't

- No looping/idle animation on functional UI except explicit loading indicators.
- No animation that delays the user seeing or acting on procurement data.
- No re-running entrance animations on every re-render.
