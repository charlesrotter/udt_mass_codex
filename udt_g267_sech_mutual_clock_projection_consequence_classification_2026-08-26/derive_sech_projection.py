#!/usr/bin/env python3
"""Exact symbolic G267 candidate-consequence derivation; reads no recorded result."""

from __future__ import annotations

import json
import sympy as sp


def main() -> None:
    delta = sp.symbols("delta", real=True)
    gamma = sp.cosh(delta)
    xi = sp.sinh(delta)
    chi = sp.tanh(delta)
    mutual = sp.sech(delta)
    arrow = sp.exp(-delta)
    checks: list[str] = []

    def zero(expr: sp.Expr, name: str) -> None:
        assert sp.simplify(sp.trigsimp(expr.rewrite(sp.exp))) == 0, name
        checks.append(name)

    zero(mutual**2 + chi**2 - 1, "unit_semicircle")
    zero(mutual * gamma - 1, "gamma_reconstruction")
    zero(mutual * xi - chi, "xi_reconstruction")
    zero((1 - chi) / mutual - arrow, "signed_arrow_reconstruction")
    zero((1 + chi) / mutual - 1 / arrow, "inverse_arrow_reconstruction")
    zero(mutual - 2 * arrow / (1 + arrow**2), "inverse_trace_arrow_form")
    zero(mutual.subs(delta, -delta) - mutual, "mutual_reversal_even")
    zero(chi.subs(delta, -delta) + chi, "position_reversal_odd")

    m1, m2, c1, c2 = sp.symbols("m1 m2 c1 c2", real=True)
    denom = 1 + c1 * c2
    m12 = m1 * m2 / denom
    c12 = (c1 + c2) / denom
    circle_residual = sp.together(m12**2 + c12**2 - 1) * denom**2
    circle_residual = sp.expand(circle_residual).subs(m1**2, 1 - c1**2)
    circle_residual = sp.expand(circle_residual).subs(m2**2, 1 - c2**2)
    zero(circle_residual, "composition_preserves_semicircle")
    zero(m12.subs({m2: 1, c2: 0}) - m1, "composition_identity_mutual")
    zero(c12.subs({m2: 1, c2: 0}) - c1, "composition_identity_position")
    inv_denom = denom.subs({m2: m1, c2: -c1})
    inv_m = m12.subs({m2: m1, c2: -c1})
    inv_c = c12.subs({m2: m1, c2: -c1})
    zero(sp.together(inv_m - 1).subs(m1**2, 1 - c1**2), "composition_inverse_mutual")
    zero(inv_c, "composition_inverse_position")
    assert sp.simplify(inv_denom - (1 - c1**2)) == 0
    checks.append("composition_inverse_denominator_positive_on_regular_state")

    d1, d2 = sp.symbols("d1 d2", real=True)
    zero(
        sp.sech(d1 + d2)
        - sp.sech(d1) * sp.sech(d2) / (1 + sp.tanh(d1) * sp.tanh(d2)),
        "mutual_composition_from_additive_depth",
    )
    zero(
        sp.tanh(d1 + d2)
        - (sp.tanh(d1) + sp.tanh(d2)) / (1 + sp.tanh(d1) * sp.tanh(d2)),
        "position_composition_from_additive_depth",
    )

    q = sp.Rational(3, 5)
    p = sp.Rational(4, 5)
    same_den = 1 + q**2
    opposite_den = 1 - q**2
    zero(p**2 / same_den - sp.Rational(8, 17), "same_sign_mutual_output")
    zero(2 * q / same_den - sp.Rational(15, 17), "same_sign_position_output")
    zero(p**2 / opposite_den - 1, "opposite_sign_mutual_output")
    zero((q - q) / opposite_den, "opposite_sign_position_output")
    assert sp.Rational(8, 17) != 1
    checks.append("mutual_alone_noncompositional_counterexample")

    zero(sp.diff(mutual, delta) + mutual * chi, "mutual_differential_interlock")
    zero(sp.diff(chi, delta) - mutual**2, "position_differential_interlock")
    zero(mutual.subs(delta, 0) - 1, "quiet_mutual_identity")
    zero(sp.diff(mutual, delta).subs(delta, 0), "quiet_mutual_no_linear_term")
    zero(sp.diff(mutual, delta, 2).subs(delta, 0) + 1, "quiet_mutual_quadratic_term")
    zero(sp.diff(chi, delta).subs(delta, 0) - 1, "quiet_position_linear_term")
    zero(sp.diff(arrow, delta).subs(delta, 0) + 1, "directional_arrow_remains_linear")
    quiet_series = sp.series(mutual, delta, 0, 6).removeO()
    zero(
        quiet_series - (1 - delta**2 / 2 + 5 * delta**4 / 24),
        "quiet_series_through_quartic",
    )
    assert sp.limit(mutual, delta, sp.oo) == 0
    checks.append("positive_loud_end_mutual_rate_zero")
    assert sp.limit(mutual, delta, -sp.oo) == 0
    checks.append("negative_loud_end_mutual_rate_zero")
    assert sp.limit(sp.exp(delta) * mutual, delta, sp.oo) == 2
    checks.append("positive_loud_end_asymptotic")
    assert sp.limit(sp.exp(-delta) * mutual, delta, -sp.oo) == 2
    checks.append("negative_loud_end_asymptotic")

    g = sp.symbols("g", positive=True)
    competitors = (1 / g, 1 / g**2, 2 / (g + 1))
    for index, function in enumerate(competitors, start=1):
        zero(function.subs(g, 1) - 1, f"competitor_{index}_normalized")
    values = [sp.simplify(function.subs(g, sp.Rational(5, 4))) for function in competitors]
    assert values == [sp.Rational(4, 5), sp.Rational(16, 25), sp.Rational(8, 9)]
    assert len(set(values)) == 3
    checks.append("three_coefficient_free_even_projections_distinct")

    landing = (
        "SECH_PROVISIONALLY_CLOSES_A_COEFFICIENT_FREE_BOUNDED_PAIR_STATE__"
        "SIGNED_COMPANION_REQUIRED_FOR_COMPOSITION__"
        "MUTUAL_EFFECT_IS_QUADRATIC_AT_QUIET_AND_SYMMETRIC_AT_LOUD_ENDS__"
        "DISTANCE_SCALE_QUERY_POPULATION_AND_HISTORY_REMAIN_OPEN"
    )
    result = {
        "status": "PASS",
        "landing": landing,
        "selected_alternative": (
            "C__SECH_NEW_PREMISE_CLOSES_COMPACT_PAIR_STATE__DISTANCE_AND_HISTORY_OPEN"
        ),
        "candidate_status": "SUPPLIED_PROVISIONAL_CANDIDATE_NOT_DERIVED_UNIQUE_NOT_CANON",
        "exact_checks": len(checks),
        "checks": checks,
        "bounded_pair_state": {
            "domain": "M>0, -1<chi<1, M^2+chi^2=1; endpoints only in closure",
            "M": "sech(delta)=1/Gamma",
            "chi": "tanh(delta)=Xi/Gamma",
            "Gamma": "1/M",
            "Xi": "chi/M",
            "r": "(1-chi)/M",
        },
        "composition": {
            "denominator": "1+chi_AB*chi_BC",
            "M_AC": "M_AB*M_BC/(1+chi_AB*chi_BC)",
            "chi_AC": "(chi_AB+chi_BC)/(1+chi_AB*chi_BC)",
            "M_alone": "INSUFFICIENT_SIGNED_COMPANION_REQUIRED",
            "associativity": "INHERITED_EXACTLY_FROM_ADDITIVE_DELTA",
        },
        "quiet_loud": {
            "quiet": "M=1-delta^2/2+5*delta^4/24+O(delta^6); no linear mutual term",
            "directional": "r=1-delta+O(delta^2); directional arrow remains first order",
            "positive_end": "M~2*exp(-delta)",
            "negative_end": "M~2*exp(delta)",
            "effect": "1-M tends from zero at quiet to one at both ends",
        },
        "projection_competitors": {
            "class": "positive normalized coefficient-free smooth functions of Gamma",
            "examples": ["1/Gamma", "1/Gamma^2", "2/(Gamma+1)"],
            "values_at_Gamma_5_over_4": ["4/5", "16/25", "8/9"],
            "uniqueness": "NOT_DERIVED_BY_F1_F4_W1_W4_G266",
        },
        "separation_ownership": {
            "M_alone": "absolute dimensionless depth |delta|",
            "M_and_chi": "signed dimensionless depth delta",
            "dimensionful_distance": "OPEN_REQUIRES_INDEPENDENT_SCALE_AND_PROTOCOL",
        },
        "history_rejection_by_candidate_definition": 0,
        "query_population": "OPEN_SUPPLIED_RELATION_ONLY",
        "redshift_guard": "r=exp(-delta) remains the signed one-way clock/frequency arrow; M is not r",
    }
    assert len(checks) == 37
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
