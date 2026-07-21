#!/usr/bin/env python3
"""Vault health check for the Orbit Design Brain.

Produces a single daily read on whether the vault is staying healthy as more
people read it and add context. It writes:

- ``HEALTH.md`` (vault root)      — full internal report; file paths allowed.
- ``vault-health.html`` (root)    — sanitized, self-contained page for
  stakeholders. Aggregate counts, status mix, trend, freshness — plus a
  drill-down of item *names* for the areas whose names are generic
  design-system vocabulary (agents, skills, components, patterns). Product
  areas (examples, platforms) stay counts-only, because their titles name real
  Efficio surfaces. **Never a repo file path.** Safe to publish.
- ``tools/health_history.json``   — one aggregate snapshot per day; the trend
  source and the basis for day-over-day deltas.

With ``--artifact-out PATH`` it also writes a body-only, *full* drill-down
version (every area including examples) for the private Claude Artifact the
owner shares deliberately.

It reuses ``lint_frontmatter``'s parser (which already strips the inline-YAML
comments that trip a naive reader) and its lintable-doc set, and shells out to
the existing gating tools to record integrity status (informational here — CI
still gates separately).

A ``DRIFT``/``HEALTHY`` verdict is printed and, with ``--json``, emitted as
machine-readable output for the CI alert step. Drift = any stale doc, any
malformed doc, any integrity check failing, or the in-review backlog growing
since the previous snapshot.

Regenerating on the same day replaces that day's snapshot, so the tool is
idempotent — a second run changes nothing but proves clean.
"""

from __future__ import annotations

import argparse
import html
import json
import subprocess
import sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lint_frontmatter as lf  # noqa: E402  (reuse parser + lintable set)

ROOT = lf.ROOT
HISTORY_PATH = ROOT / "tools" / "health_history.json"
HEALTH_MD = ROOT / "HEALTH.md"
HEALTH_HTML = ROOT / "vault-health.html"

STALE_AFTER_DAYS = lf.STALE_AFTER_DAYS
HISTORY_CAP = 180
SKIP_PARTS = {"_archive", ".obsidian", ".git"}

# Areas keyed by frontmatter `type` (robust to file moves/renames).
CONTRACT_AREAS = {
    "Component contracts": "component-contract",
    "Pattern contracts": "pattern-contract",
    "Examples": "example",
    "Platform profiles": "platform-profile",
}
AREA_ORDER = ("Agents", "Skills", "Component contracts", "Pattern contracts",
              "Examples", "Platform profiles", "Total docs")
# Cards shown in the dashboard grid (Total is promoted into the hero line).
CARD_ORDER = ("Agents", "Skills", "Component contracts", "Pattern contracts",
              "Examples", "Platform profiles")

# Plain-language gloss per area, so a stakeholder who doesn't know the vault can
# still read the dashboard. Generic (safe for the public page).
AREA_GLOSS = {
    "Agents": "AI agents that build & review designs",
    "Skills": "Guided workflows the team runs",
    "Component contracts": "Specs for reusable UI components",
    "Pattern contracts": "Specs for page-level layouts",
    "Examples": "Reference screens to build from",
    "Platform profiles": "The products the vault serves",
}

# Which areas may reveal their item names on the *public* page. Agents, skills,
# components and patterns are generic design-system vocabulary; examples and
# platform profiles name real product surfaces, so they stay counts-only.
PUBLIC_EXPANDABLE = {"Agents", "Skills", "Component contracts", "Pattern contracts"}
# The private Artifact may expand everything with items (never the Total).
PRIVATE_EXPANDABLE = PUBLIC_EXPANDABLE | {"Examples", "Platform profiles"}

# Plain-language names + one-liners for the technical integrity checks.
CHECK_LABELS = {
    "export self-check": ("All required files present", "Nothing the system depends on is missing."),
    "link check": ("Every internal link works", "No broken references between documents."),
    "frontmatter lint": ("Document metadata is valid", "Every doc is tagged and dated correctly."),
    "graph links": ("Navigation index up to date", "The cross-links between docs are current."),
}

# What each maturity status means, in plain words (for the legend).
STATUS_MEANING = {
    "stable": "reviewed & approved",
    "in-review": "being worked on",
    "draft": "just started",
}

# Gating tools run for the integrity read-out (name -> argv).
INTEGRITY_CHECKS = {
    "export self-check": ["export_brain.py", "--self-check"],
    "link check": ["check_links.py"],
    "frontmatter lint": ["lint_frontmatter.py"],
    "graph links": ["gen_graph_links.py", "--check"],
}


# --------------------------------------------------------------------------- #
# Scanning
# --------------------------------------------------------------------------- #
GENERATED_OUTPUTS = {"HEALTH.md"}  # this tool's own artifacts — not vault content


def all_docs() -> list[Path]:
    """Every living markdown doc (excludes archive/obsidian/git and this tool's
    own generated outputs)."""
    docs = []
    for path in sorted(ROOT.rglob("*.md")):
        rel = path.relative_to(ROOT)
        if any(part in SKIP_PARTS for part in rel.parts):
            continue
        if rel.as_posix() in GENERATED_OUTPUTS:
            continue
        docs.append(path)
    return docs


def _first_heading(path: Path) -> str | None:
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def _example_name(path: Path) -> str:
    heading = _first_heading(path) or path.stem
    for prefix in ("Golden Example: ", "Golden Example — "):
        if heading.startswith(prefix):
            return heading[len(prefix):]
    return heading


def build_inventory(docs: list[Path]) -> dict[str, list[dict]]:
    """area -> [{name, status}] sorted, for the drill-down."""
    by_type: dict[str, list[Path]] = {}
    for path in docs:
        fm = lf.parse_frontmatter(path)
        if fm and fm.get("type"):
            by_type.setdefault(fm["type"], []).append(path)

    def items(paths: list[Path], namer) -> list[dict]:
        out = []
        for p in paths:
            fm = lf.parse_frontmatter(p) or {}
            out.append({"name": namer(p), "status": fm.get("status")})
        return sorted(out, key=lambda d: d["name"].lower())

    agents = sorted((ROOT / "design-brain" / "agents").glob("*.md"))
    skills = sorted((ROOT / "design-brain" / "skills").glob("*/SKILL.md"))
    inv: dict[str, list[dict]] = {
        "Agents": items(agents, lambda p: p.stem),
        "Skills": [
            {"name": (lf.parse_frontmatter(p) or {}).get("name", p.parent.name),
             "status": None}
            for p in skills
        ],
        "Component contracts": items(by_type.get("component-contract", []), lambda p: p.stem),
        "Pattern contracts": items(by_type.get("pattern-contract", []), lambda p: p.stem),
        "Examples": items(by_type.get("example", []), _example_name),
        "Platform profiles": items(by_type.get("platform-profile", []), lambda p: p.stem),
    }
    inv["Skills"].sort(key=lambda d: d["name"].lower())
    return inv


def scan(today: date) -> dict:
    docs = all_docs()
    inventory = build_inventory(docs)

    areas = {label: len(inventory[label]) for label in inventory}
    areas["Total docs"] = len(docs)

    # Status mix over docs that carry a status field (skill files legitimately
    # do not — they use the Claude-skill frontmatter shape).
    status = Counter()
    for path in docs:
        fm = lf.parse_frontmatter(path)
        if fm and "status" in fm:
            status[fm["status"]] += 1

    # Attention: stale (>90d) and malformed, over the canonical governed set
    # that CI lints — lf.iter_targets() already exempts skills, templates,
    # manifests, and benchmark results, so this matches what CI enforces.
    cutoff = today - timedelta(days=STALE_AFTER_DAYS)
    stale: list[str] = []
    malformed: list[str] = []
    for path in lf.iter_targets():
        rel = path.relative_to(ROOT).as_posix()
        fm = lf.parse_frontmatter(path)
        if fm is None:
            malformed.append(f"{rel} — no frontmatter block")
            continue
        st = fm.get("status")
        if st is None:
            malformed.append(f"{rel} — missing status")
        elif st not in lf.VALID_STATUS:
            malformed.append(f"{rel} — invalid status '{st}'")
        reviewed = fm.get("last_reviewed")
        if reviewed:
            try:
                if date.fromisoformat(reviewed) < cutoff:
                    stale.append(f"{reviewed}  {rel}")
            except ValueError:
                malformed.append(f"{rel} — last_reviewed '{reviewed}' not YYYY-MM-DD")

    integrity = run_integrity()

    return {
        "date": today.isoformat(),
        "areas": areas,
        "inventory": inventory,
        "status": {k: status.get(k, 0) for k in ("stable", "in-review", "draft")},
        "status_total": sum(status.values()),
        "stale": sorted(stale),
        "malformed": sorted(malformed),
        "integrity": integrity,
    }


def run_integrity() -> dict[str, bool]:
    results: dict[str, bool] = {}
    for name, argv in INTEGRITY_CHECKS.items():
        try:
            proc = subprocess.run(
                [sys.executable, str(ROOT / "tools" / argv[0]), *argv[1:]],
                cwd=ROOT, capture_output=True, text=True, timeout=300,
            )
            results[name] = proc.returncode == 0
        except Exception:  # a check that cannot run is a failed check
            results[name] = False
    return results


# --------------------------------------------------------------------------- #
# History + verdict
# --------------------------------------------------------------------------- #
def load_history() -> list[dict]:
    if not HISTORY_PATH.is_file():
        return []
    try:
        data = json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def snapshot(scanned: dict) -> dict:
    return {
        "date": scanned["date"],
        "areas": scanned["areas"],
        "status": scanned["status"],
        "stale": len(scanned["stale"]),
        "malformed": len(scanned["malformed"]),
        "integrity_ok": all(scanned["integrity"].values()),
    }


def update_history(scanned: dict) -> tuple[list[dict], dict | None]:
    """Append/replace today's snapshot; return (history, previous_snapshot)."""
    history = [h for h in load_history() if h.get("date") != scanned["date"]]
    previous = history[-1] if history else None
    history.append(snapshot(scanned))
    history = history[-HISTORY_CAP:]
    HISTORY_PATH.write_text(
        json.dumps(history, indent=2) + "\n", encoding="utf-8"
    )
    return history, previous


def verdict(scanned: dict, previous: dict | None) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if scanned["stale"]:
        reasons.append(f"{len(scanned['stale'])} doc(s) not reviewed in {STALE_AFTER_DAYS}+ days")
    if scanned["malformed"]:
        reasons.append(f"{len(scanned['malformed'])} doc(s) with malformed frontmatter")
    failed = [n for n, ok in scanned["integrity"].items() if not ok]
    if failed:
        reasons.append("integrity check failed: " + ", ".join(failed))
    if previous is not None:
        grew = scanned["status"]["in-review"] - previous["status"]["in-review"]
        if grew > 0:
            reasons.append(f"in-review backlog grew by {grew} since {previous['date']}")
    return (not reasons), reasons


# --------------------------------------------------------------------------- #
# Markdown report (internal — file paths allowed)
# --------------------------------------------------------------------------- #
def _delta(cur: int, prev: int | None) -> str:
    if prev is None or cur == prev:
        return ""
    return f" ({'+' if cur > prev else ''}{cur - prev})"


def render_md(scanned: dict, previous: dict | None, healthy: bool, reasons: list[str]) -> str:
    a = scanned["areas"]
    s = scanned["status"]
    pa = previous["areas"] if previous else {}
    ps = previous["status"] if previous else {}
    lines = [
        "<!-- generated by tools/vault_health.py — do not hand-edit; run the tool to refresh -->",
        "# Vault Health",
        "",
        f"_Snapshot {scanned['date']}. Regenerate with `tools/vault_health.py`._",
        "",
        f"**Status: {'HEALTHY ✅' if healthy else 'NEEDS ATTENTION ⚠️'}**",
    ]
    if reasons:
        lines += [""] + [f"- {r}" for r in reasons]
    lines += ["", "## Contents", "", "| Area | Count |", "| --- | ---: |"]
    for label in AREA_ORDER:
        lines.append(f"| {label} | {a[label]}{_delta(a[label], pa.get(label))} |")

    total = scanned["status_total"] or 1
    lines += ["", "## Status mix", "",
              f"_{scanned['status_total']} docs carry a status field "
              "(skill files use a different frontmatter shape and are exempt)._",
              "", "| Status | Count | Share |", "| --- | ---: | ---: |"]
    for key in ("stable", "in-review", "draft"):
        pct = round(100 * s[key] / total)
        lines.append(f"| {key} | {s[key]}{_delta(s[key], ps.get(key))} | {pct}% |")

    lines += ["", "## Inventory", ""]
    for label in ("Agents", "Skills", "Component contracts", "Pattern contracts",
                  "Examples", "Platform profiles"):
        items = scanned["inventory"][label]
        lines.append(f"### {label} ({len(items)})")
        for it in items:
            tag = f" — {it['status']}" if it["status"] else ""
            lines.append(f"- {it['name']}{tag}")
        lines.append("")

    lines += ["## Integrity checks", "", "| Check | Result |", "| --- | --- |"]
    for name, ok in scanned["integrity"].items():
        lines.append(f"| {name} | {'pass ✅' if ok else 'FAIL ❌'} |")

    lines += ["", "## Freshness", "",
              f"- Stale (>{STALE_AFTER_DAYS}d since review): **{len(scanned['stale'])}**"]
    for item in scanned["stale"]:
        lines.append(f"  - {item}")
    lines += [f"- Malformed frontmatter: **{len(scanned['malformed'])}**"]
    for item in scanned["malformed"]:
        lines.append(f"  - {item}")
    lines.append("")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# HTML (shared body; wrapped standalone for Pages, body-only for the Artifact)
# --------------------------------------------------------------------------- #
STYLE = """
  :root{
    --bg:#f5f7fa;--panel:#fff;--panel-2:#f0f3f8;--ink:#141922;--muted:#59626f;
    --line:#e4e9f0;--accent:#0e7c86;--stable:#1f9d55;--review:#c98a00;
    --draft:#64748b;--warn:#c2410c;--track:#eaeef4;
    --shadow:0 1px 2px rgba(20,25,34,.04),0 8px 24px rgba(20,25,34,.05);
  }
  @media (prefers-color-scheme:dark){:root{
    --bg:#0c0f14;--panel:#141922;--panel-2:#0f141b;--ink:#e9edf3;--muted:#98a2b2;
    --line:#232a35;--accent:#2dd4bf;--stable:#3ecf7f;--review:#e5b84b;
    --draft:#94a3b8;--warn:#f0894e;--track:#1c232e;
    --shadow:0 1px 2px rgba(0,0,0,.3),0 10px 30px rgba(0,0,0,.35);}}
  :root[data-theme=light]{
    --bg:#f5f7fa;--panel:#fff;--panel-2:#f0f3f8;--ink:#141922;--muted:#59626f;
    --line:#e4e9f0;--accent:#0e7c86;--stable:#1f9d55;--review:#c98a00;
    --draft:#64748b;--warn:#c2410c;--track:#eaeef4;
    --shadow:0 1px 2px rgba(20,25,34,.04),0 8px 24px rgba(20,25,34,.05);}
  :root[data-theme=dark]{
    --bg:#0c0f14;--panel:#141922;--panel-2:#0f141b;--ink:#e9edf3;--muted:#98a2b2;
    --line:#232a35;--accent:#2dd4bf;--stable:#3ecf7f;--review:#e5b84b;
    --draft:#94a3b8;--warn:#f0894e;--track:#1c232e;
    --shadow:0 1px 2px rgba(0,0,0,.3),0 10px 30px rgba(0,0,0,.35);}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    line-height:1.5;-webkit-font-smoothing:antialiased}
  .mono{font-family:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;
    font-variant-numeric:tabular-nums}
  .wrap{max-width:900px;margin:0 auto;padding:40px 22px 64px}
  .eyebrow{font-size:11px;letter-spacing:.14em;text-transform:uppercase;
    color:var(--muted);font-weight:600}
  header{margin-bottom:26px}
  h1{font-size:23px;letter-spacing:-.01em;margin:6px 0 0;font-weight:650}
  .banner{margin-top:20px;display:flex;align-items:center;gap:18px;flex-wrap:wrap;
    background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--verdict);
    border-radius:14px;padding:18px 22px;box-shadow:var(--shadow)}
  .dot{width:11px;height:11px;border-radius:50%;background:var(--verdict);
    box-shadow:0 0 0 4px color-mix(in srgb,var(--verdict) 22%,transparent);flex:none}
  .banner .verdict{font-size:17px;font-weight:650}
  .banner .meta{color:var(--muted);font-size:13px;margin-left:auto;text-align:right}
  .banner .summary-line{color:var(--muted);font-size:13.5px;margin-top:3px;
    font-variant-numeric:tabular-nums}
  section{margin-top:34px}
  .s-head{margin:0 0 4px;font-size:16px;font-weight:650;letter-spacing:-.01em}
  .s-sub{margin:0 0 16px;color:var(--muted);font-size:13px}
  .kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
  .kpi,.kpi-btn{background:var(--panel);border:1px solid var(--line);border-radius:14px;
    box-shadow:var(--shadow);display:flex;flex-direction:column;padding:17px 17px 18px}
  .kpi .n,.kpi-btn .n{font-size:29px;font-weight:650;letter-spacing:-.02em;line-height:1}
  .kpi .k,.kpi-btn .k{font-size:14px;font-weight:650;margin-top:9px}
  .gloss{font-size:12px;color:var(--muted);margin-top:4px;line-height:1.4}
  /* Expandable cards are buttons that open the slide-in drawer. */
  .kpi-btn{cursor:pointer;text-align:left;font:inherit;color:inherit;width:100%;
    transition:border-color .12s ease,transform .12s ease}
  .kpi-btn:hover{border-color:var(--accent);transform:translateY(-1px)}
  .kpi-btn:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
  .expand-hint{margin-top:12px;font-size:12px;font-weight:650;color:var(--accent);
    display:flex;align-items:center;gap:6px}
  .expand-hint .chev{font-size:14px;line-height:1}
  .pill{font-size:11px;padding:2px 8px;border-radius:999px;flex:none;font-weight:600;
    letter-spacing:.02em}
  .s-stable{color:var(--stable);background:color-mix(in srgb,var(--stable) 14%,transparent)}
  .s-review{color:var(--review);background:color-mix(in srgb,var(--review) 16%,transparent)}
  .s-draft{color:var(--draft);background:color-mix(in srgb,var(--draft) 16%,transparent)}
  /* Side panel: docked right, slides in from the right, pushes content left —
     no overlay, no scrim. --dw is the panel width (full-width on small screens). */
  :root{--dw:400px}
  html{overflow-x:hidden}
  #shell{transition:margin-right .28s cubic-bezier(.4,0,.2,1)}
  body.drawer-open #shell{margin-right:var(--dw)}
  .drawer{position:fixed;top:0;right:0;height:100dvh;width:var(--dw);
    background:var(--panel);border-left:1px solid var(--line);
    box-shadow:-14px 0 34px rgba(10,14,20,.12);
    transform:translateX(100%);visibility:hidden;z-index:30;display:flex;flex-direction:column;
    transition:transform .28s cubic-bezier(.4,0,.2,1),visibility 0s linear .28s}
  body.drawer-open .drawer{transform:translateX(0);visibility:visible;
    transition:transform .28s cubic-bezier(.4,0,.2,1)}
  @media (max-width:820px){:root{--dw:100vw}
    body.drawer-open #shell{margin-right:0}}
  .drawer .dhead{display:flex;align-items:center;gap:10px;padding:20px 20px 15px;
    border-bottom:1px solid var(--line)}
  .drawer .dhead h3{margin:0;font-size:15px;font-weight:650}
  .drawer .dcount{font-size:12px;font-weight:650;color:var(--accent);
    background:color-mix(in srgb,var(--accent) 12%,transparent);border-radius:999px;padding:2px 9px}
  .drawer-close{margin-left:auto;background:none;border:1px solid var(--line);border-radius:8px;
    width:30px;height:30px;cursor:pointer;color:var(--muted);font-size:18px;line-height:1;
    display:grid;place-items:center}
  .drawer-close:hover{border-color:var(--accent);color:var(--ink)}
  .drawer-close:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
  .drawer .dgloss{padding:14px 20px 0;color:var(--muted);font-size:12.5px}
  .drawer-body{padding:10px 20px 24px;overflow:auto}
  .items{list-style:none;margin:0;padding:0}
  .items li{display:flex;align-items:center;justify-content:space-between;gap:10px;
    padding:10px 0;border-top:1px solid var(--line);font-size:13.5px}
  .items li:first-child{border-top:none}
  .items li .nm{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  @media (prefers-reduced-motion:reduce){
    .kpi-btn,.kpi-btn:hover,#shell,.drawer{transition:none}
    body.drawer-open .drawer{transition:none}}
  .panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;
    padding:22px;box-shadow:var(--shadow)}
  .legend{display:flex;flex-wrap:wrap;gap:8px 18px;margin:0 0 16px;padding-bottom:16px;
    border-bottom:1px solid var(--line)}
  .legend .lg{display:flex;align-items:center;gap:7px;font-size:12.5px;color:var(--muted)}
  .legend .lg b{color:var(--ink);font-weight:600}
  .legend .sw{width:9px;height:9px;border-radius:2px;flex:none}
  .row{display:flex;align-items:center;gap:14px;padding:11px 0}
  .row+.row{border-top:1px solid var(--line)}
  .row .name{width:96px;font-size:13.5px;font-weight:550}
  .track{flex:1;height:9px;background:var(--track);border-radius:999px;overflow:hidden}
  .fill{display:block;height:100%;border-radius:999px}
  .row .val{width:104px;text-align:right;font-size:13.5px;color:var(--muted)}
  .row .val b{color:var(--ink);font-weight:600}
  .checks{display:grid;grid-template-columns:1fr 1fr;gap:10px 22px}
  .check{display:flex;align-items:flex-start;gap:10px;font-size:13.5px}
  .check .mk{flex:none;width:20px;height:20px;border-radius:50%;display:grid;place-items:center;
    font-size:12px;font-weight:700;margin-top:1px}
  .check.ok .mk{color:var(--stable);background:color-mix(in srgb,var(--stable) 15%,transparent)}
  .check.bad .mk{color:var(--warn);background:color-mix(in srgb,var(--warn) 15%,transparent)}
  .check .ct{font-weight:600}
  .check .cd{color:var(--muted);font-size:12px;margin-top:1px}
  .fresh{display:flex;gap:16px;flex-wrap:wrap}
  .fresh .item{flex:1;min-width:150px;background:var(--panel-2);border:1px solid var(--line);
    border-radius:12px;padding:15px 16px;display:flex;align-items:center;gap:13px}
  .fresh .item .n{font-size:26px;font-weight:650}
  .fresh .item .k{font-size:13px;font-weight:600}
  .fresh .item .d{font-size:11.5px;color:var(--muted);margin-top:1px}
  .fresh .item.good .n{color:var(--stable)}
  .spark{width:100%;height:56px}
  .spark path{fill:none;stroke:var(--accent);stroke-width:2}
  .cap{color:var(--muted);font-size:12.5px;margin:0}
  footer{margin-top:34px;color:var(--muted);font-size:12px;text-align:center;line-height:1.6}
  @media (max-width:640px){
    .kpis{grid-template-columns:repeat(2,1fr)}
    .checks{grid-template-columns:1fr}
    .banner .meta{margin-left:0;text-align:left}}
"""


def _status_pill(status: str | None) -> str:
    if not status:
        return ""
    cls = {"stable": "s-stable", "in-review": "s-review", "draft": "s-draft"}.get(status, "s-draft")
    return f'<span class="pill {cls}">{html.escape(status)}</span>'


def _card(label: str, count: int, inventory: dict, expandable: set[str]) -> str:
    esc = html.escape(label)
    gloss = html.escape(AREA_GLOSS.get(label, ""))
    if label in expandable and inventory.get(label):
        hint = (f'<span class="expand-hint"><span class="chev">›</span>See all {count}</span>')
        return (
            f'<button type="button" class="kpi-btn" data-area="{esc}" '
            f'aria-haspopup="dialog" aria-label="See all {count} {esc}">'
            f'<span class="n mono">{count}</span>'
            f'<span class="k">{esc}</span><span class="gloss">{gloss}</span>{hint}</button>'
        )
    return (f'<div class="kpi"><div class="n mono">{count}</div>'
            f'<div class="k">{esc}</div><div class="gloss">{gloss}</div></div>')


def _panel_src(label: str, inventory: dict) -> str:
    """Hidden per-area list the drawer clones on open."""
    items = "".join(
        f'<li><span class="nm">{html.escape(it["name"])}</span>'
        f'{_status_pill(it["status"])}</li>'
        for it in inventory[label]
    )
    return (f'<div class="panel-src" data-area="{html.escape(label)}" '
            f'data-count="{len(inventory[label])}" '
            f'data-gloss="{html.escape(AREA_GLOSS.get(label, ""))}" hidden>'
            f'<ul class="items">{items}</ul></div>')


def _sparkline(points: list[int]) -> str:
    if len(points) < 2:
        return ('<p class="cap" style="margin:0">This is the first daily snapshot. The trend line — '
                'document count and status mix over time — appears here once a few days of history '
                'accumulate, so you can watch whether the in-review backlog is clearing or growing.</p>')
    lo, hi = min(points), max(points)
    span = (hi - lo) or 1
    n = len(points)
    coords = [f"{round(100*i/(n-1),2)},{round(50-44*(v-lo)/span,2)}" for i, v in enumerate(points)]
    return (f'<svg class="spark" viewBox="0 0 100 56" preserveAspectRatio="none">'
            f'<path d="M{"L".join(coords)}"/></svg>')


def render_body(scanned: dict, history: list[dict], healthy: bool, *, public: bool) -> str:
    a = scanned["areas"]
    s = scanned["status"]
    inv = scanned["inventory"]
    total = scanned["status_total"] or 1
    expandable = PUBLIC_EXPANDABLE if public else PRIVATE_EXPANDABLE
    vcolor = "var(--stable)" if healthy else "var(--warn)"
    vtext = "Healthy" if healthy else "Needs attention"

    cards = "".join(_card(label, a[label], inv, expandable) for label in CARD_ORDER)
    panel_srcs = "".join(
        _panel_src(label, inv) for label in CARD_ORDER
        if label in expandable and inv.get(label)
    )

    def bar(key: str, name: str) -> str:
        pct = round(100 * s[key] / total)
        color = {"stable": "var(--stable)", "in-review": "var(--review)",
                 "draft": "var(--draft)"}[key]
        return (f'<div class="row"><span class="name">{name}</span>'
                f'<span class="track"><span class="fill" style="width:{pct}%;background:{color}"></span></span>'
                f'<span class="val"><b>{s[key]}</b> · {pct}%</span></div>')

    legend = "".join(
        f'<span class="lg"><span class="sw" style="background:{c}"></span>'
        f'<b>{n}</b> — {STATUS_MEANING[k]}</span>'
        for k, n, c in (("stable", "Stable", "var(--stable)"),
                        ("in-review", "In review", "var(--review)"),
                        ("draft", "Draft", "var(--draft)"))
    )

    checks = "".join(
        f'<div class="check {"ok" if ok else "bad"}"><span class="mk">{"✓" if ok else "✕"}</span>'
        f'<span><span class="ct">{html.escape(CHECK_LABELS.get(name, (name, ""))[0])}</span>'
        f'<span class="cd">{html.escape(CHECK_LABELS.get(name, (name, ""))[1])}</span></span></div>'
        for name, ok in scanned["integrity"].items()
    )
    n_fail = sum(1 for ok in scanned["integrity"].values() if not ok)
    checks_sub = ("Run automatically on every change — all passing."
                  if n_fail == 0 else f"{n_fail} failing — see the internal report.")

    # Plain-language hero summary — the at-a-glance answer.
    overdue = len(scanned["stale"]) + len(scanned["malformed"])
    summary = " · ".join([
        f"{a['Total docs']} documents",
        "all checks passing" if n_fail == 0 else f"{n_fail} check{'s' if n_fail != 1 else ''} failing",
        "nothing overdue" if overdue == 0 else f"{overdue} item{'s' if overdue != 1 else ''} need attention",
    ])

    stale_good = "good" if not scanned["stale"] else "bad"
    mal_good = "good" if not scanned["malformed"] else "bad"
    spark = _sparkline([h["areas"].get("Total docs", 0) for h in history])
    reveal = ("Agents, Skills, Components and Patterns"
              if public else "Every card")

    return f"""<div id="shell"><div class="wrap">
  <header>
    <div class="eyebrow">Orbit Design Brain</div>
    <h1>Vault Health</h1>
    <div class="banner" style="--verdict:{vcolor}">
      <span class="dot"></span>
      <div>
        <div class="verdict">{vtext}</div>
        <div class="summary-line">{summary}</div>
      </div>
      <span class="meta">Updated {scanned['date']}<br>Refreshes daily</span>
    </div>
  </header>

  <section>
    <h2 class="s-head">What's inside</h2>
    <p class="s-sub">The building blocks the vault holds. {reveal} can be opened to list what's in them.</p>
    <div class="kpis">{cards}</div>
  </section>
  <div hidden>{panel_srcs}</div>

  <section>
    <h2 class="s-head">How ready it is</h2>
    <p class="s-sub">Where the {scanned['status_total']} documents sit on the way to approved. A large
      in-review share is normal while the team is actively building the vault.</p>
    <div class="panel">
      <div class="legend">{legend}</div>
      {bar('stable','Stable')}{bar('in-review','In review')}{bar('draft','Draft')}
    </div>
  </section>

  <section>
    <h2 class="s-head">Is anything wrong?</h2>
    <p class="s-sub">{checks_sub}</p>
    <div class="panel">
      <div class="checks">{checks}</div>
    </div>
  </section>

  <section>
    <h2 class="s-head">Needs attention</h2>
    <p class="s-sub">Documents that have drifted out of good standing.</p>
    <div class="panel">
      <div class="fresh">
        <div class="item {stale_good}"><div class="n mono">{len(scanned['stale'])}</div>
          <div><div class="k">Overdue for review</div><div class="d">Not looked at in {STALE_AFTER_DAYS}+ days</div></div></div>
        <div class="item {mal_good}"><div class="n mono">{len(scanned['malformed'])}</div>
          <div><div class="k">Metadata problems</div><div class="d">Missing or invalid tags/dates</div></div></div>
      </div>
    </div>
  </section>

  <section>
    <h2 class="s-head">Trend</h2>
    <p class="s-sub">How the vault is growing over time.</p>
    <div class="panel">{spark}</div>
  </section>

  <footer>Sanitized aggregate health of the shared Orbit Design Brain vault.<br>Counts and maturity only — never internal file paths.</footer>
</div></div>

<aside class="drawer" role="region" aria-labelledby="drawer-title" aria-hidden="true">
  <div class="dhead">
    <h3 id="drawer-title"></h3>
    <span class="dcount"></span>
    <button type="button" class="drawer-close" aria-label="Close panel">&times;</button>
  </div>
  <p class="dgloss"></p>
  <div class="drawer-body"></div>
</aside>

<script>
(function(){{
  var body=document.body,
      drawer=document.querySelector('.drawer'),
      title=drawer.querySelector('#drawer-title'),
      count=drawer.querySelector('.dcount'),
      gloss=drawer.querySelector('.dgloss'),
      dbody=drawer.querySelector('.drawer-body'),
      closeBtn=drawer.querySelector('.drawer-close'),
      last=null;
  function open(area){{
    var src=document.querySelector('.panel-src[data-area="'+area+'"]');
    if(!src) return;
    title.textContent=area;
    count.textContent=src.getAttribute('data-count');
    gloss.textContent=src.getAttribute('data-gloss')||'';
    dbody.innerHTML='';
    dbody.appendChild(src.querySelector('.items').cloneNode(true));
    body.classList.add('drawer-open');
    drawer.setAttribute('aria-hidden','false');
    closeBtn.focus();
  }}
  function close(){{
    body.classList.remove('drawer-open');
    drawer.setAttribute('aria-hidden','true');
    if(last) last.focus();
  }}
  document.querySelectorAll('.kpi-btn').forEach(function(btn){{
    btn.addEventListener('click',function(){{
      if(body.classList.contains('drawer-open')&&last===btn){{ close(); return; }}
      last=btn; open(btn.getAttribute('data-area'));
    }});
  }});
  closeBtn.addEventListener('click',close);
  document.addEventListener('keydown',function(e){{
    if(e.key==='Escape'&&body.classList.contains('drawer-open')) close();
  }});
}})();
</script>"""


def render_standalone(scanned: dict, history: list[dict], healthy: bool) -> str:
    body = render_body(scanned, history, healthy, public=True)
    # No hardcoded data-theme: let the viewer's OS preference drive the page
    # (prefers-color-scheme). The :root[data-theme=…] overrides still win if a
    # host stamps the attribute.
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Orbit Design Brain — Vault Health</title>
<style>{STYLE}</style>
</head>
<body>
{body}
</body>
</html>
"""


def render_artifact(scanned: dict, history: list[dict], healthy: bool) -> str:
    """Body-only (full drill-down) for the private Claude Artifact."""
    body = render_body(scanned, history, healthy, public=False)
    return (f"<title>Orbit Design Brain — Vault Health</title>\n"
            f"<style>{STYLE}</style>\n{body}\n")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true",
                        help="emit the verdict + metrics as JSON (for CI alerting)")
    parser.add_argument("--artifact-out", metavar="PATH",
                        help="also write a body-only full-detail HTML for the private Artifact")
    args = parser.parse_args()

    today = date.today()
    scanned = scan(today)
    history, previous = update_history(scanned)
    healthy, reasons = verdict(scanned, previous)

    HEALTH_MD.write_text(render_md(scanned, previous, healthy, reasons), encoding="utf-8")
    HEALTH_HTML.write_text(render_standalone(scanned, history, healthy), encoding="utf-8")
    if args.artifact_out:
        Path(args.artifact_out).write_text(
            render_artifact(scanned, history, healthy), encoding="utf-8")

    if args.json:
        print(json.dumps({
            "date": scanned["date"],
            "healthy": healthy,
            "reasons": reasons,
            "areas": scanned["areas"],
            "status": scanned["status"],
        }, indent=2))
    else:
        print(f"Vault health {scanned['date']}: {'HEALTHY' if healthy else 'DRIFT'}")
        for r in reasons:
            print(f"  - {r}")
        out = [HEALTH_MD.name, HEALTH_HTML.name, HISTORY_PATH.name]
        if args.artifact_out:
            out.append(args.artifact_out)
        print("Wrote " + ", ".join(out))


if __name__ == "__main__":
    main()
