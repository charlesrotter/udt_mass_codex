#!/usr/bin/env python3
"""Verify complete SHA-256 coverage of this audit package."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "SHA256SUMS.txt"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    expected = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        sha, name = line.split(None, 1)
        expected[name.strip()] = sha
    actual = {path.name for path in HERE.iterdir() if path.is_file() and path.name != MANIFEST.name}
    assert set(expected) == actual, (sorted(set(expected) - actual), sorted(actual - set(expected)))
    for name, sha in expected.items():
        assert digest(HERE / name) == sha, name
    print(f"PASS: {len(expected)} package files")


if __name__ == "__main__":
    main()
