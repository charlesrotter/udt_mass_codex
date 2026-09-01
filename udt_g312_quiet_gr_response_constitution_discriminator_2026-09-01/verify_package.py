#!/usr/bin/env python3
"""Dependency-free aggregate verifier for the G312 package."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
LANDING = "TWO_OR_MORE_INDEPENDENT_NEW_PREMISES_ARE_REQUIRED"


def run(name):
    completed = subprocess.run(
        [sys.executable, "-S", str(HERE / name)],
        cwd=HERE,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode:
        raise SystemExit(f"{name} failed: {completed.stderr}")
    return json.loads(completed.stdout)


def saved(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def main():
    required = (
        "MAP.md",
        "PONDER.md",
        "PREREGISTRATION.md",
        "PREREGISTRATION_ANCESTRY.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_SCOPE.tsv",
        "EXACT_DERIVATION.md",
        "LAY_REPORT.md",
        "STATUS_LEDGER.tsv",
        "EVIDENCE_GATES.md",
        "RUN_RECORD.md",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "PACKAGE_VERIFICATION_RESULT.json",
        "derive_response_constitution.py",
        "verify_response_constitution_independent.py",
        "run_catch_proofs.py",
        "EXTERNAL_REVIEW_REQUEST.md",
        "build_review_intake.py",
    )
    for name in required:
        if not (HERE / name).is_file():
            raise SystemExit(f"missing required file: {name}")

    production = run("derive_response_constitution.py")
    independent = run("verify_response_constitution_independent.py")
    catches = run("run_catch_proofs.py")
    production_saved = saved("DERIVATION_RESULT.json")
    independent_saved = saved("INDEPENDENT_VERIFICATION.json")
    catches_saved = saved("CATCH_PROOF_RESULT.json")

    assert production["status"] == independent["status"] == catches["status"] == "PASS"
    assert production["landing"] == independent["landing"] == LANDING
    assert production["exact_checks"] == production_saved["exact_checks"] == 4690
    assert production["landing"] == production_saved["landing"]
    assert production["ownership_result"]["not_owned"] == production_saved["not_owned"]
    assert independent == independent_saved
    assert catches == catches_saved
    assert independent["production_imported"] is False
    assert independent["production_result_read"] is False
    assert catches["grade"] == "SEMANTIC_REGRESSION_CATCHES_NOT_INDEPENDENT_CONFIRMATION"
    assert "TWO_OR_MORE_INDEPENDENT_NEW_PREMISES_ARE_REQUIRED" in (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    assert "The metric and reciprocal kernel were not changed." in (HERE / "LAY_REPORT.md").read_text(encoding="utf-8")

    result = {
        "status": "PASS",
        "landing": LANDING,
        "production_checks": production["exact_checks"],
        "independent_checks": independent["checks"],
        "semantic_regression_catches": catches["catch_count"],
        "preregistration_commit": "0c139b1c",
        "external_review": "REQUIRED",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
