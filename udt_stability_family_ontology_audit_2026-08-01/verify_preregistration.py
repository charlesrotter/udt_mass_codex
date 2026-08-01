#!/usr/bin/env python3
"""Fail-closed verifier for the ontology-audit preregistration."""

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
    if len(source) != 1605 or paths != sorted(paths) or len(paths) != len(set(paths)):
        raise RuntimeError("source census/order/uniqueness failure")
    if any(not (ROOT / row["path"]).is_file() or sha256(ROOT / row["path"]) != row["sha256"] for row in source):
        raise RuntimeError("source byte failure")
    layers = {name: sum(row["layer"] == name for row in source) for name in {"PARENT_SWEEP_SOURCE_UNIVERSE", "COMPLETE_PARENT_SWEEP_PACKAGE"}}
    if layers != {"PARENT_SWEEP_SOURCE_UNIVERSE": 1558, "COMPLETE_PARENT_SWEEP_PACKAGE": 47}:
        raise RuntimeError(f"source layers changed: {layers}")
    families = rows("FAMILY_UNIVERSE.tsv")
    axes = rows("ONTOLOGY_AXIS_UNIVERSE.tsv")
    pairs = rows("PAIRWISE_UNIVERSE.tsv")
    statuses = rows("ONTOLOGY_STATUS_LABELS.tsv")
    relations = rows("PAIR_RELATION_LABELS.tsv")
    outcomes = rows("OUTCOME_LABELS.tsv")
    if [row["family_id"] for row in families] != [f"F{i:02d}" for i in range(1, 8)]:
        raise RuntimeError("family universe failure")
    if [row["axis_id"] for row in axes] != [f"A{i:02d}" for i in range(1, 11)]:
        raise RuntimeError("axis universe failure")
    if len(pairs) != 28 or len({(row["left_family"], row["right_family"]) for row in pairs}) != 28:
        raise RuntimeError("pair universe failure")
    if sum(row["diagonal"] == "YES" for row in pairs) != 7:
        raise RuntimeError("pair diagonal failure")
    if len(statuses) != 9 or len(relations) != 11 or len(outcomes) != 5:
        raise RuntimeError("label universe failure")
    print("PASS ontology preregistration: sources=1605 families=7 axes=10 pairs=28 statuses=9 relations=11 outcomes=5")


if __name__ == "__main__":
    main()
