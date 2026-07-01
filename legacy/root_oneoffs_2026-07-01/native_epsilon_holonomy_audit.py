"""Audit epsilon holonomy effects on the transfer trace.

If the transported epsilon orientation acquires a holonomy U across the finite
cell, the transfer becomes

    T = exp(-eta/2) U

and the step multiplier is tr(T). The current model requires tr(U)=N, i.e. an
identity/trivial holonomy on the epsilon transfer space.
"""

from __future__ import annotations

import math

import numpy as np


N = 3
ETA = 1.0 / 18.0
PENALTY = math.exp(-ETA / 2.0)


def rotation_2d(theta: float) -> np.ndarray:
    mat = np.eye(N)
    mat[0, 0] = math.cos(theta)
    mat[0, 1] = -math.sin(theta)
    mat[1, 0] = math.sin(theta)
    mat[1, 1] = math.cos(theta)
    return mat


def cycle_permutation() -> np.ndarray:
    mat = np.zeros((N, N))
    for i in range(N):
        mat[(i + 1) % N, i] = 1.0
    return mat


def swap_permutation() -> np.ndarray:
    mat = np.eye(N)
    mat[0, 0] = 0.0
    mat[1, 1] = 0.0
    mat[0, 1] = 1.0
    mat[1, 0] = 1.0
    return mat


def main() -> None:
    cases = [
        ("identity", np.eye(N)),
        ("swap two orientations", swap_permutation()),
        ("3-cycle permutation", cycle_permutation()),
        ("small rotation theta=eta", rotation_2d(ETA)),
        ("rotation theta=pi/3", rotation_2d(math.pi / 3.0)),
        ("orientation reversal -I", -np.eye(N)),
    ]

    print("Epsilon holonomy audit")
    print(f"N={N}")
    print(f"eta={ETA:.12g}")
    print(f"penalty=exp(-eta/2)={PENALTY:.12g}")
    print()
    for label, holonomy in cases:
        tr_u = float(np.trace(holonomy))
        gamma = PENALTY * tr_u
        print(label)
        print(f"  tr(U)={tr_u:.12g}")
        print(f"  gamma=exp(-eta/2) tr(U)={gamma:.12g}")
        print()
    print("verdict:")
    print("  current gamma requires trivial epsilon holonomy with tr(U)=N")
    print("  nontrivial holonomy would be an additional branch-specific correction")


if __name__ == "__main__":
    main()
