#!/usr/bin/env python3
"""Independent Cartan/warped-curvature replay of the G127 load-bearing witness."""

from __future__ import annotations

from fractions import Fraction as F
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def matmul(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def transpose(a):
    return [list(row) for row in zip(*a)]


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def trace2(a):
    return a[0][0] + a[1][1]


def tracefree2(a):
    half = trace2(a) / 2
    return [[a[0][0] - half, a[0][1]], [a[1][0], a[1][1] - half]]


def frobenius2(a):
    return sum(value * value for row in a for value in row)


def main() -> None:
    # Independent exact witness: phi=log(1+q*r^2)/2 at q=r=1.
    # Cartan/warped-product formulas use E=1/b^2=exp(-2phi),
    # p=phi', h=phi'', not the production Christoffel implementation.
    q = F(1)
    r = F(1)
    E = F(1, 1 + q * r * r)
    p = q * r / (1 + q * r * r)
    h = q * (1 - q * r * r) / (1 + q * r * r) ** 2

    # a'/a=-p, b'/b=p, a''/a=p^2-h.
    T = E * ((p * p - h) - (-p) * p)
    U = E * (-p) / r
    V = E * p / r
    W = (1 - E) / (r * r)
    Xi = T - U + V - W

    c, s = F(3, 5), F(4, 5)
    radial = [[U + V, F(0)], [F(0), U + V]]
    tilted = [
        [s * s * T + c * c * U + V, F(0)],
        [F(0), U + c * c * V + s * s * W],
    ]
    cubic = [[-value / 6 for value in row] for row in tilted]
    optical_linear = [[-value / 3 for value in row] for row in tilted]

    P = [[F(5, 13), F(-12, 13)], [F(12, 13), F(5, 13)]]
    rebased = matmul(matmul(transpose(P), tilted), P)
    tf = tracefree2(tilted)
    tf_rebased = tracefree2(rebased)

    checks = {
        "cartan_scalar_T": T == F(1, 4),
        "cartan_scalar_U": U == F(-1, 4),
        "cartan_scalar_V": V == F(1, 4),
        "cartan_scalar_W": W == F(1, 2),
        "cartan_Xi": Xi == F(1, 4),
        "radial_isotropic_and_zero": radial == [[F(0), F(0)], [F(0), F(0)]],
        "tilted_exact_matrix": tilted == [[F(8, 25), F(0)], [F(0), F(4, 25)]],
        "tilted_tidal_contrast_is_s2_Xi": tilted[0][0] - tilted[1][1]
        == s * s * Xi,
        "jacobi_cubic_eigenvalue_difference": cubic[0][0] - cubic[1][1]
        == F(-2, 75),
        "optical_linear_matrix_is_minus_tidal_over_three": optical_linear
        == [[F(-8, 75), F(0)], [F(0), F(-4, 75)]],
        "optical_shear_tracefree_is_minus_tidal_tracefree_over_three": tracefree2(
            optical_linear
        )
        == [[-value / 3 for value in row] for row in tf],
        "optical_shear_eigenvalue_contrast": optical_linear[0][0]
        - optical_linear[1][1]
        == -s * s * Xi / 3,
        "screen_rotation_is_orthogonal": matmul(transpose(P), P)
        == [[F(1), F(0)], [F(0), F(1)]],
        "screen_trace_covariant": trace2(rebased) == trace2(tilted),
        "screen_determinant_covariant": det2(rebased) == det2(tilted),
        "screen_tracefree_norm_covariant": frobenius2(tf_rebased) == frobenius2(tf),
        "tilt_reversal_even": (-s) * (-s) * Xi == s * s * Xi,
    }

    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "implementation": (
            "independent standard-library Fraction replay using Cartan/warped-curvature "
            "ratios; no production import"
        ),
        "checks": checks,
        "exact_witness": {
            "T": str(T),
            "U": str(U),
            "V": str(V),
            "W": str(W),
            "Xi": str(Xi),
            "radial": [[str(v) for v in row] for row in radial],
            "tilted": [[str(v) for v in row] for row in tilted],
            "jacobi_cubic_difference": str(cubic[0][0] - cubic[1][1]),
            "optical_linear_difference": str(
                optical_linear[0][0] - optical_linear[1][1]
            ),
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
