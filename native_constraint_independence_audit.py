"""Audit independence assumptions in the constraint tensor model."""

from __future__ import annotations

import math


N = 3
ETA = 1.0 / 18.0
UNIT = N * math.exp(-ETA / 2.0)
PENALTY = math.exp(-ETA / 2.0)


def weights(constraints: int) -> dict[str, float]:
    return {
        "independent_i_per_constraint": UNIT ** constraints,
        "shared_i_all_constraints": N * (PENALTY ** constraints),
        "independent_action_shared_entropy": N * math.exp(-constraints * ETA / 2.0),
        "no_entropy": math.exp(-constraints * ETA / 2.0),
    }


def main() -> None:
    print("Constraint independence audit")
    print(f"N={N}")
    print(f"eta={ETA:.12g}")
    print()
    for d in [2, 3]:
        constraints = N + 2 * (d - 1)
        print(f"d={d} constraints={constraints}")
        for label, weight in weights(constraints).items():
            print(f"  {label:34s} weight={weight:.12g} log={math.log(weight):+.12g}")
        print()
    print("verdict:")
    print("  independent epsilon/frame index per constraint is the load-bearing entropy assumption")
    print("  shared-index alternatives are too small by powers of N")


if __name__ == "__main__":
    main()
