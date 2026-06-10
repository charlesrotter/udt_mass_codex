"""Block-structured boundary action model.

This combines the current boundary requirements in one toy action:

    epsilon block:
      hard diagonal transport i=j,
      soft unit action eta/2 for the transported orientation.

    angular block:
      independent non-scalar constraints at the core boundary and phi=0
      boundary, giving 2(d-1) angular closure constraints.

The model is not a derivation. It is a consistency check that the desired
features can coexist without forcing the wrong N^2 transfer or collapsing the
two-boundary angular count.
"""

from __future__ import annotations

import argparse
import math

import numpy as np


def epsilon_transfer(n: int, eta: float) -> np.ndarray:
    return math.exp(-eta / 2.0) * np.eye(n)


def angular_constraint_matrix(dimension: int) -> np.ndarray:
    count = max(dimension - 1, 0)
    rows = []
    cols = 2 * count
    for i in range(count):
        row = np.zeros(cols)
        row[i] = 1.0
        rows.append(row)
    for i in range(count):
        row = np.zeros(cols)
        row[count + i] = 1.0
        rows.append(row)
    return np.vstack(rows) if rows else np.zeros((0, cols))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, default=3)
    parser.add_argument("--dimensions", type=int, nargs="+", default=[2, 3])
    args = parser.parse_args()

    eta = 1.0 / (2.0 * args.N * args.N)
    transfer = epsilon_transfer(args.N, eta)
    print("Boundary action block model")
    print(f"N={args.N}")
    print(f"eta={eta:.12g}")
    print("epsilon block: hard diagonal transport + soft unit cost")
    print(f"  transfer trace={np.trace(transfer):.12g}")
    print(f"  transfer offdiag_sum={float(np.sum(transfer) - np.trace(transfer)):.12g}")
    print()

    for dimension in args.dimensions:
        angular = angular_constraint_matrix(dimension)
        angular_rank = int(np.linalg.matrix_rank(angular))
        total_closure_count = args.N + angular_rank
        target = args.N + 2 * (dimension - 1)
        print(f"d={dimension}:")
        print(f"  angular constraint shape={angular.shape}")
        print(f"  angular constraint rank={angular_rank}")
        print(f"  total closure count=N+rank={total_closure_count}")
        print(f"  target N+2(d-1)={target}")
        print(f"  matches={total_closure_count == target}")
        print()
    print("verdict:")
    print("  block structure can keep epsilon diagonal while angular constraints stay two-boundary independent")
    print("  derivation still requires this block structure from the native boundary variational problem")


if __name__ == "__main__":
    main()
