"""Boundary-transfer audit for the cascade multiplier and depth count.

This script makes the current weakest assumption explicit:

    one cascade step = N angular/epsilon transfer channels
                     * exp(-eta/2) boundary action penalty.

Then

    gamma = N exp(-eta/2).

The depth count is treated as

    n(d) = N + B(d - 1),

where B=2 is the two-boundary finite-cell hypothesis. This is not a
derivation. It is an audit scaffold for what the boundary variational problem
would need to produce.
"""

from __future__ import annotations

import math


N = 3
ETA = 1.0 / (2.0 * N * N)
ELECTRON_MEV = 0.51099895
M1 = 1.1343262
E1 = 2.10394
TARGETS = {
    "mu_like": 105.6583755,
    "tau_like": 1776.86,
}


def depth(dimension: int, boundary_count: int) -> int:
    return N + boundary_count * (dimension - 1)


def prediction(boundary_count: int, half_action_count: float) -> tuple[float, float, float]:
    gamma = N * math.exp(-half_action_count * ETA)
    mu_ratio = gamma ** depth(2, boundary_count)
    tau_ratio = (E1 / M1) * gamma ** depth(3, boundary_count)
    return gamma, ELECTRON_MEV * mu_ratio, ELECTRON_MEV * tau_ratio


def main() -> None:
    print("Boundary-transfer audit")
    print("one step: gamma = N exp(-c eta)")
    print("depth: n(d)=N+B(d-1)")
    print(f"N={N}")
    print(f"eta={ETA:.12g}")
    print()
    print("boundary/depth candidates with c=1/2")
    for boundary_count in [0, 1, 2, 3]:
        gamma, mu_mass, tau_mass = prediction(boundary_count, 0.5)
        print(
            f"  B={boundary_count} gamma={gamma:.8g} "
            f"n2={depth(2, boundary_count):2d} n3={depth(3, boundary_count):2d} "
            f"mu={mu_mass:9.4f} MeV tau={tau_mass:9.4f} MeV"
        )
    print()
    print("half-action candidates with B=2")
    for c in [0.0, 0.25, 1.0 / 3.0, 0.5, 2.0 / 3.0, 1.0]:
        gamma, mu_mass, tau_mass = prediction(2, c)
        print(
            f"  c={c:.8g} gamma={gamma:.8g} "
            f"mu_err={(mu_mass / TARGETS['mu_like'] - 1):+.3%} "
            f"tau_err={(tau_mass / TARGETS['tau_like'] - 1):+.3%}"
        )
    print()
    print("required derivation targets:")
    print("  B=2 must come from the two finite-cell closure boundaries")
    print("  c=1/2 must come from quadratic boundary action or determinant measure")
    print("  N must act as transfer multiplicity, not just static degeneracy")


if __name__ == "__main__":
    main()
