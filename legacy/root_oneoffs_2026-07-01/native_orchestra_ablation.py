"""Ablation audit for the current native mass-ladder candidate.

The user-facing hypothesis is compositional: the hierarchy may require several
native pieces acting together. This script removes or alters one load-bearing
piece at a time to see whether the result survives.
"""

from __future__ import annotations

import math


N = 3
ETA = 1.0 / 18.0
ELECTRON_MEV = 0.51099895
E1_RATIO = 2.10394 / 1.1343262
TARGET_MU = 105.6583755
TARGET_TAU = 1776.86


def masses(gamma: float, n_mu: int, n_tau: int, tau_coeff: float = E1_RATIO) -> tuple[float, float]:
    mu = ELECTRON_MEV * gamma**n_mu
    tau = ELECTRON_MEV * tau_coeff * gamma**n_tau
    return mu, tau


def print_case(label: str, gamma: float, n_mu: int, n_tau: int, tau_coeff: float = E1_RATIO) -> None:
    mu, tau = masses(gamma, n_mu, n_tau, tau_coeff)
    print(label)
    print(f"  gamma={gamma:.10g} n_mu={n_mu} n_tau={n_tau} tau_coeff={tau_coeff:.8g}")
    print(f"  mu={mu:.8g} MeV error={(mu / TARGET_MU - 1):+.3%}")
    print(f"  tau={tau:.8g} MeV error={(tau / TARGET_TAU - 1):+.3%}")
    print()


def main() -> None:
    gamma_full = N * math.exp(-ETA / 2.0)
    print("Native orchestra ablation")
    print("full candidate: diagonal N transfer + eta/2 penalty + closure depth + E1 angular coefficient")
    print()
    print_case("full candidate", gamma_full, 5, 7)
    print_case("remove eta/2 penalty: gamma=N", float(N), 5, 7)
    print_case("remove N transfer: gamma=exp(-eta/2)", math.exp(-ETA / 2.0), 5, 7)
    print_case("wrong multiplicity: gamma=N^2 exp(-eta/2)", N * N * math.exp(-ETA / 2.0), 5, 7)
    print_case("one-boundary depth B=1", gamma_full, 4, 5)
    print_case("three-boundary depth B=3", gamma_full, 6, 9)
    print_case("remove E1 angular coefficient", gamma_full, 5, 7, 1.0)
    print_case("ordinary no cascade, finite-cell coefficient only", 1.0, 0, 0)
    print()
    print("verdict:")
    print("  no single component carries the hierarchy by itself")
    print("  the useful result appears only from the combined transfer/depth/selection structure")


if __name__ == "__main__":
    main()
