#!/usr/bin/env python3
"""Dependency-free metric-first exact tensor derivation for G264.

This verifier does not import production code or saved results.  At a regular equatorial point it
constructs the inverse metric, Christoffels, differentiated Christoffels, Riemann, Ricci, scalar
curvature, Kretschmann scalar, and mixed Einstein channels directly from metric component jets.
Only then are the constructed quantities compared with the registered closed forms.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path


N = 4


def matrix() -> list[list[F]]:
    return [[F(0) for _ in range(N)] for _ in range(N)]


def rank3() -> list[list[list[F]]]:
    return [[[F(0) for _ in range(N)] for _ in range(N)] for _ in range(N)]


def rank4() -> list[list[list[list[F]]]]:
    return [
        [[[F(0) for _ in range(N)] for _ in range(N)] for _ in range(N)]
        for _ in range(N)
    ]


def metric_first(r: F, f: F, fp: F, fpp: F) -> tuple[F, F, F, F]:
    """Construct four invariants/channels from metric jets, not from target formulas."""

    if r <= 0 or f <= 0:
        raise ValueError("regular arena requires r>0 and f>0")

    # Coordinates are (t,r,theta,varphi), evaluated at theta=pi/2.  The first and second
    # theta derivatives of sin(theta)^2 there are 0 and -2, respectively.
    g = matrix()
    g[0][0], g[1][1], g[2][2], g[3][3] = -f, 1 / f, r**2, r**2
    inverse = matrix()
    inverse[0][0], inverse[1][1], inverse[2][2], inverse[3][3] = (
        -1 / f,
        f,
        1 / r**2,
        1 / r**2,
    )

    # g_first[e][a][b] = partial_e g_ab.
    g_first = rank3()
    g_first[1][0][0] = -fp
    g_first[1][1][1] = -fp / f**2
    g_first[1][2][2] = 2 * r
    g_first[1][3][3] = 2 * r

    # g_second[e][q][a][b] = partial_e partial_q g_ab.
    g_second = rank4()
    g_second[1][1][0][0] = -fpp
    g_second[1][1][1][1] = 2 * fp**2 / f**3 - fpp / f**2
    g_second[1][1][2][2] = F(2)
    g_second[1][1][3][3] = F(2)
    g_second[2][2][3][3] = -2 * r**2

    # Differentiate the inverse by d(g^-1)=-g^-1(dg)g^-1.
    inverse_first = rank3()
    for e in range(N):
        for a in range(N):
            for d in range(N):
                inverse_first[e][a][d] = -sum(
                    inverse[a][m] * g_first[e][m][n] * inverse[n][d]
                    for m in range(N)
                    for n in range(N)
                )

    gamma = rank3()
    for a in range(N):
        for b in range(N):
            for c in range(N):
                gamma[a][b][c] = sum(
                    inverse[a][d]
                    * (g_first[b][d][c] + g_first[c][d][b] - g_first[d][b][c])
                    / 2
                    for d in range(N)
                )

    # gamma_first[e][a][b][c] = partial_e Gamma^a_bc.
    gamma_first = rank4()
    for e in range(N):
        for a in range(N):
            for b in range(N):
                for c in range(N):
                    value = F(0)
                    for d in range(N):
                        bracket = (
                            g_first[b][d][c]
                            + g_first[c][d][b]
                            - g_first[d][b][c]
                        )
                        bracket_first = (
                            g_second[e][b][d][c]
                            + g_second[e][c][d][b]
                            - g_second[e][d][b][c]
                        )
                        value += (
                            inverse_first[e][a][d] * bracket
                            + inverse[a][d] * bracket_first
                        ) / 2
                    gamma_first[e][a][b][c] = value

    # R^a_bcd in the same convention as the production derivation.
    riemann_up = rank4()
    for a in range(N):
        for b in range(N):
            for c in range(N):
                for d in range(N):
                    riemann_up[a][b][c][d] = (
                        gamma_first[c][a][b][d]
                        - gamma_first[d][a][b][c]
                        + sum(
                            gamma[a][c][e] * gamma[e][b][d]
                            - gamma[a][d][e] * gamma[e][b][c]
                            for e in range(N)
                        )
                    )

    ricci = matrix()
    for b in range(N):
        for d in range(N):
            ricci[b][d] = sum(riemann_up[a][b][a][d] for a in range(N))
    scalar = sum(inverse[a][b] * ricci[a][b] for a in range(N) for b in range(N))

    einstein_cov = matrix()
    for a in range(N):
        for b in range(N):
            einstein_cov[a][b] = ricci[a][b] - g[a][b] * scalar / 2
    radial_mixed = inverse[0][0] * einstein_cov[0][0]
    angular_mixed = inverse[2][2] * einstein_cov[2][2]

    riemann_down = rank4()
    for a in range(N):
        for b in range(N):
            for c in range(N):
                for d in range(N):
                    riemann_down[a][b][c][d] = sum(
                        g[a][e] * riemann_up[e][b][c][d] for e in range(N)
                    )

    # The pointwise metric is diagonal, so the full eight-index contraction reduces to this exact
    # four-index sum; no target sectional-curvature formula is used.
    kretschmann = sum(
        inverse[a][a]
        * inverse[b][b]
        * inverse[c][c]
        * inverse[d][d]
        * riemann_down[a][b][c][d] ** 2
        for a in range(N)
        for b in range(N)
        for c in range(N)
        for d in range(N)
    )
    return scalar, kretschmann, radial_mixed, angular_mixed


def verify() -> dict[str, object]:
    assertions = 0

    def exact(left: F, right: F, name: str) -> None:
        nonlocal assertions
        if left != right:
            raise AssertionError(f"{name}: {left} != {right}")
        assertions += 1

    case_count = 250
    for i in range(1, case_count + 1):
        r = F(i % 23 + 1, i % 7 + 1)
        f = F((7 * i) % 29 + 1, (11 * i) % 19 + 1)
        fp = F((13 * i) % 31 - 15, i % 5 + 1)
        fpp = F((17 * i) % 37 - 18, i % 9 + 1)
        scalar, kretschmann, radial, angular = metric_first(r, f, fp, fpp)

        exact(scalar, -fpp - 4 * fp / r - 2 * (f - 1) / r**2, "metric-first scalar")
        exact(
            kretschmann,
            fpp**2 + 4 * (fp / r) ** 2 + 4 * ((f - 1) / r**2) ** 2,
            "metric-first kretschmann",
        )
        exact(radial, (r * fp + f - 1) / r**2, "metric-first radial channel")
        exact(angular, fpp / 2 + fp / r, "metric-first angular channel")

    return {
        "status": "PASS",
        "case_count": case_count,
        "assertion_count": assertions,
        "constructed_objects": [
            "inverse_metric",
            "inverse_metric_first_derivative",
            "christoffel",
            "christoffel_first_derivative",
            "riemann",
            "ricci",
            "scalar_curvature",
            "kretschmann_scalar",
            "radial_mixed_einstein_channel",
            "angular_mixed_einstein_channel",
        ],
        "implementation": (
            "standard_library_fraction_metric_first_no_sympy_no_production_import_no_result_read"
        ),
        "evaluation_point": "regular_equatorial_point_theta_pi_over_2",
        "qualification": "independent_exact_tensor_derivation_not_independent_physical_premise",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded)
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
