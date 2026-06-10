"""Minimal-subtraction diagnostic for angular determinant differences.

For determinant differences, subtract only the large-k divergent pieces:

  mono2 - mono1 term ~  2 log(k) + 2 + 1/k + O(1/k^2)
  ordinary - mono1  ~ -2 log(k) - 2 - 1/k + O(1/k^2)

Then sum the convergent remainder. This defines a simple finite part, but it is
still a scheme choice until UDT derives this subtraction.
"""

from __future__ import annotations

import argparse
import math


def mono_term(n: int, k: int, mu2: float) -> float:
    spin = abs(n) / 2.0
    j = spin + k
    lam = j * (j + 1.0) - spin * spin
    deg = int(round(2.0 * j + 1.0))
    return deg * math.log(lam + mu2)


def ordinary_term(ell: int, mu2: float) -> float:
    lam = ell * (ell + 1.0)
    deg = 2 * ell + 1
    return deg * math.log(lam + mu2)


def divergent_piece(name: str, k: int) -> float:
    if name == "mono2-mono1":
        return 2.0 * math.log(k) + 2.0 + 1.0 / k
    if name == "ordinary-mono1":
        return -2.0 * math.log(k) - 2.0 - 1.0 / k
    raise ValueError(name)


def raw_diff_term(name: str, k: int, mu2: float) -> float:
    if name == "mono2-mono1":
        return mono_term(2, k, mu2) - mono_term(1, k, mu2)
    if name == "ordinary-mono1":
        return ordinary_term(k, mu2) - mono_term(1, k, mu2)
    raise ValueError(name)


def finite_part(name: str, cutoff: int, mu2: float) -> float:
    # k=0 is finite and kept raw; asymptotic subtraction starts at k=1.
    total = raw_diff_term(name, 0, mu2)
    for k in range(1, cutoff + 1):
        total += raw_diff_term(name, k, mu2) - divergent_piece(name, k)
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mu2", type=float, default=1.0)
    parser.add_argument("--cutoffs", type=int, nargs="+", default=[100, 300, 1000, 3000, 10000])
    args = parser.parse_args()

    print("Angular determinant minimal-subtraction diagnostic")
    print(f"mu2={args.mu2:g}")
    print("subtraction starts at k=1; k=0 kept raw")
    print()
    for name in ["mono2-mono1", "ordinary-mono1"]:
        print(name)
        previous = None
        for cutoff in args.cutoffs:
            value = finite_part(name, cutoff, args.mu2)
            delta = value - previous if previous is not None else 0.0
            print(f"  cutoff={cutoff:7d} finite_part={value:14.8g} delta={delta:12.4g}")
            previous = value
        print()

    print("verdict:")
    print("  this produces stable finite numbers, but the subtraction itself")
    print("  must be derived from UDT before using them physically")


if __name__ == "__main__":
    main()

