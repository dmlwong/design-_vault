#!/usr/bin/env python3
"""Vault health check for the Orbit Design Brain.

Produces a single daily read on whether the vault is staying healthy as more
people read it and add context. It writes three artifacts:

- ``HEALTH.md`` (vault root)      — full internal report; file paths allowed.
- ``vault-health.html`` (root)    — sanitized, self-contained page for
  stakeholders: **counts, status mix, trend, freshness only — never a repo
  file path or name.** Safe to publish.
- ``tools/health_history.json``   — one aggregate snapshot per day; the trend
  source and the basis for day-over-day deltas.

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


def scan(today: date) -> dict:
    docs = all_docs()

    # Area totals.
    agents = sorted((ROOT / "design-brain" / "agents").glob("*.md"))
    skills = sorted((ROOT / "design-brain" / "skills").glob("*/SKILL.md"))
    areas = {"Agents": len(agents), "Skills": len(skills)}
    type_counts: Counter[str] = Counter()
    for path in docs:
        fm = lf.parse_frontmatter(path)
        if fm and fm.get("type"):
            type_counts[fm["type"]] += 1
    for label, type_name in CONTRACT_AREAS.items():
        areas[label] = type_counts.get(type_name, 0)
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
# Rendering
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
        f"_Snapshot {scanned['date']}. Regenerate with `python3 tools/vault_health.py`._",
        "",
        f"**Status: {'HEALTHY ✅' if healthy else 'NEEDS ATTENTION ⚠️'}**",
    ]
    if reasons:
        lines += [""] + [f"- {r}" for r in reasons]
    lines += ["", "## Contents", "", "| Area | Count |", "| --- | ---: |"]
    for label in ("Agents", "Skills", "Component contracts", "Pattern contracts",
                  "Examples", "Platform profiles", "Total docs"):
        lines.append(f"| {label} | {a[label]}{_delta(a[label], pa.get(label))} |")

    total = scanned["status_total"] or 1
    lines += ["", "## Status mix", "",
              f"_{scanned['status_total']} docs carry a status field "
              "(skill files use a different frontmatter shape and are exempt)._",
              "", "| Status | Count | Share |", "| --- | ---: | ---: |"]
    for key in ("stable", "in-review", "draft"):
        pct = round(100 * s[key] / total)
        lines.append(f"| {key} | {s[key]}{_delta(s[key], ps.get(key))} | {pct}% |")

    lines += ["", "## Integrity checks", "", "| Check | Result |", "| --- | --- |"]
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


def render_html(scanned: dict, history: list[dict], healthy: bool) -> str:
    """Sanitized, self-contained stakeholder page. No file paths or names."""
    a = scanned["areas"]
    s = scanned["status"]
    total = scanned["status_total"] or 1
    verdict_txt = "Healthy" if healthy else "Needs attention"
    verdict_cls = "ok" if healthy else "warn"

    area_cards = "".join(
        f'<div class="card"><div class="num">{a[label]}</div>'
        f'<div class="lbl">{label}</div></div>'
        for label in ("Agents", "Skills", "Component contracts", "Pattern contracts",
                      "Examples", "Platform profiles", "Total docs")
    )

    def bar(key: str, cls: str) -> str:
        pct = round(100 * s[key] / total)
        return (f'<div class="bar-row"><span class="bar-lbl">{key}</span>'
                f'<span class="bar-track"><span class="bar-fill {cls}" '
                f'style="width:{pct}%"></span></span>'
                f'<span class="bar-val">{s[key]} · {pct}%</span></div>')

    bars = (bar("stable", "b-stable") + bar("in-review", "b-review")
            + bar("draft", "b-draft"))

    # Trend sparkline of total docs (aggregate only).
    pts = [h["areas"].get("Total docs", 0) for h in history]
    spark = _sparkline(pts)

    integ = "".join(
        f'<li class="{"ok" if ok else "warn"}">{name}: '
        f'{"pass" if ok else "FAIL"}</li>'
        for name, ok in scanned["integrity"].items()
    )

    return f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Orbit Design Brain — Vault Health</title>
<style>
  :root {{
    --bg:#f7f8fa; --panel:#fff; --ink:#1a1d24; --muted:#5b6472;
    --line:#e4e7ec; --ok:#1f9d55; --warn:#c2410c;
    --stable:#1f9d55; --review:#c98a00; --draft:#6b7280; --track:#eceef1;
  }}
  html[data-theme="dark"] {{
    --bg:#0f1218; --panel:#171b23; --ink:#e8ebf0; --muted:#9aa4b2;
    --line:#262c37; --ok:#3ecf7f; --warn:#f0894e;
    --stable:#3ecf7f; --review:#e5b84b; --draft:#8a94a3; --track:#232935;
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
    background:var(--bg); color:var(--ink); }}
  .wrap {{ max-width:840px; margin:0 auto; padding:32px 20px 56px; }}
  header {{ display:flex; justify-content:space-between; align-items:flex-start;
    gap:16px; flex-wrap:wrap; margin-bottom:24px; }}
  h1 {{ font-size:20px; margin:0 0 4px; }}
  .sub {{ color:var(--muted); font-size:13px; }}
  .badge {{ font-weight:600; font-size:13px; padding:6px 14px; border-radius:999px;
    border:1px solid var(--line); }}
  .badge.ok {{ color:var(--ok); }} .badge.warn {{ color:var(--warn); }}
  .toggle {{ background:none; border:1px solid var(--line); color:var(--muted);
    border-radius:8px; padding:5px 10px; font-size:12px; cursor:pointer; }}
  section {{ background:var(--panel); border:1px solid var(--line); border-radius:12px;
    padding:20px; margin-bottom:16px; }}
  h2 {{ font-size:13px; text-transform:uppercase; letter-spacing:.04em;
    color:var(--muted); margin:0 0 16px; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(120px,1fr)); gap:12px; }}
  .card {{ background:var(--bg); border:1px solid var(--line); border-radius:10px;
    padding:16px; text-align:center; }}
  .num {{ font-size:26px; font-weight:650; }}
  .lbl {{ font-size:12px; color:var(--muted); margin-top:4px; }}
  .bar-row {{ display:flex; align-items:center; gap:12px; margin-bottom:10px; }}
  .bar-lbl {{ width:78px; font-size:13px; color:var(--muted); }}
  .bar-track {{ flex:1; height:10px; background:var(--track); border-radius:999px; overflow:hidden; }}
  .bar-fill {{ display:block; height:100%; border-radius:999px; }}
  .b-stable {{ background:var(--stable); }} .b-review {{ background:var(--review); }}
  .b-draft {{ background:var(--draft); }}
  .bar-val {{ width:88px; text-align:right; font-size:13px; font-variant-numeric:tabular-nums; }}
  ul.integ {{ list-style:none; margin:0; padding:0; display:flex; flex-wrap:wrap; gap:8px; }}
  ul.integ li {{ font-size:13px; padding:5px 12px; border-radius:8px; border:1px solid var(--line); }}
  ul.integ li.ok {{ color:var(--ok); }} ul.integ li.warn {{ color:var(--warn); }}
  .spark {{ width:100%; height:52px; }}
  .spark path {{ fill:none; stroke:var(--review); stroke-width:2; }}
  footer {{ color:var(--muted); font-size:12px; text-align:center; margin-top:8px; }}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div>
      <h1>Orbit Design Brain — Vault Health</h1>
      <div class="sub">Aggregate health of the shared design vault · updated {scanned['date']}</div>
    </div>
    <div style="display:flex;gap:10px;align-items:center">
      <span class="badge {verdict_cls}">{verdict_txt}</span>
      <button class="toggle" onclick="var r=document.documentElement;r.dataset.theme=r.dataset.theme==='dark'?'light':'dark'">Theme</button>
    </div>
  </header>

  <section>
    <h2>Contents</h2>
    <div class="grid">{area_cards}</div>
  </section>

  <section>
    <h2>Maturity — {scanned['status_total']} documents</h2>
    {bars}
  </section>

  <section>
    <h2>Integrity checks</h2>
    <ul class="integ">{integ}</ul>
  </section>

  <section>
    <h2>Total documents over time</h2>
    {spark}
  </section>

  <footer>Sanitized aggregate view · no internal content is exposed on this page.</footer>
</div>
</body>
</html>
"""


def _sparkline(points: list[int]) -> str:
    if len(points) < 2:
        return '<div class="sub">Trend appears once there are at least two daily snapshots.</div>'
    lo, hi = min(points), max(points)
    span = (hi - lo) or 1
    n = len(points)
    coords = []
    for i, v in enumerate(points):
        x = round(100 * i / (n - 1), 2)
        y = round(48 - 44 * (v - lo) / span, 2)
        coords.append(f"{x},{y}")
    return (f'<svg class="spark" viewBox="0 0 100 52" preserveAspectRatio="none">'
            f'<path d="M{"L".join(coords)}"/></svg>')


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true",
                        help="emit the verdict + metrics as JSON (for CI alerting)")
    args = parser.parse_args()

    today = date.today()
    scanned = scan(today)
    history, previous = update_history(scanned)
    healthy, reasons = verdict(scanned, previous)

    HEALTH_MD.write_text(render_md(scanned, previous, healthy, reasons), encoding="utf-8")
    HEALTH_HTML.write_text(render_html(scanned, history, healthy), encoding="utf-8")

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
        print(f"Wrote {HEALTH_MD.name}, {HEALTH_HTML.name}, {HISTORY_PATH.name}")


if __name__ == "__main__":
    main()
