"""Audit anchor alternatives to the compact-flux M1 branch.

The current electron anchor uses M1, which carries Pflux/Pbundle. This script
checks whether a zero-flux ordinary anchor can preserve the hierarchy structure.
"""

from __future__ import annotations

import math


N = 3
ETA = 1.0 / 18.0
GAMMA = N * math.exp(-ETA / 2.0)
ELECTRON_MEV = 0.51099895

COEFFS = {
    "M1": 1.1343262,
    "M2": 1.54635,
    "E1": 2.10394,
}

TARGET_MU = 105.6583755
TARGET_TAU = 1776.86


def predict(anchor: str, mu_sector: str, tau_sector: str, n_mu: int, n_tau: int) -> tuple[float, float]:
    anchor_coeff = COEFFS[anchor]
    mu = ELECTRON_MEV * (COEFFS[mu_sector] / anchor_coeff) * GAMMA**n_mu
    tau = ELECTRON_MEV * (COEFFS[tau_sector] / anchor_coeff) * GAMMA**n_tau
    return mu, tau


def main() -> None:
    cases = [
        ("current M1 anchor", "M1", "M1", "E1", 5, 7),
        ("E1 zero-flux anchor; same sectors", "E1", "M1", "E1", 5, 7),
        ("E1 zero-flux anchor; E1 cascades", "E1", "E1", "E1", 5, 7),
        ("M2 compact triplet anchor", "M2", "M1", "E1", 5, 7),
    ]

    print("Anchor alternative audit")
    print(f"gamma={GAMMA:.12g}")
    print()
    for label, anchor, mu_sector, tau_sector, n_mu, n_tau in cases:
        mu, tau = predict(anchor, mu_sector, tau_sector, n_mu, n_tau)
        print(label)
        print(f"  anchor={anchor} mu_sector={mu_sector} tau_sector={tau_sector}")
        print(f"  mu={mu:.8g} MeV error={(mu / TARGET_MU - 1):+.3%}")
        print(f"  tau={tau:.8g} MeV error={(tau / TARGET_TAU - 1):+.3%}")
        print()
    print("verdict:")
    print("  zero-flux E1 anchor does not preserve the current lepton-like hierarchy")
    print("  M1 compact-flux anchor remains load-bearing")


if __name__ == "__main__":
    main()
