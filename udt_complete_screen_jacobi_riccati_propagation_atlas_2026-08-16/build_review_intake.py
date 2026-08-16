#!/usr/bin/env python3
"""Build a sealed G108 review intake containing only declared files."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    package_names = [
        "ADVERSARIAL_REVIEW_REQUEST.md",
        "AUDIT_REPORT.md",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "EXTERNAL_REVIEW_RAW.md",
        "EXTERNAL_FOLLOWUP_REVIEW_RAW.md",
        "FOLLOWUP_REVIEW_REQUEST.md",
        "REVIEW_DISPATCH.md",
        "DERIVATION_RESULT.json",
        "EVIDENCE_GATES.md",
        "EXACT_DERIVATION.md",
        "FALSIFICATION_CONTRACT.tsv",
        "G68_ENDPOINT_RATE_ATLAS.tsv",
        "INDEPENDENT_VERIFICATION.json",
        "LAY_REPORT.md",
        "PACKAGE_VERIFICATION_RESULT.json",
        "PREMISE_LEDGER.tsv",
        "PREREGISTRATION.md",
        "SOURCE_MANIFEST.tsv",
        "STATUS.md",
        "STATUS_LEDGER.tsv",
        "build_review_intake.py",
        "derive_screen_propagation.py",
        "verify_package.py",
        "verify_screen_propagation_independent.py",
    ]
    source_paths = []
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        source_paths = [row["path"] for row in csv.DictReader(handle, delimiter="\t")]

    intake = Path(tempfile.mkdtemp(prefix="udt_g108_screen_review_"))
    package_target = intake / HERE.name
    package_target.mkdir()
    copied = []
    for name in package_names:
        source = HERE / name
        if not source.is_file():
            raise FileNotFoundError(source)
        target = package_target / name
        shutil.copy2(source, target)
        copied.append(target.relative_to(intake).as_posix())

    for relative in source_paths:
        source = ROOT / relative
        target = intake / "declared_sources" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(target.relative_to(intake).as_posix())

    scope = {
        "schema": "UDT_G108_SEALED_REVIEW_SCOPE_V1",
        "purpose": "read-only adversarial review of the bounded G108 screen propagation claim",
        "file_count_excluding_scope": len(copied),
        "files": sorted(copied),
        "restrictions": [
            "inspect only this sealed intake",
            "do not edit files or continue the research",
            "do not use internet or observational outcomes",
            "do not inspect repository or protected packages",
        ],
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "intake": str(intake),
        "file_count_including_scope": len(copied) + 1,
        "review_scope_sha256": sha256(scope_path),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
