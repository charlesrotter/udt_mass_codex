#!/usr/bin/env python3
"""Exact symbolic controller for the bounded R17 vertical-lift audit."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def is_zero_matrix(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def main() -> None:
    d, d1, d2, phi_p, phi_q = sp.symbols("d d1 d2 phi_p phi_q", real=True)
    lam, a, w = sp.symbols("lambda a w", real=True)
    eta = sp.diag(-1, 1, 1, 1)
    identity = sp.eye(4)
    x_lam = sp.diag(-1, 1, lam, lam)

    def lift(depth: sp.Expr, screen_weight: sp.Expr) -> sp.Matrix:
        return sp.diag(
            sp.exp(-depth), sp.exp(depth),
            sp.exp(screen_weight * depth), sp.exp(screen_weight * depth),
        )

    l_d = lift(d, lam)
    checks: dict[str, bool] = {}
    checks["exponential_equals_complete_factor"] = is_zero_matrix(
        sp.exp(d * x_lam) - l_d
    )
    checks["composition"] = is_zero_matrix(
        lift(d2, lam) * lift(d1, lam) - lift(d1 + d2, lam)
    )
    checks["reversal"] = is_zero_matrix(lift(-d, lam) - l_d.inv())
    checks["coincidence"] = is_zero_matrix(lift(0, lam) - identity)
    checks["endpoint_quotient"] = is_zero_matrix(
        lift(phi_q, lam) * lift(phi_p, lam).inv() - lift(phi_q - phi_p, lam)
    )

    pair_projection = sp.diag(1, 1, 0, 0)
    checks["pair_normalization_independent_of_screen_weight"] = is_zero_matrix(
        pair_projection * (lift(d, a) - lift(d, lam)) * pair_projection
    )
    checks["zero_fails_nonzero_founded_depth"] = not is_zero_matrix(
        lift(sp.log(2), lam) - identity
    )

    metric_a = sp.simplify(lift(d, a).T * eta * lift(d, a))
    metric_lam = sp.simplify(l_d.T * eta * l_d)
    checks["arbitrary_screen_weight_changes_complete_metric"] = sp.simplify(
        metric_a[2, 2] - metric_lam[2, 2]
    ) != 0
    checks["supplied_lambda_reproduces_complete_metric"] = is_zero_matrix(
        metric_lam - sp.diag(
            -sp.exp(-2 * d), sp.exp(2 * d),
            sp.exp(2 * lam * d), sp.exp(2 * lam * d),
        )
    )

    b11, b12, b21, b22 = sp.symbols("b11 b12 b21 b22", real=True)
    screen_generator = sp.Matrix([[b11, b12], [b21, b22]])
    solution = sp.linsolve(
        [
            2 * b11 - 2 * lam,
            b12 + b21,
            2 * b22 - 2 * lam,
        ],
        (b11, b12, b21, b22),
    )
    expected_solution = sp.FiniteSet((lam, -b21, b21, lam))
    checks["screen_generator_is_lambda_I_plus_rotation"] = solution == expected_solution

    quarter_turn = sp.diag(1, 1, 1, 1)
    quarter_turn[2, 2] = 0
    quarter_turn[2, 3] = -1
    quarter_turn[3, 2] = 1
    quarter_turn[3, 3] = 0
    checks["screen_rotation_is_isometric"] = is_zero_matrix(
        quarter_turn.T * eta * quarter_turn - eta
    )
    checks["screen_rotation_commutes_with_lift"] = is_zero_matrix(
        quarter_turn * l_d - l_d * quarter_turn
    )
    checks["screen_rotation_leaves_metric_scaling"] = is_zero_matrix(
        (quarter_turn * l_d).T * eta * (quarter_turn * l_d) - metric_lam
    )

    boost_1, boost_2, boost_3, rot_1, rot_2, rot_3 = sp.symbols(
        "boost_1 boost_2 boost_3 rot_1 rot_2 rot_3", real=True
    )
    lie_parameters = (boost_1, boost_2, boost_3, rot_1, rot_2, rot_3)
    omega = sp.Matrix(
        [
            [0, boost_1, boost_2, boost_3],
            [boost_1, 0, -rot_3, rot_2],
            [boost_2, rot_3, 0, -rot_1],
            [boost_3, -rot_2, rot_1, 0],
        ]
    )
    p_u = sp.diag(1, 0, 0, 0)
    p_n = sp.diag(0, 1, 0, 0)
    h_screen = sp.diag(0, 0, 1, 1)

    def commutator_rank(matrices: list[sp.Matrix]) -> int:
        equations = []
        for matrix in matrices:
            equations.extend(list(omega * matrix - matrix * omega))
        coefficient_matrix, _ = sp.linear_eq_to_matrix(equations, lie_parameters)
        return int(coefficient_matrix.rank())

    projector_rank = commutator_rank([p_u, p_n, h_screen])
    checks["projector_triple_stabilizer_dimension_one"] = 6 - projector_rank == 1
    grading_stabilizer_dimensions = {}
    for value in [sp.Integer(-2), sp.Integer(-1), sp.Integer(0), sp.Rational(1, 2), sp.Integer(1), sp.Integer(2)]:
        grading_rank = commutator_rank([x_lam.subs(lam, value)])
        grading_stabilizer_dimensions[str(value)] = 6 - grading_rank
    checks["grading_degeneracies_exact"] = grading_stabilizer_dimensions == {
        "-2": 1, "-1": 3, "0": 1, "1/2": 1, "1": 3, "2": 1
    }

    witness = lift(sp.log(2), sp.Rational(1, 2))
    rho1 = sp.simplify(abs((witness.T * eta * witness)[0, 0]))
    rho2 = sp.simplify(abs((witness[:2, :2].T * eta[:2, :2] * witness[:2, :2]).det()))
    q_value = sp.simplify(rho2 / rho1**2)
    checks["terminal_density_witness"] = (rho1, rho2, q_value) == (
        sp.Rational(1, 4), sp.Integer(1), sp.Integer(16)
    )

    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise AssertionError(f"failed exact checks: {failed}")

    result = {
        "primary_landing": (
            "COMPLETE_COFRAME_CONDITIONAL_VERTICAL_RECIPROCAL_METRIC_CLASS_MOD_SO2__"
            "FULL_PHYSICAL_ARROW_OPEN"
        ),
        "scope": "R17/W01 C01-C06 regular global off-shell configurations",
        "exact_checks": checks,
        "exact_check_count": len(checks),
        "pair_only_class": "clock/ruler weights fixed; screen generator remains free",
        "complete_metric_class": "screen generator lambda*I+w*J; w is SO(2) presentation freedom",
        "complete_coframe_realization_gate_used": True,
        "complete_coframe_realization_status": "CONDITIONAL_BRANCH_CONFIGURATION_INPUT",
        "founding_pair_alone_fixes_screen": False,
        "raw_arrow_uniqueness": False,
        "metric_vertical_factor_unique_modulo_screen_rotation": True,
        "zero_lift_is_a_depth_realization": False,
        "lambda_selected_across_family": False,
        "full_semidirect_assembly_selected": False,
        "physical_path_or_isometric_factor_selected": False,
        "intrinsic_endpoint_reset_selected": False,
        "pair_surface_selected": False,
        "universal_mixed_ceff_selected": False,
        "downstream_physics_derived": [],
        "lambda_values": ["-2", "-1", "0", "1/2", "1", "2"],
        "grading_stabilizer_dimensions": grading_stabilizer_dimensions,
        "projector_triple_stabilizer_dimension": 1,
        "density_witness": {"rho1": "1/4", "rho2": "1", "Q": "16"},
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"exact checks: {len(checks)}/{len(checks)}")
    print(result["primary_landing"])


if __name__ == "__main__":
    main()
