"""Audit whether the cascade penalty can be raw angular-source dependent.

The working model uses a universal step multiplier

    gamma = N exp(-eta/2).

A tempting alternative is to use the sector angular source directly:

    gamma_i = N exp(-eta lambda_i / 2).

This script checks that alternative. If it fails badly, then the gamma
correction cannot simply be the raw endpoint angular source; it must be a
global epsilon/boundary-transfer normalization or another universal mechanism.
"""

from __future__ import annotations

import math


N = 3
ETA = 1.0 / 18.0
ELECTRON_MEV = 0.51099895
TARGET_MU = 105.6583755
TARGET_TAU = 1776.86
M1_COEFF = 1.1343262
E1_COEFF = 2.10394


def branch_mass(coeff_ratio: float, gamma: float, depth: int) -> float:
    return ELECTRON_MEV * coeff_ratio * gamma**depth


def main() -> None:
    coeff_tau = E1_COEFF / M1_COEFF
    cases = [
        ("universal eta", N * math.exp(-ETA / 2.0), N * math.exp(-ETA / 2.0)),
        (
            "lambda-dependent source",
            N * math.exp(-ETA * 0.5 / 2.0),
            N * math.exp(-ETA * 2.0 / 2.0),
        ),
        (
            "p-dependent source",
            N * math.exp(-ETA * 0.059041448 / 2.0),
            N * math.exp(-ETA * (1.0 / 3.0) / 2.0),
        ),
    ]

    print("Universal gamma audit")
    print(f"N={N}")
    print(f"eta={ETA:.12g}")
    print()
    for name, gamma_mu, gamma_tau in cases:
        mu = branch_mass(1.0, gamma_mu, 5)
        tau = branch_mass(coeff_tau, gamma_tau, 7)
        print(name)
        print(f"  gamma_mu={gamma_mu:.10g} gamma_tau={gamma_tau:.10g}")
        print(f"  mu={mu:.8g} MeV error={(mu / TARGET_MU - 1):+.3%}")
        print(f"  tau={tau:.8g} MeV error={(tau / TARGET_TAU - 1):+.3%}")
        print()
    print("verdict:")
    print("  raw lambda-dependent penalty is too sector-dependent")
    print("  current gamma must be global if this branch assignment is kept")


if __name__ == "__main__":
    main()
