#!/usr/bin/env python3
"""Verify the sweep package manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


PKG = Path(__file__).resolve().parent
MANIFEST = PKG / "PACKAGE_MANIFEST.sha256"


def main() -> None:
    expected = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        digest, name = line.split(None, 1)
        expected[name.strip()] = digest
    actual_names = {path.name for path in PKG.iterdir() if path.is_file() and path != MANIFEST}
    if actual_names != set(expected):
        raise RuntimeError(f"manifest membership mismatch: missing={set(expected)-actual_names} extra={actual_names-set(expected)}")
    for name, digest in expected.items():
        if hashlib.sha256((PKG / name).read_bytes()).hexdigest() != digest:
            raise RuntimeError(f"manifest hash mismatch: {name}")
    print(f"PASS package manifest verification: files={len(expected)}")


if __name__ == "__main__":
    main()
