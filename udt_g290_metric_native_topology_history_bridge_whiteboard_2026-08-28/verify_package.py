#!/usr/bin/env python3
"""Aggregate integrity/provenance verifier for the G290 exact package."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
OUT = HERE / "PACKAGE_VERIFICATION_RESULT.json"
LANDING = (
    "EXACT_COMPLETE_PAIR_SCREEN_HOLONOMY_DESCENDS_CONDITIONALLY"
    "__CONFORMAL_TWIN_HISTORY_SEPARATOR_DERIVED"
    "__TIMELIVE_HOLONOMY_CHANGE_EQUALS_SCREEN_CURVATURE_FLUX"
    "__ORIENTABLE_SCREEN_FULL_O2_ROTATION_DATA_IS_INVERSE_CONJUGACY_CLASS"
    "__NO_PERSISTENCE_DYNAMICS_POPULATION_OR_HISTORY_SELECTION"
)


def run(script: str) -> None:
    subprocess.run([sys.executable, str(HERE / script)], cwd=HERE, check=True, capture_output=True, text=True)


def main() -> None:
    required = [
        "MAP.md", "PREREGISTRATION.md", "PREMISE_LEDGER.tsv", "WHITEBOARD_REPORT.md",
        "EXACT_DERIVATION_PREREGISTRATION.md", "EXACT_DERIVATION_PREMISE_LEDGER.tsv",
        "EXACT_DERIVATION.md", "LAY_REPORT.md", "STATUS_LEDGER.tsv", "EVIDENCE_GATES.md",
        "INTERNAL_ADVERSARIAL_REVIEW.md",
        "derive_screen_holonomy.py", "verify_screen_holonomy_independent.py",
        "run_screen_holonomy_catches.py", "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json",
    ]
    for name in required:
        if not (HERE / name).is_file():
            raise AssertionError(f"missing required file: {name}")

    sympy_available = importlib.util.find_spec("sympy") is not None
    if sympy_available:
        run("derive_screen_holonomy.py")
    run("verify_screen_holonomy_independent.py")
    run("run_screen_holonomy_catches.py")

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    if production["status"] != "PASS" or production["landing"] != LANDING:
        raise AssertionError("production landing regressed")
    if production["computed_check_count"] != 19 or production["derived_conclusion_count"] != 9:
        raise AssertionError("production count regressed")
    if independent["status"] != "PASS" or independent["assertions"] != 28801:
        raise AssertionError("independent replay regressed")
    if independent["imports_production_module"] or independent["reads_production_result"]:
        raise AssertionError("independent replay became circular")
    if catches["status"] != "PASS" or catches["passed"] != 7 or catches["total"] != 7:
        raise AssertionError("hostile claim witnesses regressed")

    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    prereg = (HERE / "EXACT_DERIVATION_PREREGISTRATION.md").read_text(encoding="utf-8")
    for token in (LANDING, "Fresh external adversarial review remains open"):
        if token not in exact:
            raise AssertionError(f"exact report token missing: {token}")
    if "FROZEN_BEFORE_EXACT_DERIVATION" not in prereg:
        raise AssertionError("preregistration status missing")

    result = {
        "status": "PASS",
        "landing": LANDING,
        "required_files": len(required),
        "production_computed_checks": 19,
        "production_derived_conclusions": 9,
        "independent_assertions": 28801,
        "hostile_claim_witnesses": 7,
        "sympy_production_replayed": sympy_available,
        "external_review": "OPEN",
        "aggregator_role": "integrity_and_provenance_only",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
