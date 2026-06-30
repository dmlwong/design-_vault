---
type: export-index
status: stable
owner: design-system
surfaces: [shared]
source: specified
last_reviewed: 2026-06-14
maturity_score: 70
tags: [orbit, design-brain, export]
---

# Exports

Use `tools/export_brain.py` to generate product-repo copies of the Design Brain.

## Normal Export

```bash
python3 tools/export_brain.py --target /path/to/orbit-product --profile all
```

## Dry Run

```bash
python3 tools/export_brain.py --target /path/to/orbit-product --profile all --dry-run
```

## Profiles

- `all`: root `AGENTS.md`, root `CLAUDE.md`, `design-brain/`, `design-brain/_benchmarks/`, and `.claude/`.
- `codex`: root `AGENTS.md`, `design-brain/`, and `design-brain/_benchmarks/`.
- `claude`: root `AGENTS.md`, root `CLAUDE.md`, `design-brain/`, `design-brain/_benchmarks/`, and `.claude/`.
- `lovable`: only `design-brain/lovable/`.
