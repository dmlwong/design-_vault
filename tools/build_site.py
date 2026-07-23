#!/usr/bin/env python3
"""Build the public team-share site for the Orbit Design Brain.

Assembles a small static site — a curated hub plus the living tools it links —
from vault sources and ``tools/site-manifest.json``. This is the "anyone with
the link" surface: the intake form and the sanitized health dashboard, one URL,
no infrastructure beyond GitHub Pages.

Two build modes:

- default (internal preview): copies tool sources verbatim.
- ``--public``: runs the sanitiser over every emitted file so product-surface
  and company names never reach a public URL, then **asserts** none survive —
  the build fails loudly if a blocked term leaks. CI publishes with ``--public``.

Usage::

    python3 tools/build_site.py --out site            # internal preview
    python3 tools/build_site.py --out site --public    # what CI publishes

Outputs into ``--out`` (default ``site/``): ``index.html`` (the hub),
one file per tool (``intake-form.html``, ``health.html``), and ``.nojekyll``
so GitHub Pages serves the files as-is.

The site is generated, never hand-edited. One-off prototypes and explainers
stay as private Claude Artifacts and are intentionally not part of this site;
only tools proven safe for a public link belong in the manifest.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tools" / "site-manifest.json"

# --------------------------------------------------------------------------- #
# Public sanitisation
#
# In --public mode every emitted file is rewritten through SANITISE (longest
# match first) and then checked against BLOCKLIST. The health page is already
# sanitised upstream; this is the guarantee for the intake form, which names
# product surfaces the vault treats as private (mirrors the health page's
# platform-profile exclusion). Governed edit: change the vault's private-name
# policy and this list together.
# --------------------------------------------------------------------------- #
SANITISE: list[tuple[str, str]] = [
    ("Orbit / Client Connected Platform (external)", "External (client) platform"),
    ("Connected Platform (internal)", "Internal platform"),
    ("ClauseIQ", "Contract workflows"),
    ("MarketIQ", "Market intelligence"),
    ("RFP Analytics", "Sourcing analytics"),
    ("RFP Builder", "RFP authoring"),
    ("Efficio", "the platform"),
]

# Proper nouns that must never appear on the public site. Checked
# case-insensitively after SANITISE runs.
BLOCKLIST = [
    "ClauseIQ",
    "MarketIQ",
    "RFP Analytics",
    "RFP Builder",
    "Efficio",
    "Client Connected Platform",
]


def sanitise(text: str) -> str:
    for needle, repl in SANITISE:
        text = text.replace(needle, repl)
    return text


def assert_clean(name: str, text: str) -> None:
    low = text.lower()
    hits = [term for term in BLOCKLIST if term.lower() in low]
    if hits:
        raise SystemExit(
            f"REFUSING TO PUBLISH: {name} still contains blocked term(s): "
            + ", ".join(sorted(set(hits)))
            + "\nExtend SANITISE in tools/build_site.py (or fix the source) and rebuild."
        )


# --------------------------------------------------------------------------- #
# Hub page
# --------------------------------------------------------------------------- #
HUB_STYLE = """
  :root{
    --bg:#f4f6fa;--panel:#fff;--panel-2:#eef1f7;--ink:#151b26;--muted:#59636f;
    --line:#e2e7ef;--accent:#0e7c86;--accent-ink:#0a5b62;
    --shadow:0 1px 2px rgba(21,27,38,.05),0 9px 24px rgba(21,27,38,.06);
  }
  @media (prefers-color-scheme:dark){:root{
    --bg:#0a0e15;--panel:#131a24;--panel-2:#0e141d;--ink:#e7ecf3;--muted:#93a0b1;
    --line:#222c39;--accent:#2dd4bf;--accent-ink:#7ff0dd;
    --shadow:0 1px 2px rgba(0,0,0,.4),0 12px 30px rgba(0,0,0,.5);}}
  :root[data-theme=light]{
    --bg:#f4f6fa;--panel:#fff;--panel-2:#eef1f7;--ink:#151b26;--muted:#59636f;
    --line:#e2e7ef;--accent:#0e7c86;--accent-ink:#0a5b62;
    --shadow:0 1px 2px rgba(21,27,38,.05),0 9px 24px rgba(21,27,38,.06);}
  :root[data-theme=dark]{
    --bg:#0a0e15;--panel:#131a24;--panel-2:#0e141d;--ink:#e7ecf3;--muted:#93a0b1;
    --line:#222c39;--accent:#2dd4bf;--accent-ink:#7ff0dd;
    --shadow:0 1px 2px rgba(0,0,0,.4),0 12px 30px rgba(0,0,0,.5);}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    line-height:1.5;-webkit-font-smoothing:antialiased}
  .wrap{max-width:720px;margin:0 auto;padding:44px 20px 64px}
  .eyebrow{font-size:11px;letter-spacing:.15em;text-transform:uppercase;color:var(--muted);font-weight:650}
  h1{font-size:25px;letter-spacing:-.02em;margin:8px 0 0;font-weight:700}
  .lede{margin:12px 0 0;font-size:14.5px;color:var(--muted);max-width:62ch}
  .group{display:flex;flex-direction:column;gap:10px;margin-top:26px}
  a.row{display:grid;grid-template-columns:1fr auto;gap:14px;align-items:center;
    text-decoration:none;color:inherit;background:var(--panel);border:1px solid var(--line);
    border-radius:14px;box-shadow:var(--shadow);padding:18px 20px;position:relative;
    transition:border-color .12s ease,transform .12s ease}
  a.row:hover{border-color:var(--accent);transform:translateY(-1px)}
  a.row:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
  a.row::before{content:"";position:absolute;left:0;top:12px;bottom:12px;width:3px;
    border-radius:3px;background:var(--accent)}
  .meta{min-width:0}
  .meta .t{font-weight:660;font-size:16px;letter-spacing:-.01em;display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
  .meta .d{font-size:13px;color:var(--muted);margin-top:5px;max-width:56ch}
  .chip{font-size:10.5px;font-weight:700;letter-spacing:.03em;text-transform:uppercase;
    padding:3px 9px;border-radius:999px;white-space:nowrap;color:#fff;background:var(--accent)}
  .open{font-size:13px;font-weight:650;color:var(--accent-ink);white-space:nowrap}
  a.row:hover .open{text-decoration:underline}
  footer{margin-top:36px;padding-top:18px;border-top:1px solid var(--line);
    color:var(--muted);font-size:12.5px;line-height:1.6}
  @media (prefers-reduced-motion:reduce){a.row{transition:none}}
  @media (max-width:560px){.open{display:none}}
"""


def render_hub(manifest: dict) -> str:
    site = manifest["site"]
    rows = []
    for tool in manifest["tools"]:
        rows.append(
            '    <a class="row" href="{href}">\n'
            '      <div class="meta"><div class="t">{title}'
            '<span class="chip">{tag}</span></div>'
            '<div class="d">{blurb}</div></div>\n'
            '      <span class="open">Open&nbsp;&rarr;</span>\n'
            "    </a>".format(
                href=html.escape(tool["href"]),
                title=html.escape(tool["title"]),
                tag=html.escape(tool["tag"]),
                blurb=html.escape(tool["blurb"]),
            )
        )
    body = "\n".join(rows)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(site['title'])}</title>
<style>{HUB_STYLE}</style>
</head>
<body>
  <div class="wrap">
    <div class="eyebrow">{html.escape(site['eyebrow'])}</div>
    <h1>{html.escape(site['title'])}</h1>
    <p class="lede">{html.escape(site['tagline'])}</p>
    <div class="group">
{body}
    </div>
    <footer>
      These tools run entirely in your browser &mdash; nothing you type is sent anywhere.
      This page is generated from the design vault; it is not hand-edited.
    </footer>
  </div>
</body>
</html>
"""


# --------------------------------------------------------------------------- #
# Build
# --------------------------------------------------------------------------- #
def build(out: Path, public: bool) -> list[str]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    out.mkdir(parents=True, exist_ok=True)
    written: list[str] = []

    # Hub
    hub = render_hub(manifest)
    if public:
        hub = sanitise(hub)
        assert_clean("index.html", hub)
    (out / "index.html").write_text(hub, encoding="utf-8")
    written.append("index.html")

    # Tools
    for tool in manifest["tools"]:
        src = ROOT / tool["source"]
        if not src.is_file():
            raise SystemExit(
                f"Missing tool source for '{tool['id']}': {tool['source']} not found. "
                "Generate it first (e.g. `python3 tools/vault_health.py` writes vault-health.html)."
            )
        text = src.read_text(encoding="utf-8")
        if public:
            text = sanitise(text)
            assert_clean(tool["href"], text)
        (out / tool["href"]).write_text(text, encoding="utf-8")
        written.append(tool["href"])

    # Pages: serve files verbatim (no Jekyll processing).
    (out / ".nojekyll").write_text("", encoding="utf-8")
    written.append(".nojekyll")
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", default="site", metavar="DIR",
                        help="output directory (default: site)")
    parser.add_argument("--public", action="store_true",
                        help="sanitise product/company names and refuse to build if any survive")
    args = parser.parse_args()

    out = (ROOT / args.out) if not Path(args.out).is_absolute() else Path(args.out)
    written = build(out, args.public)
    mode = "PUBLIC (sanitised)" if args.public else "internal"
    print(f"Built {mode} site in {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}:")
    for name in written:
        print(f"  - {name}")


if __name__ == "__main__":
    main()
