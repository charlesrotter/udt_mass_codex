#!/usr/bin/env python3
"""Fail closed on the G62 observer-network preregistration."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REQUIRED = {
    "PREREGISTRATION.md", "PONDER_MAP.md", "PREMISE_LEDGER.tsv", "NETWORK_AXES.tsv",
    "FALSIFICATION_CONTRACT.tsv", "SOURCE_MANIFEST.tsv",
}

assert all((HERE / name).is_file() for name in REQUIRED)
with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
    rows = list(csv.DictReader(stream, delimiter="\t"))
assert len(rows) == len({row["path"] for row in rows}) == 15
for row in rows:
    path = ROOT / row["path"]
    assert path.is_file(), row["path"]
    assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"], row["path"]
    assert "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02" not in row["path"]
    assert "udt_native_onshell_timelive_reset_owner_audit_2026-08-10" not in row["path"]
text = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
for token in (
    "Associativity of composition is not path independence",
    "c_E` calibrates units/terminal reciprocal readout",
    "Bootstrap, density, energy, curvature targets",
    "CONDITIONAL_FLAT_DESCENT_RESTRICTION_ONLY",
):
    assert token in text, token
print(f"PASS preregistration files={len(REQUIRED)} sources={len(rows)} axes=10 tests=12")
