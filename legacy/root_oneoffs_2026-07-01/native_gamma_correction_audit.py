"""Audit the small correction in gamma = N exp(-c eta).

With the current fixed branch assignments:

    mu-like:  M1, n=5
    tau-like: E1, n=7

this script solves for the correction coefficient c required by each target and
by the two-target least-squares fit. It then compares simple native fractions.
"""

from __future__ import annotations

import math


N = 3
ETA = 1.0 / 18.0
M1 = 1.1343262
E1 = 2.10394
TARGET_MU_RATIO = 206.768283
TARGET_TAU_RATIO = 1776.86 / 0.51099895


def c_from_gamma(gamma: float) -> float:
    return -math.log(gamma / N) / ETA


def gamma_for_target(target_ratio: float, coeff_ratio: float, depth: int) -> float:
    return (target_ratio / coeff_ratio) ** (1.0 / depth)


def main() -> None:
    coeff_tau = E1 / M1
    gamma_mu = gamma_for_target(TARGET_MU_RATIO, 1.0, 5)
    gamma_tau = gamma_for_target(TARGET_TAU_RATIO, coeff_tau, 7)

    y_mu = math.log(TARGET_MU_RATIO)
    y_tau = math.log(TARGET_TAU_RATIO / coeff_tau)
    log_gamma_fit = (5.0 * y_mu + 7.0 * y_tau) / (5.0 * 5.0 + 7.0 * 7.0)
    gamma_fit = math.exp(log_gamma_fit)

    print("Gamma correction audit")
    print("gamma=N exp(-c eta)")
    print(f"N={N}")
    print(f"eta={ETA:.12g}")
    print()
    print(f"mu-like required gamma={gamma_mu:.12g} c={c_from_gamma(gamma_mu):.8g}")
    print(f"tau-like required gamma={gamma_tau:.12g} c={c_from_gamma(gamma_tau):.8g}")
    print(f"joint least-squares gamma={gamma_fit:.12g} c={c_from_gamma(gamma_fit):.8g}")
    print()
    print("simple c values")
    for c in [0.0, 0.25, 1.0 / 3.0, 0.5, 2.0 / 3.0, 1.0]:
        gamma = N * math.exp(-c * ETA)
        mu_pred = gamma**5
        tau_pred = coeff_tau * gamma**7
        print(
            f"  c={c:.8g} gamma={gamma:.10g} "
            f"mu_err={(mu_pred / TARGET_MU_RATIO - 1):+.3%} "
            f"tau_err={(tau_pred / TARGET_TAU_RATIO - 1):+.3%}"
        )
    print()
    print("verdict:")
    print("  c=1/2 is the best simple native half-factor among tested choices")
    print("  the exact joint fit would use c about 0.459, so gamma remains ansatz-bearing")


if __name__ == "__main__":
    main()
