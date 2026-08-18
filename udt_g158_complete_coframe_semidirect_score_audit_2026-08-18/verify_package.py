#!/usr/bin/env python3
"""Package-level verification for G158."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
LANDING = (
    "GAUGE_FIXED_COMPLETE_COFRAME_SEMIDIRECT_SCORE_DERIVED__"
    "TEN_CHANNEL_REGULAR_GROUP_CLOSES__BASE_AND_SCREEN_BPLUS2_CHANNELS_"
    "ACT_ON_FOUR_MIXING_COMPONENTS__Y_Z_ARE_QUERY_REPRESENTATION_DATA_"
    "NOT_GROUP_COORDINATES__CHANGING_BALANCE_ALLOWED__PHYSICAL_CARRY_"
    "HISTORY_SCORE_AND_GLOBAL_COMPLETION_OPEN"
)
BASE_REQUIRED = {
    "PREREGISTRATION.md", "SOURCE_MANIFEST.tsv", "SOURCE_FREEZE.md",
    "derive_complete_coframe_score.py", "DERIVATION_RESULT.json",
    "verify_complete_coframe_independent.py", "INDEPENDENT_RESULT.json",
    "run_catch_proofs.py", "CATCH_PROOF_RESULT.json", "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md", "LAY_REPORT.md", "EVIDENCE_GATES.md", "RUN_RECORD.md",
    "FRESH_ADVERSARIAL_REVIEW.md", "REPAIR_RECORD.md", "verify_package.py",
}
FINAL_REQUIRED = {
    "INTERNAL_REPAIR_FOLLOWUP.md", "PREMISE_VERIFIER_OUTPUT.txt",
    "REPOSITORY_TEST_OUTPUT.txt",
}


def main() -> None:
    present = {path.name for path in HERE.iterdir() if path.is_file()}
    assert not (BASE_REQUIRED - present), sorted(BASE_REQUIRED - present)
    for script in (
        "derive_complete_coframe_score.py",
        "verify_complete_coframe_independent.py",
        "run_catch_proofs.py",
    ):
        subprocess.run([sys.executable, str(HERE / script)], check=True, stdout=subprocess.DEVNULL)

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
    assert production["status"] == independent["status"] == catches["status"] == "PASS"
    assert production["landing"] == independent["landing"] == LANDING
    assert production["registered_outcome_class"] == independent["registered_outcome_class"] == (
        "COMPLETE_COFRAME_SEMIDIRECT_SCORE_DERIVED"
    )
    assert production["source_count"] == independent["source_count"] == 10
    assert production["exact_checks"] == len(production["exact_check_names"]) == 12
    assert production["coordinate_count"] == independent["coordinate_count"] == 10
    assert production["ten_coordinate_jacobian_determinant"] == "q00**2*q11**2"
    assert independent["exact_fraction_trials"] == 500
    assert independent["fixed_generator_trials"] == 200
    assert production["changing_score_witness_noncollinear"] is True
    assert independent["changing_score_witness_noncollinear"] is True
    assert catches["catch_count"] == 10 and all(item["caught"] for item in catches["caught"])
    assert catches["algebra_mutation_count"] == catches["metadata_guard_mutation_count"] == 5
    assert catches["metadata_guards_are_independent_semantic_proofs"] is False
    for result in (production, independent):
        assert result["query_blocks_are_group_coordinates"] is False
        assert result["physical_score_derived"] is False
        assert result["physical_cross_query_carry_derived"] is False

    final_ready = not (FINAL_REQUIRED - present)
    if final_ready:
        assert "FOLLOWUP_PASS" in (HERE / "INTERNAL_REPAIR_FOLLOWUP.md").read_text()
        assert "PASS: G158-extended premise guards" in (HERE / "PREMISE_VERIFIER_OUTPUT.txt").read_text()
        assert "passed" in (HERE / "REPOSITORY_TEST_OUTPUT.txt").read_text()
    status = "PASS" if final_ready else "PRELIMINARY_PASS"
    result = {
        "status": status,
        "required_files": len(BASE_REQUIRED | (FINAL_REQUIRED if final_ready else set())),
        "source_count": 10,
        "exact_checks": 12,
        "independent_exact_trials": 500,
        "independent_fixed_generator_trials": 200,
        "algebra_mutation_count": 5,
        "metadata_guard_mutation_count": 5,
        "changing_score_witness_noncollinear": True,
        "landing": LANDING,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
