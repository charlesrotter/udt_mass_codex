#!/usr/bin/env python3
"""Deterministic G135 package and source-integrity verifier."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "VERIFICATION_RESULT.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    checks: dict[str, bool] = {}

    controller_runs = {}
    for script in (
        "derive_projective_pair_separation.py",
        "verify_projective_pair_separation_independent.py",
        "run_catch_proofs.py",
    ):
        run = subprocess.run(
            ["python3", str(HERE / script)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        controller_runs[script] = {
            "returncode": run.returncode,
            "stdout": run.stdout.strip(),
            "stderr": run.stderr.strip(),
        }
    checks["all_controllers_rerun_cleanly"] = all(
        result["returncode"] == 0 and result["stderr"] == ""
        for result in controller_runs.values()
    )

    with (HERE / "DERIVATION_RESULT.json").open() as stream:
        primary = json.load(stream)
    with (HERE / "INDEPENDENT_VERIFICATION.json").open() as stream:
        independent = json.load(stream)
    with (HERE / "CATCH_PROOF_RESULT.json").open() as stream:
        catches = json.load(stream)

    checks["primary_35_of_35"] = (
        primary["status"] == "PASS"
        and primary["checks_passed"] == primary["checks_total"] == 35
        and all(primary["checks"].values())
    )
    checks["independent_21_of_21"] = (
        independent["status"] == "PASS"
        and independent["checks_passed"] == independent["checks_total"] == 21
        and all(independent["checks"].values())
    )
    checks["catch_proofs_6_of_6"] = (
        catches["status"] == "PASS"
        and catches["caught"] == catches["total"] == 6
        and all(catches["checks"].values())
    )

    source_rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
    checks["source_manifest_15_rows"] = len(source_rows) == 15
    checks["source_manifest_paths_exist"] = all((ROOT / row["path"]).is_file() for row in source_rows)
    checks["source_manifest_hashes_match"] = all(
        sha256(ROOT / row["path"]) == row["sha256"] for row in source_rows
    )

    exact = (HERE / "EXACT_DERIVATION.md").read_text()
    report = (HERE / "AUDIT_REPORT.md").read_text()
    status_rows = {
        row["claim_id"]: row
        for row in csv.DictReader((HERE / "STATUS_LEDGER.tsv").open(), delimiter="\t")
    }
    prereg = (HERE / "PREREGISTRATION.md").read_text()

    required_exact = [
        "chi=(L-T)/(L+T)",
        "H D H^-1",
        "-45/29728",
        "physical pair query/realization",
        "strong local CSN is inactive and unnecessary",
        "No canonization is requested",
    ]
    checks["exact_derivation_required_guards"] = all(token in exact for token in required_exact)
    checks["report_grade_is_verified_with_caveats"] = (
        "VERIFIED_WITH_CAVEATS__FRESH_ZERO_CONTEXT_FOLLOWUP_PASS" in report
    )
    checks["physical_identification_remains_conditional"] = (
        status_rows["S13"]["status"] == "CONDITIONAL_ON_CONSTITUTIVE_CLARIFICATION"
        and status_rows["S14"]["status"] == "CONDITIONAL_ON_CONSTITUTIVE_CLARIFICATION"
    )
    checks["preregistered_landing_present"] = (
        "PROJECTIVE_PAIR_COORDINATE_DERIVED_IN_NATURAL_CLASS" in prereg
    )
    checks["xmax_guards_are_exact"] = (
        status_rows["S12"]["status"] == "NOT_DERIVED"
        and status_rows["S16"]["status"] == "OPEN"
    )
    checks["fresh_followup_pass_recorded"] = (
        (HERE / "FOLLOWUP_REVIEW.md").is_file()
        and "FOLLOWUP_PASS" in (HERE / "FOLLOWUP_REVIEW.md").read_text()
    )

    premise_run = subprocess.run(
        ["python3", "verify_current_scientific_premises.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    checks["current_premise_verifier_passes"] = (
        premise_run.returncode == 0 and premise_run.stdout.startswith("PASS:")
    )

    checks = {name: bool(value) for name, value in checks.items()}
    passed = sum(checks.values())
    result = {
        "schema": "udt-g135-package-verification-v1",
        "status": "PASS" if passed == len(checks) else "FAIL",
        "checks_passed": passed,
        "checks_total": len(checks),
        "checks": checks,
        "controller_runs": controller_runs,
        "premise_verifier_stdout": premise_run.stdout.strip(),
        "premise_verifier_stderr": premise_run.stderr.strip(),
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
