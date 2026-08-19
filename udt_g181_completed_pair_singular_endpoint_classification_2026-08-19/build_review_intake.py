#!/usr/bin/env python3
"""Build a sealed read-only review intake for G181."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PACKAGE_NAME = HERE.name
PACKAGE_FILES = (
    "PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "EVIDENCE_GATES.md",
    "STATUS_LEDGER.tsv",
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "REVIEW_EXECUTION_BOUNDARY.md",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "VERIFICATION_RESULT.json",
    "WITNESS_ATLAS.tsv",
    "derive_singular_endpoint_classification.py",
    "verify_singular_endpoint_independent.py",
    "run_catch_proofs.py",
    "build_review_intake.py",
    "verify_package.py",
    "verify_sealed_intake.py",
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g181_endpoint_review_", dir="/tmp"))
    payload: list[dict[str, object]] = []

    for name in PACKAGE_FILES:
        source = HERE / name
        relative = Path(PACKAGE_NAME) / name
        target = intake / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
    for row in rows:
        relative = Path(row["path"])
        target = intake / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)

    for path in sorted(path for path in intake.rglob("*") if path.is_file()):
        payload.append(
            {
                "path": str(path.relative_to(intake)),
                "sha256": sha(path),
                "bytes": path.stat().st_size,
            }
        )

    scope = {
        "audit": "G181",
        "purpose": "fresh read-only adversarial review of bounded endpoint classification",
        "payload_file_count": len(payload),
        "total_file_count": len(payload) + 1,
        "restrictions": [
            "intake only",
            "read only",
            "no repository or protected packages",
            "no internet",
            "no edits or research continuation",
        ],
        "files": payload,
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "intake": str(intake),
                "payload_files": len(payload),
                "total_files": len(payload) + 1,
                "scope_sha256": sha(scope_path),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
