#!/usr/bin/env python3
"""Generate ``artifacts/index.html`` — the in-repo, clickable index of deliverables.

Reads ``tools/artifacts-manifest.json`` and writes a real web page under
``artifacts/`` whose links point at the in-repo copies (``file``) with a fallback
to the live Claude Artifact (``url``) for anything not yet copied in. Because this
is an ordinary page — not a rendered artifact — the links actually work: open
``artifacts/index.html`` in a browser and every deliverable opens.

This is the single central viewer: source + index all live in the repo. Generated,
never hand-edited; re-run after editing the manifest.

    python3 tools/build_artifacts_index.py
"""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tools" / "artifacts-manifest.json"
OUT = ROOT / "artifacts" / "index.html"

STYLE = """
 :root{--bg:#eef1f6;--panel:#fff;--panel-2:#f4f7fb;--ink:#151b26;--muted:#5a6472;
  --line:#e0e6ee;--accent:#0e7c86;--accent-ink:#0a5b62;--warn:#c2410c;
  --shadow:0 1px 2px rgba(21,27,38,.05),0 9px 24px rgba(21,27,38,.06)}
 @media (prefers-color-scheme:dark){:root{--bg:#0a0e15;--panel:#131a24;--panel-2:#0e141d;
  --ink:#e7ecf3;--muted:#93a0b1;--line:#222c39;--accent:#2dd4bf;--accent-ink:#7ff0dd;--warn:#f0894e;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 12px 30px rgba(0,0,0,.5)}}
 :root[data-theme=light]{--bg:#eef1f6;--panel:#fff;--panel-2:#f4f7fb;--ink:#151b26;--muted:#5a6472;
  --line:#e0e6ee;--accent:#0e7c86;--accent-ink:#0a5b62;--warn:#c2410c;
  --shadow:0 1px 2px rgba(21,27,38,.05),0 9px 24px rgba(21,27,38,.06)}
 :root[data-theme=dark]{--bg:#0a0e15;--panel:#131a24;--panel-2:#0e141d;--ink:#e7ecf3;--muted:#93a0b1;
  --line:#222c39;--accent:#2dd4bf;--accent-ink:#7ff0dd;--warn:#f0894e;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 12px 30px rgba(0,0,0,.5)}
 *{box-sizing:border-box}
 body{margin:0;background:var(--bg);color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;line-height:1.55}
 .wrap{max-width:730px;margin:0 auto;padding:46px 20px 66px}
 .eyebrow{font-family:ui-monospace,Menlo,monospace;font-size:11px;letter-spacing:.15em;
  text-transform:uppercase;color:var(--accent-ink);font-weight:600}
 :root[data-theme=dark] .eyebrow{color:var(--accent)}
 @media (prefers-color-scheme:dark){.eyebrow{color:var(--accent)}}
 h1{font-size:26px;letter-spacing:-.02em;margin:8px 0 0;font-weight:700}
 .lede{margin:12px 0 0;font-size:14px;color:var(--muted);max-width:62ch}
 .note{margin-top:16px;font-size:12.5px;color:var(--muted);background:var(--panel-2);
  border:1px solid var(--line);border-radius:10px;padding:11px 14px}
 .grp{margin-top:30px}
 .gh{display:flex;align-items:baseline;gap:9px;margin:0 0 3px}
 .gn{font-size:12.5px;font-weight:700;text-transform:uppercase;letter-spacing:.06em}
 .gc{font-size:11.5px;font-weight:600;color:var(--muted)}
 .gb{font-size:12.5px;color:var(--muted);margin:0 0 12px}
 .list{display:flex;flex-direction:column;gap:8px}
 a.row{display:grid;grid-template-columns:1fr auto auto;gap:12px;align-items:center;text-decoration:none;
  color:inherit;background:var(--panel);border:1px solid var(--line);border-radius:12px;
  box-shadow:var(--shadow);padding:14px 16px;transition:border-color .12s,transform .12s}
 a.row:hover{border-color:var(--accent);transform:translateY(-1px)}
 a.row:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
 .t{font-weight:640;font-size:14px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
 .tag{font-size:10px;font-weight:700;letter-spacing:.03em;text-transform:uppercase;color:var(--accent);
  background:color-mix(in srgb,var(--accent) 12%,transparent);border-radius:999px;padding:3px 9px;white-space:nowrap}
 .tag.ext{color:var(--warn);background:color-mix(in srgb,var(--warn) 13%,transparent)}
 .open{font-size:12.5px;font-weight:650;color:var(--accent-ink);white-space:nowrap}
 :root[data-theme=dark] .open{color:var(--accent)}
 @media (prefers-color-scheme:dark){.open{color:var(--accent)}}
 a.row:hover .open{text-decoration:underline}
 @media (prefers-reduced-motion:reduce){a.row{transition:none}}
 @media (max-width:560px){a.row{grid-template-columns:1fr auto}.open{display:none}}
 footer{margin-top:34px;padding-top:18px;border-top:1px solid var(--line);color:var(--muted);font-size:12px;line-height:1.6}
 code{font-family:ui-monospace,Menlo,monospace;font-size:11.5px}
"""


def build() -> str:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    groups = [g for g in data.get("groups", []) if g.get("items")]
    total = sum(len(g["items"]) for g in groups)
    in_repo = sum(1 for g in groups for it in g["items"] if it.get("file"))

    blocks = []
    for g in groups:
        rows = []
        for it in g["items"]:
            local = it.get("file")
            href = local if local else it["url"]
            target = "" if local else ' target="_blank" rel="noopener"'
            tag = html.escape(it.get("tag", ""))
            tag_html = f'<span class="tag">{tag}</span>' if tag else ""
            if not local:
                tag_html += '<span class="tag ext">Live only</span>'
            rows.append(
                f'<a class="row" href="{html.escape(href)}"{target}>'
                f'<span class="t">{html.escape(it["title"])}</span>'
                f'{tag_html}<span class="open">Open&nbsp;&rarr;</span></a>'
            )
        blocks.append(
            f'<section class="grp"><div class="gh">'
            f'<span class="gn">{html.escape(g["name"])}</span>'
            f'<span class="gc">{len(g["items"])}</span></div>'
            f'<p class="gb">{html.escape(g.get("blurb", ""))}</p>'
            f'<div class="list">{"".join(rows)}</div></section>'
        )

    ext = total - in_repo
    ext_note = (
        f" {ext} without an in-repo copy open their live Claude Artifact instead."
        if ext else ""
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Orbit Design Brain — Artifacts</title>
<style>{STYLE}</style>
</head>
<body>
  <div class="wrap">
    <div class="eyebrow">Orbit Design Brain</div>
    <h1>Artifacts</h1>
    <p class="lede">Every deliverable built from the vault, grouped. {in_repo} of {total} are stored
      right here in the repo — the links open the copy under <code>artifacts/</code>, so they work
      offline and stay versioned with everything else.{ext_note}</p>
    <div class="note">This is a normal web page, not a Claude Artifact — open <code>artifacts/index.html</code>
      in a browser and the links work. (Links inside a rendered artifact are sandboxed and can't navigate.)</div>
    {"".join(blocks)}
    <footer>Generated from <code>tools/artifacts-manifest.json</code> by
      <code>tools/build_artifacts_index.py</code> — do not hand-edit. Re-run after changing the manifest.</footer>
  </div>
</body>
</html>
"""


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
