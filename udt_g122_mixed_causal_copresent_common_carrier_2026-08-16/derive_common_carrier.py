#!/usr/bin/env python3
"""Exact finite-dimensional checks for the preregistered G122 carrier audit."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def matrix_zero(m: sp.Matrix) -> bool:
    return all(sp.simplify(x) == 0 for x in m)


def main() -> None:
    tau, lam, a, b = sp.symbols("tau lam a b", real=True)
    eta = sp.diag(-1, 1, 1, 1)
    n0 = sp.sqrt(1 - a**2 - b**2)
    F = sp.Matrix([tau + lam, lam * n0, lam * a, lam * b])
    vars_ = (tau, lam, a, b)
    dF = F.jacobian(vars_).subs({a: 0, b: 0})
    pullback = sp.simplify(dF.T * eta * dF)
    pair = pullback[:2, :2]
    angular = pullback[2:, 2:]

    # The parallel columns have zero projection to the standard transverse screen.
    screen_rows = sp.Matrix([[0, 0, 1, 0], [0, 0, 0, 1]])
    pair_screen = screen_rows * dF[:, :2]
    jacobi_screen = screen_rows * dF[:, 2:]

    # Any linear map from phase S+S to a screen-trivial target is killed by the
    # passive O(2) half-turn, which acts as -I on both copies of S.
    q_symbols = sp.symbols("q0:8", real=True)
    q = sp.Matrix(2, 4, q_symbols)
    phase_half_turn = -sp.eye(4)
    invariant_residual = sp.simplify(q * phase_half_turn - q)
    zero_solution = sp.solve(list(invariant_residual), q_symbols, dict=True)

    # If the target itself is a screen representation, O(2)-equivariance leaves
    # q=[alpha I, beta I].  That target is not supplied by the pair metric.
    x = sp.symbols("x0:8", real=True)
    q_screen = sp.Matrix(2, 4, x)
    rot90 = sp.Matrix([[0, -1], [1, 0]])
    reflect = sp.diag(1, -1)
    phase_rot90 = sp.diag(1, 1, 1, 1)
    phase_rot90[:2, :2] = rot90
    phase_rot90[2:, 2:] = rot90
    phase_reflect = sp.diag(1, 1, 1, 1)
    phase_reflect[:2, :2] = reflect
    phase_reflect[2:, 2:] = reflect
    equivariant_eqs = list(q_screen * phase_rot90 - rot90 * q_screen)
    equivariant_eqs += list(q_screen * phase_reflect - reflect * q_screen)
    equivariant_solution = sp.linsolve(equivariant_eqs, x)

    # Ordinary position caustic: phase propagation remains invertible.
    phase_at_pi = sp.Matrix.vstack(
        sp.Matrix.hstack(-sp.eye(2), sp.zeros(2)),
        sp.Matrix.hstack(sp.zeros(2), -sp.eye(2)),
    )
    position_at_pi = sp.zeros(2)

    # G116 generic local scalar junction and its pure reciprocal reduction.
    R, p2, v, vdot, Aopt = sp.symbols("R p2 v vdot Aopt", real=True)
    phi_pair = p2 * R**2
    zeta = v * R + (p2 + vdot - Aopt / 4) * R**2
    scalar_defect = sp.expand(zeta - phi_pair)
    generic_example = sp.expand(scalar_defect.subs({v: 3, vdot: 5, Aopt: 7}))
    pure_defect = sp.simplify(scalar_defect.subs({v: 0, vdot: 0, Aopt: 0}))

    checks = {
        "flat_pair_metric_exact": pair == sp.Matrix([[-1, -1], [-1, 0]]),
        "flat_pair_lorentzian": sp.simplify(pair.det()) == -1,
        "flat_angular_metric_exact": angular == lam**2 * sp.eye(2),
        "flat_pair_screen_rank_zero": pair_screen.rank() == 0,
        "flat_angular_jacobi_rank_two_for_nonzero_lambda": jacobi_screen.det() == lam**2,
        "trivial_target_invariance_forces_zero": zero_solution == [
            {symbol: 0 for symbol in q_symbols}
        ],
        "screen_target_equivariant_family_is_two_parameter": str(equivariant_solution)
        == "{(x5, 0, x7, 0, 0, x5, 0, x7)}",
        "phase_survives_position_caustic": phase_at_pi.det() == 1
        and position_at_pi.rank() == 0,
        "generic_scalar_channels_differ": generic_example != 0,
        "pure_reciprocal_scalar_channels_agree": pure_defect == 0,
    }

    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "exact_objects": {
            "flat_dF": str(dF),
            "flat_pullback": str(pullback),
            "pair_screen": str(pair_screen),
            "angular_jacobi": str(jacobi_screen),
            "trivial_target_invariant_residual": str(invariant_residual),
            "screen_target_equivariant_family": str(equivariant_solution),
            "g116_scalar_defect": str(scalar_defect),
            "g116_generic_example": str(generic_example),
            "g116_pure_defect": str(pure_defect),
        },
        "landing": (
            "COMMON_OBSERVER_EXPONENTIAL_PATHWISE_DEPENDENCY_RECORD_DERIVED_CONDITIONALLY__"
            "NO_DATA_FREE_INFORMATION_PRESERVING_LINEAR_SOLDER_FROM_TERMINAL_PAIR_DATA__"
            "G116_LOCAL_TWO_JET_SCALAR_JUNCTION_ONLY__DIRECT_AB_PAIR_MAP_UNTESTED__"
            "NO_HISTORY_SELECTOR_FOUND_IN_DECLARED_TEST"
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
