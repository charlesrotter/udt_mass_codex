"""Regulated angular determinant diagnostic.

Candidate missing angular dynamics:

    a quantum determinant / Casimir-like boundary term from angular modes.

This script computes cutoff-regulated sums

    log Det_L = sum_{levels<=L} degeneracy * log(lambda + mu^2)

for ordinary and monopole angular ladders, then reports differences relative to
a reference sector. Strong cutoff dependence means the determinant requires a
renormalization prescription before it can be used as a prediction.
"""

from __future__ import annotations

import argparse
import math


def ordinary_levels(ell_max: int):
    for ell in range(0, ell_max + 1):
        yield f"ell={ell}", ell * (ell + 1), 2 * ell + 1


def monopole_levels(n: int, k_max: int):
    spin = abs(n) / 2.0
    for k in range(0, k_max + 1):
        j = spin + k
        lam = j * (j + 1.0) - spin * spin
        deg = int(round(2.0 * j + 1.0))
        yield f"n={n},k={k}", lam, deg


def logdet_ordinary(ell_max: int, mu2: float) -> float:
    total = 0.0
    for _label, lam, deg in ordinary_levels(ell_max):
        total += deg * math.log(lam + mu2)
    return total


def logdet_monopole(n: int, k_max: int, mu2: float) -> float:
    total = 0.0
    for _label, lam, deg in monopole_levels(n, k_max):
        total += deg * math.log(lam + mu2)
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cutoffs", type=int, nargs="+", default=[5, 10, 20, 40, 80])
    parser.add_argument("--mu2", type=float, default=1.0)
    args = parser.parse_args()

    print("Regulated angular determinant diagnostic")
    print("logDet_L = sum deg * log(lambda + mu2)")
    print(f"mu2={args.mu2:g}")
    print()
    print("cutoff  ordinary  mono_n1  mono_n2  n2-n1  ell1like-n1")
    for cutoff in args.cutoffs:
        ordinary = logdet_ordinary(cutoff, args.mu2)
        mono1 = logdet_monopole(1, cutoff, args.mu2)
        mono2 = logdet_monopole(2, cutoff, args.mu2)
        # ordinary includes ell=0; compare full determinant as a crude reference.
        print(
            f"{cutoff:6d} {ordinary:9.4f} {mono1:8.4f} {mono2:8.4f} "
            f"{mono2 - mono1:8.4f} {ordinary - mono1:12.4f}"
        )

    print()
    print("verdict:")
    print("  angular determinants can generate logarithmic contributions,")
    print("  but raw differences are cutoff/renormalization dependent")
    print("  a predictive use needs a UDT-native subtraction or running rule")


if __name__ == "__main__":
    main()

