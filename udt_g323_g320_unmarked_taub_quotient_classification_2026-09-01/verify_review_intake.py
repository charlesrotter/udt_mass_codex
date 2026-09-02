#!/usr/bin/env python3
"""Dependency-free authentication of a sealed G323 review intake."""

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def need(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    manifest_path = ROOT / "REVIEW_MANIFEST.tsv"
    seal_path = ROOT / "REVIEW_MANIFEST.sha256"
    scope_path = ROOT / "REVIEW_SCOPE.json"
    need(manifest_path.is_file(), "missing manifest")
    need(seal_path.is_file(), "missing detached seal")
    need(scope_path.is_file(), "missing scope")

    sealed_digest, sealed_name = seal_path.read_text(encoding="utf-8").strip().split()
    need(sealed_name == "REVIEW_MANIFEST.tsv", "detached-seal target")
    need(sha256(manifest_path) == sealed_digest, "detached-seal mismatch")

    with manifest_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    need(rows, "empty manifest")
    recorded = set()
    for row in rows:
        relative = Path(row["path"])
        need(not relative.is_absolute() and ".." not in relative.parts, "unsafe manifest path")
        need(relative.as_posix() not in recorded, "duplicate manifest path")
        recorded.add(relative.as_posix())
        payload = ROOT / relative
        need(payload.is_file(), f"missing payload: {relative}")
        need(payload.stat().st_size == int(row["bytes"]), f"byte mismatch: {relative}")
        need(sha256(payload) == row["sha256"], f"hash mismatch: {relative}")

    scope = json.loads(scope_path.read_text(encoding="utf-8"))
    package_count = sum(path.startswith("package/") for path in recorded)
    source_count = sum(path.startswith("sources/") for path in recorded)
    need(package_count == scope["package_payload_count"], "package count mismatch")
    need(source_count == scope["source_payload_count"], "source count mismatch")
    need(len(rows) == package_count + source_count + 1, "manifest payload count mismatch")

    actual = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
    }
    expected = recorded | {"REVIEW_MANIFEST.tsv", "REVIEW_MANIFEST.sha256"}
    need(actual == expected, f"unmanifested file set: {sorted(actual ^ expected)}")
    print(f"G323 sealed intake authentication PASS: {len(rows)} payloads; {len(actual)} files")


if __name__ == "__main__":
    main()
