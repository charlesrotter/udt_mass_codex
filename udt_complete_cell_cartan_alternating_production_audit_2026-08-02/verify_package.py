#!/usr/bin/env python3
"""Fail closed on package hashes and decisive semantic records."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    entries = []
    for line in (PACKAGE / "PACKAGE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, name = line.split(None, 1)
        target = PACKAGE / name.strip()
        assert target.is_file() and digest(target) == expected
        entries.append(name.strip())
    assert len(entries) == len(set(entries))

    result = json.loads((PACKAGE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((PACKAGE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    gates = json.loads((PACKAGE / "REPOSITORY_GATES.json").read_text(encoding="utf-8"))
    assert result["maximum_grade"] == (
        "SPLIT_RELATIVE_DIFFERENTIAL_PRODUCTION_ONLY__PRIMITIVE_AND_NATURALITY_OPEN"
    )
    assert result["cartan_contact_reconstruction"]["fixed_coefficient"] == 1
    assert result["cartan_contact_reconstruction"]["m_role"].startswith("NOT_LOAD_BEARING")
    assert independent["status"] == "PASS_VERIFIED_WITH_CAVEATS_NO_FRESH_BLIND_MODEL"
    assert independent["semantic_catch_proofs"] == 11
    assert gates["status"] == "PASS"
    package_result = {
        "status": "PASS",
        "entries": len(entries),
        "package_manifest_sha256": digest(PACKAGE / "PACKAGE_MANIFEST.sha256"),
        "source_manifest_sha256": digest(PACKAGE / "SOURCE_MANIFEST.tsv"),
        "maximum_grade": result["maximum_grade"],
    }
    (PACKAGE / "PACKAGE_VERIFICATION.json").write_text(
        json.dumps(package_result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(package_result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

