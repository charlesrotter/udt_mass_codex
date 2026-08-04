#!/usr/bin/env python3
"""Freeze tracked controlling inputs by Git blob, SHA-256, and byte size."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


paths = [line.strip() for line in (HERE / "SOURCE_PATHS.txt").read_text().splitlines() if line.strip()]
assert len(paths) == len(set(paths)) == 24

rows = ["path\tgit_blob\tsha256\tbytes"]
for relative in paths:
    path = ROOT / relative
    assert path.is_file(), relative
    blob = subprocess.check_output(["git", "rev-parse", f"HEAD:{relative}"], cwd=ROOT, text=True).strip()
    rows.append(f"{relative}\t{blob}\t{sha256(path)}\t{path.stat().st_size}")

(HERE / "SOURCE_MANIFEST.tsv").write_text("\n".join(rows) + "\n")
print(f"PASS: {len(paths)} controlling sources frozen")
