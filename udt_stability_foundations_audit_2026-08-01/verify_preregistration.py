#!/usr/bin/env python3
"""Fail closed on source, premise, base, or mutation-scope drift."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "5adeb59dde063770c0619d37b76b03f735d82038"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    snap = json.loads((HERE / "PREREG_SNAPSHOT.json").read_text())
    rows = list(csv.DictReader((HERE / "SOURCE_INVENTORY.tsv").open(), delimiter="\t"))
    premises = list(csv.DictReader((HERE / "PREMISE_LEDGER.tsv").open(), delimiter="\t"))
    assert snap["base"] == BASE
    assert len(rows) == snap["source_paths"] and len({row["path"] for row in rows}) == len(rows)
    assert len(premises) == snap["premise_rows"] == 13
    assert sha(HERE / "SOURCE_PATHS.txt") == snap["source_paths_sha256"]
    assert sha(HERE / "SOURCE_INVENTORY.tsv") == snap["source_inventory_sha256"]
    assert sha(HERE / "SOURCE_MANIFEST.sha256") == snap["source_manifest_sha256"]
    assert all(sha(ROOT / row["path"]) == row["sha256"] for row in rows)
    assert subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"], cwd=ROOT).returncode == 0
    changed = subprocess.run(["git", "diff", "--name-only", BASE, "--"], cwd=ROOT, check=True,
                             text=True, capture_output=True).stdout.splitlines()
    assert all(path.startswith(HERE.name + "/") for path in changed)
    print(f"PASS preregistration: {len(rows)} sources; {len(premises)} premises; base={BASE}")


if __name__ == "__main__":
    main()
