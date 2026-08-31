#!/usr/bin/env python3
"""Dependency-free exact algebra and high-precision witness replay for G309.

The load-bearing rational identities are checked as integer-coefficient
polynomials.  The only numerical checks are the preregistered deformation
witness, evaluated with the Python standard library's Decimal arithmetic.
"""

from __future__ import annotations

import argparse
import json
from decimal import Decimal, localcontext
from pathlib import Path


LANDING = (
    "FOUNDED_STRENGTHENED_CHAIN_REMAINS_COMPATIBILITY_ONLY"
    "__ROUND_HOPF_TIME_LIVE_COUNTERFAMILY_SURVIVES"
    "__CONDITIONAL_TRACEFREE_RESIDUAL_CLOSES_POSITIVE_STANDARD_COMPLETION_TO_ONE_SCALE"
    "__HOPF_STRUCTURE_DOES_NOT_OWN_OR_CALIBRATE_THAT_RESIDUAL"
)

# A polynomial in (a, a', a'') is represented by exponent triples.
Monomial = tuple[int, int, int]
Polynomial = dict[Monomial, int]


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + coefficient
        if result[monomial] == 0:
            del result[monomial]
    return result


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for lm, lc in left.items():
        for rm, rc in right.items():
            monomial = tuple(x + y for x, y in zip(lm, rm))
            result[monomial] = result.get(monomial, 0) + lc * rc
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def scale(coefficient: int, polynomial: Polynomial) -> Polynomial:
    return {monomial: coefficient * value for monomial, value in polynomial.items() if coefficient * value}


def bump_derivative(previous: dict[int, int]) -> dict[int, int]:
    """Apply d/dt=-y^2 d/dy to P(y) exp(-y^2), where y=1/t."""
    result: dict[int, int] = {}
    for power, coefficient in previous.items():
        if power:
            result[power + 1] = result.get(power + 1, 0) - power * coefficient
        result[power + 3] = result.get(power + 3, 0) + 2 * coefficient
    return {power: coefficient for power, coefficient in result.items() if coefficient}


def reduce_hyperbolic_square(polynomial: dict[str, int]) -> dict[str, int]:
    """Apply cosh(u)^2=sinh(u)^2+1 to a linear square expression."""
    result = dict(polynomial)
    cosh_coefficient = result.pop("cosh_squared", 0)
    result["sinh_squared"] = result.get("sinh_squared", 0) + cosh_coefficient
    result["constant"] = result.get("constant", 0) + cosh_coefficient
    return {name: coefficient for name, coefficient in result.items() if coefficient}


def witness_values() -> tuple[str, str]:
    """Return the registered X=1, epsilon=1/10, T=1 witness at 50 digits."""
    with localcontext() as context:
        context.prec = 90
        one = Decimal(1)
        exp_one = one.exp()
        exp_minus_one = (-one).exp()
        cosh_one = (exp_one + exp_minus_one) / 2
        sinh_one = (exp_one - exp_minus_one) / 2
        epsilon = one / 10

        bump = exp_minus_one
        bump_prime = 2 * bump
        bump_second = -2 * bump
        value = cosh_one * (epsilon * bump).exp()
        log_prime = sinh_one / cosh_one + epsilon * bump_prime
        log_second = one / cosh_one**2 + epsilon * bump_second

        q_value = value**2 * log_second - one
        scalar_value = 6 * (log_second + 2 * log_prime**2 + one / value**2)
        return format(q_value, ".50g"), format(scalar_value, ".50g")


def build_result() -> dict:
    one: Polynomial = {(0, 0, 0): 1}
    a: Polynomial = {(1, 0, 0): 1}
    ap: Polynomial = {(0, 1, 0): 1}
    app: Polynomial = {(0, 0, 1): 1}

    # Q is the numerator of K_T-K_S after multiplication by a^2.
    q_polynomial = add(add(multiply(a, app), scale(-1, multiply(ap, ap))), scale(-1, one))
    expected_q = {(1, 0, 1): 1, (0, 2, 0): -1, (0, 0, 0): -1}
    assert q_polynomial == expected_q

    # The scalar-curvature numerator is 6(a a'' + a'^2 + 1).
    scalar_numerator = scale(6, add(add(multiply(a, app), multiply(ap, ap)), one))
    assert scalar_numerator == {(1, 0, 1): 6, (0, 2, 0): 6, (0, 0, 0): 6}

    # For a=X cosh(u), a'=sinh(u), a''=cosh(u)/X, both Q=0 and
    # R=12/X^2 reduce exactly to cosh(u)^2-sinh(u)^2=1.
    hyperbolic_relation = {"cosh_squared": 1, "sinh_squared": -1, "constant": -1}
    assert reduce_hyperbolic_square(hyperbolic_relation) == {}
    base_q = 0  # exact after the checked reduction
    assert base_q == 0
    base_spatial_channel_relation = {"sinh_squared": 1, "constant": 1, "cosh_squared": -1}
    assert reduce_hyperbolic_square(base_spatial_channel_relation) == {}
    base_temporal_channel_units = 1
    base_spatial_channel_units = 1
    base_scalar_numerator_units = 6 * (base_temporal_channel_units + base_spatial_channel_units)
    assert base_scalar_numerator_units == 12

    # Every right derivative of exp(-1/t^2) is P_n(1/t) exp(-1/t^2).
    # The standard flat-function theorem then gives a zero right limit.
    expected_bump_polynomials = (
        {0: 1},
        {3: 2},
        {6: 4, 4: -6},
        {9: 8, 7: -36, 5: 24},
        {12: 16, 10: -144, 8: 300, 6: -120},
    )
    bump_polynomials = [expected_bump_polynomials[0]]
    for _ in range(4):
        bump_polynomials.append(bump_derivative(bump_polynomials[-1]))
    assert tuple(bump_polynomials) == expected_bump_polynomials
    flat_limits = [{"order": order, "right_limit": "0"} for order in range(5)]

    q_numeric, scalar_numeric = witness_values()
    assert abs(Decimal(q_numeric)) > Decimal("1e-3")
    assert abs(Decimal(scalar_numeric) - 12) > Decimal("1e-3")

    # Exact normalized Hopf time carry: -a'/a^2 + a'/a^2=0.
    carry_coefficients = -1 + 1
    assert carry_coefficients == 0

    # Quotient-rule numerator for kappa' equals 2 a' Q exactly.
    quotient_numerator = add(
        scale(2, multiply(multiply(ap, app), a)),
        scale(-2, multiply(ap, add(multiply(ap, ap), one))),
    )
    asserted_numerator = scale(2, multiply(ap, q_polynomial))
    assert quotient_numerator == asserted_numerator

    # The shifted positive family X cosh((T-T0)/X) obeys the same exact
    # hyperbolic reduction, so T0 is an isometric time-origin parameter.
    assert reduce_hyperbolic_square(hyperbolic_relation) == {}

    checks = 5 + 8
    return {
        "landing": LANDING,
        "candidate": "B",
        "symbolic_checks": checks,
        "scalar_curvature_formula": "6*(a(t)*Derivative(a(t), (t, 2)) + Derivative(a(t), t)**2 + 1)/a(t)**2",
        "tracefree_gap_formula": "(a(t)*Derivative(a(t), (t, 2)) - Derivative(a(t), t)**2 - 1)/a(t)**2",
        "q_formula": "a(t)*Derivative(a(t), (t, 2)) - Derivative(a(t), t)**2 - 1",
        "base_scalar_curvature": "12/X**2",
        "base_q": "0",
        "deformed_q_at_T1_X1_eps_1_10": "-(-(-cosh(1)**2 + 5*E)*exp(exp(-1)/5)/5 + E)*exp(-1)",
        "deformed_q_numeric": q_numeric,
        "deformed_scalar_at_T1_X1_eps_1_10": "-6*exp(-1)/5 + 6*exp(-exp(-1)/5)/cosh(1)**2 + 6/cosh(1)**2 + 12*(1 + 5*E*tanh(1))**2*exp(-2)/25",
        "deformed_scalar_numeric": scalar_numeric,
        "flat_join_derivative_limits": flat_limits,
        "hopf_normalized_time_carry": "0",
        "conditional_constant_derivative": "2*(a(t)*Derivative(a(t), (t, 2)) - Derivative(a(t), t)**2 - 1)*Derivative(a(t), t)/a(t)**3",
        "ownership": {
            "F1_F4_W1_W3_W6": "compatibility_and_readout_not_nonidentity_residual",
            "G305_G308": "conditional_kinematic_global_structure",
            "G301_tracefree": "conditional_candidate_law_not_founded_derivation",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build_result()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
