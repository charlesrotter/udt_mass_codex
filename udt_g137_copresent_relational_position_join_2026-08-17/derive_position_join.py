#!/usr/bin/env python3
"""Exact symbolic derivation for the preregistered G137 position join."""

from __future__ import annotations

import json

import sympy as sp


def main() -> None:
    phi, psi, kappa, xmax, ce, ceff = sp.symbols(
        "phi psi kappa X_max c_E c_eff", real=True, positive=True
    )
    # The signed-depth calculations require unrestricted real depth symbols.
    p, r = sp.symbols("p r", real=True)
    T = sp.exp(kappa - p)
    L = sp.exp(kappa + p)
    q = sp.simplify(T / L)
    xi = sp.tanh(p)
    xi_q = sp.simplify((1 - q) / (1 + q))
    xi_tl = sp.simplify((L - T) / (L + T))
    xi_p = sp.tanh(p)
    xi_r = sp.tanh(r)
    xi_comp = sp.simplify((xi_p + xi_r) / (1 + xi_p * xi_r))
    x_p = xmax * xi_p
    x_r = xmax * xi_r
    x_comp = sp.simplify((x_p + x_r) / (1 + x_p * x_r / xmax**2))

    checks = []

    def check(name: str, condition: bool) -> None:
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    check("q_from_pair_densities", sp.simplify(q - sp.exp(-2 * p)) == 0)
    check("xi_from_q", sp.simplify(xi_q - xi) == 0)
    check("xi_from_T_L", sp.simplify(xi_tl - xi) == 0)
    check(
        "q_inverse",
        sp.simplify(((1 - xi) / (1 + xi) - sp.exp(-2 * p)).rewrite(sp.exp)) == 0,
    )
    check(
        "phi_inverse",
        sp.simplify((sp.atanh(sp.tanh(p)) - p).rewrite(sp.log).rewrite(sp.exp)) == 0,
    )
    check("reversal_signed", sp.simplify(sp.tanh(-p) + xi) == 0)
    check("reversal_nonnegative", sp.Abs(sp.tanh(-p)) == sp.Abs(xi))
    check("coincidence_signed", xi.subs(p, 0) == 0)
    check("coincidence_separation", sp.Abs(xi).subs(p, 0) == 0)
    check("positive_asymptote", sp.limit(xi, p, sp.oo) == 1)
    check("negative_asymptote", sp.limit(xi, p, -sp.oo) == -1)
    check("separation_asymptote", sp.limit(sp.Abs(xi), p, sp.oo) == 1)
    check("native_signed_composition", sp.trigsimp(xi_comp - sp.tanh(p + r)) == 0)
    check("dimensional_composition", sp.trigsimp(x_comp - xmax * sp.tanh(p + r)) == 0)
    check(
        "conditional_c_eff_join",
        sp.simplify(
            (((ce - ceff) / (ce + ceff)).subs(ceff, ce * sp.exp(-2 * p)) - xi).rewrite(sp.exp)
        )
        == 0,
    )
    check("unit_slope", sp.diff(xi, p).subs(p, 0) == 1)
    check("local_first_order", sp.limit(xi / p, p, 0) == 1)

    a = sp.Rational(1, 3)
    same_sign = sp.simplify((a + a) / (1 + a * a))
    opposite_sign = sp.simplify((a - a) / (1 - a * a))
    check("magnitude_witness_same_sign", same_sign == sp.Rational(3, 5))
    check("magnitude_witness_opposite_sign", opposite_sign == 0)
    check("magnitude_inputs_identical", (abs(a), abs(a)) == (abs(a), abs(-a)))
    check("magnitude_outputs_differ", abs(same_sign) != abs(opposite_sign))

    result = {
        "classification": (
            "OWNER_ADOPTED_WORKING_POSITION_CONSTITUTION__"
            "SIGNED_AND_NONNEGATIVE_XMAX_JOIN_DERIVED_ON_SUPPLIED_REGULAR_COMPLETE_PAIRS__"
            "ORIENTATION_REQUIRED_FOR_COMPOSITION__"
            "XMAX_VALUE_PROPER_LENGTH_PAIR_REALIZATION_HISTORY_AND_GLOBAL_COMPLETION_OPEN"
        ),
        "checks_passed": len(checks),
        "checks_total": len(checks),
        "exact": {
            "q": "exp(-2*phi_pair)",
            "xi": "tanh(phi_pair)",
            "x": "X_max*tanh(phi_pair)",
            "sigma": "Abs(tanh(phi_pair))",
            "s": "X_max*Abs(tanh(phi_pair))",
            "same_sign_magnitude_output": str(same_sign),
            "opposite_sign_magnitude_output": str(opposite_sign),
        },
        "open": [
            "X_max numerical value dimensional owner profile and global realization",
            "proper length areal radius and signal distance joins",
            "pair realization and complete history",
            "singular and null strata",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
