#!/usr/bin/env python3
"""Fail closed if the audit package differs from SHA256SUMS.txt."""

from __future__ import annotations

import hashlib
import pathlib


def main() -> None:
    package = pathlib.Path(__file__).resolve().parent
    manifest = package / "SHA256SUMS.txt"
    registered: dict[str, str] = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        if name in registered:
            raise AssertionError(f"duplicate manifest path: {name}")
        registered[name] = digest
    actual = {
        path.name for path in package.iterdir()
        if path.is_file() and path.name != manifest.name
    }
    if set(registered) != actual:
        raise AssertionError(
            f"manifest coverage mismatch missing={sorted(actual - set(registered))} "
            f"extra={sorted(set(registered) - actual)}"
        )
    for name, expected in registered.items():
        path = package / name
        if path.is_symlink() or not path.is_file():
            raise AssertionError(f"not a regular package file: {name}")
        observed = hashlib.sha256(path.read_bytes()).hexdigest()
        if observed != expected:
            raise AssertionError(f"hash mismatch: {name}")
    print(f"MANIFEST PASS entries={len(registered)}")


if __name__ == "__main__":
    main()
