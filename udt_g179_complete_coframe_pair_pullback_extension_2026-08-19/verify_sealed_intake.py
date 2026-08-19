#!/usr/bin/env python3
"""Dependency-free, read-only validation of a sealed G179 intake."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import stat


ROOT = Path(__file__).resolve().parents[1]
scope_path = ROOT / "REVIEW_SCOPE.json"
scope = json.loads(scope_path.read_text())
expected = {row["path"]: row for row in scope["tree"]}
actual_paths = {
    str(path.relative_to(ROOT))
    for path in ROOT.rglob("*")
    if path.is_file() and path != scope_path
}

if actual_paths != set(expected):
    missing = sorted(set(expected) - actual_paths)
    extra = sorted(actual_paths - set(expected))
    raise SystemExit(f"tree mismatch: missing={missing}, extra={extra}")

for relative, row in expected.items():
    path = ROOT / relative
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != row["sha256"] or path.stat().st_size != row["bytes"]:
        raise SystemExit(f"content mismatch: {relative}")
    if path.stat().st_mode & (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH):
        raise SystemExit(f"writable intake file: {relative}")

if scope["files_before_scope"] != len(expected):
    raise SystemExit("scope count mismatch")

print(
    json.dumps(
        {
            "status": "PASS__SEALED_TREE_COMPLETE_AND_READ_ONLY",
            "files_before_scope": len(expected),
            "scope_sha256": hashlib.sha256(scope_path.read_bytes()).hexdigest(),
        },
        sort_keys=True,
    )
)
