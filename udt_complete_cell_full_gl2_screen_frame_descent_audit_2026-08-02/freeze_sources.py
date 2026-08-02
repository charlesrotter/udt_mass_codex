#!/usr/bin/env python3
"""Freeze the preregistered source authority set."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


with (HERE / "SOURCE_SCOPE.tsv").open(newline="", encoding="utf-8") as handle:
    scope = list(csv.DictReader(handle, delimiter="\t"))
assert len(scope) == len({row["path"] for row in scope})
rows = []
for row in scope:
    path = ROOT / row["path"]
    assert path.is_file()
    blob = subprocess.run(
        ["git", "rev-parse", f"HEAD:{row['path']}"], cwd=ROOT,
        text=True, capture_output=True, check=True,
    ).stdout.strip()
    rows.append({
        "path": row["path"], "role": row["role"], "git_blob": blob,
        "bytes": str(path.stat().st_size), "sha256": digest(path),
    })
with (HERE / "SOURCE_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(
        handle, delimiter="\t", fieldnames=["path", "role", "git_blob", "bytes", "sha256"],
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)
print(f"PASS frozen sources={len(rows)}")
