#!/usr/bin/env python3
"""Exact algebra for the time-live spherical areal-polarization audit."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def clean(value):
    if isinstance(value, sp.MatrixBase):
        return value.applyfunc(lambda entry: sp.factor(sp.trigsimp(sp.simplify(entry))))
    return sp.factor(sp.trigsimp(sp.simplify(value)))


def coordinate_tensors(metric: sp.Matrix, coords: tuple[sp.Symbol, ...]):
    dimension = len(coords)
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
    riemann_down = [[[[
        clean(sum(metric[rho, lam] * riemann_up[lam][sigma][mu][nu] for lam in range(dimension)))
        for nu in range(dimension)] for mu in range(dimension)] for sigma in range(dimension)] for rho in range(dimension)]
    ricci = sp.MutableDenseMatrix(dimension, dimension, [0] * dimension**2)
    for sigma in range(dimension):
        for nu in range(dimension):
            ricci[sigma, nu] = clean(sum(riemann_up[rho][sigma][rho][nu] for rho in range(dimension)))
    scalar = clean(sum(inverse[i, j] * ricci[i, j] for i in range(dimension) for j in range(dimension)))
    return inverse, gamma, riemann_down, ricci, scalar


def main() -> None:
    N, L = sp.symbols("N L", positive=True)
    beta, RT, Rr = sp.symbols("beta R_T R_r", real=True)
    R = sp.symbols("R", positive=True)

    h = sp.Matrix([
        [-N**2 + L**2 * beta**2, L**2 * beta],
        [L**2 * beta, L**2],
    ])
    h_inverse = clean(h.inv())
    expected_inverse = sp.Matrix([
        [-1 / N**2, beta / N**2],
        [beta / N**2, 1 / L**2 - beta**2 / N**2],
    ])
    dR = sp.Matrix([RT, Rr])
    grad_R = clean(h_inverse * dR)
    X = clean((dR.T * h_inverse * dR)[0])
    expected_X = clean(Rr**2 / L**2 - (RT - beta * Rr) ** 2 / N**2)

    epsilon_up = sp.Matrix([[0, 1 / (N * L)], [-1 / (N * L), 0]])
    K = clean(epsilon_up * dR)
    K_dot_grad = clean((K.T * h * grad_R)[0])
    K_norm = clean((K.T * h * K)[0])
    grad_norm = clean((grad_R.T * h * grad_R)[0])

    coframe = sp.Matrix([[N, 0], [L * beta, L]])
    eta2 = sp.diag(-1, 1)
    rebuilt_h = clean(coframe.T * eta2 * coframe)

    # Exact causal-branch witnesses with N=L=1,beta=0.
    branch_controls = {}
    for name, values in {
        "SPACELIKE_GRADIENT": {RT: 0, Rr: 2, N: 1, L: 1, beta: 0},
        "NULL_GRADIENT": {RT: 1, Rr: 1, N: 1, L: 1, beta: 0},
        "TIMELIKE_GRADIENT": {RT: 2, Rr: 1, N: 1, L: 1, beta: 0},
    }.items():
        branch_controls[name] = {
            "X": str(clean(X.subs(values))),
            "grad_norm": str(clean(grad_norm.subs(values))),
            "K_norm": str(clean(K_norm.subs(values))),
            "dot": str(clean(K_dot_grad.subs(values))),
            "grad": [str(clean(entry.subs(values))) for entry in grad_R],
            "K": [str(clean(entry.subs(values))) for entry in K],
        }

    # Null expansion product for l=(u+n)/sqrt(2), k=(u-n)/sqrt(2).
    uR, nR = sp.symbols("uR nR", real=True)
    ell_R = (uR + nR) / sp.sqrt(2)
    ingoing_R = (uR - nR) / sp.sqrt(2)
    X_frame = -uR**2 + nR**2
    expansion_product = clean((2 * ell_R / R) * (2 * ingoing_R / R))

    # Warped-product curvature motifs derived in a flat normal base chart.
    T, radius, theta, azimuth = sp.symbols("T radius theta azimuth", real=True)
    S = sp.Function("S")(T, radius)
    warped_metric = sp.diag(-1, 1, S**2, S**2 * sp.sin(theta) ** 2)
    _, _, warped_riemann, _, warped_scalar = coordinate_tensors(
        warped_metric, (T, radius, theta, azimuth)
    )
    X_warp = -sp.diff(S, T) ** 2 + sp.diff(S, radius) ** 2
    angular_section = clean(
        warped_riemann[2][3][2][3] / (warped_metric[2, 2] * warped_metric[3, 3])
    )
    mixed_tt = clean(warped_riemann[0][2][0][2] / warped_metric[2, 2])
    mixed_tr = clean(warped_riemann[0][2][1][2] / warped_metric[2, 2])
    mixed_rr = clean(warped_riemann[1][2][1][2] / warped_metric[2, 2])

    # Center Taylor gate from the angular sectional curvature.
    X0, X1, X2, rho = sp.symbols("X0 X1 X2 rho", real=True)
    X_taylor = X0 + X1 * rho + X2 * rho**2 / 2
    angular_taylor = clean((1 - X_taylor) / rho**2)
    center_limit = clean(sp.limit(angular_taylor.subs({X0: 1, X1: 0}), rho, 0, dir="+"))

    # Static recovery.
    A = sp.symbols("A", positive=True)
    static_h = sp.diag(-A, 1 / A)
    static_X = clean((sp.Matrix([0, 1]).T * static_h.inv() * sp.Matrix([0, 1]))[0])
    phi_static = clean(-sp.log(static_X) / 2)

    # General orthogonal areal form and same-X lapse/threading counterfamily.
    F = sp.Function("F")(radius)
    Xfun = sp.Function("X")(T, radius)
    areal_h = sp.diag(-F**2 * Xfun, 1 / Xfun)
    areal_X = clean((sp.Matrix([0, 1]).T * areal_h.inv() * sp.Matrix([0, 1]))[0])

    lapse_metric = sp.diag(-F**2, 1, radius**2, radius**2 * sp.sin(theta) ** 2)
    _, _, _, _, lapse_scalar = coordinate_tensors(lapse_metric, (T, radius, theta, azimuth))
    q = sp.symbols("q", real=True, nonzero=True)
    lapse_scalar_flat = clean(lapse_scalar.subs({F: 1, sp.diff(F, radius): 0, sp.diff(F, radius, 2): 0}))
    lapse_scalar_exp = clean(lapse_scalar.subs({
        F: sp.exp(q * radius),
        sp.diff(F, radius): q * sp.exp(q * radius),
        sp.diff(F, radius, 2): q**2 * sp.exp(q * radius),
    }))

    # Local common-scale behavior of areal X under g->Omega^2 g and R->Omega R.
    Omega = sp.symbols("Omega", positive=True)
    dOmega_T, dOmega_r = sp.symbols("Omega_T Omega_r", real=True)
    scaled_dR = sp.Matrix([Omega * RT + R * dOmega_T, Omega * Rr + R * dOmega_r])
    scaled_X = clean((scaled_dR.T * (h_inverse / Omega**2) * scaled_dR)[0])
    dlogOmega = sp.Matrix([dOmega_T / Omega, dOmega_r / Omega])
    expected_scaled_X = clean(
        X
        + 2 * R * (dR.T * h_inverse * dlogOmega)[0]
        + R**2 * (dlogOmega.T * h_inverse * dlogOmega)[0]
    )

    checks = {
        "base_inverse_exact": clean(h_inverse - expected_inverse) == sp.zeros(2),
        "base_determinant": clean(h.det() + N**2 * L**2) == 0,
        "coframe_rebuilds_shift_metric": clean(rebuilt_h - h) == sp.zeros(2),
        "shift_complete_X": clean(X - expected_X) == 0,
        "areal_dual_orthogonal": K_dot_grad == 0,
        "areal_dual_opposite_norm": clean(K_norm + X) == 0,
        "gradient_norm_is_X": clean(grad_norm - X) == 0,
        "three_causal_branches": [branch_controls[key]["X"] for key in (
            "SPACELIKE_GRADIENT", "NULL_GRADIENT", "TIMELIKE_GRADIENT"
        )] == ["4", "0", "-3"],
        "null_branch_lines_collapse": branch_controls["NULL_GRADIENT"]["grad"]
        == ["-1", "1"] and branch_controls["NULL_GRADIENT"]["K"] == ["1", "-1"],
        "full_base_signature_independent_of_X": clean(rebuilt_h.det()) == -L**2 * N**2,
        "null_expansion_product": clean(expansion_product + 2 * X_frame / R**2) == 0,
        "angular_warped_curvature": clean(angular_section - (1 - X_warp) / S**2) == 0,
        "mixed_tt_warped_curvature": clean(mixed_tt + sp.diff(S, T, 2) / S) == 0,
        "mixed_tr_warped_curvature": clean(mixed_tr + sp.diff(S, T, radius) / S) == 0,
        "mixed_rr_warped_curvature": clean(mixed_rr + sp.diff(S, radius, 2) / S) == 0,
        "center_angular_limit": center_limit == -X2 / 2,
        "static_X_recovery": static_X == A,
        "static_phi_recovery": phi_static == -sp.log(A) / 2,
        "orthogonal_areal_form_retains_X": areal_X == Xfun,
        "same_X_flat_threading_control": lapse_scalar_flat == 0,
        "same_X_curved_threading_control": clean(
            lapse_scalar_exp + 2 * q**2 + 4 * q / radius
        ) == 0,
        "local_CSN_areal_X_transform": clean(scaled_X - expected_scaled_X) == 0,
        "constant_CSN_preserves_X": clean(scaled_X.subs({dOmega_T: 0, dOmega_r: 0}) - X) == 0,
    }
    if not all(checks.values()):
        raise AssertionError([name for name, value in checks.items() if not value])

    result = {
        "schema": "udt-timelive-spherical-areal-polarization-production-1.0",
        "status": "PASS",
        "sympy_version": sp.__version__,
        "checks": checks,
        "counts": {"exact_checks": len(checks), "causal_branch_controls": 3},
        "general_identities": {
            "det_h": str(clean(h.det())),
            "X_with_shift": str(X),
            "K_dot_gradR": str(K_dot_grad),
            "K_squared": str(K_norm),
            "null_expansion_product": str(expansion_product),
            "angular_sectional_curvature": str(angular_section),
            "mixed_tt": str(mixed_tt),
            "mixed_tr": str(mixed_tr),
            "mixed_rr": str(mixed_rr),
            "same_X_lapse_scalar_general": str(lapse_scalar),
            "same_X_lapse_scalar_exp": str(lapse_scalar_exp),
            "scaled_X": str(scaled_X),
        },
        "causal_branches": branch_controls,
        "rulings": {
            "X_positive": "GRAD_R_SPACELIKE__AREAL_DUAL_TIMELIKE__CANONICAL_LOCAL_CLOCK_RADIAL_LINES",
            "X_zero": "AREAL_LINES_COLLAPSE_TO_ONE_NULL_LINE__NORMALIZED_POLARIZATION_SINGULAR",
            "X_negative": "GRAD_R_TIMELIKE__AREAL_DUAL_SPACELIKE__CAUSAL_ROLES_EXCHANGED",
            "full_metric_signature": "LORENTZIAN_THROUGH_ALL_THREE_REGULAR_BRANCHES",
            "regular_center": "BOUNDED_ANGULAR_CURVATURE_REQUIRES_X_TO_ONE_PLUS_O_OF_R_SQUARED",
            "phi_areal": "SCALAR_AND_STATIC_MATCH_ON_X_POSITIVE__CONDITIONAL_IDENTIFICATION__DIVERGES_AT_X_ZERO__REQUIRES_SIGN_BRANCH_FOR_X_NEGATIVE",
            "complete_base_metric": "NOT_FIXED_BY_X__POSITIVE_CLOCK_THREADING_FACTOR_F_SURVIVES",
            "common_scale": "X_INVARIANT_UNDER_CONSTANT_COMMON_SCALE__NOT_UNDER_GENERAL_LOCAL_CSN_WITH_R_TRANSFORMED",
        },
        "maximum_conclusion": "ANGULAR_AREAL_GEOMETRY_DERIVES_SOLUTION_SPECIFIC_TIME_LIVE_CLOCK_RADIAL_LINES_AND_AN_X_ZERO_CAUSAL_ROLE_EXCHANGE__FULL_METRIC_SIGNATURE_DOES_NOT_FLIP__PHI_EXTENSION_AND_CLOCK_THREADING_REMAIN_CONDITIONAL",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
