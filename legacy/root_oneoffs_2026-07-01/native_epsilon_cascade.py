"""Discrete epsilon-cascade diagnostic for mass hierarchy.

This is not a particle model. It tests a narrow question:

    If the N=3 epsilon sector creates discrete log-radius contractions,
    can a factor close to 3 bridge the hierarchy that ordinary finite-cell
    spectra cannot?

The diagnostic uses the eta=1/18 finite-cell ground coefficients as O(1)
angular prefactors:

    M_i / m_e = (A_i / A_e) * gamma**n.

For gamma=3, the integer n is the number of epsilon-scale contractions.
"""

from __future__ import annotations

import argparse
import itertools
import math


COEFFS = {
    "M1": 1.1343262,
    "M2": 1.54635,
    "E1": 2.10394,
}


TARGETS = {
    "mu_like": 206.768283,
    "tau_like": 3477.15,
}


def log_error(predicted: float, target: float) -> float:
    return math.log(predicted / target)


def fixed_gamma_scan(gamma: float, nmax: int) -> None:
    ae = COEFFS["M1"]
    print(f"fixed gamma={gamma:g}")
    for target_name, target in TARGETS.items():
        rows = []
        for sector, coeff in COEFFS.items():
            ar = coeff / ae
            for n in range(nmax + 1):
                pred = ar * (gamma**n)
                err = log_error(pred, target)
                rows.append((abs(err), err, sector, n, pred))
        print(f"  {target_name} target={target:g}")
        for _, err, sector, n, pred in sorted(rows)[:6]:
            print(
                f"    {sector} n={n:2d} pred={pred:10.4g} "
                f"log_err={err:+.4f} frac_err={(pred / target - 1):+.2%}"
            )
    print()


def common_gamma_scan(nmax: int) -> None:
    ae = COEFFS["M1"]
    print("best common gamma from integer cascade assignments")
    rows = []
    for mu_sector, tau_sector in itertools.product(COEFFS, repeat=2):
        mu_ar = COEFFS[mu_sector] / ae
        tau_ar = COEFFS[tau_sector] / ae
        for n_mu in range(1, nmax + 1):
            for n_tau in range(n_mu + 1, nmax + 1):
                # Least-squares one-parameter fit in log space:
                # log target_j - log A_j = n_j log gamma.
                y_mu = math.log(TARGETS["mu_like"] / mu_ar)
                y_tau = math.log(TARGETS["tau_like"] / tau_ar)
                log_gamma = (n_mu * y_mu + n_tau * y_tau) / (n_mu * n_mu + n_tau * n_tau)
                gamma = math.exp(log_gamma)
                mu_pred = mu_ar * gamma**n_mu
                tau_pred = tau_ar * gamma**n_tau
                mu_err = log_error(mu_pred, TARGETS["mu_like"])
                tau_err = log_error(tau_pred, TARGETS["tau_like"])
                rms = math.sqrt((mu_err * mu_err + tau_err * tau_err) / 2.0)
                rows.append((rms, abs(math.log(gamma / 3.0)), gamma, mu_sector, n_mu, mu_pred, mu_err, tau_sector, n_tau, tau_pred, tau_err))
    for row in sorted(rows)[:10]:
        rms, dist3, gamma, mu_sector, n_mu, mu_pred, mu_err, tau_sector, n_tau, tau_pred, tau_err = row
        print(
            f"  gamma={gamma:.6g} rms_log_err={rms:.4f} dist_from_3={dist3:.4f} | "
            f"mu {mu_sector} n={n_mu} pred={mu_pred:.4g} err={mu_err:+.4f} | "
            f"tau {tau_sector} n={n_tau} pred={tau_pred:.4g} err={tau_err:+.4f}"
        )
    print()

    near_three = sorted((row for row in rows if row[0] < 0.5), key=lambda row: (row[1], row[0]))[:10]
    print("useful assignments with gamma closest to 3")
    for row in near_three:
        rms, dist3, gamma, mu_sector, n_mu, mu_pred, mu_err, tau_sector, n_tau, tau_pred, tau_err = row
        print(
            f"  gamma={gamma:.6g} rms_log_err={rms:.4f} dist_from_3={dist3:.4f} | "
            f"mu {mu_sector} n={n_mu} err={mu_err:+.4f} | "
            f"tau {tau_sector} n={n_tau} err={tau_err:+.4f}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gamma", type=float, default=3.0)
    parser.add_argument("--nmax", type=int, default=10)
    args = parser.parse_args()

    print("Epsilon-cascade hierarchy diagnostic")
    print("M_i/m_e = (A_i/A_e) * gamma^n")
    print("A_i are eta=1/18 finite-cell angular ground coefficients")
    print()
    fixed_gamma_scan(args.gamma, args.nmax)
    common_gamma_scan(args.nmax)
    print("verdict:")
    print("  a discrete factor near 3 can supply most of the missing log hierarchy")
    print("  but integer depth, sector assignment, and residual correction are not derived")


if __name__ == "__main__":
    main()
