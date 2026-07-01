"""Quadratic unit-transfer model for the eta/2 factor.

The simplest way to get exp(-eta/2) is a normalized unit transfer in a quadratic
boundary action:

    S_step = (eta/2) ||e_i||^2 = eta/2

for a unit epsilon basis vector e_i. Summing over the N diagonal transferred
orientations gives

    gamma = sum_i exp(-S_step) = N exp(-eta/2).

This is conditional. It derives the half-factor only if the boundary closure
action is quadratic and the elementary closure move has unit norm.
"""

from __future__ import annotations

import math


N = 3
ETA = 1.0 / 18.0


def step_weight(norm_sq: float) -> float:
    return math.exp(-0.5 * ETA * norm_sq)


def main() -> None:
    print("Quadratic unit-transfer model")
    print("S_step=(eta/2)||v||^2")
    print(f"N={N}")
    print(f"eta={ETA:.12g}")
    print()
    for norm_sq in [0.25, 0.5, 1.0, 2.0, 3.0]:
        gamma = N * step_weight(norm_sq)
        print(
            f"norm_sq={norm_sq:g} step_weight={step_weight(norm_sq):.12g} "
            f"gamma={gamma:.12g}"
        )
    print()
    print("working case:")
    print(f"  norm_sq=1 -> gamma={N * step_weight(1.0):.12g}")
    print()
    print("verdict:")
    print("  eta/2 follows from a quadratic action evaluated on a unit closure move")
    print("  the missing derivation is the unit-norm boundary transfer itself")


if __name__ == "__main__":
    main()
