"""Fit the boundary-transfer norm under the quadratic unit-transfer model.

If

    gamma = N exp(-(eta/2) rho)

then rho=1 is the unit-transfer hypothesis. This script computes the rho values
implied by the fixed branch targets and compares them with rho=1.
"""

from __future__ import annotations

import math


N = 3
ETA = 1.0 / 18.0
E1_RATIO = 2.10394 / 1.1343262
TARGET_MU_RATIO = 206.768283
TARGET_TAU_RATIO = 1776.86 / 0.51099895


def rho_from_gamma(gamma: float) -> float:
    return -2.0 * math.log(gamma / N) / ETA


def main() -> None:
    gamma_mu = TARGET_MU_RATIO ** (1.0 / 5.0)
    gamma_tau = (TARGET_TAU_RATIO / E1_RATIO) ** (1.0 / 7.0)
    y_mu = math.log(TARGET_MU_RATIO)
    y_tau = math.log(TARGET_TAU_RATIO / E1_RATIO)
    gamma_joint = math.exp((5.0 * y_mu + 7.0 * y_tau) / (5.0 * 5.0 + 7.0 * 7.0))

    print("Transfer-norm fit")
    print("gamma=N exp(-(eta/2) rho)")
    print(f"N={N}")
    print(f"eta={ETA:.12g}")
    print()
    for label, gamma in [
        ("mu-like", gamma_mu),
        ("tau-like", gamma_tau),
        ("joint", gamma_joint),
        ("unit rho", N * math.exp(-ETA / 2.0)),
    ]:
        print(f"{label}: gamma={gamma:.12g} rho={rho_from_gamma(gamma):.8g}")
    print()
    print("verdict:")
    print("  rho=1 is close but not target-exact")
    print("  exact joint fit would use rho about 0.917")


if __name__ == "__main__":
    main()
