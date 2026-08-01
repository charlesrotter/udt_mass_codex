#!/usr/bin/env python3
"""Verify the frozen flat-package SHA-256 manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "PACKAGE_MANIFEST.sha256"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


rows = []
for line in MANIFEST.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    expected, name = line.split("  ", 1)
    path = HERE / name
    assert path.is_file() and digest(path) == expected
    rows.append(name)
actual = sorted(path.name for path in HERE.iterdir() if path.is_file() and path != MANIFEST)
assert rows == actual and len(rows) == len(set(rows))
print(f"PASS package manifest verification: files={len(rows)}")
