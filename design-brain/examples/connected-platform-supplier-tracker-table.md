---
type: example
status: in-review
owner: design-system
surfaces: [Connected Platform]
platform: connected-platform
source: user-provided
last_reviewed: 2026-06-15
maturity_score: 65
tags: [orbit, design-brain, example, visual-truth, connected-platform, supplier, table]
---

# Golden Example: Connected Platform Supplier Tracker Table

## Demonstrates
- Internal supplier tracker table.
- Procurement metadata density.
- Pagination and supplier shortlist tracking.

## Screenshot Evidence
- Primary screenshot:
  [connected-platform-supplier-tracker-table.png](screenshots/connected-platform/connected-platform-supplier-tracker-table.png)
- Related discovery-card screenshot:
  [connected-platform-supplier-discovery-cards.png](screenshots/connected-platform/connected-platform-supplier-discovery-cards.png)

Screenshots are in-review and restricted until design-system owners approve
sanitization.

## Pattern Represented
Internal supplier tracker table with adjacent discovery/card precedent.

Use this when creating or reviewing supplier lists, supplier trackers, shortlist views,
or procurement research tables for internal CP users.

## Components Visible
- Table/list.
- Pagination.
- Supplier metadata columns.
- Status/shortlist indicators.
- Search and filter controls.
- Discovery cards in the related screen.

## Layout Guidance
- Use tables for supplier tracking when the user needs comparison across columns.
- Keep supplier identity, category, location, status, and action data aligned for
  scanning.
- Pair discovery cards with tracker tables only when the workflow genuinely moves from
  exploration to tracked supplier list.
- Keep pagination and table controls close to the table.

## Density Guidance
- Supplier tables should support compact density and high row counts.
- Discovery cards may be richer, but should still expose evidence and action quickly.
- Avoid oversized supplier cards when comparison is the main task.

## Copy Guidance
- Internal supplier labels can be concise.
- Actions should state the destination or effect, such as adding to a tracker or
  updating shortlist state.
- Avoid client-facing reassurance copy unless the surface is actually external Orbit.

## Imitate
- Column-based supplier comparison.
- Tracker state visibility.
- Search/filter proximity.
- Pagination for long supplier datasets.

## Do Not Imitate
- Converting supplier comparison into decorative cards.
- Hiding shortlist/tracker state.
- Replacing supplier metadata with vague summaries.
- Color-only status treatment.

## Review Questions
- Which supplier metadata fields are canonical?
- Should supplier discovery cards have their own component contract?
- Which states are still missing: empty tracker, no search results, restricted supplier?
