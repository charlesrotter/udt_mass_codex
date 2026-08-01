#!/usr/bin/env python3
"""Fail-closed verifier for the premise-audit preregistration."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent
BASE = "9d17940c5ab490b281b7818b46918ed378c96bf1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (PKG / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    inventory = rows("SOURCE_INVENTORY.tsv")
    premises = rows("PREMISE_LEDGER.tsv")
    interpretations = rows("INTERPRETATION_CANDIDATES.tsv")
    return_types = rows("RETURN_TYPE_CANDIDATES.tsv")
    paths = [row["path"] for row in inventory]
    assert len(inventory) == len(set(paths)) == 1424
    assert paths == sorted(paths)
    assert sum(row["layer"] == "PARENT_1384_SOURCE_UNIVERSE" for row in inventory) == 1384
    assert sum(row["layer"] == "WHOLE_RECIPROCITY_PARENT_PACKAGE" for row in inventory) == 40
    for row in inventory:
        path = ROOT / row["path"]
        assert path.is_file()
        assert sha256(path) == row["sha256"]
        assert path.stat().st_size == int(row["bytes"])
        blob = subprocess.check_output(
            ["git", "rev-parse", f'{BASE}:{row["path"]}'], cwd=ROOT, text=True
        ).strip()
        assert blob == row["git_blob"]
    assert len(premises) == len({row["premise_id"] for row in premises}) == 18
    assert len(interpretations) == len({row["candidate_id"] for row in interpretations}) == 12
    assert len(return_types) == len({row["type_id"] for row in return_types}) == 8
    prereg = (PKG / "PREREGISTRATION.md").read_text(encoding="utf-8")
    for label in [
        "GLOBAL_LOCAL_MUTUAL_DETERMINATION_DERIVED",
        "METRIC_COMPLETENESS_SUPPLIES_ADMISSIBILITY_ONLY",
        "BOOTSTRAP_IS_DISTINCT_POSIT",
        "SEMANTICALLY_UNDERSPECIFIED_BLOCKED",
        "SOURCE_CONFLICT_OR_SCOPE_BROKEN",
    ]:
        assert label in prereg
    print("PASS premise-audit preregistration: sources=1424 premises=18 interpretations=12 return_types=8")


if __name__ == "__main__":
    main()
