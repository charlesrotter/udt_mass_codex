#!/usr/bin/env python3
"""Verify the completed audit package manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


PKG = Path(__file__).resolve().parent
MANIFEST = PKG / "PACKAGE_MANIFEST.sha256"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


rows = [line for line in MANIFEST.read_text(encoding="utf-8").splitlines() if line.strip()]
expected_names = {p.name for p in PKG.iterdir() if p.is_file() and p.name != MANIFEST.name}
manifest_names = set()
for line in rows:
    expected, name = line.split(None, 1)
    name = name.strip()
    target = PKG / name
    if not target.is_file() or sha256(target) != expected:
        raise RuntimeError(f"manifest mismatch: {name}")
    manifest_names.add(name)
if manifest_names != expected_names:
    raise RuntimeError(f"manifest coverage mismatch: missing={sorted(expected_names-manifest_names)} extra={sorted(manifest_names-expected_names)}")
print(f"PASS package manifest verification: files={len(rows)}")
