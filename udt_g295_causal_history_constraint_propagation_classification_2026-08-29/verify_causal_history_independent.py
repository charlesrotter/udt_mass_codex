#!/usr/bin/env python3
"""Independent standard-library G295 checks; imports no production module or result."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def matsub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def iszero(a):
    return all(value == 0 for row in a for value in row)


def lower(a):
    return all(a[i][j] == 0 for i in range(len(a)) for j in range(len(a[0])) if j > i)


def main() -> None:
    assertions = 0
    family_cases = 0
    A = [[Fraction(-1), Fraction(1), Fraction(0)]]

    for alpha_i in range(-5, 6):
        for gamma_i in range(-5, 6):
            for p_i in range(-3, 4):
                for q_i in range(-2, 3):
                    alpha = Fraction(alpha_i)
                    gamma = Fraction(gamma_i)
                    U = [
                        [alpha, Fraction(0), Fraction(0)],
                        [alpha - gamma, gamma, Fraction(0)],
                        [Fraction(p_i), Fraction(q_i), Fraction(2)],
                    ]
                    R = [[gamma]]
                    assert iszero(matsub(matmul(A, U), matmul(R, A)))
                    assert lower(U)
                    assertions += 2
                    family_cases += 1

                    for x_i, z_i in ((-2, 1), (0, 3), (4, -1)):
                        state = [[Fraction(x_i)], [Fraction(x_i)], [Fraction(z_i)]]
                        updated = matmul(U, state)
                        assert iszero(matmul(A, state))
                        assert iszero(matmul(A, updated))
                        assertions += 2

    # Dense simultaneous projection for x0=x2.
    half = Fraction(1, 2)
    P = [[half, 0, half], [0, 1, 0], [half, 0, half]]
    A_global = [[1, 0, -1]]
    assert iszero(matmul(A_global, P))
    assert iszero(matsub(matmul(P, P), P))
    assert not lower(P)
    assert P[0][2] == half and P[2][0] == half
    assertions += 5

    # Triangle incidence identity survives an independently varied causal vertex update.
    B = [[-1, 1, 0], [0, -1, 1], [-1, 0, 1]]
    cycle = [[1, 1, -1]]
    assert iszero(matmul(cycle, B))
    assertions += 1
    vertex_cases = 0
    for a in range(-4, 5):
        for b in range(-3, 4):
            for c in range(-2, 3):
                V = [[a, 0, 0], [b, c, 0], [1, -1, 2]]
                assert lower(V)
                assert iszero(matmul(matmul(cycle, B), V))
                assertions += 2
                vertex_cases += 1

    # Same fixed causal law, multiple admissible histories.
    U_fixed = [[2, 0, 0], [1, 1, 0], [0, 1, 3]]
    histories = []
    for initial in ([[1], [1], [0]], [[2], [2], [1]], [[-1], [-1], [2]]):
        states = [initial]
        assert iszero(matmul(A, initial))
        assertions += 1
        for _ in range(5):
            states.append(matmul(U_fixed, states[-1]))
            assert iszero(matmul(A, states[-1]))
            assertions += 1
        histories.append(states)
    assert histories[0][-1] != histories[1][-1]
    assert histories[1][-1] != histories[2][-1]
    assertions += 2

    # A scalar constraint cannot distinguish independently changed screen blocks.
    U_full_a = [
        [2, 0, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [0, 1, 3, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 2, 1],
    ]
    U_full_b = [row[:] for row in U_full_a]
    U_full_b[4][3] = 7
    A_full = [[-1, 1, 0, 0, 0]]
    assert iszero(matsub(matmul(A_full, U_full_a), A_full))
    assert iszero(matsub(matmul(A_full, U_full_b), A_full))
    assert U_full_a != U_full_b
    assertions += 3

    result = {
        "all_pass": True,
        "assertions": assertions,
        "constraint_family_cases": family_cases,
        "vertex_update_cases": vertex_cases,
        "production_imported": False,
        "production_result_read": False,
        "expected_landing": (
            "ONE_COVARIANT_HISTORY_CONDITION_IS_THE_MINIMAL_TYPE__"
            "SLICE_CONSTRAINT_AND_CAUSAL_UPDATE_ARE_A_REPRESENTATION__"
            "FORMULA_AND_REALIZED_HISTORY_REMAIN_OPEN"
        ),
    }
    (ROOT / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
