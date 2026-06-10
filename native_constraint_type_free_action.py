"""Type-separated free-action audit for closure constraints.

The current ladder assumes every closure unit contributes

    Delta = log N - eta/2.

But the closure count contains different-looking pieces:

    N epsilon transport labels,
    2(d-1) angular endpoint constraints.

This script compares what happens if only epsilon constraints carry the log N
entropy term versus all closure constraints carrying it.
"""

from __future__ import annotations

import math


N = 3
ETA = 1.0 / 18.0
ELECTRON_MEV = 0.51099895
E1_RATIO = 2.10394 / 1.1343262
TARGET_MU = 105.6583755
TARGET_TAU = 1776.86


def log_ratio_all_degenerate(dimension: int, coeff_ratio: float) -> float:
    n_close = N + 2 * (dimension - 1)
    return math.log(coeff_ratio) + n_close * (math.log(N) - ETA / 2.0)


def log_ratio_epsilon_only(dimension: int, coeff_ratio: float) -> float:
    angular_constraints = 2 * (dimension - 1)
    return (
        math.log(coeff_ratio)
        + N * (math.log(N) - ETA / 2.0)
        - angular_constraints * ETA / 2.0
    )


def log_ratio_action_only(dimension: int, coeff_ratio: float) -> float:
    n_close = N + 2 * (dimension - 1)
    return math.log(coeff_ratio) - n_close * ETA / 2.0


def mass_from_log(log_ratio: float) -> float:
    return ELECTRON_MEV * math.exp(log_ratio)


def print_case(label: str, log_mu: float, log_tau: float) -> None:
    mu = mass_from_log(log_mu)
    tau = mass_from_log(log_tau)
    print(label)
    print(f"  mu={mu:.8g} MeV error={(mu / TARGET_MU - 1):+.3%}")
    print(f"  tau={tau:.8g} MeV error={(tau / TARGET_TAU - 1):+.3%}")
    print()


def main() -> None:
    print("Constraint-type free-action audit")
    print(f"N={N}")
    print(f"eta={ETA:.12g}")
    print()
    print_case(
        "all closure units carry log N - eta/2",
        log_ratio_all_degenerate(2, 1.0),
        log_ratio_all_degenerate(3, E1_RATIO),
    )
    print_case(
        "only epsilon constraints carry log N; angular constraints action-only",
        log_ratio_epsilon_only(2, 1.0),
        log_ratio_epsilon_only(3, E1_RATIO),
    )
    print_case(
        "all constraints action-only, no log N entropy",
        log_ratio_action_only(2, 1.0),
        log_ratio_action_only(3, E1_RATIO),
    )
    print("verdict:")
    print("  the hierarchy requires angular endpoint constraints to be mediated by the same N-way transfer")
    print("  if log N applies only to epsilon constraints, the ladder collapses")


if __name__ == "__main__":
    main()
