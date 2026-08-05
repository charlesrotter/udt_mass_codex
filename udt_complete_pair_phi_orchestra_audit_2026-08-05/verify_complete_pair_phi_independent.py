#!/usr/bin/env python3
"""Independent Fraction-only checks for complete-pair phi/orchestra algebra."""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "INDEPENDENT_RESULT.json"


def eye(n: int) -> list[list[F]]:
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def transpose(A):
    return [list(row) for row in zip(*A)]


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def matsub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def iszero(A):
    return all(value == 0 for row in A for value in row)


def diag(*values):
    return [[values[i] if i == j else F(0) for j in range(len(values))] for i in range(len(values))]


def inv_lorentz(L, eta):
    return matmul(matmul(eta, transpose(L)), eta)


def strain(A, eta):
    return matmul(matmul(matmul(eta, transpose(A)), eta), A)


def require(value: bool, label: str, checks: dict[str, bool]) -> None:
    checks[label] = bool(value)
    if not value:
        raise AssertionError(label)


def main() -> None:
    checks: dict[str, bool] = {}
    eta = diag(F(-1), F(1), F(1), F(1))
    A = [
        [F(1, 2), F(0), F(0), F(0)],
        [F(0), F(2), F(0), F(0)],
        [F(1, 4), F(0), F(1), F(0)],
        [F(0), F(0), F(0), F(1)],
    ]
    Lp = [
        [F(5, 4), F(3, 4), F(0), F(0)],
        [F(3, 4), F(5, 4), F(0), F(0)],
        [F(0), F(0), F(1), F(0)],
        [F(0), F(0), F(0), F(1)],
    ]
    Lq = [
        [F(13, 12), F(0), F(5, 12), F(0)],
        [F(0), F(1), F(0), F(0)],
        [F(5, 12), F(0), F(13, 12), F(0)],
        [F(0), F(0), F(0), F(1)],
    ]
    require(iszero(matsub(matmul(matmul(transpose(Lp), eta), Lp), eta)), "source_lorentz", checks)
    require(iszero(matsub(matmul(matmul(transpose(Lq), eta), Lq), eta)), "target_lorentz", checks)
    C = strain(A, eta)
    Aprime = matmul(matmul(Lq, A), inv_lorentz(Lp, eta))
    Cprime = strain(Aprime, eta)
    expected = matmul(matmul(Lp, C), inv_lorentz(Lp, eta))
    require(iszero(matsub(Cprime, expected)), "strain_covariance", checks)
    require(C[0][0] == F(3, 16) and C[0][2] == F(-1, 4), "mixing_strain_top", checks)
    require(C[2][0] == F(1, 4) and C[2][2] == F(1), "mixing_strain_bottom", checks)
    require(C[1][1] == F(4), "ruler_stretch", checks)
    require(C[3][3] == F(1), "spectator_stretch", checks)

    # Exact characteristic data for the timelike/screen mixing block.
    trace = C[0][0] + C[2][2]
    determinant = C[0][0] * C[2][2] - C[0][2] * C[2][0]
    discriminant = trace * trace - 4 * determinant
    require(trace == F(19, 16), "mix_trace", checks)
    require(determinant == F(1, 4), "mix_determinant", checks)
    require(discriminant == F(105, 256), "mix_discriminant", checks)
    require(discriminant > 0, "mix_real_distinct_roots", checks)
    require(F(1, 4) * F(1, 4) - trace * F(1, 4) + determinant != 0, "pure_timelike_value_not_root", checks)

    # Abstract log-spectrum power sums require no transcendental evaluation.
    def rho2_sq(d, a, b):
        return d*d + (a*a + b*b) / 2

    def rho4_fourth(d, a, b):
        return d**4 + (a**4 + b**4) / 2

    require(rho2_sq(F(3), F(0), F(0)) == F(9), "rho2_pure", checks)
    require(rho4_fourth(F(3), F(0), F(0)) == F(81), "rho4_pure", checks)
    require(rho2_sq(F(1), F(1), F(0))**2 != rho4_fourth(F(1), F(1), F(0)), "spectral_nonuniqueness", checks)
    require(4 * rho2_sq(F(1), F(1), F(0)) != rho2_sq(F(2), F(0), F(0)), "norm_depth_nonadditivity", checks)

    # Multiplicative form of the exact additive character family.
    def character(r, qdet, power):
        return r * qdet**power

    r1, r2, q1, q2 = F(2), F(3), F(5), F(7)
    for power in (-2, -1, 0, 1, 2):
        require(character(r2*r1, q2*q1, power) == character(r2, q2, power) * character(r1, q1, power), f"character_comp_{power}", checks)
        require(character(1/r1, 1/q1, power) == 1/character(r1, q1, power), f"character_reverse_{power}", checks)
    require(character(r1, F(1), 0) == r1 and character(r1, F(1), 2) == r1, "character_pure_reduction", checks)
    require(character(r1, q1, 0) != character(r1, q1, 1), "character_family_distinct", checks)

    # Stationary endpoint family in multiplicative form.
    def stationary(N0, N1, R0, R1, power):
        return (N0 / N1) * (R1 / R0)**power

    N0, N1, N2 = F(2), F(3), F(11)
    R0, R1, R2 = F(5), F(7), F(13)
    for power in (-2, -1, 0, 1, 2):
        q01 = stationary(N0, N1, R0, R1, power)
        q12 = stationary(N1, N2, R1, R2, power)
        q02 = stationary(N0, N2, R0, R2, power)
        require(q01 * q12 == q02, f"stationary_comp_{power}", checks)
        require(q01 * stationary(N1, N0, R1, R0, power) == 1, f"stationary_reverse_{power}", checks)
    require(stationary(N0, N1, R0, R1, 0) != stationary(N0, N1, R0, R1, 1), "stationary_angular_modulation", checks)

    # Triangle cocycle: a potential exists exactly when the loop sum vanishes.
    d01, d12 = F(2, 3), F(-5, 7)
    d20 = -(d01 + d12)
    require(d01 + d12 + d20 == 0, "zero_period", checks)
    phi = [F(0), d01, d01 + d12]
    require(phi[1] - phi[0] == d01, "potential_01", checks)
    require(phi[2] - phi[1] == d12, "potential_12", checks)
    require(phi[0] - phi[2] == d20, "potential_20", checks)
    require(d01 + d12 + (d20 + F(1, 9)) != 0, "nonzero_period_obstructs_descent", checks)

    result = {
        "status": "PASS",
        "implementation": "stdlib Fraction; no SymPy or production import",
        "check_count": len(checks),
        "checks": checks,
        "mixing_block": {"trace": "19/16", "determinant": "1/4", "discriminant": "105/256"},
        "character_powers_tested": [-2, -1, 0, 1, 2],
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
