#!/usr/bin/env python3
"""Fail closed on the from-scratch history-restriction preregistration."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REQUIRED = {
    "PREREGISTRATION.md", "PONDER_MAP.md", "PREMISE_LEDGER.tsv",
    "CANDIDATE_OWNER_CLASSES.tsv", "FALSIFICATION_CONTRACT.tsv", "SOURCE_MANIFEST.tsv",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


missing = sorted(name for name in REQUIRED if not (HERE / name).is_file())
assert not missing, missing
with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
    rows = list(csv.DictReader(stream, delimiter="\t"))
assert len(rows) == 10
assert len({row["path"] for row in rows}) == 10
for row in rows:
    path = ROOT / row["path"]
    assert path.is_file(), row["path"]
    assert digest(path) == row["sha256"], row["path"]
    assert "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02" not in row["path"]
    assert "udt_native_onshell_timelive_reset_owner_audit_2026-08-10" not in row["path"]

text = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
for token in (
    "from-scratch metric-led ownership audit",
    "No broad legacy census is authorized",
    "COMPLETE_REGULAR_CHART_IS_LOCALLY_JET_OPEN",
    "Bootstrap remains a working hypothesis and is inactive",
):
    assert token in text, token

print(f"PASS preregistration files={len(REQUIRED)} sources={len(rows)} candidates=5")
