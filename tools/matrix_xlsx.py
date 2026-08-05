#!/usr/bin/env python3
"""Excel operator for the Definition Pack's scenario & behaviour matrix.

The people who agree behaviour — tool owners, data teams, consultants — work in Excel.
The vault needs markdown it can lint, link, diff, and generate journey flows from. This
tool is the bridge, in both directions, so neither side has to give up its surface:

    export   matrix.md  -> matrix.xlsx      hand it to the owners
    import   matrix.xlsx -> matrix.md       bring their edits back as canonical markdown
    template            -> blank.xlsx       start a new matrix from nothing
    --check                                 the round trip is exact (CI guard)

**The markdown is canonical.** The .xlsx is a working surface; anything that survives a
round trip is preserved, and the importer's serializer *defines* the canonical form:

    frontmatter verbatim · blank · H1 · blank · doc-note blockquote verbatim · blank ·
    the meta line on ONE physical line · the five sections in fixed order, one physical
    line per paragraph (no hard wrapping) · scenario bullets in the fixed nine-field
    order · trailing graph-links block verbatim · one closing newline.

`--check` asserts byte-for-byte that `import(export(golden))` and `import(golden.xlsx)`
both reproduce the golden markdown. That is only meaningful because the golden file is
stored in exactly this canonical shape — which is why it was normalised once when this
tool landed. Hard-wrapped prose is joined; no words changed. `build_journey_flows.py`
joins wrapped lines when it parses, so the generated page is provably unaffected.

Stdlib only, on purpose: CI installs nothing. An .xlsx is a zip of XML, which `zipfile`
and `xml.etree` handle fine. Writes use inline strings (no shared-strings table) and a
fixed timestamp so the same input always produces byte-identical output.

Exit codes: 0 ok · 1 parse/validation failure · 2 --check found drift.
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MD = ROOT / "discovery" / "definition" / "clauseiq-supplier-rounds.md"
DEFAULT_XLSX = ROOT / "discovery" / "definition" / "clauseiq-supplier-rounds.xlsx"

NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
RNS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

# The nine fields every scenario carries, in the order the flows generator expects.
SCENARIO_FIELDS = (
    "Subtitle", "Rules", "Starting state", "User actions", "Backend",
    "Front-end result", "Next action", "Expected outcome", "Worked example",
)
SCENARIO_COLUMNS = ("Ref", "Title", "Open") + SCENARIO_FIELDS
SHEETS = ("Meta", "Rules", "Clarifications", "Green Path", "Edge Paths")
# Excel refuses to open a workbook whose sheet name exceeds 31 chars or repeats.
assert all(len(s) <= 31 for s in SHEETS)


def fail(msg: str) -> None:
    raise SystemExit(f"matrix_xlsx: {msg}")


# --------------------------------------------------------------------------- #
# Markdown -> model
# --------------------------------------------------------------------------- #
def _unwrap(lines: list[str]) -> str:
    """Join a hard-wrapped paragraph into one logical line."""
    return " ".join(l.strip() for l in lines if l.strip())


def parse_md(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")

    frontmatter = ""
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end == -1:
            fail(f"{path.name}: unterminated frontmatter")
        frontmatter = text[: end + 4].rstrip("\n")
        body = text[end + 4:]

    graph_block = ""
    gm = re.search(r"<!-- graph-links:start.*?graph-links:end -->", body, re.S)
    if gm:
        graph_block = gm.group(0)
        body = body[: gm.start()] + body[gm.end():]

    m = re.search(r"^# Scenario & Behaviour Matrix:\s*(.+)$", body, re.M)
    if not m:
        fail(f"{path.name}: missing '# Scenario & Behaviour Matrix: <name>' heading")
    concept = m.group(1).strip()

    # The doc-note is the blockquote between the H1 and the meta line.
    head = body[m.end():]
    note_lines: list[str] = []
    for line in head.splitlines():
        if line.startswith(">"):
            note_lines.append(line)
        elif note_lines and not line.strip():
            break
        elif note_lines:
            break
    doc_note = "\n".join(note_lines)

    meta_line = ""
    mm = re.search(r"^\*\*Source Concept Pack:\*\*.*$", body, re.M)
    if mm:
        # A wrapped meta line continues until the blank line.
        rest = body[mm.start():].splitlines()
        buf = [rest[0]]
        for line in rest[1:]:
            if not line.strip() or line.startswith(("#", ">")):
                break
            buf.append(line)
        meta_line = _unwrap(buf)

    sections: dict[str, str] = {}
    for chunk in re.split(r"^## ", body, flags=re.M)[1:]:
        name, _, rest = chunk.partition("\n")
        sections[name.strip()] = rest

    def section(prefix: str) -> str:
        for key, val in sections.items():
            if key.lower().startswith(prefix.lower()):
                return val
        fail(f"{path.name}: missing '## {prefix}' section")

    def blocks(raw: str):
        for blk in re.split(r"^### ", raw, flags=re.M)[1:]:
            head_line, _, rest = blk.partition("\n")
            yield head_line.strip(), rest

    def parse_rules(raw: str, kind: str) -> list[dict]:
        out = []
        for head_line, rest in blocks(raw):
            hm = re.match(rf"({kind}\d+)\s*·\s*(.+)", head_line)
            if not hm:
                fail(f"{path.name}: bad heading '### {head_line}'")
            body_txt = _unwrap([l for l in rest.splitlines() if not l.strip().startswith(">")])
            owner = ""
            if kind == "C":
                om = re.search(r"Owner:\s*(.+?)\.?\s*$", body_txt)
                if not om:
                    fail(f"{path.name}: {hm.group(1)} has no trailing 'Owner: <team>'")
                owner = om.group(1).strip()
                body_txt = body_txt[: om.start()].strip()
            out.append({"ref": hm.group(1), "title": hm.group(2).strip(),
                        "body": body_txt, "owner": owner})
        return out

    def parse_scenarios(raw: str, prefix: str) -> list[dict]:
        out = []
        for head_line, rest in blocks(raw):
            hm = re.match(rf"({prefix}-\d+)\s*·\s*(.+)", head_line)
            if not hm:
                fail(f"{path.name}: bad scenario heading '### {head_line}'")
            title = hm.group(2).strip()
            is_open = bool(re.search(r"\(open\)\s*$", title))
            title = re.sub(r"\s*\(open\)\s*$", "", title)
            row = {"ref": hm.group(1), "title": title, "open": is_open, "fields": {}}
            current = None
            for line in rest.splitlines():
                bm = re.match(r"-\s+\*\*(.+?):\*\*\s*(.*)", line.strip())
                if bm:
                    current = bm.group(1).strip()
                    if current not in SCENARIO_FIELDS:
                        fail(f"{path.name}: {row['ref']} has unknown field '{current}'")
                    row["fields"][current] = bm.group(2).strip()
                elif current and line.strip() and not line.strip().startswith(">"):
                    row["fields"][current] += " " + line.strip()
            missing = [f for f in SCENARIO_FIELDS if f not in row["fields"]]
            if missing:
                fail(f"{path.name}: {row['ref']} missing field(s): {', '.join(missing)}")
            out.append(row)
        return out

    return {
        "concept": concept,
        "frontmatter": frontmatter,
        "doc_note": doc_note,
        "meta_line": meta_line,
        "graph_block": graph_block,
        "rules": parse_rules(section("Key rules"), "R"),
        "clarifications": parse_rules(section("Open clarifications"), "C"),
        "green": parse_scenarios(section("Green Path"), "G"),
        "edge": parse_scenarios(section("Red & Edge Paths"), "E"),
    }


# --------------------------------------------------------------------------- #
# Model -> markdown (this serializer DEFINES the canonical form)
# --------------------------------------------------------------------------- #
def render_md(model: dict) -> str:
    out: list[str] = []
    if model["frontmatter"]:
        out += [model["frontmatter"], ""]
    out += [f"# Scenario & Behaviour Matrix: {model['concept']}", ""]
    if model["doc_note"]:
        out += [model["doc_note"], ""]
    if model["meta_line"]:
        out += [model["meta_line"], ""]

    out += ["## Key rules (agreed)", ""]
    for r in model["rules"]:
        out += [f"### {r['ref']} · {r['title']}", r["body"], ""]

    out += ["## Open clarifications (to confirm)", ""]
    for c in model["clarifications"]:
        body = c["body"].rstrip()
        owner = f"{body} Owner: {c['owner']}." if body else f"Owner: {c['owner']}."
        out += [f"### {c['ref']} · {c['title']}", owner, ""]

    for heading, rows in (("## Green Path", model["green"]),
                          ("## Red & Edge Paths", model["edge"])):
        out += [heading, ""]
        for s in rows:
            title = f"{s['title']} (open)" if s["open"] else s["title"]
            out.append(f"### {s['ref']} · {title}")
            for field in SCENARIO_FIELDS:
                out.append(f"- **{field}:** {s['fields'][field]}")
            out.append("")

    if model["graph_block"]:
        out += [model["graph_block"], ""]
    text = "\n".join(out)
    return text.rstrip("\n") + "\n"


# --------------------------------------------------------------------------- #
# xlsx writing (inline strings, deterministic archive)
# --------------------------------------------------------------------------- #
def _xml_escape(value: str) -> str:
    return (value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                 .replace('"', "&quot;"))


def _col_name(idx: int) -> str:
    """1 -> A, 27 -> AA."""
    name = ""
    while idx:
        idx, rem = divmod(idx - 1, 26)
        name = chr(65 + rem) + name
    return name


# Column widths per sheet, so the workbook is editable on arrival rather than a wall of
# truncated cells. Anything past the list falls back to the last width.
_WIDTHS = {
    "Meta": [16, 90],
    "Rules": [8, 34, 96],
    "Clarifications": [8, 34, 80, 20],
    "Green Path": [8, 34, 7] + [46] * 9,
    "Edge Paths": [8, 34, 7] + [46] * 9,
}


def _sheet_xml(rows: list[list[str]], widths: list[int] | None = None) -> str:
    parts = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        f'<worksheet xmlns="{NS}">',
        # Freeze the header row: these sheets are read by scrolling, and a lost header
        # is how a cell ends up in the wrong column.
        '<sheetViews><sheetView workbookViewId="0">'
        '<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>'
        '</sheetView></sheetViews>',
        '<sheetFormatPr defaultRowHeight="15"/>',
    ]
    if widths:
        cols = "".join(
            f'<col min="{i}" max="{i}" width="{w}" customWidth="1"/>'
            for i, w in enumerate(widths, start=1))
        parts.append(f"<cols>{cols}</cols>")
    parts.append("<sheetData>")
    for r_i, row in enumerate(rows, start=1):
        cells = []
        for c_i, value in enumerate(row, start=1):
            if value is None or value == "":
                continue  # blank cells are omitted; readers use the r= attribute
            ref = f"{_col_name(c_i)}{r_i}"
            style = 1 if r_i == 1 else 0
            cells.append(
                f'<c r="{ref}" s="{style}" t="inlineStr"><is><t xml:space="preserve">'
                f"{_xml_escape(value)}</t></is></c>")
        parts.append(f'<row r="{r_i}">{"".join(cells)}</row>')
    parts.append("</sheetData></worksheet>")
    return "".join(parts)


def _model_to_sheets(model: dict) -> dict[str, list[list[str]]]:
    meta = [["Key", "Value"],
            ["concept", model["concept"]],
            ["frontmatter", model["frontmatter"]],
            ["doc_note", model["doc_note"]],
            ["meta_line", model["meta_line"]],
            ["graph_block", model["graph_block"]]]
    rules = [["Ref", "Title", "Body"]] + [[r["ref"], r["title"], r["body"]]
                                          for r in model["rules"]]
    clar = [["Ref", "Title", "Body", "Owner"]] + [
        [c["ref"], c["title"], c["body"], c["owner"]] for c in model["clarifications"]]

    def scen(rows):
        out = [list(SCENARIO_COLUMNS)]
        for s in rows:
            out.append([s["ref"], s["title"], "yes" if s["open"] else ""]
                       + [s["fields"][f] for f in SCENARIO_FIELDS])
        return out

    return {"Meta": meta, "Rules": rules, "Clarifications": clar,
            "Green Path": scen(model["green"]), "Edge Paths": scen(model["edge"])}


def write_xlsx(sheets: dict[str, list[list[str]]], out: Path) -> None:
    names = list(SHEETS)
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        + "".join(
            f'<Override PartName="/xl/worksheets/sheet{i}.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            for i in range(1, len(names) + 1))
        + '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
        "</Types>")
    root_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        "</Relationships>")
    wb = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<workbook xmlns="{NS}" xmlns:r="{RNS}"><sheets>'
        + "".join(
            f'<sheet name="{_xml_escape(n)}" sheetId="{i}" r:id="rId{i}"/>'
            for i, n in enumerate(names, start=1))
        + "</sheets></workbook>")
    wb_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        + "".join(
            f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>'
            for i in range(1, len(names) + 1))
        + f'<Relationship Id="rId{len(names) + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        "</Relationships>")
    # Two cell formats: 0 = body (wrapped, top-aligned — these cells hold paragraphs),
    # 1 = header (bold). A named "Normal" cell style is required or readers warn that
    # the workbook has no default.
    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              f'<styleSheet xmlns="{NS}">'
              '<fonts count="2">'
              '<font><sz val="11"/><name val="Calibri"/></font>'
              '<font><b/><sz val="11"/><name val="Calibri"/></font></fonts>'
              '<fills count="2"><fill><patternFill patternType="none"/></fill>'
              '<fill><patternFill patternType="gray125"/></fill></fills>'
              '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
              '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
              '<cellXfs count="2">'
              '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1">'
              '<alignment vertical="top" wrapText="1"/></xf>'
              '<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/>'
              '</cellXfs>'
              '<cellStyles count="1">'
              '<cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
              '</styleSheet>')

    members = [("[Content_Types].xml", content_types), ("_rels/.rels", root_rels),
               ("xl/workbook.xml", wb), ("xl/_rels/workbook.xml.rels", wb_rels),
               ("xl/styles.xml", styles)]
    for i, name in enumerate(names, start=1):
        members.append((f"xl/worksheets/sheet{i}.xml",
                        _sheet_xml(sheets[name], _WIDTHS.get(name))))

    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in members:
            # Fixed timestamp: same input -> identical bytes, so a committed .xlsx
            # only changes when its content does.
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o600 << 16
            zf.writestr(info, data)


# --------------------------------------------------------------------------- #
# xlsx reading
# --------------------------------------------------------------------------- #
def _cell_text(cell: ET.Element, shared: list[str]) -> str:
    kind = cell.get("t", "n")
    if kind == "inlineStr":
        node = cell.find(f"{{{NS}}}is")
        return "".join(t.text or "" for t in node.iter(f"{{{NS}}}t")) if node is not None else ""
    v = cell.find(f"{{{NS}}}v")
    if v is None or v.text is None:
        return ""
    if kind == "s":  # real Excel rewrites inline strings into the shared table
        try:
            return shared[int(v.text)]
        except (ValueError, IndexError):
            return ""
    return v.text


def read_xlsx(path: Path) -> dict[str, list[list[str]]]:
    if not path.exists():
        fail(f"workbook not found: {path}")
    with zipfile.ZipFile(path) as zf:
        names = set(zf.namelist())
        shared: list[str] = []
        if "xl/sharedStrings.xml" in names:
            sst = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            shared = ["".join(t.text or "" for t in si.iter(f"{{{NS}}}t"))
                      for si in sst.findall(f"{{{NS}}}si")]

        wb = ET.fromstring(zf.read("xl/workbook.xml"))
        rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
        target = {r.get("Id"): r.get("Target") for r in rels}

        sheets: dict[str, list[list[str]]] = {}
        for sheet in wb.find(f"{{{NS}}}sheets"):
            rid = sheet.get(f"{{{RNS}}}id")
            part = target.get(rid, "")
            if not part:
                continue
            member = part if part.startswith("xl/") else "xl/" + part.lstrip("/")
            if member not in names:
                continue
            ws = ET.fromstring(zf.read(member))
            rows: list[list[str]] = []
            for row in ws.iter(f"{{{NS}}}row"):
                cells: dict[int, str] = {}
                for cell in row.findall(f"{{{NS}}}c"):
                    ref = cell.get("r") or ""
                    letters = "".join(ch for ch in ref if ch.isalpha())
                    idx = 0
                    for ch in letters:
                        idx = idx * 26 + (ord(ch.upper()) - 64)
                    if idx:
                        cells[idx] = _cell_text(cell, shared)
                width = max(cells) if cells else 0
                rows.append([cells.get(i, "") for i in range(1, width + 1)])
            sheets[sheet.get("name", "")] = rows
    return sheets


def sheets_to_model(sheets: dict[str, list[list[str]]], src: str) -> dict:
    def get(name: str) -> list[list[str]]:
        if name not in sheets:
            fail(f"{src}: missing '{name}' sheet")
        return sheets[name]

    def cell(row: list[str], i: int) -> str:
        return row[i].strip() if i < len(row) else ""

    meta_rows = get("Meta")[1:]
    meta = {cell(r, 0): (r[1] if len(r) > 1 else "") for r in meta_rows if cell(r, 0)}
    if not meta.get("concept"):
        fail(f"{src}: Meta sheet has no 'concept' value")

    def rules_from(name: str, kind: str) -> list[dict]:
        out = []
        for row in get(name)[1:]:
            ref = cell(row, 0)
            if not ref:
                continue
            if not re.fullmatch(rf"{kind}\d+", ref):
                fail(f"{src}: '{name}' ref '{ref}' is not {kind}<n>")
            out.append({"ref": ref, "title": cell(row, 1), "body": cell(row, 2),
                        "owner": cell(row, 3) if kind == "C" else ""})
        if kind == "C":
            for item in out:
                if not item["owner"]:
                    fail(f"{src}: clarification {item['ref']} has no Owner — "
                         "every open question leaves with a named owner")
        return out

    def scen_from(name: str, prefix: str) -> list[dict]:
        rows = get(name)
        header = [h.strip() for h in rows[0]] if rows else []
        if header[:3] != list(SCENARIO_COLUMNS[:3]):
            fail(f"{src}: '{name}' header must start Ref | Title | Open")
        out = []
        for row in rows[1:]:
            ref = cell(row, 0)
            if not ref:
                continue
            if not re.fullmatch(rf"{prefix}-\d+", ref):
                fail(f"{src}: '{name}' ref '{ref}' is not {prefix}-NN")
            fields = {}
            for i, field in enumerate(SCENARIO_FIELDS, start=3):
                value = cell(row, i)
                if not value:
                    fail(f"{src}: {ref} has no '{field}' — all nine fields are required")
                fields[field] = value
            out.append({"ref": ref, "title": cell(row, 1),
                        "open": cell(row, 2).lower() in {"yes", "true", "y", "1"},
                        "fields": fields})
        return out

    return {
        "concept": meta["concept"],
        "frontmatter": meta.get("frontmatter", "").rstrip("\n"),
        "doc_note": meta.get("doc_note", "").rstrip("\n"),
        "meta_line": meta.get("meta_line", "").strip(),
        "graph_block": meta.get("graph_block", "").rstrip("\n"),
        "rules": rules_from("Rules", "R"),
        "clarifications": rules_from("Clarifications", "C"),
        "green": scen_from("Green Path", "G"),
        "edge": scen_from("Edge Paths", "E"),
    }


# --------------------------------------------------------------------------- #
# Blank starter
# --------------------------------------------------------------------------- #
TEMPLATE_MODEL = {
    "concept": "<concept name>",
    "frontmatter": "\n".join([
        "---", "type: definition-matrix", "status: draft",
        "owner: <concept-team member running the definition>",
        "surfaces: [<surface>]", "source: product", "last_reviewed: <YYYY-MM-DD>",
        "tags: [orbit, discovery, definition-matrix]", "---"]),
    "doc_note": "",
    "meta_line": "**Source Concept Pack:** `discovery/briefs/<the Ready brief>.md` · "
                 "**Working draft:** v0.1 · <date>",
    "graph_block": "",
    "rules": [{"ref": "R1", "title": "<rule name>",
               "body": "<What the rule is, in one paragraph. Name the systems and fields "
                       "it touches.>", "owner": ""}],
    "clarifications": [{"ref": "C1", "title": "<clarification name>",
                        "body": "<The open question, and the options if known.>",
                        "owner": "<team/person>"}],
    "green": [{"ref": "G-01", "title": "<scenario title>", "open": False,
               "fields": {f: f"<{f.lower()}>" for f in SCENARIO_FIELDS}}],
    "edge": [{"ref": "E-01", "title": "<edge scenario title>", "open": False,
              "fields": {f: f"<{f.lower()}>" for f in SCENARIO_FIELDS}}],
}


# --------------------------------------------------------------------------- #
# Commands
# --------------------------------------------------------------------------- #
def cmd_export(src: Path, out: Path) -> None:
    write_xlsx(_model_to_sheets(parse_md(src)), out)
    print(f"matrix_xlsx: wrote {out} from {src}")


def cmd_import(src: Path, out: Path) -> None:
    model = sheets_to_model(read_xlsx(src), src.name)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_md(model), encoding="utf-8")
    print(f"matrix_xlsx: wrote {out} from {src} "
          f"({len(model['green'])}G/{len(model['edge'])}E/"
          f"{len(model['rules'])}R/{len(model['clarifications'])}C)")


def cmd_template(out: Path) -> None:
    write_xlsx(_model_to_sheets(TEMPLATE_MODEL), out)
    print(f"matrix_xlsx: wrote a blank matrix workbook to {out}")


def cmd_check(md: Path, xlsx: Path) -> None:
    """Both directions must reproduce the canonical markdown byte-for-byte."""
    if not md.exists():
        fail(f"--check: {md} does not exist")
    expected = md.read_text(encoding="utf-8")

    round_tripped = render_md(sheets_to_model(_model_to_sheets(parse_md(md)),
                                              f"{md.name} (in memory)"))
    if round_tripped != expected:
        print(f"matrix_xlsx: DRIFT — export/import of {md} does not reproduce it.\n"
              "The markdown is not in canonical form, or the serializer changed.",
              file=sys.stderr)
        raise SystemExit(2)

    if xlsx.exists():
        from_book = render_md(sheets_to_model(read_xlsx(xlsx), xlsx.name))
        if from_book != expected:
            print(f"matrix_xlsx: DRIFT — {xlsx} no longer reproduces {md}.\n"
                  f"Re-export it: python3 tools/matrix_xlsx.py export {md} -o {xlsx}",
                  file=sys.stderr)
            raise SystemExit(2)
        print(f"matrix_xlsx: OK — {md.name} round-trips, and {xlsx.name} matches it")
    else:
        print(f"matrix_xlsx: OK — {md.name} round-trips ({xlsx.name} not committed)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd")

    p_exp = sub.add_parser("export", help="matrix markdown -> .xlsx")
    p_exp.add_argument("src", nargs="?", default=str(DEFAULT_MD))
    p_exp.add_argument("-o", "--out", default=None)

    p_imp = sub.add_parser("import", help=".xlsx -> canonical matrix markdown")
    p_imp.add_argument("src", nargs="?", default=str(DEFAULT_XLSX))
    p_imp.add_argument("-o", "--out", default=None)

    p_tpl = sub.add_parser("template", help="write a blank matrix workbook")
    p_tpl.add_argument("-o", "--out", required=True)

    ap.add_argument("--check", action="store_true",
                    help="assert the round trip reproduces the canonical markdown")
    ap.add_argument("--md", default=str(DEFAULT_MD), help="--check: the canonical markdown")
    ap.add_argument("--xlsx", default=str(DEFAULT_XLSX), help="--check: the committed workbook")
    args = ap.parse_args()

    if args.check:
        cmd_check(Path(args.md), Path(args.xlsx))
        return
    if args.cmd == "export":
        src = Path(args.src)
        cmd_export(src, Path(args.out) if args.out else src.with_suffix(".xlsx"))
    elif args.cmd == "import":
        src = Path(args.src)
        cmd_import(src, Path(args.out) if args.out else src.with_suffix(".md"))
    elif args.cmd == "template":
        cmd_template(Path(args.out))
    else:
        ap.print_help()
        raise SystemExit(1)


if __name__ == "__main__":
    main()
