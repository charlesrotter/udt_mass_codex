#!/usr/bin/env python3
"""Verify banked R3 evidence and the self-contained ScratchDisk raw-output archive."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SCRATCH = Path("/media/udt-admin/ScratchDisk/Data/UDT_BOSS_R3_2026-08-14")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path):
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def check(base, records):
    for row in records:
        path = base / row["artifact"]
        assert path.stat().st_size == int(row["bytes"])
        assert digest(path) == row["sha256"]


def main() -> int:
    final_records = rows(ROOT / "R3_FINAL_EVIDENCE_MANIFEST.tsv")
    check(ROOT, final_records)
    output_records = rows(SCRATCH / "R3_OUTPUT_MANIFEST.tsv")
    assert len(output_records) == 201
    check(SCRATCH, output_records)
    print(
        f"PASS: R3 final package ({len(final_records)} banked evidence rows; "
        f"{len(output_records)} ScratchDisk output rows)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
