#!/usr/bin/env python3
"""Independent Fraction-only verification; imports no production code or SymPy."""

from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent


def det2(a: tuple[int, int], b: tuple[int, int]) -> int:
    return a[0] * b[1] - a[1] * b[0]


def canonical(v: tuple[int, int]) -> tuple[int, int]:
    d = math.gcd(abs(v[0]), abs(v[1]))
    if d == 0:
        raise ValueError("zero")
    x, y = v[0] // d, v[1] // d
    return (-x, -y) if x < 0 or (x == 0 and y < 0) else (x, y)


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def matmul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def det3(a: list[list[F]]) -> F:
    return (
        a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
        - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
        + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
    )


def inverse(a: list[list[F]]) -> list[list[F]]:
    n = len(a)
    aug = [row[:] + [F(int(i == j)) for j in range(n)] for i, row in enumerate(a)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if aug[i][col] != 0)
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [v / scale for v in aug[col]]
        for i in range(n):
            if i == col:
                continue
            scale = aug[i][col]
            aug[i] = [x - scale * y for x, y in zip(aug[i], aug[col])]
    return [row[n:] for row in aug]


def trace(a: list[list[F]]) -> F:
    return sum(a[i][i] for i in range(len(a)))


def require(name: str, condition: bool, checks: list[str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks.append(name)


def gram(c: F, alpha: F, u: F, f: F, b: F) -> list[list[F]]:
    q = 1 / u - alpha * alpha * u
    return [
        [-c * c * u, -c * alpha * u, -c * alpha * u * f],
        [-c * alpha * u, q, q * f],
        [-c * alpha * u * f, q * f, q * f * f + b],
    ]


def xgram(c: F, alpha: F, u: F, f: F, b: F, chi: F, df: F, db: F) -> list[list[F]]:
    du = -2 * u * chi
    q = 1 / u - alpha * alpha * u
    dq = -du / (u * u) - alpha * alpha * du
    return [
        [-c * c * du, -c * alpha * du, -c * alpha * (du * f + u * df)],
        [-c * alpha * du, dq, dq * f + q * df],
        [-c * alpha * (du * f + u * df), dq * f + q * df, dq * f * f + 2 * q * f * df + db],
    ]


def expected_d(c: F, alpha: F, u: F, f: F, b: F, chi: F, df: F, db: F) -> list[list[F]]:
    return [
        [-2 * chi, -4 * alpha * chi / c, -4 * alpha * chi * f / c],
        [
            alpha * c * df * f * u / b,
            (alpha * alpha * df * f * u * u + 2 * b * chi * u - df * f) / (b * u),
            (
                alpha * alpha * df * f * f * u * u
                + 2 * b * chi * f * u
                + b * df * u
                - db * f * u
                - df * f * f
            )
            / (b * u),
        ],
        [
            -alpha * c * df * u / b,
            -df * (alpha * alpha * u * u - 1) / (b * u),
            -(alpha * alpha * df * f * u * u - db * u - df * f) / (b * u),
        ],
    ]


def main() -> None:
    checks: list[str] = []
    samples = [
        (F(2), F(1, 3), F(3, 2), F(-2, 5), F(7, 4), F(2, 7), F(3, 11), F(-5, 13)),
        (F(3), F(-2, 5), F(5, 3), F(1, 4), F(9, 5), F(-3, 8), F(-4, 9), F(7, 10)),
        (F(5, 2), F(0), F(4, 3), F(-1, 3), F(11, 6), F(5, 12), F(2, 9), F(1, 7)),
        (F(7, 3), F(3, 7), F(7, 5), F(3, 8), F(13, 9), F(-2, 9), F(5, 14), F(-3, 10)),
    ]

    for index, values in enumerate(samples, 1):
        c, alpha, u, f, b, chi, df, db = values
        g = gram(c, alpha, u, f, b)
        require(f"R{index:02d}_det", det3(g) == -b * c * c, checks)
        d = matmul(inverse(g), xgram(*values))
        require(f"R{index:02d}_D", d == expected_d(*values), checks)
        require(f"R{index:02d}_trace", trace(d) == db / b, checks)
        gd = matmul(g, d)
        require(f"R{index:02d}_self_adjoint", gd == transpose(gd), checks)

        tr = trace(d)
        d2 = matmul(d, d)
        s2 = (tr * tr - trace(d2)) / 2
        det_d = det3(d)
        expected_s2 = alpha * alpha * df * df * u / b - df * df / (b * u) - 4 * chi * chi
        expected_det = 2 * alpha * alpha * df * df * u * chi / b - 4 * db * chi * chi / b + 2 * df * df * chi / (b * u)
        require(f"R{index:02d}_char_s2", s2 == expected_s2, checks)
        require(f"R{index:02d}_char_det", det_d == expected_det, checks)

        def char_at(lam: F) -> F:
            return lam**3 - tr * lam**2 + s2 * lam - det_d

        require(f"R{index:02d}_char_minus", char_at(-2 * chi) == -4 * alpha * alpha * df * df * u * chi / b, checks)
        require(f"R{index:02d}_char_plus", char_at(2 * chi) == -4 * df * df * chi / (b * u), checks)

        # Direct plane-Gram determinants for a grid of all coefficients.
        for r, s, m, n in [
            (F(0), F(0), F(1), F(0)),
            (F(1, 2), F(-1, 3), F(2), F(1)),
            (F(-2, 3), F(3, 5), F(1), F(-2)),
            (F(4, 7), F(2, 9), F(-1), F(3)),
        ]:
            basis = [[F(1), F(0)], [r, m], [s, n]]
            h = matmul(transpose(basis), matmul(g, basis))
            direct = h[0][0] * h[1][1] - h[0][1] * h[1][0]
            delta = r * n - m * s
            z = m + n * f
            expected = b * delta * delta / u - c * c * z * z - u * b * (c * n + alpha * delta) ** 2
            require(f"R{index:02d}_plane_{r}_{s}_{m}_{n}", direct == expected, checks)

        # Direct differentiation of a generic Killing norm.
        t, p, q = F(5, 4), F(-2, 3), F(3, 5)
        sm = p + q * f
        du = -2 * u * chi
        norm = -u * (c * t + alpha * sm) ** 2 + sm * sm / u + q * q * b
        dnorm = (
            -du * (c * t + alpha * sm) ** 2
            - 2 * u * (c * t + alpha * sm) * alpha * q * df
            + 2 * sm * q * df / u
            - sm * sm * du / (u * u)
            + q * q * db
        )
        residual = dnorm + 2 * chi * norm
        expected_residual = (
            -2 * alpha * alpha * df * f * q * q * u * u
            - 2 * alpha * alpha * df * p * q * u * u
            - 2 * alpha * c * df * q * t * u * u
            + 2 * b * chi * q * q * u
            + 4 * chi * f * f * q * q
            + 8 * chi * f * p * q
            + 4 * chi * p * p
            + db * q * q * u
            + 2 * df * f * q * q
            + 2 * df * p * q
        ) / u
        require(f"R{index:02d}_clock_residual", residual == expected_residual, checks)

    # Independent exact double-plane witness at several rational interior points.
    for index, (f, u) in enumerate([(F(0), F(3, 2)), (F(1, 3), F(7, 5)), (F(-2, 5), F(9, 7))], 1):
        b = (1 - f * f) / u
        g = gram(F(3), F(0), u, f, b)
        kv = [[g[0][0], g[0][1]], [g[1][0], g[1][1]]]
        ky = [[g[0][0], g[0][2]], [g[2][0], g[2][2]]]
        target = [[-9 * u, F(0)], [F(0), 1 / u]]
        require(f"W{index:02d}_KV", kv == target, checks)
        require(f"W{index:02d}_KY", ky == target, checks)

    # Larger cap census than production: primitive caps in [-3,3]^2 and
    # candidate circles in [-8,8]^2.
    cap_pairs = 0
    free_line_histogram: dict[int, int] = {}
    for vm in itertools.product(range(-3, 4), repeat=2):
        if math.gcd(abs(vm[0]), abs(vm[1])) != 1:
            continue
        for vp in itertools.product(range(-3, 4), repeat=2):
            if abs(det2(vm, vp)) != 1:
                continue
            cap_pairs += 1
            found: set[tuple[int, int]] = set()
            for w in itertools.product(range(-8, 9), repeat=2):
                if w == (0, 0) or math.gcd(abs(w[0]), abs(w[1])) != 1:
                    continue
                if abs(det2(vm, w)) == 1 and abs(det2(vp, w)) == 1:
                    found.add(canonical(w))
            expected = {canonical((vm[0] + vp[0], vm[1] + vp[1])), canonical((vm[0] - vp[0], vm[1] - vp[1]))}
            require(f"C{cap_pairs:04d}", found == expected and len(found) == 2, checks)
            free_line_histogram[len(found)] = free_line_histogram.get(len(found), 0) + 1
    require("C_final_nonempty", cap_pairs > 104, checks)
    require("C_final_two_only", free_line_histogram == {2: cap_pairs}, checks)

    result = {
        "schema": "udt-higher-isometry-plane-ownership-independent-1.0",
        "method": "stdlib_Fraction_direct_matrix_algebra_no_production_import_no_sympy",
        "status": "PASS",
        "checks_passed": len(checks),
        "rational_orbit_samples": len(samples),
        "independent_cap_pair_count": cap_pairs,
        "free_line_histogram": free_line_histogram,
        "verified": [
            "full_3x3_Gram_and_response",
            "characteristic_coefficients_and_reciprocal_rate_obstructions",
            "all_plane_determinant_formula",
            "all_direction_clock_response_formula",
            "nonconstant_depth_double_reciprocal_plane_witness",
            "two_free_unoriented_circle_theorem_on_larger_cap_census",
        ],
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
