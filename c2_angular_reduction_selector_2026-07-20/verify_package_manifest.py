#!/usr/bin/env python3
"""Fail closed on package hash or coverage drift."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDED = {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}


def main() -> None:
    manifest = HERE/"SHA256SUMS.txt"
    entries = [line.split("  ", 1) for line in manifest.read_text(encoding="utf-8").splitlines() if line]
    names = [name for _, name in entries]
    actual = sorted(path.name for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDED)
    if names != actual or len(names) != len(set(names)):
        raise AssertionError(f"coverage mismatch: {sorted(set(names)^set(actual))}")
    for expected, name in entries:
        if hashlib.sha256((HERE/name).read_bytes()).hexdigest() != expected:
            raise AssertionError(f"hash mismatch: {name}")
    print(f"PASS entries={len(entries)} manifest_sha256={hashlib.sha256(manifest.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
