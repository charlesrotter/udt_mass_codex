#!/usr/bin/env python3
"""Replay the frozen source manifest from the preregistered Git base."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "3897ef1152af9ef79fc24aee8fe91403a22e4119"


with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
    rows = list(csv.DictReader(stream, delimiter="\t"))
assert len(rows) == 10
assert len({row["path"] for row in rows}) == 10
for row in rows:
    completed = subprocess.run(
        ["git", "show", f"{BASE}:{row['path']}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    assert hashlib.sha256(completed.stdout).hexdigest() == row["sha256"], row["path"]
print(f"PASS base={BASE} sources={len(rows)}")
