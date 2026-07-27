#!/usr/bin/env python3
"""Freeze the preregistered source scope by Git blob and byte SHA-256."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


rows = []
with (HERE / "SOURCE_SCOPE.tsv").open(newline="", encoding="utf-8") as handle:
    for row in csv.DictReader(handle, delimiter="\t"):
        path = ROOT / row["path"]
        data = path.read_bytes()
        rows.append(
            {
                **row,
                "git_blob": git("rev-parse", f"HEAD:{row['path']}"),
                "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": str(len(data)),
            }
        )

with (HERE / "SOURCE_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as handle:
    fields = ["source_id", "path", "role", "git_blob", "sha256", "bytes"]
    writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

print(f"frozen_sources={len(rows)}")

