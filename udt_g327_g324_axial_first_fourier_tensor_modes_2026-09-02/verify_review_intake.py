#!/usr/bin/env python3
"""Dependency-free manifest and read-only-boundary verifier for a sealed G327 intake."""

from __future__ import annotations

import csv
import hashlib
import json
import stat
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    intake = Path(__file__).resolve().parent
    manifest = intake / "REVIEW_MANIFEST.tsv"
    seal = intake / "REVIEW_MANIFEST.sha256"
    assert manifest.is_file(), "manifest_missing"
    assert seal.is_file(), "detached_seal_missing"
    assert seal.read_text(encoding="utf-8").strip() == digest(manifest), "seal_mismatch"

    with manifest.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert rows, "empty_manifest"
    registered = set()
    for row in rows:
        relative = row["relative_path"]
        path = intake / relative
        assert path.is_file(), f"missing:{relative}"
        assert path.stat().st_size == int(row["bytes"]), f"size:{relative}"
        assert digest(path) == row["sha256"], f"sha256:{relative}"
        assert not path.stat().st_mode & (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH), (
            f"writable:{relative}"
        )
        registered.add(relative)

    actual = {
        path.relative_to(intake).as_posix()
        for path in intake.rglob("*")
        if path.is_file() and path.name not in {"REVIEW_MANIFEST.tsv", "REVIEW_MANIFEST.sha256"}
    }
    assert actual == registered, "unregistered_or_missing_payload"
    scope = json.loads((intake / "REVIEW_SCOPE.json").read_text(encoding="utf-8"))
    assert scope["evidence_read_only"] is True
    assert scope["research_continuation_allowed"] is False
    assert scope["ephemeral_copy_checks_allowed"] is True
    print(json.dumps({
        "status": "PASS",
        "payload_count": len(rows),
        "manifest_sha256": digest(manifest),
        "read_only_payloads": True,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

