---
type: foundation
status: stable
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-06-14
maturity_score: 70
tags: [orbit, design-brain, ux-copy]
---

# ux-copy.md — Voice & microcopy

Copy is part of the component. Generated text follows these rules; component contracts
specify defaults.

## Voice
- Clear, calm, professional. Procurement professionals at work — respect their time.
- Plain language over jargon; precise over clever. No jokes in error/empty states.
- Sentence case for UI labels and buttons. Consistent terminology across surfaces.

## Buttons & actions
- Verb-led and specific: "Save changes", "Run analysis", "Add clause" — not "OK", "Submit".
- One primary action per view/section.

## Empty states
Say what this is, why it's empty, and the one next action. Avoid blame and filler.

## Errors
- What happened, in plain terms, + how to recover. No raw codes as the only message.
- Pair with a non-colour signal (icon/label) per `accessibility.md`.

## Loading
Honest, brief, specific where useful ("Loading clauses…"). Prefer skeletons to spinners.

## Numbers, dates, units
Consistent formatting; locale-aware. Procurement data (currency, %, dates) must be
unambiguous. Note localisation needs in the contract.

## Don't
- ❌ "Oops! Something went wrong" as the entire error message.
- ❌ Inconsistent terms for the same concept across ClauseIQ / MarketIQ / RFP surfaces.
