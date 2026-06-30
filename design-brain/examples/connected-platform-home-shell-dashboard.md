---
type: example
status: in-review
owner: design-system
surfaces: [Connected Platform]
platform: connected-platform
source: user-provided
last_reviewed: 2026-06-15
maturity_score: 65
tags: [orbit, design-brain, example, visual-truth, connected-platform]
---

# Golden Example: Connected Platform Home Shell Dashboard

## Demonstrates
- Internal Connected Platform shell/navigation.
- Dashboard card density for operational users.
- Compact global navigation paired with a task-focused work surface.

## Screenshot Evidence
- Primary screenshot:
  [connected-platform-home-shell-dashboard.png](screenshots/connected-platform/connected-platform-home-shell-dashboard.png)
- Supporting reference only:
  [connected-platform-home-shell-dashboard-dock-visible.png](screenshots/connected-platform/connected-platform-home-shell-dashboard-dock-visible.png)

Screenshots are in-review and restricted until design-system owners approve
sanitization. Do not treat browser chrome, OS dock, or capture artifacts as product UI.

## Pattern Represented
Internal home/dashboard shell for Connected Platform.

Use this when creating or reviewing internal CP landing, home, or dashboard surfaces
where users need fast access to work, status, and navigation.

## Components Visible
- Persistent shell/navigation.
- Dashboard cards.
- Status/count indicators.
- Work summary regions.
- Link/action groups.

## Layout Guidance
- Keep the left navigation persistent, compact, and grouped around work areas.
- Let the main dashboard content carry the hierarchy; avoid oversized hero treatment.
- Use cards to expose operational information, not to decorate the page.
- Keep the dashboard arranged for scanning across work, actions, and status.

## Density Guidance
- Default to comfortable-enterprise density, closer to compact than client-facing Orbit.
- Preserve enough whitespace to separate regions, but avoid sparse SaaS landing-page
  spacing.
- Keep repeated cards stable in size and aligned to a clear grid.

## Copy Guidance
- Internal labels can be concise and operational.
- Prefer direct labels that name the work object, status, or action.
- Do not add client-facing explanation unless the internal workflow genuinely needs it.

## Imitate
- Persistent internal navigation rhythm.
- Compact card density.
- Work-first hierarchy.
- Status and action visibility.

## Do Not Imitate
- OS/browser chrome from the screenshot.
- Marketing hero layout.
- Generic feature cards with no operational state.
- Orbit / Client Connected Platform explanatory tone.

## Review Questions
- Which dashboard cards are approved canonical CP modules?
- Are all labels and counts safe for documentation screenshots?
- Which status/count indicators need component contracts?
