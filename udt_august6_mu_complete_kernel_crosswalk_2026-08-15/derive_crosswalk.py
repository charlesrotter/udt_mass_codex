#!/usr/bin/env python3
"""Exact symbolic derivation for the August-6 mu / modern-kernel crosswalk."""

from __future__ import annotations

import json

import sympy as sp


def is_zero_matrix(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def main() -> None:
    a, r, s, mu, lam = sp.symbols("a r s mu lam", nonzero=True, real=True)
    eta3 = sp.diag(-1, 1, 1)

    # August upper comparison arrow and its metric adjoint/lower dual.
    upper = sp.Matrix([[a, 0, mu], [0, r, 0], [0, 0, s]])
    lower = sp.simplify(eta3.inv() * upper.T * eta3)
    expected_lower = sp.Matrix([[a, 0, 0], [0, r, 0], [-mu, 0, s]])
    upper_strain = sp.simplify(lower * upper)
    lower_strain = sp.simplify(upper * lower)
    similarity_residual = sp.simplify(lower_strain - upper * upper_strain * upper.inv())

    # One-screen restriction of the modern lower-block coframe chart.
    base = sp.diag(a, r)
    screen = sp.Matrix([[s]])
    modern_s = sp.Matrix([[-mu / s, 0]])
    zero_21 = sp.zeros(2, 1)
    modern_lower = base.row_join(zero_21).col_join((screen * modern_s).row_join(screen))

    # Exact strain data, with the founded reciprocal condition a=1/r imposed only at readout.
    cp_upper = sp.Poly(upper_strain.charpoly(lam).as_expr(), lam)
    cp_lower = sp.Poly(lower_strain.charpoly(lam).as_expr(), lam)
    reciprocal_trace = sp.simplify(sp.trace(upper_strain).subs(a, 1 / r))
    reciprocal_det = sp.simplify(upper_strain.det().subs(a, 1 / r))
    reciprocal_inv2 = sp.simplify(
        (
            sp.trace(upper_strain) ** 2
            - sp.trace(upper_strain * upper_strain)
        ).subs(a, 1 / r)
        / 2
    )

    # Base-aligned modern pair pullback J=[I;0].
    eta2 = sp.diag(-1, 1)
    y = sp.eye(2)
    z = sp.zeros(1, 2)
    h = sp.simplify(y.T * base.T * eta2 * base * y + (modern_s * y + z).T * screen.T * screen * (modern_s * y + z))
    expected_h = sp.diag(-a**2 + mu**2, r**2)
    terminal_ratio_sq = sp.simplify(((-h[0, 0]) ** 2) / (-h.det()))
    terminal_ratio_sq_reciprocal = sp.factor(terminal_ratio_sq.subs(a, 1 / r))

    # Pullback non-identifiability: S->S+D and Z->Z-DY leaves the screen leg and h fixed.
    d0, d1, z0, z1 = sp.symbols("d0 d1 z0 z1", real=True)
    dmat = sp.Matrix([[d0, d1]])
    z_generic = sp.Matrix([[z0, z1]])
    r_before = sp.simplify(modern_s * y + z_generic)
    r_after = sp.simplify((modern_s + dmat) * y + (z_generic - dmat * y))

    # Full 2+2 restricted slice: P has mu^2 in one slot, but infinitely many extensions agree there.
    t, alpha, u, v = sp.symbols("t alpha u v", nonzero=True, real=True)
    q4 = sp.diag(s, t)
    s_restricted = sp.Matrix([[-mu / s, 0], [0, 0]])
    p_restricted = sp.simplify(s_restricted.T * q4.T * q4 * s_restricted)
    f_alpha_restricted = sp.simplify(sp.trace(p_restricted) + alpha * p_restricted.det())
    s_generic = sp.Matrix([[-mu / s, 0], [0, u / t]])
    p_generic = sp.simplify(s_generic.T * q4.T * q4 * s_generic)
    f_alpha_generic = sp.simplify(sp.trace(p_generic) + alpha * p_generic.det())
    extension_difference = sp.simplify(f_alpha_generic.subs(alpha, 1) - f_alpha_generic.subs(alpha, 0))

    # Conditional general endpoint transition formula, checked on dense symbolic 2x2 blocks.
    bp = sp.Matrix(sp.symbols("bp0:4")).reshape(2, 2)
    bq = sp.Matrix(sp.symbols("bq0:4")).reshape(2, 2)
    qp = sp.Matrix(sp.symbols("qp0:4")).reshape(2, 2)
    qq = sp.Matrix(sp.symbols("qq0:4")).reshape(2, 2)
    spm = sp.Matrix(sp.symbols("sp0:4")).reshape(2, 2)
    sqm = sp.Matrix(sp.symbols("sq0:4")).reshape(2, 2)
    zero2 = sp.zeros(2)
    ep = bp.row_join(zero2).col_join((qp * spm).row_join(qp))
    eq = bq.row_join(zero2).col_join((qq * sqm).row_join(qq))
    transition = sp.simplify(eq * ep.inv())
    expected_transition = (bq * bp.inv()).row_join(zero2).col_join(
        (qq * (sqm - spm) * bp.inv()).row_join(qq * qp.inv())
    )

    checks = {
        "upper_adjoint_is_lower_modern_slice": is_zero_matrix(lower - expected_lower),
        "modern_one_screen_coframe_equals_lower_dual": is_zero_matrix(modern_lower - lower),
        "upper_lower_strains_are_similar": is_zero_matrix(similarity_residual),
        "upper_lower_charpolys_equal": sp.simplify(cp_upper.as_expr() - cp_lower.as_expr()) == 0,
        "august_trace_reproduced": sp.simplify(reciprocal_trace - (r**2 + r**-2 + s**2 - mu**2)) == 0,
        "august_inv2_reproduced": sp.simplify(reciprocal_inv2 - (1 + r**2 * s**2 + s**2 / r**2 - mu**2 * r**2)) == 0,
        "august_det_reproduced": sp.simplify(reciprocal_det - s**2) == 0,
        "base_aligned_pair_metric": is_zero_matrix(h - expected_h),
        "pair_pullback_independent_of_screen_scale": all(s not in entry.free_symbols for entry in h),
        "pullback_fiber_exact": is_zero_matrix(r_after - r_before),
        "restricted_gram_is_mu2_rank_one": is_zero_matrix(p_restricted - sp.diag(mu**2, 0)),
        "all_extensions_agree_on_restricted_slice": sp.simplify(f_alpha_restricted - mu**2) == 0,
        "extensions_differ_on_rank_two_slice": sp.simplify(extension_difference - mu**2 * u**2) == 0,
        "general_endpoint_transition_formula": is_zero_matrix(transition - expected_transition),
    }

    result = {
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "conditional_crosswalk": {
            "lower_transition_mixing_block": "Q_q (S_q-S_p) B_p^-1",
            "one_screen_relation": "m_lower=-mu_lock=Q_q*(S_q-S_p)*B_p^-1|screen,clock",
            "reference_slice": "B_p=Q_p=I, S_p=0; B_q=diag(a,r), Q_q=s, S_q=(-mu/s,0)",
        },
        "pair_pullback": {
            "h": str(h),
            "terminal_ratio_squared_a_eq_1_over_r": str(terminal_ratio_sq_reciprocal),
            "old_full_arrow_trace": str(reciprocal_trace),
            "screen_scale_retained_by_old_arrow": str(sp.diff(reciprocal_trace, s)),
            "screen_scale_retained_by_base_pair_h": str(sp.diff(h[0, 0], s)),
        },
        "nonuniqueness_witness": {
            "restricted_P": str(p_restricted),
            "F_alpha_restricted": str(f_alpha_restricted),
            "F_alpha_rank_two": str(f_alpha_generic),
            "F_1_minus_F_0_rank_two": str(extension_difference),
        },
        "landing": "MIXED__RESTRICTED_S_COORDINATE_BRIDGE_EXISTS__MU_LOCK_INVARIANT_REMAINS_FULL_ARROW_CHANNEL__TERMINAL_PAIR_RECOVERY_NONUNIQUE",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
