#!/usr/bin/env python3
"""Fast banked-artifact and frozen-source verification for G181."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import subprocess
import sys
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
        "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md",
        "EXTERNAL_ADVERSARIAL_REVIEW_TRANSCRIPT.txt.gz",
        "EXTERNAL_REVIEW_ADJUDICATION.md",
        "TRANSMISSION_RECORD.md",
        "REVIEW_REPAIR_PREREGISTRATION.md",
        "FOLLOWUP_REVIEW_REQUEST.md",
        "FOLLOWUP_RECOVERY_REVIEW_REQUEST.md",
        "EXTERNAL_REPAIR_FOLLOWUP_ABORTED_TRANSCRIPT.txt.gz",
        "EXTERNAL_REPAIR_FOLLOWUP_INCOMPLETE_RAW.md",
        "EXTERNAL_REPAIR_FOLLOWUP_INCOMPLETE_TRANSCRIPT.txt.gz",
        "EXTERNAL_REPAIR_FOLLOWUP_RAW.md",
        "EXTERNAL_REPAIR_FOLLOWUP_TRANSCRIPT.txt.gz",
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

    replay_environment = os.environ.copy()
    replay_environment["UDT_READ_ONLY_REPLAY"] = "1"
    replay_environment["PYTHONDONTWRITEBYTECODE"] = "1"
    replay_scripts = (
        "derive_singular_endpoint_classification.py",
        "verify_singular_endpoint_independent.py",
        "run_catch_proofs.py",
    )
    replay_results: dict[str, dict[str, object]] = {}
    for script in replay_scripts:
        completed = subprocess.run(
            [sys.executable, "-I", "-S", str(HERE / script)],
            cwd=HERE,
            env=replay_environment,
            check=False,
            capture_output=True,
            text=True,
        )
        replay_results[script] = {
            "returncode": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        }

    checks = {
        "seven_sources": len(rows) == 7 and not hash_failures,
        "derivation_pass": derivation.get("status") == "PASS",
        "independent_pass": independent.get("status") == "PASS",
        "twenty_thousand_trials": independent.get("exact_trials") == 20_000,
        "rational_exponent_population": independent.get("rational_exponent_trials") == 20_000
        and independent.get("noninteger_exponent_trials", 0) > 0,
        "assertion_floor": independent.get("exact_assertions", 0) >= 140_000,
        "nine_cross_classes": independent.get("required_cross_classes") == 9,
        "twenty_eight_executable_catches": catches.get("status") == "PASS"
        and catches.get("catch_count") == 28,
        "six_separate_semantic_guards": catches.get("semantic_guard_count") == 6,
        "isolated_read_only_replays": all(
            result["returncode"] == 0 for result in replay_results.values()
        ),
        "landing_matches": derivation.get("landing") == LANDING
        and summary.get("landing") == LANDING,
        "preregistration_commit": summary.get("preregistration_commit") == "a4dacea9",
        "external_repair_accepted": summary.get("external_followup")
        == "G181_REPAIR_ACCEPTED"
        and (HERE / "EXTERNAL_REPAIR_FOLLOWUP_RAW.md")
        .read_text()
        .startswith("G181_REPAIR_ACCEPTED"),
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
        "replays": replay_results,
    }
    if failed:
        raise SystemExit(json.dumps(result, sort_keys=True))
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
