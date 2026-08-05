---
type: concept-brief
status: stable
owner: Alexandre Blois
platform: connected-platform
surfaces: [Other / shared]
source: product
last_reviewed: 2026-08-05
tags: [orbit, discovery, concept-brief]
---

# Concept brief: Surface the latest RAID & commentary before a PM status review

**Requester:** Alexandre Blois · **Team:** Concept · **Submitted:** 2026-07-21

## A · Which corner of Efficio
- **Platform:** Connected Platform (internal)
- **Surface / feature area:** Other / shared

## B · The problem
- **Problem statement:** Before a weekly status meeting, a PM cannot quickly see the current risks, issues, decisions, actions and commentary for one initiative: they live behind a hidden top-right modal split by period and written as free text, so the PM rebuilds the picture in an offline tracker and can miss what changed since last period.
- **Why now / evidence:** Initial evidence shows recurring PM demand for consolidated, surfaced commentary and for audit information — who added or changed a note, when, and what changed. Status preparation is where that pain bites hardest and where offline trackers get created.

## C · Who and what they do
- **Primary user + situation:** A PM opening one initiative in CP the day before its status meeting, needing the current RAID position and what changed since last period.
- **Key journey / tasks:**
  1. PM opens the initiative and sees a surfaced Latest updates area instead of the hidden modal
  2. PM filters by type (risk, issue, decision, action, commentary) and sees who added each item and when
  3. PM identifies what changed since last period and flags the items to update before the meeting

## D · Success and edges
- **Key outcomes:** In a status-prep session, the PM can identify every RAID item changed since the last period, and who changed it, in under a minute — without opening the old modal or an offline tracker.
- **Out of scope / non-goals:** No new update types or fields and no change to how updates are captured; not the multi-initiative bulk view; not Sigma or status-output reuse; not rebuilding the RAID/commentary data model. CCP replication is out of scope this round but the surfacing pattern should not block it. This round only surfaces, filters, and diffs what CP already stores.
- **Known constraints:** Uses the risks, issues, actions and commentary already held in the existing modal. Depends on author/timestamp (who/when) metadata existing on current updates — flagged unknown if not. One sprint. Lives on the CP initiative detail / status surface.

## E · What already exists
- **Existing material:** Sponsor Intake concept pack (Sprint 83). Current state: hidden top-right modal split last period / this period, free text. Concrete surface: the CP initiative detail view where the modal button lives today. Related explore prototype: Delivery Radar (internal).
- **Open questions / assumptions you're unsure about:** Whether created-by / created-date / last-edited metadata already exists on current updates; where to surface the Latest updates area (initiative overview vs a status tab).

## Gate log

| Date | Verdict | By | Notes / gaps / override reason |
| ---- | ------- | -- | ------------------------------ |
| 2026-07-21 | Ready | brief-reviewer (opus, fresh context) | All eight criteria pass. Criterion 7: who/when metadata existence is CANNOT VERIFY from the vault → routed to the Context Pack backlog. Narrowed from `discovery/briefs/2026-07-21-enhancements-to-risks-issues-decisions-commentary-raid.md`. |

**Context gaps routed to the Efficio Context Pack backlog:** whether created-by / created-date / last-edited metadata exists on current CP updates; the existing RAID/commentary modal data model; approved CP visual truth for the initiative-detail surface.

## Explore outcome (2026-07-21)
Ran the `explore` method on this Ready brief: built a genuinely interactive concept
prototype (a PM status-prep view — surfaced RAID + commentary, filter by type, a
"changed since last review" toggle + hero stat, a since-last-review divider, expandable
change history, and a "flag → to update before the meeting" tray). Verified headless
(filters, diff, flag/tray flow, both themes, clean console). Delivered as a Claude
Artifact (session-private).

**Prototype record:** `discovery/prototypes/raid-status-prep/record.md` — archived
2026-08-05. The original Artifact was session-private and unrecoverable, so the archived
build is a labelled reconstruction of the feature list above; the record says so plainly.

A blind adversarial critique then pressure-tested the
**concept** and surfaced kill-risks that must be validated before this graduates:

1. **Load-bearing data unknown.** The whole value (who/when/what-changed) rests on
   per-field edit history + author attribution that the brief itself flags as unverified.
   If CP stores only current values, the honest concept shrinks to "the modal, on the
   page." **Validate first.**
2. **"Changed" is defined two ways.** Per-user last-view (what the prototype built) vs a
   shared period/meeting boundary (what the job needs). Pick one; confirm CP can compute it.
3. **Possibly the wrong bet.** The offline tracker may persist because *capture* or the
   *multi-initiative sweep* is the real pain — both explicitly out of scope here. A
   read-only single-initiative view may solve the easy third.

Also flagged: adoption/parallel-tool risk, and edge cases the demo hides (volume,
deletions, first-ever visit with no baseline, client-visible vs internal items).

**Status: not ready for Port.** Do not fund build until questions 1 and 2 come back
green from a real PM session. These feed the Efficio Context Pack backlog.

## Graduation
- **Discovery pack:** not yet — gated on the explore validation above.

<!-- graph-links:start — generated by tools/gen_graph_links.py; do not hand-edit -->
## Vault graph
[[discovery/briefs/2026-07-21-enhancements-to-risks-issues-decisions-commentary-raid|2026-07-21-enhancements-to-risks-issues-decisions-commentary-raid]] · [[discovery/prototypes/raid-status-prep/record|record]]
<!-- graph-links:end -->
