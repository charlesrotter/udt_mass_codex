"""Audit candidate epsilon transfer matrix forms.

The working gamma requires

    tr(T) = N exp(-eta/2).

Several plausible-looking quadratic transfer forms do not give this. This
script compares them so the derivation target is not ambiguous.
"""

from __future__ import annotations

import math


N = 3
ETA = 1.0 / 18.0
TARGET_GAMMA = N * math.exp(-ETA / 2.0)


def identity_damped() -> list[list[float]]:
    return [[math.exp(-ETA / 2.0) if i == j else 0.0 for j in range(N)] for i in range(N)]


def mismatch_penalty() -> list[list[float]]:
    # T_ij = exp[-eta/2 ||e_i-e_j||^2]. Diagonal cost 0, off-diagonal cost eta.
    return [[1.0 if i == j else math.exp(-ETA) for j in range(N)] for i in range(N)]


def independent_boundary_penalty() -> list[list[float]]:
    # Each side has a unit boundary cost eta/2, so a pair costs eta.
    return [[math.exp(-ETA) for _j in range(N)] for _i in range(N)]


def projector_average() -> list[list[float]]:
    # A fully averaged epsilon singlet projector with unit total trace.
    return [[1.0 / N if i == j else 0.0 for j in range(N)] for i in range(N)]


def trace(matrix: list[list[float]]) -> float:
    return sum(matrix[i][i] for i in range(len(matrix)))


def total_sum(matrix: list[list[float]]) -> float:
    return sum(sum(row) for row in matrix)


def main() -> None:
    forms = [
        ("damped identity", identity_damped()),
        ("mismatch penalty", mismatch_penalty()),
        ("independent boundary penalty", independent_boundary_penalty()),
        ("projector average", projector_average()),
    ]

    print("Epsilon transfer-form audit")
    print(f"N={N}")
    print(f"eta={ETA:.12g}")
    print(f"target gamma=N exp(-eta/2)={TARGET_GAMMA:.12g}")
    print()
    for label, matrix in forms:
        tr = trace(matrix)
        tsum = total_sum(matrix)
        print(label)
        print(f"  trace={tr:.12g} trace_error={tr - TARGET_GAMMA:+.8g}")
        print(f"  total_sum={tsum:.12g}")
        print()
    print("verdict:")
    print("  the working gamma requires a damped diagonal identity transfer")
    print("  mismatch penalties or independent boundary sums give different physics")


if __name__ == "__main__":
    main()
