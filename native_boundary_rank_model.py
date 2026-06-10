"""Boundary constraint-rank model for the closure depth.

This is a toy linear constraint model for the count

    n_close(d) = N + 2(d - 1).

Variables are not solved dynamically here. The script only constructs the
minimal independent constraint rows implied by the current closure story:

    N epsilon orientation closure constraints,
    d-1 non-scalar angular constraints at the core boundary,
    d-1 non-scalar angular constraints at the phi=0 boundary.

The rank equals the proposed closure depth if the rows are independent.
"""

from __future__ import annotations

import argparse

import numpy as np


def constraint_matrix(n_epsilon: int, dimension: int) -> np.ndarray:
    rows: list[np.ndarray] = []
    total_cols = n_epsilon + 2 * max(dimension - 1, 0)

    for i in range(n_epsilon):
        row = np.zeros(total_cols)
        row[i] = 1.0
        rows.append(row)

    offset = n_epsilon
    for i in range(dimension - 1):
        row = np.zeros(total_cols)
        row[offset + i] = 1.0
        rows.append(row)

    offset = n_epsilon + max(dimension - 1, 0)
    for i in range(dimension - 1):
        row = np.zeros(total_cols)
        row[offset + i] = 1.0
        rows.append(row)

    return np.vstack(rows) if rows else np.zeros((0, total_cols))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, default=3)
    parser.add_argument("--dimensions", type=int, nargs="+", default=[1, 2, 3, 5])
    args = parser.parse_args()

    print("Boundary constraint-rank model")
    print("rank target: N+2(d-1)")
    print(f"N={args.N}")
    print()
    for dimension in args.dimensions:
        matrix = constraint_matrix(args.N, dimension)
        rank = np.linalg.matrix_rank(matrix)
        target = args.N + 2 * (dimension - 1)
        print(f"d={dimension}:")
        print(f"  matrix shape={matrix.shape}")
        print(f"  rank={rank}")
        print(f"  target={target}")
        print(f"  matches={rank == target}")
        if dimension == 1:
            print("  caveat=formal scalar count only")
        print()
    print("verdict:")
    print("  closure depth is the rank of the assumed independent constraint set")
    print("  the missing derivation is the constraint set itself")


if __name__ == "__main__":
    main()
