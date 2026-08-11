#!/usr/bin/env python3
"""Fail closed on the time-live orchestra preregistration and frozen sources."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REQUIRED = {
    "PREREGISTRATION.md", "PONDER_MAP.md", "PREMISE_LEDGER.tsv", "TIMELIVE_AXES.tsv",
    "FALSIFICATION_CONTRACT.tsv", "COMPLETENESS_MAP.md", "SOURCE_MANIFEST.tsv",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


missing = sorted(name for name in REQUIRED if not (HERE / name).is_file())
assert not missing, missing
with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
    rows = list(csv.DictReader(stream, delimiter="\t"))
assert len(rows) == 13
assert len({row["path"] for row in rows}) == 13
for row in rows:
    path = ROOT / row["path"]
    assert path.is_file(), row["path"]
    assert digest(path) == row["sha256"], row["path"]
    assert "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02" not in row["path"]
    assert "udt_native_onshell_timelive_reset_owner_audit_2026-08-10" not in row["path"]

text = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
for token in (
    "No time, angular, shift, scale, or mixing component\nis frozen",
    "bootstrap density/curvature selection",
    "EXACT_COMPATIBILITY_ORCHESTRA_BUT_NO_EVOLUTION_LAW",
    "equations of motion and light cones from characteristics",
):
    assert token in text, token

print(f"PASS preregistration files={len(REQUIRED)} sources={len(rows)}")
