#!/usr/bin/env python3
"""Exact symbolic G115 leading-jet derivation.

The script derives rather than inserts the regular-center null graph, pullback blocks,
affine radial tangent, optical coefficient, and source-boundary rank controls.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def trunc(expr: sp.Expr, var: sp.Symbol, order: int) -> sp.Expr:
    return sp.expand(sp.series(expr, var, 0, order).removeO())


def zero_through(expr: sp.Expr, var: sp.Symbol, order: int) -> bool:
    return sp.simplify(trunc(expr, var, order)) == 0


def main() -> None:
    T, R, lam = sp.symbols("T R lambda", real=True)
    n, nt, ell, ellt = sp.symbols("n n_T ell ell_T", real=True)
    b, bt, btt = sp.symbols("b b_T b_TT", real=True)
    q, qt = sp.symbols("q q_T", real=True)
    wx, wy = sp.symbols("w_x w_y", real=True)
    w2 = wx**2 + wy**2

    # FREE history/source jets at the central event. Higher radial jets remain remainders.
    nT = n + nt * T
    ellT = ell + ellt * T
    bT = b + bt * T + sp.Rational(1, 2) * btt * T**2
    qT = q + qt * T

    N = 1 + nT * R**2
    L = 1 + ellT * R**2
    beta = bT * R

    g2_exact = sp.Matrix(
        [
            [-N**2 + L**2 * beta**2, L**2 * beta],
            [L**2 * beta, L**2],
        ]
    )
    # Only the complete declared two-jet enters the connection calculation. Truncating before
    # contraction avoids spending time simplifying irrelevant higher-order rational functions.
    g2 = g2_exact.applyfunc(lambda x: trunc(x, R, 3))
    g2_inv = sp.Matrix(
        [
            [trunc(-1 / N**2, R, 3), trunc(beta / N**2, R, 3)],
            [
                trunc(beta / N**2, R, 3),
                trunc(1 / L**2 - beta**2 / N**2, R, 3),
            ],
        ]
    )

    # Outgoing null graph T(tau=0,R). The coefficients are solved from the null ODE.
    a2, a3 = sp.symbols("a2 a3", real=True)
    T_path_trial = R + a2 * R**2 + a3 * R**3
    null_slope = trunc(L / (N - L * beta), R, 4)
    slope_on_trial = trunc(null_slope.subs(T, T_path_trial), R, 3)
    ode_residual = trunc(sp.diff(T_path_trial, R) - slope_on_trial, R, 3)
    solved = sp.solve(
        [sp.expand(ode_residual).coeff(R, 1), sp.expand(ode_residual).coeff(R, 2)],
        [a2, a3],
        dict=True,
    )[0]
    T_path = sp.expand(T_path_trial.subs(solved))
    expected_T_path = R + b * R**2 / 2 + (b**2 + ell - n + bt) * R**3 / 3

    # Neighboring observer-time derivative at fixed R, derived from a2(tau)=b(tau)/2.
    T_tau = 1 + bt * R**2 / 2
    path_sub = {T: T_path}
    Np = trunc(N.subs(path_sub), R, 3)
    Lp = trunc(L.subs(path_sub), R, 3)
    betap = trunc(beta.subs(path_sub), R, 3)
    pp = trunc(null_slope.subs(path_sub), R, 3)

    gTTp = trunc((-N**2 + L**2 * beta**2).subs(path_sub), R, 3)
    gTRp = trunc((L**2 * beta).subs(path_sub), R, 3)
    gRRp = trunc((L**2).subs(path_sub), R, 3)

    h00 = trunc(gTTp * T_tau**2 + R**2 * w2, R, 3)
    h01 = trunc(T_tau * (gTTp * pp + gTRp), R, 3)
    h11 = trunc(gTTp * pp**2 + 2 * gTRp * pp + gRRp, R, 3)
    h01_identity = trunc(h01 + Lp * Np * T_tau, R, 3)

    # Fixed-label terminal readout. The orthogonal quotient removes the celestial-drift term.
    phi_pair = trunc(
        sp.Rational(1, 2) * (sp.log(-h01) - sp.log(-h00)), R, 3
    )
    h00_quotient = trunc(h00 - R**2 * w2, R, 3)
    phi_quotient = trunc(
        sp.Rational(1, 2) * (sp.log(-h01) - sp.log(-h00_quotient)), R, 3
    )
    kappa_pair = trunc(sp.Rational(1, 2) * sp.log(-h01), R, 3)
    beta_pair = trunc(h01 / h00, R, 3)

    expected_phi = (
        sp.Rational(1, 2)
        * (ell - n + b**2 - bt / 2 + w2)
        * R**2
    )
    expected_phi_quotient = (
        sp.Rational(1, 2) * (ell - n + b**2 - bt / 2) * R**2
    )
    expected_kappa = sp.Rational(1, 2) * (ell + n + bt / 2) * R**2

    X = trunc(1 / Lp**2 - betap**2 / Np**2, R, 3)
    phi_areal = trunc(-sp.Rational(1, 2) * sp.log(X), R, 3)
    expected_X = 1 - (2 * ell + b**2) * R**2
    expected_phi_areal = (ell + b**2 / 2) * R**2

    # Direct Christoffel construction of the affine radial tangent.
    coords = (T, R)
    Gamma = [[[(sp.Integer(0)) for _ in range(2)] for _ in range(2)] for _ in range(2)]
    for alpha in range(2):
        for mu in range(2):
            for nu in range(2):
                Gamma[alpha][mu][nu] = trunc(
                    sum(
                        g2_inv[alpha, delta]
                        * (
                            sp.diff(g2[delta, nu], coords[mu])
                            + sp.diff(g2[delta, mu], coords[nu])
                            - sp.diff(g2[mu, nu], coords[delta])
                        )
                        for delta in range(2)
                    )
                    / 2,
                    R,
                    2,
                )
    geodesic_combination = trunc(
        Gamma[1][0][0] * null_slope**2
        + 2 * Gamma[1][0][1] * null_slope
        + Gamma[1][1][1],
        R,
        2,
    )
    comb_path = trunc(geodesic_combination.subs(path_sub), R, 2)
    optical_A = sp.simplify(2 * ell + 2 * n + bt)
    expected_comb = optical_A * R

    k2 = sp.symbols("k2", real=True)
    KR_trial = 1 + k2 * R**2
    affine_residual = trunc(sp.diff(sp.log(KR_trial), R) + comb_path, R, 2)
    k2_solution = sp.solve(sp.expand(affine_residual).coeff(R, 1), k2)[0]
    KR = sp.expand(KR_trial.subs(k2, k2_solution))
    expected_KR = 1 - optical_A * R**2 / 2

    # Convert to affine distance and construct the vertex Jacobi/phase series.
    c3 = sp.symbols("c3", real=True)
    R_lam_trial = lam + c3 * lam**3
    kr_on_lam = trunc(KR.subs(R, R_lam_trial), lam, 4)
    affine_map_residual = trunc(sp.diff(R_lam_trial, lam) - kr_on_lam, lam, 3)
    c3_solution = sp.solve(sp.expand(affine_map_residual).coeff(lam, 2), c3)[0]
    R_lam = sp.expand(R_lam_trial.subs(c3, c3_solution))
    D = R_lam
    Ddot = sp.diff(D, lam)
    C = 1 - optical_A * lam**2 / 2
    Cdot = sp.diff(C, lam)
    P1 = sp.Matrix([[C, D], [Cdot, Ddot]])
    Omega1 = sp.Matrix([[0, 1], [-1, 0]])
    symplectic_residual = P1.T * Omega1 * P1 - Omega1
    symplectic_residual_truncated = symplectic_residual.applyfunc(
        lambda x: trunc(x, lam, 4)
    )
    jacobi_residual = trunc(sp.diff(D, lam, 2) + optical_A * D, lam, 3)

    # Source-frame frequency. q(T)R is a FREE smooth radial velocity relative to Eulerian flow.
    omega_euler = trunc(Np * pp * KR, R, 3)
    v_path = trunc(qT.subs(T, T_path) * R, R, 3)
    log_omega_source = trunc(
        sp.log(omega_euler)
        + sp.Rational(1, 2) * sp.log((1 - v_path) / (1 + v_path)),
        R,
        3,
    )
    expected_log_omega_source = (
        (b - q) * R
        + (b**2 / 2 - n + bt / 2 - qt) * R**2
    )

    # Full pullback and exact Schur complement at the retained order.
    H = sp.Matrix(
        [
            [h00, h01, R**2 * wx, R**2 * wy],
            [h01, h11, 0, 0],
            [R**2 * wx, 0, R**2, 0],
            [R**2 * wy, 0, 0, R**2],
        ]
    )
    pair = H[:2, :2]
    mixed = H[:2, 2:]
    angular = H[2:, 2:]
    schur = pair - mixed * (sp.eye(2) / R**2) * mixed.T
    schur_expected = sp.Matrix([[h00_quotient, h01], [h01, h11]])
    schur_residual = (schur - schur_expected).applyfunc(
        lambda x: trunc(x, R, 3)
    )

    # Exact source-boundary classification.
    hs, ht, hu, slope = sp.symbols("h_11 h_12 h_22 q_s", real=True)
    Hs = sp.Matrix([[hs, ht], [ht, hu]])
    rank_polynomial = sp.factor((Hs - slope * sp.eye(2)).det())

    # Residual areal-time slicing T'=T+a(T)R^2+O(R^4). Individual coefficients move;
    # the observable combinations below must not.
    a, at = sp.symbols("a a_T", real=True)
    gauge_map = {
        b: b + 2 * a,
        ell: ell - 2 * a * b - 2 * a**2,
        n: n + 2 * a * b + 2 * a**2 - at,
        bt: bt + 2 * at,
        q: q + 2 * a,
        qt: qt + 2 * at,
    }
    invariant_combinations = {
        "terminal_quotient": ell - n + b**2 - bt / 2,
        "areal": 2 * ell + b**2,
        "optical": 2 * ell + 2 * n + bt,
        "frequency_linear": b - q,
        "frequency_quadratic": b**2 / 2 - n + bt / 2 - qt,
    }
    gauge_residuals = {
        name: sp.expand(expr.xreplace(gauge_map) - expr)
        for name, expr in invariant_combinations.items()
    }

    checks = {
        "null_graph_coefficients": sp.simplify(T_path - expected_T_path) == 0,
        "null_pullback_h11": h11 == 0,
        "null_cross_identity": h01_identity == 0,
        "phi_pair_formula": sp.simplify(phi_pair - expected_phi) == 0,
        "phi_quotient_formula": sp.simplify(phi_quotient - expected_phi_quotient) == 0,
        "kappa_formula": sp.simplify(kappa_pair - expected_kappa) == 0,
        "areal_X_formula": sp.simplify(X - expected_X) == 0,
        "areal_phi_formula": sp.simplify(phi_areal - expected_phi_areal) == 0,
        "geodesic_combination": sp.simplify(comb_path - expected_comb) == 0,
        "affine_radial_tangent": sp.simplify(KR - expected_KR) == 0,
        "affine_radius_map": sp.simplify(R_lam - (lam - optical_A * lam**3 / 6)) == 0,
        "jacobi_equation_through_order": zero_through(jacobi_residual, lam, 3),
        "phase_symplectic_through_order": symplectic_residual_truncated == sp.zeros(2),
        "source_frequency_formula": sp.simplify(
            log_omega_source - expected_log_omega_source
        )
        == 0,
        "schur_reconstruction": schur_residual == sp.zeros(2),
        "rank_polynomial": rank_polynomial
        == sp.factor((hs - slope) * (hu - slope) - ht**2),
        "flat_control": all(
            sp.simplify(expr.subs({n: 0, ell: 0, b: 0, bt: 0, wx: 0, wy: 0}))
            == 0
            for expr in (phi_pair, phi_areal, optical_A)
        ),
        "static_reciprocal_control": sp.simplify(
            phi_pair.subs({n: -slope, ell: slope, b: 0, bt: 0, wx: 0, wy: 0})
            - slope * R**2
        )
        == 0,
        "celestial_drift_difference": sp.simplify(
            phi_pair - phi_quotient - w2 * R**2 / 2
        )
        == 0,
        "residual_areal_time_gauge_invariants": all(
            residual == 0 for residual in gauge_residuals.values()
        ),
    }

    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise SystemExit("FAIL: " + ", ".join(failed))

    result = {
        "status": "PASS",
        "declared_order": {
            "metric": "smooth central fixed-time two-jet",
            "terminal_scalars": "through R^2",
            "vertex_jacobi": "through lambda^3",
            "source_boundary_rank": "exact",
        },
        "derived": {
            "T_path": str(T_path),
            "T_tau": str(T_tau),
            "h00": str(h00),
            "h01": str(h01),
            "h11": str(h11),
            "phi_pair": str(phi_pair),
            "phi_orthogonal_quotient": str(phi_quotient),
            "kappa_pair": str(kappa_pair),
            "beta_pair": str(beta_pair),
            "X": str(X),
            "phi_areal": str(phi_areal),
            "affine_KR": str(KR),
            "optical_A": str(optical_A),
            "R_lambda": str(R_lam),
            "D_vertex": str(D),
            "Ddot_vertex": str(Ddot),
            "log_source_frequency_ratio": str(log_omega_source),
            "source_graph_rank_polynomial": str(rank_polynomial),
            "residual_time_gauge_invariants": {
                name: str(expr) for name, expr in invariant_combinations.items()
            },
        },
        "source_boundary_classification": {
            "point_event_noncaustic": 0,
            "point_event_vertical_caustic_with_nonzero_momentum": 2,
            "resolved_screen_phase_rank": "UNDEFINED_WITHOUT_PHASE_BOUNDARY",
            "graph_H_rank_2": "H=q_s I",
            "graph_H_rank_1": "det(H-q_s I)=0 and H!=q_s I",
            "graph_H_rank_0": "det(H-q_s I)!=0",
            "two_spherical_observer_planes": "rank 2 iff q_i=q_j, otherwise rank 0",
            "worldtube_zero_order_gate": "ray phase point must satisfy Khat_s=k_s before tangent rank is typed",
            "spherical_worldtube_after_zero_order_match": "rank 2 automatically",
        },
        "checks": checks,
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
