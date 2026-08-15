#!/usr/bin/env python3
"""Write the immutable R5 final-evidence manifest after all closure records exist."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ARTIFACTS = (
    "R5_PREREGISTRATION.md",
    "R5_PREMISE_LEDGER.tsv",
    "R5_FALSIFICATION_CONTRACT.tsv",
    "run_r5_common_subspace_atlas.py",
    "verify_r5_preregistration.py",
    "R5_FIRST_ASSEMBLY_METHOD_FAILURE.json",
    "R5_COVARIANCE_SUBSPACE_CORRECTION_PREREGISTRATION.md",
    "verify_r5_subspace_correction_preregistration.py",
    "R5_VIEW_SPECTRA.tsv",
    "R5_RANKED_SUBSPACE_OVERLAPS.tsv",
    "R5_COVARIANCE_SUBSPACE_ATLAS.tsv",
    "R5_COVARIANCE_SUBSPACE_SUMMARY.tsv",
    "R5_RESULT.json",
    "R5_OUTPUT_MANIFEST.tsv",
    "R5_VERIFICATION_PREREGISTRATION.md",
    "verify_r5.py",
    "R5_VERIFIER_FIRST_FAILURE.json",
    "R5_VERIFIER_CHORD_CORRECTION_PREREGISTRATION.md",
    "R5_VERIFIER_SECOND_FAILURE.json",
    "R5_VERIFIER_FULLSPACE_TOLERANCE_CORRECTION_PREREGISTRATION.md",
    "R5_VERIFICATION_RESULT.json",
    "catch_proof_r5_verifier.py",
    "R5_VERIFIER_CATCH_PROOF_RESULT.json",
    "R5_COVARIANCE_RANGE_OWNERSHIP_REPAIR_PREREGISTRATION.md",
    "R5_ADVERSARIAL_REVIEW_REQUEST.md",
    "R5_EXTERNAL_ADVERSARIAL_REVIEW.md",
    "R5_EXTERNAL_REVIEW_REPAIR_RESULT.json",
    "R5_FOLLOWUP_ADVERSARIAL_REVIEW_REQUEST.md",
    "R5_EXTERNAL_FOLLOWUP_REVIEW.md",
    "R5_OUTCOME_REPORT.md",
    "R5_FINAL_STATUS.json",
    "STATUS_LEDGER.tsv",
    "finalize_r5_package.py",
    "verify_r5_final_package.py",
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main():
    output = HERE / "R5_FINAL_EVIDENCE_MANIFEST.tsv"
    if output.exists():
        raise FileExistsError(output)
    records = []
    for name in ARTIFACTS:
        path = HERE / name
        if not path.is_file():
            raise FileNotFoundError(path)
        records.append({"artifact": name, "bytes": path.stat().st_size, "sha256": digest(path)})
    temporary = output.with_suffix(".tsv.tmp")
    with temporary.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["artifact", "bytes", "sha256"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(records)
    temporary.replace(output)
    print(f"PASS: wrote {len(records)} R5 final evidence rows")


if __name__ == "__main__":
    main()
