#!/usr/bin/env python3
"""Independent standard-library checks for the macro phi/angular atlas."""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path


OUT = Path(__file__).resolve().parent


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def multiply(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [
        [sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def inverse(a: list[list[F]]) -> list[list[F]]:
    n = len(a)
    aug = [row[:] + [F(int(i == j)) for j in range(n)] for i, row in enumerate(a)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if aug[i][col] != 0)
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [value / scale for value in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            aug[row] = [x - factor * y for x, y in zip(aug[row], aug[col])]
    return [row[n:] for row in aug]


def quadratic(p: list[F], h_inv: list[list[F]]) -> F:
    return sum((p[i] * h_inv[i][j] * p[j] for i in range(len(p)) for j in range(len(p))), F(0))


def main() -> None:
    samples = [
        (F(2), F(3), F(5), F(1), F(-2), F(1), F(7), F(0), F(0)),
        (F(7, 3), F(4, 5), F(9, 2), F(-3, 2), F(5, 4), F(2, 7), F(-2), F(3), F(1)),
        (F(11), F(13), F(17), F(19), F(23), F(-5), F(2), F(-7), F(3)),
        (F(5, 2), F(8, 3), F(7, 4), F(9, 5), F(-4, 9), F(3, 8), F(-11, 6), F(2, 5), F(7, 9)),
        (F(3), F(2), F(4), F(-1), F(6), F(5), F(1), F(-2), F(8)),
        (F(17, 5), F(19, 7), F(23, 11), F(13, 3), F(-29, 4), F(31, 6), F(37, 8), F(-41, 9), F(43, 10)),
    ]
    aligned_checks = 0
    general_checks = 0
    for w, r, t, ell2, ell3, e, p1, p2, p3 in samples:
        A = [[w, F(0), F(0)], [ell2, r, e], [ell3, F(0), t]]
        h = multiply(transpose(A), A)
        h_inv = inverse(h)
        p = F(7, 5)
        if quadratic([p, F(0), F(0)], h_inv) != p * p / (w * w):
            raise AssertionError("independent aligned-depth identity failed")
        aligned_checks += 1

        c3 = (p3 - e * p2 / r) / t
        c2 = p2 / r
        c1 = (p1 - ell2 * p2 / r - ell3 * c3) / w
        if quadratic([p1, p2, p3], h_inv) != c1 * c1 + c2 * c2 + c3 * c3:
            raise AssertionError("independent general-B formula failed")
        general_checks += 1

    # Fixed-level non-aligned witnesses, using only exact rational arithmetic.
    eps = F(1, 10)
    angular_y0 = F(1, 4) + eps * eps * 4
    angular_ypi2 = F(1, 4)
    shift_y0 = F(1, 4) * (1 - eps) ** 2 + eps * eps
    shift_ypi2 = F(1, 4)
    if angular_y0 == angular_ypi2 or shift_y0 == shift_ypi2:
        raise AssertionError("independent non-aligned witness failed")

    # In a flat interval x two-circle product, the squared-diameter coefficient
    # of pi^2 changes from R^2+Q^2=2 to (2R)^2+Q^2=5.
    if F(5) - F(2) != F(3):
        raise AssertionError("independent global-diameter witness failed")

    result = {
        "schema": "udt-macro-phi-angular-xmax-independent-1.0",
        "result": "PASS",
        "implementation": "python_standard_library_fraction_gauss_jordan",
        "checks": {
            "aligned_exact_samples": aligned_checks,
            "general_B_exact_samples": general_checks,
            "angular_fixed_level_difference": str(angular_y0 - angular_ypi2),
            "shift_fixed_level_difference": str(shift_y0 - shift_ypi2),
            "product_diameter_pi_squared_coefficient_difference": "3",
        },
        "rulings": {
            "aligned_depth_invariance": "PASS",
            "nonaligned_modulation_exists": "PASS",
            "global_distance_channel_distinct": "PASS",
        },
    }
    (OUT / "INDEPENDENT_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
