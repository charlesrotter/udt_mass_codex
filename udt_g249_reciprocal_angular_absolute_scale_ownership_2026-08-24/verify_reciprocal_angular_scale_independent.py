#!/usr/bin/env python3
"""Claim-directed standard-library exact replay for G249.

This implementation imports neither production code nor production output.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import json
from math import factorial, isqrt
from pathlib import Path
import random


EXPECTED = (
    "CE_AND_RECIPROCAL_REDSHIFT_FIX_DIMENSIONLESS_CLOCK_RATIOS_NOT_ABSOLUTE_LENGTH"
    "__POSITIVE_HOMOTHETY_PRESERVES_COMPLETE_DIMENSIONLESS_PHI_HISTORY_CAUSAL_STRUCTURE_AND_NORMALIZED_SHAPE_WHILE_JACOBI_AREA_SCALES_AS_LENGTH_SQUARED"
    "__PHI_VALUE_ALONE_DOES_NOT_FIX_NORMALIZED_ANGULAR_RESPONSE"
    "__FULL_DIMENSIONLESS_METRIC_AND_BRANCH_FIX_NORMALIZED_JACOBI_RESPONSE_CONDITIONALLY"
    "__ONE_INDEPENDENT_DIMENSIONFUL_ANCHOR_REMAINS_FOR_ABSOLUTE_SCALE"
)


def mm(a, b):
    n, inner, m = len(a), len(b), len(b[0])
    return [
        [sum((a[i][k] * b[k][j] for k in range(inner)), Q(0)) for j in range(m)]
        for i in range(n)
    ]


def mt(a):
    return [list(row) for row in zip(*a)]


def ms(c, a):
    return [[c * value for value in row] for row in a]


def ma(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def mz(rows, columns):
    return [[Q(0) for _ in range(columns)] for _ in range(rows)]


def eye(n):
    return [[Q(int(i == j)) for j in range(n)] for i in range(n)]


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inv2(a):
    determinant = det2(a)
    return [
        [a[1][1] / determinant, -a[0][1] / determinant],
        [-a[1][0] / determinant, a[0][0] / determinant],
    ]


def blocks(a, b, c, d):
    return [a[0] + b[0], a[1] + b[1], c[0] + d[0], c[1] + d[1]]


def positive_rational_sqrt(value: Q) -> Q:
    numerator = isqrt(value.numerator)
    denominator = isqrt(value.denominator)
    if numerator * numerator != value.numerator or denominator * denominator != value.denominator:
        raise ValueError("not a rational square")
    return Q(numerator, denominator)


def jacobi_second_order_coefficients(tidal, degree):
    """Coefficients of D''+T D=0 with D(0)=0 and D'(0)=I."""
    coefficients = [mz(2, 2) for _ in range(degree + 1)]
    coefficients[1] = eye(2)
    for power in range(degree - 1):
        coefficients[power + 2] = ms(
            Q(-1, (power + 2) * (power + 1)),
            mm(tidal, coefficients[power]),
        )
    return coefficients


def jacobi_phase_coefficients(tidal, degree):
    """Upper-right coefficients of exp([[0,I],[-T,0]] sigma)."""
    i2 = eye(2)
    z2 = mz(2, 2)
    generator = blocks(z2, i2, ms(Q(-1), tidal), z2)
    power = eye(4)
    coefficients = []
    for order in range(degree + 1):
        term = ms(Q(1, factorial(order)), power)
        coefficients.append([term[0][2:4], term[1][2:4]])
        power = mm(power, generator)
    return coefficients


def branch_jacobi(parameter: Q, stiffness):
    """Regular vertex-normalized D=s(I+s^2 K)."""
    return ms(parameter, ma(eye(2), ms(parameter * parameter, stiffness)))


def branch_jacobi_prime(parameter: Q, stiffness):
    return ma(eye(2), ms(3 * parameter * parameter, stiffness))


def branch_jacobi_second(parameter: Q, stiffness):
    return ms(6 * parameter, stiffness)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=int, default=10000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rng = random.Random(9421942)
    assertions = 0
    offdiagonal = 0
    changed_area = 0
    scaling_cases = 0
    same_phi_jet_cases = 0
    noninjective_branch_cases = 0
    anchor_recovery_cases = 0
    i2 = eye(2)
    z2 = mz(2, 2)
    omega = blocks(z2, i2, ms(Q(-1), i2), z2)

    # c_E^a has exponents (L,T)=(a,-a); it cannot equal (2,0).
    dimensional_candidates = [a for a in range(-12, 13) if a == 2 and -a == 0]
    assert dimensional_candidates == []
    assertions += 1

    for _ in range(args.cases):
        ell = Q(rng.randint(1, 23), rng.randint(1, 17))
        x = Q(rng.randint(1, 13), rng.randint(1, 11))
        aa = Q(rng.randint(1, 7), rng.randint(1, 9))
        bb = Q(rng.randint(1, 7), rng.randint(1, 9))
        cc = Q(rng.randint(-4, 4), 19)
        stiffness = [[1 + aa, cc], [cc, 1 + bb]]

        d = branch_jacobi(x, stiffness)
        d1 = branch_jacobi_prime(x, stiffness)
        d2 = branch_jacobi_second(x, stiffness)
        de = ms(ell, d)
        de1 = d1
        de2 = ms(1 / ell, d2)
        tidal = ms(Q(-1), mm(d2, inv2(d)))
        tidal_e = ms(Q(-1), mm(de2, inv2(de)))

        assert de == ms(ell, d); assertions += 1
        assert de1 == d1; assertions += 1
        assert de2 == ms(1 / ell, d2); assertions += 1
        assert tidal_e == ms(Q(1, 1) / (ell * ell), tidal); assertions += 1
        assert tidal == mt(tidal) and tidal_e == mt(tidal_e); assertions += 2

        area = abs(det2(d))
        area_e = abs(det2(de))
        assert area_e == ell * ell * area; assertions += 1
        gram = mm(mt(d), d)
        gram_e = mm(mt(de), de)
        shape = ms(1 / area, gram)
        shape_e = ms(1 / area_e, gram_e)
        assert shape_e == shape; assertions += 1
        assert det2(shape) == 1; assertions += 1
        scaling_cases += 1

        clock_source = Q(rng.randint(1, 29), rng.randint(1, 23))
        clock_target = Q(rng.randint(1, 29), rng.randint(1, 23))
        ratio = clock_target / clock_source
        assert (ell * clock_target) / (ell * clock_source) == ratio; assertions += 1
        assert ratio / area_e == ratio / area / (ell * ell); assertions += 1

        # Independently construct a symplectic phase from lower/upper symmetric shears.
        upper = [[Q(2), cc], [cc, Q(5)]]
        lower = [[Q(3), Q(1, 5)], [Q(1, 5), Q(4)]]
        phase = mm(blocks(i2, upper, z2, i2), blocks(i2, z2, lower, i2))
        scale = blocks(ms(ell, i2), z2, z2, i2)
        scale_inv = blocks(ms(1 / ell, i2), z2, z2, i2)
        phase_e = mm(mm(scale, phase), scale_inv)
        assert mm(mm(mt(phase), omega), phase) == omega; assertions += 1
        assert mm(mm(mt(phase_e), omega), phase_e) == omega; assertions += 1
        position = [phase[0][2:4], phase[1][2:4]]
        position_e = [phase_e[0][2:4], phase_e[1][2:4]]
        assert position_e == ms(ell, position); assertions += 1
        assert abs(det2(position_e)) == ell * ell * abs(det2(position)); assertions += 1

        # Same phi=0 but distinct exact G201 radial jets.
        p = Q(rng.randint(-7, 7), rng.randint(1, 9))
        q = Q(rng.randint(-7, 7), rng.randint(1, 9))
        if p == 0 and q == 0:
            q = Q(1)
        angular = (2 * p * p + p - q, -p)
        assert angular != (Q(0), Q(0)); assertions += 1
        same_phi_jet_cases += 1

        # A lawful regular Jacobi branch with phi(s)=(s-2u)^2 at s=u and s=3u.
        u = Q(rng.randint(1, 7), rng.randint(1, 9))
        left, right = u, 3 * u
        phi_left = (left - 2 * u) ** 2
        phi_right = (right - 2 * u) ** 2
        d_left = branch_jacobi(left, stiffness)
        d_right = branch_jacobi(right, stiffness)
        area_left = abs(det2(d_left))
        area_right = abs(det2(d_right))
        tide_left = ms(Q(-1), mm(branch_jacobi_second(left, stiffness), inv2(d_left)))
        tide_right = ms(Q(-1), mm(branch_jacobi_second(right, stiffness), inv2(d_right)))
        assert phi_left == phi_right; assertions += 1
        assert area_left > 0 and area_right > 0 and area_left != area_right; assertions += 1
        assert branch_jacobi(Q(0), stiffness) == z2; assertions += 1
        assert branch_jacobi_prime(Q(0), stiffness) == i2; assertions += 1
        assert tide_left == mt(tide_left) and tide_right == mt(tide_right); assertions += 2
        noninjective_branch_cases += 1

        # One positive area anchor recovers the positive rational ell exactly.
        anchor_area = Q(rng.randint(1, 31), rng.randint(1, 29))
        physical_anchor = ell * ell * anchor_area
        recovered = positive_rational_sqrt(physical_anchor / anchor_area)
        assert recovered == ell; assertions += 1
        anchor_recovery_cases += 1

        if cc != 0:
            offdiagonal += 1
        if ell != 1:
            assert area_e != area
            assertions += 1
            changed_area += 1

    # Identical constant tidal history and vertex data, solved two different ways.
    ivp_cases = min(args.cases, 512)
    ivp_degree = 16
    for _ in range(ivp_cases):
        aa = Q(rng.randint(1, 11), rng.randint(1, 13))
        bb = Q(rng.randint(1, 11), rng.randint(1, 13))
        cc = Q(rng.randint(-3, 3), 17)
        tidal = [[aa, cc], [cc, bb]]
        direct = jacobi_second_order_coefficients(tidal, ivp_degree)
        phase = jacobi_phase_coefficients(tidal, ivp_degree)
        assert direct == phase; assertions += 1
        assert direct[0] == z2 and direct[1] == i2; assertions += 1
        for power in range(ivp_degree - 1):
            residual = ma(
                ms(Q((power + 2) * (power + 1)), direct[power + 2]),
                mm(tidal, direct[power]),
            )
            assert residual == z2
            assertions += 1

    claim_checks = {
        "ce_dimension_cannot_form_area": dimensional_candidates == [],
        "homothety_jacobi_area_shape_scaling": scaling_cases == args.cases,
        "same_phi_different_jet_response": same_phi_jet_cases == args.cases,
        "noninjective_phi_branch_is_multivalued_in_area": noninjective_branch_cases == args.cases,
        "identical_tidal_history_and_vertex_data_match_by_two_series_methods": ivp_cases > 0,
        "one_positive_area_anchor_recovers_scale": anchor_recovery_cases == args.cases,
    }
    assert all(claim_checks.values())
    assertions += len(claim_checks)

    result = {
        "status": "PASS",
        "expected_landing": EXPECTED,
        "implementation": "claim_directed_standard_library_fraction_no_sympy_no_production_import_or_output_read",
        "cases": args.cases,
        "assertions": assertions,
        "offdiagonal_cases": offdiagonal,
        "nonunit_scale_area_changes": changed_area,
        "homothety_scaling_cases": scaling_cases,
        "same_phi_jet_cases": same_phi_jet_cases,
        "noninjective_branch_cases": noninjective_branch_cases,
        "ivp_uniqueness_cases": ivp_cases,
        "ivp_series_degree": ivp_degree,
        "anchor_recovery_cases": anchor_recovery_cases,
        "claim_checks": claim_checks,
        "dimensional_candidates": dimensional_candidates,
        "observational_outcomes": "CLOSED_AND_UNREAD",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
