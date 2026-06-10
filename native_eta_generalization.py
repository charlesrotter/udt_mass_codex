"""Generalization test for eta_l = 1/(2(2l+1)^2).

If eta=1/18 comes from eta_l=1/(2N_l^2), N_l=2l+1, then the endpoint
admissibility product for an ordinary l sector is

    s_l = eta_l * lambda_l = l(l+1) / (2(2l+1)^2).

This script checks whether that rule keeps all l finite-action, caps them, or
selects l=1 specially. It is an audit for whether eta=1/18 is a universal
normalization or specifically an l=1-sector normalization.
"""

from __future__ import annotations

import argparse
import math


def p_soft(source: float) -> float | None:
    disc = 1.0 - 8.0 * source
    if disc < 0.0:
        return None
    return 0.5 * (1.0 - math.sqrt(disc))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ell-max", type=int, default=20)
    args = parser.parse_args()

    print("Eta generalization audit")
    print("eta_l = 1/(2(2l+1)^2), source s_l=eta_l*l(l+1)")
    print("finite action requires s_l < 1/8")
    print()
    print("ell  N  eta_l        lambda    source       p_soft")
    for ell in range(1, args.ell_max + 1):
        n = 2 * ell + 1
        eta_l = 1.0 / (2.0 * n * n)
        lam = ell * (ell + 1)
        source = eta_l * lam
        p = p_soft(source)
        print(
            f"{ell:3d} {n:3d} {eta_l:12.8g} {lam:8.3g} "
            f"{source:11.8g} {p if p is not None else float('nan'):10.6g}"
        )
    print()
    print("as ell -> infinity, source -> 1/8 from below and p -> 1/2")
    print("verdict:")
    print("  eta_l=1/(2N_l^2) is a universal near-critical normalization,")
    print("  not an ell=1 selector. To select ell=1, eta must be fixed by")
    print("  the ell=1 N=3 sector globally, not recomputed for every ell.")


if __name__ == "__main__":
    main()

