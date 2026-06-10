"""Can entropy correlations explain the residuals?

The full candidate uses maximal independent entropy. Correlations between
epsilon choices reduce Shannon effective entropy. That can lower a branch mass,
but it cannot raise a branch above the independent-entropy prediction.
"""

from __future__ import annotations

import itertools
import math


N = 3
ETA = 1.0 / 18.0
ELECTRON_MEV = 0.51099895
E1_RATIO = 2.10394 / 1.1343262
TARGET_MU = 105.6583755
TARGET_TAU = 1776.86


def entropy_components(nodes: int, kappa: float) -> float:
    weights = []
    for labels in itertools.product(range(N), repeat=nodes):
        equal_edges = sum(1 for a, b in zip(labels, labels[1:]) if a == b)
        weights.append(math.exp(kappa * equal_edges))
    total = sum(weights)
    entropy = 0.0
    for weight in weights:
        p = weight / total
        entropy -= p * math.log(p)
    return entropy / math.log(N)


def mass_with_components(components: float, constraints: int, coeff: float) -> float:
    # Replace log N * constraints with log N * effective_components, but keep
    # the action penalty per actual constraint.
    log_ratio = math.log(coeff) + components * math.log(N) - constraints * ETA / 2.0
    return ELECTRON_MEV * math.exp(log_ratio)


def main() -> None:
    print("Entropy correlation residual audit")
    print("correlations reduce effective entropy components")
    print()
    for kappa in [0.0, 0.25, 0.5, 1.0, 2.0]:
        comp_mu = entropy_components(5, kappa)
        comp_tau = entropy_components(7, kappa)
        mu = mass_with_components(comp_mu, 5, 1.0)
        tau = mass_with_components(comp_tau, 7, E1_RATIO)
        print(f"kappa={kappa:g}")
        print(f"  mu components={comp_mu:.6g} mass={mu:.8g} error={(mu / TARGET_MU - 1):+.3%}")
        print(f"  tau components={comp_tau:.6g} mass={tau:.8g} error={(tau / TARGET_TAU - 1):+.3%}")
        print()
    print("verdict:")
    print("  entropy correlations can reduce the mu-like branch")
    print("  they cannot raise the tau-like branch above the independent-entropy prediction")


if __name__ == "__main__":
    main()
