---
type: platform-index
status: stable
owner: design-system
surfaces: [shared]
platform: shared
source: specified
last_reviewed: 2026-06-15
maturity_score: 72
tags: [orbit, design-brain, platforms]
---

# platforms/ — Platform Profiles

The Design Brain has one shared foundation and two platform profiles. Agents must choose
the platform before making screen-level design decisions.

## Platform Index

| Platform | File | Audience | Visual truth status |
| -------- | ---- | -------- | ------------------- |
| Connected Platform | `connected-platform.md` | internal Efficio users | `connected-platform-visual-truth.md`, in review |
| Orbit / Client Connected Platform | `orbit-client-connected-platform.md` | external client users | `orbit-client-connected-platform-visual-truth.md`, in review |

## Shared vs Platform-Specific

Shared:
- tokens, accessibility, motion, base components, data-viz rules, and generic component
  contracts.

Platform-specific:
- shell/navigation precedent, visual truth screenshots, copy tone, density defaults,
  RBAC messaging, page-pattern emphasis, and product examples.

## Rule

If a request does not identify the platform, ask before creating or reviewing UI. Do not
blend internal Connected Platform visual patterns into external Orbit / Client Connected
Platform screens.

Before designing or reviewing a screen, read the matching platform profile and visual
truth note:

- Connected Platform: `connected-platform.md` and
  `connected-platform-visual-truth.md`
- Orbit / Client Connected Platform: `orbit-client-connected-platform.md` and
  `orbit-client-connected-platform-visual-truth.md`
