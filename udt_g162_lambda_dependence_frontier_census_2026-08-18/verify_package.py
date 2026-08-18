#!/usr/bin/env python3
"""Fail-closed package verification for G162."""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTCOME_CLASS = (
    "SECOND_REPAIR_SCALAR_KERNEL_DESCENDS_TO_QUOTIENT__CANONICAL_ENDPOINT_CARRY_EXACT__"
    "JOINED_ROUTE_FRAME_CHANNEL_RETAINS_LAMBDA__HISTORY_GAP_UNCHANGED"
)
LANDING = (
    "BOUNDED_SCALAR_RECIPROCAL_KERNEL_IS_RESIDUAL_LORENTZ_INVARIANT__"
    "UNIQUE_POSITIVE_ENDPOINT_ROOTS_GIVE_EXACT_FLAT_CALIBRATION_CARRY__"
    "GENERAL_COMPATIBLE_CARRY_FACTORS_AS_RB_INVERSE_LAMBDA_RA__JOINED_C_"
    "AND_GAMMA_RETAIN_SUPPLIED_ROUTE_FRAME_RAPIDITY__NORMAL_HOLONOMY_"
    "JACOBI_AND_EXTRINSIC_CHANNELS_REMAIN_SEPARATELY_TYPED__RAPIDITY_"
    "SELECTION_RETIRED_AS_SCALAR_KERNEL_GATE_ONLY__PHYSICAL_HISTORY_QUERY_"
    "PATH_CARRY_XMAX_AND_COMPLETION_OPEN"
)
BASE_REQUIRED = {
    "PREREGISTRATION.md", "PREREGISTRATION_REPAIR.md", "PREREGISTRATION_REPAIR_2.md",
    "INITIAL_TYPE_FAILURE_RECORD.json", "FIRST_REPAIR_FAILURE_RECORD.json",
    "SOURCE_FREEZE.md", "SOURCE_MANIFEST.tsv", "SOURCE_OBJECT_CROSSWALK.tsv",
    "SECOND_REPAIR_EXECUTION_NOTE.md",
    "derive_lambda_census.py", "DERIVATION_RESULT.json", "DEPENDENCY_CENSUS.tsv",
    "verify_lambda_census_independent.py", "INDEPENDENT_RESULT.json",
    "run_catch_proofs.py", "CATCH_PROOF_RESULT.json", "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md", "LAY_REPORT.md", "STATUS_LEDGER.tsv", "EVIDENCE_GATES.md",
    "RUN_RECORD.md", "ADVERSARIAL_REVIEW_REQUEST.md", "FRESH_ADVERSARIAL_REVIEW.md",
    "verify_package.py",
}
FINAL_REQUIRED = {"PREMISE_VERIFIER_OUTPUT.txt", "REPOSITORY_TEST_OUTPUT.txt"}


def main():
    present = {path.name for path in HERE.iterdir() if path.is_file()}
    assert not (BASE_REQUIRED - present), sorted(BASE_REQUIRED - present)

    for script in (
        "derive_lambda_census.py",
        "verify_lambda_census_independent.py",
        "run_catch_proofs.py",
    ):
        subprocess.run([sys.executable, str(HERE / script)], check=True,
                       stdout=subprocess.DEVNULL)

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text())
    assert production["status"] == independent["status"] == catches["status"] == "PASS"
    assert production["registered_outcome_class"] == independent["registered_outcome_class"] == OUTCOME_CLASS
    assert production["landing"] == independent["landing"] == LANDING
    assert production["source_count"] == independent["source_count"] == 13
    assert production["exact_checks"] == len(production["exact_check_names"]) == 14
    assert independent["fraction_dual_trials"] == 900
    assert independent["general_factorization_trials"] == 900
    assert independent["reverse_factorization_trials"] == 900
    assert independent["metric_rate_split_trials"] == 900
    assert independent["canonical_section_trials"] == 900
    assert independent["three_observer_composition_trials"] == 900
    assert independent["live_first_jet_trials"] == 900
    assert independent["independent_expected_object_inventory_rows"] == 22
    assert independent["source_object_crosswalk_rows"] == 13
    assert catches["catch_count"] == 12
    assert catches["algebra_mutation_count"] == 4
    assert catches["metadata_guard_mutation_count"] == 8
    assert catches["metadata_guards_are_independent_semantic_proofs"] is False
    assert all(item["caught"] for item in catches["caught"])

    for result in (production, independent):
        assert result["census_rows"] == 22
        assert result["scalar_kernel_lambda_invariant"] is True
        assert result["canonical_endpoint_section_exact_and_composable"] is True
        assert result["canonical_endpoint_section_is_physical_overlap_or_path"] is False
        assert result["joined_C_Gamma_lambda_sensitive"] is True
        assert result["all_active_objects_lambda_invariant"] is False
        assert result["normal_jacobi_extrinsic_channels_reduced_to_tangent_lambda"] is False
        assert result["rapidity_selection_remains_scalar_kernel_gate"] is False
        assert result["physical_history_derived"] is False
        assert result["physical_query_path_carry_derived"] is False

    with (HERE / "DEPENDENCY_CENSUS.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert [row["id"] for row in rows] == [f"D{i:02d}" for i in range(1, 23)]
    classes = {row["class"] for row in rows}
    assert "REPRESENTATIVE_COFRAME_GAUGE_CHANNEL__NOT_A_QUOTIENT_OBSERVABLE" in classes
    assert production["class_counts"] == independent["class_counts"] == {
        "QUOTIENT_OWNED__LAMBDA_INVARIANT": 9,
        "CANONICAL_ENDPOINT_SECTION__LAMBDA_SET_TO_IDENTITY_BY_REBUILD": 1,
        "SUPPLIED_ROUTE_FRAME_CHANNEL__LAMBDA_SENSITIVE": 5,
        "REPRESENTATIVE_COFRAME_GAUGE_CHANNEL__NOT_A_QUOTIENT_OBSERVABLE": 2,
        "INDEPENDENT_PATH_OR_EXTRINSIC_CHANNEL__NOT_REDUCIBLE_TO_TANGENT_LAMBDA": 3,
        "HISTORY_VALUE_OR_EVOLUTION_OPEN__CENSUS_DOES_NOT_SELECT": 2,
    }
    initial = json.loads((HERE / "INITIAL_TYPE_FAILURE_RECORD.json").read_text())
    assert initial["initial_registered_outcome"] == "DEPENDENCY_CENSUS_TYPE_FAILURE"
    assert initial["status"] == "CAUGHT_BEFORE_BANKING"
    first_repair = json.loads((HERE / "FIRST_REPAIR_FAILURE_RECORD.json").read_text())
    assert first_repair["status"] == "FRESH_ADVERSARIAL_FAIL_BEFORE_BANKING"

    review = (HERE / "FRESH_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
    assert "Verdict: `PASS`" in review or "Verdict: `PASS_WITH_CAVEATS`" in review

    final_ready = not (FINAL_REQUIRED - present)
    if final_ready:
        assert "PASS:" in (HERE / "PREMISE_VERIFIER_OUTPUT.txt").read_text()
        assert "passed" in (HERE / "REPOSITORY_TEST_OUTPUT.txt").read_text()

    result = {
        "status": "PASS" if final_ready else "PRELIMINARY_PASS",
        "required_files": len(BASE_REQUIRED | (FINAL_REQUIRED if final_ready else set())),
        "source_count": 13,
        "exact_checks": 14,
        "independent_trials_per_family": 900,
        "census_rows": 22,
        "catch_count": 12,
        "fresh_adversarial": "PASS_OR_PASS_WITH_CAVEATS",
        "landing": LANDING,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
