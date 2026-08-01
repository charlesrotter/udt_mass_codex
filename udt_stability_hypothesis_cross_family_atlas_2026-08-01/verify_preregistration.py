#!/usr/bin/env python3
"""Fail-closed preregistration verifier."""

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
    if len(source) != 1469 or paths != sorted(paths) or len(paths) != len(set(paths)):
        raise RuntimeError("source census/order/uniqueness failure")
    if any(not (ROOT / row["path"]).is_file() or sha256(ROOT / row["path"]) != row["sha256"] for row in source):
        raise RuntimeError("source byte failure")
    layers = {name: sum(row["layer"] == name for row in source) for name in {
        "PARENT_PREMISE_AUDIT_SOURCE_UNIVERSE",
        "GLOBAL_LOCAL_PREMISE_PARENT_PACKAGE",
        "CONTROLLING_ANCHOR_ADDITION_CORRECTION_02",
    }}
    if layers != {
        "PARENT_PREMISE_AUDIT_SOURCE_UNIVERSE": 1424,
        "GLOBAL_LOCAL_PREMISE_PARENT_PACKAGE": 42,
        "CONTROLLING_ANCHOR_ADDITION_CORRECTION_02": 3,
    }:
        raise RuntimeError(f"source layer failure: {layers}")
    required_additions = {
        "PONDER_MATH_ELEGANCE_2026-07-31.md",
        "udt_p4_period_gate_2026-07-30/AUDIT_REPORT.md",
        "udt_p4_period_gate_2026-07-30/PERIOD_LEDGER.tsv",
    }
    observed_additions = {
        row["path"] for row in source if row["layer"] == "CONTROLLING_ANCHOR_ADDITION_CORRECTION_02"
    }
    if observed_additions != required_additions:
        raise RuntimeError(f"correction 02 source failure: {sorted(observed_additions)}")

    families = rows("FAMILY_UNIVERSE.tsv")
    claims = rows("HYPOTHESIS_CLAIM_UNIVERSE.tsv")
    premises = rows("PREMISE_LEDGER.tsv")
    outcomes = rows("OUTCOME_LABELS.tsv")
    if [row["family_id"] for row in families] != [f"F{i:02d}" for i in range(1, 8)]:
        raise RuntimeError("family universe failure")
    if [row["claim_id"] for row in claims] != [f"H{i:02d}" for i in range(1, 9)]:
        raise RuntimeError("claim universe failure")
    if [row["premise_id"] for row in premises] != [f"P{i:02d}" for i in range(1, 19)]:
        raise RuntimeError("premise universe failure")
    if len(outcomes) != 6 or len({row["outcome"] for row in outcomes}) != 6:
        raise RuntimeError("outcome universe failure")
    print("PASS atlas preregistration: sources=1469 families=7 claims=8 premises=18 outcomes=6")


if __name__ == "__main__":
    main()
