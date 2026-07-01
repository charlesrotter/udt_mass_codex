"""Boundary-variation skeleton for the closure-count model.

For ordinary angular boundary data, a variational principle on a finite interval
has independent endpoint variations:

    delta S_boundary = P_core delta a_core + P_outer delta a_outer.

For d-1 non-scalar angular modes, that gives 2(d-1) independent boundary
conditions unless a separate constraint identifies them.

The epsilon orientation is different in the current model: it is treated as a
transported topological/holonomy label, so the two endpoint labels are related
diagonally rather than varied independently.
"""

from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, default=3)
    parser.add_argument("--dimensions", type=int, nargs="+", default=[2, 3])
    args = parser.parse_args()

    print("Boundary-variation skeleton")
    print("ordinary angular modes: endpoint variations independent")
    print("epsilon orientation: diagonal transported label")
    print(f"N={args.N}")
    print()

    for dimension in args.dimensions:
        nonscalar = dimension - 1
        angular_boundary_terms = 2 * nonscalar
        epsilon_transport_labels = args.N
        total = angular_boundary_terms + epsilon_transport_labels
        print(f"d={dimension}:")
        print(f"  non-scalar angular modes={nonscalar}")
        print(f"  angular endpoint variation terms=2*{nonscalar}={angular_boundary_terms}")
        print(f"  diagonal epsilon transport labels={epsilon_transport_labels}")
        print(f"  closure count={total}")
        print()

    print("boundary logic:")
    print("  angular independence is variationally natural on a finite interval")
    print("  epsilon diagonality is not variationally automatic; it needs a holonomy/topological rule")
    print()
    print("verdict:")
    print("  Pdepth has a variational skeleton")
    print("  Ptransfer-space still needs the topological diagonal transport derivation")


if __name__ == "__main__":
    main()
