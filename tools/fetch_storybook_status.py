#!/usr/bin/env python3
"""Refresh ``tools/storybook-status.json`` from the component repo's CI.

The vault documents Storybook (``design-brain/storybook.md``) but the tool
itself lives in the product repo. This script fetches two facts from GitHub so
the health dashboard can report on it:

1. the conclusion of the latest ``CI`` workflow run on the component repo's
   default branch, and
2. how many components have stories — the number that actually matters, since
   ``extract-contract`` derives contracts from stories, and a component without
   them gets a contract written from source reading alone.

**This script never fails the build.** Any network, auth, rate-limit or parse
problem leaves the existing JSON exactly as it was and exits 0 with a warning
on stderr. ``vault_health.py`` must stay runnable offline, and a stale-but-real
status is more useful than a crash. Staleness is handled at render time: the
dashboard shows "unknown" rather than a stale green tick once ``fetched`` ages
past its threshold.

Set ``GITHUB_TOKEN`` for a higher rate limit. The component repo is public, so
unauthenticated requests work too.

``--self-test`` exercises the two parsers against fixtures without touching the
network — the HTTP calls are thin, the parsing is where mistakes hide.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tools" / "storybook-status.json"

OWNER = "dmlwong"
REPO = "efficio-design-system"
BRANCH = "main"
WORKFLOW = "ci.yml"
SITE_URL = f"https://{OWNER}.github.io/{REPO}/"

API = "https://api.github.com"
TIMEOUT = 20

# Suffixes that are not components even though they are .tsx under src/.
NON_COMPONENT_SUFFIXES = (".test.tsx", ".stories.tsx", ".figma.tsx")
STORY_SUFFIX = ".stories.tsx"


# --------------------------------------------------------------------------- #
# Parsing (pure — covered by --self-test)
# --------------------------------------------------------------------------- #
def parse_run(payload: dict) -> dict:
    """Pull the fields we render from a workflow-runs response."""
    runs = payload.get("workflow_runs") or []
    if not runs:
        # No run recorded yet (e.g. the workflow has not reached the default
        # branch). Explicitly null rather than absent, so the renderer can tell
        # "never built" apart from "could not fetch".
        return {"conclusion": None, "run_url": None, "run_started": None, "head_sha": None}
    r = runs[0]
    return {
        "conclusion": r.get("conclusion"),
        "run_url": r.get("html_url"),
        "run_started": (r.get("run_started_at") or "")[:10] or None,
        "head_sha": (r.get("head_sha") or "")[:7] or None,
    }


def parse_tree(payload: dict) -> dict:
    """Count components and stories from a recursive git-tree response."""
    paths = [n["path"] for n in payload.get("tree", []) if n.get("type") == "blob"]
    src = [p for p in paths if p.startswith("packages/orbit/src/")]
    stories = [p for p in src if p.endswith(STORY_SUFFIX)]
    components = [
        p for p in src
        if p.endswith(".tsx")
        and not p.endswith(NON_COMPONENT_SUFFIXES)
        and Path(p).stem != "index"
    ]
    storied = {Path(p).name[: -len(STORY_SUFFIX)] for p in stories}
    with_stories = sorted({Path(c).stem for c in components} & storied)
    return {
        "story_files": len(stories),
        "components": len(components),
        "components_with_stories": len(with_stories),
        # The component NAMES that have stories — vault_health.py maps these onto
        # contract slugs to compute contracted-first coverage. A count alone can't
        # answer "do the components we've written contracts for have stories?".
        "storied_components": with_stories,
        # A truncated tree would silently understate the counts, so record it
        # rather than quietly reporting a wrong denominator.
        "tree_truncated": bool(payload.get("truncated")),
    }


# --------------------------------------------------------------------------- #
# Fetching
# --------------------------------------------------------------------------- #
def _get(url: str) -> dict:
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "orbit-vault-health",
    })
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> None:
    if "--self-test" in sys.argv:
        self_test()
        return

    try:
        run = parse_run(_get(
            f"{API}/repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW}/runs"
            f"?branch={BRANCH}&status=completed&per_page=1"
        ))
        tree = parse_tree(_get(
            f"{API}/repos/{OWNER}/{REPO}/git/trees/{BRANCH}?recursive=1"
        ))
    except (urllib.error.URLError, urllib.error.HTTPError, OSError,
            json.JSONDecodeError, KeyError, TypeError) as exc:
        # Deliberately not fatal — see the module docstring.
        print(f"warning: could not refresh Storybook status "
              f"({exc.__class__.__name__}: {exc}); leaving {OUT.name} unchanged",
              file=sys.stderr)
        return

    data = {
        "_comment": (
            "GENERATED by tools/fetch_storybook_status.py — do not hand-edit. "
            "Read by tools/vault_health.py to render the Component library "
            "section. Informational only: it never gates the health verdict."
        ),
        "fetched": date.today().isoformat(),
        "repo": f"{OWNER}/{REPO}",
        "branch": BRANCH,
        "site_url": SITE_URL,
        **run,
        **tree,
    }
    OUT.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Storybook status: {data['conclusion'] or 'no run on ' + BRANCH} · "
          f"{data['components_with_stories']}/{data['components']} components have stories")


# --------------------------------------------------------------------------- #
# Self-test
# --------------------------------------------------------------------------- #
def self_test() -> None:
    failures = []

    def eq(label, got, want):
        if got != want:
            failures.append(f"{label}: got {got!r}, want {want!r}")

    # --- parse_run -------------------------------------------------------- #
    eq("run/empty", parse_run({"workflow_runs": []}),
       {"conclusion": None, "run_url": None, "run_started": None, "head_sha": None})
    eq("run/missing-key", parse_run({}),
       {"conclusion": None, "run_url": None, "run_started": None, "head_sha": None})
    eq("run/success", parse_run({"workflow_runs": [{
        "conclusion": "success",
        "html_url": "https://github.com/o/r/actions/runs/1",
        "run_started_at": "2026-07-28T13:57:14Z",
        "head_sha": "c01df1058db7e1e07358b0ab2ed7c79b5bf673c4",
    }]}), {"conclusion": "success",
           "run_url": "https://github.com/o/r/actions/runs/1",
           "run_started": "2026-07-28", "head_sha": "c01df10"})
    eq("run/failure-conclusion-preserved",
       parse_run({"workflow_runs": [{"conclusion": "failure"}]})["conclusion"], "failure")

    # --- parse_tree ------------------------------------------------------- #
    def blob(p):
        return {"path": p, "type": "blob"}

    tree = {"tree": [
        blob("packages/orbit/src/actions/Button.tsx"),
        blob("packages/orbit/src/actions/Button.stories.tsx"),
        blob("packages/orbit/src/actions/Button.test.tsx"),
        blob("packages/orbit/src/actions/IconButton.tsx"),
        blob("packages/orbit/src/index.tsx"),              # barrel — not a component
        blob("packages/orbit/src/layout/ToggleCard.tsx"),
        blob("packages/orbit/src/layout/ToggleCard.figma.ts"),  # not .tsx at all
        blob("packages/orbit/src/actions/Button.module.css"),   # not .tsx
        blob("apps/prototypes/Thing.tsx"),                 # outside the package
        {"path": "packages/orbit/src/actions", "type": "tree"},  # dir entry
    ]}
    got = parse_tree(tree)
    eq("tree/components", got["components"], 3)            # Button, IconButton, ToggleCard
    eq("tree/story_files", got["story_files"], 1)
    eq("tree/with_stories", got["components_with_stories"], 1)
    eq("tree/storied_names", got["storied_components"], ["Button"])
    eq("tree/truncated", got["tree_truncated"], False)
    eq("tree/truncated-flag", parse_tree({"tree": [], "truncated": True})["tree_truncated"], True)
    eq("tree/empty", parse_tree({})["components"], 0)

    # A story whose component was deleted must not inflate coverage above the
    # component count — the intersection, not the story count, is the metric.
    orphan = {"tree": [
        blob("packages/orbit/src/actions/Gone.stories.tsx"),
        blob("packages/orbit/src/actions/Here.tsx"),
    ]}
    eq("tree/orphan-story", parse_tree(orphan)["components_with_stories"], 0)
    eq("tree/orphan-story-count", parse_tree(orphan)["story_files"], 1)
    # The name list must agree with the count, or the dashboard's contracted-first
    # coverage and its headline number would disagree.
    eq("tree/orphan-story-names", parse_tree(orphan)["storied_components"], [])
    eq("tree/names-match-count",
       len(got["storied_components"]), got["components_with_stories"])

    if failures:
        print("SELF-TEST FAILED:", file=sys.stderr)
        for f in failures:
            print("  -", f, file=sys.stderr)
        raise SystemExit(1)
    print("Self-test passed: parse_run and parse_tree behave as specified.")


if __name__ == "__main__":
    main()
