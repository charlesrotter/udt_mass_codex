#!/usr/bin/env python3
"""Fail-closed repository-context verifier for the fixed G213 sources."""

import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
manifest = PACKAGE / "SOURCE_MANIFEST.tsv"
rows = []
for line in manifest.read_text().splitlines()[1:]:
    expected, rel = line.split("\t", 1)
    path = ROOT / rel
    if not path.is_file():
        raise FileNotFoundError(rel)
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        raise AssertionError(f"source hash mismatch: {rel}")
    rows.append(rel)

if len(rows) != 12:
    raise AssertionError(f"expected 12 sources, got {len(rows)}")

print(json.dumps({
    "audit": "G213",
    "status": "PASS",
    "source_count": len(rows),
    "all_source_hashes_match": True,
}, sort_keys=True))

