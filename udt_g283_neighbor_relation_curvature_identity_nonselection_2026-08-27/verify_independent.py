#!/usr/bin/env python3
"""Independent exact-coordinate and numerical-network verification for G283."""

from __future__ import annotations

import csv
import json
import math
import random
from fractions import Fraction
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
SEED = 28320260827


def poly(coeffs: list[Fraction], u: Fraction, derivative: int = 0) -> Fraction:
    current = coeffs[:]
    for _ in range(derivative):
        current = [Fraction(i) * current[i] for i in range(1, len(current))]
    total = Fraction(0)
    for coefficient in reversed(current):
        total = total * u + coefficient
    return total


def inverse_metric(H: Fraction) -> list[list[Fraction]]:
    z = Fraction(0)
    o = Fraction(1)
    return [[z, -o, z, z], [-o, -H, z, z], [z, z, o, z], [z, z, z, o]]


def direct_geometry(
    coeffs: tuple[list[Fraction], list[Fraction], list[Fraction]],
    u: Fraction,
    x: Fraction,
    y: Fraction,
) -> tuple[list, list, list]:
    values = [[poly(item, u, order) for order in range(3)] for item in coeffs]
    (a, ap, app), (b, bp, bpp), (c, cp, cpp) = values
    H = -(a * x * x + 2 * b * x * y + c * y * y)
    Hu = -(ap * x * x + 2 * bp * x * y + cp * y * y)
    Hx = -2 * a * x - 2 * b * y
    Hy = -2 * b * x - 2 * c * y
    Huu = -(app * x * x + 2 * bpp * x * y + cpp * y * y)
    Hux = -2 * ap * x - 2 * bp * y
    Huy = -2 * bp * x - 2 * cp * y
    Hxx, Hxy, Hyy = -2 * a, -2 * b, -2 * c

    z = Fraction(0)
    o = Fraction(1)
    g = [[H, -o, z, z], [-o, z, z, z], [z, z, o, z], [z, z, z, o]]
    gi = inverse_metric(H)
    dg = [[[z for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for k, value in enumerate((Hu, z, Hx, Hy)):
        dg[k][0][0] = value
    ddg = [[[[z for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
    second = {
        (0, 0): Huu,
        (0, 2): Hux,
        (2, 0): Hux,
        (0, 3): Huy,
        (3, 0): Huy,
        (2, 2): Hxx,
        (2, 3): Hxy,
        (3, 2): Hxy,
        (3, 3): Hyy,
    }
    for (k, l), value in second.items():
        ddg[k][l][0][0] = value

    dgi = [[[z for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for k in range(4):
        for rho in range(4):
            for delta in range(4):
                dgi[k][rho][delta] = -sum(
                    gi[rho][p] * dg[k][p][q] * gi[q][delta]
                    for p in range(4)
                    for q in range(4)
                )

    gamma = [[[z for _ in range(4)] for _ in range(4)] for _ in range(4)]
    dgamma = [[[[z for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for rho in range(4):
        for mu in range(4):
            for nu in range(4):
                C = [dg[mu][delta][nu] + dg[nu][delta][mu] - dg[delta][mu][nu] for delta in range(4)]
                gamma[rho][mu][nu] = sum(gi[rho][delta] * C[delta] for delta in range(4)) / 2
                for k in range(4):
                    dC = [
                        ddg[k][mu][delta][nu]
                        + ddg[k][nu][delta][mu]
                        - ddg[k][delta][mu][nu]
                        for delta in range(4)
                    ]
                    dgamma[k][rho][mu][nu] = (
                        sum(dgi[k][rho][delta] * C[delta] for delta in range(4))
                        + sum(gi[rho][delta] * dC[delta] for delta in range(4))
                    ) / 2

    rup = [[[[z for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
    rlow = [[[[z for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for rho in range(4):
        for sigma in range(4):
            for mu in range(4):
                for nu in range(4):
                    rup[rho][sigma][mu][nu] = (
                        dgamma[mu][rho][nu][sigma]
                        - dgamma[nu][rho][mu][sigma]
                        + sum(
                            gamma[rho][mu][lam] * gamma[lam][nu][sigma]
                            - gamma[rho][nu][lam] * gamma[lam][mu][sigma]
                            for lam in range(4)
                        )
                    )
    for rho in range(4):
        for sigma in range(4):
            for mu in range(4):
                for nu in range(4):
                    rlow[rho][sigma][mu][nu] = sum(
                        g[rho][alpha] * rup[alpha][sigma][mu][nu] for alpha in range(4)
                    )
    return g, gamma, rlow


def matmul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def add_scaled(a: list[list[float]], b: list[list[float]], scale: float) -> list[list[float]]:
    return [[a[i][j] + scale * b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def transpose(a: list[list[float]]) -> list[list[float]]:
    return [list(row) for row in zip(*a)]


def identity(n: int) -> list[list[float]]:
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def max_abs(a: list[list[float]]) -> float:
    return max(abs(item) for row in a for item in row)


def matrix_difference(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def float_poly(coeffs: list[float], u: float) -> float:
    total = 0.0
    for coefficient in reversed(coeffs):
        total = total * u + coefficient
    return total


def generator(coeffs: tuple[list[float], list[float], list[float]], u: float) -> list[list[float]]:
    a, b, c = (float_poly(item, u) for item in coeffs)
    return [
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
        [-a, -b, 0.0, 0.0],
        [-b, -c, 0.0, 0.0],
    ]


def integrate(coeffs: tuple[list[float], list[float], list[float]], start: float, end: float, steps: int) -> list[list[float]]:
    h = (end - start) / steps
    state = identity(4)
    u = start
    for _ in range(steps):
        k1 = matmul(generator(coeffs, u), state)
        mid1 = add_scaled(state, k1, h / 2)
        k2 = matmul(generator(coeffs, u + h / 2), mid1)
        mid2 = add_scaled(state, k2, h / 2)
        k3 = matmul(generator(coeffs, u + h / 2), mid2)
        end_state = add_scaled(state, k3, h)
        k4 = matmul(generator(coeffs, u + h), end_state)
        state = [
            [state[i][j] + h * (k1[i][j] + 2 * k2[i][j] + 2 * k3[i][j] + k4[i][j]) / 6 for j in range(4)]
            for i in range(4)
        ]
        u += h
    return state


def det2(block: list[list[float]]) -> float:
    return block[0][0] * block[1][1] - block[0][1] * block[1][0]


def main() -> None:
    rng = random.Random(SEED)
    exact_cases = 128
    exact_assertions = 0
    for _ in range(exact_cases):
        coefficients = tuple(
            [Fraction(rng.randint(-4, 4), rng.randint(1, 5)) for _ in range(4)]
            for _ in range(3)
        )
        u = Fraction(rng.randint(-3, 3), rng.randint(2, 7))
        g, gamma, curvature = direct_geometry(coefficients, u, Fraction(0), Fraction(0))
        a, b, c = (poly(item, u) for item in coefficients)
        expected_metric = [[Fraction(0), Fraction(-1), Fraction(0), Fraction(0)], [Fraction(-1), Fraction(0), Fraction(0), Fraction(0)], [Fraction(0), Fraction(0), Fraction(1), Fraction(0)], [Fraction(0), Fraction(0), Fraction(0), Fraction(1)]]
        assert g == expected_metric
        exact_assertions += 16
        assert all(gamma[rho][mu][nu] == 0 for rho in range(4) for mu in range(4) for nu in range(4))
        exact_assertions += 64
        assert curvature[0][2][0][2] == a
        assert curvature[0][2][0][3] == b
        assert curvature[0][3][0][2] == b
        assert curvature[0][3][0][3] == c
        exact_assertions += 4
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    for l in range(4):
                        assert curvature[i][j][k][l] == curvature[k][l][i][j]
                        assert curvature[i][j][k][l] + curvature[i][k][l][j] + curvature[i][l][j][k] == 0
                        exact_assertions += 2

        a_prime, b_prime, c_prime = (poly(item, u, 1) for item in coefficients)
        derivative_values = [[a_prime, b_prime], [b_prime, c_prime]]
        dR = [[[[[Fraction(0) for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
        for ii, i in enumerate((2, 3)):
            for jj, j in enumerate((2, 3)):
                for p, q, sign1 in ((0, i, 1), (i, 0, -1)):
                    for r, s, sign2 in ((0, j, 1), (j, 0, -1)):
                        dR[0][p][q][r][s] = sign1 * sign2 * derivative_values[ii][jj]
        for e in range(4):
            for aa in range(4):
                for bb in range(4):
                    for cc in range(4):
                        for dd in range(4):
                            assert dR[e][aa][bb][cc][dd] + dR[cc][aa][bb][dd][e] + dR[dd][aa][bb][e][cc] == 0
                            exact_assertions += 1

    J = [[0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0], [-1.0, 0.0, 0.0, 0.0], [0.0, -1.0, 0.0, 0.0]]
    numerical_cases = 64
    maximum_symplectic_residual = 0.0
    maximum_composition_residual = 0.0
    maximum_reversal_residual = 0.0
    different_area_cases = 0
    rows = []
    for case in range(numerical_cases):
        if case == 0:
            coefficients_float = ([0.7], [0.0], [-0.7])
        else:
            coefficients_float = tuple(
                [rng.uniform(-0.6, 0.6) for _ in range(4)] for _ in range(3)
            )
        length = 0.45
        midpoint = length / 2
        full = integrate(coefficients_float, 0.0, length, 800)
        first = integrate(coefficients_float, 0.0, midpoint, 400)
        second = integrate(coefficients_float, midpoint, length, 400)
        reverse = integrate(coefficients_float, length, 0.0, 800)
        symplectic = matmul(matmul(transpose(full), J), full)
        composition = matmul(second, first)
        reversal = matmul(reverse, full)
        symplectic_residual = max_abs(matrix_difference(symplectic, J))
        composition_residual = max_abs(matrix_difference(composition, full))
        reversal_residual = max_abs(matrix_difference(reversal, identity(4)))
        maximum_symplectic_residual = max(maximum_symplectic_residual, symplectic_residual)
        maximum_composition_residual = max(maximum_composition_residual, composition_residual)
        maximum_reversal_residual = max(maximum_reversal_residual, reversal_residual)
        jacobi = [[full[i][j + 2] for j in range(2)] for i in range(2)]
        area = det2(jacobi)
        if abs(area - length * length) > 1e-10:
            different_area_cases += 1
        rows.append(
            {
                "case": case,
                "area": f"{area:.17g}",
                "flat_area": f"{length * length:.17g}",
                "symplectic_residual": f"{symplectic_residual:.3e}",
                "composition_residual": f"{composition_residual:.3e}",
                "reversal_residual": f"{reversal_residual:.3e}",
            }
        )

    q = math.sqrt(0.7)
    exact_constant_area = math.sin(q * 0.45) * math.sinh(q * 0.45) / (q * q)
    constant_area_error = abs(float(rows[0]["area"]) - exact_constant_area)
    checks = {
        "direct_fraction_curvature_cases_pass": exact_cases == 128,
        "all_exact_component_and_Bianchi_assertions_pass": exact_assertions > 150000,
        "all_interval_transfers_symplectic": maximum_symplectic_residual < 2e-11,
        "all_interval_compositions_close": maximum_composition_residual < 2e-11,
        "all_interval_reversals_close": maximum_reversal_residual < 2e-11,
        "constant_tracefree_area_matches_exact": constant_area_error < 2e-12,
        "nonflat_optical_responses_exist": different_area_cases >= 60,
    }
    if not all(checks.values()):
        raise AssertionError({name: value for name, value in checks.items() if not value})

    with (PACKAGE / "INDEPENDENT_CASES.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)
    result = {
        "audit": "G283_INDEPENDENT_COORDINATE_AND_NETWORK_VERIFICATION",
        "status": "PASS",
        "seed": SEED,
        "exact_cases": exact_cases,
        "exact_assertions": exact_assertions,
        "numerical_cases": numerical_cases,
        "different_area_cases": different_area_cases,
        "maximum_symplectic_residual": maximum_symplectic_residual,
        "maximum_composition_residual": maximum_composition_residual,
        "maximum_reversal_residual": maximum_reversal_residual,
        "constant_tracefree_area_error": constant_area_error,
        "checks": checks,
    }
    (PACKAGE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
