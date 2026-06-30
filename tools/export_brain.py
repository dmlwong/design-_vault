#!/usr/bin/env python3
"""Export the canonical Orbit Design Brain into a product repo.

The Obsidian vault is canonical. Product repo copies are generated artifacts.
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "AGENTS.md",
    "CLAUDE.md",
    "_review/Platform Visual Truth Review Checklist.md",
    "_benchmarks/accessibility-artifact-process.md",
    "_benchmarks/agent-benchmark-tasks.md",
    "_benchmarks/scorecard-template.md",
    "_benchmarks/ux-scorecard-template.md",
    "design-brain/principles.md",
    "design-brain/tokens.md",
    "design-brain/anti-patterns.md",
    "design-brain/accessibility.md",
    "design-brain/motion.md",
    "design-brain/ux-copy.md",
    "design-brain/data-viz.md",
    "design-brain/defaults.md",
    "design-brain/interaction-defaults.md",
    "design-brain/platforms/README.md",
    "design-brain/platforms/connected-platform.md",
    "design-brain/platforms/connected-platform-visual-truth.md",
    "design-brain/platforms/orbit-client-connected-platform.md",
    "design-brain/platforms/orbit-client-connected-platform-visual-truth.md",
    "design-brain/components/README.md",
    "design-brain/patterns/README.md",
    "design-brain/patterns/home-dashboard.md",
    "design-brain/patterns/tool-hub.md",
    "design-brain/patterns/focus-mode-results.md",
    "design-brain/patterns/guided-conversational-workflow.md",
    "design-brain/patterns/list-detail.md",
    "design-brain/patterns/config-wizard.md",
    "design-brain/patterns/analytics-dashboard.md",
    "design-brain/patterns/review-and-approve-workflow.md",
    "design-brain/examples/README.md",
    "design-brain/examples/connected-platform-home-shell-dashboard.md",
    "design-brain/examples/connected-platform-initiative-list-table.md",
    "design-brain/examples/connected-platform-clauseiq-contract-wizard-modal.md",
    "design-brain/examples/connected-platform-supplier-tracker-table.md",
    "design-brain/examples/orbit-client-home-ai-tools-dashboard.md",
    "design-brain/examples/orbit-client-sourcing-execution-tool-hub.md",
    "design-brain/examples/orbit-client-marketiq-guided-workflow.md",
    "design-brain/examples/orbit-client-marketiq-research-output-next-actions.md",
    "design-brain/examples/orbit-client-delivery-engine-initiative-detail.md",
    "design-brain/examples/orbit-client-marketiq-research-output-flow.md",
    "design-brain/examples/screenshots/connected-platform/manifest.md",
    "design-brain/examples/screenshots/orbit-client-connected-platform/manifest.md",
    "design-brain/lovable/knowledge-base.md",
    "design-brain/lovable/workspace-knowledge.md",
    "discovery/_TEMPLATE.md",
    "discovery/README.md",
]

REQUIRED_DIRS = [
    "_benchmarks",
    "_review",
    "design-brain/components",
    "design-brain/platforms",
    "design-brain/patterns",
    "design-brain/examples",
    "design-brain/examples/screenshots/connected-platform",
    "design-brain/examples/screenshots/orbit-client-connected-platform",
    "design-brain/skills",
    "design-brain/agents",
    "design-brain/lovable",
    "discovery",
]

EXCLUDED_NAMES = {".DS_Store", "__pycache__"}


@dataclass(frozen=True)
class CopyOp:
    source: Path
    destination: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, help="Product repo path to export into.")
    parser.add_argument(
        "--profile",
        choices=["all", "codex", "claude", "lovable"],
        default="all",
        help="Export profile. 'all' is the normal product-repo pack.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print changes without writing.")
    return parser.parse_args()


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def ensure_required() -> None:
    missing = []
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            missing.append(rel)
    for rel in REQUIRED_DIRS:
        if not (ROOT / rel).is_dir():
            missing.append(rel)
    if missing:
        fail("Missing required Design Brain files:\n" + "\n".join(f"- {item}" for item in missing))


def iter_tree(source_dir: Path, destination_dir: Path) -> list[CopyOp]:
    ops: list[CopyOp] = []
    for source in sorted(source_dir.rglob("*")):
        if any(part in EXCLUDED_NAMES for part in source.parts):
            continue
        if source.is_dir():
            continue
        rel = source.relative_to(source_dir)
        ops.append(CopyOp(source, destination_dir / rel))
    return ops


def build_ops(target: Path, profile: str) -> list[CopyOp]:
    ops: list[CopyOp] = []

    if profile in {"all", "codex", "claude"}:
        ops.append(CopyOp(ROOT / "AGENTS.md", target / "AGENTS.md"))
        ops.extend(iter_tree(ROOT / "design-brain", target / "design-brain"))
        ops.extend(iter_tree(ROOT / "_benchmarks", target / "design-brain" / "_benchmarks"))
        ops.extend(iter_tree(ROOT / "_review", target / "design-brain" / "_review"))
        ops.extend(iter_tree(ROOT / "discovery", target / "discovery"))

    if profile in {"all", "claude"}:
        ops.append(CopyOp(ROOT / "CLAUDE.md", target / "CLAUDE.md"))
        ops.extend(iter_tree(ROOT / "design-brain" / "skills", target / ".claude" / "skills"))
        ops.append(
            CopyOp(
                ROOT / "design-brain" / "agents" / "design-reviewer.md",
                target / ".claude" / "agents" / "design-reviewer.md",
            )
        )

    if profile == "lovable":
        ops.extend(iter_tree(ROOT / "design-brain" / "lovable", target / "design-brain" / "lovable"))

    if profile == "all":
        marker = ROOT / "_exports" / "GENERATED_EXPORT_NOTICE.md"
        if marker.is_file():
            ops.append(CopyOp(marker, target / "DESIGN_BRAIN_EXPORT.md"))

    return ops


def op_status(op: CopyOp) -> str | None:
    if not op.destination.exists():
        return "ADD"
    if not filecmp.cmp(op.source, op.destination, shallow=False):
        return "UPDATE"
    return None


def apply_ops(ops: list[CopyOp], dry_run: bool) -> int:
    changed = [(op, op_status(op)) for op in ops]
    changed = [(op, status) for op, status in changed if status]

    if not changed:
        print("No export changes.")
        return 0

    print("Export changes:")
    for op, status in changed:
        rel = op.destination
        print(f"- {status}: {rel}")

    if dry_run:
        print("Dry run only. No files written.")
        return len(changed)

    for op, _ in changed:
        op.destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(op.source, op.destination)

    print(f"Wrote {len(changed)} file(s).")
    return len(changed)


def main() -> None:
    args = parse_args()
    ensure_required()
    target = Path(args.target).expanduser().resolve()
    if not target.exists():
        fail(f"Target does not exist: {target}")
    if not target.is_dir():
        fail(f"Target is not a directory: {target}")
    ops = build_ops(target, args.profile)
    if not ops:
        fail(f"No export operations built for profile: {args.profile}")
    apply_ops(ops, args.dry_run)


if __name__ == "__main__":
    main()
