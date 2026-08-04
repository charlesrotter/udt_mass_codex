#!/usr/bin/env python3
"""Freeze the preregistered source universe deterministically."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


paths = [line for line in (HERE / "SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines() if line]
assert len(paths) == len(set(paths)) == 32

rows = []
hash_lines = []
for relative in paths:
    path = ROOT / relative
    assert path.is_file(), relative
    blob = subprocess.check_output(["git", "hash-object", relative], cwd=ROOT, text=True).strip()
    commit = subprocess.check_output(["git", "log", "-1", "--format=%H", "--", relative], cwd=ROOT, text=True).strip()
    digest = sha256(path)
    rows.append({"path": relative, "blob": blob, "sha256": digest, "bytes": path.stat().st_size, "last_commit": commit})
    hash_lines.append(f"{digest}  ../{relative}\n")

with (HERE / "SOURCE_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=("path", "blob", "sha256", "bytes", "last_commit"), delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

(HERE / "SOURCE_MANIFEST.sha256").write_text("".join(hash_lines), encoding="utf-8")
print(f"PASS sources={len(rows)} manifest_sha256={sha256(HERE / 'SOURCE_MANIFEST.sha256')}")

