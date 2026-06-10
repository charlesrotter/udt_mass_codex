"""Audit independent versus shared epsilon choices across closure constraints.

The current hierarchy assumes every independent closure constraint has its own
N-way epsilon-mediated choice. If instead all constraints share one global
epsilon label, the entropy is only log N once, not per constraint.
"""

from __future__ import annotations

import math


N = 3
ETA = 1.0 / 18.0
ELECTRON_MEV = 0.51099895
E1_RATIO = 2.10394 / 1.1343262
TARGET_MU = 105.6583755
TARGET_TAU = 1776.86


def log_independent(d: int, coeff: float) -> float:
    n = N + 2 * (d - 1)
    return math.log(coeff) + n * (math.log(N) - ETA / 2.0)


def log_shared(d: int, coeff: float) -> float:
    n = N + 2 * (d - 1)
    return math.log(coeff) + math.log(N) - n * ETA / 2.0


def log_block_shared(d: int, coeff: float) -> float:
    # One shared epsilon choice for each block: epsilon block, core angular block, outer angular block.
    n = N + 2 * (d - 1)
    active_blocks = 1 + (1 if d > 1 else 0) + (1 if d > 1 else 0)
    return math.log(coeff) + active_blocks * math.log(N) - n * ETA / 2.0


def mass(log_ratio: float) -> float:
    return ELECTRON_MEV * math.exp(log_ratio)


def print_case(name: str, mu_log: float, tau_log: float) -> None:
    mu = mass(mu_log)
    tau = mass(tau_log)
    print(name)
    print(f"  mu={mu:.8g} MeV error={(mu / TARGET_MU - 1):+.3%}")
    print(f"  tau={tau:.8g} MeV error={(tau / TARGET_TAU - 1):+.3%}")
    print()


def main() -> None:
    print("Epsilon choice-correlation audit")
    print(f"N={N}")
    print(f"eta={ETA:.12g}")
    print()
    print_case("independent epsilon choice per constraint", log_independent(2, 1.0), log_independent(3, E1_RATIO))
    print_case("one global epsilon choice shared by all constraints", log_shared(2, 1.0), log_shared(3, E1_RATIO))
    print_case("one epsilon choice per closure block", log_block_shared(2, 1.0), log_block_shared(3, E1_RATIO))
    print("verdict:")
    print("  the hierarchy requires independent or effectively independent epsilon choices per constraint")
    print("  a single global transported label collapses the entropy")


if __name__ == "__main__":
    main()
