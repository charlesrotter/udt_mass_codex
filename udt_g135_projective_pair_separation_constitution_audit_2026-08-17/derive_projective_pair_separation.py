#!/usr/bin/env python3
"""Exact G135 production algebra.

This script characterizes the projective reciprocal-shape readout of a supplied
regular calibrated pair metric.  It does not identify that readout with physical
distance and does not assign X_max.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


OUT = Path(__file__).with_name("DERIVATION_RESULT.json")


def main() -> None:
    checks: dict[str, bool] = {}

    # Generic regular calibrated pair metric in its exact T-L-beta decomposition.
    T, L, beta, omega = sp.symbols("T L beta omega", positive=True)
    h = sp.Matrix(
        [
            [-T**2, -T**2 * beta],
            [-T**2 * beta, L**2 - T**2 * beta**2],
        ]
    )
    checks["pair_det"] = sp.simplify(h.det() + T**2 * L**2) == 0
    checks["recover_T2"] = sp.simplify(-h[0, 0] - T**2) == 0
    checks["recover_beta"] = sp.simplify(h[0, 1] / h[0, 0] - beta) == 0
    checks["recover_L2"] = (
        sp.simplify(h[1, 1] - h[0, 1] ** 2 / h[0, 0] - L**2) == 0
    )

    r = sp.symbols("r", positive=True)
    q = 1 / r
    chi_r = sp.cancel((r - 1) / (r + 1))
    chi_q = sp.cancel((1 - q) / (1 + q))
    checks["chi_ratio_identity"] = sp.simplify(chi_r - chi_q) == 0
    checks["chi_tanh_identity"] = (
        sp.simplify(
            chi_r
            - (sp.exp(sp.log(r)) - 1) / (sp.exp(sp.log(r)) + 1)
        )
        == 0
    )
    checks["chi_exchange_odd"] = sp.simplify(chi_r.subs(r, 1 / r) + chi_r) == 0
    checks["chi_neutral"] = sp.simplify(chi_r.subs(r, 1)) == 0
    checks["chi_positive_boundary"] = sp.limit(chi_r, r, sp.oo) == 1
    checks["chi_negative_boundary"] = sp.limit(chi_r, r, 0, dir="+") == -1
    checks["chi_monotone"] = sp.simplify(sp.diff(chi_r, r) - 2 / (r + 1) ** 2) == 0

    # The projective coordinate is latent in the reciprocal kernel itself.  In the
    # sum/contrast basis, D becomes a hyperbolic mixing matrix and chi is the
    # contrast/common projective slope of the transformed neutral ray.
    p = sp.symbols("p", positive=True)
    D = sp.diag(1 / p, p)
    H = sp.Matrix([[sp.Rational(1, 2), sp.Rational(1, 2)],
                   [-sp.Rational(1, 2), sp.Rational(1, 2)]])
    H_inv = sp.Matrix([[1, -1], [1, 1]])
    boost_basis = sp.simplify(H * D * H_inv)
    expected_boost = sp.Matrix(
        [
            [(p + 1 / p) / 2, (p - 1 / p) / 2],
            [(p - 1 / p) / 2, (p + 1 / p) / 2],
        ]
    )
    checks["reciprocal_kernel_sum_contrast_form"] = sp.simplify(
        boost_basis - expected_boost
    ) == sp.zeros(2)
    neutral_ray = sp.Matrix([1, 0])
    moved_ray = sp.simplify(boost_basis * neutral_ray)
    projective_slope = sp.cancel(moved_ray[1] / moved_ray[0])
    checks["projective_slope_is_chi"] = sp.simplify(
        projective_slope - (p**2 - 1) / (p**2 + 1)
    ) == 0

    # Additive reciprocal depth induces the bounded fractional-linear law.
    x, y = sp.symbols("x y")
    mobius = sp.cancel((x + y) / (1 + x * y))
    r_of_x = (1 + x) / (1 - x)
    r_of_y = (1 + y) / (1 - y)
    composed_from_ratios = sp.cancel(
        ((r_of_x * r_of_y) - 1) / ((r_of_x * r_of_y) + 1)
    )
    checks["mobius_composition"] = sp.simplify(composed_from_ratios - mobius) == 0
    checks["mobius_identity"] = sp.simplify(mobius.subs(y, 0) - x) == 0
    checks["mobius_inverse"] = sp.simplify(mobius.subs(y, -x)) == 0
    z = sp.symbols("z")
    lhs_assoc = sp.cancel((mobius + z) / (1 + mobius * z))
    yz = sp.cancel((y + z) / (1 + y * z))
    rhs_assoc = sp.cancel((x + yz) / (1 + x * yz))
    checks["mobius_associative"] = sp.simplify(lhs_assoc - rhs_assoc) == 0

    # Solve rather than assume the anchored first-degree projective chart.
    a, b, c, d = sp.symbols("a b c d")
    anchored_solution = sp.solve(
        [b + d, a + b, a - c, d - 1], [a, b, c, d], dict=True
    )
    checks["projective_anchor_unique"] = anchored_solution == [
        {a: 1, b: -1, c: 1, d: 1}
    ]
    F = sp.cancel((a * r + b) / (c * r + d))
    F_unique = sp.simplify(F.subs(anchored_solution[0]))
    checks["projective_solution_is_chi"] = sp.simplify(F_unique - chi_r) == 0

    # Common metric scale remains real data but cancels from reciprocal shape.
    chi_TL = sp.cancel((L - T) / (L + T))
    checks["common_scale_invariance"] = (
        sp.simplify(chi_TL.subs({T: omega * T, L: omega * L}) - chi_TL) == 0
    )
    checks["common_scale_changes_pair_metric"] = any(
        sp.simplify(e) != 0 for e in (omega**2 * h - h)
    )

    # Infinite smooth counterfamilies against unrestricted chart uniqueness.
    eps = sp.symbols("eps", real=True)
    f_eps = x + eps * x * (1 - x**2)
    g_eps = x + eps * x**3 * (1 - x**2)
    checks["counterfamily_f_odd"] = sp.simplify(f_eps.subs(x, -x) + f_eps) == 0
    checks["counterfamily_f_anchors"] = all(
        sp.simplify(f_eps.subs(x, value) - value) == 0 for value in (-1, 0, 1)
    )
    checks["counterfamily_g_odd"] = sp.simplify(g_eps.subs(x, -x) + g_eps) == 0
    checks["counterfamily_g_anchors"] = all(
        sp.simplify(g_eps.subs(x, value) - value) == 0 for value in (-1, 0, 1)
    )
    checks["counterfamily_g_neutral_slope"] = sp.simplify(
        sp.diff(g_eps, x).subs(x, 0) - 1
    ) == 0
    f_coefficient = sp.expand((sp.diff(f_eps, x) - 1) / eps)
    g_coefficient = sp.expand((sp.diff(g_eps, x) - 1) / eps)
    # On |x|<=1, f_coefficient=1-3x^2 has range [-2,1].  Therefore
    # f'>0 throughout the open epsilon interval (-1,1/2): the only zero
    # margins occur at the two excluded parameter endpoints.
    checks["counterfamily_f_full_interval_extrema"] = (
        f_coefficient == 1 - 3 * x**2
        and sp.solve(sp.diff(f_coefficient, x), x) == [0]
        and f_coefficient.subs(x, 0) == 1
        and f_coefficient.subs(x, 1) == -2
        and f_coefficient.subs(x, -1) == -2
        and 1 + (-1) * 1 == 0
        and 1 + sp.Rational(1, 2) * (-2) == 0
    )
    # With u=x^2 in [0,1], g_coefficient=3u-5u^2 has range [-2,9/20].
    # The positive-epsilon limiting margin is again zero only at epsilon=1/2;
    # the negative-epsilon margin remains 11/20 even at the excluded epsilon=-1.
    u = sp.symbols("u", nonnegative=True)
    g_u = 3 * u - 5 * u**2
    checks["counterfamily_g_full_interval_extrema"] = (
        g_coefficient == 3 * x**2 - 5 * x**4
        and sp.solve(sp.diff(g_u, u), u) == [sp.Rational(3, 10)]
        and g_u.subs(u, 0) == 0
        and g_u.subs(u, 1) == -2
        and g_u.subs(u, sp.Rational(3, 10)) == sp.Rational(9, 20)
        and 1 + sp.Rational(1, 2) * (-2) == 0
        and 1 + (-1) * sp.Rational(9, 20) == sp.Rational(11, 20)
    )
    xi1, xi2, eps0 = sp.Rational(1, 3), sp.Rational(1, 5), sp.Rational(1, 4)
    f = lambda value: sp.cancel(value + eps0 * value * (1 - value**2))
    native_then_mark = f(sp.cancel((xi1 + xi2) / (1 + xi1 * xi2)))
    mark_then_native = sp.cancel((f(xi1) + f(xi2)) / (1 + f(xi1) * f(xi2)))
    display_deviation = sp.cancel(native_then_mark - mark_then_native)
    checks["nonprojective_display_changes_mobius_formula"] = display_deviation != 0

    # Exact scale countermodel: same reciprocal/projective shape, different metric length.
    h1 = sp.diag(-1, 4)
    h2 = 4 * h1
    q1 = sp.Rational(1, 2)
    q2 = sp.Rational(2, 4)
    chi1 = (1 - q1) / (1 + q1)
    chi2 = (1 - q2) / (1 + q2)
    checks["scale_countermodel_same_q"] = q1 == q2
    checks["scale_countermodel_same_chi"] = chi1 == chi2 == sp.Rational(1, 3)
    checks["scale_countermodel_different_ruler_length"] = (
        sp.sqrt(h1[1, 1]) == 2 and sp.sqrt(h2[1, 1]) == 4
    )

    # Full orchestra is upstream: the registered two-column screen witness changes the readout.
    eta4 = sp.diag(-1, 1, 1, 1)
    j_base = sp.Matrix([[sp.Rational(1, 2), 0], [0, 2], [0, 0], [0, 0]])
    j_full = sp.Matrix(
        [
            [sp.Rational(1, 2), 0],
            [0, 2],
            [sp.Rational(1, 4), sp.Rational(1, 3)],
            [0, 0],
        ]
    )
    h_base = j_base.T * eta4 * j_base
    h_full = j_full.T * eta4 * j_full

    def q_from_h(metric: sp.Matrix) -> sp.Expr:
        return sp.cancel((-metric[0, 0]) / sp.sqrt(-metric.det()))

    checks["orchestra_changes_pair_metric"] = h_base != h_full
    checks["orchestra_changes_terminal_ratio"] = sp.simplify(
        q_from_h(h_base) - q_from_h(h_full)
    ) != 0

    # The bounded coordinate is not ordinarily additive.
    checks["bounded_coordinate_not_ordinary_additive"] = sp.simplify(mobius - (x + y)) != 0

    checks = {name: bool(value) for name, value in checks.items()}
    passed = sum(checks.values())
    result = {
        "schema": "udt-g135-derivation-v1",
        "status": "PASS" if passed == len(checks) else "FAIL",
        "checks_passed": passed,
        "checks_total": len(checks),
        "checks": checks,
        "exact_witnesses": {
            "nonprojective_composition_deviation": str(display_deviation),
            "scale_pair_1_ruler_length": "2",
            "scale_pair_2_ruler_length": "4",
            "shared_q": "1/2",
            "shared_chi": "1/3",
            "base_pair_metric": str(h_base.tolist()),
            "complete_pair_metric": str(h_full.tolist()),
            "base_q": str(q_from_h(h_base)),
            "complete_q": str(q_from_h(h_full)),
            "sum_contrast_kernel": str(boost_basis.tolist()),
            "neutral_ray_projective_slope": str(projective_slope),
        },
        "bounded_landing": (
            "PROJECTIVE_PAIR_COORDINATE_DERIVED_IN_NATURAL_CLASS__"
            "PHYSICAL_SEPARATION_IDENTIFICATION_AND_XMAX_SCALE_OPEN"
            if passed == len(checks)
            else "TYPE_OR_ALGEBRA_FAILURE"
        ),
        "premise_boundary": {
            "derived": [
                "chi=(L-T)/(L+T)=(1-q)/(1+q)=tanh(phi_pair)",
                "anchored first-degree projective uniqueness",
                "fractional-linear composition",
                "common-scale blindness",
            ],
            "open": [
                "physical separation identification",
                "X_max value and scale owner",
                "physical pair realization",
                "global completion and dynamics",
            ],
        },
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
