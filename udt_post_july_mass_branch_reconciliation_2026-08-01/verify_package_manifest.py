#!/usr/bin/env python3
"""Verify the frozen reconciliation package without importing its builder."""

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
        if not line.strip():
            continue
        expected, name = line.split(None, 1)
        name = name.strip()
        assert name != MANIFEST.name
        target = PKG / name
        assert target.is_file(), name
        assert digest(target) == expected, name
        rows.append(name)
    assert len(rows) == len(set(rows))
    actual = sorted(path.name for path in PKG.iterdir() if path.is_file() and path != MANIFEST)
    assert sorted(rows) == actual
    print(f"PASS package files={len(rows)} manifest_sha256={digest(MANIFEST)}")


if __name__ == "__main__":
    main()
