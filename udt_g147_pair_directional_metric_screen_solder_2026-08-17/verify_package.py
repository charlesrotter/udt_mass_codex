#!/usr/bin/env python3
"""Fail-closed package verifier for G147."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def main() -> None:
    checks: dict[str, bool] = {}
    required = (
        "PREREGISTRATION.md",
        "SOURCE_MANIFEST.tsv",
        "derive_pair_screen_solder.py",
        "verify_pair_screen_solder_independent.py",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_RESULT.json",
        "RUN_NOTE.md",
        "EXACT_DERIVATION.md",
        "LAY_REPORT.md",
        "OUTCOME_PREMISE_LEDGER.tsv",
        "EVIDENCE_GATES.md",
        "AUDIT_REPORT.md",
        "FRESH_ADVERSARIAL_REVIEW.md",
        "REVIEW_REPAIR.md",
        "FRESH_ADVERSARIAL_FOLLOWUP.md",
    )
    for name in required:
        checks[f"file_{name}"] = (HERE / name).is_file()

    for script, expected in (
        ("derive_pair_screen_solder.py", "53/53"),
        ("verify_pair_screen_solder_independent.py", "39/39"),
    ):
        run = subprocess.run(
            [sys.executable, str(HERE / script)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        checks[f"run_{script}"] = run.returncode == 0 and expected in run.stdout

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    checks["production_landing"] = production["landing"] == "CONDITIONAL_QUERY_RELATIVE_REST_SPACE_IDENTITY__PHYSICAL_THREE_POSITION_LIFT_AND_CROSS_QUERY_CARRY_OPEN"
    checks["production_count"] = production["passed"] == production["total"] == 53
    checks["production_no_failures"] = production["failures"] == []
    checks["independent_landing"] = independent["landing"] == "INDEPENDENT_PASS"
    checks["independent_count"] = independent["passed"] == independent["total"] == 39
    checks["independent_no_failures"] = independent["failures"] == []
    checks["independent_method"] = "no production imports" in independent["method"]
    checks["pair_metric_exact_match"] = production["registered_witness"]["h"] == independent["witness"]["h"]
    checks["projector_exact_match"] = production["registered_witness"]["screen_projector"] == independent["witness"]["screen_projector"]
    checks["screen_gram_exact_match"] = production["registered_witness"]["screen_gram"] == independent["witness"]["screen_gram"]
    for block_name in "B Q S Y Z".split():
        checks[f"{block_name}_production_h_sensitivity"] = production["checks"][f"{block_name}_sensitivity_changes_h"]
        checks[f"{block_name}_production_projector_sensitivity"] = production["checks"][f"{block_name}_sensitivity_changes_screen_projector"]
        checks[f"{block_name}_independent_h_sensitivity"] = independent["checks"][f"{block_name}_sensitivity_changes_h"]
        checks[f"{block_name}_independent_projector_sensitivity"] = independent["checks"][f"{block_name}_sensitivity_changes_screen_projector"]

    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    checks["source_count"] = len(rows) == 7
    for index, row in enumerate(rows, start=1):
        path = ROOT / row["path"]
        checks[f"source_{index}_exists"] = path.is_file()
        checks[f"source_{index}_hash"] = path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]

    prereg_commit = subprocess.run(
        ["git", "show", "--format=", "--name-only", "9d9b9e90"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    checks["prereg_commit_present"] = (
        prereg_commit.returncode == 0
        and "PREREGISTRATION.md" in prereg_commit.stdout
        and "SOURCE_MANIFEST.tsv" in prereg_commit.stdout
    )

    audit = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    ledger = (HERE / "OUTCOME_PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    for token in (
        "CONDITIONAL_QUERY_RELATIVE_REST_SPACE_IDENTITY__PHYSICAL_THREE_POSITION_LIFT_AND_CROSS_QUERY_CARRY_OPEN",
        "defined conditional lift",
        "physical multidirectional position carrier",
        "FOLLOWUP_PASS",
    ):
        checks[f"audit_{token}"] = token in audit
    for token in (
        "rho=0",
        "A bare Lorentzian two-plane",
        "No orientation or reversal theorem is claimed",
        "different pair queries",
    ):
        checks[f"exact_{token}"] = token in exact
    for token in (
        "SUPPLIED_QUERY_CALIBRATION",
        "DEFINED_SUPPLIED_CONDITIONAL_QUERY_RELATIVE_LIFT",
        "OPEN_OUTSIDE_SCOPE",
        "gyration equals U_gamma",
    ):
        checks[f"ledger_{token}"] = token in ledger

    failures = [name for name, passed in checks.items() if not passed]
    if failures:
        raise SystemExit(f"FAIL: {failures}")
    print(f"PASS: {sum(checks.values())}/{len(checks)} G147 package checks")


if __name__ == "__main__":
    main()
