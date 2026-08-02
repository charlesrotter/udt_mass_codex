#!/usr/bin/env python3
"""Fail closed on missing, extra, duplicate, or mutated package files."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


PKG = Path(__file__).resolve().parent
EXCLUDED = {"PACKAGE_MANIFEST.sha256", "PACKAGE_MANIFEST_VERIFICATION.json"}


def main() -> int:
    manifest = PKG / "PACKAGE_MANIFEST.sha256"
    rows = []
    for line in manifest.read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        rows.append((digest, name))
    names = [name for _, name in rows]
    actual = sorted(path.name for path in PKG.iterdir() if path.is_file() and path.name not in EXCLUDED)
    checks = {
        "manifest_rows_unique": len(names) == len(set(names)),
        "manifest_complete_exact_file_set": sorted(names) == actual,
        "all_sha256_match": all(
            (PKG / name).is_file() and hashlib.sha256((PKG / name).read_bytes()).hexdigest() == digest
            for digest, name in rows
        ),
    }
    result = {
        "checks": checks,
        "files_manifested": len(rows),
        "manifest_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest(),
        "status": "PASS" if all(checks.values()) else "FAIL",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
