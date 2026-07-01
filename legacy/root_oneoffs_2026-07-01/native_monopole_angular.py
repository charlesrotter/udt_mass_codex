"""Angular spectrum for a charged scalar on S^2 with monopole flux.

This is a diagnostic for the topological route. A monopole number n changes
the angular ladder from ordinary ell=0,1,2,... to monopole harmonics with

    j = |n|/2, |n|/2 + 1, ...
    lambda = j(j+1) - (n/2)^2
    degeneracy = 2j + 1

For odd n, the angular labels are half-integer and the lowest multiplet is a
doublet at n=1. This resembles spinorial structure, but the half-integer has
entered through the monopole flux unit. It is not derived from the metric
puncture alone.
"""

from __future__ import annotations

import argparse


def monopole_ladder(n: int, levels: int):
    s = abs(n) / 2.0
    for k in range(levels):
        j = s + k
        eigenvalue = j * (j + 1.0) - s * s
        degeneracy = int(round(2.0 * j + 1.0))
        yield j, eigenvalue, degeneracy


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nmax", type=int, default=4)
    parser.add_argument("--levels", type=int, default=4)
    args = parser.parse_args()

    print("Monopole angular ladders on S^2")
    print("j=|n|/2+k, lambda=j(j+1)-(n/2)^2, degeneracy=2j+1")
    print()
    for n in range(args.nmax + 1):
        print(f"monopole_number n={n}")
        for j, eigenvalue, degeneracy in monopole_ladder(n, args.levels):
            print(f"  j={j:4.1f}  lambda={eigenvalue:7.3f}  degeneracy={degeneracy}")
        print()


if __name__ == "__main__":
    main()

