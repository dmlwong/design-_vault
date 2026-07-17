#!/usr/bin/env python3
"""Lint frontmatter across the Orbit Design Brain vault.

Checks every ``design-brain/**/*.md`` plus the governance layer (``_review/``,
``discovery/``) for:

- required keys: type, status, owner, surfaces, source, last_reviewed,
  maturity_score, tags
- ``status`` in {draft, in-review, stable}
- ``last_reviewed`` parseable as YYYY-MM-DD and not in the future
- ``context_tier`` (optional) in {always-on, task-core, reference, archive}

Skipped: ``skills/*/SKILL.md`` (Claude-skill frontmatter is a different shape),
templates (``_TEMPLATE``), screenshot manifests, ``_archive/``, and benchmark
results (records, not living docs).

``--stale-report`` lists files whose ``last_reviewed`` is older than 90 days.
It never fails the build — it is informational, for the weekly CI run.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_KEYS = (
    "type",
    "status",
    "owner",
    "surfaces",
    "source",
    "last_reviewed",
    "maturity_score",
    "tags",
)
VALID_STATUS = {"draft", "in-review", "stable"}
VALID_TIERS = {"always-on", "task-core", "reference", "archive"}
STALE_AFTER_DAYS = 90

LINT_TREES = ("design-brain", "_review", "discovery")
SKIP_PARTS = {"_archive", ".obsidian", ".git"}
SKIP_TREES = ("_benchmarks/results",)


def iter_targets() -> list[Path]:
    targets = []
    for tree in LINT_TREES:
        for path in sorted((ROOT / tree).rglob("*.md")):
            rel = path.relative_to(ROOT)
            if any(part in SKIP_PARTS for part in rel.parts):
                continue
            if any(rel.as_posix().startswith(t) for t in SKIP_TREES):
                continue
            if path.name == "SKILL.md":  # Claude-skill frontmatter shape
                continue
            if "_TEMPLATE" in path.name:  # templates document the shape, not content
                continue
            if path.parent.name in {"connected-platform", "orbit-client-connected-platform"} \
                    and path.name == "manifest.md":
                continue
            targets.append(path)
    return targets


def parse_frontmatter(path: Path) -> dict[str, str] | None:
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    fm: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fm
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if m:
            value = m.group(2)
            # strip inline YAML comments (discovery packs annotate lifecycle values)
            value = re.split(r"\s+#", value, maxsplit=1)[0]
            fm[m.group(1)] = value.strip()
    return None  # never closed


def lint(path: Path, fm: dict[str, str] | None, today: date) -> list[str]:
    rel = path.relative_to(ROOT).as_posix()
    if fm is None:
        return [f"{rel}: no frontmatter block"]
    problems = []
    required = REQUIRED_KEYS
    if rel.startswith("discovery/"):
        # discovery packs are lifecycle docs; maturity_score is not meaningful there
        required = tuple(k for k in REQUIRED_KEYS if k != "maturity_score")
    for key in required:
        if key not in fm:
            problems.append(f"{rel}: missing key '{key}'")
    status = fm.get("status")
    if status and status not in VALID_STATUS:
        problems.append(f"{rel}: invalid status '{status}'")
    tier = fm.get("context_tier")
    if tier and tier not in VALID_TIERS:
        problems.append(f"{rel}: invalid context_tier '{tier}'")
    reviewed = fm.get("last_reviewed")
    if reviewed:
        try:
            when = date.fromisoformat(reviewed)
            if when > today:
                problems.append(f"{rel}: last_reviewed {reviewed} is in the future")
        except ValueError:
            problems.append(f"{rel}: last_reviewed '{reviewed}' is not YYYY-MM-DD")
    return problems


def stale_report(today: date) -> None:
    cutoff = today - timedelta(days=STALE_AFTER_DAYS)
    stale: list[tuple[str, str]] = []
    for path in iter_targets():
        fm = parse_frontmatter(path)
        if not fm or "last_reviewed" not in fm:
            continue
        try:
            when = date.fromisoformat(fm["last_reviewed"])
        except ValueError:
            continue
        if when < cutoff:
            stale.append((fm["last_reviewed"], path.relative_to(ROOT).as_posix()))
    if not stale:
        print(f"Stale report: nothing older than {STALE_AFTER_DAYS} days. ")
        return
    print(f"Stale report ({len(stale)} files not reviewed in {STALE_AFTER_DAYS}+ days):")
    for reviewed, rel in sorted(stale):
        print(f"- {reviewed}  {rel}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stale-report", action="store_true",
                        help="list files not reviewed in 90 days (never fails)")
    args = parser.parse_args()
    today = date.today()

    if args.stale_report:
        stale_report(today)
        return

    problems: list[str] = []
    targets = iter_targets()
    for path in targets:
        problems.extend(lint(path, parse_frontmatter(path), today))
    if problems:
        print(f"FRONTMATTER PROBLEMS ({len(problems)}):")
        for p in problems:
            print(f"- {p}")
        raise SystemExit(1)
    print(f"Frontmatter lint passed: {len(targets)} files checked.")


if __name__ == "__main__":
    main()
