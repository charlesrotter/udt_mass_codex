"""Audit which transfer-operator observable is being used.

For a boundary transfer matrix T, possible scalar reductions include:

    trace(T), largest eigenvalue, determinant(T), spectral radius, total sum.

The current ladder uses trace(T)=N exp(-eta/2), not the largest eigenvalue or
determinant. This matters: trace means "sum over diagonal transported labels,"
while largest eigenvalue means "dominant channel only."
"""

from __future__ import annotations

import math

import numpy as np


N = 3
ETA = 1.0 / 18.0
PENALTY = math.exp(-ETA / 2.0)


def observables(matrix: np.ndarray) -> dict[str, float]:
    eigvals = np.linalg.eigvals(matrix)
    return {
        "trace": float(np.trace(matrix).real),
        "largest_eigenvalue": float(max(eigvals.real)),
        "spectral_radius": float(max(abs(v) for v in eigvals)),
        "determinant": float(np.linalg.det(matrix).real),
        "total_sum": float(np.sum(matrix).real),
    }


def main() -> None:
    identity_transfer = PENALTY * np.eye(N)
    uniform_projector = PENALTY * np.ones((N, N)) / N
    single_channel = np.zeros((N, N))
    single_channel[0, 0] = PENALTY

    cases = [
        ("damped identity", identity_transfer),
        ("uniform rank-one projector", uniform_projector),
        ("single transported channel", single_channel),
    ]

    print("Transfer observable audit")
    print(f"N={N}")
    print(f"eta={ETA:.12g}")
    print(f"penalty={PENALTY:.12g}")
    print()
    for label, matrix in cases:
        print(label)
        for key, value in observables(matrix).items():
            print(f"  {key:18s} {value:.12g}")
        print()
    print("verdict:")
    print("  the current gamma is trace(damped identity), not an eigenvalue")
    print("  this means all N transported labels contribute additively")


if __name__ == "__main__":
    main()
