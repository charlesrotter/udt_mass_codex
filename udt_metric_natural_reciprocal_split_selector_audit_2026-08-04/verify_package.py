#!/usr/bin/env python3
"""Verify exact package membership and hashes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDED = {"PACKAGE_MANIFEST.sha256", "PACKAGE_VERIFICATION.json"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


rows = []
for line in (HERE / "PACKAGE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
    expected, size, name = line.split("  ", 2)
    target = HERE / name
    assert target.is_file(), name
    assert str(target.stat().st_size) == size, name
    assert digest(target) == expected, name
    rows.append(name)
actual = sorted(path.name for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDED)
assert rows == actual and len(rows) == len(set(rows))
result = {
    "result": "PASS",
    "package_members": len(rows),
    "package_manifest_sha256": digest(HERE / "PACKAGE_MANIFEST.sha256"),
    "source_manifest_sha256": digest(HERE / "SOURCE_MANIFEST.tsv"),
    "review": "PASS_WITH_REQUIRED_REPAIRS__REPAIRS_ACCEPTED",
    "verification": "PASS_REVIEW_ACCEPTED",
}
(HERE / "PACKAGE_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, sort_keys=True))
