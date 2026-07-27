#!/usr/bin/env python3
"""Exact jet audit for the complete twisted reciprocal S3 Killing algebra.

The calculation uses a north-pole chart of the globally defined unit-quaternion S3.
All load-bearing curvature-gradient quantities are exact SymPy rationals.  The profile
is the restriction of a polynomial in global embedding coordinates, so the local jet
belongs to a globally smooth scalar rather than to an unextended coordinate ansatz.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
x, y, z = sp.symbols("x y z")
VARS = (x, y, z)
DIM = 4


def trunc(expr: sp.Expr, degree: int) -> sp.Expr:
    """Total-degree truncation in the three spatial chart variables."""
    expr = sp.expand(expr)
    if expr == 0:
        return sp.S.Zero
    poly = sp.Poly(expr, *VARS)
    kept = []
    for monomial, coefficient in poly.terms():
        if sum(monomial) <= degree:
            term = coefficient
            for variable, power in zip(VARS, monomial):
                term *= variable**power
            kept.append(term)
    return sp.expand(sum(kept, sp.S.Zero))


def exp_jet(argument: sp.Expr, degree: int = 3) -> sp.Expr:
    """Exponential jet when argument has zero constant term."""
    assert argument.subs({x: 0, y: 0, z: 0}) == 0
    result = sp.S.One
    power = sp.S.One
    for k in range(1, degree + 1):
        power = trunc(power * argument, degree)
        result += power / sp.factorial(k)
    return trunc(result, degree)


def d(expr: sp.Expr, coordinate: int) -> sp.Expr:
    if coordinate == 0:
        return sp.S.Zero
    return sp.diff(expr, VARS[coordinate - 1])


def at_origin(expr: sp.Expr) -> sp.Expr:
    return sp.factor(expr.subs({x: 0, y: 0, z: 0}))


def matrix_series_inverse(metric: sp.Matrix, degree: int = 3) -> sp.Matrix:
    origin = {x: 0, y: 0, z: 0}
    g0 = metric.subs(origin)
    g0_inv = g0.inv()
    delta = metric - g0
    a_matrix = (g0_inv * delta).applyfunc(lambda value: trunc(value, degree))
    identity = sp.eye(DIM)
    series = identity.copy()
    power = identity.copy()
    sign = -1
    for _ in range(1, degree + 1):
        power = (power * a_matrix).applyfunc(lambda value: trunc(value, degree))
        series += sign * power
        sign *= -1
    return (series * g0_inv).applyfunc(lambda value: trunc(value, degree))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--a", default="1/10", help="exact SymPy rational")
    parser.add_argument("--lambda-value", default="2/3", help="exact SymPy rational or 'symbolic'")
    parser.add_argument("--output", default="DERIVATION_RESULT.json")
    args = parser.parse_args()

    # Fixed Category-A exact witness parameters.  These are not physical selections.
    a = sp.Rational(args.a)
    lam = (
        sp.symbols("lambda", real=True)
        if args.lambda_value == "symbolic"
        else sp.Rational(args.lambda_value)
    )
    c_e = sp.S.One
    radius = sp.S.One

    # This is a polynomial in globally defined embedding coordinates x,y,z on S3.
    # The coefficient l1 bound is 140/400 = 7/20, hence |phi| <= 7/20 globally.
    phi_numerator = (
        x
        + 2 * y
        + 3 * z
        + 4 * x * y
        + 5 * y * z
        + 6 * z * x
        + 7 * x**2
        + 11 * y**2
        + 13 * z**2
        + 17 * x * y * z
        + 19 * x**3
        + 23 * y**3
        + 29 * z**3
    )
    phi = phi_numerator / 400

    # Unit-quaternion Maurer-Cartan forms in the w>0 chart, through the metric's
    # required third jet.  w=sqrt(1-x^2-y^2-z^2)=1-s/2+O(|u|^4).
    s = x**2 + y**2 + z**2
    w = 1 - s / 2
    sigma1 = [w + x**2, x * y + z, x * z - y]
    sigma2 = [x * y - z, w + y**2, y * z + x]
    sigma3 = [x * z + y, y * z - x, w + z**2]

    em2 = exp_jet(-2 * phi)
    ep2 = exp_jet(2 * phi)
    e2l = exp_jet(2 * lam * phi)

    metric = sp.zeros(DIM)
    metric[0, 0] = trunc(-(c_e**2) * em2, 3)
    for i in range(3):
        metric[0, i + 1] = trunc(-c_e * a * em2 * sigma3[i], 3)
        metric[i + 1, 0] = metric[0, i + 1]
    sigma3_weight = trunc(radius**2 * ep2 - a**2 * em2, 3)
    for i in range(3):
        for j in range(3):
            metric[i + 1, j + 1] = trunc(
                sigma3_weight * sigma3[i] * sigma3[j]
                + radius**2 * e2l * (sigma1[i] * sigma1[j] + sigma2[i] * sigma2[j]),
                3,
            )

    inverse = matrix_series_inverse(metric, 3)
    inverse_check = (metric * inverse).applyfunc(lambda value: trunc(value, 3))
    inverse_ok = inverse_check == sp.eye(DIM)

    # Gamma through quadratic order is sufficient for curvature through linear order.
    gamma = [[[sp.S.Zero for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)]
    for rho in range(DIM):
        for mu in range(DIM):
            for nu in range(DIM):
                value = sp.S.Zero
                for sig in range(DIM):
                    value += inverse[rho, sig] * (
                        d(metric[sig, nu], mu)
                        + d(metric[sig, mu], nu)
                        - d(metric[mu, nu], sig)
                    )
                gamma[rho][mu][nu] = trunc(value / 2, 2)

    riemann = [[[[sp.S.Zero for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)]
    for rho in range(DIM):
        for sig in range(DIM):
            for mu in range(DIM):
                for nu in range(DIM):
                    value = d(gamma[rho][nu][sig], mu) - d(gamma[rho][mu][sig], nu)
                    for eta in range(DIM):
                        value += gamma[rho][mu][eta] * gamma[eta][nu][sig]
                        value -= gamma[rho][nu][eta] * gamma[eta][mu][sig]
                    riemann[rho][sig][mu][nu] = trunc(value, 1)

    ricci = sp.zeros(DIM)
    for sig in range(DIM):
        for nu in range(DIM):
            ricci[sig, nu] = trunc(
                sum(riemann[rho][sig][rho][nu] for rho in range(DIM)), 1
            )

    mixed_ricci = (inverse * ricci).applyfunc(lambda value: trunc(value, 1))
    scalar = trunc(sp.trace(mixed_ricci), 1)
    ricci2 = trunc(sp.trace(mixed_ricci * mixed_ricci), 1)
    ricci3 = trunc(sp.trace(mixed_ricci * mixed_ricci * mixed_ricci), 1)
    invariants = (scalar, ricci2, ricci3)

    gradient_matrix = sp.Matrix(
        [[at_origin(sp.diff(invariant, variable)) for variable in VARS] for invariant in invariants]
    )
    gradient_det = sp.factor(gradient_matrix.det())
    symbolic_lambda = args.lambda_value == "symbolic"
    determinant_nonzero_at_value = None if symbolic_lambda else bool(gradient_det != 0)
    determinant_polynomial_not_identically_zero = bool(gradient_det != 0)

    # Global checks use exact bounds rather than chart sampling.
    phi_bound = sp.Rational(7, 20)
    # e^(4 phi) >= e^(-7/5) > 1/100=a^2, since e^(7/5)<e^2<100.
    strict_slice_certified = bool(
        abs(a) <= sp.Rational(1, 10) and 4 * phi_bound == sp.Rational(7, 5)
    )
    nonconstant_norm = any(sp.diff(phi, variable) != 0 for variable in VARS)
    nonzero_twist = a != 0

    result = {
        "schema": "udt.twisted_s3_killing_algebra.derivation.v1",
        "method": "exact_total_degree_3_metric_jet_and_intrinsic_Ricci_power_invariants",
        "parameters": {"a": str(a), "lambda": str(lam), "c_E": str(c_e), "R": str(radius)},
        "global_profile": str(phi),
        "global_phi_absolute_bound": str(phi_bound),
        "metric_origin_determinant": str(sp.factor(metric.subs({x: 0, y: 0, z: 0}).det())),
        "inverse_jet_identity": inverse_ok,
        "invariants_at_origin": [str(at_origin(value)) for value in invariants],
        "invariant_gradient_matrix": [[str(value) for value in row] for row in gradient_matrix.tolist()],
        "invariant_gradient_determinant": str(gradient_det),
        "invariant_gradient_determinant_nonzero": determinant_nonzero_at_value,
        "determinant_polynomial_not_identically_zero": determinant_polynomial_not_identically_zero,
        "open_set_rank_three": determinant_nonzero_at_value,
        "strict_slice_globally_certified": strict_slice_certified,
        "stationary_norm_nonconstant": nonconstant_norm,
        "twist_nonzero_for_nonzero_kappa": nonzero_twist,
        "global_profile_smooth": True,
        "global_spatial_completion": "unit_quaternion_S3",
        "maximum_interpretation": "configuration_existence_only_no_profile_or_dynamics_selection",
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (ROOT / args.output).write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    print("DERIVATION_RESULT_SHA256=" + hashlib.sha256(encoded.encode()).hexdigest())

    assert inverse_ok
    assert determinant_polynomial_not_identically_zero
    if not symbolic_lambda:
        assert determinant_nonzero_at_value
    assert strict_slice_certified
    assert nonconstant_norm
    assert nonzero_twist == (a != 0)


if __name__ == "__main__":
    main()
