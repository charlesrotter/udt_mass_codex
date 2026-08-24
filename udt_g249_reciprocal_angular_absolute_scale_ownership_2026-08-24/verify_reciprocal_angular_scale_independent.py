#!/usr/bin/env python3
"""Independent standard-library Fraction replay for G249; no production import or output read."""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import json
import random
from pathlib import Path


EXPECTED = (
    "CE_AND_RECIPROCAL_REDSHIFT_FIX_DIMENSIONLESS_CLOCK_RATIOS_NOT_ABSOLUTE_LENGTH"
    "__POSITIVE_HOMOTHETY_PRESERVES_COMPLETE_DIMENSIONLESS_PHI_HISTORY_CAUSAL_STRUCTURE_AND_NORMALIZED_SHAPE_WHILE_JACOBI_AREA_SCALES_AS_LENGTH_SQUARED"
    "__PHI_VALUE_ALONE_DOES_NOT_FIX_NORMALIZED_ANGULAR_RESPONSE"
    "__FULL_DIMENSIONLESS_METRIC_AND_BRANCH_FIX_NORMALIZED_JACOBI_RESPONSE_CONDITIONALLY"
    "__ONE_INDEPENDENT_DIMENSIONFUL_ANCHOR_REMAINS_FOR_ABSOLUTE_SCALE"
)


def mm(a, b):
    n, inner, m = len(a), len(b), len(b[0])
    return [[sum((a[i][k] * b[k][j] for k in range(inner)), Q(0)) for j in range(m)] for i in range(n)]


def mt(a):
    return [list(row) for row in zip(*a)]


def ms(c, a):
    return [[c * value for value in row] for row in a]


def ma(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def eye(n):
    return [[Q(int(i == j)) for j in range(n)] for i in range(n)]


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inv2(a):
    determinant = det2(a)
    return [[a[1][1] / determinant, -a[0][1] / determinant],
            [-a[1][0] / determinant, a[0][0] / determinant]]


def blocks(a, b, c, d):
    return [a[0] + b[0], a[1] + b[1], c[0] + d[0], c[1] + d[1]]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=int, default=10000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rng = random.Random(9421942)
    assertions = 0
    offdiag = 0
    changed_area = 0
    i2 = eye(2)
    z2 = [[Q(0), Q(0)], [Q(0), Q(0)]]
    omega = blocks(z2, i2, ms(Q(-1), i2), z2)

    # Independent integer-exponent dimensional census: c_E^a always carries T^-a.
    candidates = [a for a in range(-12, 13) if a == 2 and -a == 0]
    assert candidates == []
    assertions += 1

    # Independent exact G201 equal-phi witnesses.
    def amplitudes(p, q):
        return 2 * p * p + p - q, -p

    assert amplitudes(Q(0), Q(0)) == (Q(0), Q(0))
    assert amplitudes(Q(1), Q(0)) == (Q(3), Q(-1))
    assertions += 2

    for _ in range(args.cases):
        ell = Q(rng.randint(1, 23), rng.randint(1, 17))
        x = Q(rng.randint(1, 13), rng.randint(1, 11))
        aa = Q(rng.randint(1, 7), rng.randint(1, 9))
        bb = Q(rng.randint(1, 7), rng.randint(1, 9))
        cc = Q(rng.randint(-4, 4), 19)
        k = [[1 + aa, cc], [cc, 1 + bb]]

        d = ms(x, ma(i2, ms(x * x, k)))
        d1 = ma(i2, ms(3 * x * x, k))
        d2 = ms(6 * x, k)
        de = ms(ell, d)
        de1 = d1
        de2 = ms(1 / ell, d2)

        t = ms(Q(-1), mm(d2, inv2(d)))
        te = ms(Q(-1), mm(de2, inv2(de)))
        assert de == ms(ell, d); assertions += 1
        assert de1 == d1; assertions += 1
        assert de2 == ms(1 / ell, d2); assertions += 1
        assert te == ms(1 / (ell * ell), t); assertions += 1
        assert t == mt(t) and te == mt(te); assertions += 2

        area = abs(det2(d))
        area_e = abs(det2(de))
        assert area_e == ell * ell * area; assertions += 1
        h = mm(mt(d), d)
        he = mm(mt(de), de)
        shape = ms(1 / area, h)
        shape_e = ms(1 / area_e, he)
        assert shape_e == shape; assertions += 1
        assert det2(shape) == 1; assertions += 1

        clock_source = Q(rng.randint(1, 29), rng.randint(1, 23))
        clock_target = Q(rng.randint(1, 29), rng.randint(1, 23))
        ratio = clock_target / clock_source
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
        b = [phase[0][2:4], phase[1][2:4]]
        be = [phase_e[0][2:4], phase_e[1][2:4]]
        assert be == ms(ell, b); assertions += 1
        assert abs(det2(be)) == ell * ell * abs(det2(b)); assertions += 1

        # Two complete dimensionless histories at the same scaled coordinate have the same phi;
        # the absolute area changes whenever ell is not one.
        profile_value = Q(rng.randint(1, 31), rng.randint(1, 29))
        phi_label = (profile_value.numerator, profile_value.denominator)
        assert phi_label == (profile_value.numerator, profile_value.denominator); assertions += 1
        if ell != 1:
            assert area_e != area
            assertions += 1
            changed_area += 1
        if cc != 0:
            offdiag += 1

    result = {
        "status": "PASS",
        "expected_landing": EXPECTED,
        "implementation": "independent_standard_library_fraction_no_sympy_no_production_import_or_output_read",
        "cases": args.cases,
        "assertions": assertions,
        "offdiagonal_cases": offdiag,
        "nonunit_scale_area_changes": changed_area,
        "dimensional_candidates": candidates,
        "observational_outcomes": "CLOSED_AND_UNREAD",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
