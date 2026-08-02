#!/usr/bin/env python3
"""Verify final package identity and all result gates."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDE = {"PACKAGE_MANIFEST.sha256", "PACKAGE_VERIFICATION.json"}


def main() -> int:
    manifest: dict[str, str] = {}
    for line in (HERE / "PACKAGE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        digest, name = line.split(None, 1)
        name = name.strip()
        assert name not in manifest and (HERE / name).is_file()
        assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest
        manifest[name] = digest
    actual = {
        path.name for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDE
    }
    assert set(manifest) == actual
    assert json.loads((HERE / "DERIVATION_RESULT.json").read_text())["status"] == "PASS"
    assert json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())["status"] == "PASS"
    verification = json.loads((HERE / "VERIFICATION_RESULT.json").read_text())
    assert verification["status"] == "PASS" and verification["mutation_catches"] == 24
    gates = json.loads((HERE / "REPOSITORY_GATES.json").read_text())
    assert gates["status"] == "PASS" and gates["tests"] == "70 passed, 1 xfailed"
    result = {
        "schema": "udt.projector_deformation_neighborhood.package.v1",
        "status": "PASS",
        "manifest_files": len(manifest),
        "manifest_sha256": hashlib.sha256(
            (HERE / "PACKAGE_MANIFEST.sha256").read_bytes()
        ).hexdigest(),
        "scientific_grade": "VERIFIED_WITH_CAVEATS_PENDING_FRESH_EXTERNAL_SEMANTIC_REVIEW",
    }
    (HERE / "PACKAGE_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

