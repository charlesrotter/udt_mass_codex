#!/usr/bin/env python3
"""Exact coordinate-tensor derivation for the static spherical reciprocal metric."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def clean(value):
    return sp.factor(sp.trigsimp(sp.simplify(value)))


def main() -> None:
    t, r, theta, azimuth = sp.symbols("t r theta azimuth", real=True)
    c = sp.symbols("c", positive=True)
    X = sp.symbols("X", positive=True)
    a, b = sp.symbols("a b", real=True)
    A = sp.Function("A")(r)
    coords = (t, r, theta, azimuth)
    dimension = 4

    metric = sp.diag(-c**2 * A, 1 / A, r**2, r**2 * sp.sin(theta) ** 2)
    inverse = clean(metric.inv())

    gamma = [[[
        clean(sp.Rational(1, 2) * sum(
            inverse[upper, delta] * (
                sp.diff(metric[delta, right], coords[left])
                + sp.diff(metric[delta, left], coords[right])
                - sp.diff(metric[left, right], coords[delta])
            )
            for delta in range(dimension)
        ))
        for right in range(dimension)] for left in range(dimension)] for upper in range(dimension)]

    # R^rho_{ sigma mu nu } = d_mu Gamma^rho_{nu sigma} - d_nu Gamma^rho_{mu sigma} + ...
    riemann_up = [[[[
        clean(
            sp.diff(gamma[rho][nu][sigma], coords[mu])
            - sp.diff(gamma[rho][mu][sigma], coords[nu])
            + sum(
                gamma[rho][mu][lam] * gamma[lam][nu][sigma]
                - gamma[rho][nu][lam] * gamma[lam][mu][sigma]
                for lam in range(dimension)
            )
        )
        for nu in range(dimension)] for mu in range(dimension)] for sigma in range(dimension)] for rho in range(dimension)]

    ricci = sp.MutableDenseMatrix(dimension, dimension, [0] * (dimension * dimension))
    for sigma in range(dimension):
        for nu in range(dimension):
            ricci[sigma, nu] = clean(sum(riemann_up[rho][sigma][rho][nu] for rho in range(dimension)))
    scalar = clean(sum(inverse[i, j] * ricci[i, j] for i in range(dimension) for j in range(dimension)))

    riemann_down = [[[[
        clean(sum(metric[rho, lam] * riemann_up[lam][sigma][mu][nu] for lam in range(dimension)))
        for nu in range(dimension)] for mu in range(dimension)] for sigma in range(dimension)] for rho in range(dimension)]

    # Diagonal inverse lets the quadratic contractions be evaluated without eight nested sums.
    kretschmann = clean(sum(
        inverse[i, i] * inverse[j, j] * inverse[k, k] * inverse[l, l]
        * riemann_down[i][j][k][l] ** 2
        for i in range(dimension) for j in range(dimension)
        for k in range(dimension) for l in range(dimension)
    ))
    ricci_squared = clean(sum(
        inverse[i, i] * inverse[j, j] * ricci[i, j] ** 2
        for i in range(dimension) for j in range(dimension)
    ))
    weyl_squared = clean(kretschmann - 2 * ricci_squared + scalar**2 / 3)

    expected_scalar = clean(-sp.diff(A, r, 2) - 4 * sp.diff(A, r) / r + 2 * (1 - A) / r**2)
    expected_kretschmann = clean(
        sp.diff(A, r, 2) ** 2
        + 4 * sp.diff(A, r) ** 2 / r**2
        + 4 * (1 - A) ** 2 / r**4
    )
    expected_weyl = clean(
        (sp.diff(A, r, 2) - 2 * sp.diff(A, r) / r + 2 * (A - 1) / r**2) ** 2 / 3
    )

    substitutions = {
        "flat": {A: 1, sp.diff(A, r): 0, sp.diff(A, r, 2): 0},
        "constant": {A: a, sp.diff(A, r): 0, sp.diff(A, r, 2): 0},
        "regular_quadratic": {A: 1 + a * r**2, sp.diff(A, r): 2 * a * r, sp.diff(A, r, 2): 2 * a},
        "linear_center": {A: 1 + b * r, sp.diff(A, r): b, sp.diff(A, r, 2): 0},
        "wrl": {A: 1 - r / X, sp.diff(A, r): -1 / X, sp.diff(A, r, 2): 0},
    }

    controls = {
        name: {
            "R": str(clean(scalar.subs(values))),
            "Ricci2": str(clean(ricci_squared.subs(values))),
            "K": str(clean(kretschmann.subs(values))),
            "C2": str(clean(weyl_squared.subs(values))),
        }
        for name, values in substitutions.items()
    }

    constant_reversal_difference = clean(
        scalar.subs(substitutions["constant"])
        - scalar.subs(substitutions["constant"]).subs(a, 1 / a)
    )

    # In the C2 Taylor class A=A0+A1*r+A2*r^2/2+o(r^2), bounded K forces A0=1,A1=0.
    A0, A1, A2 = sp.symbols("A0 A1 A2", real=True)
    taylor_A = A0 + A1 * r + A2 * r**2 / 2
    taylor_K = clean(expected_kretschmann.subs({
        A: taylor_A,
        sp.diff(A, r): sp.diff(taylor_A, r),
        sp.diff(A, r, 2): sp.diff(taylor_A, r, 2),
    }))
    regular_center_K = clean(sp.limit(taylor_K.subs({A0: 1, A1: 0}), r, 0, dir="+"))

    # Reciprocal coframe and null readout.
    coframe = sp.diag(c * sp.sqrt(A), 1 / sp.sqrt(A), r, r * sp.sin(theta))
    eta = sp.diag(-1, 1, 1, 1)
    rebuilt_metric = clean(coframe.T * eta * coframe)
    determinant = clean(metric.det())
    coordinate_null_speed_squared = clean(-metric[0, 0] / metric[1, 1])
    local_null_speed_squared = clean(
        (coordinate_null_speed_squared / A) / A
    )  # (dell/dtau)^2=(dr^2/A)/(A dt^2)
    Apos, rpos, spos = sp.symbols("Apos rpos spos", positive=True)
    regular_point_diagonal = (-c**2 * Apos, 1 / Apos, rpos**2, rpos**2 * spos**2)
    angular_lower_remainder = clean(
        expected_kretschmann - 4 * (1 - A) ** 2 / r**4
    )

    checks = {
        "inverse_exact": clean(metric * inverse - sp.eye(4)) == sp.zeros(4),
        "coframe_rebuilds_metric": clean(rebuilt_metric - metric) == sp.zeros(4),
        "determinant_phi_independent": determinant == -c**2 * r**4 * sp.sin(theta) ** 2,
        "finite_A_signature_lorentzian": [entry.is_positive for entry in regular_point_diagonal]
        == [False, True, True, True],
        "scalar_formula": clean(scalar - expected_scalar) == 0,
        "kretschmann_formula": clean(kretschmann - expected_kretschmann) == 0,
        "weyl_formula": clean(weyl_squared - expected_weyl) == 0,
        "flat_control": all(value == "0" for value in controls["flat"].values()),
        "constant_imbalance_curved_unless_balanced": controls["constant"]["R"] == "-2*(a - 1)/r**2"
        and controls["constant"]["K"] == "4*(a - 1)**2/r**4",
        "regular_quadratic_center_finite": controls["regular_quadratic"] == {
            "R": "-12*a", "Ricci2": "36*a**2", "K": "24*a**2", "C2": "0"
        },
        "linear_center_singular": controls["linear_center"]["R"] == "-6*b/r"
        and controls["linear_center"]["K"] == "8*b**2/r**2",
        "wrl_control": controls["wrl"] == {
            "R": "6/(X*r)", "Ricci2": "10/(X**2*r**2)",
            "K": "8/(X**2*r**2)", "C2": "0"
        },
        "wrl_wall_invariants_finite": clean(scalar.subs(substitutions["wrl"]).subs(r, X) - 6 / X**2) == 0
        and clean(kretschmann.subs(substitutions["wrl"]).subs(r, X) - 8 / X**4) == 0,
        "constant_phi_reversal_not_generic_symmetry": constant_reversal_difference != 0
        and clean(constant_reversal_difference.subs(a, 1)) == 0,
        "regular_center_taylor_limit": regular_center_K == 6 * A2**2,
        "coordinate_null_slope": coordinate_null_speed_squared == c**2 * A**2,
        "local_normalized_null_speed": local_null_speed_squared == c**2,
        "angular_term_is_exact_nonnegative_K_lower_bound": clean(
            angular_lower_remainder
            - sp.diff(A, r, 2) ** 2
            - 4 * sp.diff(A, r) ** 2 / r**2
        ) == 0,
    }
    if not all(checks.values()):
        raise AssertionError([name for name, value in checks.items() if not value])

    result = {
        "schema": "udt-reciprocity-regime-angular-center-production-1.0",
        "status": "PASS",
        "sympy_version": sp.__version__,
        "checks": checks,
        "counts": {"exact_checks": len(checks), "profile_controls": len(controls)},
        "general_formulas": {
            "R": str(expected_scalar),
            "Ricci2": str(ricci_squared),
            "K": str(expected_kretschmann),
            "C2": str(expected_weyl),
            "det_g": str(determinant),
            "coordinate_radial_null_speed_squared": str(coordinate_null_speed_squared),
            "local_radial_null_speed_squared": str(local_null_speed_squared),
        },
        "orthonormal_curvature_motifs_up_to_convention": {
            "clock_depth": "A''/2",
            "clock_angular_pair": "A'/(2r)",
            "depth_angular_pair": "-A'/(2r)",
            "angular_intrinsic": "(1-A)/r^2",
        },
        "controls": controls,
        "regular_center": {
            "class": "C2_TAYLOR_STATIC_SPHERICAL_AREAL",
            "necessary_and_sufficient_for_bounded_K": "A(0)=1 AND A'(0)=0 WITH FINITE A''(0)",
            "phi_translation": "phi(0)=0 AND phi'(0)=0; phi=O(r^2)",
            "K_limit": str(regular_center_K),
        },
        "regime_rulings": {
            "finite_phi_A_positive": "LORENTZIAN_NONDEGENERATE__LOCAL_FRAME_TYPE_UNCHANGED",
            "A_to_zero_finite_radius": "STATIC_CHART_LIMIT__REGULARITY_DEPENDS_ON_DERIVATIVES_AND_EXTENSION",
            "wrl_A_to_zero": "REGULAR_HORIZON_CONTROL__STATIC_OBSERVER_FRAME_TERMINATES__LOCAL_LORENTZIAN_EXTENSION_EXISTS",
            "A_to_infinity_finite_radius": "CURVATURE_SINGULAR_FROM_ANGULAR_TERM",
            "areal_center": "REGULARITY_FORCES_A_TO_ONE_AND_PHI_TO_ZERO_IN_STATED_CLASS",
            "phi_reversal": "NOT_A_GENERIC_SYMMETRY_OF_COMPLETE_STATIC_SPHERICAL_METRIC",
        },
        "maximum_conclusion": "NO_INVARIANT_FINITE_PHI_FRAME_FLIP_IN_STATIC_SPHERICAL_CLASS__ANGULAR_SECTOR_FORCES_RECIPROCAL_BALANCE_AT_A_REGULAR_AREAL_CENTER__TIME_LIVE_AND_MICRO_SCALE_REMAIN_OPEN",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
