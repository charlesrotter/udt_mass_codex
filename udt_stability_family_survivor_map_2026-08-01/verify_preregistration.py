#!/usr/bin/env python3
"""Fail-closed verifier for the survivor-map preregistration."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent


def rows(name: str) -> list[dict[str, str]]:
    with (PKG / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    source = rows("SOURCE_INVENTORY.tsv")
    paths = [row["path"] for row in source]
    if len(source) != 1513 or paths != sorted(paths) or len(paths) != len(set(paths)):
        raise RuntimeError("source census/order/uniqueness failure")
    if any(not (ROOT / row["path"]).is_file() or sha256(ROOT / row["path"]) != row["sha256"] for row in source):
        raise RuntimeError("source byte failure")
    layers = {
        name: sum(row["layer"] == name for row in source)
        for name in {"PARENT_EFFECTIVE_SOURCE_UNIVERSE", "COMPLETE_PARENT_ATLAS_PACKAGE"}
    }
    if layers != {"PARENT_EFFECTIVE_SOURCE_UNIVERSE": 1469, "COMPLETE_PARENT_ATLAS_PACKAGE": 44}:
        raise RuntimeError(f"source layers changed: {layers}")

    families = rows("FAMILY_UNIVERSE.tsv")
    cells = rows("CELL_UNIVERSE.tsv")
    readiness = rows("READINESS_LABELS.tsv")
    outcomes = rows("OUTCOME_LABELS.tsv")
    if [row["family_id"] for row in families] != [f"F{i:02d}" for i in range(1, 8)]:
        raise RuntimeError("family universe failure")
    if len({row["effective_partition_key"] for row in families}) != 7:
        raise RuntimeError("family partition overlap")
    if [row["cell_id"] for row in cells] != [f"C{i:02d}" for i in range(1, 13)]:
        raise RuntimeError("cell universe failure")
    if len(readiness) != 11 or len({row["label"] for row in readiness}) != 11:
        raise RuntimeError("readiness universe failure")
    if len(outcomes) != 5 or len({row["outcome"] for row in outcomes}) != 5:
        raise RuntimeError("outcome universe failure")
    print("PASS survivor-map preregistration: sources=1513 families=7 cells=12 readiness=11 outcomes=5")


if __name__ == "__main__":
    main()
