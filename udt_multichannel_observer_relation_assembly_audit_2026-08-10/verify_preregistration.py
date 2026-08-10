#!/usr/bin/env python3
"""Verify frozen preregistration structure and source identities."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "3330601b9fd04adc9a9f78e13e5756bd868ba146"
PROTECTED = "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02"


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> int:
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == BASE
    sources = rows("SOURCE_MANIFEST.tsv")
    assert len(sources) == 19
    assert [row["source_id"] for row in sources] == [f"S{i:02d}" for i in range(1, 20)]
    assert all(PROTECTED not in row["path"] for row in sources)
    for row in sources:
        data = subprocess.check_output(["git", "show", row["source_ref"]], cwd=ROOT)
        assert len(data) == int(row["size"]), row["path"]
        assert hashlib.sha256(data).hexdigest() == row["sha256"], row["path"]
        blob = subprocess.check_output(
            ["git", "rev-parse", row["source_ref"]], cwd=ROOT, text=True
        ).strip()
        assert blob == row["git_blob"], row["path"]
    assert len(rows("PREMISE_LEDGER.tsv")) == 15
    assert len(rows("CHANNEL_UNIVERSE.tsv")) == 16
    assert len(rows("EQUIVALENCE_CONTRACT.tsv")) == 10
    assert len(rows("REGIME_AXIS.tsv")) == 8
    assert len(rows("FALSIFICATION_CONTRACT.tsv")) == 14
    print("PASS: base pinned; 19/19 sources; 15 premises; 16 candidates; 10 equivalences; 8 regime axes; 14 falsifiers; protected atlas excluded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
