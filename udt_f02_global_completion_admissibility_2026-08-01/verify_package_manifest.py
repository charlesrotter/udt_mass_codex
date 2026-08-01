#!/usr/bin/env python3
"""Verify the immutable package manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


PKG = Path(__file__).resolve().parent
MANIFEST = PKG / "PACKAGE_MANIFEST.sha256"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    count = 0
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        expected, name = line.split(None, 1)
        path = PKG / name.strip()
        assert path.is_file() and digest(path) == expected
        count += 1
    assert count == len([p for p in PKG.iterdir() if p.is_file() and p != MANIFEST])
    print(f"PASS package files={count}")


if __name__ == "__main__":
    main()
