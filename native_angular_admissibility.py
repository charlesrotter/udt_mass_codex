"""Angular admissibility cap from finite-action endpoint softening.

For angular-source softening,

    p(1-p)/2 = eta * lambda

has a real softened branch only if

    eta * lambda <= 1/8.

Finite action is strict: eta * lambda < 1/8. Equality is the p=1/2
log-divergent edge. This creates a native angular cap before any SM labels are
introduced.
"""

from __future__ import annotations

import argparse
import math


def p_soft(source: float) -> float | None:
    disc = 1.0 - 8.0 * source
    if disc < 0.0:
        return None
    return 0.5 * (1.0 - math.sqrt(disc))


def ordinary_lambda(ell: int) -> float:
    return float(ell * (ell + 1))


def monopole_lambda(n: int, k: int = 0) -> float:
    spin = abs(n) / 2.0
    j = spin + k
    return float(j * (j + 1.0) - spin * spin)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--etas", type=float, nargs="+", default=[0.01, 0.03, 0.06])
    parser.add_argument("--ell-max", type=int, default=12)
    parser.add_argument("--n-max", type=int, default=16)
    args = parser.parse_args()

    print("Angular admissibility cap")
    print("real softened endpoint iff eta * lambda <= 1/8")
    print("finite action requires strict eta * lambda < 1/8")
    print()
    for eta in args.etas:
        lambda_cap = 1.0 / (8.0 * eta)
        print(f"eta={eta:g} lambda_cap={lambda_cap:.6g}")

        ordinary_allowed = []
        for ell in range(args.ell_max + 1):
            lam = ordinary_lambda(ell)
            if eta * lam <= 1.0 / 8.0:
                ordinary_allowed.append((ell, lam, p_soft(eta * lam)))

        monopole_allowed = []
        for n in range(args.n_max + 1):
            lam = monopole_lambda(n, 0)
            if eta * lam <= 1.0 / 8.0:
                monopole_allowed.append((n, lam, p_soft(eta * lam)))

        print("  ordinary lowest sectors:")
        for ell, lam, p in ordinary_allowed:
            print(f"    ell={ell:2d} lambda={lam:7.3f} p={p:.6g}")
        print("  monopole lowest sectors:")
        for n, lam, p in monopole_allowed:
            print(f"    n={n:2d} lambda={lam:7.3f} p={p:.6g}")
        print()

    print("verdict:")
    print("  finite-action softening creates a native angular cap")
    print("  its value depends on eta; deriving eta would make this predictive")


if __name__ == "__main__":
    main()
