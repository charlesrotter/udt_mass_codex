"""Audit simple N-derived cascade-depth rules.

The cascade multiplier has native candidates. The depth rule does not.
This script keeps that problem honest by checking whether low-complexity
integer depths built from N=3 are at least competitive under the current
gamma candidate.
"""

from __future__ import annotations

import itertools
import math


N = 3
ETA = 1.0 / 18.0
GAMMA = N * math.exp(-ETA / 2.0)

COEFFS = {
    "M1": 1.1343262,
    "M2": 1.54635,
    "E1": 2.10394,
}

TARGETS = {
    "mu_like": 206.768283,
    "tau_like": 3477.15,
}


DEPTHS = {
    "0": 0,
    "N-1": N - 1,
    "N": N,
    "N+1": N + 1,
    "2N-1": 2 * N - 1,
    "2N": 2 * N,
    "2N+1": 2 * N + 1,
    "N^2-2": N * N - 2,
    "N^2-1": N * N - 1,
    "N^2": N * N,
    "3N+1": 3 * N + 1,
}


def log_error(predicted: float, target: float) -> float:
    return math.log(predicted / target)


def main() -> None:
    ae = COEFFS["M1"]
    rows = []
    for (mu_label, n_mu), (tau_label, n_tau) in itertools.product(DEPTHS.items(), repeat=2):
        if n_mu <= 0 or n_tau <= n_mu:
            continue
        for mu_sector, tau_sector in itertools.product(COEFFS, repeat=2):
            mu_ar = COEFFS[mu_sector] / ae
            tau_ar = COEFFS[tau_sector] / ae
            mu_pred = mu_ar * GAMMA**n_mu
            tau_pred = tau_ar * GAMMA**n_tau
            mu_err = log_error(mu_pred, TARGETS["mu_like"])
            tau_err = log_error(tau_pred, TARGETS["tau_like"])
            rms = math.sqrt((mu_err * mu_err + tau_err * tau_err) / 2.0)
            complexity = len(mu_label) + len(tau_label)
            rows.append((rms, complexity, mu_label, n_mu, mu_sector, mu_pred, mu_err, tau_label, n_tau, tau_sector, tau_pred, tau_err))

    print("N-derived cascade-depth audit")
    print(f"N={N}")
    print(f"eta={ETA:.12g}")
    print(f"gamma=N exp(-eta/2)={GAMMA:.12g}")
    print()
    print("best low-complexity depth assignments")
    for row in sorted(rows)[:12]:
        rms, complexity, mu_label, n_mu, mu_sector, mu_pred, mu_err, tau_label, n_tau, tau_sector, tau_pred, tau_err = row
        print(
            f"  rms={rms:.4f} complexity={complexity:2d} | "
            f"mu {mu_sector} {mu_label}={n_mu} pred={mu_pred:.4g} err={mu_err:+.4f} | "
            f"tau {tau_sector} {tau_label}={n_tau} pred={tau_pred:.4g} err={tau_err:+.4f}"
        )
    print()

    print("specific symmetric-depth candidate around 2N")
    for mu_sector, tau_sector in itertools.product(COEFFS, repeat=2):
        n_mu = 2 * N - 1
        n_tau = 2 * N + 1
        mu_ar = COEFFS[mu_sector] / ae
        tau_ar = COEFFS[tau_sector] / ae
        mu_pred = mu_ar * GAMMA**n_mu
        tau_pred = tau_ar * GAMMA**n_tau
        mu_err = log_error(mu_pred, TARGETS["mu_like"])
        tau_err = log_error(tau_pred, TARGETS["tau_like"])
        rms = math.sqrt((mu_err * mu_err + tau_err * tau_err) / 2.0)
        print(
            f"  rms={rms:.4f} | mu {mu_sector} n={n_mu} err={mu_err:+.4f} | "
            f"tau {tau_sector} n={n_tau} err={tau_err:+.4f}"
        )
    print()
    print("verdict:")
    print("  n=2N-1 and n=2N+1 is a compact candidate depth pattern")
    print("  but compactness is not derivation; a native selection rule is still missing")


if __name__ == "__main__":
    main()
