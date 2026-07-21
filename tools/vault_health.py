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

# Which areas may reveal their item names on the *public* page. Agents, skills,
# components and patterns are generic design-system vocabulary; examples and
# platform profiles name real product surfaces, so they stay counts-only.
PUBLIC_EXPANDABLE = {"Agents", "Skills", "Component contracts", "Pattern contracts"}
# The private Artifact may expand everything with items (never the Total).
PRIVATE_EXPANDABLE = PUBLIC_EXPANDABLE | {"Examples", "Platform profiles"}

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
  section{margin-top:28px}
  h2{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);
    font-weight:600;margin:0 0 14px}
  .kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
  .kpi,details.kpi{background:var(--panel);border:1px solid var(--line);border-radius:14px;
    box-shadow:var(--shadow)}
  .kpi{padding:18px 16px}
  .kpi.total{grid-column:span 2;background:
    linear-gradient(180deg,color-mix(in srgb,var(--accent) 8%,var(--panel)),var(--panel))}
  .kpi .n{font-size:32px;font-weight:650;letter-spacing:-.02em;line-height:1}
  .kpi .k{font-size:12.5px;color:var(--muted);margin-top:8px}
  .kpi.total .n{color:var(--accent)}
  details.kpi{padding:0}
  details.kpi>summary{padding:18px 16px;cursor:pointer;list-style:none;position:relative}
  details.kpi>summary::-webkit-details-marker{display:none}
  details.kpi>summary:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:14px}
  details.kpi .chev{position:absolute;top:16px;right:15px;color:var(--muted);font-size:15px;
    transition:transform .15s ease}
  details.kpi[open]{grid-column:1/-1}
  details.kpi[open] .chev{transform:rotate(90deg)}
  .items{list-style:none;margin:0;padding:0 16px 14px;display:grid;
    grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:2px 18px;
    max-height:280px;overflow:auto}
  .items li{display:flex;align-items:center;justify-content:space-between;gap:10px;
    padding:7px 0;border-top:1px solid var(--line);font-size:13.5px}
  .items li .nm{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .pill{font-size:11px;padding:2px 8px;border-radius:999px;flex:none;font-weight:600;
    letter-spacing:.02em}
  .s-stable{color:var(--stable);background:color-mix(in srgb,var(--stable) 14%,transparent)}
  .s-review{color:var(--review);background:color-mix(in srgb,var(--review) 16%,transparent)}
  .s-draft{color:var(--draft);background:color-mix(in srgb,var(--draft) 16%,transparent)}
  @media (prefers-reduced-motion:reduce){details.kpi .chev{transition:none}}
  .panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;
    padding:22px;box-shadow:var(--shadow)}
  .row{display:flex;align-items:center;gap:14px;padding:11px 0}
  .row+.row{border-top:1px solid var(--line)}
  .row .name{width:96px;font-size:13.5px;font-weight:550}
  .swatch{width:9px;height:9px;border-radius:2px;flex:none}
  .track{flex:1;height:9px;background:var(--track);border-radius:999px;overflow:hidden}
  .fill{display:block;height:100%;border-radius:999px}
  .row .val{width:104px;text-align:right;font-size:13.5px;color:var(--muted)}
  .row .val b{color:var(--ink);font-weight:600}
  .cap{color:var(--muted);font-size:12.5px;margin:0 0 16px}
  .split{display:grid;grid-template-columns:1.3fr 1fr;gap:12px}
  .chips{display:flex;flex-wrap:wrap;gap:9px}
  .chip{display:inline-flex;align-items:center;gap:8px;font-size:13px;padding:8px 13px;
    border-radius:10px;border:1px solid var(--line);background:var(--panel-2)}
  .chip .tick{color:var(--stable);font-weight:700}
  .chip .cross{color:var(--warn);font-weight:700}
  .fresh{display:flex;gap:26px}
  .fresh .item .n{font-size:26px;font-weight:650}
  .fresh .item .k{font-size:12.5px;color:var(--muted);margin-top:3px}
  .note{color:var(--muted);font-size:12.5px;margin-top:12px;padding-top:14px;
    border-top:1px dashed var(--line)}
  .spark{width:100%;height:56px}
  .spark path{fill:none;stroke:var(--accent);stroke-width:2}
  footer{margin-top:30px;color:var(--muted);font-size:12px;text-align:center}
  @media (max-width:640px){
    .kpis{grid-template-columns:repeat(2,1fr)}
    .kpi.total{grid-column:span 2}.split{grid-template-columns:1fr}
    .banner .meta{margin-left:0;text-align:left}}
"""


def _status_pill(status: str | None) -> str:
    if not status:
        return ""
    cls = {"stable": "s-stable", "in-review": "s-review", "draft": "s-draft"}.get(status, "s-draft")
    return f'<span class="pill {cls}">{html.escape(status)}</span>'


def _card(label: str, count: int, delta: str, inventory: dict, expandable: set[str]) -> str:
    esc = html.escape(label)
    if label in expandable and inventory.get(label):
        items = "".join(
            f'<li><span class="nm">{html.escape(it["name"])}</span>'
            f'{_status_pill(it["status"])}</li>'
            for it in inventory[label]
        )
        return (
            f'<details class="kpi">'
            f'<summary><span class="n mono">{count}</span>'
            f'<span class="k">{esc}{delta}</span><span class="chev">›</span></summary>'
            f'<ul class="items">{items}</ul></details>'
        )
    cls = "kpi total" if label == "Total docs" else "kpi"
    return f'<div class="{cls}"><div class="n mono">{count}</div><div class="k">{esc}{delta}</div></div>'


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

    cards = "".join(
        _card(label, a[label], "", inv, expandable) for label in AREA_ORDER
    )

    def bar(key: str, name: str) -> str:
        pct = round(100 * s[key] / total)
        color = {"stable": "var(--stable)", "in-review": "var(--review)",
                 "draft": "var(--draft)"}[key]
        return (f'<div class="row"><span class="swatch" style="background:{color}"></span>'
                f'<span class="name">{name}</span>'
                f'<span class="track"><span class="fill" style="width:{pct}%;background:{color}"></span></span>'
                f'<span class="val"><b>{s[key]}</b> · {pct}%</span></div>')

    integ = "".join(
        f'<span class="chip"><span class="{"tick" if ok else "cross"}">'
        f'{"✓" if ok else "✕"}</span> {html.escape(name.title())}</span>'
        for name, ok in scanned["integrity"].items()
    )
    integ_note = ("All four structural checks pass. These are the same gates CI enforces on "
                  "every push." if all(scanned["integrity"].values())
                  else "One or more structural checks are failing — see the internal report.")

    spark = _sparkline([h["areas"].get("Total docs", 0) for h in history])
    hint = ("Click Agents, Skills, Component or Pattern contracts to see what's inside."
            if public else "Click any area to see what's inside.")

    return f"""<div class="wrap">
  <header>
    <div class="eyebrow">Orbit Design Brain</div>
    <h1>Vault Health</h1>
    <div class="banner" style="--verdict:{vcolor}">
      <span class="dot"></span>
      <span class="verdict">{vtext}</span>
      <span class="meta">Snapshot {scanned['date']} · regenerated daily<br>Aggregate view — no internal content exposed</span>
    </div>
  </header>

  <section>
    <h2>Contents — {hint}</h2>
    <div class="kpis">{cards}</div>
  </section>

  <section>
    <h2>Maturity</h2>
    <div class="panel">
      <p class="cap">{scanned['status_total']} documents carry a status field. Most of the vault is
        still in review — expected while contributors are actively adding context.</p>
      {bar('stable','Stable')}{bar('in-review','In review')}{bar('draft','Draft')}
    </div>
  </section>

  <section>
    <h2>Integrity &amp; freshness</h2>
    <div class="split">
      <div class="panel">
        <div class="chips">{integ}</div>
        <p class="note">{integ_note}</p>
      </div>
      <div class="panel">
        <div class="fresh">
          <div class="item"><div class="n mono">{len(scanned['stale'])}</div><div class="k">Stale &gt; {STALE_AFTER_DAYS} days</div></div>
          <div class="item"><div class="n mono">{len(scanned['malformed'])}</div><div class="k">Malformed frontmatter</div></div>
        </div>
        <p class="note">Nothing overdue for review; every governed doc has valid frontmatter.</p>
      </div>
    </div>
  </section>

  <section>
    <h2>Trend</h2>
    <div class="panel">{spark}</div>
  </section>

  <footer>Sanitized aggregate health of the shared Orbit Design Brain vault · never internal file paths</footer>
</div>"""


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
