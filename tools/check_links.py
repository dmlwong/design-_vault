#!/usr/bin/env python3
"""Check vault-internal file references in the Orbit Design Brain.

References in the brain are back-ticked paths (not wikilinks), written in one of
three conventions:

1. vault-root-relative:            `design-brain/tokens.md`
2. export-relative benchmarks:     `design-brain/_benchmarks/...`
   (in the vault, `_benchmarks/` sits at the root; the exporter maps it under
   `design-brain/`, so both spellings are accepted)
3. design-brain-relative (common in `_benchmarks/` and `_review/`):
   `components/data-table.md`, `platforms/connected-platform.md`
4. sibling / well-known-dir bare names: `tokens.md`, `badge-status.md`,
   `<screenshot>.png` (resolved against the referencing file's folder and the
   standard brain folders)

Anything that resolves under none of these is reported and the script exits 1.
Product-repo paths (`packages/`, `apps/`, ...) are out of scope. Historical
benchmark results (`_benchmarks/results/`) and `_archive/` are skipped: they are
records, not living docs.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHECK_EXTENSIONS = (".md", ".tsx", ".py", ".css", ".png", ".canvas", ".base")

SKIP_DIRS = {".git", ".obsidian", "_archive"}
SKIP_TREES = ("_benchmarks/results",)  # historical artifacts, not living docs

# References into the product repo or scratch areas — not resolvable here.
EXTERNAL_PREFIXES = (
    "packages/",
    "apps/",
    "scripts/",
    "test/",
    "Test/",
    "~",
    ".claude/",
    "efficio-orbit/",
    "design-md/",
    "src/",
    "_private/",
    "themes/",  # product-repo token theme files (packages/orbit/styles/tokens/themes/)
)
EXTERNAL_BASENAMES = {
    "DESIGN.md",
    "DESIGN.prose.md",
    "AGENTS.md",  # bare mentions usually mean the root file, which always exists
    "CLAUDE.md",
    # product-repo token source files referenced by basename in tokens.md/defaults.md
    "colors.css",
    "semantics.css",
    "components.css",
    "spacing.css",
    "typography.css",
    "elevation.css",
    "orbit.css",
    "tokens.css",
    # scratch-convention artifact names used by the stress-test guides
    "review.md",
    "brain.tsx",
    "baseline.tsx",
    "rubric.md",
    "rubric-blind.md",
    "candidate-1.md",
    "candidate-2.md",
}

# Folders bare-name references are allowed to resolve against.
WELL_KNOWN_DIRS = (
    "design-brain",
    "design-brain/components",
    "design-brain/patterns",
    "design-brain/examples",
    "design-brain/platforms",
    "design-brain/lovable",
    "design-brain/agents",
    "_benchmarks",
    "_review",
    "_canvases",
    "discovery",
    "tools",
    "design-brain/examples/screenshots/connected-platform",
    "design-brain/examples/screenshots/orbit-client-connected-platform",
)

REF_PATTERN = re.compile(
    r"`([A-Za-z_~.][\w\-/ .]*?\.(?:md|tsx|py|css|png|canvas|base))`"
)


def iter_docs() -> list[Path]:
    docs = []
    for path in sorted(ROOT.rglob("*.md")):
        rel = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if any(rel.as_posix().startswith(tree) for tree in SKIP_TREES):
            continue
        docs.append(path)
    return docs


def resolves(ref: str, doc: Path) -> bool:
    if ref.startswith(EXTERNAL_PREFIXES):
        return True
    if "/" not in ref and ref in EXTERNAL_BASENAMES:
        return True

    candidates = [ROOT / ref, doc.parent / ref, ROOT / "design-brain" / ref]
    if ref.startswith("design-brain/_benchmarks/"):
        candidates.append(ROOT / ref.replace("design-brain/_benchmarks/", "_benchmarks/", 1))
    if "/" not in ref:
        candidates.extend(ROOT / d / ref for d in WELL_KNOWN_DIRS)
    return any(c.is_file() for c in candidates)


def main() -> None:
    broken: list[tuple[str, str]] = []
    for doc in iter_docs():
        text = doc.read_text(encoding="utf-8", errors="ignore")
        for match in REF_PATTERN.finditer(text):
            ref = match.group(1)
            if not resolves(ref, doc):
                broken.append((doc.relative_to(ROOT).as_posix(), ref))

    if broken:
        print(f"BROKEN REFERENCES ({len(broken)}):")
        for doc, ref in broken:
            print(f"- {doc} -> {ref}")
        raise SystemExit(1)
    print(f"Link check passed: {len(iter_docs())} docs scanned, no broken references.")


if __name__ == "__main__":
    main()
