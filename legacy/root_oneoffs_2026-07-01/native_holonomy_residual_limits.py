"""Check whether epsilon holonomy can explain the residual signs.

For real orthogonal/unitary-like holonomy, the real trace is bounded above by N.
Identity holonomy already gives the maximum gamma=N exp(-eta/2). Therefore
holonomy can lower branch masses but cannot raise a branch that is predicted
too low, unless the transfer is not norm-preserving or another mechanism is
present.
"""

from __future__ import annotations

import math


N = 3
ETA = 1.0 / 18.0
PENALTY = math.exp(-ETA / 2.0)
GAMMA_ID = N * PENALTY
ELECTRON_MEV = 0.51099895
E1_RATIO = 2.10394 / 1.1343262
TARGET_MU = 105.6583755
TARGET_TAU = 1776.86


def required_trace(target_mass: float, coeff_ratio: float, depth: int) -> float:
    gamma_required = (target_mass / (ELECTRON_MEV * coeff_ratio)) ** (1.0 / depth)
    return gamma_required / PENALTY


def main() -> None:
    tr_mu = required_trace(TARGET_MU, 1.0, 5)
    tr_tau = required_trace(TARGET_TAU, E1_RATIO, 7)
    print("Holonomy residual-limit audit")
    print(f"N={N}")
    print(f"identity gamma={GAMMA_ID:.12g}")
    print()
    print("required real trace if residual is assigned only to holonomy:")
    print(f"  mu-like:  tr(U)={tr_mu:.12g}  allowed_by_trace_bound={tr_mu <= N}")
    print(f"  tau-like: tr(U)={tr_tau:.12g}  allowed_by_trace_bound={tr_tau <= N}")
    print()
    print("verdict:")
    print("  identity holonomy is already the maximum trace case")
    print("  holonomy could reduce the mu-like branch but cannot raise the tau-like branch")
    print("  residuals require more than a common norm-preserving holonomy correction")


if __name__ == "__main__":
    main()
