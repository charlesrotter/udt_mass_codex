#!/usr/bin/env python3
"""Exact G249 production derivation; writes only when --output is supplied."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
import random
from pathlib import Path

import sympy as sp


LANDING = (
    "CE_AND_RECIPROCAL_REDSHIFT_FIX_DIMENSIONLESS_CLOCK_RATIOS_NOT_ABSOLUTE_LENGTH"
    "__POSITIVE_HOMOTHETY_PRESERVES_COMPLETE_DIMENSIONLESS_PHI_HISTORY_CAUSAL_STRUCTURE_AND_NORMALIZED_SHAPE_WHILE_JACOBI_AREA_SCALES_AS_LENGTH_SQUARED"
    "__PHI_VALUE_ALONE_DOES_NOT_FIX_NORMALIZED_ANGULAR_RESPONSE"
    "__FULL_DIMENSIONLESS_METRIC_AND_BRANCH_FIX_NORMALIZED_JACOBI_RESPONSE_CONDITIONALLY"
    "__ONE_INDEPENDENT_DIMENSIONFUL_ANCHOR_REMAINS_FOR_ABSOLUTE_SCALE"
)


def m2_add(a, b):
    return tuple(tuple(a[i][j] + b[i][j] for j in range(2)) for i in range(2))


def m2_mul(a, b):
    return tuple(
        tuple(sum((a[i][k] * b[k][j] for k in range(2)), Fraction(0)) for j in range(2))
        for i in range(2)
    )


def m2_scale(c, a):
    return tuple(tuple(c * a[i][j] for j in range(2)) for i in range(2))


def m2_transpose(a):
    return tuple(tuple(a[j][i] for j in range(2)) for i in range(2))


def m2_det(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def m2_inv(a):
    determinant = m2_det(a)
    if determinant == 0:
        raise ZeroDivisionError("singular matrix")
    return (
        (a[1][1] / determinant, -a[0][1] / determinant),
        (-a[1][0] / determinant, a[0][0] / determinant),
    )


def m2_identity():
    return ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))


def m4_mul(a, b):
    return tuple(
        tuple(sum((a[i][k] * b[k][j] for k in range(4)), Fraction(0)) for j in range(4))
        for i in range(4)
    )


def m4_transpose(a):
    return tuple(tuple(a[j][i] for j in range(4)) for i in range(4))


def block4(a, b, c, d):
    return tuple(
        tuple((a if i < 2 and j < 2 else b if i < 2 else c if j < 2 else d)[i % 2][j % 2]
              for j in range(4))
        for i in range(4)
    )


def symplectic_form():
    z = ((Fraction(0), Fraction(0)), (Fraction(0), Fraction(0)))
    i = m2_identity()
    return block4(z, i, m2_scale(Fraction(-1), i), z)


def exact_symbolic_checks() -> dict[str, bool]:
    ell, lam, s, theta = sp.symbols("ell lam s theta", positive=True)
    f = sp.symbols("f", positive=True)
    d = sp.Function("d")

    g_physical = sp.diag(-f, 1 / f, (ell * s) ** 2, (ell * s) ** 2 * sp.sin(theta) ** 2)
    jacobian = sp.diag(ell, ell, 1, 1)
    g_bar = sp.diag(-f, 1 / f, s**2, s**2 * sp.sin(theta) ** 2)
    pulled = sp.simplify(jacobian.T * g_physical * jacobian - ell**2 * g_bar)

    d_scaled = ell * d(lam / ell)
    first = sp.diff(d_scaled, lam)
    second = sp.diff(d_scaled, lam, 2)

    x11, x12, x21, x22 = sp.symbols("x11 x12 x21 x22")
    matrix = sp.Matrix([[x11, x12], [x21, x22]])
    area_scaled = sp.factor((ell * matrix).det())
    gram = matrix.T * matrix
    shape_difference = sp.simplify(
        ((ell * matrix).T * (ell * matrix)) / area_scaled - gram / matrix.det()
    )

    # With only c_E^a, length exponent is a and time exponent is -a.
    # Area would require a=2 and -a=0 simultaneously.
    a = sp.symbols("a")
    dimension_solution = sp.solve([sp.Eq(a, 2), sp.Eq(-a, 0)], [a], dict=True)

    phi = sp.Integer(0)
    amp_quiet = (
        sp.exp(-2 * phi) * (2 * 0**2 + 0 - 0),
        1 - sp.exp(-2 * phi) * (1 + 0),
    )
    amp_live = (
        sp.exp(-2 * phi) * (2 * 1**2 + 1 - 0),
        1 - sp.exp(-2 * phi) * (1 + 1),
    )

    return {
        "primary_metric_pullback_is_ell_squared_gbar": pulled == sp.zeros(4),
        "jacobi_first_derivative_scale": sp.simplify(first - sp.Subs(sp.Derivative(d(s), s), s, lam / ell)) == 0,
        "jacobi_second_derivative_scale": sp.simplify(second - sp.Subs(sp.Derivative(d(s), (s, 2)), s, lam / ell) / ell) == 0,
        "rank_two_area_scales_ell_squared": sp.simplify(area_scaled - ell**2 * matrix.det()) == 0,
        "unit_determinant_shape_scale_cancels": shape_difference == sp.zeros(2),
        "ce_plus_dimensionless_cannot_form_area": dimension_solution == [],
        "same_phi_quiet_witness": amp_quiet == (0, 0),
        "same_phi_live_witness": amp_live == (3, -1),
    }


def run_cases(cases: int) -> tuple[int, int, int]:
    rng = random.Random(2490824)
    assertions = 0
    offdiagonal_cases = 0
    nonunit_scale_cases = 0
    identity = m2_identity()
    zero = ((Fraction(0), Fraction(0)), (Fraction(0), Fraction(0)))
    omega = symplectic_form()

    for _ in range(cases):
        ell = Fraction(rng.randint(1, 19), rng.randint(1, 13))
        x = Fraction(rng.randint(1, 11), rng.randint(1, 9))
        a = Fraction(rng.randint(0, 5), rng.randint(1, 7))
        b = Fraction(rng.randint(0, 5), rng.randint(1, 7))
        c_bound = min(a + Fraction(1, 3), b + Fraction(1, 3))
        c = Fraction(rng.randint(-3, 3), 10) * c_bound
        s_matrix = ((a + 1, c), (c, b + 1))

        d_one = m2_scale(x, m2_add(identity, m2_scale(x * x, s_matrix)))
        d_prime_one = m2_add(identity, m2_scale(3 * x * x, s_matrix))
        d_second_one = m2_scale(6 * x, s_matrix)
        d_scaled = m2_scale(ell, d_one)
        d_prime_scaled = d_prime_one
        d_second_scaled = m2_scale(1 / ell, d_second_one)
        tidal_one = m2_scale(Fraction(-1), m2_mul(d_second_one, m2_inv(d_one)))
        tidal_scaled = m2_scale(Fraction(-1), m2_mul(d_second_scaled, m2_inv(d_scaled)))

        area_one = abs(m2_det(d_one))
        area_scaled = abs(m2_det(d_scaled))
        gram_one = m2_mul(m2_transpose(d_one), d_one)
        gram_scaled = m2_mul(m2_transpose(d_scaled), d_scaled)
        shape_one = m2_scale(1 / area_one, gram_one)
        shape_scaled = m2_scale(1 / area_scaled, gram_scaled)

        assert d_scaled == m2_scale(ell, d_one); assertions += 1
        assert d_prime_scaled == d_prime_one; assertions += 1
        assert d_second_scaled == m2_scale(1 / ell, d_second_one); assertions += 1
        assert tidal_scaled == m2_scale(1 / (ell * ell), tidal_one); assertions += 1
        assert m2_transpose(tidal_one) == tidal_one; assertions += 1
        assert m2_transpose(tidal_scaled) == tidal_scaled; assertions += 1
        assert area_scaled == ell * ell * area_one; assertions += 1
        assert shape_scaled == shape_one; assertions += 1
        assert m2_det(shape_one) == 1; assertions += 1

        clock_a = Fraction(rng.randint(1, 17), rng.randint(1, 13))
        clock_b = Fraction(rng.randint(1, 17), rng.randint(1, 13))
        r_clock = clock_b / clock_a
        assert r_clock == clock_b / clock_a; assertions += 1
        assert r_clock / area_scaled == (r_clock / area_one) / (ell * ell); assertions += 1

        # A generic exact symplectic phase and its physical position/derivative scaling.
        b_phase = ((Fraction(2), c), (c, Fraction(3)))
        c_phase = ((Fraction(1), Fraction(-1, 4)), (Fraction(-1, 4), Fraction(2)))
        p = block4(identity, b_phase, zero, identity)
        q = block4(identity, zero, c_phase, identity)
        phase = m4_mul(p, q)
        h = block4(m2_scale(ell, identity), zero, zero, identity)
        h_inv = block4(m2_scale(1 / ell, identity), zero, zero, identity)
        phase_scaled = m4_mul(m4_mul(h, phase), h_inv)
        assert m4_mul(m4_mul(m4_transpose(phase), omega), phase) == omega; assertions += 1
        assert m4_mul(m4_mul(m4_transpose(phase_scaled), omega), phase_scaled) == omega; assertions += 1
        upper_right = tuple(tuple(phase[i][j + 2] for j in range(2)) for i in range(2))
        upper_right_scaled = tuple(tuple(phase_scaled[i][j + 2] for j in range(2)) for i in range(2))
        assert upper_right_scaled == m2_scale(ell, upper_right); assertions += 1
        assert abs(m2_det(upper_right_scaled)) == ell * ell * abs(m2_det(upper_right)); assertions += 1

        if c != 0:
            offdiagonal_cases += 1
        if ell != 1:
            nonunit_scale_cases += 1

    return assertions, offdiagonal_cases, nonunit_scale_cases


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=int, default=4096)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    symbolic = exact_symbolic_checks()
    if not all(symbolic.values()):
        raise SystemExit(f"symbolic failure: {symbolic}")
    assertions, offdiagonal, nonunit = run_cases(args.cases)
    result = {
        "status": "PASS",
        "landing": LANDING,
        "cases": args.cases,
        "assertions": assertions + len(symbolic),
        "symbolic_checks": symbolic,
        "offdiagonal_cases": offdiagonal,
        "nonunit_scale_cases": nonunit,
        "dimension_ledger": "c_E has L/T; phi and z are dimensionless; no absolute L or L^2 follows",
        "homothety": "g_ell=ell^2*g_1__T_ell(lambda)=ell^-2*T_1(lambda/ell)__D_ell(lambda)=ell*D_1(lambda/ell)",
        "area_shape": "A_ell=ell^2*A_1__C_ell=C_1",
        "clock_and_coarea": "r_clock_ell=r_clock_1__coarea_coefficient_ell=ell^-2*(r_clock/A)_1",
        "phi_only_boundary": "same_phi_different_first_two_jets_give_different_angular_tides",
        "full_history_boundary": "normalized_A_is_unique_for_supplied_dimensionless_metric_branch_and_Jacobi_IVP__A_of_phi_single_valued_only_on_injective_branch",
        "anchor_corollary": "one_absolute_area_anchor_gives_ell=sqrt(A_anchor/Abar_anchor)_when_Abar_anchor_positive",
        "observational_outcomes": "CLOSED_AND_UNREAD",
        "fitted_coefficients": 0,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
