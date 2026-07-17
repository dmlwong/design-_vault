---
type: discovery-pack
status: draft            # draft → active → shipped → archived
owner: Product Owner / Concept Lead
platform: both
initiative: Research Agent in Initiatives — unify CP + Orbit research generation
epic: https://efficio.atlassian.net/browse/CP-9877
ai_designs: https://whirl-vast-00262476.figma.site/
sprint: 2026-01-18
surfaces: [Research Agent, MarketIQ]
source: product
last_reviewed: 2026-06-17
linked_patterns: [list-detail, review-and-approve-workflow, guided-conversational-workflow]
linked_components: [card-panel, button, dialog, badge-status, data-table]
tags: [orbit, discovery]
---

# Discovery: Research Agent in Initiatives — unify CP + Orbit research generation

> Distilled from the 4D Concept Discovery Pack (`2026-01-18_Research Agent in
> initiatives_1. Discover.docx`). Word doc remains the human source of truth. Stakeholder
> table, recommended-tools, and disclaimer dropped.

## Design surface — read first
- **Platform(s):** CP **and** Orbit. CP-led; delivered as a single internal change once
  Orbit has adopted the Research Agent — **no standalone client-facing release**.
- **Front-end in scope:** CP workspace research card (re-run option, timestamps, who-ran,
  remove summarised text, remove GPT name, 250-char limit); Orbit Key Tool Coverage Card
  states; usage tracking in Orbit initiative overview; cross-platform visibility/log with a
  CP-vs-Orbit distinction; share (Orbit→CP).
- **Out of UI scope:** research chatbot in CP; history tracking + history UI in Orbit.
- **States to design:** Key Tool Coverage Card = **2 states only — Completed and Running**
  (auto-triggered, so no incomplete state). Empty: no category selected → no pack created.

## Reference designs & visual truth
- **AI designs / prototype:** https://whirl-vast-00262476.figma.site/
- **Current-state screenshots (Appendix A):** "Research usage tracking in Orbit"; "Research
  packs in CP today" — note today there is **no timestamp and no re-run option**; download
  is available from notifications.
- **Align with:** existing ClauseIQ / Sourcing tool designs (styling to be matched;
  workflows may need SME workshopping — led by Product Design Lead).

## Executive summary
- **What:** Replace CP's legacy GPT-mapping logic with the same Research Agent already used
  in Orbit — one shared mechanism, consistent outputs, cross-platform visibility.
- **Why:** Remove duplication/tech debt of two research-generation mechanisms; ensure
  consistent quality across internal (CP) and client-facing (Orbit); enable reuse/scale.
- **How:** Direct calls to the Research Agent aligned to Orbit parameters; preserve CP UX
  (auto-generate on initiative creation, no workflow change); bi-directional visibility
  using established patterns (e.g. ClauseIQ); limited enhancements (re-run, timestamps,
  usage tracking) without expanding into chat/history UIs.
- **Success:** single mechanism live (legacy GPT mapping removed); no user disruption;
  consistent outputs + tracking visible in both platforms; lower operational overhead.
- **Constraints:** preserve existing CP UX; single internal change; Orbit must already have
  adopted the Research Agent.

## Problem statements
- **A. Harmonise technologies:** CP and Orbit generate primers with different tech →
  duplication and maintenance overhead.
- **B. Output consistency:** different logic risks divergent research quality.
- **C. Share CP → Orbit:** no consistent mechanism to share CP-generated research with
  clients in Orbit.

## Goals & success criteria (by priority)
**In scope**
- Single mechanism to generate primers — **Success:** CP and Orbit call the same Research Agent.
- Remove legacy GPT-mapping logic — **Success:** admin-based GPT lookup no longer used.
- Maintain existing CP behaviour — **Success:** no change to when/where primers appear.
- Cross-platform visibility — **Success:** research from CP or Orbit is visible in both.
- Consistent usage tracking — **Success:** runs logged in a unified way.
- Auto-generate on initiative creation in Orbit; re-run option in CP workspace card; track
  usage in Orbit initiative overview whether run from Orbit or CP.

**Out of scope** *(do NOT build this sprint)*
- Research chatbot within CP.
- History tracking + history UI for research usage within Orbit.

## User journeys
> Verify against the personas in the linked platform profiles.

**In scope**
- **Journey A — created in CP:** research auto-generated, surfaced in the CP workspace, and
  reflected in Orbit via the agent backend (works on manual and bulk upload as today).
- **Journey B — created in Orbit:** generated via the Research Agent, surfaced in the CP
  workspace, tracked in Orbit; users opening the initiative in CP see the pack, by whom,
  when, and can re-run (Efficio-led / Jointly-led only).
- **Journey C — re-run from CP:** user re-runs an existing primer, replacing the previous
  output; sees timestamp, who ran it, and the re-run option.

Key UX outcomes: timestamp + icon for who generated (auto → default to initiative owner);
CP and Orbit surface the same reports for the same parameters within a **3-month window**
unless exception; consultants can change parameters to obtain a different pack.

## Detailed UI / interaction notes (from appendices/workshop)
- **Workspace re-run card:** remove the summarised text; **3 buttons** — Download, Re-run,
  History/Share. Re-run opens a **modal to select Category / Countries (like "add
  initiative")**; sends a notification on re-run.
- **Card cleanup:** remove the GPT name; max **250 characters**.
- **Share (Orbit→CP):** **paper-plane icon** next to Download → shares the document to the
  CP share modal; Status column shows **"Shared by client"** (similar to ClauseIQ).
- **Orbit Key Tool Coverage Card:** "In Progress" while running → "Completed" card same as
  ClauseIQ.

## Prior decisions & rejected alternatives
- **Decided:** use the same Research Agent + **same REST API** as Orbit.
- **Decided:** **keep** the GPT mapping for "AI Supplier Sentiment" and other admin-only
  GPTs (disable all fields except "Only show on Admin Page") — do **not** fully remove it.
- **Decided:** one-to-many client→Efficio taxonomy mapping assigned **alphabetically**.
- **Decided:** if no category selected → **no pack auto-created**.
- **Decided:** Orbit→CP sharing pushes to CP history tables, **not editable** by consultant.
- **Ruled out (this sprint):** CP research chatbot; Orbit history UI.

## Concept summary table
| Goal | Metric / target | Owner | Target date | Status |
| ---- | --------------- | ----- | ----------- | ------ |
| Single mechanism | CP + Orbit call same Research Agent | CP Team | TBC | Not provided in source |
| Remove legacy GPT mapping | Admin GPT lookup unused (except AI Supplier Sentiment) | CP Team | TBC | Decision noted |

## Linked design (bridge to the brain)
- **Platform profile + personas:** `design-brain/platforms/connected-platform.md` (CP-led)
  and `design-brain/platforms/orbit-client-connected-platform.md`.
- **Pattern(s):** `design-brain/patterns/list-detail.md` (initiative workspace + detail),
  `review-and-approve-workflow.md` (generated output + share), `guided-conversational-workflow.md`
  (re-run parameter modal).
- **Component(s):** `card-panel.md` (workspace / Key Tool Coverage card), `button.md`,
  `dialog.md` (re-run modal), `badge-status.md` (states / "Shared by client"), `data-table.md`
  (usage/history log).
- **Defaults:** `design-brain/defaults.md`.
- **Product surfaces referenced:** CP workspace carousel card, Key Tool Coverage Card,
  AI Centre, Admin Page.

## Delivery context (pre-fills the HAND OVER package — Part D)
- **Assumptions:** preserve existing CP UX (no workflow change); Orbit has already adopted
  the Research Agent; output will differ but appear in the same place/time.
- **Dependencies & technical constraints:** Research Agent readiness (SMEs); parameters
  agreed and same as Orbit; same REST API; notification alignment across CP + Orbit; define
  inherited vs user-supplied parameters; consistent overwrite semantics; security testing
  for bad AI/agent behaviour; review whether Admin GPT-mapping is used elsewhere before
  removing.
- **Risks:** removing GPT mapping could break other features (AI Supplier Sentiment);
  divergent outputs if parameters aren't aligned; bad agent behaviour (security).
- **Open questions / outstanding decisions:**
  - Refresh for in-flight initiatives after 3mo (Orbit)? → TBC — auto-refresh + notification;
    old pack stored in the documents page.
  - Refresh after 3mo (CP)? → TBC — auto-refresh + notification; old-pack storage location TBC.
  - How many states for the Key Tool Coverage card? → **2: Completed and Running.**
  - One-to-many client→Efficio taxonomy mapping? → **alphabetical order.**
  - User hasn't selected a category? → **no pack created automatically.**
  - Handle Orbit→CP sharing? → TBC — push to CP history tables, not editable; un/share by
    consultant.

## Delivery learnings to reuse
- Reuse **ClauseIQ** patterns: completed-card treatment, the share modal, and the
  "Shared by client" status; re-run parameter modal mirrors "add initiative".

## Future vision (context only — do not build)
- Completes consolidation of research-primer generation across Efficio platforms; later, a
  possible Orbit chatbot extension.

## Status & owner
- **Status:** draft
- **Owner:** Product Owner / Concept Lead
- **Last reviewed:** 2026-06-17

<!-- graph-links:start — generated by tools/gen_graph_links.py; do not hand-edit -->
## Vault graph
[[design-brain/components/badge-status|badge-status]] · [[design-brain/components/button|button]] · [[design-brain/components/card-panel|card-panel]] · [[design-brain/components/data-table|data-table]] · [[design-brain/components/dialog|dialog]] · [[design-brain/defaults|defaults]] · [[design-brain/patterns/guided-conversational-workflow|guided-conversational-workflow]] · [[design-brain/patterns/list-detail|list-detail]] · [[design-brain/patterns/review-and-approve-workflow|review-and-approve-workflow]] · [[design-brain/platforms/connected-platform|connected-platform]] · [[design-brain/platforms/orbit-client-connected-platform|orbit-client-connected-platform]]
<!-- graph-links:end -->
