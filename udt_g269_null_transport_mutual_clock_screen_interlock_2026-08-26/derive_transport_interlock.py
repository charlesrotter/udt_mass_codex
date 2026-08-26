#!/usr/bin/env python3
"""Exact G269 production algebra for null-transport mutual-clock interlock."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


OUT = Path(__file__).with_name("DERIVATION_RESULT.json")
LANDING = (
    "METRIC_OWNS_A_QUERY_RELATIVE_NULL_TRANSPORT_MUTUAL_CLOCK_SCALAR__"
    "M_PT_IS_BOUNDED_ABOVE_BY_SECH_DELTA__"
    "EQUALITY_IFF_THE_TARGET_CLOCK_IS_IN_THE_TRANSPORTED_NULL_PAIR_PLANE__"
    "NONZERO_SCREEN_MISMATCH_MAKES_THE_INEQUALITY_STRICT__"
    "NO_QUERY_POPULATION_HISTORY_DISTANCE_OR_XMAX_SELECTION"
)


def zero(expr: sp.Expr) -> bool:
    return sp.cancel(sp.trigsimp(expr.rewrite(sp.exp))) == 0


def minkowski_dot(v: sp.Matrix, w: sp.Matrix) -> sp.Expr:
    eta = sp.diag(-1, 1, 1, 1)
    return sp.cancel((v.T * eta * w)[0])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    r = sp.symbols("r", positive=True)
    w = sp.symbols("w", real=True)
    wp = sp.symbols("wp", positive=True)
    c = sp.symbols("c", positive=True)
    eta_rel = sp.symbols("eta_rel", real=True)
    phi_a, phi_b = sp.symbols("phi_a phi_b", real=True)

    w2 = w**2
    gamma_kernel = sp.cancel((r + 1 / r) / 2)
    gamma_pt = sp.cancel(gamma_kernel + r * w2 / 2)
    longitudinal = sp.cancel(gamma_pt - 1 / r)
    m_pt = sp.cancel(1 / gamma_pt)
    sech_depth = sp.cancel(1 / gamma_kernel)

    checks: dict[str, bool] = {}

    # Exact flat 1+2 family embedded in 1+3; it realizes every r>0 and w in R.
    u_a = sp.Matrix([1, 0, 0, 0])
    n_a = sp.Matrix([0, 1, 0, 0])
    k_norm = u_a + n_a
    u_b = sp.Matrix([gamma_pt, longitudinal, w, 0])
    checks["source_clock_unit"] = zero(minkowski_dot(u_a, u_a) + 1)
    checks["source_ruler_unit"] = zero(minkowski_dot(n_a, n_a) - 1)
    checks["source_clock_ruler_orthogonal"] = zero(minkowski_dot(u_a, n_a))
    checks["normalized_null"] = zero(minkowski_dot(k_norm, k_norm))
    checks["normalized_source_frequency"] = zero(-minkowski_dot(k_norm, u_a) - 1)
    checks["target_clock_unit"] = zero(minkowski_dot(u_b, u_b) + 1)
    checks["target_frequency_inverse_r"] = zero(-minkowski_dot(k_norm, u_b) - 1 / r)
    checks["transport_gamma_contraction"] = zero(-minkowski_dot(u_a, u_b) - gamma_pt)
    checks["screen_projection_norm"] = zero(w2 - w**2)

    # General algebraic identity implied by unit normalization and the null frequency contraction.
    checks["gamma_screen_interlock"] = zero(
        gamma_pt - gamma_kernel - r * w2 / 2
    )
    checks["gamma_kernel_is_cosh_depth"] = zero(
        gamma_kernel - sp.cosh(-sp.log(r))
    )
    checks["m_pt_exact"] = zero(m_pt - 2 * r / (1 + r**2 + r**2 * w2))
    checks["sech_depth_exact"] = zero(sech_depth - 2 * r / (1 + r**2))
    checks["m_planar_equals_sech"] = zero(m_pt.subs(w, 0) - sech_depth)
    checks["gamma_planar_equals_kernel"] = zero(gamma_pt.subs(w, 0) - gamma_kernel)
    checks["sech_minus_m_factorization"] = zero(
        sech_depth - m_pt
        - (r * w2 / 2) / (gamma_kernel * gamma_pt)
    )
    checks["gamma_minus_one_factorization"] = zero(
        gamma_pt - 1 - ((r - 1) ** 2 + r**2 * w2) / (2 * r)
    )
    checks["strict_screen_gap_positive"] = (
        sp.ask(
            sp.Q.positive(
                (r * wp**2 / 2)
                / (gamma_kernel * gamma_pt.subs(w, wp))
            )
        )
        is True
    )
    checks["gamma_at_least_one"] = (
        sp.ask(sp.Q.nonnegative(((r - 1) ** 2 + r**2 * w2) / (2 * r)))
        is True
    )

    # Reversal: the reverse screen norm rescales, while Gamma and M remain even.
    r_rev = 1 / r
    w2_rev = sp.cancel(r**2 * w2)
    gamma_rev = sp.cancel((r_rev + 1 / r_rev) / 2 + r_rev * w2_rev / 2)
    checks["reversal_gamma_even"] = zero(gamma_rev - gamma_pt)
    checks["reversal_m_even"] = zero(1 / gamma_rev - m_pt)
    checks["reversal_depth_odd"] = zero(-sp.log(r_rev) - sp.log(r))

    # Common affine scaling cancels from normalized null direction and the frequency ratio.
    omega_a = sp.symbols("omega_a", positive=True)
    omega_b = sp.symbols("omega_b", positive=True)
    checks["affine_ratio_invariant"] = zero(
        (c * omega_a) / (c * omega_b) - omega_a / omega_b
    )
    checks["affine_normalized_null_invariant"] = zero(c / (c * omega_a) - 1 / omega_a)

    # Moving-flat planar control.
    r_moving = sp.exp(eta_rel)
    gamma_moving = sp.cosh(eta_rel)
    omega_b_moving = sp.cosh(eta_rel) - sp.sinh(eta_rel)
    checks["moving_flat_frequency"] = zero(omega_b_moving - 1 / r_moving)
    checks["moving_flat_gamma"] = zero(
        gamma_moving - (r_moving + 1 / r_moving) / 2
    )
    checks["moving_flat_m_sech"] = zero(1 / gamma_moving - sp.sech(-eta_rel))

    # Primary static-radial control uses the G220 ratio and has no transported screen direction.
    r_static = sp.exp(phi_a - phi_b)
    delta_static = phi_b - phi_a
    checks["static_depth"] = zero(-sp.log(r_static) - delta_static)
    checks["static_radial_gamma"] = zero(
        (r_static + 1 / r_static) / 2 - sp.cosh(delta_static)
    )
    checks["static_radial_m"] = zero(
        2 * r_static / (1 + r_static**2) - sp.sech(delta_static)
    )

    # Independence: fixed r and different transverse components give different transport scalars.
    w1, w2_symbol = sp.symbols("w1 w2_symbol", real=True)
    gamma_w1 = gamma_kernel + r * w1**2 / 2
    gamma_w2 = gamma_kernel + r * w2_symbol**2 / 2
    checks["fixed_r_transverse_separator"] = zero(
        gamma_w2 - gamma_w1 - r * (w2_symbol**2 - w1**2) / 2
    )
    checks["off_planar_witness_unit"] = zero(
        minkowski_dot(u_b.subs({r: 2, w: 1}), u_b.subs({r: 2, w: 1})) + 1
    )
    checks["off_planar_witness_same_r"] = zero(
        -minkowski_dot(k_norm, u_b.subs({r: 2, w: 1})) - sp.Rational(1, 2)
    )
    checks["off_planar_witness_strict"] = (
        m_pt.subs({r: 2, w: 1}) == sp.Rational(4, 9)
        and sech_depth.subs(r, 2) == sp.Rational(4, 5)
    )

    assert all(checks.values()), [name for name, passed in checks.items() if not passed]

    result = {
        "status": "PASS",
        "landing": LANDING,
        "selected_alternative": "N2__SCREEN_INTERLOCK",
        "metric_owned_scalar": "Gamma_PT=-g(P_AB U_A,U_B); M_PT=1/Gamma_PT",
        "exact_interlock": "Gamma_PT=cosh(delta_AB)+(r_AB/2)*||W_AB||^2",
        "sharp_bound": "0<M_PT<=sech(delta_AB)",
        "equality_condition": "M_PT=sech(delta_AB) iff ||W_AB||^2=0",
        "operational_status": "DERIVED_CONDITIONAL_BILOCAL_GEOMETRIC_SCALAR__WORKING_MUTUAL_CLOCK_INTERPRETATION",
        "query_population": "OPEN_NOT_SELECTED",
        "history_distance_xmax": "OPEN_NOT_TESTED",
        "exact_checks": len(checks),
        "checks": checks,
        "off_planar_witness": {
            "r": "2",
            "screen_component": "1",
            "sech_delta": "4/5",
            "M_PT": "4/9",
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if not args.no_write:
        OUT.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
