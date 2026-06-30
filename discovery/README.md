---
type: discovery-index
status: draft
owner: design-system
surfaces: [shared]
source: product
last_reviewed: 2026-06-17
maturity_score: 40
tags: [orbit, discovery, index]
---

# discovery/ — Business logic & requirements packs

This folder holds **Discovery packs**: the business logic, rules, and requirements for
each assigned piece of design work. It is a layer **parallel to** the Design Brain, not
part of it.

| | Design Brain (`design-brain/`) | Discovery (`discovery/`) |
| --- | --- | --- |
| Answers | *How* Orbit looks & behaves | *What* we're building & *why* |
| Lifecycle | Stable, slow-changing | Per-initiative, project-speed |
| Governance | Owner-approved, change-controlled | Owned by the initiative; not gated |
| Shape | One canonical set | A template + many instances |

Keeping these separate is deliberate: pouring volatile project requirements into the
stable brain would bloat it and erode trust in it. The two layers **link** to each other
but age independently.

## How an AI finds the right pack

1. `AGENTS.md` §3 routes any "assigned feature/initiative" task to
   `discovery/<initiative>.md`.
2. Name the initiative in your prompt (e.g. *"build the supplier tracker for the ACME
   sourcing initiative"*) so the agent can match the pack.
3. The agent confirms platform + linked patterns from the pack's header, then reads those
   brain files before building.

## How to add a pack

1. Distill the sprint's **4D Concept Discovery Pack** (Word) into the template — keep the
   design-relevant signal, drop ToC / stakeholder lists / recommended-tools / disclaimer.
2. Copy `_TEMPLATE.md` to `discovery/<initiative-name>.md` and fill it. Set `platform`,
   `linked_patterns`, and `linked_components` so the bridge to the brain is explicit.
3. Add a row to the index below.

## Lifecycle (keeps sprint churn clean)

Each pack carries a `status`: `draft → active → shipped → archived`. When a sprint ends,
mark its pack `shipped` (then `archived`) so an agent never treats stale requirements as
live. Only `active` packs are authoritative. Don't create a full pack for throwaway
explorations — a pack is for work real enough to build against.

## Index

| Initiative | Pack | Platform | Linked patterns | Status |
| ---------- | ---- | -------- | --------------- | ------ |
| MarketIQ Research Agent — n8n upgrade | `discovery/marketiq-research-agent-n8n-upgrade.md` | both (CCP priority) | guided-conversational-workflow, review-and-approve-workflow | draft (example) |
| Research Agent in Initiatives — unify CP + Orbit | `discovery/research-agent-in-initiatives-cp-orbit.md` | both (CP-led) | list-detail, review-and-approve-workflow, guided-conversational-workflow | draft (example) |
