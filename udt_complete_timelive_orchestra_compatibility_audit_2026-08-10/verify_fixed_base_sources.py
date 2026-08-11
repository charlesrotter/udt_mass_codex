#!/usr/bin/env python3
"""Verify the frozen source manifest against the preregistered Git base."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "78f925459eb7ee8a4251dcc86460d3c581634bc8"


def git_bytes(path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{BASE}:{path}"], cwd=ROOT, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    return result.stdout


with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle, delimiter="\t"))

assert len(rows) == 13
assert len({row["path"] for row in rows}) == 13
for row in rows:
    actual = hashlib.sha256(git_bytes(row["path"])).hexdigest()
    assert actual == row["sha256"], row["path"]

print(f"PASS fixed_base={BASE} sources={len(rows)}")
