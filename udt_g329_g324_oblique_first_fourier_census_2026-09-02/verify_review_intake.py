#!/usr/bin/env python3
"""Dependency-free authentication verifier for a sealed G329 review intake."""

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
    scope_path = root / "REVIEW_SCOPE.json"
    assert manifest.is_file() and seal.is_file() and scope_path.is_file()
    assert digest(manifest) == seal.read_text(encoding="utf-8").strip(), "seal mismatch"

    with manifest.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    registered = set()
    for row in rows:
        relative = row["relative_path"]
        path = root / relative
        assert path.is_file(), f"missing payload: {relative}"
        assert path.stat().st_size == int(row["bytes"]), f"size mismatch: {relative}"
        assert digest(path) == row["sha256"], f"hash mismatch: {relative}"
        registered.add(relative)

    actual = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and ".review_runtime" not in path.parts
    }
    expected = registered | {"REVIEW_MANIFEST.tsv", "REVIEW_MANIFEST.sha256"}
    assert actual == expected, "unregistered or missing intake files"
    scope = json.loads(scope_path.read_text(encoding="utf-8"))
    assert scope["manifest_payload_count"] == len(rows)
    assert not scope["evidence_write_allowed"]
    assert not scope["research_continuation_allowed"]
    assert scope["ephemeral_copy_checks_allowed"]

    required = {
        "EXACT_DERIVATION.md", "DERIVATION_RESULT.json", "RAW_RESIDUALS.json",
        "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json",
        "PACKAGE_VERIFICATION_RESULT.json", "verify_package.py",
        "VENDORED_SYMPY_RUNTIME.zip", "sealed_runtime.py",
        "PREREGISTRATION_COMMIT_OBJECT.txt", "ADVERSARIAL_REVIEW_REQUEST.md",
    }
    assert required <= registered, "required review evidence missing"
    print(json.dumps({
        "schema": "udt-g329-review-intake-verification-v1",
        "status": "PASS",
        "payload_count": len(rows),
        "scope_sha256": digest(scope_path),
        "manifest_sha256": digest(manifest),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
