---
type: review
status: draft
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-08-06
maturity_score: 0
tags: [orbit, design-brain, intake, concept-desk, rollout]
---

# Concept Desk — rollout plan

> The pipeline is built and merged. This is the plan for putting it in people's hands.
> It assumes nothing is installed anywhere yet.
>
> **Read the test plan first:** `_review/2026-08-06-two-doors-test-plan.md`. Phase 0 below
> is that document. Do not provision for other people until you have walked both doors
> yourself — you cannot support what you have not run.

## What is ready

Every claim here has a file behind it. If a row's file is missing, the row is a lie.

| Capability | Proof on disk |
| --- | --- |
| Coached brief (Door 1) | `design-brain/agents/brief-coach.md` |
| Reverse-brief from a prototype (Door 2) | same file — "Reverse-brief mode" section |
| Blind gate, eight criteria | `design-brain/agents/brief-reviewer.md` · `design-brain/brief-contract.md` |
| Explore → a working prototype | `design-brain/skills/explore/SKILL.md` |
| Prototypes kept, not lost | `discovery/prototypes/_TEMPLATE-record.md` (worked: `discovery/prototypes/raid-status-prep/record.md`) |
| Define → journey matrix + flows | `design-brain/skills/define/SKILL.md` · `tools/matrix_xlsx.py` |
| Port onto the design system | `design-brain/skills/port-to-orbit/SKILL.md` |
| Live per-concept tracking | "Concepts in flight" in `HEALTH.md` — generated, never hand-edited |
| Runs on any assistant | `design-brain/projects/brief-coach-anytool.md` · `design-brain/projects/brief-reviewer-anytool.md` |
| Six automated guards | `.github/workflows/vault-integrity.yml` |

**The five-item Concept Pack** — brief, verdict, typed gap report, working prototype,
registry card — is identical from either door. A cleared concept then earns a **Definition
Pack**: the journey matrix (authored in Excel) and the user flows generated from it.

## Phase 0 · Rehearse it yourself

**Before anyone else is involved.** Follow `_review/2026-08-06-two-doors-test-plan.md`
Part A: push a synthetic concept through both doors, watch each artifact appear, run the
negative checks, delete it. About 45 minutes. You will then know exactly what a stakeholder
sees, and what a broken run looks like.

## Phase 1 · Provision — once, ~20 minutes

### 1.1 Decide who is on which tool

| They use | They need | Setup time |
| --- | --- | --- |
| Claude | `design-brain/projects/brief-coach-project.md` pasted into a Claude Project | ~5 min each, once |
| Codex **with repo access** | nothing — it reads `AGENTS.md` and the agent specs directly | none |
| Codex **without repo access** | `design-brain/projects/brief-coach-anytool.md` pasted into a chat | per session |
| ChatGPT | the same `-anytool` file in a Project or custom GPT | ~5 min, once |
| Copilot | the `-anytool` file attached in chat, or added as repo instructions | per session, or once |
| No AI at all | the intake form on the team site — nothing else | none |

> **The Codex caveat, stated plainly.** "Zero setup" holds only if the person has a repo
> that contains the brain — this vault, or a product repo someone has exported it into.
> `tools/export_brain.py` is **not** wired into CI (the drift-check step in
> `.github/workflows/vault-integrity.yml` is still commented out pending product-repo
> access), so a product repo has the brain only if it was exported by hand. If in doubt,
> give them the `-anytool` file; it always works.

### 1.2 Set up the two roles

Coach and reviewer, **separately**. Claude: two Projects. Any other tool: two chats, or a
Project/GPT each. Whatever the tool, the rule is the same and it is not negotiable:

> The assistant that coaches a brief must never be the one that judges it. A reviewer that
> saw the coaching approves what it helped write, and the gate becomes theatre.

Optionally add `design-brain/platforms/*.md` to the reviewer's knowledge so criterion 8 is
checked against real platform context instead of guessed.

### 1.3 Confirm the tester path works

Open the team site, click **Concept Brief Intake**, type one line, hit **Download .md**.
If a file lands in your downloads, a stakeholder with no AI access can still enter the
pipeline. Test this even if you expect everyone to use the coach — it is the fallback.

### 1.4 Name the intake owner and the clock

One person runs the reviewer and replies **within two working days**. It can be you.
Without a named owner, briefs pile up and the pilot stalls quietly rather than loudly.

## Phase 2 · Pilot — weeks 1–2

- **2–3 people, each with a real, current idea.** Not a made-up test case; a genuine thing
  they wish existed. That is what stresses the pipeline honestly.
- **Mix coached and cold.** Some use the coach first, some fill the intake form straight.
  Comparing the two is the single most useful piece of data the pilot produces.
- **One concept through each door.** At least one idea-first, at least one that arrives as
  an existing prototype — Door 2 is the one people do not expect to work.
- **Every pack handed back inside 48 hours.** If you cannot hold that, say so up front and
  set a different number; a missed promise costs more than a slower one.

## Phase 3 · Readout — week 4

Put the coached and the cold brief side by side and answer four questions:

1. Did the packs land inside 48 hours?
2. Did the gate catch at least one thing that would otherwise have reached the build team?
3. Did every open question leave with a **named owner**?
4. Was the registry checked for duplication before work started?

Then decide: keep, adjust, or stop. The evidence decides, not the enthusiasm.

## Success criteria

The rollout has worked if, at the readout:

- [ ] Both packs delivered inside the promised window
- [ ] ≥1 gap caught that would otherwise have reached the build team
- [ ] Every open question in every gap report carries a named owner
- [ ] Duplication checked against the registry for both concepts
- [ ] At least one participant used a non-Claude tool and got a usable result
- [ ] "Concepts in flight" shows every pilot concept at its true stage

## Known gaps — say these out loud

Do not let anyone discover these on their own.

- **Door 2's worked example is mid-flight by design.** The initiatives-tracker reverse
  brief (`discovery/briefs/2026-07-31-initiatives-tracker-reverse-brief.md`) reads "not yet
  submitted" because it needs its owner to confirm the sections a prototype cannot answer.
  That is the process working, not a defect — but it means the demo's Door 2 arc stops at
  the handback.
- **The RAID concept is deliberately blocked.** Its own critique says do not proceed until
  two questions come back green from a real PM session. It stays at *Explored*.
- **Judgement quality varies by model.** The specs port cleanly to any assistant; the
  reviewer is the one making a call. Spot-check a couple of verdicts from a new tool
  against a known-good one before trusting them equally. An honest "cannot verify" is a
  good sign; invented context is not.
- **The demo page still has a placeholder.** Door 2's "before" image is missing until the
  original Lovable screenshot is supplied.
- **Regenerate after editing a spec.** If `brief-coach.md` or `brief-reviewer.md` changes,
  run `tools/build_project_bundles.py` and re-paste into any Project or GPT already
  configured. Pasted copies do not update themselves.

## If it stalls

| Symptom | Most likely cause | Fix |
| --- | --- | --- |
| Briefs stop arriving | No named intake owner, or the 48h promise slipped | Re-name the owner; publish the actual turnaround |
| Every brief comes back "Needs work" | Testers skipping the coach | That is the finding — it is the coached-vs-cold comparison, not a failure |
| A stage chip never lights | The artifact was delivered but not archived | Only files light chips; check the gap list under "Concepts in flight" |
| Stakeholders route around the desk | The desk felt slower than building | Shorten the promise or narrow the pilot; do not add process |

<!-- graph-links:start — generated by tools/gen_graph_links.py; do not hand-edit -->
## Vault graph
[[AGENTS|AGENTS]] · [[_review/2026-08-06-two-doors-test-plan|2026-08-06-two-doors-test-plan]] · [[design-brain/agents/brief-coach|brief-coach]] · [[design-brain/agents/brief-reviewer|brief-reviewer]] · [[design-brain/brief-contract|brief-contract]] · [[design-brain/projects/brief-coach-anytool|brief-coach-anytool]] · [[design-brain/projects/brief-coach-project|brief-coach-project]] · [[design-brain/projects/brief-reviewer-anytool|brief-reviewer-anytool]] · [[design-brain/skills/define/SKILL|define SKILL]] · [[design-brain/skills/explore/SKILL|explore SKILL]] · [[design-brain/skills/port-to-orbit/SKILL|port-to-orbit SKILL]] · [[discovery/briefs/2026-07-31-initiatives-tracker-reverse-brief|2026-07-31-initiatives-tracker-reverse-brief]] · [[discovery/prototypes/_TEMPLATE-record|_TEMPLATE-record]] · [[discovery/prototypes/raid-status-prep/record|record]]
<!-- graph-links:end -->
