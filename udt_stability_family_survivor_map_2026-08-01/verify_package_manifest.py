#!/usr/bin/env python3
"""Verify deterministic survivor-map package manifest."""

import hashlib
from pathlib import Path


PKG = Path(__file__).resolve().parent
MANIFEST = PKG / "PACKAGE_MANIFEST.sha256"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


records = [line for line in MANIFEST.read_text(encoding="utf-8").splitlines() if line]
expected_names = {path.name for path in PKG.iterdir() if path.is_file() and path.name != MANIFEST.name}
actual_names = set()
for line in records:
    expected, name = line.split(None, 1)
    name = name.strip()
    if not (PKG / name).is_file() or sha256(PKG / name) != expected:
        raise RuntimeError(f"manifest mismatch: {name}")
    actual_names.add(name)
if actual_names != expected_names:
    raise RuntimeError(f"manifest coverage mismatch: missing={sorted(expected_names - actual_names)} extra={sorted(actual_names - expected_names)}")
print(f"PASS package manifest verification: files={len(records)}")
