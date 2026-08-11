#!/usr/bin/env python3
"""Build the exact G72 sealed-review manifest."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PACKAGE_FILES = (
    "PREREGISTRATION.md",
    "SOURCE_MANIFEST_CORRECTION_PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "derive_screen_response.py",
    "verify_screen_response_independent.py",
    "run_catch_proofs.py",
    "verify_package.py",
    "verify_repository_gates.py",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION_RESULT.json",
    "G68_RESPONSE_ATLAS.tsv",
    "TYPE_LEDGER.tsv",
    "RESPONSE_OWNERSHIP_LEDGER.tsv",
    "PREMISE_LEDGER.tsv",
    "FALSIFICATION_CONTRACT.tsv",
    "CATCH_PROOF_RESULTS.json",
    "PACKAGE_VERIFICATION_RESULT.json",
    "REPOSITORY_GATES.json",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "RUN_RECORD.md",
    "EXTERNAL_REVIEW_DISPATCH.md",
    "build_review_manifest.py",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    source_rows = []
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        source_rows = list(csv.DictReader(stream, delimiter="\t"))
    paths = [str(HERE.relative_to(ROOT) / name) for name in PACKAGE_FILES]
    paths.extend(row["path"] for row in source_rows)
    assert len(paths) == len(set(paths))
    assert all((ROOT / path).is_file() for path in paths)
    with (HERE / "REVIEW_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "sha256", "role"))
        for path in paths:
            role = "G72_PACKAGE" if path.startswith(HERE.name + "/") else "FROZEN_SOURCE"
            writer.writerow((path, digest(ROOT / path), role))
    print(f"PASS: {len(paths)} review payloads")


if __name__ == "__main__":
    main()
