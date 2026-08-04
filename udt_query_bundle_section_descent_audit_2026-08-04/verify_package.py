#!/usr/bin/env python3
"""Verify the frozen package as a closed regular-file set."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDED = {"PACKAGE_MANIFEST.sha256", "PACKAGE_VERIFICATION.json"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


rows: list[tuple[str, str]] = []
for line in (HERE / "PACKAGE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
    expected, name = line.split(None, 1)
    rows.append((expected, name.strip()))

assert len(rows) == len({name for _, name in rows}) == 48
actual = {path.name for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDED}
assert actual == {name for _, name in rows}
for expected, name in rows:
    assert digest(HERE / name) == expected

result = {
    "status": "PASS",
    "package_members": len(rows),
    "manifest_sha256": digest(HERE / "PACKAGE_MANIFEST.sha256"),
    "source_manifest_sha256": digest(HERE / "SOURCE_MANIFEST.tsv"),
    "review_sha256": digest(HERE / "FRESH_ADVERSARIAL_REVIEW.md"),
}
(HERE / "PACKAGE_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, sort_keys=True))
