#!/usr/bin/env python3
"""Fail closed on the preregistered solved-geometry atlas."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REQUIRED = {
    "PREREGISTRATION.md", "PONDER_MAP.md", "PREMISE_LEDGER.tsv", "SOLVER_COMPLETENESS_MAP.md",
    "SURVIVOR_AXES.tsv", "WITNESS_UNIVERSE.tsv", "FALSIFICATION_CONTRACT.tsv",
    "SOURCE_MANIFEST.tsv",
}
assert all((HERE / name).is_file() for name in REQUIRED)


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


sources = rows("SOURCE_MANIFEST.tsv")
assert len(sources) == len({row["path"] for row in sources}) == 22
for row in sources:
    path = ROOT / row["path"]
    assert path.is_file(), row["path"]
    assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"], row["path"]
    assert "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02" not in row["path"]
    assert "udt_native_onshell_timelive_reset_owner_audit_2026-08-10" not in row["path"]
assert len(rows("PREMISE_LEDGER.tsv")) == 12
assert len(rows("SURVIVOR_AXES.tsv")) == 12
assert len(rows("WITNESS_UNIVERSE.tsv")) == 5
assert len(rows("FALSIFICATION_CONTRACT.tsv")) == 18
text = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
for token in (
    "geometric persistence", "not call perturbation persistence", "INSUFFICIENT_OWNED_SOLVED_GEOMETRY_DATA",
    "TYPE_FAILURE_IN_MATCHED_COMPARISON", "fresh adversarial review",
):
    assert token in text
print("PASS preregistration files=8 sources=22 premises=12 axes=12 witnesses=5 tests=18")
