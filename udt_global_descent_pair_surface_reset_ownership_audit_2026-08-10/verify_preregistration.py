#!/usr/bin/env python3
"""Fail closed on the G56 preregistration and pinned source corpus."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED_BASE = "eca93e1395c2f690f8357f015ea5901fec9f8310"


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> int:
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == EXPECTED_BASE
    sources = rows("SOURCE_MANIFEST.tsv")
    assert len(sources) == 20
    assert [row["source_id"] for row in sources] == [f"S{i:02d}" for i in range(1, 21)]
    for row in sources:
        raw = subprocess.check_output(["git", "show", row["source_ref"]], cwd=ROOT)
        assert len(raw) == int(row["size"]), row["path"]
        assert hashlib.sha256(raw).hexdigest() == row["sha256"], row["path"]
        assert subprocess.check_output(
            ["git", "rev-parse", row["source_ref"]], cwd=ROOT, text=True
        ).strip() == row["git_blob"], row["path"]
    assert len(rows("CANDIDATE_UNIVERSE.tsv")) == 10
    assert len(rows("DESCENT_AXES.tsv")) == 10
    assert len(rows("FALSIFICATION_CONTRACT.tsv")) == 19
    assert len(rows("PREMISE_LEDGER.tsv")) == 10
    protected = "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/"
    assert all(not row["path"].startswith(protected) for row in sources)
    print("PASS: G56 preregistration; 20 pinned sources; 10 candidate sets; 10 axes; 19 falsification tests; protected atlas excluded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
