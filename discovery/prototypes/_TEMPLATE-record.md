---
type: prototype-record
status: draft
owner: <the idea owner — same person as the brief's owner>
surfaces: [<MarketIQ | ClauseIQ | RFP Analytics | RFP Builder | Other / shared>]
source: product
last_reviewed: <YYYY-MM-DD>
tags: [orbit, discovery, prototype-record]
brief: `discovery/briefs/<date>-<slug>.md`
prototype: prototype.html
---

# Prototype record: <concept name>

> **The fourth Concept Pack deliverable, made durable.** An explore prototype is delivered
> running — as an Artifact the stakeholder can click — but a delivery link is not evidence:
> sessions expire and Artifacts are private. This record plus the `prototype.html` beside it
> are what survive, and what the Vault Health "Concepts in flight" tracker reads to light a
> concept's *Explored* stage.
>
> **Status here means:** `draft` delivered but not yet verified · `in-review` verified, its
> critique still open · `stable` the concept it proves has been validated.
>
> Copy this file to `discovery/prototypes/<slug>/record.md`, fill every section, and put the
> self-contained HTML beside it as `prototype.html`.

**Brief:** `discovery/briefs/<date>-<slug>.md`

## Provenance

<Mandatory, and answer honestly. Either: "Original — the file beside this record is the
exact build delivered on <date>." Or: "Reconstruction — the original delivery was
session-private and is unrecoverable; rebuilt on <date> to the feature list recorded in the
brief, approved by <owner>." A reconstruction is useful evidence; an undisclosed one is not.>

## Verification

<What was actually checked, not what should have been. Name the method (headless driver,
manual pass), the flows exercised, both themes if applicable, and the console state. If a
check was skipped, say so.>

## What it demonstrates

<The bet this prototype makes clickable — the one thing a stakeholder can now judge that a
written brief could not make them judge.>

## Known gaps / critique pointers

<Where the critique landed, what the prototype deliberately fakes or omits, and which
questions must come back green before this graduates. Link the brief's gate log or explore
outcome rather than restating it.>

---

*`prototype.html` is vault-only: it is withheld from product-repo exports by
`tools/export_brain.py` (throwaway concept code, often with client-shaped sample data).
This record travels; the runnable file stays here.*
