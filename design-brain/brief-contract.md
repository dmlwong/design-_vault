---
type: governance
status: draft
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-07-21
maturity_score: 0
tags: [orbit, design-brain, intake, brief, governance, explore]
---

# Brief Contract — the standard a concept brief must meet

> The written standard the intake gate checks against, so a brief is judged consistently
> and the judgement is auditable. A brief is the structured intent captured at intake
> (via `tools/intake-form.html`) that seeds the `explore` skill. This contract is to a
> brief what a component contract is to a component: the bar it is measured against.
> **Draft** — piloted, not yet promoted. See the proposal:
> `_review/2026-07-21-context-first-intake-proposal.md`.

## Why the gate exists

A brief that is vague, a solution in disguise, or missing context does not produce a
worse prototype — it produces a *convincing* one built on the wrong premise, which costs
more downstream than a rejected brief. The gate catches that at the cheapest point:
before generation. Governance here means a **written standard, a recorded verdict, and a
named owner** — not a locked door.

## Two layers

- **Layer 1 — completeness (a rule).** Deterministic, in the intake form's browser JS
  (and later a committed-brief linter in CI): required fields present, platform is a valid value,
  journey has real steps, no placeholder or too-short text. Catches empty and malformed
  briefs for free. Cannot judge quality.
- **Layer 2 — the review (judgement).** The `brief-reviewer` agent
  (`design-brain/agents/brief-reviewer.md`) scores the brief against the eight criteria
  below and returns a verdict. It reviews the **input**, before anything is built — the
  upstream sibling of `design-reviewer`, which reviews the output.

**Two roles, one contract (a firewall).** The same eight criteria are used two ways by two
*separate* agents. `brief-coach` (`design-brain/agents/brief-coach.md`) helps a stakeholder
*write* a strong brief — Socratic, drawing their own answers out, never a verdict.
`brief-reviewer` then *judges* it independently, blind to the coaching. The same agent must
never both coach and judge the same brief, or the gate passes what it authored. The rules say
what's wrong; the coach helps make it right; the reviewer confirms — separately.

## The eight criteria

Each criterion is PASS or FAIL with quoted evidence from the brief. A criterion that the
brief does not give enough to judge is a FAIL (missing is not passing).

1. **Problem, not solution.** States a user problem, not a pre-chosen feature.
   - Good: "reviewers can't tell which contract clauses changed between rounds."
   - Red flag: "add a diff filter" (a solution — it forecloses the exploration).
2. **One primary user and moment.** A single user in a specific situation.
   - Red flag: "all users", "everyone in procurement".
3. **One testable bet.** A single core flow to prototype.
   - Red flag: five journeys bundled into one ask — `explore` can only test one.
4. **Falsifiable outcome.** Success is observable or measurable.
   - Good: "reviewer spots every changed clause in under a minute."
   - Red flag: "make it more intuitive", "improve the experience".
5. **Evidence over appeal.** Grounded in a real signal, not novelty.
   - Red flag: "a competitor has it", "would be cool".
6. **Scope is fenced.** At least one explicit non-goal.
   - Red flag: unbounded — everything is in scope, so nothing can be cut.
7. **Feasibility acknowledged.** Constraints named, or unknowns flagged.
   - Red flag: assumes data, an integration, or a permission that does not exist.
   - **Ceiling note:** this criterion is only as strong as the tech reality in the vault.
     Until the Efficio Context Pack lands, the reviewer judges *whether feasibility was
     considered*, and says plainly when it cannot verify buildability.
8. **Context sufficiency.** The vault (or the brief) supplies enough to build well.
   - Red flag: needs context the vault lacks → the reviewer routes a gap to the Context
     Pack backlog rather than guessing.

## Verdicts

The verdict maps to the brief's `status`, so the file itself records where it is in the gate.

| Verdict | Meaning | Brief `status` | What happens |
| ------- | ------- | -------------- | ------------ |
| **Ready** | All eight pass (or a logged override). | `stable` | Proceeds to `explore`. |
| **Needs work** | Fixable gaps on one or more criteria. | `in-review` | Returns to the requester with the specific gaps and suggested rewrites — the common early outcome. Fix in the form (Import → edit → regenerate) and resubmit. |
| **Blocked** | Fundamental — not a real problem, or missing feasibility/context that cannot be resolved by rewording. | `in-review` | Escalates to a human owner; may spawn a Context Pack task. |

## Operations — whose job the gate is

- Briefs arrive from the form to the **design-team intake owner** (a named person, not a
  rota-of-nobody). Any design-team member may run the review.
- The review is triggered **manually** in a Claude Code session (the `brief-review` task
  in `design-brain/routing.json`). It is deliberately **not** wired to CI — same rule as
  lessons-inbox triage: no API secrets in the pipeline until the owner decides otherwise.
- **Turnaround target: 2 working days** from submission to verdict.
- Every verdict and any override is logged in the brief's `## Gate log` section.

## Human override

A verdict is advice with authority, not a wall. The **product owner or design-system
owner** may override a `Needs work`/`Blocked` verdict and let a brief proceed — the
override and its reason are recorded in the brief's `## Gate log`. Accountability, not a
locked door.

## Graduation — a Ready brief does not die

When a concept clears `explore` and the team wants to take it forward, the brief **seeds
the full discovery pack** (`discovery/_TEMPLATE.md`): its fields map onto pack sections
(problem statements, user journeys, goals & success criteria), and the pack links back to
the brief. One intake format flowing forward — not a second, disconnected one.

## Related

- `discovery/briefs/_TEMPLATE.md` — the brief template the form fills.
- `tools/intake-form.html` — the intake form (Layer 1 + brief generation).
- `design-brain/agents/brief-coach.md` — the coach that helps a stakeholder meet this standard.
- `design-brain/agents/brief-reviewer.md` — the Layer 2 reviewer.
- `design-brain/skills/explore/SKILL.md` — what a Ready brief feeds.
- `_review/2026-07-17-efficio-context-pack-proposal.md` — the context that lifts the
  feasibility ceiling (criterion 7).

<!-- graph-links:start — generated by tools/gen_graph_links.py; do not hand-edit -->
## Vault graph
[[_review/2026-07-17-efficio-context-pack-proposal|2026-07-17-efficio-context-pack-proposal]] · [[_review/2026-07-21-context-first-intake-proposal|2026-07-21-context-first-intake-proposal]] · [[design-brain/agents/brief-coach|brief-coach]] · [[design-brain/agents/brief-reviewer|brief-reviewer]] · [[design-brain/skills/explore/SKILL|explore SKILL]] · [[discovery/_TEMPLATE|discovery _TEMPLATE]] · [[discovery/briefs/_TEMPLATE|briefs _TEMPLATE]]
<!-- graph-links:end -->
