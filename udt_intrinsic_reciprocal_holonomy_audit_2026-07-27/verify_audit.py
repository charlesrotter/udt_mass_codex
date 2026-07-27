#!/usr/bin/env python3
"""Fail-closed verifier and exercised catch proofs for the holonomy audit."""

from __future__ import annotations

import copy
import csv
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
STAMPS = (
    "COPRESENCE = WORKING_INTERPRETIVE_FRAME",
    "METRIC_CAUSAL_STRUCTURE = DERIVED_CONDITIONAL",
    "INSTANTANEOUS_OPERATIONAL_ACCESS = NOT_DERIVED",
    "COMPLETE_WHOLE_SOLUTION_LAW = OPEN",
)
LAMBDAS = ("-2", "-1", "0", "0.5", "1", "2")
EVENTS = ("P00", "P01", "P02")
LOOPS = ("G1", "G2", "G3", "L12", "L23", "L31")


def rows(name: str) -> list[dict]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def baseline_state() -> dict:
    return {
        "stamps": STAMPS, "lambdas": LAMBDAS, "events": EVENTS, "declared_loops": LOOPS,
        "observed_pairs": 36, "cpu": True, "float64": True,
        "coframe_error": 0.0, "lorentz_error": 0.0, "composition_error": 0.0,
        "convergence_error": 0.0, "rk_count": 12, "rk_error": 0.0,
        "coordinate_count": 18, "coordinate_error": 0.0, "coordinate_ranks": (6,),
        "rank_rtol": 1.0e-9, "anchor": "-3/25", "nabla_rows": 18,
        "ordinary_distinct_from_inversion": True, "reset_not_selected": True,
        "lorentz_conjugate_count": 0, "branch_selected": False,
        "global_topology_claimed": False, "physical_solution_claimed": False,
        "path_groupoid_invalidated": False, "universal_claimed": False,
        "path_or_seam_selected": False, "downstream_physics_inferred": False,
        "premise_promoted": False,
    }


def validate(state: dict) -> None:
    assert state["stamps"] == STAMPS
    assert state["lambdas"] == LAMBDAS
    assert state["events"] == EVENTS and state["declared_loops"] == LOOPS
    assert state["observed_pairs"] == 36
    assert state["cpu"] and state["float64"]
    assert state["coframe_error"] <= 2.0e-10
    assert state["lorentz_error"] <= 2.0e-8
    assert state["composition_error"] <= 2.0e-8
    assert state["convergence_error"] <= 2.0e-7
    assert state["rk_count"] == 12 and state["rk_error"] <= 2.0e-6
    assert state["coordinate_count"] == 18 and state["coordinate_error"] <= 2.0e-8
    assert state["coordinate_ranks"] == (6,)
    assert state["rank_rtol"] == 1.0e-9
    assert state["anchor"] == "-3/25" and state["nabla_rows"] == 18
    assert state["ordinary_distinct_from_inversion"] and state["reset_not_selected"]
    assert state["lorentz_conjugate_count"] == 0
    assert not state["branch_selected"] and not state["global_topology_claimed"]
    assert not state["physical_solution_claimed"] and not state["path_groupoid_invalidated"]
    assert not state["universal_claimed"] and not state["path_or_seam_selected"]
    assert not state["downstream_physics_inferred"] and not state["premise_promoted"]


def exercised_failure(field: str, value) -> str:
    candidate = copy.deepcopy(baseline_state())
    candidate[field] = value
    try:
        validate(candidate)
    except AssertionError:
        return "PASS"
    raise AssertionError(f"corruption accepted: {field}")


def main() -> int:
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    local = rows("LOCAL_NABLA_X.tsv")
    curvature = rows("CURVATURE_HOLONOMY.tsv")
    loops = rows("LOOP_HOLONOMY.tsv")
    coordinate = rows("INDEPENDENT_CURVATURE_HOLDOUTS.tsv")
    rk4 = rows("RK4_HOLDOUTS.tsv")
    signatures = rows("INVERSION_SIGNATURES.tsv")
    contracts = rows("FALSIFICATION_CONTRACT.tsv")

    assert result["status"] == "COMPUTED" and independent["status"] == "PASS"
    assert len(local) == len(curvature) == len(coordinate) == 18
    assert len(loops) == 36 and len(rk4) == 12 and len(signatures) == 6
    expected_local = {(lam, event) for lam in LAMBDAS for event in EVENTS}
    expected_loops = {(lam, loop) for lam in LAMBDAS for loop in LOOPS}
    assert {(row["lambda"], row["event_id"]) for row in local} == expected_local
    assert {(row["lambda"], row["event_id"]) for row in curvature} == expected_local
    assert {(row["lambda"], row["event_id"]) for row in coordinate} == expected_local
    assert {(row["lambda"], row["loop_id"]) for row in loops} == expected_loops
    assert Counter(row["lambda"] for row in loops) == {lam: 6 for lam in LAMBDAS}

    assert result["exact_P00_nabla_E0_X_0_1"] == independent["exact_P00_nabla_E0_X_0_1"] == "-3/25"
    assert min(float(row["clock_ruler"]) for row in local) > 0
    assert max(float(row["screen_internal"]) for row in local) == 0
    assert all(float(row["clock_screen"]) == 0 for row in local if row["lambda"] == "-1")
    assert all(float(row["ruler_screen"]) == 0 for row in local if row["lambda"] == "1")
    assert all(int(row["curvature_span_rank"]) == int(row["lie_closure_rank"]) == 6 for row in curvature)
    assert all(int(row["independent_curvature_span_rank"]) == 6 for row in coordinate)
    assert Counter(int(row["centralizer_dimension_in_holonomy"]) for row in curvature) == {1: 12, 3: 6}
    assert min(float(row["max_basis_commutator_with_X"]) for row in curvature) > 0

    assert min(float(row["nonidentity_max"]) for row in loops) > 0
    assert min(float(row["ordinary_closure_residual"]) for row in loops) > 1.0e-10
    assert all(row["Lorentz_conjugate"] == "NO" for row in signatures)
    assert result["loops_with_nonzero_ordinary_closure_residual"] == 36

    observed = baseline_state()
    observed.update({
        "coframe_error": result["maximum_global_chart_coframe_scaled_error"],
        "lorentz_error": result["maximum_loop_lorentz_residual"],
        "composition_error": result["maximum_loop_composition_residual"],
        "convergence_error": result["maximum_loop_convergence_residual"],
        "rk_error": independent["maximum_RK4_DOP853_difference"],
        "coordinate_error": independent["maximum_coordinate_frame_scaled_error"],
        "coordinate_ranks": tuple(independent["independent_curvature_span_ranks"]),
        "lorentz_conjugate_count": independent["sampled_X_and_minus_X_Lorentz_conjugate_count"],
    })
    validate(observed)

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    for stamp in STAMPS:
        assert stamp in report and stamp in prereg

    mutations = {
        "F01": ("stamps", STAMPS[:-1]), "F02": ("lambdas", LAMBDAS[:-1]),
        "F03": ("declared_loops", LOOPS[:-1]), "F04": ("observed_pairs", 35),
        "F05": ("cpu", False), "F06": ("coframe_error", 3.0e-10),
        "F07": ("lorentz_error", 3.0e-8), "F08": ("composition_error", 3.0e-8),
        "F09": ("convergence_error", 3.0e-7), "F10": ("rk_count", 11),
        "F11": ("coordinate_error", 3.0e-8), "F12": ("rank_rtol", 1.0e-6),
        "F13": ("anchor", "+3/25"), "F14": ("ordinary_distinct_from_inversion", False),
        "F15": ("reset_not_selected", False), "F16": ("lorentz_conjugate_count", 1),
        "F17": ("branch_selected", True), "F18": ("global_topology_claimed", True),
        "F19": ("physical_solution_claimed", True), "F20": ("path_groupoid_invalidated", True),
        "F21": ("universal_claimed", True), "F22": ("path_or_seam_selected", True),
        "F23": ("downstream_physics_inferred", True), "F24": ("premise_promoted", True),
    }
    assert set(mutations) == {row["catch_id"] for row in contracts}
    catch_rows = [{
        "catch_id": row["catch_id"],
        "result": exercised_failure(*mutations[row["catch_id"]]),
        "corruption_or_overclaim": row["corruption_or_overclaim"],
    } for row in contracts]
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(catch_rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(catch_rows)

    verification = {
        "schema": "udt-intrinsic-reciprocal-holonomy-verification-1.0",
        "status": "PASS", "local_rows": 18, "curvature_rows": 18,
        "loop_transports": 36, "coordinate_holdouts": 18, "RK4_holdouts": 12,
        "exact_nonparallel_anchor": "-3/25", "curvature_span_rank": 6,
        "ordinary_loop_nonclosure_count": 36, "Lorentz_inversion_conjugate_count": 0,
        "catch_proofs": "24/24", "numerical_gates": "7/7",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(verification, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
