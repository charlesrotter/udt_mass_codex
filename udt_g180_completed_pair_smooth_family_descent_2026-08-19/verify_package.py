#!/usr/bin/env python3
"""Fast banked-artifact and source verification for G180."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def main() -> None:
    rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
    failures = []
    for row in rows:
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
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "VERIFICATION_RESULT.json",
        "derive_completed_pair_family.py",
        "verify_family_descent_independent.py",
        "run_catch_proofs.py",
        "build_review_intake.py",
        "verify_sealed_intake.py",
        "verify_package.py",
        "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md",
        "EXTERNAL_ADVERSARIAL_REVIEW_TRANSCRIPT.txt.gz",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "TRANSMISSION_RECORD.md",
        "REVIEW_EXECUTION_BOUNDARY.md",
        "REVIEW_REPAIR_PREREGISTRATION.md",
        "FOLLOWUP_REVIEW_REQUEST.md",
        "EXTERNAL_FOLLOWUP_REVIEW_RAW.md",
        "EXTERNAL_FOLLOWUP_REVIEW_TRANSCRIPT.txt.gz",
        "FOLLOWUP_TRANSMISSION_RECORD.md",
    }
    missing = sorted(name for name in required if not (HERE / name).is_file())
    landing = "COMPLETED_PAIR_SMOOTH_FAMILY_DESCENT__ORCHESTRA_ENTERS_THE_PHYSICAL_TAPE_MAP"
    checks = {
        "nine_sources": len(rows) == 9 and not failures,
        "derivation_pass": derivation.get("status") == "PASS",
        "independent_pass": independent.get("status") == "PASS",
        "twenty_thousand_trials": independent.get("exact_fraction_regular_trials") == 20_000,
        "assertion_floor": independent.get("exact_assertions", 0) >= 300_000,
        "twenty_eight_catches": catches.get("status") == "PASS"
        and catches.get("catch_count") == 28,
        "landing_matches": derivation.get("landing") == landing
        and summary.get("landing") == landing,
        "external_review_accepted": "G180_ACCEPTED_WITH_STATED_BOUNDS"
        in (HERE / "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md").read_text(),
        "repair_scope_preregistered": "make no change to the theorem"
        in (HERE / "REVIEW_REPAIR_PREREGISTRATION.md").read_text(),
        "repair_followup_accepted": "G180_REPAIR_ACCEPTED"
        in (HERE / "EXTERNAL_FOLLOWUP_REVIEW_RAW.md").read_text(),
        "files_present": not missing,
    }
    failed = [name for name, passed in checks.items() if not passed]
    result = {
        "audit": "G180",
        "status": "PASS" if not failed else "FAIL",
        "landing": landing,
        "checks": checks,
        "source_hash_failures": failures,
        "missing_files": missing,
    }
    if failed:
        raise SystemExit(json.dumps(result, sort_keys=True))
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
