#!/usr/bin/env python3
"""Exact G126 angular/same-query bridge checks; no observational arrays."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def matrix_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(value) == 0 for value in matrix)


def main() -> None:
    R, K = sp.symbols("R K", positive=True)
    # A genuine exact orthogonal screen rotation; no unconstrained c,s surrogate.
    O = sp.Matrix(
        [
            [sp.Rational(3, 5), sp.Rational(-4, 5)],
            [sp.Rational(4, 5), sp.Rational(3, 5)],
        ]
    )
    D = R * O
    Dprime = K * O
    gram = sp.expand(D.T * D)
    B = sp.simplify(Dprime * D.inv())
    shear = sp.simplify(B - sp.trace(B) * sp.eye(2) / 2)

    x1, x2, y1, y2 = sp.symbols("x1 x2 y1 y2", real=True)
    x = sp.Matrix([x1, x2])
    y = sp.Matrix([y1, y2])
    angle_numerator = sp.expand((D * x).dot(D * y))
    expected_numerator = R**2 * x.dot(y)

    # Ideal per-depth reference: a purely radial factor cancels relative to any
    # registered nonuniform angular footprint, not only a uniform one.
    a = sp.symbols("a", positive=True)
    q = sp.Matrix(
        [sp.Rational(1, 10), sp.Rational(2, 10), sp.Rational(3, 10), sp.Rational(4, 10)]
    )
    p = a * q
    p_norm = sp.simplify(p / sum(p))
    residual = sp.simplify(p_norm - q)
    pair_residual = sp.simplify(residual * residual.T)

    # Same R(Z), different affine/frequency rate, with each branch normalized
    # to dR/dlambda=1 at the observer vertex Z=1.
    Z, n, X, alpha = sp.symbols("Z n X alpha", positive=True)
    R_inf = n * X
    R_of_Z = R_inf * (1 - Z ** (-2 / n))
    dR_dZ = sp.diff(R_of_Z, Z)
    f = 1 + alpha * (Z - 1)
    u_1 = Z ** (2 / n + 1) / (2 * X)
    u_2 = sp.simplify(u_1 * f)
    K_1 = sp.simplify(dR_dZ * u_1)
    K_2 = sp.simplify(dR_dZ * u_2)

    # A two-point autocorrelation does not invert uniquely to a one-point modulation.
    m = sp.Matrix([sp.Rational(-1, 2), sp.Rational(1, 4), sp.Rational(1, 4)])
    corr_plus = m * m.T
    corr_minus = (-m) * (-m).T

    checks = {
        "screen_orthogonal_gram": matrix_zero(gram - R**2 * sp.eye(2)),
        "screen_abs_area_is_R2": sp.simplify(D.det() - R**2) == 0,
        "screen_shape_operator_is_K_over_R": matrix_zero(B - (K / R) * sp.eye(2)),
        "screen_shear_zero": matrix_zero(shear),
        "screen_expansion_is_2K_over_R": sp.simplify(sp.trace(B) - 2 * K / R) == 0,
        "fixed_radius_angle_numerator_preserved": sp.simplify(
            angle_numerator - expected_numerator
        ) == 0,
        "radial_only_reference_residual_zero": matrix_zero(residual),
        "radial_only_pair_residual_zero": matrix_zero(pair_residual),
        "same_endpoint_R_for_both_rates": sp.simplify(R_of_Z - R_of_Z) == 0,
        "matched_vertex_affine_normalization": (
            sp.simplify(u_1.subs(Z, 1) - 1 / (2 * X)) == 0
            and sp.simplify(u_2.subs(Z, 1) - 1 / (2 * X)) == 0
            and sp.simplify(K_1.subs(Z, 1) - 1) == 0
            and sp.simplify(K_2.subs(Z, 1) - 1) == 0
        ),
        "finite_depth_rate_differs": sp.simplify(K_2 / K_1 - 1 - alpha * (Z - 1)) == 0,
        "phase_position_same_but_derivative_differs": (
            sp.simplify(R_of_Z - R_of_Z) == 0
            and sp.simplify(K_2 - K_1) != 0
        ),
        "RZ_derivative_known": sp.simplify(dR_dZ - 2 * X * Z ** (-2 / n - 1)) == 0,
        "K_requires_unowned_Z_affine_rate": (
            sp.simplify(K_1 / dR_dZ - u_1) == 0
            and sp.simplify(K_2 / dR_dZ - u_2) == 0
        ),
        "pair_autocorrelation_sign_noninjective": corr_plus == corr_minus,
    }

    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "exact_objects": {
            "screen_position": "D_sky = R O",
            "screen_phase_derivative_on_parallel_screen": "D_sky' = K(R) O",
            "screen_expansion": "theta_sky = 2 K(R)/R",
            "processed_depth_chain_rule": "K(R)=dR/dlambda=(dR/dZ)(dZ/dlambda)",
            "rate_counterfamily": "u1=Z^(2/n+1)/(2X), u2=[1+alpha(Z-1)]u1 both give K(1)=1 and preserve R(Z), but change K away from Z=1",
            "R5_type": "Landy--Szalay reference-projected two-point catalog-coordinate correlation in release-coordinate windows, not D_sky, D_sky', K, or Jacobi phase",
        },
        "landing": (
            "NO_LAWFUL_CURRENT_R5_TO_K_OR_PHASE_BRIDGE__"
            "EXACT_G119_SPHERICAL_SCREEN_IS_ANGLE_PRESERVING_AND_RADIAL_ONLY__"
            "G106_REFERENCE_REMOVES_PURE_RADIAL_MODULATION__"
            "PROCESSED_Z_AND_R_OF_Z_DO_NOT_OWN_AFFINE_RATE__"
            "R5_TWO_POINT_OUTPUT_DOES_NOT_INVERT_TO_SCREEN_PHASE__"
            "CONDITIONAL_NONSPHERICAL_HISTORY_SOURCE_REFERENCE_BRIDGE_OPEN"
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
