"""Branch-separated residual audit in the orchestra framing.

The baseline boundary-entropy ladder predicts:

    M1/mu-like branch slightly high,
    E1/tau-like branch slightly low.

Because the signs differ, the residual cannot come from one common correction.
This script separates the residual into possible branch-local roles:

    M1: entropy-correlation damping can lower the branch.
    E1: needs a positive boost from a different native instrument.

This is not a fit proposal. It quantifies the required sizes.
"""

from __future__ import annotations

import itertools
import math

from native_angular_ms_subtraction import finite_part


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


def branch_mass(components: float, constraints: int, coeff: float, extra_log: float = 0.0) -> float:
    log_ratio = math.log(coeff) + components * math.log(N) - constraints * ETA / 2.0 + extra_log
    return ELECTRON_MEV * math.exp(log_ratio)


def solve_mu_kappa() -> float:
    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        mass = branch_mass(entropy_components(5, mid), 5, 1.0)
        if mass > TARGET_MU:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def main() -> None:
    baseline_mu = branch_mass(5.0, 5, 1.0)
    baseline_tau = branch_mass(7.0, 7, E1_RATIO)
    mu_log_need = math.log(TARGET_MU / baseline_mu)
    tau_log_need = math.log(TARGET_TAU / baseline_tau)

    kappa_mu = solve_mu_kappa()
    mu_components = entropy_components(5, kappa_mu)
    mu_corrected = branch_mass(mu_components, 5, 1.0)

    det_ordinary_m1 = finite_part("ordinary-mono1", 10000, 1.0)
    det_m2_m1 = finite_part("mono2-mono1", 10000, 1.0)
    positive_candidates = [
        ("eta/2", ETA / 2.0),
        ("eta/3", ETA / 3.0),
        ("eta^2", ETA * ETA),
        ("E1 core action", 0.0167668973),
        ("-eta*MS(ordinary-M1)", -ETA * det_ordinary_m1),
        ("eta*MS(M2-M1)", ETA * det_m2_m1),
    ]

    print("Orchestra residual separation audit")
    print(f"eta={ETA:.12g}")
    print()
    print("baseline residuals")
    print(f"  mu-like baseline={baseline_mu:.8g} log_need={mu_log_need:+.10f}")
    print(f"  tau-like baseline={baseline_tau:.8g} log_need={tau_log_need:+.10f}")
    print()
    print("M1 damping instrument")
    print(f"  kappa needed to place mu-like target={kappa_mu:.8g}")
    print(f"  effective entropy components={mu_components:.8g}")
    print(f"  corrected mu-like mass={mu_corrected:.8g}")
    print()
    print("E1 positive-boost budget")
    print(f"  required tau boost log={tau_log_need:+.10f} = {tau_log_need / ETA:+.6f} eta")
    for label, value in positive_candidates:
        print(f"  {label:24s} value={value:+.10f} ratio_to_need={value / tau_log_need:+.4f}")
    print()
    print("verdict:")
    print("  M1 residual can be explained by a small branch-local entropy correlation")
    print("  E1 still needs a separate positive native effect")
    print("  this supports the orchestra framing and warns against one-knob residual fitting")


if __name__ == "__main__":
    main()
