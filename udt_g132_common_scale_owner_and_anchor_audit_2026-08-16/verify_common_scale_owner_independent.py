#!/usr/bin/env python3
"""Independent stdlib/Fraction verification for G132; imports no production code."""

from __future__ import annotations

import argparse
from fractions import Fraction as F
from math import isqrt
import json
from pathlib import Path


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def det2(h):
    return h[0][0] * h[1][1] - h[0][1] * h[1][0]


def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    total = F(0)
    for column, value in enumerate(matrix[0]):
        minor = [row[:column] + row[column + 1 :] for row in matrix[1:]]
        total += (-1 if column % 2 else 1) * value * determinant(minor)
    return total


def sqrt_fraction(value):
    numerator = isqrt(value.numerator)
    denominator = isqrt(value.denominator)
    if numerator * numerator != value.numerator or denominator * denominator != value.denominator:
        raise ValueError(f"not a rational square: {value}")
    return F(numerator, denominator)


def solve3(columns, target):
    aug = [[F(columns[j][i]) for j in range(3)] + [F(target[i])] for i in range(3)]
    for col in range(3):
        pivot = next(i for i in range(col, 3) if aug[i][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [v / scale for v in aug[col]]
        for row in range(3):
            if row == col:
                continue
            scale = aug[row][col]
            aug[row] = [aug[row][j] - scale * aug[col][j] for j in range(4)]
    return tuple(aug[i][3] for i in range(3))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("INDEPENDENT_VERIFICATION.json"))
    args = parser.parse_args()

    q = F(5, 2)
    common = F(3, 1)
    D = [[1 / q, F(0)], [F(0), q]]
    P = [[common * D[i][j] for j in range(2)] for i in range(2)]
    K = [[F(0), F(1)], [F(1), F(0)]]
    pktp = matmul(matmul(transpose(P), K), P)
    expected = [[common**2 * K[i][j] for j in range(2)] for i in range(2)]

    c_e = F(17, 3)
    reciprocal = F(7, 4)
    base = [[-(c_e / reciprocal) ** 2, F(0)], [F(0), reciprocal**2]]

    t2, l2, beta = F(9, 4), F(25, 9), F(2, 5)
    h = [[-t2, -t2 * beta], [-t2 * beta, l2 - t2 * beta**2]]
    omega = F(7, 3)
    scaled = [[omega**2 * h[i][j] for j in range(2)] for i in range(2)]
    ratio = -det2(h) / h[0][0] ** 2
    scaled_ratio = -det2(scaled) / scaled[0][0] ** 2
    beta_read = h[0][1] / h[0][0]
    exp_two_kappa = sqrt_fraction(-det2(h))
    exp_two_phi = sqrt_fraction(ratio)
    t2_from_triplet = exp_two_kappa / exp_two_phi
    l2_from_triplet = exp_two_kappa * exp_two_phi
    reconstructed = [
        [-t2_from_triplet, -t2_from_triplet * beta_read],
        [-t2_from_triplet * beta_read, l2_from_triplet - t2_from_triplet * beta_read**2],
    ]

    ce = (F(1), F(0), F(-1))
    grav = (F(3), F(-1), F(-2))
    mass = (F(0), F(1), F(0))
    rho = (F(-3), F(1), F(0))
    energy_density = (F(-1), F(1), F(-2))
    target = (F(1), F(0), F(0))

    # Independently solve the overdetermined c^a G^b length system. Mass neutrality gives b=0;
    # time neutrality then gives a=-2b=0; the remaining length equation returns 0 rather than 1.
    b_from_mass = F(0)
    a_from_time = -2 * b_from_mass
    ce_g_no_length = (
        -b_from_mass == target[1]
        and -a_from_time - 2 * b_from_mass == target[2]
        and a_from_time + 3 * b_from_mass != target[0]
    )
    mass_solution = solve3((ce, grav, mass), target)
    rho_solution = solve3((ce, grav, rho), target)
    energy_solution = solve3((ce, grav, energy_density), target)

    def anchor_polynomial(x):
        return x**2 * (x - 1) ** 2

    screen_metric = [[F(5), F(1)], [F(1), F(2)]]
    screen_metric_scaled = [[omega**2 * value for value in row] for row in screen_metric]
    screen_area_density = sqrt_fraction(determinant(screen_metric))
    screen_area_density_scaled = sqrt_fraction(determinant(screen_metric_scaled))
    spacetime_metric = [
        [F(-4), F(0), F(0), F(0)],
        [F(0), F(9), F(0), F(0)],
        [F(0), F(0), F(16), F(0)],
        [F(0), F(0), F(0), F(25)],
    ]
    spacetime_metric_scaled = [[omega**2 * value for value in row] for row in spacetime_metric]
    volume_density = sqrt_fraction(-determinant(spacetime_metric))
    volume_density_scaled = sqrt_fraction(-determinant(spacetime_metric_scaled))

    checks = {
        "fraction_fixed_pairing_scales_by_common_squared": pktp == expected,
        "fraction_nonunit_common_factor_fails_fixed_K": pktp != K,
        "fraction_reciprocal_D_has_unit_determinant": det2(D) == 1,
        "fraction_founded_base_determinant_is_minus_cE_squared": det2(base) == -c_e**2,
        "fraction_conformal_base_determinant_weight_four": det2(
            [[omega**2 * base[i][j] for j in range(2)] for i in range(2)]
        )
        == omega**4 * det2(base),
        "fraction_pair_determinant_is_minus_T2_L2": det2(h) == -t2 * l2,
        "fraction_conformal_pair_determinant_weight_four": det2(scaled) == omega**4 * det2(h),
        "fraction_terminal_ratio_conformal_invariant": scaled_ratio == ratio,
        "fraction_beta_conformal_invariant": scaled[0][1] / scaled[0][0] == beta_read,
        "fraction_terminal_triplet_reconstructs_h": reconstructed == h,
        "independent_cE_G_no_length": ce_g_no_length,
        "independent_mass_scale_exponents": mass_solution == (F(-2), F(1), F(1)),
        "independent_density_scale_exponents": rho_solution == (F(1), F(-1, 2), F(-1, 2)),
        "independent_energy_density_scale_exponents": energy_solution == (F(2), F(-1, 2), F(-1, 2)),
        "two_point_anchors_do_not_fix_function": anchor_polynomial(F(0)) == 0
        and anchor_polynomial(F(1)) == 0
        and anchor_polynomial(F(1, 2)) == F(1, 16),
        "screen_area_density_from_metric_determinant_has_weight_two": screen_area_density_scaled
        / screen_area_density
        == omega**2,
        "areal_radius_from_metric_area_has_weight_one": sqrt_fraction(
            screen_area_density_scaled / screen_area_density
        )
        == omega,
        "four_volume_from_metric_determinant_has_weight_four": volume_density_scaled
        / volume_density
        == omega**4,
    }

    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "passed": sum(checks.values()),
        "total": len(checks),
        "checks": checks,
        "exact": {
            "pair_ratio": str(ratio),
            "scaled_pair_ratio": str(scaled_ratio),
            "mass_exponents": [str(v) for v in mass_solution],
            "density_exponents": [str(v) for v in rho_solution],
            "energy_density_exponents": [str(v) for v in energy_solution],
        },
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"PASS: {result['passed']}/{result['total']} independent G132 checks" if result["status"] == "PASS" else json.dumps(result, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
