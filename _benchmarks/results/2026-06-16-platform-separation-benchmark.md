---
type: benchmark-result
status: in-review
owner: design-system
surfaces: [Connected Platform, Orbit, Client Connected Platform, MarketIQ, docs]
source: code
last_reviewed: 2026-06-16
maturity_score: 86
tags: [orbit, design-brain, benchmark, platform-separation]
---

# Benchmark Result: Platform Separation

## Task
Build two small docs benchmark screens using the exported Orbit Design Brain:

1. Connected Platform internal initiative list/detail screen.
2. Orbit / Client Connected Platform client-facing MarketIQ guided workflow screen.

## Product Repo
`the efficio-orbit repo`

## Required References Read

Connected Platform:
- `design-brain/platforms/connected-platform.md`
- `design-brain/platforms/connected-platform-visual-truth.md`
- `design-brain/examples/connected-platform-initiative-list-table.md`
- `design-brain/examples/connected-platform-home-shell-dashboard.md`
- `design-brain/patterns/list-detail.md`

Orbit / Client Connected Platform:
- `design-brain/platforms/orbit-client-connected-platform.md`
- `design-brain/platforms/orbit-client-connected-platform-visual-truth.md`
- `design-brain/examples/orbit-client-marketiq-guided-workflow.md`
- `design-brain/examples/orbit-client-marketiq-research-output-next-actions.md`
- `design-brain/patterns/guided-conversational-workflow.md`

Shared foundations and contracts:
- `design-brain/tokens.md`
- `design-brain/principles.md`
- `design-brain/accessibility.md`
- `design-brain/ux-copy.md`
- `design-brain/motion.md`
- `design-brain/anti-patterns.md`
- `design-brain/components/data-table.md`
- `design-brain/components/card-panel.md`
- `design-brain/components/button.md`
- `design-brain/components/badge-status.md`
- `design-brain/components/tabs.md`
- `design-brain/components/input.md`
- `design-brain/components/select-combobox.md`
- `design-brain/components/dialog.md`

## Implementation
- Connected route:
  `apps/docs/app/design-system/benchmarks/platform-separation/connected-platform/page.tsx`
- Connected component:
  `apps/docs/app/design-system/benchmarks/platform-separation/connected-platform/ConnectedPlatformSeparationBenchmark.tsx`
- Connected styles:
  `apps/docs/app/design-system/benchmarks/platform-separation/connected-platform/ConnectedPlatformSeparationBenchmark.module.css`
- Orbit route:
  `apps/docs/app/design-system/benchmarks/platform-separation/orbit-marketiq/page.tsx`
- Orbit component:
  `apps/docs/app/design-system/benchmarks/platform-separation/orbit-marketiq/OrbitMarketIQSeparationBenchmark.tsx`
- Orbit styles:
  `apps/docs/app/design-system/benchmarks/platform-separation/orbit-marketiq/OrbitMarketIQSeparationBenchmark.module.css`
- Docs index:
  `apps/docs/app/design-system/page.tsx`
- Automated accessibility route list:
  `test/benchmarks/accessibility-artifact.test.tsx`

## Connected Platform Score
Reported score: **18/18 - PASS**.

| Category | Score | Notes |
| -------- | ----- | ----- |
| Tokens only | 2 | New route styles use Orbit semantic/component tokens for color, spacing, type, border, radius, and sizing. Targeted raw visual-value scan found no `hex`, `rgb`, or `px` literals in the new platform-separation files. |
| Theme support | 2 | Uses token-backed CP semantic families and no theme-conditional logic; the screen remains token-driven when rendered in the docs shell. |
| Full states | 2 | Includes data, loading, empty filter result, sync error, permission-limited/no-access, disabled actions, and selected-detail states. |
| Accessibility | 2 | Generated artifact PASS: 34/34 keyboard stops, 35 named elements, 1 named table, 0 violations. Browser check confirmed focus-ring token on an active button sample. |
| Density | 2 | Comfortable and compact density controls are present; compact switches the Orbit `Table` to `density="Compact"`. Layout was patched to avoid page-level overflow while preserving table scrolling. |
| Contract match | 2 | Uses contracted `Table`, `Card`, `Button`, `Badge`, `Searchbox`, and `Dropdown`; loading/error/permission wrappers stay at page layer. |
| Pattern match | 2 | Matches `list-detail`: dense internal queue, filters/search, stable row identity, selected detail panel, owner/status/next action proximity, and recoverable actions. |
| Copy and motion | 2 | Internal operational labels are concise and action-led; no decorative motion was added. |
| Orbit feel | 2 | Correctly separates CP as internal, denser, operational, and metadata-rich rather than client-guided or promotional. |

Total: `18/18`

## Orbit / Client Connected Platform Score
Reported score: **18/18 - PASS**.

| Category | Score | Notes |
| -------- | ----- | ----- |
| Tokens only | 2 | New route styles use Orbit tokens only for visual styling; no hardcoded color, spacing, radius, or font-size literals were found in the platform-separation scan. |
| Theme support | 2 | Route root sets `data-theme="orbit"` for the client-facing benchmark and uses theme tokens rather than component logic. |
| Full states | 2 | Includes ready, generating, results, partial-data warning, permission-limited review, disabled generation, empty picker result, and modal selection states. |
| Accessibility | 2 | Generated artifact PASS: 16/16 keyboard stops, 16 named elements, 0 violations. Overlay uses `aria-labelledby`, focus trap/restoration from `Overlay`, and generated state uses a polite status region. |
| Density | 2 | Guided cards are compact but readable; picker table uses `density="Compact"` and keeps client initiative comparison focused. |
| Contract match | 2 | Uses contracted `PageHeader`, `Card`, `Button`, `Badge`, `Dropdown`, `Searchbox`, `Table`, and `Overlay` APIs. |
| Pattern match | 2 | Matches `guided-conversational-workflow`: selected context persists, parameters remain visible, generation state is honest, results stay traceable, and next actions are concrete. |
| Copy and motion | 2 | Client-safe copy explains state and recovery without internal shorthand or AI hype; no decorative animation added. |
| Orbit feel | 2 | Correctly separates Orbit as guided, polished, client-safe, and review-oriented while preserving enterprise density. |

Total: `18/18`

## Verification
- `npx tsc -p apps/docs/tsconfig.json --noEmit` passed.
- `npm run audit:design-system` passed with 27 checks.
- `npm run build:docs` passed and prerendered both new routes.
- `npm run bench:a11y -- --artifact design-brain/_benchmarks/results/2026-06-16-platform-separation-accessibility-artifact.md` passed with all 6 benchmark routes passing.
- Browser check used the production docs server at `http://127.0.0.1:3002` because the existing port-3000 server was stale and Next dev blocked `127.0.0.1` dev chunks.
- Connected browser checks: route title/H1 present, one main landmark, internal navigation present, table named `Connected Platform internal initiative list`, 6 data rows, compact density control hydrated, document-level horizontal overflow false after layout patch.
- Orbit browser checks: route title/H1 present, one main landmark, root `data-theme="orbit"`, selected initiative pill visible, next-actions section present, no document overflow, initiative picker dialog opened with table named `Client initiative picker`, generating state displayed a live status region.
- Browser focus sample: active button exposed a solid `2px` focus outline using the focus-ring color token.

## Accessibility Artifact
Generated artifact:
`design-brain/_benchmarks/results/2026-06-16-platform-separation-accessibility-artifact.md`

Artifact route results:
- `/design-system/benchmarks/platform-separation/connected-platform`: PASS, 34/34 keyboard stops, 0 violations.
- `/design-system/benchmarks/platform-separation/orbit-marketiq`: PASS, 16/16 keyboard stops, 0 violations.

Screen-reader artifact status: **NEEDS HUMAN CONFIRMATION**. No VoiceOver, NVDA, JAWS, or other assistive technology pass was performed in this implementation turn.

## Platform Separation Findings
- Connected Platform keeps internal controls, owner/workstream metadata, bulk import/export actions, exception scanning, and operational notes close to the table/detail workflow.
- Orbit / Client Connected Platform avoids CP shorthand and instead keeps selected initiative context, MarketIQ parameters, generated evidence, and client-safe follow-on actions visible.
- The two screens share Orbit primitives and tokens, but differ in density, copy, shell treatment, and workflow emphasis.

## Residual Risk
- Browser checks were structural and interaction-focused, not a formal rendered contrast audit.
- Screen-reader quality remains human-confirmation work.
- Source screenshots and visual truth notes are still in-review/restricted, so these benchmark screens should not be treated as canonical production visual precedent.
