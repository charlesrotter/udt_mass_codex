#!/usr/bin/env python3
"""Verify the non-self-referential G75 package SHA-256 manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent


def main() -> None:
    rows = []
    for line in (HERE / "PACKAGE_SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, name = line.split(None, 1)
        target = HERE / name.strip()
        assert target.is_file(), name
        assert hashlib.sha256(target.read_bytes()).hexdigest() == expected, name
        rows.append(name.strip())
    assert len(rows) == len(set(rows)) == 23
    print("PASS: 23 G75 package hashes")


if __name__ == "__main__":
    main()
