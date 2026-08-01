#!/usr/bin/env python3
"""Fail closed if the cold-review frozen inputs or unit census drift."""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "2e93a621aeeee0a0844543068363d0ba94094357"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    snap = json.loads((HERE / "PREREG_SNAPSHOT.json").read_text())
    units = list(csv.DictReader((HERE / "FROZEN_REVIEW_UNITS.tsv").open(), delimiter="\t"))
    inventory = list(csv.DictReader((HERE / "SOURCE_INVENTORY.tsv").open(), delimiter="\t"))
    assert snap["base"] == BASE
    assert len(units) == 37 and len({r["unit_id"] for r in units}) == 37
    assert sum(r["unit_kind"] == "PACKAGE_HEADLINE_BUNDLE" for r in units) == 29
    assert sum(r["unit_kind"] == "CROSS_CUTTING_QUESTION" for r in units) == 8
    assert sha(HERE / "FROZEN_REVIEW_UNITS.tsv") == snap["frozen_review_units_sha256"]
    assert sha(HERE / "SOURCE_INVENTORY.tsv") == snap["source_inventory_sha256"]
    assert sha(HERE / "SOURCE_MANIFEST.sha256") == snap["source_manifest_sha256"]
    assert len(inventory) == snap["source_paths"]
    assert len({r["path"] for r in inventory}) == len(inventory)
    assert all(sha(ROOT / r["path"]) == r["sha256"] for r in inventory)
    ancestor = subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"], cwd=ROOT)
    assert ancestor.returncode == 0
    changed = subprocess.run(["git", "diff", "--name-only", BASE, "--"], cwd=ROOT,
                             check=True, text=True, capture_output=True).stdout.splitlines()
    assert all(path.startswith("udt_p4_cold_adversarial_review_2026-08-01/") for path in changed)
    print(f"PASS preregistration: {len(units)} units; {len(inventory)} source paths; base {BASE}")


if __name__ == "__main__":
    main()
