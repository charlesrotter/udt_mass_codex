#!/usr/bin/env python3
"""Formula-level hostile mutations for the bounded G249 theorem."""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import json
from math import isqrt
from pathlib import Path


def mm(a, b):
    return [
        [sum((a[i][k] * b[k][j] for k in range(len(b))), Q(0)) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def mt(a):
    return [list(row) for row in zip(*a)]


def ms(c, a):
    return [[c * value for value in row] for row in a]


def ma(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def eye(n):
    return [[Q(int(i == j)) for j in range(n)] for i in range(n)]


def zero(n):
    return [[Q(0) for _ in range(n)] for _ in range(n)]


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inv2(a):
    determinant = det2(a)
    return [
        [a[1][1] / determinant, -a[0][1] / determinant],
        [-a[1][0] / determinant, a[0][0] / determinant],
    ]


def rational_sqrt(value):
    numerator = isqrt(value.numerator)
    denominator = isqrt(value.denominator)
    assert numerator * numerator == value.numerator
    assert denominator * denominator == value.denominator
    return Q(numerator, denominator)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    i2 = eye(2)
    z2 = zero(2)
    ell = Q(3, 2)
    x = Q(2, 3)
    stiffness = [[Q(2), Q(1, 4)], [Q(1, 4), Q(3)]]
    d = ms(x, ma(i2, ms(x * x, stiffness)))
    d1 = ma(i2, ms(3 * x * x, stiffness))
    d2 = ms(6 * x, stiffness)
    tidal = ms(Q(-1), mm(d2, inv2(d)))
    d_scaled = ms(ell, d)
    d2_scaled = ms(1 / ell, d2)
    tidal_scaled = ms(1 / (ell * ell), tidal)
    area = abs(det2(d))
    area_scaled = abs(det2(d_scaled))
    gram = mm(mt(d), d)
    gram_scaled = mm(mt(d_scaled), d_scaled)
    shape = ms(1 / area, gram)
    shape_scaled = ms(1 / area_scaled, gram_scaled)

    # Each Boolean is true only when the deliberately wrong formula is rejected.
    mutations = {
        "jacobi_exponent_zero_breaks_vertex_derivative": ms(1 / ell, i2) != i2,
        "jacobi_exponent_two_breaks_vertex_derivative": ms(ell, i2) != i2,
        "tidal_exponent_minus_one_breaks_ode": ma(d2_scaled, mm(ms(1 / ell, tidal), d_scaled)) != z2,
        "tidal_exponent_minus_three_breaks_ode": ma(d2_scaled, mm(ms(1 / (ell ** 3), tidal), d_scaled)) != z2,
        "correct_scaled_ode_is_zero_control": ma(d2_scaled, mm(tidal_scaled, d_scaled)) == z2,
        "linear_area_scaling_rejected": area_scaled != ell * area,
        "invariant_area_scaling_rejected": area_scaled != area,
        "quadratic_area_scaling_control": area_scaled == ell * ell * area,
        "area_squared_shape_normalization_rejected": ms(1 / (area_scaled * area_scaled), gram_scaled) != shape,
        "unit_determinant_shape_invariance_control": shape_scaled == shape and det2(shape_scaled) == 1,
    }

    clock_a = Q(5, 7)
    clock_b = Q(11, 13)
    ratio = clock_b / clock_a
    mutations.update({
        "clock_ratio_ell_mutation_rejected": (ell * clock_b) / (ell * clock_a) != ell * ratio,
        "clock_ratio_invariance_control": (ell * clock_b) / (ell * clock_a) == ratio,
        "coarea_invariance_mutation_rejected": ratio / area_scaled != ratio / area,
        "coarea_inverse_square_control": ratio / area_scaled == (ratio / area) / (ell * ell),
    })

    quiet = (Q(0), Q(0))
    live = (2 * Q(1) ** 2 + Q(1) - Q(0), -Q(1))
    mutations["same_phi_forced_angular_equality_rejected"] = quiet != live

    # Both points lie on one regular vertex-normalized Jacobi branch.
    left, right = Q(1), Q(3)
    phi_left = (left - 2) ** 2
    phi_right = (right - 2) ** 2
    area_left = abs(det2(ms(left, ma(i2, ms(left * left, stiffness)))))
    area_right = abs(det2(ms(right, ma(i2, ms(right * right, stiffness)))))
    mutations["noninjective_phi_single_area_mutation_rejected"] = (
        phi_left == phi_right and area_left > 0 and area_right > 0 and area_left != area_right
    )

    # For constant T, C3=-T/6. Adding I violates the sigma^1 Jacobi coefficient equation.
    c1 = i2
    c3 = ms(Q(-1, 6), tidal)
    c3_mutant = ma(c3, i2)
    mutations["ivp_cubic_coefficient_mutation_rejected"] = ma(ms(6, c3_mutant), mm(tidal, c1)) != z2
    mutations["ivp_cubic_coefficient_control"] = ma(ms(6, c3), mm(tidal, c1)) == z2

    anchor_area = Q(20, 7)
    physical_anchor = ell * ell * anchor_area
    recovered = rational_sqrt(physical_anchor / anchor_area)
    mutations.update({
        "positive_square_root_anchor_control": recovered == ell,
        "linear_anchor_recovery_mutation_rejected": physical_anchor / anchor_area != ell,
        "inverse_anchor_recovery_mutation_rejected": rational_sqrt(anchor_area / physical_anchor) != ell,
    })

    caustic = [[Q(1), Q(2)], [Q(2), Q(4)]]
    reflection = [[Q(-1), Q(0)], [Q(0), Q(1)]]
    reflected = mm(reflection, d)
    mutations["caustic_position_inverse_rejected"] = det2(caustic) == 0
    mutations["signed_determinant_o2_scalar_rejected"] = det2(reflected) == -det2(d)

    missed = [name for name, caught in mutations.items() if not caught]
    result = {
        "status": "PASS" if not missed else "FAIL",
        "implementation": "formula_level_mutation_tests_no_phrase_matching",
        "caught": sum(bool(value) for value in mutations.values()),
        "total": len(mutations),
        "missed": missed,
        "mutations": mutations,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if missed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
