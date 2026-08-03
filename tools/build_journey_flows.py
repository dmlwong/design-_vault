#!/usr/bin/env python3
"""Generate the interactive journey-flows page from a definition-matrix markdown file.

The Definition Pack's scenario & behaviour matrix is authored in markdown (the
canonical copy — see discovery/definition/_TEMPLATE-scenario-matrix.md); this
script projects it into the tabbed journey-flows page: overview, Green Path,
Red & Edge Paths, and Rules & Clarifications, with expandable stage-rail cards
per scenario. The output is an artifact-style fragment (a <title> + <style> +
markup, no <head>), so tools/build_site.py's inject_chrome wraps it like every
other site source. No external requests, no CDN — the page is self-contained.

The generated page is a projection: never hand-edit it, edit the matrix and rerun.

Usage:
    python3 tools/build_journey_flows.py                # golden example defaults
    python3 tools/build_journey_flows.py SRC -o OUT
    python3 tools/build_journey_flows.py --check        # regenerate + diff (CI parity)

Exit codes: 0 ok · 1 parse/validation failure · 2 --check found drift.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SRC = ROOT / "discovery" / "definition" / "clauseiq-supplier-rounds.md"
DEFAULT_OUT = ROOT / "artifacts" / "clauseiq-journey-flows.html"

# The scenario bullet fields, in rail order. Subtitle and Rules are card chrome;
# the rest form the stage rail; Worked example renders as the card footer.
SCENARIO_FIELDS = (
    "Subtitle",
    "Rules",
    "Starting state",
    "User actions",
    "Backend",
    "Front-end result",
    "Next action",
    "Expected outcome",
    "Worked example",
)
RAIL_FIELDS = (
    "Starting state",
    "User actions",
    "Backend",
    "Front-end result",
    "Next action",
    "Expected outcome",
)


@dataclass
class Rule:
    ref: str  # "R1" / "C1"
    title: str
    body: str
    owner: str = ""  # C-items only


@dataclass
class Scenario:
    ref: str  # "G-01" / "E-09"
    title: str
    is_open: bool = False  # "(open)" suffix — hangs on an unconfirmed C-item
    fields: dict = field(default_factory=dict)


@dataclass
class Matrix:
    concept: str
    meta_line: str
    rules: list
    clarifications: list
    green: list
    edge: list


def fail(msg: str) -> None:
    raise SystemExit(f"build_journey_flows: {msg}")


# --------------------------------------------------------------------------- #
# Parse
# --------------------------------------------------------------------------- #
def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end == -1:
            fail("unterminated frontmatter")
        return text[end + 4 :]
    return text


def parse(src: Path) -> Matrix:
    text = strip_frontmatter(src.read_text(encoding="utf-8"))
    # Drop the generated graph-links block and HTML comments.
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)

    m = re.search(r"^# Scenario & Behaviour Matrix:\s*(.+)$", text, re.M)
    if not m:
        fail(f"{src.name}: missing '# Scenario & Behaviour Matrix: <name>' heading")
    concept = m.group(1).strip()

    # The meta line is a paragraph and may wrap — capture until the blank line.
    meta = re.search(r"^\*\*Source Concept Pack:\*\*\s*(.+?)(?:\n\s*\n|\Z)", text, re.M | re.S)
    meta_line = ""
    if meta:
        meta_line = "Source Concept Pack: " + " ".join(
            l.strip() for l in meta.group(1).splitlines() if l.strip()
        )
    meta_line = re.sub(r"\s*·\s*\*\*Working draft:\*\*\s*", " · Working draft: ", meta_line)
    meta_line = meta_line.replace("**", "")

    # Split into ## sections.
    sections: dict[str, str] = {}
    for sec in re.split(r"^## ", text, flags=re.M)[1:]:
        name, _, body = sec.partition("\n")
        sections[name.strip()] = body

    def section(name: str) -> str:
        for key, body in sections.items():
            if key.lower().startswith(name.lower()):
                return body
        fail(f"{src.name}: missing '## {name}' section")

    def h3_blocks(body: str):
        """Yield (heading, block-body) for each ### in a section, skipping doc-note quotes."""
        for blk in re.split(r"^### ", body, flags=re.M)[1:]:
            head, _, rest = blk.partition("\n")
            yield head.strip(), rest

    def para(body: str) -> str:
        lines = [l.strip() for l in body.splitlines() if l.strip() and not l.strip().startswith(">")]
        return " ".join(lines)

    def parse_rules(body: str, kind: str) -> list:
        out = []
        for head, rest in h3_blocks(body):
            hm = re.match(rf"({kind}\d+)\s*·\s*(.+)", head)
            if not hm:
                fail(f"{src.name}: bad {kind}-heading '### {head}' (want '### {kind}<n> · <name>')")
            text_body = para(rest)
            owner = ""
            if kind == "C":
                om = re.search(r"Owner:\s*(.+?)\.?\s*$", text_body)
                if not om:
                    fail(f"{src.name}: clarification {hm.group(1)} has no trailing 'Owner: <team>'")
                owner = om.group(1).strip()
                text_body = text_body[: om.start()].strip()
            out.append(Rule(hm.group(1), hm.group(2).strip(), text_body, owner))
        return out

    def parse_scenarios(body: str, prefix: str) -> list:
        out = []
        for head, rest in h3_blocks(body):
            hm = re.match(rf"({prefix}-\d+)\s*·\s*(.+)", head)
            if not hm:
                fail(f"{src.name}: bad scenario heading '### {head}' (want '### {prefix}-NN · <title>')")
            title = hm.group(2).strip()
            is_open = bool(re.search(r"\(open\)\s*$", title))
            title = re.sub(r"\s*\(open\)\s*$", "", title)
            sc = Scenario(hm.group(1), title, is_open)
            current = None
            for line in rest.splitlines():
                bm = re.match(r"-\s+\*\*(.+?):\*\*\s*(.*)", line.strip())
                if bm:
                    current = bm.group(1).strip()
                    if current not in SCENARIO_FIELDS:
                        fail(f"{src.name}: {sc.ref} has unknown field '{current}'")
                    sc.fields[current] = bm.group(2).strip()
                elif current and line.strip() and not line.strip().startswith(">"):
                    sc.fields[current] += " " + line.strip()
            missing = [f for f in SCENARIO_FIELDS if f not in sc.fields]
            if missing:
                fail(f"{src.name}: {sc.ref} missing field(s): {', '.join(missing)}")
            out.append(sc)
        return out

    matrix = Matrix(
        concept=concept,
        meta_line=meta_line,
        rules=parse_rules(section("Key rules"), "R"),
        clarifications=parse_rules(section("Open clarifications"), "C"),
        green=parse_scenarios(section("Green Path"), "G"),
        edge=parse_scenarios(section("Red & Edge Paths"), "E"),
    )

    # Validate: every Rules: ref resolves to a known R/C item; refs unique.
    known = {r.ref for r in matrix.rules} | {c.ref for c in matrix.clarifications}
    seen: set[str] = set()
    for sc in matrix.green + matrix.edge:
        if sc.ref in seen:
            fail(f"{src.name}: duplicate scenario ref {sc.ref}")
        seen.add(sc.ref)
        for ref in re.split(r"[,\s]+", sc.fields["Rules"].strip()):
            if not ref:
                continue
            if not re.fullmatch(r"[RC]\d+", ref):
                fail(f"{src.name}: {sc.ref} Rules ref '{ref}' is not R<n>/C<n>")
            if ref not in known:
                fail(f"{src.name}: {sc.ref} references unknown rule '{ref}'")
    return matrix


# --------------------------------------------------------------------------- #
# Render
# --------------------------------------------------------------------------- #
def esc(text: str) -> str:
    return html.escape(text, quote=False)


def inline(text: str) -> str:
    """Escape, then apply the only inline markdown the matrix uses: bold + code."""
    out = esc(text)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    return out


def ref_id(ref: str) -> str:
    return ref.lower()


def rule_chips(rules_field: str) -> str:
    chips = []
    for ref in re.split(r"[,\s]+", rules_field.strip()):
        if ref:
            chips.append(f'<a class="rchip" href="#{ref_id(ref)}">{esc(ref)}</a>')
    return "".join(chips)


def scenario_card(sc: Scenario, kind: str) -> str:
    open_pill = '<span class="pill pill-open">open</span>' if sc.is_open else ""
    rail = []
    for name in RAIL_FIELDS:
        key = name.lower().replace(" ", "-").replace("front-end", "frontend")
        rail.append(
            f'<div class="st st-{key}"><div class="st-k">{esc(name)}</div>'
            f'<div class="st-v">{inline(sc.fields[name])}</div></div>'
        )
    return f"""<details class="sc sc-{kind}" id="{ref_id(sc.ref)}">
<summary>
  <span class="ref ref-{kind}">{esc(sc.ref)}</span>
  <span class="sc-head"><span class="sc-title">{inline(sc.title)}{open_pill}</span>
  <span class="sc-sub">{inline(sc.fields["Subtitle"])}</span></span>
  <span class="chev" aria-hidden="true"></span>
</summary>
<div class="sc-body">
  <div class="sc-rules"><span class="sc-rules-k">Rules</span>{rule_chips(sc.fields["Rules"])}</div>
  <div class="rail">{"".join(rail)}</div>
  <div class="worked"><div class="st-k">Worked example</div><div class="st-v">{inline(sc.fields["Worked example"])}</div></div>
</div>
</details>"""


def overview_item(sc: Scenario, kind: str) -> str:
    open_pill = '<span class="pill pill-open">open</span>' if sc.is_open else ""
    return (
        f'<a class="ov" href="#{ref_id(sc.ref)}">'
        f'<span class="ref ref-{kind}">{esc(sc.ref)}</span>'
        f'<span class="ov-t"><span class="ov-title">{inline(sc.title)}{open_pill}</span>'
        f'<span class="ov-sub">{inline(sc.fields["Subtitle"])}</span></span></a>'
    )


def rule_card(r: Rule, kind: str) -> str:
    owner = f'<span class="pill pill-owner">Owner · {esc(r.owner)}</span>' if r.owner else ""
    return (
        f'<article class="rule rule-{kind}" id="{ref_id(r.ref)}">'
        f'<div class="rule-head"><span class="ref ref-{kind}">{esc(r.ref)}</span>'
        f'<h3>{inline(r.title)}</h3>{owner}</div>'
        f'<p>{inline(r.body)}</p></article>'
    )


def render(matrix: Matrix, src: Path) -> str:
    src_rel = src.resolve().relative_to(ROOT).as_posix()
    green_cards = "\n".join(scenario_card(s, "g") for s in matrix.green)
    edge_cards = "\n".join(scenario_card(s, "e") for s in matrix.edge)
    ov_green = "\n".join(overview_item(s, "g") for s in matrix.green)
    ov_edge = "\n".join(overview_item(s, "e") for s in matrix.edge)
    r_cards = "\n".join(rule_card(r, "r") for r in matrix.rules)
    c_cards = "\n".join(rule_card(c, "c") for c in matrix.clarifications)
    n_open = sum(1 for s in matrix.edge if s.is_open)
    open_note = f" · {n_open} open" if n_open else ""
    meta_html = f'<p class="meta">{esc(matrix.meta_line)}</p>' if matrix.meta_line else ""

    return f"""<!-- generated by tools/build_journey_flows.py from {src_rel} — do not hand-edit.
     Edit the matrix and rerun: python3 tools/build_journey_flows.py -->
<title>{esc(matrix.concept)} · Journey flows</title>
<style>
  :root {{
    --bg: #EFF1F4; --surface: #FFFFFF; --surface-2: #E7EAEF;
    --ink: #171C26; --ink-soft: #566173; --ink-faint: #8A93A3;
    --line: #DBDFE6; --line-strong: #C6CCD6;
    --accent: #2450B8; --accent-ink: #1C3F96; --accent-2: #6D3BD1; --accent-2-ink: #59309F;
    --good: #2F7D58; --good-bg: #E4F1EA; --warn: #B07817; --warn-bg: #F7EDDA;
    --crit: #BC3B2E; --crit-bg: #F8E7E4;
    --font-sans: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    --font-serif: Charter, "Bitstream Charter", "Iowan Old Style", Georgia, "Times New Roman", serif;
    --font-mono: ui-monospace, "SF Mono", "JetBrains Mono", "Cascadia Code", Menlo, Consolas, monospace;
    --maxw: 940px; --radius: 14px; --radius-sm: 9px;
    --shadow: 0 1px 2px rgba(20,28,42,0.04), 0 8px 30px rgba(20,28,42,0.06);
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg: #0D1118; --surface: #141A24; --surface-2: #1B2330;
      --ink: #E9ECF2; --ink-soft: #98A4B6; --ink-faint: #647082;
      --line: #26303D; --line-strong: #33404F;
      --accent: #7EA6FF; --accent-ink: #9DBCFF; --accent-2: #A883F2; --accent-2-ink: #C3AEF8;
      --good: #4FB483; --good-bg: #14261E; --warn: #E0A63E; --warn-bg: #2A2113;
      --crit: #E5695B; --crit-bg: #2B1714;
      --shadow: 0 1px 2px rgba(0,0,0,0.3), 0 12px 40px rgba(0,0,0,0.35);
    }}
  }}
  :root[data-theme="light"] {{
    --bg: #EFF1F4; --surface: #FFFFFF; --surface-2: #E7EAEF;
    --ink: #171C26; --ink-soft: #566173; --ink-faint: #8A93A3;
    --line: #DBDFE6; --line-strong: #C6CCD6;
    --accent: #2450B8; --accent-ink: #1C3F96; --accent-2: #6D3BD1; --accent-2-ink: #59309F;
    --good: #2F7D58; --good-bg: #E4F1EA; --warn: #B07817; --warn-bg: #F7EDDA;
    --crit: #BC3B2E; --crit-bg: #F8E7E4;
    --shadow: 0 1px 2px rgba(20,28,42,0.04), 0 8px 30px rgba(20,28,42,0.06);
  }}
  :root[data-theme="dark"] {{
    --bg: #0D1118; --surface: #141A24; --surface-2: #1B2330;
    --ink: #E9ECF2; --ink-soft: #98A4B6; --ink-faint: #647082;
    --line: #26303D; --line-strong: #33404F;
    --accent: #7EA6FF; --accent-ink: #9DBCFF; --accent-2: #A883F2; --accent-2-ink: #C3AEF8;
    --good: #4FB483; --good-bg: #14261E; --warn: #E0A63E; --warn-bg: #2A2113;
    --crit: #E5695B; --crit-bg: #2B1714;
    --shadow: 0 1px 2px rgba(0,0,0,0.3), 0 12px 40px rgba(0,0,0,0.35);
  }}

  * {{ box-sizing: border-box; }}
  body {{ margin: 0; }}
  .page {{ background: var(--bg); color: var(--ink); font-family: var(--font-sans);
    line-height: 1.6; -webkit-font-smoothing: antialiased; letter-spacing: -0.005em; min-height: 100vh; }}
  .wrap {{ max-width: var(--maxw); margin: 0 auto; padding: 0 22px; }}
  code {{ font-family: var(--font-mono); font-size: 0.88em; background: var(--surface-2);
    padding: 0.08em 0.35em; border-radius: 5px; }}
  a {{ color: var(--accent-ink); }}

  .jf-hero {{ padding: 46px 0 8px; }}
  .eyebrow {{ font-family: var(--font-mono); font-size: 0.72rem; letter-spacing: 0.16em;
    text-transform: uppercase; color: var(--accent-ink); margin: 0 0 14px;
    display: flex; align-items: center; gap: 10px; }}
  .eyebrow::before {{ content: ""; width: 22px; height: 1px; background: var(--accent); }}
  h1 {{ font-family: var(--font-serif); font-weight: 640; letter-spacing: -0.015em;
    font-size: clamp(1.7rem, 4vw, 2.5rem); line-height: 1.1; margin: 0; text-wrap: balance; }}
  .lede {{ margin: 12px 0 0; color: var(--ink-soft); max-width: 62ch;
    font-size: clamp(0.98rem, 1.5vw, 1.08rem); }}
  .meta {{ margin: 14px 0 0; font-size: 0.82rem; color: var(--ink-faint);
    font-family: var(--font-mono); }}

  /* Tabs: hidden without JS — every panel then renders stacked, so the page
     degrades to a scrollable document. */
  .jf-tabs {{ display: none; }}
  .js .jf-tabs {{ display: flex; gap: 6px; flex-wrap: wrap; position: sticky; top: 0; z-index: 30;
    padding: 12px 0; margin-top: 22px;
    background: color-mix(in srgb, var(--bg) 90%, transparent); backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--line); }}
  .jf-tab {{ appearance: none; border: 1px solid var(--line); background: var(--surface);
    color: var(--ink-soft); font: inherit; font-size: 0.86rem; font-weight: 620;
    padding: 7px 14px; border-radius: 999px; cursor: pointer; }}
  .jf-tab:hover {{ border-color: var(--line-strong); color: var(--ink); }}
  .jf-tab[aria-selected="true"] {{ background: var(--ink); color: var(--bg); border-color: var(--ink); }}
  .jf-tab:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
  .jf-tab .n {{ opacity: 0.65; font-weight: 500; margin-left: 5px; }}

  .jf-panel {{ padding: 22px 0 8px; }}
  .js .jf-panel[hidden] {{ display: none; }}
  .jf-panel > h2 {{ font-family: var(--font-serif); font-weight: 640; letter-spacing: -0.015em;
    font-size: 1.35rem; margin: 0 0 4px; }}
  .js .jf-panel > h2 {{ position: absolute; width: 1px; height: 1px; overflow: hidden;
    clip: rect(0 0 0 0); white-space: nowrap; }} /* tabs already name the panel */
  .jf-panel > .p-lede {{ margin: 0 0 18px; color: var(--ink-soft); font-size: 0.94rem; max-width: 68ch; }}

  .ref {{ font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.04em; padding: 3px 9px; border-radius: 999px; white-space: nowrap;
    flex: none; border: 1px solid transparent; }}
  .ref-g {{ background: var(--good-bg); color: var(--good); border-color: color-mix(in srgb, var(--good) 35%, transparent); }}
  .ref-e {{ background: var(--crit-bg); color: var(--crit); border-color: color-mix(in srgb, var(--crit) 35%, transparent); }}
  .ref-r {{ background: color-mix(in srgb, var(--accent) 12%, transparent); color: var(--accent-ink);
    border-color: color-mix(in srgb, var(--accent) 35%, transparent); }}
  .ref-c {{ background: color-mix(in srgb, var(--accent-2) 12%, transparent); color: var(--accent-2-ink);
    border-color: color-mix(in srgb, var(--accent-2) 35%, transparent); }}
  .pill {{ font-size: 0.66rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase;
    padding: 2px 8px; border-radius: 999px; margin-left: 8px; vertical-align: 2px; white-space: nowrap; }}
  .pill-open {{ background: var(--warn-bg); color: var(--warn); }}
  .pill-owner {{ background: var(--surface-2); color: var(--ink-soft); margin-left: auto; }}

  /* Overview */
  .ov-group {{ margin-bottom: 26px; }}
  .ov-group h3 {{ font-size: 0.78rem; letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--ink-faint); font-family: var(--font-mono); margin: 0 0 10px; font-weight: 650; }}
  .ov-list {{ display: flex; flex-direction: column; gap: 8px; }}
  .ov {{ display: flex; gap: 12px; align-items: baseline; text-decoration: none; color: inherit;
    background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius-sm);
    padding: 11px 14px; transition: border-color 0.12s ease; }}
  .ov:hover {{ border-color: var(--accent); }}
  .ov:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
  .ov-t {{ min-width: 0; }}
  .ov-title {{ display: block; font-weight: 630; font-size: 0.95rem; letter-spacing: -0.01em; }}
  .ov-sub {{ display: block; font-size: 0.83rem; color: var(--ink-soft); margin-top: 2px; }}

  /* Scenario cards */
  .sc {{ background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius);
    box-shadow: var(--shadow); margin-bottom: 12px; overflow: hidden; }}
  .sc[open] {{ border-color: var(--line-strong); }}
  .sc > summary {{ display: flex; gap: 13px; align-items: baseline; padding: 15px 18px;
    cursor: pointer; list-style: none; }}
  .sc > summary::-webkit-details-marker {{ display: none; }}
  .sc > summary:focus-visible {{ outline: 2px solid var(--accent); outline-offset: -2px;
    border-radius: var(--radius); }}
  .sc-head {{ min-width: 0; flex: 1; }}
  .sc-title {{ display: block; font-weight: 650; font-size: 1rem; letter-spacing: -0.01em; }}
  .sc-sub {{ display: block; font-size: 0.85rem; color: var(--ink-soft); margin-top: 3px; }}
  .chev {{ flex: none; width: 9px; height: 9px; border-right: 2px solid var(--ink-faint);
    border-bottom: 2px solid var(--ink-faint); transform: rotate(45deg) translateY(-2px);
    transition: transform 0.15s ease; align-self: center; }}
  .sc[open] > summary .chev {{ transform: rotate(225deg) translateY(-1px); }}
  @media (prefers-reduced-motion: reduce) {{ .chev {{ transition: none; }} }}
  .sc-body {{ padding: 2px 18px 18px; border-top: 1px solid var(--line); }}
  .sc-rules {{ display: flex; gap: 6px; align-items: center; flex-wrap: wrap; padding: 13px 0 4px; }}
  .sc-rules-k {{ font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase;
    color: var(--ink-faint); font-family: var(--font-mono); font-weight: 650; margin-right: 2px; }}
  .rchip {{ font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700;
    text-decoration: none; padding: 2px 8px; border-radius: 999px;
    background: color-mix(in srgb, var(--accent) 10%, transparent); color: var(--accent-ink);
    border: 1px solid color-mix(in srgb, var(--accent) 30%, transparent); }}
  .rchip:hover {{ background: color-mix(in srgb, var(--accent) 18%, transparent); }}
  .rchip:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}

  /* Stage rail: the user → backend → front-end → next → outcome spine. */
  .rail {{ margin-top: 10px; }}
  .st {{ position: relative; padding: 0 0 14px 22px; }}
  .st::before {{ content: ""; position: absolute; left: 4px; top: 7px; width: 8px; height: 8px;
    border-radius: 50%; background: var(--ink-faint); }}
  .st::after {{ content: ""; position: absolute; left: 7.5px; top: 19px; bottom: 2px; width: 1px;
    background: var(--line-strong); }}
  .st:last-child::after {{ display: none; }}
  .st-user-actions::before {{ background: var(--accent); }}
  .st-backend::before {{ background: var(--accent-2); }}
  .st-frontend-result::before {{ background: var(--good); }}
  .st-expected-outcome::before {{ background: var(--ink); }}
  .st-k {{ font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase;
    color: var(--ink-faint); font-family: var(--font-mono); font-weight: 650; }}
  .st-v {{ font-size: 0.92rem; margin-top: 2px; max-width: 72ch; }}
  .worked {{ margin-top: 6px; background: var(--surface-2); border-radius: var(--radius-sm);
    padding: 12px 14px; }}
  .worked .st-v {{ font-size: 0.89rem; }}

  /* Rules & clarifications */
  .rule {{ background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius);
    box-shadow: var(--shadow); padding: 15px 18px; margin-bottom: 12px; }}
  .rule:target, .sc:target {{ border-color: var(--accent); }}
  .rule-head {{ display: flex; gap: 12px; align-items: baseline; flex-wrap: wrap; }}
  .rule-head h3 {{ margin: 0; font-size: 0.98rem; font-weight: 650; letter-spacing: -0.01em; }}
  .rule p {{ margin: 8px 0 0; font-size: 0.92rem; color: var(--ink-soft); max-width: 78ch; }}
  .rule-c p {{ color: var(--ink); }}
  .c-divider {{ font-size: 0.78rem; letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--ink-faint); font-family: var(--font-mono); margin: 26px 0 10px; font-weight: 650; }}

  footer.jf-foot {{ margin: 34px 0 0; padding: 18px 0 56px; border-top: 1px solid var(--line);
    color: var(--ink-faint); font-size: 0.8rem; line-height: 1.7; }}
  footer.jf-foot code {{ font-size: 0.95em; }}

  @media (max-width: 620px) {{
    .sc > summary {{ flex-wrap: wrap; }}
    .ov {{ flex-wrap: wrap; }}
    .pill-owner {{ margin-left: 0; }}
  }}
</style>

<div class="page" id="jf">
  <div class="wrap">
    <header class="jf-hero">
      <p class="eyebrow">Definition Pack · Journey flows</p>
      <h1>{esc(matrix.concept)}</h1>
      <p class="lede">The agreed end-to-end journeys and the edge behaviours that branch off
        them — every scenario expands into its stage rail: what the user does, what the backend
        does, what the front end shows, and what is guaranteed at the end.</p>
      {meta_html}
    </header>

    <div class="jf-tabs" role="tablist" aria-label="Journey flow views">
      <button class="jf-tab" role="tab" id="tab-overview" aria-controls="panel-overview" aria-selected="true">Overview</button>
      <button class="jf-tab" role="tab" id="tab-green" aria-controls="panel-green" aria-selected="false">Green Path<span class="n">{len(matrix.green)}</span></button>
      <button class="jf-tab" role="tab" id="tab-edge" aria-controls="panel-edge" aria-selected="false">Red &amp; Edge<span class="n">{len(matrix.edge)}</span></button>
      <button class="jf-tab" role="tab" id="tab-rules" aria-controls="panel-rules" aria-selected="false">Rules &amp; Clarifications<span class="n">{len(matrix.rules)}+{len(matrix.clarifications)}</span></button>
    </div>

    <section class="jf-panel" id="panel-overview" role="tabpanel" aria-labelledby="tab-overview" tabindex="-1">
      <h2>Overview</h2>
      <p class="p-lede">Every scenario at a glance. Open one to see its full stage rail.</p>
      <div class="ov-group">
        <h3>Green Path · {len(matrix.green)} scenarios</h3>
        <div class="ov-list">
{ov_green}
        </div>
      </div>
      <div class="ov-group">
        <h3>Red &amp; Edge Paths · {len(matrix.edge)} scenarios{esc(open_note)}</h3>
        <div class="ov-list">
{ov_edge}
        </div>
      </div>
    </section>

    <section class="jf-panel" id="panel-green" role="tabpanel" aria-labelledby="tab-green" tabindex="-1">
      <h2>Green Path</h2>
      <p class="p-lede">The intended end-to-end journey, in order.</p>
{green_cards}
    </section>

    <section class="jf-panel" id="panel-edge" role="tabpanel" aria-labelledby="tab-edge" tabindex="-1">
      <h2>Red &amp; Edge Paths</h2>
      <p class="p-lede">Failure and edge behaviours that branch off the Green Path — never a
        silent failure. Scenarios marked <em>open</em> hang on an unconfirmed clarification.</p>
{edge_cards}
    </section>

    <section class="jf-panel" id="panel-rules" role="tabpanel" aria-labelledby="tab-rules" tabindex="-1">
      <h2>Rules &amp; Clarifications</h2>
      <p class="p-lede">The agreed rules every journey relies on, and the open items — each with
        a named owner — that block build, not definition.</p>
{r_cards}
      <p class="c-divider">Open clarifications · {len(matrix.clarifications)} to confirm</p>
{c_cards}
    </section>

    <footer class="jf-foot">
      <p>Generated from the canonical matrix <code>{esc(src_rel)}</code> by
        <code>tools/build_journey_flows.py</code> — edit the matrix and rerun; never hand-edit
        this page. The cross-scenario master map (diagram view) is planned for v2.</p>
    </footer>
  </div>
</div>

<script>
(function () {{
  var root = document.getElementById('jf');
  root.classList.add('js');
  var tabs = Array.prototype.slice.call(root.querySelectorAll('.jf-tab'));
  var panels = Array.prototype.slice.call(root.querySelectorAll('.jf-panel'));

  function activate(tab, focusPanel) {{
    tabs.forEach(function (t) {{
      var on = t === tab;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
    }});
    panels.forEach(function (p) {{
      p.hidden = p.id !== tab.getAttribute('aria-controls');
    }});
    if (focusPanel) document.getElementById(tab.getAttribute('aria-controls')).focus();
  }}

  activate(tabs.filter(function (t) {{ return t.getAttribute('aria-selected') === 'true'; }})[0], false);

  tabs.forEach(function (tab, i) {{
    tab.tabIndex = tab.getAttribute('aria-selected') === 'true' ? 0 : -1;
    tab.addEventListener('click', function () {{ activate(tab, false); }});
    tab.addEventListener('keydown', function (e) {{
      var j = null;
      if (e.key === 'ArrowRight') j = (i + 1) % tabs.length;
      else if (e.key === 'ArrowLeft') j = (i - 1 + tabs.length) % tabs.length;
      else if (e.key === 'Home') j = 0;
      else if (e.key === 'End') j = tabs.length - 1;
      if (j !== null) {{ e.preventDefault(); tabs[j].focus(); activate(tabs[j], false); }}
    }});
  }});

  // Deep links (#g-01, #r4, overview clicks): activate the containing panel,
  // open the card if it's a <details>, then scroll to it.
  function jump() {{
    var id = location.hash.slice(1);
    if (!id) return;
    var el = document.getElementById(id);
    if (!el) return;
    var panel = el.closest('.jf-panel');
    if (panel) {{
      var tab = tabs.filter(function (t) {{ return t.getAttribute('aria-controls') === panel.id; }})[0];
      if (tab) activate(tab, false);
    }}
    if (el.tagName === 'DETAILS') el.open = true;
    el.scrollIntoView({{ block: 'start' }});
  }}
  window.addEventListener('hashchange', jump);
  jump();
}})();
</script>
"""


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("src", nargs="?", default=str(DEFAULT_SRC),
                    help="definition-matrix markdown (default: the ClauseIQ golden example)")
    ap.add_argument("-o", "--out", default=None,
                    help=f"output HTML path (default: {DEFAULT_OUT.relative_to(ROOT)})")
    ap.add_argument("--check", action="store_true",
                    help="regenerate and diff against the existing output; exit 2 on drift")
    args = ap.parse_args()

    src = Path(args.src)
    out = Path(args.out) if args.out else DEFAULT_OUT
    if not src.exists():
        fail(f"source not found: {src}")

    matrix = parse(src)
    page = render(matrix, src)

    if args.check:
        if not out.exists():
            fail(f"--check: output does not exist yet: {out}")
        if out.read_text(encoding="utf-8") != page:
            print(f"build_journey_flows: DRIFT — {out} does not match a fresh render of {src}.\n"
                  f"Run: python3 tools/build_journey_flows.py {src} -o {out}", file=sys.stderr)
            raise SystemExit(2)
        print(f"build_journey_flows: OK — {out} matches {src} "
              f"({len(matrix.green)}G/{len(matrix.edge)}E/{len(matrix.rules)}R/{len(matrix.clarifications)}C)")
        return

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"build_journey_flows: wrote {out} — {len(matrix.green)} green, {len(matrix.edge)} edge, "
          f"{len(matrix.rules)} rules, {len(matrix.clarifications)} clarifications")


if __name__ == "__main__":
    main()
