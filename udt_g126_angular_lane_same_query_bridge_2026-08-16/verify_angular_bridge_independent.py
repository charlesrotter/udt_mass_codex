#!/usr/bin/env python3
"""Independent exact-Fraction G126 replay; imports no production code."""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent


def matmul(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def transpose(a):
    return [list(row) for row in zip(*a)]


def main() -> None:
    # Rational orthogonal rotation, R=7, K=3.
    O = [[F(3, 5), F(-4, 5)], [F(4, 5), F(3, 5)]]
    R, K = F(7), F(3)
    D = [[R * value for value in row] for row in O]
    Dprime = [[K * value for value in row] for row in O]
    gram = matmul(transpose(D), D)

    x = [F(2), F(-1)]
    y = [F(1), F(3)]
    Dx = [sum(D[i][j] * x[j] for j in range(2)) for i in range(2)]
    Dy = [sum(D[i][j] * y[j] for j in range(2)) for i in range(2)]

    radial_weight = F(11, 7)
    q = [F(1, 10), F(2, 10), F(3, 10), F(4, 10)]
    p = [radial_weight * value for value in q]
    p_norm = [value / sum(p) for value in p]
    residual = [p_norm[i] - q[i] for i in range(4)]

    # n=2, X=5 gives R(Z)=10(1-1/Z), dR/dZ=10/Z^2.
    Z = F(3, 2)
    dR_dZ = F(10) / (Z * Z)
    # u1=Z^2/(2X) makes K1=1 identically and u1(1)=1/(2X).
    u = Z * Z / F(10)
    alpha = F(2, 5)
    factor = 1 + alpha * (Z - 1)
    K1 = dR_dZ * u
    K2 = K1 * factor
    vertex_factor = 1 + alpha * (F(1) - 1)
    vertex_u1 = F(1, 10)
    vertex_u2 = vertex_factor * vertex_u1
    vertex_K1 = F(10) * vertex_u1
    vertex_K2 = F(10) * vertex_u2
    endpoint_position = tuple(tuple(row) for row in D)
    phase_one = (endpoint_position, K1)
    phase_two = (endpoint_position, K2)

    m = [F(-1, 2), F(1, 4), F(1, 4)]
    corr_plus = [[m[i] * m[j] for j in range(3)] for i in range(3)]
    corr_minus = [[(-m[i]) * (-m[j]) for j in range(3)] for i in range(3)]

    checks = {
        "orthogonal_rotation": matmul(transpose(O), O) == [[F(1), F(0)], [F(0), F(1)]],
        "screen_gram_R2": gram == [[R * R, F(0)], [F(0), R * R]],
        "screen_abs_area_R2": abs(D[0][0] * D[1][1] - D[0][1] * D[1][0]) == R * R,
        "screen_derivative_is_KO": Dprime == [[K * value for value in row] for row in O],
        "angle_inner_product_scaled_only": sum(Dx[i] * Dy[i] for i in range(2)) == R * R * sum(x[i] * y[i] for i in range(2)),
        "radial_reference_residual_zero": residual == [F(0)] * 4,
        "radial_pair_residual_zero": all(residual[i] * residual[j] == 0 for i in range(4) for j in range(4)),
        "matched_vertex_rate": (
            vertex_factor == 1
            and vertex_u1 == F(1, 10)
            and vertex_u2 == F(1, 10)
            and vertex_K1 == 1
            and vertex_K2 == 1
        ),
        "same_RZ_allows_distinct_finite_rate": K2 != K1 and K2 / K1 == factor,
        "K_requires_Z_affine_rate": K1 / dR_dZ == u,
        "pair_autocorrelation_does_not_fix_sign": corr_plus == corr_minus,
        "position_block_does_not_fix_phase_rate": (
            phase_one[0] == phase_two[0] and phase_one != phase_two
        ),
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "implementation": "independent standard-library Fraction replay; no production import",
        "checks": checks,
        "witness": {
            "R": str(R),
            "K_screen_example": str(K),
            "K1": str(K1),
            "K2": str(K2),
            "rate_factor": str(factor),
        },
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
