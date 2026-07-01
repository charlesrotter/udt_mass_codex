"""Minimize the remaining compact-flux postulate.

Earlier Pflux bundled several assumptions together. After the topology audit,
the minimal remaining input can be stated more narrowly.
"""

from __future__ import annotations


def main() -> None:
    print("Compact-flux postulate minimization")
    print()
    print("Old broad Pflux:")
    print("  compact endpoint flux sectors may exist")
    print("  flux labels transport across the cell")
    print("  primitive n=1 is the electron anchor")
    print()
    print("Reduced status:")
    print("  transport: derived if compact U(1) bundle exists on S2 x I")
    print("  integer label: Chern number n in H^2(S2 x I, Z)=Z")
    print("  primitive selection: |n|=1 is unique nontrivial primitive sector")
    print("  higher n: nonprimitive and flux-energy superadditive")
    print()
    print("Remaining minimal postulate Pbundle0:")
    print("  elementary negative-phi matter cells may occupy the primitive")
    print("  nontrivial compact U(1) line-bundle sector on the linking S2.")
    print()
    print("verdict:")
    print("  Pflux is reduced to Pbundle0")
    print("  Pbundle0 is still not derived from the metric alone")


if __name__ == "__main__":
    main()
