#!/usr/bin/env python3
"""Fast banked-artifact and frozen-source verification for G181."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
LANDING = (
    "COMPLETED_PAIR_ENDPOINT_CLASSIFICATION__"
    "REMOVABLE_STALLS_SEPARATED_FROM_INTRINSIC_BOUNDARIES"
)


def main() -> None:
    rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
    hash_failures = []
    for row in rows:
        actual = hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest()
        if actual != row["sha256"]:
            hash_failures.append(row["path"])

    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
    summary = json.loads((HERE / "VERIFICATION_RESULT.json").read_text())
    required = {
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
        "verify_sealed_intake.py",
        "verify_package.py",
    }
    missing = sorted(name for name in required if not (HERE / name).is_file())
    checks = {
        "seven_sources": len(rows) == 7 and not hash_failures,
        "derivation_pass": derivation.get("status") == "PASS",
        "independent_pass": independent.get("status") == "PASS",
        "twenty_thousand_trials": independent.get("exact_trials") == 20_000,
        "assertion_floor": independent.get("exact_assertions", 0) >= 175_000,
        "nine_cross_classes": independent.get("required_cross_classes") == 9,
        "thirty_three_catches": catches.get("status") == "PASS"
        and catches.get("catch_count") == 33,
        "landing_matches": derivation.get("landing") == LANDING
        and summary.get("landing") == LANDING,
        "preregistration_commit": summary.get("preregistration_commit") == "a4dacea9",
        "files_present": not missing,
    }
    failed = [name for name, passed in checks.items() if not passed]
    result = {
        "audit": "G181",
        "status": "PASS" if not failed else "FAIL",
        "landing": LANDING,
        "checks": checks,
        "source_hash_failures": hash_failures,
        "missing_files": missing,
    }
    if failed:
        raise SystemExit(json.dumps(result, sort_keys=True))
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
