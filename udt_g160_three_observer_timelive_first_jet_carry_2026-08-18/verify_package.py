#!/usr/bin/env python3
"""Fail-closed package verification for G160."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
LANDING = (
    "TIMELIVE_PAIR_FIRST_JET_CARRY_DERIVED__FULL_GLPLUS2_PULLBACK_AND_"
    "RIGHT_CONNECTION_COMPOSITION_EXACT__CARRY_CLOSURE_SUFFICIENT_NOT_"
    "NECESSARY_DUE_TO_LORENTZ_STABILIZER__ONLY_COMBINED_CARRIED_FIRST_JET_"
    "IS_LIVE_SOURCE_GAUGE_COVARIANT__JOINED_TOTAL_RATE_IS_LIVE_ENDPOINT_"
    "GAUGE_INVARIANT__KAPPA_HAS_UNIVERSAL_DETERMINANT_RATE__NO_PHI_BETA_"
    "CARRY_ONLY_LAW_ON_UNRESTRICTED_GLPLUS2__BPLUS2_SUFFICIENT_NOT_NECESSARY_"
    "FOR_EXACT_CHARACTER_LAWS__SCALAR_RATE_CLOSURE_WEAKER_THAN_MATRIX_RATE_CLOSURE__PHYSICAL_"
    "CARRY_HISTORY_QUERY_LAMBDA_AND_COMPLETION_OPEN"
)
OUTCOME_CLASS = (
    "TIMELIVE_PAIR_FIRST_JET_CARRY_DERIVED__FULL_GLPLUS2_TENSOR_AND_"
    "CONNECTION_COMPOSITION__TERMINAL_CHARACTER_BOUNDARY_CLASSIFIED"
)
BASE_REQUIRED = {
    "PREREGISTRATION.md", "SOURCE_FREEZE.md", "SOURCE_MANIFEST.tsv",
    "derive_timelive_first_jet_carry.py", "DERIVATION_RESULT.json",
    "verify_timelive_carry_independent.py", "INDEPENDENT_RESULT.json",
    "run_catch_proofs.py", "CATCH_PROOF_RESULT.json", "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md", "LAY_REPORT.md", "EVIDENCE_GATES.md", "RUN_RECORD.md",
    "FRESH_ADVERSARIAL_REVIEW.md", "verify_package.py",
}
FINAL_REQUIRED = {"PREMISE_VERIFIER_OUTPUT.txt", "REPOSITORY_TEST_OUTPUT.txt"}


def main() -> None:
    present = {path.name for path in HERE.iterdir() if path.is_file()}
    assert not (BASE_REQUIRED - present), sorted(BASE_REQUIRED - present)

    for script in (
        "derive_timelive_first_jet_carry.py",
        "verify_timelive_carry_independent.py",
        "run_catch_proofs.py",
    ):
        subprocess.run(
            [sys.executable, str(HERE / script)],
            check=True,
            stdout=subprocess.DEVNULL,
        )

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
    assert production["status"] == independent["status"] == catches["status"] == "PASS"
    assert production["landing"] == independent["landing"] == LANDING
    assert production["registered_outcome_class"] == independent["registered_outcome_class"] == OUTCOME_CLASS
    assert production["source_count"] == independent["source_count"] == 10
    assert production["exact_checks"] == len(production["exact_check_names"]) == 13
    assert independent["general_glplus2_trials"] == 500
    assert independent["bplus2_terminal_trials"] == 500
    assert independent["live_endpoint_gauge_trials"] == 500
    assert independent["closed_three_observer_trials"] == 500
    assert independent["nonclosed_defect_rate_trials"] == 500
    assert independent["general_phi_beta_rate_trials"] == 500
    assert independent["total_transition_live_gauge_trials"] == 500
    assert independent["total_transition_composition_trials"] == 500
    assert catches["catch_count"] == 15 and all(item["caught"] for item in catches["caught"])
    assert catches["algebra_mutation_count"] == 11
    assert catches["metadata_guard_mutation_count"] == 4
    assert catches["metadata_guards_are_independent_semantic_proofs"] is False

    for result in (production, independent):
        assert result["general_glplus2_tensor_carry_derived"] is True
        assert result["right_connection_rate_composition_derived"] is True
        assert result["combined_first_jet_live_endpoint_gauge_covariant"] is True
        assert result["intrinsic_connection_split_gauge_independent"] is False
        assert result["phi_beta_carry_only_law_exists_on_full_glplus2"] is False
        assert result["bplus2_sufficient_for_phi_beta_character_laws"] is True
        assert result["bplus2_necessary_for_every_phi_beta_character_law"] is False
        assert result["pair_first_jet_faithfully_detects_carry_closure"] is False
        assert result["lorentz_stabilizer_invisible_to_pair_first_jet"] is True
        assert result["scalar_rate_closure_implies_matrix_rate_closure"] is False
        assert result["physical_carry_derived"] is False
        assert result["physical_history_derived"] is False
        assert result["physical_lambda_owned"] is False

    review = (HERE / "FRESH_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
    assert "Verdict: `PASS`" in review

    final_ready = not (FINAL_REQUIRED - present)
    if final_ready:
        premise = (HERE / "PREMISE_VERIFIER_OUTPUT.txt").read_text(encoding="utf-8")
        tests = (HERE / "REPOSITORY_TEST_OUTPUT.txt").read_text(encoding="utf-8")
        assert "PASS: G160-extended premise guards" in premise
        assert "passed" in tests

    result = {
        "status": "PASS" if final_ready else "PRELIMINARY_PASS",
        "required_files": len(BASE_REQUIRED | (FINAL_REQUIRED if final_ready else set())),
        "source_count": 10,
        "exact_checks": 13,
        "independent_general_trials": 500,
        "independent_bplus2_trials": 500,
        "independent_live_gauge_trials": 500,
        "independent_closed_triangle_trials": 500,
        "independent_nonclosed_defect_trials": 500,
        "independent_general_phi_beta_rate_trials": 500,
        "independent_total_live_gauge_trials": 500,
        "independent_total_composition_trials": 500,
        "algebra_mutation_count": 11,
        "metadata_guard_mutation_count": 4,
        "fresh_adversarial": "PASS",
        "landing": LANDING,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
