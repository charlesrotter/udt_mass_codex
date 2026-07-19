#!/usr/bin/env python3
"""Fail closed on any package file missing from or differing from SHA256SUMS."""

from __future__ import annotations

import hashlib
import pathlib


def main() -> None:
    package = pathlib.Path(__file__).resolve().parent
    manifest = package / "SHA256SUMS.txt"
    expected: dict[str, str] = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        if name in expected:
            raise AssertionError(f"duplicate manifest row: {name}")
        expected[name] = digest
    excluded = {manifest.name, "REPOSITORY_GATES.json"}
    actual = {path.name for path in package.iterdir() if path.is_file() and path.name not in excluded}
    if set(expected) != actual:
        raise AssertionError(f"manifest coverage mismatch missing={actual-set(expected)} extra={set(expected)-actual}")
    for name, digest in expected.items():
        observed = hashlib.sha256(package.joinpath(name).read_bytes()).hexdigest()
        if observed != digest:
            raise AssertionError(f"hash mismatch: {name}")
    print(f"MANIFEST VERIFIED entries={len(expected)}")


if __name__ == "__main__":
    main()
