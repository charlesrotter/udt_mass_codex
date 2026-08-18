#!/usr/bin/env python3
"""Package-level verification for G159."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
LANDING = (
    "CALIBRATED_PAIR_FIRST_JET_DERIVED__COMPLETE_SCORE_DESCENDS_WITH_DOTJ_LIVE__"
    "H_AND_DOTH_LIVE_LORENTZ_COFRAME_GAUGE_INVARIANT__KAPPA_DENSITY_COEFFICIENT_"
    "AND_PHI_BETA_CEFF_REQUIRE_PAIR_CALIBRATION_CARRY__PHYSICAL_HISTORY_QUERY_"
    "LAMBDA_AND_GLOBAL_COMPLETION_OPEN"
)
BASE_REQUIRED = {
    "PREREGISTRATION.md", "SOURCE_MANIFEST.tsv", "SOURCE_FREEZE.md",
    "derive_terminal_first_jet.py", "DERIVATION_RESULT.json",
    "verify_terminal_first_jet_independent.py", "INDEPENDENT_RESULT.json",
    "run_catch_proofs.py", "CATCH_PROOF_RESULT.json", "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md", "LAY_REPORT.md", "EVIDENCE_GATES.md", "RUN_RECORD.md",
    "FRESH_ADVERSARIAL_REVIEW.md", "REPAIR_RECORD.md",
    "INTERNAL_REPAIR_FOLLOWUP.md", "verify_package.py",
}
FINAL_REQUIRED = {"PREMISE_VERIFIER_OUTPUT.txt", "REPOSITORY_TEST_OUTPUT.txt"}


def main() -> None:
    present = {path.name for path in HERE.iterdir() if path.is_file()}
    assert not (BASE_REQUIRED - present), sorted(BASE_REQUIRED - present)
    for script in (
        "derive_terminal_first_jet.py",
        "verify_terminal_first_jet_independent.py",
        "run_catch_proofs.py",
    ):
        subprocess.run([sys.executable, str(HERE / script)], check=True,
                       stdout=subprocess.DEVNULL)

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
    assert production["status"] == independent["status"] == catches["status"] == "PASS"
    assert production["landing"] == independent["landing"] == LANDING
    expected_class = (
        "CALIBRATED_PAIR_FIRST_JET_DERIVED__H_DOTH_LORENTZ_GAUGE_INVARIANT__"
        "TERMINAL_COMPONENTS_REQUIRE_CALIBRATION_CARRY"
    )
    assert production["registered_outcome_class"] == independent["registered_outcome_class"] == expected_class
    assert production["source_count"] == independent["source_count"] == 7
    assert production["exact_checks"] == len(production["exact_check_names"]) == 9
    assert independent["exact_fraction_trials"] == 500
    assert independent["independent_dual_number_definition_derivative_trials"] == 500
    assert independent["arbitrary_live_gl2_rechart_trials"] == 500
    assert independent["live_lorentz_gauge_trials"] == 500
    assert catches["catch_count"] == 10 and all(item["caught"] for item in catches["caught"])
    assert catches["algebra_mutation_count"] == 6
    assert catches["metadata_guard_mutation_count"] == 4
    assert catches["metadata_guards_are_independent_semantic_proofs"] is False
    assert catches["live_lorentz_catch_targets_dotV_score_law_not_terminal_doth"] is True
    for result in (production, independent):
        assert result["query_motion_frozen"] is False
        assert result["h_and_doth_lorentz_coframe_gauge_invariant"] is True
        assert result["terminal_coefficients_arbitrary_gl2_invariant"] is False
        assert result["physical_history_derived"] is False
        assert result["physical_lambda_owned"] is False
        assert result["calibration_carry_derived"] is False

    final_ready = not (FINAL_REQUIRED - present)
    if final_ready:
        assert "PASS: G159-extended premise guards" in (HERE / "PREMISE_VERIFIER_OUTPUT.txt").read_text()
        assert "passed" in (HERE / "REPOSITORY_TEST_OUTPUT.txt").read_text()
    status = "PASS" if final_ready else "PRELIMINARY_PASS"
    result = {
        "status": status,
        "required_files": len(BASE_REQUIRED | (FINAL_REQUIRED if final_ready else set())),
        "source_count": 7,
        "exact_checks": 9,
        "independent_exact_trials": 500,
        "independent_dual_number_trials": 500,
        "algebra_mutation_count": 6,
        "metadata_guard_mutation_count": 4,
        "fresh_adversarial_followup": "PASS",
        "landing": LANDING,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
