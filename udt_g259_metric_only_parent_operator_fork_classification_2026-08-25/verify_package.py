#!/usr/bin/env python3
"""Verify the bounded G259 evidence package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
LANDING = (
    "CONDITIONAL_LOVELOCK_CLASS_SELECTS_EINSTEIN_ZERO_SET"
    "__CLASS_ASSUMPTIONS_NOT_UDT_DERIVED"
    "__EXTREME_METRIC_DEPARTURE_REQUIRES_EXPLICIT_NEW_STRUCTURE"
    "__SOURCE_HISTORY_REMAINS_OPEN"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    required = (
        "MAP.md",
        "PREMISE_LEDGER.tsv",
        "PREREGISTRATION.md",
        "REPAIR_PREREGISTRATION.md",
        "REPAIR_CERTIFICATION.json",
        "SOURCE_MANIFEST.tsv",
        "EXACT_DERIVATION.md",
        "LOVELOCK_NAVARRO_SCOPE.md",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "STATUS_LEDGER.tsv",
        "EVIDENCE_GATES.md",
        "RUN_RECORD.md",
        "REVIEW_REQUEST.md",
        "REPAIR_FOLLOWUP_REQUEST.md",
        "EXTERNAL_REVIEW_GPT54.md",
        "TRANSMISSION_RECORD.md",
        "CANDIDATE_CLASS_ATLAS.tsv",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "DEPENDENCY_FREE_REPLAY_RESULT.json",
        "derive_parent_operator_fork.py",
        "verify_independent.py",
        "run_catch_proofs.py",
        "verify_dependency_free.py",
        "verify_package.py",
        "build_review_intake.py",
    )
    missing = [name for name in required if not (ROOT / name).is_file()]
    assert not missing, missing

    with (ROOT / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    assert len(sources) == 11
    for source in sources:
        path = REPO / source["path"]
        assert path.is_file(), source["path"]
        assert digest(path) == source["sha256"], source["path"]

    with (ROOT / "PREMISE_LEDGER.tsv").open(newline="") as handle:
        premises = {row["id"]: row for row in csv.DictReader(handle, delimiter="\t")}
    for name in ("locality", "rank_two_symmetry", "second_order", "divergence_free"):
        assert premises[name]["status"] == "NEW_PREMISE_CANDIDATE"
        assert premises[name]["included"] == "explored_not_owned"
    assert premises["W3"]["status"] == "WORKING_POSIT_NOT_CANON"
    assert premises["G258_knots"]["included"] == "no_selection"

    result = json.loads((ROOT / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text())
    dependency_free = json.loads((ROOT / "DEPENDENCY_FREE_REPLAY_RESULT.json").read_text())
    repair = json.loads((ROOT / "REPAIR_CERTIFICATION.json").read_text())
    assert result["status"] == "PASS" and result["landing"] == LANDING
    assert result["lovelock_method"]["basis"] == ["metric", "Einstein"]
    assert result["lovelock_method"]["basis_dimension"] == 2
    assert result["lovelock_method"]["flat_quiet_removes_metric_term"] is True
    assert result["lovelock_method"]["assumptions_owned_by_F1_F4_W1_W3"] is False
    assert result["lovelock_method"]["theorem_scope_file"] == "LOVELOCK_NAVARRO_SCOPE.md"
    assert result["lovelock_method"]["zero_operator_excluded"] is True
    assert result["lovelock_method"]["nonzero_coefficient_required"] is True
    assert result["spherical_replay"]["dependence"] == "0"
    assert result["spherical_replay"]["vacuum_family"] == "f=1+C/r"
    assert result["higher_order_counterfamily"]["retains_every_Ricci_flat_metric"] is True
    assert result["higher_order_counterfamily"]["lambda_values_registered"] == [1, 2]
    assert result["dimension_audit"]["cE_and_Gobs_form_length"] is False
    assert result["G258_value_gate"]["values_select_operator"] is False
    assert result["fit_coefficients"] == 0
    assert result["observational_values_used"] == 0
    assert result["gpu_used"] is False and result["protected_inputs_used"] == 0

    assert independent["status"] == "PASS" and independent["assertions"] == 111
    assert independent["production_imported"] is False
    assert independent["production_result_read"] is False
    assert all(independent["checks"].values())
    assert catches["status"] == "PASS" and catches["caught_count"] == 11
    assert all(catches["catches"].values())
    assert dependency_free["status"] == "PASS" and dependency_free["assertions"] == 139
    assert dependency_free["standard_library_only"] is True
    assert dependency_free["sympy_imported"] is False
    assert dependency_free["production_imported"] is False
    assert dependency_free["production_result_read"] is False
    assert all(dependency_free["checks"].values())
    assert repair["status"] == "PASS" and repair["scientific_landing_changed"] is False
    assert repair["dependency_free_assertions"] == 139
    assert repair["hostile_catches"] == 11
    assert repair["full_repository_tests"]["observed_exit_code"] == 0
    assert all(
        proof["observed_exit_code"] != 0 and proof["result"] == "RED"
        for proof in repair["catch_proofs"].values()
    )

    with (ROOT / "CANDIDATE_CLASS_ATLAS.tsv").open(newline="") as handle:
        atlas = list(csv.DictReader(handle, delimiter="\t"))
    assert len(atlas) == 6
    by_class = {row["class"]: row for row in atlas}
    assert by_class["currently_owned_F1_F4_W1_W3"]["status"] == "NO_PARENT_OPERATOR"
    assert (
        by_class["local_metric_only_second_order_divergence_free"]["selection"]
        == "Einstein_vacuum_zero_set_for_nonzero_operator"
    )
    assert by_class["local_metric_only_higher_derivative"]["selection"] == "nonunique"

    prereg = (ROOT / "PREREGISTRATION.md").read_text()
    exact = (ROOT / "EXACT_DERIVATION.md").read_text()
    theorem_scope = (ROOT / "LOVELOCK_NAVARRO_SCOPE.md").read_text()
    assert "a1fa9d7d" not in prereg  # outcome commit was not known at preregistration time
    assert "arXiv:1306.4354" in prereg and "arXiv:1005.2386" in prereg
    assert "This use of the theorem is mathematical method" in exact
    assert "The degenerate case \\(a=0\\) is the identically zero operator" in exact
    assert "not a physical parent law" in exact
    assert "Theorem 5.3" in theorem_scope and "2m <= n-1" in theorem_scope
    assert "does not say that UDT's physical parent operator belongs to this class" in theorem_scope
    assert "Current premises select neither fork" in exact

    verification = {
        "status": "PASS",
        "landing": LANDING,
        "source_hashes": len(sources),
        "candidate_classes": len(atlas),
        "independent_assertions": independent["assertions"],
        "hostile_catches": catches["caught_count"],
        "dependency_free_assertions": dependency_free["assertions"],
        "external_review": "ACCEPT_WITH_REPAIRS__R1_R2_R3_IMPLEMENTED__FOLLOWUP_OPEN",
    }
    (ROOT / "VERIFICATION_RESULT.json").write_text(
        json.dumps(verification, indent=2, sort_keys=True) + "\n"
    )
    print(
        "PASS: G259 package, "
        f"{len(sources)} source hashes, {len(atlas)} classes, "
        f"{independent['assertions']} independent assertions, "
        f"{dependency_free['assertions']} dependency-free assertions, "
        f"{catches['caught_count']} catches"
    )


if __name__ == "__main__":
    main()
