#!/usr/bin/env python3
"""Verify the frozen package without importing a builder."""

from __future__ import annotations

import hashlib
from pathlib import Path


PKG = Path(__file__).resolve().parent
MANIFEST = PKG / "PACKAGE_MANIFEST.sha256"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    rows = []
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if line.strip():
            expected, name = line.split(None, 1)
            name = name.strip()
            target = PKG / name
            assert name != MANIFEST.name and target.is_file() and digest(target) == expected
            rows.append(name)
    assert len(rows) == len(set(rows))
    actual = sorted(path.name for path in PKG.iterdir() if path.is_file() and path != MANIFEST)
    assert sorted(rows) == actual
    print(f"PASS package files={len(rows)} manifest_sha256={digest(MANIFEST)}")


if __name__ == "__main__":
    main()
