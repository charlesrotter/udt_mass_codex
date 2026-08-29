#!/usr/bin/env python3
"""Exact G295 architecture checks. Mathematical classifiers, not a UDT field equation."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent


def check(name: str, value, expected, checks: list[dict]) -> None:
    passed = sp.simplify(value - expected) == 0 if not isinstance(value, bool) else value == expected
    checks.append({"name": name, "value": str(value), "expected": str(expected), "pass": bool(passed)})
    if not passed:
        raise AssertionError(f"{name}: {value!r} != {expected!r}")


def matrix_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def causal_lower_triangular(matrix: sp.Matrix) -> bool:
    return all(matrix[i, j] == 0 for i in range(matrix.rows) for j in range(matrix.cols) if j > i)


def main() -> None:
    checks: list[dict] = []

    # Full-row-rank constraint A x = 0 and the most general displayed causal family preserving it.
    alpha, gamma, p, q, s = sp.symbols("alpha gamma p q s")
    A = sp.Matrix([[-1, 1, 0]])
    U = sp.Matrix(
        [
            [alpha, 0, 0],
            [alpha - gamma, gamma, 0],
            [p, q, s],
        ]
    )
    R = sp.Matrix([[gamma]])
    check("constraint_rank", A.rank(), 1, checks)
    check("constraint_propagation_AU_equals_RA", matrix_zero(A * U - R * A), True, checks)
    check("causal_family_lower_triangular", causal_lower_triangular(U), True, checks)

    x, z = sp.symbols("x z")
    constrained_state = sp.Matrix([x, x, z])
    check("input_constraint_zero", (A * constrained_state)[0], 0, checks)
    check("updated_constraint_zero", (A * U * constrained_state)[0], 0, checks)

    # Same constraint, distinct causal updates: compatibility does not select coefficients.
    U1 = U.subs({alpha: 2, gamma: 1, p: 0, q: 1, s: 3})
    U2 = U.subs({alpha: 3, gamma: -2, p: 4, q: -1, s: 2})
    check("first_distinct_update_preserves", matrix_zero(A * U1 - sp.Matrix([[1]]) * A), True, checks)
    check("second_distinct_update_preserves", matrix_zero(A * U2 - sp.Matrix([[-2]]) * A), True, checks)
    check("updates_are_distinct", U1 != U2, True, checks)
    check("first_update_causal", causal_lower_triangular(U1), True, checks)
    check("second_update_causal", causal_lower_triangular(U2), True, checks)

    # Causal support and constraint preservation are independent conditions.
    U_causal_bad = sp.Matrix([[1, 0, 0], [0, 2, 0], [0, 0, 1]])
    check("causal_bad_is_causal", causal_lower_triangular(U_causal_bad), True, checks)
    check("causal_bad_fails_constraint", matrix_zero(A * U_causal_bad - A), False, checks)

    # Orthogonal simultaneous projection onto x0=x2 is constraint preserving but dense/off-cone.
    A_global = sp.Matrix([[1, 0, -1]])
    P_global = sp.eye(3) - A_global.T * (A_global * A_global.T).inv() * A_global
    check("global_projection_idempotent", matrix_zero(P_global * P_global - P_global), True, checks)
    check("global_projection_hits_constraint", matrix_zero(A_global * P_global), True, checks)
    check("global_projection_offcone_02", P_global[0, 2], sp.Rational(1, 2), checks)
    check("global_projection_offcone_20", P_global[2, 0], sp.Rational(1, 2), checks)
    check("global_projection_not_causal_mask", causal_lower_triangular(P_global), False, checks)

    U_dense_bad = sp.Matrix([[1, 1, 1], [1, 0, 1], [0, 1, 2]])
    check("dense_bad_not_causal", causal_lower_triangular(U_dense_bad), False, checks)
    check("dense_bad_not_constraint_preserving", matrix_zero(A_global * U_dense_bad), False, checks)

    # Incidence composition is preserved for every vertex update and therefore is an identity layer.
    B = sp.Matrix([[-1, 1, 0], [0, -1, 1], [-1, 0, 1]])
    cycle = sp.Matrix([[1, 1, -1]])
    check("triangle_cycle_identity", matrix_zero(cycle * B), True, checks)
    v00, v10, v11, v20, v21, v22 = sp.symbols("v00 v10 v11 v20 v21 v22")
    U_vertex = sp.Matrix([[v00, 0, 0], [v10, v11, 0], [v20, v21, v22]])
    check("cycle_identity_survives_arbitrary_causal_vertex_update", matrix_zero(cycle * B * U_vertex), True, checks)
    check("vertex_update_causal", causal_lower_triangular(U_vertex), True, checks)
    check("incidence_rank", B.rank(), 2, checks)
    check("incidence_constant_kernel", B * sp.ones(3, 1) == sp.zeros(3, 1), True, checks)

    # A scalar constraint leaves the complete screen sector unconstrained.
    t1, t2, t3, t4 = sp.symbols("t1 t2 t3 t4")
    screen_1 = sp.Matrix([[t1, 0], [t2, t3]])
    screen_2 = sp.Matrix([[t1, 0], [t2 + 1, t4]])
    U_full_1 = sp.diag(U1, screen_1)
    U_full_2 = sp.diag(U1, screen_2)
    A_full = sp.Matrix([[-1, 1, 0, 0, 0]])
    check("full_state_constraint_preserved_1", matrix_zero(A_full * U_full_1 - A_full), True, checks)
    check("full_state_constraint_preserved_2", matrix_zero(A_full * U_full_2 - A_full), True, checks)
    check("different_screen_updates_same_scalar_constraint", U_full_1 != U_full_2, True, checks)
    check("full_state_dimension_retained", U_full_1.rows, 5, checks)

    # A nonidentity condition can reject a G286-style future, but its choice is not owned here.
    A_future = sp.Matrix([[0, 1]])
    future_0 = sp.Matrix([1, 0])
    future_7 = sp.Matrix([1, 7])
    check("future_zero_admitted", (A_future * future_0)[0], 0, checks)
    check("future_seven_rejected", (A_future * future_7)[0] != 0, True, checks)

    # One fixed law/update still admits different initial data and therefore multiple histories.
    initial_1 = sp.Matrix([1, 1, 0])
    initial_2 = sp.Matrix([2, 2, 1])
    check("initial_1_admissible", (A * initial_1)[0], 0, checks)
    check("initial_2_admissible", (A * initial_2)[0], 0, checks)
    check("initial_data_distinct", initial_1 != initial_2, True, checks)
    history_1 = [initial_1]
    history_2 = [initial_2]
    for _ in range(3):
        history_1.append(U1 * history_1[-1])
        history_2.append(U1 * history_2[-1])
    check("history_1_constraints_propagate", all((A * state)[0] == 0 for state in history_1), True, checks)
    check("history_2_constraints_propagate", all((A * state)[0] == 0 for state in history_2), True, checks)
    check("same_law_different_histories", history_1[-1] != history_2[-1], True, checks)

    # The sliced pair is one residual on adjacent complete states; this is packaging, not a formula choice.
    xin = sp.Matrix(sp.symbols("x0:3"))
    xout = sp.Matrix(sp.symbols("y0:3"))
    history_residual = (A * xin).col_join(xout - U * xin)
    check("unified_sliced_residual_dimension", history_residual.rows, 4, checks)
    check("unified_residual_contains_constraint", history_residual[0], -xin[0] + xin[1], checks)
    check("unified_residual_contains_update", history_residual[1], xout[0] - alpha * xin[0], checks)

    classification = [
        {
            "class": "IDENTITY_DESCENT_ONLY",
            "nonidentity": False,
            "causal": "COMPATIBLE_BUT_NO_RESPONSE_LAW",
            "status": "RECONSTRUCTIVE_NOT_HISTORY_SELECTIVE",
        },
        {
            "class": "INSTANT_GLOBAL_PROJECTION",
            "nonidentity": True,
            "causal": False,
            "status": "REJECTED_AS_CONTROLLABLE_UPDATE_WHEN_OFFCONE_ENTRIES_ARE_ACTIVE",
        },
        {
            "class": "SLICE_CONSTRAINT_PLUS_CAUSAL_UPDATE",
            "nonidentity": True,
            "causal": True,
            "status": "VIABLE_REPRESENTATION_IF_AU_EQUALS_RA_AND_A_SLICING_IS_OWNED",
        },
        {
            "class": "WHOLE_HISTORY_COVARIANT_CONDITION",
            "nonidentity": True,
            "causal": "REQUIRES_WELL_POSED_METRIC_CAUSAL_RESPONSE",
            "status": "LEAST_FOLIATION_DEPENDENT_MISSING_LAW_TYPE_FORMULA_OPEN",
        },
        {
            "class": "INITIAL_OR_BOUNDARY_DATA_ONLY",
            "nonidentity": "MEMBER_SELECTION_ONLY",
            "causal": "NOT_AN_UPDATE",
            "status": "CAN_SELECT_ONE_MEMBER_ONLY_AFTER_A_HISTORY_LAW_EXISTS",
        },
    ]

    result = {
        "all_pass": all(item["pass"] for item in checks),
        "exact_checks": len(checks),
        "checks": checks,
        "classification": classification,
        "landing": (
            "ONE_COVARIANT_HISTORY_CONDITION_IS_THE_MINIMAL_TYPE__"
            "SLICE_CONSTRAINT_AND_CAUSAL_UPDATE_ARE_A_REPRESENTATION__"
            "FORMULA_AND_REALIZED_HISTORY_REMAIN_OPEN"
        ),
        "grade": "INTERNALLY_DERIVED_PENDING_INDEPENDENT_VERIFICATION",
    }
    (ROOT / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"landing": result["landing"], "exact_checks": len(checks)}, indent=2))


if __name__ == "__main__":
    main()
