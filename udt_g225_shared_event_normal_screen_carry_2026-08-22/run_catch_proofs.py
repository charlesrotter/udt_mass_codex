#!/usr/bin/env python3
"""Hostile result and algorithm mutations for the G225 contract."""

from __future__ import annotations

import copy
import json
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LANDING = (
    "METRIC_AND_SHARED_CLOCK_DEFINE_POSITIVE_INCIDENT_SCREEN_PLANES"
    "__CANONICAL_LEAST_TURNING_DIRECT_SCREEN_ISOMETRY_EXISTS_OFF_ANTIPODES"
    "__THREE_DIRECTION_COMPOSITION_RETAINS_FINITE_O2_HOLONOMY_AND_NO_GLOBAL_ENDPOINT_ONLY_FLAT_SCREEN_CARRY_EXISTS"
    "__G188_JACOBI_TRANSPORT_REMAINS_SEPARATE"
)


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def validate(production: dict, independent: dict) -> None:
    require(production["status"] == "PASS", "production status")
    require(production["symbolic_checks"] == 39, "symbolic count")
    require(production["screen_planes_metric_derived"] is True, "screen planes")
    require(production["least_turning_direct_isometry_nonantipodal"] is True, "direct isometry")
    require(not production["direct_isometry_exact_vertex_cocycle"], "false cocycle")
    require(production["finite_composition_holonomy"] is True, "holonomy")
    require(not production["antipodal_least_turning_extension_unique"], "antipodal uniqueness")
    require(not production["global_endpoint_only_flat_screen_carry"], "global flat carry")
    require(production["G224_scalar_carry_retained"] is True, "scalar carry")
    require(not production["G188_Jacobi_replaced"], "Jacobi replacement")
    require(not production["pointwise_direct_map_physical_transport_selected"], "physical transport")
    require(not production["independent_direct_relation_constrained"], "direct relation")
    require(not production["universal_null_protocol_selected"], "universal protocol")
    require(not production["physical_history_selected"], "physical history")
    require(production["landing"] == LANDING, "production landing")

    require(independent["status"] == "PASS", "independent status")
    require(independent["cases"] == 20000, "independent cases")
    require(independent["exact_rational_assertions"] == 580013, "independent assertions")
    require(independent["nontrivial_composition_defects"] == 19922, "defect count")
    require(not independent["production_code_imported"], "production import")
    require(not independent["sympy_imported"], "SymPy import")
    require(independent["landing"] == LANDING, "independent landing")


def matrix_multiply(left: tuple[tuple[F, ...], ...], right: tuple[tuple[F, ...], ...]):
    return tuple(
        tuple(sum((left[i][k] * right[k][j] for k in range(3)), F(0)) for j in range(3))
        for i in range(3)
    )


def matrix_vector(matrix: tuple[tuple[F, ...], ...], vector: tuple[F, ...]):
    return tuple(sum((matrix[i][j] * vector[j] for j in range(3)), F(0)) for i in range(3))


def main() -> None:
    production = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    validate(production, independent)

    mutations = (
        ("production_status", "p", "status", "FAIL"),
        ("symbolic_count", "p", "symbolic_checks", 38),
        ("screen_planes", "p", "screen_planes_metric_derived", False),
        ("direct_isometry", "p", "least_turning_direct_isometry_nonantipodal", False),
        ("false_cocycle", "p", "direct_isometry_exact_vertex_cocycle", True),
        ("delete_holonomy", "p", "finite_composition_holonomy", False),
        ("antipodal_promotion", "p", "antipodal_least_turning_extension_unique", True),
        ("global_flat_promotion", "p", "global_endpoint_only_flat_screen_carry", True),
        ("scalar_deletion", "p", "G224_scalar_carry_retained", False),
        ("Jacobi_collapse", "p", "G188_Jacobi_replaced", True),
        ("physical_transport_promotion", "p", "pointwise_direct_map_physical_transport_selected", True),
        ("direct_relation_promotion", "p", "independent_direct_relation_constrained", True),
        ("protocol_promotion", "p", "universal_null_protocol_selected", True),
        ("history_promotion", "p", "physical_history_selected", True),
        ("production_landing", "p", "landing", "PROMOTED"),
        ("independent_status", "i", "status", "FAIL"),
        ("case_count", "i", "cases", 19999),
        ("assertion_count", "i", "exact_rational_assertions", 580012),
        ("defect_count", "i", "nontrivial_composition_defects", 0),
        ("production_import", "i", "production_code_imported", True),
        ("sympy_import", "i", "sympy_imported", True),
    )
    rejected: list[str] = []
    for name, target, field, value in mutations:
        p_test = copy.deepcopy(production)
        i_test = copy.deepcopy(independent)
        (p_test if target == "p" else i_test)[field] = value
        try:
            validate(p_test, i_test)
        except AssertionError:
            rejected.append(name)
    require(len(rejected) == len(mutations), "payload mutation escaped")

    # Four algorithm-level hostile controls on the exact octant witness.
    identity = ((F(1), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(1)))
    ex = (F(1), F(0), F(0))
    ey = (F(0), F(1), F(0))
    correct_xy = ((F(0), F(-1), F(0)), (F(1), F(0), F(0)), (F(0), F(0), F(1)))
    wrong_sign_xy = ((F(0), F(1), F(0)), (F(-1), F(0), F(0)), (F(0), F(0), F(1)))
    omitted_quadratic = ((F(1), F(-1), F(0)), (F(1), F(1), F(0)), (F(0), F(0), F(1)))
    correct_yz = ((F(1), F(0), F(0)), (F(0), F(0), F(-1)), (F(0), F(1), F(0)))
    direct_xz = ((F(0), F(0), F(-1)), (F(0), F(1), F(0)), (F(1), F(0), F(0)))
    anti_one = ((F(-1), F(0), F(0)), (F(0), F(-1), F(0)), (F(0), F(0), F(1)))
    anti_two = ((F(-1), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(-1)))

    algorithm_rejected = []
    if matrix_vector(wrong_sign_xy, ex) != ey:
        algorithm_rejected.append("wrong_Rodrigues_sign")
    if matrix_multiply(tuple(zip(*omitted_quadratic)), omitted_quadratic) != identity:
        algorithm_rejected.append("omitted_quadratic_term")
    if matrix_multiply(correct_yz, correct_xy) != direct_xz:
        algorithm_rejected.append("false_exact_cocycle")
    if anti_one != anti_two:
        algorithm_rejected.append("false_antipodal_uniqueness")
    require(len(algorithm_rejected) == 4, "algorithm mutation escaped")

    result = {
        "status": "PASS",
        "payload_mutations_attempted": len(mutations),
        "payload_mutations_rejected": len(rejected),
        "rejected": rejected,
        "algorithm_mutations_attempted": 4,
        "algorithm_mutations_rejected": 4,
        "algorithm_rejected": algorithm_rejected,
        "total_contract_mutations": len(mutations) + 4,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
