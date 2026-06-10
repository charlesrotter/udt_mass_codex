"""Toy variation of the block boundary action.

This records the minimal boundary-action structure needed by the current
candidate:

    S_b = S_epsilon + S_angular

where

    S_epsilon = eta/2 for one transported unit epsilon orientation, with a hard
                delta selecting the same orientation at both ends;
    S_angular = sum_a P_c,a A_c,a + sum_a P_o,a A_o,a

The angular variations at the two endpoints are independent. The epsilon
orientation is not varied as two independent endpoint labels; it is a transported
discrete label.
"""

from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, default=3)
    parser.add_argument("--dimension", type=int, default=3)
    args = parser.parse_args()

    nonscalar = max(args.dimension - 1, 0)
    epsilon_labels = args.N
    angular_terms = 2 * nonscalar
    total = epsilon_labels + angular_terms

    print("Block boundary-action variation")
    print("S_b = S_epsilon + S_angular")
    print(f"N={args.N}")
    print(f"d={args.dimension}")
    print()
    print("epsilon block")
    print("  hard condition: epsilon_outer = epsilon_core")
    print("  unit action: S_step = eta/2")
    print(f"  transported labels counted in trace={epsilon_labels}")
    print()
    print("angular block")
    for idx in range(nonscalar):
        print(f"  core variation term:  P_c,{idx + 1} delta A_c,{idx + 1}")
    for idx in range(nonscalar):
        print(f"  outer variation term: P_o,{idx + 1} delta A_o,{idx + 1}")
    print(f"  independent angular endpoint terms={angular_terms}")
    print()
    print(f"closure count={total}")
    print()
    print("verdict:")
    print("  the toy variation gives the desired count only if epsilon is discrete/transported")
    print("  treating epsilon as two ordinary endpoint variables would change the model")


if __name__ == "__main__":
    main()
