"""Toy tensor model for epsilon-mediated angular closure.

Suppose each independent closure constraint C_a is paired with one transported
orthonormal frame label i in {1..N}. The local boundary weight is

    W_a = sum_i exp(-eta/2) delta(C_a solved by i).

If the constraints are independent and all N frame labels are admissible for
each one, then each W_a contributes N exp(-eta/2).

This script only counts tensor indices; it does not derive the local constraint
equations.
"""

from __future__ import annotations

import argparse
import math


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, default=3)
    parser.add_argument("--dimension", type=int, default=3)
    args = parser.parse_args()

    eta = 1.0 / (2.0 * args.N * args.N)
    constraints = args.N + 2 * (args.dimension - 1)
    local_weight = args.N * math.exp(-eta / 2.0)
    total_weight = local_weight ** constraints

    print("Constraint tensor model")
    print(f"N={args.N}")
    print(f"d={args.dimension}")
    print(f"eta={eta:.12g}")
    print()
    print("local constraint tensor:")
    print("  index a = closure constraint")
    print("  index i = transported epsilon/frame label")
    print("  local weight W_a = sum_i exp(-eta/2)")
    print()
    print(f"closure constraints={constraints}")
    print(f"local weight={local_weight:.12g}")
    print(f"total weight={total_weight:.12g}")
    print(f"log total={math.log(total_weight):.12g}")
    print()
    print("verdict:")
    print("  tensor-index model reproduces the entropy if each constraint has an independent i index")
    print("  derivation target: show boundary equations factorize this way")


if __name__ == "__main__":
    main()
