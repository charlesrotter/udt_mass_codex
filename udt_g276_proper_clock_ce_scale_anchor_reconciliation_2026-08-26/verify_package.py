#!/usr/bin/env python3
"""Verify frozen sources, artifacts, and no-write G276 replays."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
SCOPE_ROOT = ROOT.parent.resolve()
OUT = ROOT / "VERIFICATION_RESULT.json"
PREREG_COMMIT = "e5fddc76"
SEALED_REVIEW = (SCOPE_ROOT / "REVIEW_SCOPE.json").is_file()
LANDING = (
    "ONE_INDEPENDENT_SAME_SEGMENT_PROPER_CLOCK_RECORD_HAS_HOMOTHETY_WEIGHT_PLUS_ONE__"
    "CE_CARRIES_THE_ATTACHED_TIME_TO_A_UNIQUE_LENGTH_SCALE__"
    "CE_ALONE_DIMENSIONLESS_PROJECTIVE_STATE_AND_SELF_EVALUATION_ARE_SCALE_BLIND__"
    "NO_HISTORY_DISTANCE_PROTOCOL_OR_XMAX_SELECTED"
)


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def frozen_source(relative: str, expected: str) -> bytes:
    sealed = (ROOT / "sources" / relative).resolve()
    source_root = (ROOT / "sources").resolve()
    if SEALED_REVIEW:
        assert sealed.is_relative_to(source_root) and sealed.is_file(), relative
        payload = sealed.read_bytes()
        assert sha256(payload) == expected, relative
        return payload

    live = (SCOPE_ROOT / relative).resolve()
    if live.is_relative_to(SCOPE_ROOT) and live.is_file():
        payload = live.read_bytes()
        if sha256(payload) == expected:
            return payload
    completed = subprocess.run(
        ["git", "show", f"{PREREG_COMMIT}:{relative}"],
        cwd=SCOPE_ROOT,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, relative
    assert sha256(completed.stdout) == expected, relative
    return completed.stdout


def replay(script: str) -> None:
    completed = subprocess.run(
        [sys.executable, str(ROOT / script), "--no-write"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    with (ROOT / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        sources = list(csv.DictReader(stream, delimiter="\t"))
    assert len(sources) == 7
    for row in sources:
        frozen_source(row["path"], row["sha256"])

    required = (
        "ADVERSARIAL_REVIEW_REQUEST.md",
        "AUDIT_REPORT.md",
        "CATCH_PROOF_RESULT.json",
        "COMMANDS.md",
        "DERIVATION_RESULT.json",
        "EVIDENCE_GATES.md",
        "EXACT_DERIVATION.md",
        "EXTERNAL_REVIEW.md",
        "INDEPENDENT_VERIFICATION.json",
        "LAY_REPORT.md",
        "MAP.md",
        "PREMISE_LEDGER.tsv",
        "PREREGISTRATION.md",
        "REPAIR_PREREGISTRATION.md",
        "REPAIR_RESULT.md",
        "REVIEW_TRANSMISSION_RECORD.md",
        "RUN_RECORD.md",
        "SOURCE_MANIFEST.tsv",
        "STATUS_LEDGER.tsv",
        "build_review_intake.py",
        "derive_proper_clock_scale.py",
        "run_catch_proofs.py",
        "verify_package.py",
        "verify_proper_clock_scale_independent.py",
    )
    for name in required:
        assert (ROOT / name).is_file(), name

    production = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (ROOT / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
    )
    catches = json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    assert production["status"] == independent["status"] == catches["status"] == "PASS"
    assert production["landing"] == independent["landing"] == LANDING
    assert production["exact_checks"] == 22 and all(production["checks"].values())
    assert production["scope"]["metric_or_kernel_modified"] is False
    assert production["scope"]["c_E_numerical_value_derived"] is False
    assert independent["production_imported"] is False
    assert independent["production_output_read"] is False
    assert independent["cases"] == 20_000
    assert independent["exact_assertions"] == 320_003
    assert independent["inconsistent_records_rejected"] == 20_000
    assert independent["self_evaluations_rejected"] == 20_000
    assert independent["same_segment_mismatches_rejected"] == 20_000
    assert catches["implementation_mutations_caught"] == 6
    assert catches["typed_scope_catches_passed"] == 2
    assert len(catches["mutation_ledger"]) == 8
    assert all(
        row["baseline_passed"] and row["mutant_rejected"]
        for row in catches["mutation_ledger"]
    )

    replay("derive_proper_clock_scale.py")
    replay("verify_proper_clock_scale_independent.py")
    replay("run_catch_proofs.py")

    report = (ROOT / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    assert "EXTERNALLY_REVIEWED_ACCEPT_WITH_REPAIRS__R1_IMPLEMENTED__FOLLOWUP_PENDING" in report
    assert "ACCEPT_WITH_REPAIRS" in report
    assert "R1_IMPLEMENTED" in report
    assert "do not fix" in report
    assert "not canon" in report
    forbidden = (
        "c_E alone fixes",
        "history is selected",
        "X_max is derived",
        "metric was modified",
        "kernel was modified",
    )
    assert not any(token in report for token in forbidden)

    result = {
        "status": "PASS",
        "landing": LANDING,
        "source_rows": len(sources),
        "production_checks": 22,
        "independent_cases": 20_000,
        "independent_exact_assertions": 320_003,
        "inconsistent_records_rejected": 20_000,
        "self_evaluations_rejected": 20_000,
        "same_segment_mismatches_rejected": 20_000,
        "implementation_mutations_caught": 6,
        "typed_scope_catches_passed": 2,
        "no_write_replays": 3,
        "grade": "EXTERNALLY_REVIEWED_ACCEPT_WITH_REPAIRS__R1_IMPLEMENTED__FOLLOWUP_PENDING",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        assert OUT.read_text(encoding="utf-8") == rendered
    else:
        OUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
