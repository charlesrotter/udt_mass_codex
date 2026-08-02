#!/usr/bin/env python3
"""Verify package identity and every load-bearing gate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
EXCLUDE = {"PACKAGE_MANIFEST.sha256", "PACKAGE_VERIFICATION.json"}


def main() -> int:
    manifest = {}
    for line in (PACKAGE / "PACKAGE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        expected, name = line.split(None, 1)
        name = name.strip()
        path = PACKAGE / name
        assert name not in manifest and path.is_file()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected
        manifest[name] = expected
    actual = {
        path.name for path in PACKAGE.iterdir() if path.is_file() and path.name not in EXCLUDE
    }
    assert set(manifest) == actual

    derivation = json.loads((PACKAGE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((PACKAGE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    verification = json.loads((PACKAGE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    gates = json.loads((PACKAGE / "REPOSITORY_GATES.json").read_text(encoding="utf-8"))
    assert derivation["outcome"] == "MINIMAL_CROSS_SECTOR_RESPONSE_EXISTS__LAW_SELECTION_OPEN"
    assert derivation["checks_passed"] == derivation["checks_total"] == 43
    assert independent["checks_passed"] == independent["checks_total"] == 29
    assert independent["semantic_catches_passed"] == independent["semantic_catches_total"] == 15
    assert verification["status"] == gates["status"] == "PASS"
    assert verification["candidate_outcomes"] == 16
    assert verification["source_identities"] == 15
    assert verification["law_selected"] is False
    assert verification["density_scan_authorized"] is False
    assert gates["frozen_manifests"] == 6 and gates["frozen_package_paths"] == 133
    assert gates["current_paths"] == 1114 and gates["frontier_targets"] == 101
    assert gates["tests"] == "70 passed, 1 xfailed"

    result = {
        "schema": "udt.fc07.broader_coframe_hodge_response.package.v1",
        "status": "PASS",
        "manifest_files": len(manifest),
        "manifest_sha256": hashlib.sha256(
            (PACKAGE / "PACKAGE_MANIFEST.sha256").read_bytes()
        ).hexdigest(),
        "scientific_grade": "VERIFIED_WITH_CAVEATS",
        "outcome": derivation["outcome"],
        "law_selected": False,
        "density_scan_authorized": False,
    }
    (PACKAGE / "PACKAGE_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
