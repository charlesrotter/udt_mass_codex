#!/usr/bin/env python3
"""Fail-closed checks for the frozen branchwise-census preregistration."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent
BASE = "156b8a57d2e4ce65a588e5f7c2d82d0bd1f88334"


def rows(name: str) -> list[dict[str, str]]:
    with (PKG / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def git_tree() -> dict[str, str]:
    raw = subprocess.run(
        ["git", "ls-tree", "-r", "-z", BASE], cwd=ROOT, capture_output=True, check=True
    ).stdout
    result = {}
    for item in raw.split(b"\0"):
        if not item:
            continue
        head, path = item.split(b"\t", 1)
        result[path.decode("utf-8", "surrogateescape")] = head.decode("ascii").split()[2]
    return result


def main() -> int:
    base = rows("BASE_TREE_MANIFEST.tsv")
    reports = rows("AUDIT_REPORT_UNIVERSE.tsv")
    groups = rows("PACKAGE_GROUP_UNIVERSE.tsv")
    premises = rows("PREMISE_LEDGER.tsv")
    candidates = rows("CANDIDATE_CLASSES.tsv")
    falsifiers = rows("FALSIFICATION_CONTRACT.tsv")
    discovery = rows("DISCOVERY_RULES.tsv")
    saved = json.loads((PKG / "PREREGISTRATION_UNIVERSE_RESULT.json").read_text(encoding="utf-8"))
    tree = git_tree()
    checks = {
        "base_exact": saved["base"] == BASE,
        "base_paths_unique": len(base) == len({row["path"] for row in base}),
        "base_paths_match_git_tree": {row["path"]: row["git_blob"] for row in base} == tree,
        "base_count_matches_saved": len(base) == saved["base_tree_paths"],
        "text_count_matches_saved": sum(row["text_discovery_eligible"] == "YES" for row in base) == saved["text_discovery_eligible"],
        "report_paths_unique": len(reports) == len({row["path"] for row in reports}),
        "report_count_matches_saved": len(reports) == saved["audit_reports"],
        "reports_are_base_tree_subset": all(row["path"] in tree and row["git_blob"] == tree[row["path"]] for row in reports),
        "groups_unique": len(groups) == len({row["top_group"] for row in groups}),
        "group_count_matches_saved": len(groups) == saved["top_groups"],
        "premises_22_unique": len(premises) == 22 and len({row["id"] for row in premises}) == 22,
        "candidates_15_unique": len(candidates) == 15 and len({row["id"] for row in candidates}) == 15,
        "falsifiers_18_unique": len(falsifiers) == 18 and len({row["id"] for row in falsifiers}) == 18,
        "discovery_10_unique": len(discovery) == 10 and len({row["id"] for row in discovery}) == 10,
        "no_projector_outcome_retained": any(row["id"] == "C14" for row in candidates),
        "incomplete_outcome_retained": any(row["id"] == "C15" for row in candidates),
        "manifest_hashes_match_saved": all(
            hashlib.sha256((PKG / name).read_bytes()).hexdigest() == saved[key]
            for name, key in (
                ("BASE_TREE_MANIFEST.tsv", "base_tree_manifest_sha256"),
                ("AUDIT_REPORT_UNIVERSE.tsv", "audit_report_universe_sha256"),
                ("PACKAGE_GROUP_UNIVERSE.tsv", "package_group_universe_sha256"),
            )
        ),
    }
    result = {
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "counts": {
            "base_paths": len(base),
            "text_paths": sum(row["text_discovery_eligible"] == "YES" for row in base),
            "audit_reports": len(reports),
            "top_groups": len(groups),
            "premises": len(premises),
            "candidate_classes": len(candidates),
            "falsifiers": len(falsifiers),
            "discovery_rules": len(discovery),
        },
        "status": "PASS" if all(checks.values()) else "FAIL",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
