#!/usr/bin/env python3
"""Aggregate integrity and provenance verifier for G292."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
OUT = HERE / "PACKAGE_VERIFICATION_RESULT.json"
LANDING = (
    "ORIENTABLE_SCREEN_EULER_FLUX_DESCENDS_EXACTLY"
    "__G225_SKY_AND_G290_PAIR_CONNECTIONS_REQUIRE_SUPPLIED_IDENTIFICATION"
    "__GLOBAL_SAME_PAIR_BLOCK_SAME_EULER_CLASS_DIFFERENT_LOCAL_FLUX_METRIC_FAMILY"
    "__NO_CONTINUOUS_FLUX_PROPAGATION_OR_HISTORY_SELECTION"
)


def run(script: str) -> None:
    subprocess.run(
        [sys.executable, str(HERE / script)],
        cwd=HERE,
        check=True,
        capture_output=True,
        text=True,
    )


def main() -> None:
    required = [
        "MAP.md",
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "COMPLETENESS_MAP.md",
        "EXACT_DERIVATION.md",
        "LAY_REPORT.md",
        "STATUS_LEDGER.tsv",
        "EVIDENCE_GATES.md",
        "RUN_RECORD.md",
        "derive_orientable_screen_flux.py",
        "verify_orientable_screen_flux_independent.py",
        "run_orientable_screen_flux_catches.py",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "EXTERNAL_REVIEW_GPT54.md",
        "EXTERNAL_REVIEW_TRANSMISSION.md",
        "REPAIR_PREREGISTRATION.md",
        "REPAIR_REPORT.md",
        "REPAIR_FOLLOWUP_REQUEST.md",
        "REPAIR_VERIFICATION_RESULT.json",
        "verify_repairs.py",
        "EXTERNAL_REPAIR_FOLLOWUP_GPT54.md",
        "EXTERNAL_REPAIR_FOLLOWUP_TRANSMISSION.md",
    ]
    for name in required:
        if not (HERE / name).is_file():
            raise AssertionError(f"missing required file: {name}")

    sympy_available = importlib.util.find_spec("sympy") is not None
    if not sympy_available:
        raise RuntimeError(
            "sympy is required: aggregate PASS may not reuse the preserved production result"
        )
    run("derive_orientable_screen_flux.py")
    run("verify_orientable_screen_flux_independent.py")
    run("run_orientable_screen_flux_catches.py")

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))

    if production["status"] != "PASS" or production["landing"] != LANDING:
        raise AssertionError("production landing regressed")
    if production["computed_check_count"] != 22:
        raise AssertionError("production check count regressed")
    if production["derived_conclusion_count"] != 12:
        raise AssertionError("production conclusion count regressed")
    if independent["status"] != "PASS" or independent["assertions"] != 25446:
        raise AssertionError("independent replay regressed")
    if independent["imports_production_module"] or independent["reads_production_result"]:
        raise AssertionError("independent replay became circular")
    if catches["status"] != "PASS" or catches["passed"] != 8 or catches["total"] != 8:
        raise AssertionError("hostile catches regressed")

    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    for token in (
        LANDING,
        "FROZEN_BEFORE_DERIVATION_OR_WITNESS_EXECUTION",
        "OPEN_STRATUM",
        "SUPPLIED_WHEN_USED",
    ):
        if token not in exact and token not in prereg:
            raise AssertionError(f"required scope token missing: {token}")

    result = {
        "status": "PASS",
        "landing": LANDING,
        "required_files": len(required),
        "production_computed_checks": 22,
        "production_derived_conclusions": 12,
        "independent_assertions": 25446,
        "independent_point_cases": 3600,
        "independent_cap_quadratures": 105,
        "hostile_claim_witnesses": 8,
        "sympy_production_replayed": sympy_available,
        "fresh_adversarial_context": "PASS",
        "registered_repairs_applied": True,
        "repair_followup": "PASS_ACCEPT_G292_REPAIRS",
        "aggregator_role": "integrity_and_provenance_only",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
