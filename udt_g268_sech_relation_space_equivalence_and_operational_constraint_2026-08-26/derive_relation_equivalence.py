#!/usr/bin/env python3
"""Exact G268 production derivation; no observational or protected inputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


OUT = Path(__file__).with_name("DERIVATION_RESULT.json")
LANDING = (
    "FINITE_REGULAR_SECH_STATE_IS_EXACTLY_EQUIVALENT_TO_THE_RECIPROCAL_RELATION_SPACE__"
    "COMPACT_ENDPOINTS_FORM_ONLY_A_PARTIAL_NONGROUP_CLOSURE__"
    "INDEPENDENT_M_WOULD_GIVE_A_CONDITIONAL_CROSS_READOUT_LAW__"
    "NO_RELATION_NETWORK_HISTORY_DISTANCE_OR_XMAX_SELECTION"
)


def zero(expr: sp.Expr) -> bool:
    return sp.cancel(sp.trigsimp(expr.rewrite(sp.exp))) == 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    d, d1, d2 = sp.symbols("d d1 d2", real=True)
    r, r1, r2 = sp.symbols("r r1 r2", positive=True)
    q0, q1, q2, q3 = sp.symbols("q0 q1 q2 q3", positive=True)
    m, x = sp.symbols("m x", real=True)
    mp = sp.symbols("mp", positive=True)
    xp = sp.symbols("xp", real=True)

    def state_from_r(rr: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
        return sp.cancel(2 * rr / (1 + rr**2)), sp.cancel((1 - rr**2) / (1 + rr**2))

    def compose(
        a: tuple[sp.Expr, sp.Expr], b: tuple[sp.Expr, sp.Expr]
    ) -> tuple[sp.Expr, sp.Expr]:
        ma, xa = a
        mb, xb = b
        den = 1 + xa * xb
        return sp.cancel(ma * mb / den), sp.cancel((xa + xb) / den)

    checks: dict[str, bool] = {}
    md = sp.sech(d)
    xd = sp.tanh(d)
    checks["hyperbolic_circle"] = zero(md**2 + xd**2 - 1)
    checks["r_from_depth"] = zero(sp.exp(-d) - (1 - xd) / md)
    checks["rinv_from_depth"] = zero(sp.exp(d) - (1 + xd) / md)
    inverse_depth = sp.atanh(xd)
    checks["depth_from_chi_derivative"] = zero(sp.diff(inverse_depth, d) - 1)
    checks["depth_from_chi_origin"] = inverse_depth.subs(d, 0) == 0
    checks["dchi_rank"] = zero(sp.diff(xd, d) - md**2)
    rank_numerator = 4 * sp.exp(2 * d)
    rank_denominator = (sp.exp(2 * d) + 1) ** 2
    checks["dchi_rank_exponential_form"] = zero(md**2 - rank_numerator / rank_denominator)
    checks["dchi_rank_numerator_positive"] = sp.ask(sp.Q.positive(rank_numerator)) is True
    checks["dchi_rank_denominator_positive"] = sp.ask(sp.Q.positive(rank_denominator)) is True
    checks["dm_interlock"] = zero(sp.diff(md, d) + md * xd)

    mr, xr = state_from_r(r)
    checks["rational_circle"] = zero(mr**2 + xr**2 - 1)
    checks["rational_inverse_r"] = zero((1 - xr) / mr - r)
    checks["rational_inverse_rinv"] = zero((1 + xr) / mr - 1 / r)
    checks["kernel_leg_r"] = zero(1 / mr - xr / mr - r)
    checks["kernel_leg_rinv"] = zero(1 / mr + xr / mr - 1 / r)
    checks["identity_state"] = state_from_r(sp.Integer(1)) == (sp.Integer(1), sp.Integer(0))

    minv, xinv = state_from_r(1 / r)
    checks["reversal_even_m"] = zero(minv - mr)
    checks["reversal_odd_chi"] = zero(xinv + xr)

    s1 = state_from_r(r1)
    s2 = state_from_r(r2)
    s12 = compose(s1, s2)
    direct12 = state_from_r(r1 * r2)
    checks["composition_m"] = zero(s12[0] - direct12[0])
    checks["composition_chi"] = zero(s12[1] - direct12[1])
    composition_denominator = 1 + s1[1] * s2[1]
    positive_factorization = 2 * (r1**2 * r2**2 + 1) / (
        (r1**2 + 1) * (r2**2 + 1)
    )
    checks["composition_denominator_factorization"] = zero(
        composition_denominator - positive_factorization
    )
    checks["composition_denominator_positive"] = (
        sp.ask(sp.Q.positive(positive_factorization)) is True
    )

    r3 = sp.symbols("r3", positive=True)
    s3 = state_from_r(r3)
    left = compose(compose(s1, s2), s3)
    right = compose(s1, compose(s2, s3))
    checks["associativity_m"] = zero(left[0] - right[0])
    checks["associativity_chi"] = zero(left[1] - right[1])

    # Algebraic surjectivity modulo the target circle equation m^2+x^2=1.
    r_back = (1 - x) / m
    m_back, x_back = state_from_r(r_back)
    num_m = sp.together(m_back - m).as_numer_denom()[0]
    num_x = sp.together(x_back - x).as_numer_denom()[0]
    circle = m**2 + x**2 - 1
    checks["surjectivity_m_mod_circle"] = sp.rem(sp.Poly(num_m, m), sp.Poly(circle, m)) == 0
    checks["surjectivity_chi_mod_circle"] = sp.rem(sp.Poly(num_x, m), sp.Poly(circle, m)) == 0
    right_semicircle_assumptions = (
        sp.Q.positive(mp) & sp.Q.negative(xp - 1) & sp.Q.positive(xp + 1)
    )
    checks["inverse_positive_on_right_semicircle"] = (
        sp.ask(sp.Q.positive((1 - xp) / mp), right_semicircle_assumptions) is True
    )
    global_interior_diffeomorphism = all(
        checks[name]
        for name in (
            "rational_inverse_r",
            "rational_inverse_rinv",
            "surjectivity_m_mod_circle",
            "surjectivity_chi_mod_circle",
            "inverse_positive_on_right_semicircle",
            "dchi_rank_exponential_form",
            "dchi_rank_numerator_positive",
            "dchi_rank_denominator_positive",
        )
    )

    # Endpoint-potential network: q_j/q_i composes and cycles exactly.
    r01, r12, r23 = q1 / q0, q2 / q1, q3 / q2
    r02, r03 = q2 / q0, q3 / q0
    checks["network_chain_02"] = zero(r01 * r12 - r02)
    checks["network_chain_03"] = zero(r01 * r12 * r23 - r03)
    checks["network_cycle_product"] = zero((q1 / q0) * (q2 / q1) * (q0 / q2) - 1)
    net02 = compose(state_from_r(r01), state_from_r(r12))
    checks["network_bounded_02_m"] = zero(net02[0] - state_from_r(r02)[0])
    checks["network_bounded_02_chi"] = zero(net02[1] - state_from_r(r02)[1])
    net03 = compose(net02, state_from_r(r23))
    checks["network_bounded_03_m"] = zero(net03[0] - state_from_r(r03)[0])
    checks["network_bounded_03_chi"] = zero(net03[1] - state_from_r(r03)[1])
    checks["network_reconstruction_up_to_reference"] = zero(q0 * r03 - q3)

    # The closed semicircle adds ideal endpoints but opposite ends have zero denominator.
    plus = (sp.Integer(0), sp.Integer(1))
    minus = (sp.Integer(0), sp.Integer(-1))
    checks["same_plus_endpoint_denominator_nonzero"] = 1 + plus[1] * plus[1] == 2
    checks["same_minus_endpoint_denominator_nonzero"] = 1 + minus[1] * minus[1] == 2
    checks["opposite_endpoint_denominator_zero"] = 1 + plus[1] * minus[1] == 0

    # Enlarged operational type: this is nonidentity only if M is independently supplied.
    cross_residual = sp.cancel(m - 2 * r / (1 + r**2))
    off_residual = cross_residual.subs({r: sp.Rational(2), m: sp.Rational(1, 2)})
    checks["cross_readout_residual_is_nonzero_function"] = cross_residual != 0
    checks["off_law_extended_datum_rejected"] = off_residual == sp.Rational(-3, 10)
    checks["candidate_data_zero_residual"] = zero(cross_residual.subs(m, mr))

    assert all(checks.values()), [name for name, passed in checks.items() if not passed]
    assert global_interior_diffeomorphism
    result = {
        "status": "PASS",
        "landing": LANDING,
        "relation_space_landing": "R0__EXACT_EQUIVALENCE_ONLY",
        "boundary_landing": "R2__BOUNDARY_ONLY_CHANGE",
        "operational_landing": "O1__CONDITIONAL_CROSS_READOUT_LAW",
        "owned_operational_protocol": False,
        "regular_relation_rejections": 0,
        "finite_network_rejections": 0,
        "history_rejections": 0,
        "compact_closure_total_group": False,
        "global_interior_diffeomorphism": global_interior_diffeomorphism,
        "analytic_scope_conclusions_not_counted_as_symbolic_checks": {
            "regular_relation_rejections": 0,
            "finite_network_rejections": 0,
            "history_rejections": 0,
            "owned_operational_protocol": False,
        },
        "exact_checks": len(checks),
        "checks": checks,
        "off_law_witness": {
            "r": "2",
            "M_supplied": "1/2",
            "M_candidate": "4/5",
            "residual": "-3/10",
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if not args.no_write:
        OUT.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
