#!/usr/bin/env python3
"""Write the immutable R4 final-evidence manifest after all closure records exist."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ARTIFACTS = (
    "R4_PREREGISTRATION.md",
    "R4_PREMISE_LEDGER.tsv",
    "R4_FALSIFICATION_CONTRACT.tsv",
    "run_r4_empirical_relation_atlas.py",
    "verify_r4_preregistration.py",
    "R4_RELATION_ATLAS.tsv",
    "R4_CROSS_LAG_ATLAS.npz",
    "R4_CAP_COVARIANCE_ATLAS.tsv",
    "R4_SUMMARY.tsv",
    "R4_RESULT.json",
    "R4_OUTPUT_MANIFEST.tsv",
    "verify_r4.py",
    "catch_proof_r4_verifier.py",
    "R4_VERIFICATION_RESULT.json",
    "R4_VERIFIER_CATCH_PROOF_RESULT.json",
    "R4_VERIFIER_FIRST_FAILURE.json",
    "R4_VERIFIER_METHOD_CORRECTION_PREREGISTRATION.md",
    "R4_VERIFIER_SECOND_FAILURE.json",
    "R4_VERIFIER_RANGE_PROJECTOR_CORRECTION_PREREGISTRATION.md",
    "R4_VERIFIER_THIRD_FAILURE.json",
    "R4_VERIFIER_EIGENCONDITION_CORRECTION_PREREGISTRATION.md",
    "R4_ADVERSARIAL_REVIEW_REQUEST.md",
    "R4_EXTERNAL_ADVERSARIAL_REVIEW.md",
    "R4_OUTCOME_REPORT.md",
    "R4_FINAL_STATUS.json",
    "STATUS_LEDGER.tsv",
    "finalize_r4_package.py",
    "verify_r4_final_package.py",
)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main():
    output = HERE / "R4_FINAL_EVIDENCE_MANIFEST.tsv"
    if output.exists():
        raise FileExistsError(output)
    rows = []
    for name in ARTIFACTS:
        path = HERE / name
        if not path.is_file():
            raise FileNotFoundError(path)
        rows.append({"artifact": name, "bytes": path.stat().st_size, "sha256": digest(path)})
    temp = output.with_suffix(".tsv.tmp")
    with temp.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["artifact", "bytes", "sha256"],
                                delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    temp.replace(output)
    print(f"PASS: wrote {len(rows)} R4 final evidence rows")


if __name__ == "__main__":
    main()
