"""Hard/soft split audit for epsilon boundary transfer.

The desired transfer is

    T_ij = exp(-eta/2) delta_ij.

This can be read as two different ingredients:

    hard rule:  epsilon orientation is conserved, so i=j;
    soft rule:  each transported unit orientation carries action eta/2.

If the diagonal condition is not hard, a soft mismatch penalty gives extra
off-diagonal channels. If the action cost is not soft, gamma becomes N.
"""

from __future__ import annotations

import math


N = 3
ETA = 1.0 / 18.0


def hard_soft(i: int, j: int) -> float:
    return math.exp(-ETA / 2.0) if i == j else 0.0


def hard_only(i: int, j: int) -> float:
    return 1.0 if i == j else 0.0


def soft_mismatch(i: int, j: int) -> float:
    return math.exp(-ETA / 2.0 * (0.0 if i == j else 2.0))


def soft_independent(i: int, j: int) -> float:
    return math.exp(-ETA)


def matrix(fn):
    return [[fn(i, j) for j in range(N)] for i in range(N)]


def trace(mat: list[list[float]]) -> float:
    return sum(mat[i][i] for i in range(N))


def offdiag_sum(mat: list[list[float]]) -> float:
    return sum(mat[i][j] for i in range(N) for j in range(N) if i != j)


def main() -> None:
    forms = [
        ("hard diagonal + soft unit cost", matrix(hard_soft)),
        ("hard diagonal only", matrix(hard_only)),
        ("soft mismatch only", matrix(soft_mismatch)),
        ("soft independent pair", matrix(soft_independent)),
    ]
    target = N * math.exp(-ETA / 2.0)

    print("Hard/soft transfer audit")
    print(f"N={N}")
    print(f"eta={ETA:.12g}")
    print(f"target trace={target:.12g}")
    print()
    for label, mat in forms:
        print(label)
        print(f"  trace={trace(mat):.12g}")
        print(f"  offdiag_sum={offdiag_sum(mat):.12g}")
        print(f"  total_sum={trace(mat) + offdiag_sum(mat):.12g}")
        print()
    print("verdict:")
    print("  the working transfer requires both pieces")
    print("  hard diagonal selection removes off-diagonal channels")
    print("  soft unit action cost lowers N to N exp(-eta/2)")


if __name__ == "__main__":
    main()
