---
type: definition-matrix
status: draft
owner: design-system
surfaces: [ClauseIQ]
source: product
last_reviewed: 2026-08-03
tags: [orbit, discovery, definition-matrix, clauseiq]
---

# Scenario & Behaviour Matrix: ClauseIQ — Supplier Rounds

> **The golden example** for the Definition Pack stage — the shape every matrix follows.
> Reconstructed into the canonical template from the owner's original working documents
> (ClauseIQ Scenarios & Behaviour Matrix + Journey Flows, working draft v0.1 ·
> 23 July 2026). The generated journey-flows page is built from this file by
> `tools/build_journey_flows.py` — never hand-edit the generated page.

**Source Concept Pack:** predates the pack chain — this matrix is the exemplar the chain
was designed around. · **Working draft:** v0.1 · 23 July 2026

## Key rules (agreed)

### R1 · Round grouping (version key)
Rounds group by salesforce_id + project + initiative + a fourth parameter — the supplier ID when available (detected or assigned), else a round UUID assigned at first upload per unknown context; round-2+ uploads send that previous ID so the backend links rounds (R9). This combination decides first version vs new version vs exact duplicate. TO CONFIRM: exact definition of the fourth parameter and the round-UUID → supplier-ID handover (C1).

### R2 · Supplier detection (round 1)
CP sends no supplier name on first upload. Detection runs on upload, before/in parallel with analysis (analysis never needs the name and always proceeds). Detected supplier is displayed — no confirmation step — and is editable via dropdown. If detection fails, the contract is bucketed as Unknown N (R9).

### R3 · Accept by default — two states only
AI recommendations stand as the user's position unless edited — "what's in your Excel is true unless you've edited it". No tracked distinction between AI-generated and user-edited. Each clause is either OPEN (position not accepted; a recommended next position exists) or MET/ACCEPTED (position met, or supplier's position accepted).

### R4 · Benchmark — the comment IS the negotiation guide
The per-clause comment holds the current agreed position: the AI recommendation (default), the user's edit, or the supplier's accepted wording. If a comment exists, deviation is calculated against it; else vs best practice / playbook. From round 2 no carried-over clause should lack a comment — round-1 deviation-None clauses get the supplier's wording auto-populated (mechanics open, C6). Only a brand-new supplier-introduced clause is evaluated vs best practice.

### R5 · Met / Not met (binary)
Derived 1:1 from deviation vs the R4 benchmark. None = Met. Low/Medium/High = a single "Not met" label colour-tiered (Low green, Medium amber, High red). No "partially met". The tag sits on the SUPPLIER'S latest position and answers: has the supplier reached MY position?

### R6 · Score
Each round's score is calculated from that round's deviation outputs — i.e. against the live negotiation baseline (comments where present, best practice otherwise).

### R7 · Regression
A clause whose previous-round deviation was None now deviates. Calculated CP-side from stored previous-round deviations; surfaced as a distinct Regression bucket. NOT regression: (a) Low → High (already Not met, just worse); (b) a change that still evaluates to None — stays Met, not flagged (R10).

### R8 · Accept supplier position
The recommended-next-position field greys out, the row drops to the Met list, and the supplier's current wording is pasted into that field. Next round it becomes the "previous negotiation position". If the supplier later changes it and it deviates → regression; if it still evaluates None → stays Met. This is why accepted rows are retained, not deleted.

### R9 · Unknown suppliers, aliases & fingerprinting
Undetected suppliers bucket as Unknown 1, 2, … per contract (never lumped; filename shown, never auto-used as the name). Resolved via type-ahead over the DUNS-ID master list or free-text alias. Aliases fingerprint to a new Efficio supplier ID; an alias is a front-end label only and never appears in other users' dropdowns. Once fingerprinted, future contracts can auto-detect.

### R10 · Immaterial changes
Wording changed but deviation still None → the comparison summary records it, the front end does NOT flag it. The tool answers "is my contract safe", not redlining; wording audit trails live in Word track changes.

### R11 · Duplicates
Identical content to a processed version is not reprocessed. Backend returns the existing aws_file_id (regenerating comment-aware actionability first if comments were added since); CP shows existing results. No new round.

### R12 · Guide contents & sorting
The guide contains ALL clauses — one table sorted by deviation, flagged at top (High → Medium → Low), met/None below, missing terms as rows. Comparison rounds: Not met on top (High → Medium → Low), regressions called out, Met collapsed at bottom. Downloads include every clause — an auditable record, never just the outstanding ones.

### R13 · Negotiation guide versioning
Guide version is bound to the contract round, not to edits or downloads. Contract v1 → Guide V1 (active); any number of edits/downloads stay within V1 (stamps differentiate activity). Contract v2 → Guide V2, and so on. Downloads are point-in-time snapshots of the active version.

### R14 · Convergence
The convergence score appears from Round 1: total clauses vs Met/None — e.g. 50 clauses with 23 deviations (not met) shows convergence 27/50, with 23 open clauses to negotiate.

## Open clarifications (to confirm)

### C1 · Fourth grouping parameter
Agree exact mechanics with the data team: the parameter's formal definition/name in the payload, and the handover when an Unknown resolves — does the round UUID persist as key with supplier ID attached, or does the key remap (and how are earlier rounds re-linked)? Owner: Data team.

### C2 · Template review mode
Ship a dedicated template mode (entry question + named grouping, no detection/fingerprinting), or route templates through the Unknown/alias path with guidance? See E-09. Owner: ADV / Data team.

### C3 · Missing-clause tag & filter
Do we want an explicit label/pill and filter for missing clauses? If so: is "missing" passed back by ClauseIQ or derived front-end? Candidate rule: clause expected per playbook + supplier position blank → "Missing" pill; recommendation = include the clause. Owner: Data & CCP teams.

### C4 · Rounds against unresolved Unknowns
Confirm: (a) selecting Unknown N and uploading a new version adds a round via its round UUID — supported? (b) a fresh no-detection upload creates Unknown N+1 and can never silently attach to an existing Unknown — confirm; (c) or must Unknowns be resolved before round 2? Agree the model and make the UI make it obvious. Owner: Data team.

### C5 · When is the supplier value sent to the data team?
On assign/correct (E-01/02/03/04): immediate update/callback (fingerprints sooner, fixes grouping at once) vs bundled into the next ClauseIQ run payload (simpler, but leaves a window where CP and the data team disagree). Agree trigger and payload. Owner: Data team.

### C6 · Auto-populating comments for deviation-None clauses
Intended rule per R4. To agree: who populates it (front end on guide generation vs data team in run output), when (round-1 results vs round-2 submission), and whether auto-accepted rows are visually distinguishable from explicitly accepted ones (probably not — per R3 there are only two states). Owner: Data team + front end.

## Green Path

### G-01 · Round 1 — first upload, supplier detected
- **Subtitle:** The very first contract lands in a blank initiative
- **Rules:** R1, R2, R3, R4, R12
- **Starting state:** New initiative. No ClauseIQ history for this supplier context.
- **User actions:** Open initiative → open ClauseIQ → click 'Upload contract' → select PDF → submit. Wait through ~10 min processing (progress shown). Detected supplier is displayed (e.g. 'Supplier: Aurora Networks') — no confirmation needed; click it to change if wrong.
- **Backend:** CP sends metadata (salesforce_id, project, initiative, supplier = blank, filename). Supplier-detection run extracts the supplier from the contract; ClauseIQ V1 run proceeds in parallel (doesn't need the name): clause extraction → no comments exist → every clause benchmarked vs best-practice / client playbook (R4) → deviation levels, recommendations, rationale, score → persisted → callback returns aws_file_id + detected supplier.
- **Front-end result:** Results modal (V1 variant): overall score + High/Medium/Low deviation counts vs best practice. View Results page with clause-level detail. Negotiation guide generated containing ALL clauses in one table, sorted by deviation — flagged at top (High → Medium → Low), met/none below — with missing terms as rows (R12). Detected supplier displayed with an edit option (click to change via dropdown).
- **Next action:** Open the negotiation guide and triage (G-02 / G-03 / G-04); correct the displayed supplier only if it looks wrong (E-03).
- **Expected outcome:** First version recorded under Aurora Networks (version key per R1). Guide pre-populated with AI recommended positions, all defaulted to accepted (R3).
- **Worked example:** Upload 'Aurora_Networks_MSA_draft1.pdf'. Score 62/100; of 100 clauses, 60 flagged: 18 High, 26 Medium, 16 Low. Payment terms clause: contract says 60 days; playbook position 45 days; deviation High; AI recommendation 'Payment terms not to exceed 45 days'.

### G-02 · Round 1 guide — defaults stand (no edits)
- **Subtitle:** Accept-by-default: doing nothing IS a decision
- **Rules:** R3, R4
- **Starting state:** Guide generated (G-01). User reviews but changes nothing.
- **User actions:** Open guide → scroll/review rows → close (no per-row actions taken).
- **Backend:** Comments persisted per guided clause = the AI recommendations, unchanged (accept by default, R3). These are the benchmark for round 2 (R4).
- **Front-end result:** Guide displays as generated — the default state IS the accepted position, so no separate 'accepted' status is shown and nothing is marked as edited. No last-updated stamp appears, since nothing has been changed (the stamp only appears once someone edits).
- **Next action:** Download Guide V1 (G-05) and negotiate.
- **Expected outcome:** Round 2 evaluates the next contract against the AI recommendations as-is. If the supplier complies with every recommendation, round 2 returns everything Met.
- **Worked example:** Guide shows all 100 clauses, the 60 flagged sorted to the top. User accepts all 60 recommendations implicitly. Supplier's next draft adopts all recommended wording → round 2: 60/60 Met, all rows greyed, zero actions.

### G-03 · Round 1 guide — edit a position
- **Subtitle:** The user's goalpost replaces the AI's — no tracked distinction
- **Rules:** R3, R4
- **Starting state:** Guide generated (G-01). User wants a different goalpost on specific clauses.
- **User actions:** Open guide → click row (Payment terms) → Edit → change recommended position inline → Save → move to next row.
- **Backend:** Comment for that clause updated to the user's wording; the edited comment is now the benchmark for that clause (R4). All other clauses keep the default recommendations.
- **Front-end result:** Row simply shows the updated recommended next position — no separate edited-vs-generated status is tracked or displayed. Guide 'last updated' stamp appears/refreshes.
- **Next action:** Continue triage; download Guide V1 when done.
- **Expected outcome:** Round 2 evaluates that clause against the USER'S position, not the playbook. A contract meeting the playbook but not the user's tougher position is Not met.
- **Worked example:** Playbook says 45 days; user edits position to 30 days. Round 2 contract returns 45 days → NOT met (deviation vs 30-day comment) even though playbook-compliant. Returns 30 days → Met.

### G-04 · Round 1 guide — accept supplier position
- **Subtitle:** Conceding a clause stores the wording — it doesn't delete the row
- **Rules:** R3, R8
- **Starting state:** Guide generated (G-01). User is content with the supplier's current wording on a clause despite the flagged deviation.
- **User actions:** Open guide → click row (Liability cap) → 'Accept supplier position'.
- **Backend:** The supplier's current clause wording is pasted into the recommended-position (comment) field (R8), so the backend always has a comparison point for future rounds. Deviation for this clause in later rounds is calculated vs this accepted wording.
- **Front-end result:** Success message confirms the supplier's latest position has been accepted; the wording is copied into the recommended-next-position field with a tag reading 'Accepted supplier's position as above'. The row greys out and transitions (brief animation) down into the MET section — no action required, not counted in open actions.
- **Next action:** Continue triage; download Guide V1 when done.
- **Expected outcome:** If the supplier leaves the clause unchanged, later rounds show it Met/greyed with no action. If the supplier changes it, deviation vs the accepted wording flags it as regression (see E-07).
- **Worked example:** Playbook wants liability cap at 150% of fees; supplier offers 100%; user accepts 100%. '…total aggregate liability shall not exceed 100% of fees paid' is stored as the position for this clause.

### G-05 · Export Guide V1 and negotiate
- **Subtitle:** Point-in-time snapshot + downloaded/locked banner protects the live baseline
- **Rules:** R12, R13
- **Starting state:** Triage complete: a set of OPEN clauses (current position not met, each carrying a recommended next position — left as generated or edited, no distinction) and a set of MET/ACCEPTED clauses.
- **User actions:** Click 'Download negotiation position' → Excel snapshot (Guide V1) saved locally — contains ALL clauses, agreed and outstanding (R12), as an auditable record. Share with colleagues / use in supplier discussion. Ask the supplier to return a revised contract.
- **Backend:** No processing. Live guide (comments) remains stored in-app as the single working baseline; the download is a point-in-time snapshot of the active version — multiple downloads within a round are all Guide V1 snapshots; the version only advances when the next contract uploads (R13).
- **Front-end result:** Download completes. Guide takes a downloaded/locked status with a banner: 'Version has been downloaded. Please check with your team if it's safe to edit this page, as the supplier may be negotiating the current terms.' Two stamps: last edited ({timestamp} by {user} — only once an edit has been made) and last downloaded ({timestamp} by {user}).
- **Next action:** Negotiate with the supplier; await revised contract, then G-06.
- **Expected outcome:** The app remains the source of truth — nothing needs re-uploading for comparison to work; round 2 compares against the stored live guide automatically. The locked banner protects against someone editing the live baseline while the snapshot is mid-negotiation (which would desync the two). Lifecycle: banner appears on download, persists until the next contract version uploads (then clears — the new round's comparison hasn't been downloaded yet), and reappears on each subsequent download.
- **Worked example:** Guide V1.xlsx shared with the category lead; negotiation call held with Aurora Networks referencing the 22 open positions.

### G-06 · Round 2 — upload revised contract
- **Subtitle:** From here on, the benchmark is YOUR guide — not the playbook
- **Rules:** R1, R4, R5, R6, R7, R13
- **Starting state:** Supplier returns revised contract. Live guide holds the round-1 positions.
- **User actions:** Return to the ClauseIQ conversation → select supplier 'Aurora Networks' (detected/confirmed in round 1) → click 'Upload new version' → select file → submit.
- **Backend:** Version detection via salesforce_id + project + initiative + supplier → NEW VERSION (R1). Backend loads previous version output + comments; generates comparison_summary per clause (what changed vs previous version); per-clause deviation vs comment-if-present-else-playbook (R4); Met/Not met derived (R5); score from deviation outputs (R6); previous-round deviation levels available for regression logic (R7); callback.
- **Front-end result:** Results modal (V2 variant): Met / Not met counts, labelled 'Evaluated against your negotiation guide', plus the round's score (R6); best practice applies per clause only where no comment exists (e.g. new clauses). Comparison view per row, three columns: (1) previous negotiation position sent to supplier, (2) latest supplier position — carrying the Met/Not met tag colour-tiered by deviation (R5), (3) recommended next position — the AI recommendation, editable, present on all Not met rows including regressions. Sort: Not met at top ranked High → Medium → Low, regressions specifically called out, Met collapsed/greyed at the bottom.
- **Next action:** Review Not met rows (G-07).
- **Expected outcome:** Uploading contract v2 activates Negotiation Guide V2 (R13). Progress is measured against the user's own positions. Met rows need no attention; the default view answers 'what do I still need to action?'
- **Worked example:** Round 2 results: 41 Met (collapsed), 17 Not met (5 red/high, 8 amber/medium, 4 green/low), 2 accepted-position rows unchanged (greyed), 0 regressions. Payment terms returned at 30 days → Met, greyed.

### G-07 · Round 2 guide — action the Not met rows
- **Subtitle:** Keep, edit, or concede each open clause; comments become the round-3 benchmark
- **Rules:** R3, R8, R13
- **Starting state:** Round 2 comparison on screen (G-06).
- **User actions:** Expand a Not met row → review the previous negotiation position sent to the supplier, the latest supplier position (tagged Met/Not met), and the recommended next position → leave the recommendation, Edit it inline, or 'Accept supplier position' if conceding → repeat for each Not met row incl. regressions (bulk actions where appropriate).
- **Backend:** Comments updated per actioned clause within Negotiation Guide V2 (active since contract v2 uploaded, R13) — edits do not change the version. Updated comments are the round-3 benchmark.
- **Front-end result:** Rows update state as actioned; open-action count falls; guide 'last updated' refreshes.
- **Next action:** Download Guide V2 (as G-05) and hold the next negotiation round.
- **Expected outcome:** Every clause always carries a current position: kept, edited, or the supplier's accepted wording (R3/R8). The loop tightens each round. On downloading Guide V2, the last-downloaded stamp and locked warning reappear (per G-05); the warning clears when the next contract version uploads.
- **Worked example:** Termination notice still 90 days vs my 30 → Not met (red). New AI recommendation proposes 45 as a landing zone; user edits to 30 and holds firm. Insurance clause conceded → Accept supplier position.

### G-08 · Round 3 — upload, rolling context
- **Subtitle:** Context never resets; comparison is always vs your latest positions
- **Rules:** R1, R4, R5, R6, R7
- **Starting state:** Supplier returns a third draft. Live guide = Guide V2 positions.
- **User actions:** Select supplier → 'Upload new version' → submit (same flow as G-06).
- **Backend:** New version detected (round 3). Same processing as G-06: comparison vs previous version; deviation vs current comments; Met/Not met; score; regression check vs round-2 deviations.
- **Front-end result:** Per row, same three columns: previous negotiation position sent to supplier (Guide V2) → latest supplier position (contract v3, tagged Met/Not met) → recommended next position (editable) on Not met/regression rows. Rolling one-round-back context; deeper history via the optional detail view.
- **Next action:** Action remaining Not met rows; download Guide V3 if another round is needed.
- **Expected outcome:** Context never resets: each round the comparison is against the user's latest positions, with last round's terms visible per row.
- **Worked example:** Round 3: 55 Met, 4 Not met (all amber/green), 1 regression flagged (see E-06/E-07 mechanics). User pushes on the last 4.

### G-09 · Convergence — ready to sign
- **Subtitle:** The loop simply isn't continued; everything is traceable
- **Rules:** R12, R13, R14
- **Starting state:** Round N results show no red items and the user is satisfied.
- **User actions:** Review round-level view: score trend by round, Met/Not met counts, open actions = 0 (or all remaining consciously accepted).
- **Backend:** No special processing — the loop simply isn't continued.
- **Front-end result:** Round-level panel: score trend rising across rounds; all guide rows Met or accepted; version history lists every uploaded contract (version, file name, upload date, score) with open/download.
- **Next action:** Proceed to signature outside the tool.
- **Expected outcome:** The user can evidence exactly what was asked for, what the supplier agreed, and when — every position traceable to a guide row and round.
- **Worked example:** Round 3 closes with 58 Met / 2 accepted positions. Score trend 62 → 78 → 91. User downloads final guide and contract v3 for the deal file and proceeds to sign.

## Red & Edge Paths

### E-01 · Round 1 — no supplier detected (single contract)
- **Subtitle:** Analysis never blocks; the contract becomes Unknown 1 until resolved
- **Rules:** R1, R2, R9
- **Starting state:** First upload; the contract has no extractable supplier name (e.g. name only in a logo image, or a blank template).
- **User actions:** Upload contract as normal (G-01). Processing completes. On the results page a card shows: 'No supplier detected — please assign a supplier' → click card → type-ahead search of the master supplier list (DUNS-ID suppliers) → select the supplier; or enter a free-text alias if not found (E-04).
- **Backend:** Supplier-detection run returns 'missing'. ClauseIQ analysis still completes vs best practice (detection failure never blocks analysis). The user's selection/alias is sent back to the data team referencing the run/contract ID; alias is fingerprinted to an Efficio supplier ID (R9).
- **Front-end result:** Full round-1 results shown as normal, plus the unresolved-supplier card. Contract is grouped as Unknown 1 (file name visible for identification) until resolved.
- **Next action:** Resolve the supplier via the card when known — or continue working against Unknown 1: its round UUID (R1) groups rounds, so revisions can be uploaded against it and the supplier assigned later.
- **Expected outcome:** Once resolved, round-2 uploads are made against the named supplier; until then the context is keyed by its round UUID (R1), and round-2 sends that previous ID so the backend links rounds correctly.
- **Worked example:** Aurora's returned template has the name only in the header logo. Detection fails → Unknown 1 ('Aurora_response.pdf'). User assigns 'Aurora Networks Ltd' from the master list; rounds link from round 2 onward.

### E-02 · Round 1 — multiple contracts, no supplier detected on any
- **Subtitle:** Every no-name contract gets its OWN Unknown — never one shared bucket
- **Rules:** R1, R9
- **Starting state:** Same user/initiative issued a blank template to several suppliers; all responses come back with no extractable supplier name. Supplier identity only evident from file names.
- **User actions:** Upload each contract as normal. Each shows its own unresolved-supplier card. For each Unknown: click card → select supplier from master list or enter alias → confirm.
- **Backend:** Each contract becomes its OWN context with its own round UUID (R1) — Unknown 1, Unknown 2, Unknown 3… They are never lumped into one 'other' bucket, and the file name is never auto-used as the supplier name (R9). Backend does not associate the Unknowns with each other as rounds. On round 2, CP sends the previous Unknown's round UUID so the backend links the rounds to the right negotiation.
- **Front-end result:** Initiative shows Unknown 1 ('Deloitte_response.pdf'), Unknown 2 ('PWC_response.pdf'), Unknown 3 ('KPMG_response.pdf') — each with its file name so the user can tell them apart.
- **Next action:** Resolve each Unknown where known — recommended, not mandatory. To continue unresolved, select that Unknown (via its file name) and upload the next round against it; its round UUID keeps rounds grouped. Assign the supplier later at any point (open question C4).
- **Expected outcome:** Each negotiation correctly grouped; no cross-contamination of rounds. Resolution can happen at any point without losing history (round UUID persists). The failure mode this design prevents: five no-name contracts collapsing into one shared 'other' context.
- **Worked example:** 5 suppliers return no-name contracts. User maps Unknown 1→Deloitte, 2→PWC, 3→KPMG, 4→alias 'Northern Fencing Co' (not in master list), 5→EY. Round 2 uploads land against the right suppliers.

### E-03 · Round 1 — wrong supplier detected
- **Subtitle:** Correct the match before it ever becomes the version key
- **Rules:** R1, R2, R9
- **Starting state:** Detection returns a confident but incorrect match.
- **User actions:** The displayed supplier reads 'Yorkshire Water'. User clicks the displayed supplier → dropdown opens (type-ahead over the master supplier list — suppliers with a DUNS ID only) → select the correct supplier, or enter a free-text alias (E-04).
- **Backend:** Corrected supplier mapping is sent to the data team against the run/contract ID, replacing the detected value. Grouping key updated before round 2.
- **Front-end result:** Displayed supplier updates to the corrected name; conversation/grouping renamed accordingly.
- **Next action:** Proceed with triage as normal.
- **Expected outcome:** Round 2 uploads land against the corrected supplier; the wrong detection never becomes the version key.
- **Worked example:** Contract references Yorkshire Water as a third party; detection picks it as the supplier. User corrects to 'Severn Trent Services'. Rounds group under Severn Trent.

### E-04 · Brand-new supplier — free-text alias & fingerprinting
- **Subtitle:** Aliases are private front-end labels; fingerprinting enables future auto-detect
- **Rules:** R9
- **Starting state:** The genuine supplier is a small/local company not in the master supplier list.
- **User actions:** On the unresolved-supplier card (or wrong-match correction), type the name → no match found in the DUNS-ID list → choose 'Add as new' and enter the free-text alias → confirm.
- **Backend:** Alias is passed to the data team and fingerprinted, creating a new Efficio supplier ID. The alias remains a front-end label for this context only — it never appears in other users'/clients' dropdowns. Once fingerprinted, future contracts from this supplier can auto-detect (R9).
- **Front-end result:** Supplier shows under the alias name in this initiative; version grouping works normally.
- **Next action:** Continue the negotiation loop as normal.
- **Expected outcome:** Aliases can't pollute other clients' supplier lists; the master list shown for selection remains DUNS-ID suppliers only.
- **Worked example:** 'Northern Fencing Co' isn't in the master list. User adds it as an alias; fingerprinting assigns Efficio supplier ID SUP-88412. A later initiative uploading a Northern Fencing contract auto-detects it.

### E-05 · Exact duplicate upload
- **Subtitle:** Identical content is never reprocessed and never creates a round
- **Rules:** R11
- **Starting state:** User re-uploads a contract whose content is identical to a version already processed in this supplier context (e.g. wrong file picked, or same file re-sent).
- **User actions:** Select supplier → 'Upload new version' → select file → submit.
- **Backend:** Duplicate detection matches content to an existing processed version → NOT reprocessed. If comments were added since the original run, comment-aware actionability is regenerated for those clauses first. Callback returns the EXISTING aws_file_id with a duplicate message (R11).
- **Front-end result:** Message: this file matches an existing version — showing existing results. No new round appears in version history.
- **Next action:** Check the file; upload the correct revised contract if this was a mistake.
- **Expected outcome:** No wasted ~10 min processing; version history stays clean; scores/rounds are not distorted by accidental re-uploads.
- **Worked example:** User re-uploads round-2 file by mistake in week 3. ClauseIQ returns the existing round-2 results instantly; version history still shows exactly 2 versions.

### E-06 · Regression — previously fine clause worsens
- **Subtitle:** Was deviation None, now deviates → the Regression bucket catches it
- **Rules:** R4, R5, R7
- **Starting state:** Round 1: a clause had deviation None (Met — nothing to negotiate; its comment auto-populated with the supplier's round-1 wording per R4, i.e. the supplier's position is the accepted working position). Round 2: the supplier quietly changes it for the worse.
- **User actions:** Upload round 2 as normal (G-06).
- **Backend:** The clause's comment is the supplier's accepted round-1 wording (R4). The latest position is evaluated against that previous accepted position and deviates → deviation High → Not met (tag on the supplier's position). Comparison summary records what changed. Previous-round deviation was None, now High → Regression bucket (R7).
- **Front-end result:** Clause surfaces prominently in the Regression bucket — visually distinct from ordinary Not met rows — with the comparison summary showing what changed.
- **Next action:** Challenge the supplier ('we never raised this because it was fine — why has it changed?'); add/accept a recommendation to restore it.
- **Expected outcome:** Silent worsening of previously-acceptable clauses cannot slip through. Note: Low → High is NOT regression — that clause was already Not met and simply worsened (trend visible via previous deviation level).
- **Worked example:** Round 1 confidentiality clause: mutual, standard carve-outs → deviation None; wording stored as the accepted position. Round 2: supplier inserts a broad 'business purposes' disclosure right → deviates from their own round-1 wording → deviation High → Regression bucket, red.

### E-07 · Regression on an accepted-supplier-position clause
- **Subtitle:** Why 'accept' stores the wording instead of deleting the row
- **Rules:** R7, R8
- **Starting state:** Round 1: user accepted the supplier's position on a clause (G-04) — supplier wording stored as the comparison point. A later round changes that clause.
- **User actions:** Upload the new round as normal.
- **Backend:** The clause HAS a comment (the accepted supplier wording, per R8), so deviation is calculated against it. The stored text appears this round as the 'previous negotiation position'. If the changed wording deviates (Low/Medium/High) from the accepted position → Not met (colour-tiered on the supplier's position), and previous deviation was None → Regression bucket (R7). If the change still evaluates to deviation None → remains Met, no regression.
- **Front-end result:** The previously greyed row un-greys and surfaces in the Regression bucket: 'we agreed this — it has changed'.
- **Next action:** Challenge the supplier; re-accept, or set a new position for the next round.
- **Expected outcome:** This is exactly why 'accept supplier position' stores the wording rather than deleting the row: an accepted clause remains protected against later material changes — while immaterial rewording (deviation None) passes silently.
- **Worked example:** Round 1: user accepted liability cap at 100% of fees. Round 3: supplier drops it to 50%. Deviation vs the stored 100% wording → Regression, red. Without the stored wording this change would have been invisible.

### E-08 · Immaterial change on a compliant clause
- **Subtitle:** The tool answers 'is my contract safe', not 'did any words change'
- **Rules:** R5, R10
- **Starting state:** The supplier rewords a clause between rounds, but the new wording still satisfies the benchmark (deviation None).
- **User actions:** Upload the new round as normal.
- **Backend:** Comparison summary records the wording change. Deviation vs the benchmark remains None → Met (R5). Front end does NOT flag it for action (R10).
- **Front-end result:** Row stays Met/greyed in the default view. The wording change is visible only if the user drills into the row's comparison detail.
- **Next action:** None required.
- **Expected outcome:** No noise: the tool answers 'is my contract safe', not redlining. Full wording audit ultimately belongs to Word track changes on the document itself.
- **Worked example:** Supplier rewords the notices clause from 'registered post' to 'registered post or reputable courier' — still compliant. No flag; visible in comparison summary only.

### E-09 · Template review mode (open)
- **Subtitle:** Open decision: dedicated mode vs routing through the Unknown/alias path
- **Rules:** C2
- **Starting state:** A user wants to iterate a contract template (no supplier exists at all), e.g. hardening a client's standard MSA before issue.
- **User actions:** PROPOSED (open decision): first question on entry — 'Are you reviewing a template or an actual supplier contract?' If template: give it a name, which becomes the grouping ID; no supplier detection or fingerprinting is triggered.
- **Backend:** Template runs skip supplier detection/fingerprinting; versions group under the template name. Without a dedicated mode, a template would fall into the Unknown/alias path (E-01/E-04) — workable, but fingerprinting a template name as a 'supplier' pollutes supplier data, which is what the mode avoids.
- **Front-end result:** Template appears as its own named grouping with normal round/version behaviour.
- **Next action:** DECISION NEEDED: ship a dedicated template mode (requires landing-page design update), or route templates through the alias path with guidance.
- **Expected outcome:** Open decision. Owner: ADV / Data Team.
- **Worked example:** Consultant iterates 'Client_MSA_template_v3.docx' three times to harden it before a tender. Grouping: template 'Client MSA 2026'; no supplier ever attached.
