#!/usr/bin/env python3
"""Replay the preregistered source census from its fixed Git base."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "52960c35232c67cab757e238b9f69df94c9e0d0e"


with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
    rows = list(csv.DictReader(stream, delimiter="\t"))
assert len(rows) == len({row["path"] for row in rows}) == 15
for row in rows:
    completed = subprocess.run(
        ["git", "show", f"{BASE}:{row['path']}"], cwd=ROOT, check=True, capture_output=True
    )
    assert hashlib.sha256(completed.stdout).hexdigest() == row["sha256"], row["path"]
    assert "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02" not in row["path"]
    assert "udt_native_onshell_timelive_reset_owner_audit_2026-08-10" not in row["path"]
print(f"PASS base={BASE} sources={len(rows)}")
