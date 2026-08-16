#!/usr/bin/env python3
"""Build a sealed G109 review intake containing only declared files."""

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
        "CONTROL_ATLAS.tsv",
        "DERIVATION_RESULT.json",
        "EVIDENCE_GATES.md",
        "EXACT_DERIVATION.md",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "EXTERNAL_REVIEW_FOLLOWUP_REQUEST.md",
        "EXTERNAL_REVIEW_FOLLOWUP_RAW.md",
        "EXTERNAL_REVIEW_RAW.md",
        "FALSIFICATION_CONTRACT.tsv",
        "INDEPENDENT_VERIFICATION.json",
        "LAY_REPORT.md",
        "PACKAGE_VERIFICATION_RESULT.json",
        "PREMISE_LEDGER.tsv",
        "PREREGISTRATION.md",
        "REVIEW_DISPATCH.md",
        "SOURCE_MANIFEST.tsv",
        "STATUS.md",
        "STATUS_LEDGER.tsv",
        "build_review_intake.py",
        "derive_same_query_join.py",
        "verify_package.py",
        "verify_same_query_join_independent.py",
    ]
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        source_paths = [row["path"] for row in csv.DictReader(handle, delimiter="\t")]

    intake = Path(tempfile.mkdtemp(prefix="udt_g109_same_query_review_"))
    target_package = intake / HERE.name
    target_package.mkdir()
    copied = []
    for name in package_names:
        source = HERE / name
        if not source.is_file():
            raise FileNotFoundError(source)
        target = target_package / name
        shutil.copy2(source, target)
        copied.append(target.relative_to(intake).as_posix())
    for relative in source_paths:
        source = ROOT / relative
        target = intake / "declared_sources" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(target.relative_to(intake).as_posix())

    scope = {
        "schema": "UDT_G109_SEALED_REVIEW_SCOPE_V1",
        "purpose": "read-only review of the bounded same-query terminal-depth propagation join",
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
    print(
        json.dumps(
            {
                "intake": str(intake),
                "file_count_including_scope": len(copied) + 1,
                "review_scope_sha256": sha256(scope_path),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
