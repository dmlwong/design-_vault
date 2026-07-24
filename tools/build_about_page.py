#!/usr/bin/env python3
"""Generate ``artifacts/about-the-vault.html`` from ``tools/about-template.html``.

The "About the Orbit Vault" explainer is a *generated projection*, like the health
page and DESIGN.md — so the counts, the agent roster, and the status mix can never
drift from the vault the way the three hand-authored decks it replaces did (they
claimed 8 agents / 97 docs when reality was 10 / 139).

Live facts come from the same source as the health dashboard (the latest entry in
``tools/health_history.json``, written by ``tools/vault_health.py``) and from the
agent frontmatter (``design-brain/agents/*.md``) — so a new agent appears here
automatically, on its real model tier, with no code change.

Two build-time guards make the drift fix *structural*: the generator fails loudly
if (a) any ``{{token}}`` is left unresolved, or (b) any banned stale claim survives
in the output. A later template edit cannot silently reintroduce "8 agents" / "97"
/ "~85/100" without breaking the build.

    python3 tools/build_about_page.py
"""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import lint_frontmatter as lf  # noqa: E402  (reuse the frontmatter parser)

ROOT = lf.ROOT
TEMPLATE = ROOT / "tools" / "about-template.html"
HISTORY = ROOT / "tools" / "health_history.json"
AGENTS_DIR = ROOT / "design-brain" / "agents"
OUT = ROOT / "artifacts" / "about-the-vault.html"

# Editorial one-liners per agent. Facts (tier, status, existence) come from
# frontmatter; only this prose is curated. A new agent with no blurb still renders
# (its humanized `type` is the fallback), so the roster never breaks or omits one.
ROLE_BLURBS = {
    "context-scout": "Assembles the context packet — which files, which platform, which agent a task needs.",
    "vault-librarian": "Link checks, metadata lint, staleness sweeps; triages the corrections inbox.",
    "contract-extractor": "Reads real source code and writes the component contract for it.",
    "component-builder": "Builds or refactors one component to its written contract.",
    "screen-builder": "Composes multi-component screens from the page patterns.",
    "porter": "Ports external / Lovable prototypes onto Orbit tokens and components.",
    "design-reviewer": "Judges finished work against the brain — fresh eyes, never grading its own build.",
    "benchmark-judge": "Blind A/B scoring for quality benchmarks — the scoring-integrity gate.",
    "brief-coach": "Draws a testable concept brief out of a stakeholder through questions — never judges it.",
    "brief-reviewer": "Independently gates a concept brief against the contract, blind to the coaching.",
}

TIER_RANK = {"haiku": 0, "sonnet": 1, "opus": 2}

# Strings that would mean the page has gone stale again. Checked case-sensitively
# against the final output; any hit fails the build.
BANNED = [
    "Eight specialist", "eight specialist", "8 agents", "8 AI agents",
    "97 ", "~85", "85 / 100", "85/100", "13 heuristics", "13 interaction",
    "weekly staleness",
]


def latest_health() -> dict:
    data = json.loads(HISTORY.read_text(encoding="utf-8"))
    if not data:
        raise SystemExit("health_history.json is empty — run tools/vault_health.py first.")
    return data[-1]


def build_roster() -> str:
    agents = []
    for path in sorted(AGENTS_DIR.glob("*.md")):
        fm = lf.parse_frontmatter(path) or {}
        name = fm.get("name", path.stem)
        model = (fm.get("model") or "sonnet").strip().lower()
        status = (fm.get("status") or "").strip()
        atype = (fm.get("type") or "").strip()
        role = ROLE_BLURBS.get(name) or atype.replace("-", " ").capitalize() or "Specialist agent"
        agents.append((TIER_RANK.get(model, 1), name, model, status, role))
    agents.sort(key=lambda a: (a[0], a[1]))

    cards = []
    for _, name, model, status, role in agents:
        tier_cls = model if model in TIER_RANK else "sonnet"
        tier_label = model.capitalize()
        # Show a status chip only when it's not yet final — highlights draft/in-review honestly.
        st_chip = ""
        if status and status != "stable":
            st_chip = f'<span class="st">{status}</span>'
        cards.append(
            '<div class="agent"><div class="agent-top">'
            f'<span class="name">{name}</span>'
            f'<span class="chips">{st_chip}<span class="tier {tier_cls}">{tier_label}</span></span>'
            f'</div><p class="role">{role}</p></div>'
        )
    return "\n".join(cards)


def main() -> None:
    h = latest_health()
    a = h["areas"]
    s = h["status"]
    total_status = sum(s.values()) or 1
    healthy = h.get("integrity_ok", True) and not h.get("stale", 0) and not h.get("malformed", 0)

    def pct(x: int) -> int:
        return round(100 * x / total_status)

    tokens = {
        "TOTAL_DOCS": a["Total docs"],
        "AGENTS": a["Agents"],
        "SKILLS": a["Skills"],
        "COMPONENTS": a["Component contracts"],
        "PATTERNS": a["Pattern contracts"],
        "PLATFORMS": a["Platform profiles"],
        "EXAMPLES": a["Examples"],
        "STATUS_STABLE": s.get("stable", 0),
        "STATUS_INREVIEW": s.get("in-review", 0),
        "STATUS_DRAFT": s.get("draft", 0),
        "STATUS_TOTAL": total_status,
        "PCT_STABLE": pct(s.get("stable", 0)),
        "PCT_INREVIEW": pct(s.get("in-review", 0)),
        "PCT_DRAFT": pct(s.get("draft", 0)),
        "HEALTH_VERDICT": "HEALTHY" if healthy else "NEEDS ATTENTION",
        "AGENT_ROSTER": build_roster(),
        "BUILD_DATE": h.get("date", date.today().isoformat()),
    }

    html = TEMPLATE.read_text(encoding="utf-8")
    for key, val in tokens.items():
        html = html.replace("{{" + key + "}}", str(val))

    # Guard 1: no unresolved placeholders.
    leftover = re.findall(r"\{\{[A-Z_]+\}\}", html)
    if leftover:
        raise SystemExit(f"Unresolved template tokens: {sorted(set(leftover))}")

    # Guard 2: no banned stale claim survives.
    hits = [b for b in BANNED if b in html]
    if hits:
        raise SystemExit(
            "Stale claim(s) present in output: " + ", ".join(repr(h) for h in hits)
            + "\nFix tools/about-template.html — the vault has moved on from these numbers."
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} "
          f"({a['Agents']} agents, {a['Total docs']} docs, verdict {tokens['HEALTH_VERDICT']}).")


if __name__ == "__main__":
    main()
