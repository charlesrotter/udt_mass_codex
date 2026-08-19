#!/usr/bin/env python3
"""Fast banked-artifact and source verification for G179."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def main() -> None:
    source_rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
    failures = []
    for row in source_rows:
        actual = hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest()
        if actual != row["sha256"]:
            failures.append(row["path"])

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
        "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md",
        "EXTERNAL_ADVERSARIAL_REVIEW_TRANSCRIPT.txt.gz",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "REVIEW_EXECUTION_BOUNDARY.md",
        "TRANSMISSION_RECORD.md",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "VERIFICATION_RESULT.json",
        "derive_complete_coframe_extension.py",
        "verify_complete_coframe_independent.py",
        "run_catch_proofs.py",
        "build_review_intake.py",
        "verify_sealed_intake.py",
        "verify_package.py",
    }
    missing = sorted(name for name in required if not (HERE / name).is_file())
    expected_landing = (
        "GENERAL_COMPLETE_COFRAME_PULLBACK_EXTENDS_COMPLETED_PAIR_KERNEL_"
        "WITHOUT_EXTRA_SCALAR"
    )
    checks = {
        "ten_sources": len(source_rows) == 10 and not failures,
        "derivation_pass": derivation.get("status") == "PASS",
        "independent_pass": independent.get("status") == "PASS",
        "twenty_thousand_trials": independent.get("exact_fraction_regular_trials") == 20_000,
        "thirty_catches": catches.get("status") == "PASS" and catches.get("catch_count") == 30,
        "landing_matches": derivation.get("landing") == expected_landing
        and summary.get("landing") == expected_landing,
        "external_review_accepted": summary.get("external_review")
        == "G179_ACCEPTED_WITH_STATED_BOUNDS",
        "external_review_hash": hashlib.sha256(
            (HERE / "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md").read_bytes()
        ).hexdigest()
        == "af2009155fde266e62038bac7bddbc084dc87e7ab1a1d4d7d73b610d56fc6744",
        "external_transcript_hash": hashlib.sha256(
            (HERE / "EXTERNAL_ADVERSARIAL_REVIEW_TRANSCRIPT.txt.gz").read_bytes()
        ).hexdigest()
        == "6ebb508f634198344628a5ea75859a1970f1991455ce8a6912ad93b8e8fed0c5",
        "files_present": not missing,
    }
    failed = [name for name, passed in checks.items() if not passed]
    result = {
        "audit": "G179",
        "status": "PASS" if not failed else "FAIL",
        "landing": expected_landing,
        "checks": checks,
        "source_hash_failures": failures,
        "missing_files": missing,
    }
    if failed:
        raise SystemExit(json.dumps(result, sort_keys=True))
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
