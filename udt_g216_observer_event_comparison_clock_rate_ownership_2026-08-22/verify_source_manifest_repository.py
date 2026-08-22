#!/usr/bin/env python3
"""Verify G216 frozen source hashes against the repository root."""

import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
MANIFEST = PACKAGE / "SOURCE_MANIFEST.tsv"

rows = []
for line in MANIFEST.read_text().splitlines()[1:]:
    if not line.strip():
        continue
    expected, relative = line.split("\t", 1)
    actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
    rows.append({"path": relative, "expected": expected, "actual": actual, "match": expected == actual})

print(json.dumps({
    "audit": "G216",
    "status": "PASS" if rows and all(row["match"] for row in rows) else "FAIL",
    "source_count": len(rows),
    "all_source_hashes_match": bool(rows) and all(row["match"] for row in rows),
    "rows": rows,
}, sort_keys=True))

