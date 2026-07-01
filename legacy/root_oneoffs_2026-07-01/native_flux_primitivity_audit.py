"""Primitive-flux stability audit.

For the native radial U(1) flux sector, the classical energy scales as q^2.
This means a flux-n cell has a superadditive core cost relative to separated
primitive flux cells:

    E(n) / [n E(1)] = n.

This does not prove a decay channel exists, but it does make non-primitive flux
a poor elementary-stable candidate unless another native binding term overcomes
the superadditive flux cost.
"""

from __future__ import annotations

import argparse


def flux_energy_scale(n: int, cutoff: float, rmax: float) -> float:
    return float(n * n) * (1.0 / cutoff - 1.0 / rmax)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nmax", type=int, default=6)
    parser.add_argument("--cutoff", type=float, default=0.01)
    parser.add_argument("--rmax", type=float, default=10.0)
    args = parser.parse_args()

    e1 = flux_energy_scale(1, args.cutoff, args.rmax)
    print("Primitive-flux stability audit")
    print("native radial flux energy: E_n proportional to n^2")
    print(f"cutoff={args.cutoff:g} rmax={args.rmax:g}")
    print()
    print("n  E_n/E_1  E_n/(n E_1)  excess_vs_n_primitives")
    for n in range(1, args.nmax + 1):
        en = flux_energy_scale(n, args.cutoff, args.rmax)
        ratio = en / e1
        primitive_ratio = en / (n * e1)
        excess = en - n * e1
        print(f"{n:1d}  {ratio:7.3f}  {primitive_ratio:12.3f}  {excess / e1:21.3f} E_1")
    print()
    print("verdict:")
    print("  n=1 is the only compact flux sector without superadditive flux cost")
    print("  n=2 is eligible as a representation but not favored as elementary")


if __name__ == "__main__":
    main()
