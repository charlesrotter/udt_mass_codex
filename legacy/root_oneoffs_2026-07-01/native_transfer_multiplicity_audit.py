"""Audit transfer multiplicity: N versus N^2.

The working cascade uses one factor of N per closure transfer:

    gamma = N exp(-eta/2).

If the core-side and phi=0 boundary epsilon labels were independently summed,
the multiplicity would be N^2 instead. The current model therefore requires a
diagonal/trace closure: the same epsilon orientation must be transported across
the cell.
"""

from __future__ import annotations

import math


N = 3
ETA = 1.0 / 18.0
ELECTRON_MEV = 0.51099895
E1_RATIO = 2.10394 / 1.1343262
TARGET_MU = 105.6583755
TARGET_TAU = 1776.86


def masses(step_multiplier: float) -> tuple[float, float]:
    mu = ELECTRON_MEV * step_multiplier**5
    tau = ELECTRON_MEV * E1_RATIO * step_multiplier**7
    return mu, tau


def main() -> None:
    penalty = math.exp(-ETA / 2.0)
    candidates = [
        ("single channel", penalty),
        ("trace/diagonal N", N * penalty),
        ("independent pair N^2", N * N * penalty),
        ("epsilon triples choose(N,3)", math.comb(N, 3) * penalty),
    ]

    print("Transfer multiplicity audit")
    print(f"N={N}")
    print(f"eta={ETA:.12g}")
    print(f"penalty=exp(-eta/2)={penalty:.12g}")
    print()
    for label, gamma in candidates:
        mu, tau = masses(gamma)
        print(label)
        print(f"  gamma={gamma:.12g}")
        print(f"  mu={mu:.8g} MeV error={(mu / TARGET_MU - 1):+.3%}")
        print(f"  tau={tau:.8g} MeV error={(tau / TARGET_TAU - 1):+.3%}")
        print()
    print("verdict:")
    print("  the current hierarchy requires trace/diagonal N multiplicity")
    print("  independent core/outer label sums would overcount by N per step")


if __name__ == "__main__":
    main()
