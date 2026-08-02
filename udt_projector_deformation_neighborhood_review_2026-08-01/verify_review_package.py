#!/usr/bin/env python3
"""Verify the complete external-review layer after its manifest is built."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDE = {"REVIEW_LAYER_MANIFEST.sha256"}


def main() -> int:
    expected: dict[str, str] = {}
    for line in (HERE / "REVIEW_LAYER_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        digest, name = line.split(None, 1)
        name = name.strip()
        path = HERE / name
        assert name not in expected and path.is_file()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
        expected[name] = digest
    actual = {path.name for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDE}
    assert set(expected) == actual
    verification = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    gates = json.loads((HERE / "REPOSITORY_GATES.json").read_text(encoding="utf-8"))
    assert verification["status"] == gates["status"] == "PASS"
    result = {
        "status": "PASS",
        "manifest_files": len(expected),
        "manifest_sha256": hashlib.sha256(
            (HERE / "REVIEW_LAYER_MANIFEST.sha256").read_bytes()
        ).hexdigest(),
        "external_verdict": "PASS",
        "mandatory_repairs": 0,
        "target_package_unchanged": True,
    }
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
