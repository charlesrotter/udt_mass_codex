#!/usr/bin/env python3
"""Verify package identity and all result gates."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXCLUDE = {"PACKAGE_MANIFEST.sha256", "PACKAGE_VERIFICATION.json"}


def main() -> int:
    manifest: dict[str, str] = {}
    for line in (HERE / "PACKAGE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        expected, name = line.split(None, 1)
        name = name.strip()
        path = HERE / name
        assert name not in manifest and path.is_file()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected
        manifest[name] = expected
    actual = {path.name for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDE}
    assert set(manifest) == actual
    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    verification = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    gates = json.loads((HERE / "REPOSITORY_GATES.json").read_text(encoding="utf-8"))
    assert derivation["status"] == independent["status"] == verification["status"] == gates["status"] == "PASS"
    assert derivation["passing_complete_intersections"] == 0
    assert verification["mutation_catches"] == 16
    result = {
        "schema": "udt.bootstrap_projector_admissibility_interface.package.v1",
        "status": "PASS",
        "manifest_files": len(manifest),
        "manifest_sha256": hashlib.sha256((HERE / "PACKAGE_MANIFEST.sha256").read_bytes()).hexdigest(),
        "scientific_grade": "VERIFIED_WITH_CAVEATS",
        "maximum_conclusion": derivation["maximum_conclusion"],
    }
    (HERE / "PACKAGE_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
