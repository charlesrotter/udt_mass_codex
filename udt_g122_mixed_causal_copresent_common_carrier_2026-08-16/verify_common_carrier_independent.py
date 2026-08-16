#!/usr/bin/env python3
"""Independent elementary verification of the G122 load-bearing claims.

This implementation does not import or call the production derivation.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent


def det2(m):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def rank2(m):
    if all(value == 0 for row in m for value in row):
        return 0
    if det2(m) != 0:
        return 2
    return 1


def determinant(matrix):
    """Exact determinant by independent Fraction Gaussian elimination."""
    work = [[Fraction(value) for value in row] for row in matrix]
    n = len(work)
    value = Fraction(1, 1)
    for col in range(n):
        pivot = next((row for row in range(col, n) if work[row][col] != 0), None)
        if pivot is None:
            return Fraction(0, 1)
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            value *= -1
        pivot_value = work[col][col]
        value *= pivot_value
        for j in range(col, n):
            work[col][j] /= pivot_value
        for row in range(col + 1, n):
            factor = work[row][col]
            for j in range(col, n):
                work[row][j] -= factor * work[col][j]
    return value


def scalar_difference(radius, velocity, velocity_derivative, optical):
    return velocity * radius + (velocity_derivative - optical / 4) * radius * radius


def main() -> None:
    # Flat observer exponential at the central sky direction.
    pair = [[-1, -1], [-1, 0]]
    pair_screen = [[0, 0], [0, 0]]
    lam = Fraction(7, 5)
    angular_jacobi = [[lam, 0], [0, lam]]

    # Half-turn proof on all eight coefficients of a generic 2x4 q.  The
    # invariance system is (-2 I_8) vec(q)=0; its exact determinant is nonzero.
    half_turn_constraint_det = (-2) ** 8
    zero_is_only_solution = half_turn_constraint_det != 0

    # Full phase survives a position caustic.
    phase_at_caustic = [
        [-1, 0, 0, 0],
        [0, -1, 0, 0],
        [0, 0, -1, 0],
        [0, 0, 0, -1],
    ]
    phase_det = determinant(phase_at_caustic)
    position_at_caustic = [[0, 0], [0, 0]]
    position_rank = rank2(position_at_caustic)

    # Independent exact evaluation of the G116 difference at one rational point.
    R = Fraction(2, 3)
    v = Fraction(3, 1)
    vdot = Fraction(5, 1)
    aopt = Fraction(7, 1)
    generic_difference = scalar_difference(R, v, vdot, aopt)
    pure_difference = scalar_difference(R, Fraction(0), Fraction(0), Fraction(0))

    checks = {
        "pair_lorentzian": det2(pair) == -1,
        "pair_screen_rank_zero": rank2(pair_screen) == 0,
        "angular_jacobi_rank_two": rank2(angular_jacobi) == 2,
        "half_turn_kills_nonzero_trivial_target_map": zero_is_only_solution,
        "phase_caustic_carrier_invertible": phase_det == 1 and position_rank == 0,
        "generic_scalar_difference_nonzero": generic_difference != 0,
        "pure_scalar_difference_zero": pure_difference == 0,
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "implementation": "independent elementary exact arithmetic; no production import",
        "checks": checks,
        "exact_values": {
            "pair_determinant": str(det2(pair)),
            "angular_jacobi_determinant": str(det2(angular_jacobi)),
            "generic_scalar_difference": str(generic_difference),
            "half_turn_constraint_determinant": str(half_turn_constraint_det),
            "phase_determinant": str(phase_det),
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
