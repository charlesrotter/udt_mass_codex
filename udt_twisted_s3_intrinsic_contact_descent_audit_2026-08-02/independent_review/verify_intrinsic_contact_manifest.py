#!/usr/bin/env python3
"""Independent frozen-source and target-artifact hash verifier."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path("/home/udt-admin/udt_mass_codex")
PKG = ROOT / "udt_twisted_s3_intrinsic_contact_descent_audit_2026-08-02"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


with (PKG / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle, delimiter="\t"))

failures = []
for row in rows:
    data = subprocess.run(
        ["git", "cat-file", "blob", row["git_blob"]],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    if len(data) != int(row["bytes"]) or sha(data) != row["sha256"]:
        failures.append(row["path"])

manifest_hash = sha((PKG / "SOURCE_MANIFEST.tsv").read_bytes())
expected_manifest_hash = (PKG / "SOURCE_MANIFEST.sha256").read_text(encoding="utf-8").strip()
artifact_hashes = {
    path.name: sha(path.read_bytes())
    for path in sorted(PKG.iterdir())
    if path.is_file()
}
status = subprocess.run(
    ["git", "status", "--short", "--branch"], cwd=ROOT, check=True, capture_output=True, text=True
).stdout.splitlines()
print(json.dumps({
    "source_rows": len(rows),
    "unique_source_paths": len({row["path"] for row in rows}),
    "blob_failures": failures,
    "manifest_sha256": manifest_hash,
    "manifest_expected_sha256": expected_manifest_hash,
    "manifest_hash_matches": manifest_hash == expected_manifest_hash,
    "target_artifact_sha256": artifact_hashes,
    "git_status": status,
}, indent=2, sort_keys=True))
