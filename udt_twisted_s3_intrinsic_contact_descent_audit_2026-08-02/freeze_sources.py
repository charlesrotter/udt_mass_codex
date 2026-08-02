#!/usr/bin/env python3
"""Freeze exact source blobs for the intrinsic contact descent audit."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


with (HERE / "SOURCE_SCOPE.tsv").open(newline="", encoding="utf-8") as handle:
    scope = list(csv.DictReader(handle, delimiter="\t"))
assert len(scope) == len({row["path"] for row in scope}) == 30

rows = []
for item in scope:
    path = ROOT / item["path"]
    assert path.is_file(), item["path"]
    blob = subprocess.run(
        ["git", "rev-parse", f"HEAD:{item['path']}"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()
    content = subprocess.run(
        ["git", "cat-file", "blob", blob],
        cwd=ROOT,
        capture_output=True,
        check=True,
    ).stdout
    assert content == path.read_bytes()
    rows.append({
        "path": item["path"],
        "role": item["role"],
        "git_blob": blob,
        "bytes": str(len(content)),
        "sha256": sha256_bytes(content),
    })

with (HERE / "SOURCE_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(
        handle,
        delimiter="\t",
        fieldnames=["path", "role", "git_blob", "bytes", "sha256"],
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)

manifest_hash = sha256_bytes((HERE / "SOURCE_MANIFEST.tsv").read_bytes())
(HERE / "SOURCE_MANIFEST.sha256").write_text(manifest_hash + "\n", encoding="utf-8")
print(f"PASS frozen_sources={len(rows)} manifest_sha256={manifest_hash}")

