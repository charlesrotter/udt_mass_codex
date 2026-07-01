"""Primitive compact-bundle selection audit.

Assume compact U(1) line bundles on S2 x I are admitted. They are labeled by
an integer Chern number n. This script audits why |n|=1 is the primitive
elementary candidate:

    n=0: trivial bundle, no compact-flux doublet;
    |n|=1: primitive nontrivial bundle, lowest monopole doublet;
    |n|>1: nonprimitive, superadditive flux energy, decomposable into primitive
           topological charge units.
"""

from __future__ import annotations


def lowest_degeneracy(n: int) -> int:
    return abs(n) + 1


def lowest_lambda(n: int) -> float:
    s = abs(n) / 2.0
    j = s
    return j * (j + 1.0) - s * s


def flux_energy_ratio(n: int) -> int:
    return n * n


def main() -> None:
    print("Primitive compact-bundle selection audit")
    print("Assumption: compact U(1) line bundle admitted on S2 x I")
    print()
    print("n  trivial primitive deg lambda E_n/E_1 status")
    for n in range(0, 6):
        trivial = n == 0
        primitive = abs(n) == 1
        if trivial:
            status = "trivial/background"
            energy = 0
        elif primitive:
            status = "elementary primitive candidate"
            energy = flux_energy_ratio(n)
        else:
            status = "nonprimitive/diagnostic"
            energy = flux_energy_ratio(n)
        print(
            f"{n:1d}  {str(trivial):7s} {str(primitive):9s} "
            f"{lowest_degeneracy(n):3d} {lowest_lambda(n):6.3f} "
            f"{energy:7d} {status}"
        )
    print()
    print("verdict:")
    print("  if a nontrivial compact bundle is admitted, |n|=1 is the unique primitive sector")
    print("  this selects the M1 doublet without selecting higher flux as elementary")


if __name__ == "__main__":
    main()
