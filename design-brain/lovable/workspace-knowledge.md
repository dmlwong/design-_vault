---
type: tool-projection
status: in-review
owner: design-system
surfaces: [shared]
source: code
last_reviewed: 2026-06-14
maturity_score: 68
tags: [orbit, design-brain, lovable]
---

# Lovable Workspace Knowledge (applies to all projects)

Paste into **Workspace Knowledge** so these rules apply across every Lovable project,
then keep each project's `knowledge-base.md` for project specifics.

## Standing rules
- All UI targets Orbit / Efficio standards unless a project says otherwise.
- Identify the platform before designing: Connected Platform is internal Efficio;
  Orbit / Client Connected Platform is external client-facing.
- Semantic design tokens only; never hardcode visual values.
- WCAG 2.2 AA minimum on everything interactive.
- Never ship the default ShadCN/Tailwind aesthetic — match Orbit.
- Never treat docs benchmark screenshots as current product visual truth.
- Every component implements full states (incl. loading/empty/error/disabled).
- Professional, plain microcopy; functional, reduced-motion-aware animation.
- Current Orbit source repo is `the efficio-orbit repo`.
- Use the real Orbit package components: `Table`, `Button`, `IconButton`, `Input`,
  `Dropdown`, `MultiSelectDropdown`, `Overlay`, `Toast`, `TabButton`, `PageHeader`,
  `Badge`, and `Card`.

## Reuse
- Prefer the connected Orbit **Design System** (Enterprise) as source of truth for
  components and tokens over re-generating components per project.
