#!/usr/bin/env python3
"""Verify the additions-only ontology source-correction layer."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent


def read(name: str) -> list[dict[str, str]]:
    with (PKG / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    original = read("SOURCE_INVENTORY.tsv")
    added = read("SOURCE_ADDENDUM.tsv")
    effective = read("EFFECTIVE_SOURCE_INVENTORY.tsv")
    expected_added = {
        "NEGATIVES_REGISTRY.md",
        "udt_p4_bookkeeping_forcing_2026-07-29/EXACT_DERIVATION.md",
        "udt_p4_routeD_field_registration_2026-07-29/AUDIT_REPORT.md",
    }
    if len(original) != 1605 or len(added) != 3 or {row["path"] for row in added} != expected_added:
        raise RuntimeError("source-correction census failure")
    if {row["path"] for row in original} & expected_added:
        raise RuntimeError("source correction is not additions-only")
    paths = [row["path"] for row in effective]
    if len(paths) != 1608 or paths != sorted(paths) or len(paths) != len(set(paths)):
        raise RuntimeError("effective source order/uniqueness failure")
    if set(paths) != {row["path"] for row in original} | expected_added:
        raise RuntimeError("effective source union failure")
    for row in effective:
        path = ROOT / row["path"]
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"]:
            raise RuntimeError(f"effective source byte mismatch: {row['path']}")
    print("PASS source correction: original=1605 added=3 effective=1608")


if __name__ == "__main__":
    main()
