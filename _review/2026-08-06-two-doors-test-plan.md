---
type: review
status: draft
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-08-06
maturity_score: 0
tags: [orbit, design-brain, intake, concept-desk, test-plan]
---

# Testing the two doors — a script you can follow

> **Part A** pushes a throwaway concept through both doors so you can see every artifact
> appear, then deletes it. About 45 minutes. **Part B** does it for real.
>
> Every step says what to do, what to expect, and **how to verify** — the file that must
> exist and the stage chip that must light. If a step does not behave as written, that is a
> finding: record it rather than working around it.
>
> **This script has been executed end to end**, not just written — see the verification
> record at the end of Part A for exactly what was confirmed.

## Before you start

```
cd <your vault checkout>
git pull
python3 tools/vault_health.py
```

Open `HEALTH.md`, find **## Concepts in flight**. You should see two rows (the RAID
concept and the initiatives tracker). That table is your instrument panel for the whole
test — after every step you regenerate and read it again.

The five stages are **Briefed → Gated → Explored → Defined → Ported**. A stage lights
**only** when the file that proves it exists. Prose never lights a chip; that is the point.

---

# Part A · Dry run

Synthetic concept, deleted at the end. Slug used throughout: `test-supplier-alerts`.

## A1 · Door 1 — coach an idea into a brief

**Do:** open your Brief Coach (Claude Project, or paste
`design-brain/projects/brief-coach-anytool.md` into any assistant). Give it a rough idea —
deliberately vague, so you can watch it narrow. For example:

> "Buyers keep missing when a supplier's risk score changes. We should alert them somehow —
> maybe email, maybe in the app, maybe a digest."

Answer its questions honestly. It should push you toward **one** user, **one** moment, and
**one** countable outcome, and refuse to tell you whether the brief will pass.

**Expect:** a played-back brief in the shape of `discovery/briefs/_TEMPLATE.md`, plus a list
of things you did not know — those become the gap report.

**Do next:** save it as **discovery/briefs/&lt;today&gt;-test-supplier-alerts.md**, using
`discovery/briefs/_TEMPLATE.md` for the frontmatter. Set `status: draft`, and leave the gate
log with a single unsubmitted row:

```
| Date | Verdict | By | Notes / gaps / override reason |
| ---- | ------- | -- | ------------------------------ |
| — | not yet submitted | — | Dry run |
```

**Verify:**
```
python3 tools/lint_frontmatter.py     # must pass — catches a malformed brief immediately
python3 tools/vault_health.py
grep -A6 "Concepts in flight" HEALTH.md
```
A third row appears: **Briefed ✅, everything else –**, gate reads *Not yet submitted*.

> If lint fails, the brief's frontmatter is wrong — fix it now. Every later step assumes a
> well-formed brief.

## A2 · The gate — a blind verdict

**Do:** open your Brief Reviewer — a **different** Project, or at minimum a **brand-new
chat**. Never continue the coaching conversation. Paste the brief and ask for a verdict.

**Expect:** a verdict of **Ready / Needs work / Blocked** scored against eight criteria,
with specifics. A first-time "Needs work" is normal and is not a failure — it is the
cheapest possible failure.

**Do next:** log it in the brief's `## Gate log`:

```
| 2026-08-06 | Ready | brief-reviewer (dry run) | All eight pass. Dry run. |
```

Set `status: stable` if Ready (the frontmatter `status` tracks gate position:
draft → in-review → stable).

**Verify:**
```
python3 tools/vault_health.py && grep -A6 "Concepts in flight" HEALTH.md
```
The row now reads **Briefed ✅ Gated ✅**, gate column shows *Ready*.

> **Try this** — it proves the verdict is read by date, not by position: add a second row
> dated *earlier* with a different verdict. The table still shows the latest one.

## A3 · Explore — a prototype that gets kept

**Do:** in Claude Code, `/explore discovery/briefs/2026-08-06-test-supplier-alerts.md`.
For the dry run you can also hand-write a minimal HTML file — the point is the archiving
step, not the prototype's quality.

**Do next — this is the step that used to get skipped:**

```
mkdir -p discovery/prototypes/test-supplier-alerts
# put the prototype at discovery/prototypes/test-supplier-alerts/prototype.html
# write record.md from discovery/prototypes/_TEMPLATE-record.md
```

In the record file, the `brief:` key must point at the brief **in backticks** — that link is
what lights the *Explored* chip, and the link checker validates it for you.

**Verify:**
```
python3 tools/check_links.py          # proves the brief: link resolves
python3 tools/vault_health.py && grep -A6 "Concepts in flight" HEALTH.md
```
**Briefed ✅ Gated ✅ Explored ✅.**

### A3b · Negative check — prove the guard is real

```
mv discovery/prototypes/test-supplier-alerts/prototype.html /tmp/held.html
python3 tools/vault_health.py && grep -A20 "Concepts in flight" HEALTH.md
```
A gap line appears naming the record whose prototype is missing. **This is the honesty
check working** — a record pointing at a file that is not there is reported, not rendered
as if everything were fine. Restore it and regenerate:
```
mv /tmp/held.html discovery/prototypes/test-supplier-alerts/prototype.html
python3 tools/vault_health.py
```
The gap disappears.

## A4 · Define — behaviour agreed in Excel

Only for a **Ready** concept. In Claude Code: `/define <the Ready brief>`, or drive it by
hand:

```
python3 tools/matrix_xlsx.py template -o test-supplier-alerts.xlsx
```

Open that workbook. Five tabs: **Meta, Rules, Clarifications, Green Path, Edge Paths**.
Fill in a minimum viable matrix — one rule, one clarification, one green scenario, one edge
scenario. Two things must be right or the import will refuse:

- **Meta → `meta_line`** must carry the source brief in backticks. This is the field that
  lights the *Defined* chip:
  **Source Concept Pack:** followed by your brief's path in backticks
- **Every scenario needs all nine fields.** Subtitle, Rules, Starting state, User actions,
  Backend, Front-end result, Next action, Expected outcome, Worked example. The importer
  names any you miss.

```
python3 tools/matrix_xlsx.py import test-supplier-alerts.xlsx \
  -o discovery/definition/test-supplier-alerts.md
python3 tools/build_journey_flows.py discovery/definition/test-supplier-alerts.md \
  -o artifacts/test-supplier-alerts-journey-flows.html
```

Open that HTML in a browser: tabbed journey flows, one expandable card per scenario.

**Verify:**
```
python3 tools/vault_health.py && grep -A6 "Concepts in flight" HEALTH.md
```
**Briefed ✅ Gated ✅ Explored ✅ Defined ✅** — Ported still shows *not yet*, honestly,
because nothing has been built.

> **Try this** — type a line break inside a scenario cell (Alt+Enter) and re-import. It
> refuses and names the cell. Excel line breaks cannot survive the markdown round trip, so
> they are caught at the door rather than silently corrupting the file.

## A5 · Negative check — the link guard

```
# in the brief's ## Graduation section, set:
#   - **Discovery pack:** point it at a file that does not exist (in backticks)
python3 tools/check_links.py     # FAILS — names the broken reference
```
This is why a dangling handoff cannot reach main. Revert it to `not yet`.

> Note the deliberate design: prose like ``not yet — blocked on `TBD` `` does **not** mark a
> concept as Ported. Only a real `discovery/…md` path counts.

## A6 · Door 2 — a prototype arrives with no brief

**Do:** take any prototype — a Lovable export, an old HTML mock, anything — and open your
Brief Coach. This time say:

> "I've already built this. Can you work out what the brief should have been?"

**Expect:** the coach reads the prototype as a set of **claims**, extracts what it can, and
marks every extracted section *"confirm with owner"*. What no UI can answer becomes a
**typed gap report** — each gap typed as `edge case`, `open question`, `risk`, or
`duplication`, each with a suggested owner.

**Verify:** the typing is not decoration — it is routing. Edge cases become E-rows in the
Definition Pack; open questions become C-items with owners. Compare against the worked
example: `discovery/briefs/2026-07-31-initiatives-tracker-reverse-brief.md`.

Save it as a brief with the `reverse-brief` tag in frontmatter, then:
```
python3 tools/vault_health.py && grep -A8 "Concepts in flight" HEALTH.md
```
The new row's Door column reads **Door 2 · prototype-first** — derived from that tag.

> A Door 2 brief legitimately stops at "not yet submitted" until its owner confirms the
> extracted sections. That is the process, not a stall.

## A7 · Clean up

```
rm discovery/briefs/2026-08-06-test-supplier-alerts.md
rm -rf discovery/prototypes/test-supplier-alerts
rm discovery/definition/test-supplier-alerts.md
rm -f artifacts/test-supplier-alerts-journey-flows.html test-supplier-alerts.xlsx
# plus the Door 2 dry-run brief if you saved one
python3 tools/gen_graph_links.py
python3 tools/vault_health.py
grep -A6 "Concepts in flight" HEALTH.md      # back to the original rows
python3 tools/check_links.py && python3 tools/lint_frontmatter.py
```

If anything was committed during the dry run, `git checkout` the generated files too —
`HEALTH.md`, `vault-health.html`, `tools/health_history.json` regenerate constantly and are
not worth committing from a rehearsal.

## Verification record

Part A was run start to finish in a throwaway clone on 2026-08-06, following this document
literally. Confirmed:

| Step | Claim | Result |
| --- | --- | --- |
| A1 | A new brief appears as **Briefed ✅**, gate *Not yet submitted* | as written |
| A2 | Logging a Ready row lights **Gated ✅** | as written |
| A2 | An *earlier-dated* row does not override the latest verdict | as written — still Ready |
| A3 | A record whose `brief:` resolves lights **Explored ✅** | as written |
| A3b | Removing the prototype html produces a named gap line | as written |
| A3b | Restoring it clears the gap | as written |
| A4 | `template` emits Meta / Rules / Clarifications / Green Path / Edge Paths | as written |
| A4 | A filled workbook imports and lights **Defined ✅** | as written |
| A4 | A line break in a scenario cell is refused, naming the cell | as written |
| A5 | A Graduation link to a missing file fails `check_links.py` | as written |
| A5 | Prose like ``not yet — blocked on `TBD` `` does **not** mark Ported | as written |
| A6 | The `reverse-brief` tag renders **Door 2 · prototype-first** | as written |
| A7 | Cleanup restores the original rows; all five checks pass | as written |

The only steps not machine-verified are the ones that need a person: the coaching
conversation (A1), the blind verdict (A2), and the reverse-brief interrogation (A6). Those
are judgement, not machinery — which is exactly why they are the parts worth your time.

---

# Part B · The real thing

Same walk, three differences:

1. **A real idea from a real person.** The playbook is explicit: not a made-up test case —
   an actual thing they wish existed. Made-up ideas produce made-up gaps.
2. **No cleanup.** The artifacts stay; that is the point. The brief in `discovery/briefs/`
   *is* the registry card, the fifth Concept Pack item.
3. **Hand the pack back.** Give the stakeholder all five: brief, verdict, typed gap report,
   working prototype, and where it lives. Then say what happens next — who owns which open
   question, and what would move it to Define.

Log what you learn while it is fresh: how long each stage took, what the coach surfaced
that the form would not have, and whether the gate caught anything real. That is the
readout evidence, and it evaporates within a day.

---

# Appendix · What good looks like

Recognising a bad output matters as much as producing a good one.

**A gate log row** — dated, attributed, specific about what failed:
```
| 2026-07-21 | Needs work | brief-reviewer (opus, fresh context) | FAIL on criteria 2, 3, 4, 8. Four bets bundled; situation and outcome too broad. Narrow to the single highest-evidence bet. |
```

**A typed gap** — routed, owned, honest about what a prototype cannot say:
```
| 4 | open question | Savings-variance column: where does the number come from, who maintains the calculation? | Data team |
| 6 | risk | The prototype shows every value to everyone. Who must *not* see savings figures? | Owner + platform |
```

**A prototype record** — provenance stated, verification stated:
> Reconstruction, owner-approved — the original was session-private and is unrecoverable;
> rebuilt to the brief's recorded feature list. Verified: filters, diff toggle, tray, both
> themes, clean console.

**A clarification** — an unresolved decision carried as a first-class row, not quietly
resolved:
```
### C2 · Template review mode
Dedicated mode, or routed through the alias path? Owner: ADV / Data team.
```

## Signals something is wrong

| You see | It means |
| --- | --- |
| Every criterion passes first time, no conditions | The reviewer saw the coaching, or is being agreeable. Use a fresh chat |
| A gap report with no owners | Gaps that land nowhere are notes, not findings |
| A stage chip lights with no file | Cannot happen — chips are derived. If you believe it did, that is a bug worth reporting |
| A gap line under "Concepts in flight" | Something points at a file that is not there. Fix the reference, not the dashboard |
| The reviewer invents platform context | It should say "cannot verify" instead. Model quality issue — spot-check that tool's verdicts |

<!-- graph-links:start — generated by tools/gen_graph_links.py; do not hand-edit -->
## Vault graph
[[design-brain/projects/brief-coach-anytool|brief-coach-anytool]] · [[discovery/briefs/2026-07-31-initiatives-tracker-reverse-brief|2026-07-31-initiatives-tracker-reverse-brief]] · [[discovery/briefs/_TEMPLATE|briefs _TEMPLATE]]
<!-- graph-links:end -->
