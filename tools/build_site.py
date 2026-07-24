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
    # Order matters: replacements run top-down, so put whole phrases BEFORE the
    # single-word rules (otherwise "Efficio" -> "the platform" mangles the phrase
    # it appears inside). Add new phrase rules at the top of this list.
    ("About the Vault · Efficio Orbit", "About the Vault · Orbit"),
    ("Connected Platform (internal Efficio users) and Orbit / Client Connected Platform (external clients)",
     "The internal platform (for our own teams) and the client-facing platform"),
    ("efficio-orbit repo", "the component repo"),
    ("an Efficio Context Pack", "a platform Context Pack"),
    ("Efficio Context Pack", "platform Context Pack"),
    ("The Commentary / RAID Enhancements Sponsor Intake pack",
     "A real sponsor intake pack"),
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
    # Internal initiative names that appear in the explainers' worked examples.
    # Kept as multi-word phrases on purpose: a bare "RAID" would false-positive on
    # ordinary words (e.g. "afraid").
    "Commentary / RAID",
    "RAID Enhancements",
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


# --------------------------------------------------------------------------- #
# Shared site chrome
#
# Nav + a token "skin" are injected at BUILD time, not into the source files.
# The sources double as standalone Claude Artifacts, where cross-page links are
# sandboxed and would be dead — so the chrome belongs to the site only. One nav,
# generated from the manifest: add a page there and it appears in every page's
# nav automatically.
#
# The skin unifies the NEUTRAL + ACCENT layer only. Semantic hues are left alone
# on purpose — the flow chart's teal/violet/indigo encode Govern/Explore/Port and
# the health page's green/amber/grey encode stable/in-review/draft. Consistency
# must not flatten meaning.
# --------------------------------------------------------------------------- #
SITE_NAME = "Orbit Design Brain"

CHROME_CSS = """
/* ---- injected site chrome (tools/build_site.py) ---- */
:root{
  --site-accent:#2450B8; --site-accent-ink:#1C3F96; --site-accent-2:#6D3BD1;
  --site-bg:#EFF1F5; --site-panel:#FFFFFF; --site-ink:#151B26; --site-muted:#586274;
  --site-line:#DFE4EC;
  --site-serif:Charter,"Bitstream Charter","Iowan Old Style",Georgia,serif;
}
@media (prefers-color-scheme:dark){:root{
  --site-accent:#7EA6FF; --site-accent-ink:#9DBCFF; --site-accent-2:#A883F2;
  --site-bg:#0B0F16; --site-panel:#141A24; --site-ink:#E8ECF3; --site-muted:#96A2B4;
  --site-line:#242E3B;
}}
:root[data-theme=light]{
  --site-accent:#2450B8; --site-accent-ink:#1C3F96; --site-accent-2:#6D3BD1;
  --site-bg:#EFF1F5; --site-panel:#FFFFFF; --site-ink:#151B26; --site-muted:#586274;
  --site-line:#DFE4EC;
}
:root[data-theme=dark]{
  --site-accent:#7EA6FF; --site-accent-ink:#9DBCFF; --site-accent-2:#A883F2;
  --site-bg:#0B0F16; --site-panel:#141A24; --site-ink:#E8ECF3; --site-muted:#96A2B4;
  --site-line:#242E3B;
}
/* Map each page's own neutral/accent tokens onto the site palette. Pages use
   different names for the same role, so every alias is restated. */
:root,:root[data-theme=light],:root[data-theme=dark]{
  --bg:var(--site-bg); --panel:var(--site-panel); --surface:var(--site-panel);
  --ink:var(--site-ink); --muted:var(--site-muted); --ink-soft:var(--site-muted);
  --ink-faint:var(--site-muted);
  --line:var(--site-line);
  --accent:var(--site-accent); --accent-ink:var(--site-accent-ink);
}
@media (prefers-color-scheme:dark){:root{
  --bg:var(--site-bg); --panel:var(--site-panel); --surface:var(--site-panel);
  --ink:var(--site-ink); --muted:var(--site-muted); --ink-soft:var(--site-muted);
  --ink-faint:var(--site-muted);
  --line:var(--site-line);
  --accent:var(--site-accent); --accent-ink:var(--site-accent-ink);
}}
/* --accent must stay legible as TEXT on the page ground, so in dark it is a light
   blue. That makes white-on-accent FILLS fail AA, so fills get their own ink. */
:root{--on-accent:#FFFFFF}
@media (prefers-color-scheme:dark){:root{--on-accent:#0B0F16}}
:root[data-theme=light]{--on-accent:#FFFFFF}
:root[data-theme=dark]{--on-accent:#0B0F16}
.btn-primary,.chip{color:var(--on-accent)}
/* Pilot playbook's lane chips: the tester lane was teal, which now fights the blue
   chrome. Point it at the site accent — the owner lane stays purple, so the two
   lanes remain distinguishable. */
:root{--tester:var(--site-accent)}
/* Guarantee the document itself carries the site ground. Some pages paint their
   background on an inner wrapper instead of body, which would leave the injected
   nav sitting on an unstyled (white/transparent) strip — badly wrong in dark mode. */
body{margin:0;background:var(--site-bg);color:var(--site-ink);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}

/* Page overlays must sit ABOVE the injected nav. The health dashboard's detail
   drawer is position:fixed;top:0;z-index:30 — under a z-index:200 nav its header
   and close button were unreachable (on mobile, tapping the X navigated away). */
.drawer{z-index:300}

/* The injected nav replaces any per-page brand bar — otherwise the wordmark
   renders twice, stacked. Page-level metadata that lived there (build date) is
   repeated in each page's footer, so nothing is lost. */
.topbar{display:none}

/* One display voice across every page. */
h1{font-family:var(--site-serif);font-weight:640;letter-spacing:-.015em}

/* ---- the nav itself ---- */
.sitenav{position:sticky;top:0;z-index:200;background:var(--site-bg);border-bottom:1px solid var(--site-line);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.sitenav .snwrap{max-width:1080px;margin:0 auto;padding:0 20px;display:flex;align-items:center;
  gap:20px;height:52px}
.sitenav .brand{display:flex;align-items:center;gap:9px;font-size:13.5px;font-weight:660;
  color:var(--site-ink);text-decoration:none;white-space:nowrap;letter-spacing:-.01em}
.sitenav .brand .mk{width:16px;height:16px;border-radius:50%;flex:none;position:relative}
.sitenav .brand .mk::before,.sitenav .brand .mk::after{content:"";position:absolute;inset:0;
  border-radius:50%;border:1.5px solid var(--site-accent)}
.sitenav .brand .mk::after{inset:5px;border-color:var(--site-accent-2)}
.sitenav .links{display:flex;align-items:center;gap:2px;margin-left:auto;overflow-x:auto;
  scrollbar-width:none;-ms-overflow-style:none}
.sitenav .links::-webkit-scrollbar{display:none}
/* Shield the chrome from each page's global element selectors. pilot-playbook
   ships a bare `a{border-bottom:...}` which underlined every nav item, and
   about-the-vault's line-height shrank the tap targets. State these explicitly
   so the nav is byte-identical everywhere regardless of the host page's CSS. */
.sitenav a,.sitenav a.snl,.sitenav .brand{border:0;box-shadow:none;text-decoration:none;
  text-transform:none;line-height:1.2;font-style:normal;background-image:none}
.sitenav a.snl{font-size:13px;font-weight:560;color:var(--site-muted);
  padding:8px 11px;border-radius:8px;white-space:nowrap;display:inline-block;
  transition:color .12s,background .12s}
.sitenav a.snl:hover{color:var(--site-ink);background:color-mix(in srgb,var(--site-ink) 7%,transparent)}
.sitenav a.snl:focus-visible,.sitenav .brand:focus-visible,.skip-link:focus-visible{
  outline:2px solid var(--site-accent);outline-offset:2px}
.skip-link{position:absolute;left:8px;top:-44px;z-index:300;background:var(--site-panel);
  color:var(--site-accent-ink);border:1px solid var(--site-line);border-radius:8px;
  padding:9px 14px;font-size:13px;font-weight:640;text-decoration:none;transition:top .12s}
.skip-link:focus{top:8px}
.sitenav a.snl[aria-current=page]{color:var(--site-accent-ink);
  background:color-mix(in srgb,var(--site-accent) 13%,transparent);font-weight:660}
@media (prefers-color-scheme:dark){.sitenav a.snl[aria-current=page]{color:var(--site-accent)}}
/* Mobile: wrap rather than horizontally scroll. A suppressed-scrollbar overflow
   strip hid half the site and could hide the current-page pill entirely. */
@media (max-width:720px){
  .sitenav .snwrap{gap:8px 12px;padding:8px 14px;height:auto;flex-wrap:wrap}
  .sitenav .links{margin-left:0;width:100%;flex-wrap:wrap;overflow:visible;gap:2px}
  .sitenav a.snl{padding:7px 9px;font-size:12.5px}
}
@media (prefers-reduced-motion:reduce){.sitenav a.snl,.skip-link{transition:none}}
"""


def render_nav(manifest: dict, current: str) -> str:
    """Sticky nav listing every page in the manifest, marking the current one."""
    items = [("index.html", "Home")] + [
        (t["href"], t.get("nav") or t["title"]) for t in manifest["tools"]
    ]
    links = "".join(
        '<a class="snl" href="{h}"{cur}>{label}</a>'.format(
            h=html.escape(href),
            cur=' aria-current="page"' if href == current else "",
            label=html.escape(label),
        )
        for href, label in items
    )
    return (
        '<a class="skip-link" href="#main-content">Skip to content</a>'
        '<nav class="sitenav" aria-label="Site">'
        f'<div class="snwrap"><a class="brand" href="index.html">'
        f'<span class="mk"></span><span>{html.escape(SITE_NAME)}</span></a>'
        f'<div class="links">{links}</div></div></nav>'
        '<span id="main-content" tabindex="-1"></span>'
    )


def inject_chrome(text: str, nav: str, fallback_title: str = SITE_NAME) -> str:
    """Put the nav at the top of the document and the skin at the very end.

    Sources are a mix of full documents and artifact-style fragments, so handle
    both. The skin goes last so it wins the cascade over each page's own tokens
    without needing !important.
    """
    # The nav already carries the wordmark, so a page-level eyebrow that says only
    # the site name renders it twice. Drop the exact-match ones; eyebrows that add
    # context ("About the Vault · Orbit") are left alone.
    text = re.sub(
        r'<(div|p)\s+class="eyebrow"[^>]*>\s*' + re.escape(SITE_NAME) + r'\s*</\1>',
        "", text, flags=re.I)

    skin = f"<style>{CHROME_CSS}</style>"
    m = re.search(r"<body[^>]*>", text, flags=re.I)
    if m:
        text = text[: m.end()] + "\n" + nav + text[m.end():]
        end = re.search(r"</body>", text, flags=re.I)
        if end:
            return text[: end.start()] + skin + "\n" + text[end.start():]
        return text + "\n" + skin

    # Artifact-style fragment: no document shell. Wrapping it is not cosmetic —
    # without <meta viewport> a phone reports innerWidth ~1000px and renders the
    # desktop layout scaled to ~40%, and without lang= it fails WCAG 3.1.1 (A).
    tm = re.search(r"<title>(.*?)</title>", text, flags=re.I | re.S)
    title = tm.group(1).strip() if tm else fallback_title
    if tm:
        text = text[: tm.start()] + text[tm.end():]
    return (
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{html.escape(title)}</title>\n</head>\n<body>\n"
        f"{nav}\n{text}\n{skin}\n</body>\n</html>\n"
    )


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
    hub = inject_chrome(render_hub(manifest), render_nav(manifest, "index.html"))
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
        text = inject_chrome(src.read_text(encoding="utf-8"),
                             render_nav(manifest, tool["href"]),
                             tool["title"])
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
