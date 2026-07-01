"""Topology audit for compact U(1) bundle transport on the finite cell.

The negative-phi matter cell preserves a linking S2 through radius. The radial
collar between core-side and phi=0 boundaries has topology

    S2 x I.

Complex line bundles over S2 x I are classified by H^2(S2 x I, Z) = Z, the
same Chern number measured on either boundary sphere. Therefore, if a compact
U(1) bundle is admitted at all, its integer flux label is transported across
the cell topologically.

This does not force a nonzero bundle. It only turns bundle transport into a
topological consequence once Pbundle is admitted.
"""

from __future__ import annotations


def main() -> None:
    print("Compact bundle topology audit")
    print("cell collar topology: S2 x I")
    print("H^2(S2 x I, Z) = Z")
    print()
    print("consequences if compact U(1) bundle is admitted:")
    print("  integer Chern number n labels the bundle")
    print("  n is the same on core-side and phi=0 boundary spheres")
    print("  radial transport of the flux label is topological")
    print("  primitive nonzero sector is |n|=1")
    print()
    print("not derived by topology alone:")
    print("  that the bundle must be nontrivial")
    print("  that compact U(1) is mandatory")
    print("  that a charged probe/matter field must live in the bundle")
    print()
    print("verdict:")
    print("  Pbundle-transport is derived conditional on admitting a compact U(1) bundle")
    print("  the remaining postulate is primitive nontrivial compact bundle: |n|=1")


if __name__ == "__main__":
    main()
