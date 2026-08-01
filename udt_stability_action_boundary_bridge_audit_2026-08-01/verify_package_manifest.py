#!/usr/bin/env python3
"""Verify the package manifest and report its identity."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


PKG = Path(__file__).resolve().parent
EXCLUDED = {"PACKAGE_MANIFEST.sha256", "PACKAGE_VERIFICATION_RESULT.json"}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    manifest = PKG / "PACKAGE_MANIFEST.sha256"
    rows = []
    for line in manifest.read_text(encoding="utf-8").splitlines():
        expected, name = line.split(None, 1)
        target = PKG / name.strip()
        if not target.is_file() or digest(target) != expected:
            raise AssertionError(target)
        rows.append(name.strip())
    expected_names = sorted(
        path.name for path in PKG.iterdir()
        if path.is_file() and path.name not in EXCLUDED
    )
    if rows != expected_names or len(rows) != len(set(rows)):
        raise AssertionError("manifest coverage mismatch")
    result = {
        "status": "PASS",
        "manifested_files": len(rows),
        "manifest_sha256": digest(manifest),
        "excluded_generated_files": sorted(EXCLUDED),
    }
    (PKG / "PACKAGE_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

