"""Entropy count implied by epsilon-mediated closure constraints."""

from __future__ import annotations

import math


N = 3


def main() -> None:
    print("Constraint entropy count")
    print(f"N={N}")
    print()
    for dimension in [1, 2, 3, 5]:
        n_constraints = N + 2 * (dimension - 1)
        configurations = N ** n_constraints
        print(f"d={dimension}:")
        print(f"  closure constraints={n_constraints}")
        print(f"  N^constraints={configurations}")
        print(f"  log entropy={math.log(configurations):.12g}")
        if dimension == 1:
            print("  caveat=scalar/background, not matter branch")
        print()
    print("verdict:")
    print("  the hierarchy-scale entropy is large because closure choices multiply")
    print("  this is plausible only if constraints are independently epsilon-mediated")


if __name__ == "__main__":
    main()
