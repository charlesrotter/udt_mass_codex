#!/usr/bin/env python3
"""Authenticate a sealed G325 review intake without repository access."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    root = Path(__file__).resolve().parent
    manifest = root / "REVIEW_MANIFEST.tsv"
    seal = root / "REVIEW_MANIFEST.sha256"
    scope = root / "REVIEW_SCOPE.json"
    assert digest(manifest) == seal.read_text().strip(), "detached manifest seal mismatch"
    rows = list(csv.DictReader(manifest.open(newline=""), delimiter="\t"))
    for row in rows:
        path = root / row["relative_path"]
        assert path.is_file(), row["relative_path"]
        assert path.stat().st_size == int(row["bytes"]), row["relative_path"]
        assert digest(path) == row["sha256"], row["relative_path"]
    metadata = json.loads(scope.read_text())
    assert len(rows) == metadata["manifest_payload_count"]
    assert metadata["evidence_read_only"] is True
    assert metadata["research_continuation_allowed"] is False
    print(json.dumps({
        "status": "PASS",
        "manifest_payload_count": len(rows),
        "total_file_count": len(rows) + 2,
        "manifest_sha256": digest(manifest),
        "scope_sha256": digest(scope),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
