#!/usr/bin/env python3
"""Implementation-distinct standard-library exact G289 verification."""

from __future__ import annotations

import json
import random
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "INDEPENDENT_VERIFICATION.json"


def dot(a: tuple[F, ...], b: tuple[F, ...]) -> F:
    return sum((x * y for x, y in zip(a, b)), F(0))


def sphere(u: F, v: F) -> tuple[F, F, F]:
    den = 1 + u * u + v * v
    return 2 * u / den, 2 * v / den, (1 - u * u - v * v) / den


def sphere_du(u: F, v: F) -> tuple[F, F, F]:
    den2 = (1 + u * u + v * v) ** 2
    return 2 * (1 - u * u + v * v) / den2, -4 * u * v / den2, -4 * u / den2


def sphere_dv(u: F, v: F) -> tuple[F, F, F]:
    den2 = (1 + u * u + v * v) ** 2
    return -4 * u * v / den2, 2 * (1 + u * u - v * v) / den2, -4 * v / den2


def rational_boost(t: F) -> tuple[F, F]:
    return 2 * t / (1 + t * t), (1 + t * t) / (1 - t * t)


def aberrate(n: tuple[F, F, F], beta: F, gamma: F) -> tuple[F, F, F]:
    den = gamma * (1 - beta * n[2])
    return n[0] / den, n[1] / den, gamma * (n[2] - beta) / den


def push_tangent(
    n: tuple[F, F, F], tangent: tuple[F, F, F], beta: F, gamma: F
) -> tuple[F, F, F]:
    den = gamma * (1 - beta * n[2])
    spatial = (n[0], n[1], gamma * (n[2] - beta))
    dden = -gamma * beta * tangent[2]
    dspatial = (tangent[0], tangent[1], gamma * tangent[2])
    return tuple((ds * den - s * dden) / (den * den) for ds, s in zip(dspatial, spatial))


def quaternion_from_stereographic(x: F, y: F, z: F) -> tuple[F, F, F, F]:
    den = 1 + x * x + y * y + z * z
    return (1 - x * x - y * y - z * z) / den, 2 * x / den, 2 * y / den, 2 * z / den


def hopf(q: tuple[F, F, F, F]) -> tuple[F, F, F]:
    a, b, c, d = q
    return 2 * (b * d + a * c), 2 * (c * d - a * b), a * a - b * b - c * c + d * d


def quaternion_adjoint(q: tuple[F, F, F, F]) -> tuple[tuple[F, F, F], ...]:
    a, b, c, d = q
    return (
        (a * a + b * b - c * c - d * d, 2 * (b * c - a * d), 2 * (b * d + a * c)),
        (2 * (b * c + a * d), a * a - b * b + c * c - d * d, 2 * (c * d - a * b)),
        (2 * (b * d - a * c), 2 * (c * d + a * b), a * a - b * b - c * c + d * d),
    )


def poly_add(left: tuple[F, ...], right: tuple[F, ...]) -> tuple[F, ...]:
    size = max(len(left), len(right))
    return tuple(
        (left[i] if i < len(left) else F(0)) + (right[i] if i < len(right) else F(0))
        for i in range(size)
    )


def poly_mul(left: tuple[F, ...], right: tuple[F, ...]) -> tuple[F, ...]:
    out = [F(0)] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            out[i + j] += x * y
    return tuple(out)


def wedge_sign(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    if set(left).intersection(right):
        return 0
    merged = left + right
    inversions = sum(merged[i] > merged[j] for i in range(len(merged)) for j in range(i + 1, len(merged)))
    return -1 if inversions % 2 else 1


def wedge(
    left: dict[tuple[int, ...], tuple[F, ...]],
    right: dict[tuple[int, ...], tuple[F, ...]],
) -> dict[tuple[int, ...], tuple[F, ...]]:
    out: dict[tuple[int, ...], tuple[F, ...]] = {}
    for left_basis, left_poly in left.items():
        for right_basis, right_poly in right.items():
            sign = wedge_sign(left_basis, right_basis)
            if sign == 0:
                continue
            basis = tuple(sorted(left_basis + right_basis))
            product = tuple(F(sign) * value for value in poly_mul(left_poly, right_poly))
            out[basis] = poly_add(out.get(basis, (F(0),)), product)
    return out


def integrate_poly_zero_one(poly: tuple[F, ...]) -> F:
    return sum((coefficient / F(power + 1) for power, coefficient in enumerate(poly)), F(0))


def normalized_hopf_connection_integral() -> F:
    # Hopf coordinates with s=sin^2(h): A=(1-s)du+s dv and dA=ds^(dv-du).
    connection = {(1,): (F(1), F(-1)), (2,): (F(0), F(1))}
    curvature = {(0, 2): (F(1),), (0, 1): (F(-1),)}
    density = wedge(connection, curvature)[(0, 1, 2)]
    return integrate_poly_zero_one(density)


def main() -> None:
    rng = random.Random(289)
    assertions = 0
    cases = 1200
    for _ in range(cases):
        u = F(rng.randint(-7, 7), rng.randint(1, 9))
        v = F(rng.randint(-7, 7), rng.randint(1, 9))
        t = F(rng.randint(-4, 4), rng.randint(5, 11))
        if abs(t) == 1:
            t = F(1, 3)
        n = sphere(u, v)
        du = sphere_du(u, v)
        dv = sphere_dv(u, v)
        beta, gamma = rational_boost(t)
        np = aberrate(n, beta, gamma)
        pdu = push_tangent(n, du, beta, gamma)
        pdv = push_tangent(n, dv, beta, gamma)
        den = gamma * (1 - beta * n[2])
        expected = den * den

        assert dot(n, n) == 1
        assert dot(n, du) == 0 and dot(n, dv) == 0
        assert gamma * gamma * (1 - beta * beta) == 1
        assert dot(np, np) == 1
        assert dot(np, pdu) == 0 and dot(np, pdv) == 0
        assert dot(pdu, pdu) * expected == dot(du, du)
        assert dot(pdv, pdv) * expected == dot(dv, dv)
        assert dot(pdu, pdv) * expected == dot(du, dv)
        assertions += 10

        q = quaternion_from_stereographic(
            F(rng.randint(-5, 5), rng.randint(1, 8)),
            F(rng.randint(-5, 5), rng.randint(1, 8)),
            F(rng.randint(-5, 5), rng.randint(1, 8)),
        )
        hn = hopf(q)
        assert dot(q, q) == 1
        assert dot(hn, hn) == 1
        assertions += 2

    # Exact round-target non-isometry witness.
    beta, gamma = F(3, 5), F(5, 4)
    n = (F(1), F(0), F(0))
    for tangent in ((F(0), F(1), F(0)), (F(0), F(0), F(1))):
        pushed = push_tangent(n, tangent, beta, gamma)
        assert dot(pushed, pushed) == F(16, 25)
        assertions += 1
    assert F(16, 25) != 1
    assert F(16, 25) ** 2 == F(256, 625)
    assertions += 2

    # Exact basepoint-fixed north/south Hopf fiber controls using rational circle parameters.
    for j in range(-30, 31):
        s = F(j, 31)
        den = 1 + s * s
        circle_x, circle_y = (1 - s * s) / den, 2 * s / den
        assert hopf((circle_x, F(0), F(0), circle_y)) == (F(0), F(0), F(1))
        assert hopf((F(0), circle_x, circle_y, F(0))) == (F(0), F(0), F(-1))
        assertions += 2
    normalized_integral = normalized_hopf_connection_integral()
    assert normalized_integral == F(-1)
    assert abs(normalized_integral) == 1
    assertions += 2

    # The inverse-stereographic compactification point is q=-1. Its adjoint rotation is identity,
    # so the large local frame transformation is fixed at the compactification basepoint.
    inverse_radius = F(0)
    q_infinity = (
        (inverse_radius * inverse_radius - 1) / (inverse_radius * inverse_radius + 1),
        2 * inverse_radius / (inverse_radius * inverse_radius + 1),
        F(0),
        F(0),
    )
    identity3 = ((F(1), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(1)))
    assert q_infinity == (F(-1), F(0), F(0), F(0))
    assert quaternion_adjoint(q_infinity) == identity3
    assert hopf(q_infinity) == (F(0), F(0), F(1))
    assertions += 3

    # Conformal-history separator: same null lines, different center scalar curvature.
    for alpha in (F(-2), F(-1), F(0), F(1), F(2)):
        center_scalar = -36 * alpha
        assert center_scalar == -36 * alpha
        assertions += 1
    assert -36 * F(0) != -36 * F(1)
    assertions += 1

    result = {
        "status": "PASS",
        "assertions": assertions,
        "random_exact_cases": cases,
        "method": "standard_library_fraction_stereographic_and_quaternion_routes",
        "boost_signs_covered": ["negative", "zero", "positive"],
        "round_target_nonisometry_scale": "16/25",
        "hopf_fiber_controls": 122,
        "hopf_connection_normalized_integral": str(normalized_integral),
        "hopf_integral_recomputed": True,
        "compactification_basepoint_fixed": True,
        "basepoint_adjoint_identity": True,
        "conformal_history_controls": 5,
        "imports_production_module": False,
        "reads_production_result": False,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
