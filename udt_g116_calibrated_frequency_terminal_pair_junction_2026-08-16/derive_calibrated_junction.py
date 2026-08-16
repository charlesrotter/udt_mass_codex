#!/usr/bin/env python3
"""Exact symbolic derivation of the bounded G116 pair/frequency junction."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def trunc(expr: sp.Expr, var: sp.Symbol, order: int) -> sp.Expr:
    return sp.expand(sp.series(expr, var, 0, order).removeO())


def main() -> None:
    T, R = sp.symbols("T R", real=True)
    ell, n, b, bt, q, qt, w2 = sp.symbols("ell n b b_T q q_T w2", real=True)
    nt, ellt, btt = sp.symbols("n_T ell_T b_TT", real=True)
    a, at = sp.symbols("a a_T", real=True)

    # Reconstruct the G115 inputs from the raw metric rather than importing its saved formulas.
    nT = n + nt * T
    ellT = ell + ellt * T
    bT = b + bt * T + btt * T**2 / 2
    qT = q + qt * T
    N = 1 + nT * R**2
    L = 1 + ellT * R**2
    beta = bT * R
    null_slope = trunc(L / (N - L * beta), R, 4)
    a2, a3 = sp.symbols("a2 a3", real=True)
    path_trial = R + a2 * R**2 + a3 * R**3
    slope_trial = trunc(null_slope.subs(T, path_trial), R, 3)
    ode = trunc(sp.diff(path_trial, R) - slope_trial, R, 3)
    solution = sp.solve(
        [sp.expand(ode).coeff(R, 1), sp.expand(ode).coeff(R, 2)],
        [a2, a3],
        dict=True,
    )[0]
    path = sp.expand(path_trial.subs(solution))
    path_sub = {T: path}
    T_tau = 1 + bt * R**2 / 2
    pp = trunc(null_slope.subs(path_sub), R, 3)
    Np = trunc(N.subs(path_sub), R, 3)
    Lp = trunc(L.subs(path_sub), R, 3)
    betap = trunc(beta.subs(path_sub), R, 3)
    gTT = trunc((-N**2 + L**2 * beta**2).subs(path_sub), R, 3)
    gTR = trunc((L**2 * beta).subs(path_sub), R, 3)
    h00_quot = trunc(gTT * T_tau**2, R, 3)
    h00_fixed = trunc(h00_quot + w2 * R**2, R, 3)
    h01 = trunc(T_tau * (gTT * pp + gTR), R, 3)
    phi_quot_raw = trunc((sp.log(-h01) - sp.log(-h00_quot)) / 2, R, 3)
    phi_fixed_raw = trunc((sp.log(-h01) - sp.log(-h00_fixed)) / 2, R, 3)

    # Direct Christoffel reconstruction of the radial affine coefficient.
    g2 = sp.Matrix([
        [trunc(-N**2 + L**2 * beta**2, R, 3), trunc(L**2 * beta, R, 3)],
        [trunc(L**2 * beta, R, 3), trunc(L**2, R, 3)],
    ])
    g2_inv = sp.Matrix([
        [trunc(-1 / N**2, R, 3), trunc(beta / N**2, R, 3)],
        [trunc(beta / N**2, R, 3), trunc(1 / L**2 - beta**2 / N**2, R, 3)],
    ])
    coords = (T, R)
    gamma = [[[sp.Integer(0) for _ in range(2)] for _ in range(2)] for _ in range(2)]
    for aa in range(2):
        for mu in range(2):
            for nu in range(2):
                gamma[aa][mu][nu] = trunc(
                    sum(
                        g2_inv[aa, d]
                        * (sp.diff(g2[d, nu], coords[mu]) + sp.diff(g2[d, mu], coords[nu]) - sp.diff(g2[mu, nu], coords[d]))
                        for d in range(2)
                    ) / 2,
                    R,
                    2,
                )
    affine_combination = trunc(
        (
            gamma[1][0][0] * null_slope**2
            + 2 * gamma[1][0][1] * null_slope
            + gamma[1][1][1]
        ).subs(path_sub),
        R,
        2,
    )
    optical_raw = sp.simplify(affine_combination.coeff(R, 1))
    KR = 1 - optical_raw * R**2 / 2
    omega_euler = trunc(Np * pp * KR, R, 3)
    source_v = trunc(qT.subs(path_sub) * R, R, 3)
    zeta_raw = trunc(
        sp.log(omega_euler) + sp.log((1 - source_v) / (1 + source_v)) / 2,
        R,
        3,
    )

    # Raw coefficients independently registered by the G115 metric/query construction.
    p2_quot = sp.Rational(1, 2) * (ell - n + b**2 - bt / 2)
    p2_fixed = p2_quot + w2 / 2
    optical = 2 * ell + 2 * n + bt
    vrel = b - q
    dvrel = bt - qt
    zeta2 = b**2 / 2 - n + bt / 2 - qt

    phi_quot = p2_quot * R**2
    phi_fixed = p2_fixed * R**2
    zeta = vrel * R + zeta2 * R**2

    junction_quot = vrel * R + (p2_quot - optical / 4 + dvrel) * R**2
    junction_fixed = vrel * R + (
        p2_fixed - w2 / 2 - optical / 4 + dvrel
    ) * R**2

    # The pair-c calibration contributes exactly phi=-1/2 log(c_eff/c_E).
    log_ceff_quot = -2 * phi_quot
    log_ceff_fixed = -2 * phi_fixed
    junction_from_ceff_quot = (
        -log_ceff_quot / 2
        + vrel * R
        + (dvrel - optical / 4) * R**2
    )
    junction_from_ceff_fixed = (
        -log_ceff_fixed / 2
        + vrel * R
        + (dvrel - optical / 4 - w2 / 2) * R**2
    )

    # Frequency ratio rather than its logarithm, frozen through O(R^2).
    Z = trunc(sp.exp(zeta), R, 3)
    z_observed_if_frequency_query = sp.expand(Z - 1)
    z2 = sp.simplify(zeta2 + vrel**2 / 2)

    # Residual areal-time slicing inherited from G115.
    gauge_map = {
        b: b + 2 * a,
        ell: ell - 2 * a * b - 2 * a**2,
        n: n + 2 * a * b + 2 * a**2 - at,
        bt: bt + 2 * at,
        q: q + 2 * a,
        qt: qt + 2 * at,
    }
    invariants = {
        "terminal_p2_quotient": p2_quot,
        "terminal_p2_fixed_without_active_sky": p2_fixed - w2 / 2,
        "optical": optical,
        "relative_drift": vrel,
        "relative_drift_time_derivative": dvrel,
        "frequency_quadratic": zeta2,
        "frequency_ratio_quadratic": z2,
    }
    gauge_residuals = {
        name: sp.expand(expr.xreplace(gauge_map) - expr)
        for name, expr in invariants.items()
    }

    # Pure stationary reciprocal control: N=e^{-pR^2}, L=e^{+pR^2} at this order.
    p = sp.symbols("p", real=True)
    pure = {ell: p, n: -p, b: 0, bt: 0, q: 0, qt: 0, w2: 0}

    # Exact endpoint frequency composition on one supplied ray/covector calibration.
    omega_s, omega_m, omega_o = sp.symbols(
        "omega_s omega_m omega_o", positive=True
    )
    Z_sm = omega_s / omega_m
    Z_mo = omega_m / omega_o
    Z_so = omega_s / omega_o

    # Matched terminal state composition is separate and only conditional on common calibration.
    C_s, C_m, C_o = sp.symbols("C_s C_m C_o", positive=True)
    C_sm = C_m / C_s
    C_mo = C_o / C_m
    C_so = C_o / C_s

    # All continuous additive combinations of two already-descended scalar channels.
    alpha = sp.symbols("alpha", real=True)
    z1, z2s, ph1, ph2 = sp.symbols("zeta_1 zeta_2 phi_1 phi_2", real=True)
    delta_family = alpha * (z1 + z2s) + (1 - alpha) * (ph1 + ph2)
    delta_composed = (
        alpha * z1 + (1 - alpha) * ph1
        + alpha * z2s + (1 - alpha) * ph2
    )
    pure_family = sp.simplify((alpha * z1 + (1 - alpha) * ph1).subs(ph1, z1))

    checks = {
        "raw_metric_terminal_reconstruction": sp.simplify(phi_quot_raw - phi_quot) == 0,
        "raw_metric_fixed_label_reconstruction": sp.simplify(phi_fixed_raw - phi_fixed) == 0,
        "raw_metric_frequency_reconstruction": sp.simplify(zeta_raw - zeta) == 0,
        "raw_metric_optical_reconstruction": sp.simplify(optical_raw - optical) == 0,
        "junction_quotient": sp.simplify(zeta - junction_quot) == 0,
        "junction_fixed_label": sp.simplify(zeta - junction_fixed) == 0,
        "junction_from_ceff_quotient": sp.simplify(zeta - junction_from_ceff_quot) == 0,
        "junction_from_ceff_fixed": sp.simplify(zeta - junction_from_ceff_fixed) == 0,
        "frequency_ratio_series": sp.simplify(
            z_observed_if_frequency_query - (vrel * R + z2 * R**2)
        )
        == 0,
        "residual_slicing_invariants": all(x == 0 for x in gauge_residuals.values()),
        "pure_phi": sp.simplify(phi_quot.subs(pure) - p * R**2) == 0,
        "pure_zeta": sp.simplify(zeta.subs(pure) - p * R**2) == 0,
        "pure_optical_zero": sp.simplify(optical.subs(pure)) == 0,
        "pure_ceff_frequency": sp.simplify(
            log_ceff_quot.subs(pure) + 2 * zeta.subs(pure)
        )
        == 0,
        "frequency_composition": sp.simplify(Z_sm * Z_mo - Z_so) == 0,
        "frequency_reversal": sp.simplify(Z_sm * (omega_m / omega_s) - 1) == 0,
        "terminal_matched_composition": sp.simplify(C_sm * C_mo - C_so) == 0,
        "terminal_matched_reversal": sp.simplify(C_sm * (C_s / C_m) - 1) == 0,
        "normalized_additive_family": sp.simplify(delta_family - delta_composed) == 0,
        "family_pure_reduction": sp.simplify(pure_family - z1) == 0,
        "two_inequivalent_survivors": sp.simplify(
            (alpha * z1 + (1 - alpha) * ph1).subs(alpha, 1)
            - (alpha * z1 + (1 - alpha) * ph1).subs(alpha, 0)
            - (z1 - ph1)
        )
        == 0,
        "naive_sum_double_counts_pure_branch": sp.simplify(
            (z1 + ph1).subs(ph1, z1) - 2 * z1
        )
        == 0,
    }

    if not all(checks.values()):
        raise SystemExit("FAIL: " + ", ".join(k for k, v in checks.items() if not v))

    result = {
        "status": "PASS",
        "scope": "regular central spherical time-live metric/query two-jet through R^2",
        "derived": {
            "raw_null_path": str(path),
            "raw_terminal_depth": str(phi_quot_raw),
            "raw_fixed_label_depth": str(phi_fixed_raw),
            "raw_frequency_depth": str(zeta_raw),
            "raw_optical_coefficient": str(optical_raw),
            "phi_pair_quotient": str(phi_quot),
            "phi_pair_fixed_label": str(phi_fixed),
            "log_frequency_ratio": str(zeta),
            "relative_drift": str(vrel),
            "relative_drift_time_derivative": str(dvrel),
            "optical_coefficient": str(optical),
            "junction_quotient": str(junction_quot),
            "junction_fixed_label": str(junction_fixed),
            "frequency_ratio_Z": str(Z),
            "frequency_redshift_if_query_declares_it": str(z_observed_if_frequency_query),
            "continuous_normalized_combination_family": "delta_alpha=alpha*zeta+(1-alpha)*phi; conditional on both channels descending in one matched scalar system",
        },
        "classification": {
            "frequency_query": "canonical invariant ratio for a declared direct frequency-ratio query once source clock, observer clock, ray covector, normalization, and group law are supplied",
            "terminal_pair_query": "unique reciprocal imbalance once regular calibrated pair metric is supplied",
            "junction": "coefficient-free identity for the same G115 metric/query jet",
            "founding_only_selector": "NONUNIQUE on the full abstract two-channel additive group or a spanning realized image: composition/reversal/pure normalization leave alpha free",
            "registered_exp_phi_redshift": "exact only on the pure stationary reciprocal reduction or another branch where the correction vanishes",
        },
        "gauge_residuals": {k: str(v) for k, v in gauge_residuals.items()},
        "checks": checks,
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
