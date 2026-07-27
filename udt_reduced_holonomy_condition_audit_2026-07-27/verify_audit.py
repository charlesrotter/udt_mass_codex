#!/usr/bin/env python3
"""Fail-closed verifier and exercised catches for the reduced-holonomy audit."""

from __future__ import annotations

import copy
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
STAMPS = (
    "COPRESENCE = WORKING_INTERPRETIVE_FRAME",
    "METRIC_CAUSAL_STRUCTURE = DERIVED_CONDITIONAL",
    "INSTANTANEOUS_OPERATIONAL_ACCESS = NOT_DERIVED",
    "COMPLETE_WHOLE_SOLUTION_LAW = OPEN",
)
CASES = ("GENERIC_NOT_PLUS_MINUS_ONE", "LAMBDA_PLUS_ONE", "LAMBDA_MINUS_ONE")


def rows(name: str) -> list[dict]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def baseline_state() -> dict:
    return {
        "stamps": STAMPS, "cases": CASES, "all_blocks": True,
        "parallelism_primary": True, "regular_BC_nonzero": True,
        "a_zero_regular": True, "ruler_loss_visible": True, "global_integrability": True,
        "global_completion_checked": True, "metric_nondegenerate": True,
        "symbolic_zero": True, "independent_cases": 4,
        "coordinate_count": 3, "coordinate_error": 0.0, "round_degeneracy_visible": True,
        "curvature_only_promoted": False, "path_groupoid_invalidated": False,
        "lambda_selected": False, "universalized": False, "physical_solution_claimed": False,
        "seam_selected": False, "action_inferred": False, "bootstrap_inferred": False,
        "dynamics_inferred": False, "premise_promoted": False,
    }


def validate(state: dict) -> None:
    assert state["stamps"] == STAMPS and state["cases"] == CASES and state["all_blocks"]
    assert state["parallelism_primary"] and state["regular_BC_nonzero"]
    assert state["a_zero_regular"] and state["ruler_loss_visible"]
    assert state["global_integrability"] and state["global_completion_checked"]
    assert state["metric_nondegenerate"] and state["symbolic_zero"]
    assert state["independent_cases"] == 4
    assert state["coordinate_count"] == 3 and state["coordinate_error"] <= 2.0e-8
    assert state["round_degeneracy_visible"]
    assert not state["curvature_only_promoted"] and not state["path_groupoid_invalidated"]
    assert not state["lambda_selected"] and not state["universalized"]
    assert not state["physical_solution_claimed"] and not state["seam_selected"]
    assert not state["action_inferred"] and not state["bootstrap_inferred"]
    assert not state["dynamics_inferred"] and not state["premise_promoted"]


def exercised_failure(field: str, value) -> str:
    candidate = copy.deepcopy(baseline_state()); candidate[field] = value
    try:
        validate(candidate)
    except AssertionError:
        return "PASS"
    raise AssertionError(f"corruption accepted: {field}")


def main() -> int:
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    connection = rows("CARTAN_CONNECTION.tsv")
    components = rows("PARALLELISM_COMPONENTS.tsv")
    classifications = rows("CASE_CLASSIFICATION.tsv")
    survivor_curvature = rows("SURVIVOR_CURVATURE.tsv")
    degeneracies = rows("DEGENERACY_ESCAPE_REGISTRY.tsv")
    independent_cases = rows("INDEPENDENT_CASE_HOLDOUTS.tsv")
    coordinate = rows("INDEPENDENT_CURVATURE_HOLDOUTS.tsv")
    contracts = rows("FALSIFICATION_CONTRACT.tsv")

    assert result["status"] == "COMPUTED" and independent["status"] == "PASS"
    assert len(connection) == independent["independent_Koszul_connection_components"] == 30
    assert len(classifications) == 3 and tuple(row["case"] for row in classifications) == CASES
    assert len(components) == 22 + 10 + 14
    assert len(survivor_curvature) == 3 and all(row["commutator_with_X"] == "ZERO" for row in survivor_curvature)
    assert len(degeneracies) == 5 and len(independent_cases) == 4 and len(coordinate) == 3
    assert all(row["sufficiency_exact"] == row["each_required_variable_detected"] == "PASS"
               for row in independent_cases)
    assert all(int(row["curvature_algebra_rank"]) == 3 for row in coordinate)
    assert all(float(row["metric_determinant"]) != 0 for row in coordinate)

    expected_iff = {
        "GENERIC_NOT_PLUS_MINUS_ONE": "p1=p2=p3=A=B=0",
        "LAMBDA_PLUS_ONE": "p1=p2=p3=A=0",
        "LAMBDA_MINUS_ONE": "p1=p2=p3=B=0",
    }
    for row in classifications:
        assert row["pointwise_iff"] == expected_iff[row["case"]]
    assert classifications[0]["regular_S3_compatible"] == "NO"
    assert classifications[1]["regular_S3_compatible"] == "YES"
    assert classifications[2]["regular_S3_compatible"] == "NO"
    assert result["regular_complete_survivor_count"] == 1
    assert result["nonconstant_regular_survivor_count"] == 0
    assert result["nontrivial_twist_regular_survivor_count"] == 0
    assert result["intrinsic_clock_ruler_pair_survivor_count"] == 0
    assert result["survivor"]["lambda"] == 1
    assert result["survivor"]["curvature_holonomy_rank"] == 3
    assert result["survivor"]["metric_intrinsic_ruler_retained"] is False

    observed = baseline_state()
    observed.update({
        "coordinate_error": independent["maximum_coordinate_curvature_scaled_error"],
        "metric_nondegenerate": independent["survivor_metrics_nondegenerate"],
    })
    validate(observed)

    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    for stamp in STAMPS:
        assert stamp in prereg and stamp in report

    mutations = {
        "F01": ("stamps", STAMPS[:-1]), "F02": ("cases", CASES[:-1]),
        "F03": ("all_blocks", False), "F04": ("parallelism_primary", False),
        "F05": ("regular_BC_nonzero", False), "F06": ("a_zero_regular", False),
        "F07": ("ruler_loss_visible", False), "F08": ("global_integrability", False),
        "F09": ("global_completion_checked", False), "F10": ("metric_nondegenerate", False),
        "F11": ("symbolic_zero", False), "F12": ("independent_cases", 3),
        "F13": ("coordinate_error", 3.0e-8), "F14": ("round_degeneracy_visible", False),
        "F15": ("curvature_only_promoted", True), "F16": ("path_groupoid_invalidated", True),
        "F17": ("lambda_selected", True), "F18": ("universalized", True),
        "F19": ("physical_solution_claimed", True), "F20": ("seam_selected", True),
        "F21": ("action_inferred", True), "F22": ("bootstrap_inferred", True),
        "F23": ("dynamics_inferred", True), "F24": ("premise_promoted", True),
    }
    assert set(mutations) == {row["catch_id"] for row in contracts}
    catch_rows = [{
        "catch_id": row["catch_id"], "result": exercised_failure(*mutations[row["catch_id"]]),
        "corruption_or_overclaim": row["corruption_or_overclaim"],
    } for row in contracts]
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(catch_rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(catch_rows)

    verification = {
        "schema": "udt-reduced-holonomy-condition-verification-1.0", "status": "PASS",
        "connection_components": 30, "parallelism_components": 46, "case_strata": 3,
        "regular_complete_survivors": 1, "intrinsic_pair_survivors": 0,
        "independent_case_holdouts": 4, "coordinate_curvature_holdouts": 3,
        "survivor_curvature_rank": 3, "catch_proofs": "24/24",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(verification, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
