---
type: review
status: stable
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-06-15
maturity_score: 88
tags: [orbit, design-brain, maturity]
---

# Maturity Scorecard

Use this to track progress from the current structured vault toward the 85-90 target.

| Area | Target | Current |
| ---- | ------ | ------- |
| Obsidian vault structure | Root entry points, bases, canvas, review docs | Done |
| Agent auto-load wiring | Root `AGENTS.md`, root `CLAUDE.md`, exporter | Done |
| Platform split | CP and Orbit profiles, screenshot manifests, platform metadata | Profiles and manifests added; real screenshots missing |
| Token source | Real token paths and validation command | Source-backed |
| Motion source | Real duration/easing tokens | Source-backed gap: no motion tokens found |
| Component contracts | Top 10 source-derived contracts | 9 source-backed; drawer gap documented |
| Pattern contracts | 4-6 source-validated patterns | ClauseIQ guided workflow source-backed; focus-mode, settings-form, and analytics-dashboard have benchmark evidence; others need validation |
| Golden examples | Real code/story/screen links | 6 linked to code/tests plus 4 benchmark routes; benchmark screenshot pack captured but not accepted as platform visual precedent; production MarketIQ/RFP still missing |
| Lovable projection | Current tokens and component guidance | Updated with real token and component guidance |
| Benchmarks | Five repeatable agent tasks | Tasks 1-5 passed; review loop proven |
| Accessibility artifacts | Repeatable benchmark route artifact | `npm run bench:a11y` and browser visual pass both pass all four benchmark routes; screen-reader artifact prepared and parked for human AT confirmation |
| Governance | Owner approval and review loop | Done |

## Current Estimated Score

**88/100**

The structure, operating system, real token paths, first top-10 component pass, and
ClauseIQ guided-workflow example are in place. The first five benchmarks passed
strongly, Task 2 improved the real `Input` API, Task 3 proved the analytics pattern can
prevent generic dashboard output, and Task 4 proved a real Lovable/ShadCN prototype can
be translated into Orbit components and tokens. Task 5 proved the review loop can find
and fix accessibility/state issues, then feed the lessons back into the brain. The
benchmark accessibility artifact now passes for all four benchmark routes using the
existing Vitest/jsdom stack. The browser visual pass also passes for all four routes,
with screenshot evidence, rendered CSS contrast sampling, theme/density coverage, and
real-browser focus-ring traversal. The screen-reader pass prepared the manual checklist,
fixed rendered semantic issues, and records **NEEDS HUMAN CONFIRMATION** until
VoiceOver, NVDA, or JAWS spoken output is verified. That human assistive-technology
pass is intentionally parked in `_review/Parked Items.md` so it does not block the next
build-out. The benchmark screenshot pack provides stable screenshots for all four
benchmark routes across both themes and density modes, but it has been reclassified as
benchmark evidence only because it does not match the current live platform closely
enough to be a visual source of truth. The remaining active lift is validation depth:
production Storybook or equivalent examples, drawer decision, dedicated data-viz tokens,
production product precedents, source-backed page patterns, and recurring review.

## 85-90 Exit Criteria

- Token docs point to real files and validation passes.
- Top 10 component contracts match source exactly.
- Six patterns are validated against real product precedent.
- Six golden examples link to real implementation or product screens.
- Exporter is used in at least one product repo.
- Codex, Claude Code, and Lovable benchmark tasks score 16/18 or higher with no blocker.
