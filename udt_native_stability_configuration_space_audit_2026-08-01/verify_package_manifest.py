#!/usr/bin/env python3
"""Fail closed on any missing, extra, duplicated, or byte-mismatched package file."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


PKG = Path(__file__).resolve().parent
EXCLUDE = {"PACKAGE_MANIFEST.sha256", "PACKAGE_VERIFICATION_RESULT.json"}


def main() -> None:
    rows = []
    for line in (PKG / "PACKAGE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        rows.append((name, digest))
    names = [name for name, _digest in rows]
    if len(names) != len(set(names)):
        raise AssertionError("duplicate manifest path")
    actual = sorted(path.name for path in PKG.iterdir() if path.is_file() and path.name not in EXCLUDE)
    if names != actual:
        raise AssertionError("manifest coverage differs from package files")
    for name, expected in rows:
        observed = hashlib.sha256((PKG / name).read_bytes()).hexdigest()
        if observed != expected:
            raise AssertionError(f"package hash mismatch: {name}")
    result = {"status": "PASS", "manifested_files": len(rows)}
    (PKG / "PACKAGE_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
