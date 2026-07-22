---
type: review
status: draft
owner: design-system
surfaces: [Connected Platform]
platform: connected-platform
source: user-provided
last_reviewed: 2026-06-29
maturity_score: 0
tags: [orbit, design-brain, personas, connected-platform, wip, review]
---

# Connected Platform personas — working file (WIP)

Staging for the 4 real Connected Platform personas (owner-provided 2026-06-29).
- **Section A** — distilled **trait → design consequence** blocks (red-lined). Written into
  `design-brain/platforms/connected-platform.md` (replacing the 3 provisional `[CONFIRM]`
  personas) once all 4 are confirmed.
- **Section B** — **parked test protocols** (raw harness inputs). Built into a
  `_benchmarks/` persona-evaluation harness once all 4 are done (one coherent artifact).
- Delete this WIP file after both are promoted.

Progress: **2 / 4 confirmed** (Delivery Project Lead, Hands-On Senior Consultant).
⏸️ **Paused 2026-06-29** — Personas 3 & 4 not ready. **Resume by pasting Persona 3.** Nothing is written to `connected-platform.md` until all 4 are confirmed.

---

## Section A — Distilled persona blocks (for the profile)

### Persona 1 — Delivery Project Lead — Manager / PM / Principal ✅ CONFIRMED 2026-06-29
*(internal Efficio; leads delivery across multiple client engagements)*
- Starts the day scanning RAG and wants every initiative's health in <5 min → **portfolio health is the default landing surface; RAG / status / owner / dates / savings and "needs-attention" exceptions visible at a glance, not behind clicks.**
- Pragmatic adopter who reverts to Excel when the platform adds friction → **the common path must beat Excel on speed: minimal setup, fast scanning, no mandatory ceremony; allow flexibility for non-standard work.**
- Chases consultants for stale RAG/savings updates → **surface staleness/overdue items and prompt for them — design for data-freshness visibility, not manual chasing.**
- Accountable for DPIA + regional AI-usage rules (KSA vs ROW), checked before deliverables ship → **show governance/compliance constraints inline at point of use; make each AI tool's permitted/restricted state explicit in context.**
- Reports to Principals and clients; must look credible → **progress/savings views presentation-ready; states honest (no fake success) since outputs face clients.**
- New-project setup feels overwhelming; wants permissions without Principal hand-offs → **progressive disclosure + smart defaults on setup; self-serve role assignment at PM tier.**

### Persona 2 — Hands-On Senior Consultant — Analyst / Senior Analyst / Senior Consultant ✅ CONFIRMED 2026-06-29
*(internal Efficio; runs multiple initiatives day-to-day, drafts deliverables under deadline)*
- Asks "what's my next step?" rather than reading methodology; success = "I always know my next mandatory step"; wants to avoid rework from missed steps → **each active initiative surfaces its single next mandatory action up front (incl. QC/gate requirements before submission); lead with the next required step — methodology is disclosed on demand, not the landing content.**
- Heavy-edits AI outputs before they're deliverable-ready (esp. RFP Builder) → **AI tool outputs must be submission-ready and structured for edit-in-place — design for minimal-edit handoff, not raw prose drafts the consultant has to rewrite.**
- Duplicates tracking across Excel and the platform → **status / savings / tracking captured once and reused across initiative updates and client outputs — no re-keying between platform and Excel.**
- Blocked by missing day-one permissions and unpredictable client AI restrictions → **show permissions state and the client's AI Green/Amber/Red classification up front and in context at point of tool use — permitted/restricted explicit before work begins.** *(shared consequence with Persona 1 — governance/AI-state at point of use)*
- Loses time to low discoverability, too many clicks, inconsistent UI → **tools and next actions reachable in few clicks with consistent patterns; minimise navigation depth.**
- Early-adopter power user (Promoter) who still falls back to Excel/PowerPoint → **the in-platform path must be faster than dropping to external tools — fast paths, no hand-holding ceremony — or the power user leaves.**
- *Cut:* "mentoring juniors / flags bottlenecks" — no distinct design consequence.

### Persona 3 — _pending_
### Persona 4 — _pending_

---

## Section B — Parked test protocols (raw harness inputs)

> The **generic test wrapper** (how-to-test stance, "while testing pay attention to…", per-task
> report format, and end deliverables: top-5 usability issues / adoption risks / missing
> features / trust-blockers / changes-to-make) is **shared across all personas** — capture it
> ONCE when building the harness. Below, only the **persona-specific** inputs are parked.

### Persona 1 — Delivery Project Lead (Manager / PM / Principal)
- **Success criterion:** "I can see the health of every initiative I own in under five minutes and know exactly what needs my attention."
- **Tech comfort / stance:** High; pragmatic *passive* adopter — uses it when it clearly helps, else reverts to familiar tools (Excel).
- **Targeted tools / product areas (AI & Tools Centre):** Efficio Consulting Partner; Public Sector Procurement Regulations Advisor; RFP Analytics; ClauseIQ; Strategy Advisor (G1); AI Category Briefing; Contract Management Companion; Fleet Market Briefcase; RFP Builder; Efficio Butler Model; Efficio RFP Helper.
- **Hypotheses to VALIDATE (not design facts — probe, don't assert):** portfolio-level health view as default landing; automated status nudges instead of manager chasing; region-specific AI guidance inline at point of use; self-serve permissions at PM tier.
- **Task pack:**
  1. Set up / review a new sourcing project from scratch — scope, client, workstreams, team permissions.
  2. Check team roles, permissions and ownership across the project — confirm who can do what.
  3. Review milestones, deliverables, RAG status and savings progress for ≥2 initiatives.
  4. Check whether the platform actively prompts consultants to keep RAG / savings / status / deliverables / required updates current.
  5. Review how AI tool usage is governed by client DPIA and regional (KSA vs ROW) restrictions, and whether those rules are visible at point of use.
  6. Assess whether the portfolio dashboard gives instant project-health visibility without manually chasing the team.
  7. Use assigned tools (ClauseIQ, RFP Analytics, RFP Builder, Strategy Advisor G1, AI Category Briefing) to spot-check QC and AI-assisted deliverables on an active initiative.
  8. Flag anything that creates delivery admin, compliance risk, weak ownership, or poor project control.

### Persona 2 — Hands-On Senior Consultant (Analyst / Senior Analyst / Senior Consultant)
- **Success criterion:** "I always know my next mandatory step and the AI tools save me real time instead of creating rework."
- **Tech comfort / stance:** High; **Promoter** — early-adopter, willing to push the tool hard. Lives in the platform but still drafts in Excel/PowerPoint.
- **Targeted tools / product areas (AI & Tools Centre):** Commodity Price Watch; RFP Capability Analyser; BeroeLive AI; ChatGPT Prompt Generator; Strategy Doc. Reviewer (G1); RFP Analytics; ClauseIQ; Strategy Advisor (G1); AI Category Briefing; RFP Builder; Efficio Butler Model; Efficio RFP Helper.
- **Hypotheses to VALIDATE (not design facts — probe via interaction, don't assert):** lead with the next required action over full methodology; RFP Builder output quality good enough that consultants edit less; client AI Green/Amber/Red classification shown in context; platform↔Excel tracking duplication reduced.
- **Task pack:**
  1. Run / progress a sourcing initiative end-to-end inside the platform.
  2. Use assigned tools (ClauseIQ, RFP Builder, RFP Capability Analyser, RFP Analytics, Commodity Price Watch, BeroeLive AI, AI Category Briefing, ChatGPT Prompt Generator, Strategy Advisor G1) to complete ≥1 realistic supplier / category / RFP / market analysis task.
  3. Prepare a supplier / category / RFP / market analysis suitable for a client deliverable.
  4. Update initiative status, savings assumptions and supporting deliverables.
  5. Critically evaluate whether AI tool outputs are accurate and submission-ready, or need heavy rewriting.
  6. Identify any duplication between in-platform analysis, initiative updates and client-facing outputs.
  7. Flag anything that would push you back to Excel, PowerPoint or external tools instead of the platform.

<!-- graph-links:start — generated by tools/gen_graph_links.py; do not hand-edit -->
## Vault graph
[[design-brain/platforms/connected-platform|connected-platform]]
<!-- graph-links:end -->
