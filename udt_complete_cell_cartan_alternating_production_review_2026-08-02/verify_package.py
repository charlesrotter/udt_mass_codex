#!/usr/bin/env python3
"""Fail closed on review-package hashes and decisive corrected fields."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


entries = []
for line in (HERE / "PACKAGE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
    expected, name = line.split(None, 1)
    target = HERE / name.strip()
    assert target.is_file() and digest(target) == expected
    entries.append(name.strip())
assert len(entries) == len(set(entries))

result = json.loads((HERE / "CORRECTION_RESULT.json").read_text(encoding="utf-8"))
gates = json.loads((HERE / "REPOSITORY_GATES.json").read_text(encoding="utf-8"))
assert result["status"] == "PASS_AFTER_REQUIRED_CORRECTIONS"
assert result["curvature"]["forward"]["mixed_row_count"] == 12
assert result["curvature"]["reverse"]["mixed_row_count"] == 12
assert len(result["curvature"]["forward_mixed_row_identities"]) == 12
assert len(result["curvature"]["reverse_mixed_row_identities"]) == 12
assert result["curvature"]["mixed_identity_set_same"] is False
assert result["parent_package_modified"] is False
assert result["catch_proofs"] == 8
assert gates["status"] == "PASS"
verification = {
    "status": "PASS_AFTER_REQUIRED_CORRECTIONS",
    "entries": len(entries),
    "package_manifest_sha256": digest(HERE / "PACKAGE_MANIFEST.sha256"),
    "source_manifest_sha256": digest(HERE / "SOURCE_MANIFEST.tsv"),
    "parent_package_manifest_sha256": result["identity"]["parent_package_manifest_sha256"],
}
(HERE / "PACKAGE_VERIFICATION.json").write_text(
    json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps(verification, sort_keys=True))
