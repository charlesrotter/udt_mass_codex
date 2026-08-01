#!/usr/bin/env python3
"""Fail-closed verifier for the sweep preregistration."""

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
    if len(source) != 1558 or paths != sorted(paths) or len(paths) != len(set(paths)):
        raise RuntimeError("source census/order/uniqueness failure")
    if any(not (ROOT / row["path"]).is_file() or sha256(ROOT / row["path"]) != row["sha256"] for row in source):
        raise RuntimeError("source byte failure")
    layers = {name: sum(row["layer"] == name for row in source) for name in {"PARENT_SURVIVOR_SOURCE_UNIVERSE", "COMPLETE_PARENT_SURVIVOR_PACKAGE"}}
    if layers != {"PARENT_SURVIVOR_SOURCE_UNIVERSE": 1513, "COMPLETE_PARENT_SURVIVOR_PACKAGE": 45}:
        raise RuntimeError(f"source layers changed: {layers}")
    groups = rows("GROUP_UNIVERSE.tsv")
    objects = rows("OBJECT_UNIVERSE.tsv")
    statuses = rows("OBJECT_STATUS_LABELS.tsv")
    outcomes = rows("OUTCOME_LABELS.tsv")
    if [row["group_id"] for row in groups] != [f"Q{i:02d}" for i in range(1, 5)]:
        raise RuntimeError("group universe failure")
    if [row["object_id"] for row in objects] != [f"O{i:02d}" for i in range(1, 16)]:
        raise RuntimeError("object universe failure")
    if len(statuses) != 7 or len({row["status"] for row in statuses}) != 7:
        raise RuntimeError("status universe failure")
    if len(outcomes) != 5 or len({row["outcome"] for row in outcomes}) != 5:
        raise RuntimeError("outcome universe failure")
    print("PASS sweep preregistration: sources=1558 groups=4 objects=15 statuses=7 outcomes=5")


if __name__ == "__main__":
    main()
