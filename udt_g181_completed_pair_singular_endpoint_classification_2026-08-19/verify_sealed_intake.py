#!/usr/bin/env python3
"""Verify a sealed G181 intake against its root REVIEW_SCOPE.json."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    scope_path = ROOT / "REVIEW_SCOPE.json"
    scope = json.loads(scope_path.read_text())
    failures = []
    for item in scope["files"]:
        path = ROOT / item["path"]
        if not path.is_file():
            failures.append(f"missing:{item['path']}")
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != item["sha256"]:
            failures.append(f"hash:{item['path']}")
    actual_files = sorted(
        str(path.relative_to(ROOT))
        for path in ROOT.rglob("*")
        if path.is_file() and path != scope_path
    )
    expected_files = sorted(item["path"] for item in scope["files"])
    if actual_files != expected_files:
        failures.append("file_set")
    if failures:
        raise SystemExit(json.dumps({"status": "FAIL", "failures": failures}, sort_keys=True))
    print(
        json.dumps(
            {
                "status": "PASS",
                "payload_files": len(expected_files),
                "total_files_with_scope": len(expected_files) + 1,
                "scope_sha256": hashlib.sha256(scope_path.read_bytes()).hexdigest(),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
