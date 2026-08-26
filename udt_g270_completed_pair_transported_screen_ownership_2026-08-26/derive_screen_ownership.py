#!/usr/bin/env python3
"""Exact G270 completed-pair versus transported-screen derivation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "DERIVATION_RESULT.json"
LANDING = (
    "FULL_SUPPLIED_REALIZATION_EVALUATES_TRANSPORTED_SCREEN_MISMATCH__"
    "COMPLETED_PAIR_DUAL_RECIPROCITY_NORMALIZES_ONLY_THE_INTRINSIC_PULLBACK__"
    "EXACT_SAME_PULLBACK_TILTED_NULL_RIBBONS_HAVE_DIFFERENT_W__"
    "NO_UNIVERSAL_W_VALUE_POPULATION_HISTORY_DISTANCE_OR_XMAX_SELECTION"
)


def mdot(x: sp.Matrix, y: sp.Matrix) -> sp.Expr:
    return sp.expand(-x[0] * y[0] + x[1] * y[1] + x[2] * y[2])


def zero(expr: sp.Expr) -> bool:
    return sp.simplify(expr) == 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    r = sp.symbols("r", positive=True)
    w = sp.symbols("w", real=True)
    lam, tau = sp.symbols("lam tau", real=True)

    u_a = sp.Matrix([1, 0, 0])
    n_a = sp.Matrix([0, 1, 0])
    e_screen = sp.Matrix([0, 0, 1])
    k = sp.Matrix([1, 1, 0])

    gamma = (r + 1 / r + r * w**2) / 2
    longitudinal = gamma - 1 / r
    u = sp.Matrix([gamma, longitudinal, w])
    omega = 1 / r
    k_normalized = r * k
    n = k_normalized - u
    w_vec = u - gamma * u_a - longitudinal * n_a

    h = sp.Matrix([
        [mdot(u, u), mdot(u, k)],
        [mdot(k, u), mdot(k, k)],
    ])
    h_expected = sp.Matrix([[-1, -1 / r], [-1 / r, 0]])
    beta = sp.simplify(h[0, 1] / h[0, 0])
    l_sigma_sq = sp.simplify(h[1, 1] - h[0, 1] ** 2 / h[0, 0])
    m = 1 / r
    h_completed = sp.Matrix([
        [h[0, 0], h[0, 1] / m],
        [h[1, 0] / m, h[1, 1] / m**2],
    ])
    h_completed_expected = sp.Matrix([[-1, -1], [-1, 0]])

    gamma_pt = -mdot(u_a, u)
    m_pt = sp.simplify(1 / gamma_pt)
    sech_depth = sp.simplify(2 * r / (1 + r**2))
    screen_norm = mdot(w_vec, w_vec)

    u_planar = u.subs(w, 0)
    u_tilted = u.subs(w, 1)
    h_planar = h.subs(w, 0)
    h_tilted = h.subs(w, 1)

    # Smooth nonconstant ribbon control: r(lambda)=1+lambda and w(lambda)=lambda.
    r_l = 1 + lam
    w_l = lam
    u_l = sp.simplify(u.subs({r: r_l, w: w_l}))
    du_l = u_l.diff(lam)
    f_tau = u_l
    f_lam = k + tau * du_l
    h_ribbon = sp.Matrix([
        [mdot(f_tau, f_tau), mdot(f_tau, f_lam)],
        [mdot(f_lam, f_tau), mdot(f_lam, f_lam)],
    ])
    h_ribbon_axis = sp.simplify(h_ribbon.subs(tau, 0))
    det_ribbon = sp.factor(h_ribbon.det())

    checks: dict[str, bool] = {}
    checks["source_clock_unit"] = zero(mdot(u_a, u_a) + 1)
    checks["source_ruler_unit"] = zero(mdot(n_a, n_a) - 1)
    checks["source_pair_orthogonal"] = zero(mdot(u_a, n_a))
    checks["affine_null_tangent"] = zero(mdot(k, k))
    checks["target_clock_unit"] = zero(mdot(u, u) + 1)
    checks["target_frequency"] = zero(-mdot(k, u) - omega)
    checks["target_ruler_unit"] = zero(mdot(n, n) - 1)
    checks["target_pair_orthogonal"] = zero(mdot(u, n))
    checks["target_normalized_null"] = zero(mdot(k_normalized, k_normalized))
    checks["target_null_clock_normalization"] = zero(-mdot(u, k_normalized) - 1)
    checks["target_null_frame_sum"] = all(zero(x) for x in k_normalized - u - n)
    checks["screen_projection_vector"] = all(zero(x) for x in w_vec - w * e_screen)
    checks["screen_projection_norm"] = zero(screen_norm - w**2)
    checks["transport_gamma"] = zero(gamma_pt - gamma)
    checks["g269_interlock"] = zero(gamma_pt - (r + 1 / r) / 2 - r * screen_norm / 2)
    checks["intrinsic_pullback"] = all(zero(x) for x in h - h_expected)
    checks["intrinsic_pullback_det"] = zero(h.det() + 1 / r**2)
    checks["intrinsic_pullback_w_blind"] = all(zero(sp.diff(x, w)) for x in h)
    checks["completed_beta"] = zero(beta - 1 / r)
    checks["completed_ruler_square"] = zero(l_sigma_sq - 1 / r**2)
    checks["completed_density"] = zero(m**2 + h.det())
    checks["completed_metric"] = all(
        zero(x) for x in h_completed - h_completed_expected
    )
    checks["completed_det_one"] = zero(h_completed.det() + 1)
    checks["completed_metric_r_blind"] = all(zero(sp.diff(x, r)) for x in h_completed)
    checks["completed_metric_w_blind"] = all(zero(sp.diff(x, w)) for x in h_completed)
    checks["same_pullback_planar_tilted"] = all(zero(x) for x in h_planar - h_tilted)
    checks["different_ambient_clocks"] = any(
        not zero(x) for x in u_planar - u_tilted
    )
    checks["different_screen_mismatch"] = (
        screen_norm.subs(w, 0) == 0 and screen_norm.subs(w, 1) == 1
    )
    checks["fixed_r_different_transport_readout"] = (
        m_pt.subs({r: 2, w: 0}) == sp.Rational(4, 5)
        and m_pt.subs({r: 2, w: 1}) == sp.Rational(4, 9)
    )
    checks["planar_sech"] = zero(m_pt.subs(w, 0) - sech_depth)
    checks["ribbon_clock_unit"] = zero(mdot(u_l, u_l) + 1)
    checks["ribbon_clock_derivative_orthogonal"] = zero(mdot(u_l, du_l))
    checks["ribbon_frequency_derivative"] = zero(mdot(k, du_l) - 1 / r_l**2)
    checks["ribbon_axis_pullback"] = all(
        zero(x) for x in h_ribbon_axis - h_expected.subs(r, r_l)
    )
    checks["ribbon_axis_regular"] = zero(h_ribbon_axis.det() + 1 / r_l**2)
    checks["ribbon_local_continuity"] = zero(det_ribbon.subs(tau, 0) + 1 / r_l**2)

    assert all(checks.values()), [name for name, passed in checks.items() if not passed]

    result = {
        "status": "PASS",
        "landing": LANDING,
        "selected_alternative": (
            "C__REALIZATION_EVALUATES_W__INTRINSIC_COMPLETED_PAIR_DOES_NOT_SELECT_IT"
        ),
        "ownership": {
            "full_supplied_realization": "EVALUATES_W_UNIQUELY",
            "intrinsic_completed_pair_metric": "DOES_NOT_DETERMINE_W",
            "completed_pair_dual_reciprocity": "DOES_NOT_SELECT_W",
        },
        "same_pullback_family": (
            "h_sigma=[[-1,-1/r],[-1/r,0]] and h_s=[[-1,-1],[-1,0]] for every real w"
        ),
        "transported_mismatch": "||W||^2=w^2",
        "g269_interlock": "Gamma_PT=cosh(delta)+(r/2)*||W||^2",
        "fixed_r_separator": {
            "r": "2",
            "planar_W2": "0",
            "planar_M_PT": "4/5",
            "tilted_W2": "1",
            "tilted_M_PT": "4/9",
            "intrinsic_pullback_equal": True,
        },
        "smooth_ribbon": {
            "r(lambda)": "1+lambda",
            "w(lambda)": "lambda",
            "axis_determinant": "-1/(1+lambda)^2",
            "local_regular_neighborhood": "DERIVED_BY_CONTINUITY_ABOUT_TAU_ZERO",
        },
        "w_is_jacobi_screen": False,
        "query_population": "OPEN_NOT_SELECTED",
        "history_distance_xmax": "OPEN_NOT_TESTED",
        "exact_checks": len(checks),
        "checks": checks,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if not args.no_write:
        OUT.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
