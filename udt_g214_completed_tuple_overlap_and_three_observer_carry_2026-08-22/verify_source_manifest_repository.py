#!/usr/bin/env python3
"""Verify the frozen G214 repository-source manifest."""

import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
rows = []
for line in (PACKAGE / "SOURCE_MANIFEST.tsv").read_text().splitlines()[1:]:
    expected, relative = line.split("\t", 1)
    actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
    rows.append({"path": relative, "expected": expected, "actual": actual, "match": actual == expected})

print(json.dumps({
    "audit": "G214",
    "status": "PASS" if all(row["match"] for row in rows) else "FAIL",
    "source_count": len(rows),
    "all_source_hashes_match": all(row["match"] for row in rows),
    "rows": rows,
}, sort_keys=True))
