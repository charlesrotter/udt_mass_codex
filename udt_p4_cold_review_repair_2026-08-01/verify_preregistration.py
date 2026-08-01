#!/usr/bin/env python3
"""Fail closed if the forward-repair preregistration no longer matches its base."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "c9c8b3848a7ff85b7941e803bf87c0ff48b9f98c"
REVIEW = ROOT / "udt_p4_cold_adversarial_review_2026-08-01"
SUMMARY = ROOT / "P4_ARC_SUMMARY_2026-07-31.md"
OLD = "K₄ = real points of the gauge-spent screen U(1)"
NEW = "the screen-character image {+1,-1}, not K₄ itself, is the real two-torsion of the gauge-spent screen U(1)"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, text=True, capture_output=True
    ).stdout.strip()


def main() -> None:
    snap = json.loads((HERE / "PREREG_SNAPSHOT.json").read_text())
    assert snap["base"] == BASE
    assert git("merge-base", "--is-ancestor", BASE, "HEAD") == ""
    assert git("rev-parse", f"{BASE}:udt_p4_cold_adversarial_review_2026-08-01") == snap["cold_review_tree"]
    assert git("rev-parse", "HEAD:udt_p4_cold_adversarial_review_2026-08-01") == snap["cold_review_tree"]
    assert sha(SUMMARY) == snap["summary_sha256"]
    assert sha(REVIEW / "TRANSITIVE_DEPENDENCY_OVERLAY.tsv") == snap["overlay_sha256"]
    with (REVIEW / "TRANSITIVE_DEPENDENCY_OVERLAY.tsv").open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == snap["overlay_rows"]
    assert Counter(r["classification"] for r in rows) == Counter(
        {"LOAD_BEARING": snap["load_bearing"], "SUPPORTING": snap["supporting"]}
    )
    assert all(r["overlay_status"] == "NON_RETROACTIVE_POST_OUTCOME_DEPENDENCY_RECORD" for r in rows)
    assert SUMMARY.read_text().count(OLD) == 1
    assert SUMMARY.read_text().count(NEW) == 0
    changed = git("diff", "--name-only", BASE, "--").splitlines()
    assert changed and all(path.startswith(HERE.name + "/") for path in changed)
    print(f"PASS preregistration: base={BASE}; overlay={len(rows)} (7+6); review tree frozen")


if __name__ == "__main__":
    main()
