"""Failure modes for the closure-depth constraint count.

If some closure constraints are identified or dependent, the depth drops below
N+2(d-1). If extra cross-boundary constraints exist, the depth rises. This
script quantifies those alternatives.
"""

from __future__ import annotations

import argparse


def depth_independent(n: int, d: int) -> int:
    return n + 2 * (d - 1)


def depth_identified_boundaries(n: int, d: int) -> int:
    # Core and outer non-scalar constraints are one shared set.
    return n + (d - 1)


def depth_no_epsilon(n: int, d: int) -> int:
    return 2 * (d - 1)


def depth_extra_cross(n: int, d: int) -> int:
    # One extra cross-boundary compatibility for every non-scalar angular mode.
    return n + 3 * (d - 1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, default=3)
    parser.add_argument("--dimensions", type=int, nargs="+", default=[2, 3])
    args = parser.parse_args()

    print("Constraint-count failure modes")
    print(f"N={args.N}")
    print()
    for d in args.dimensions:
        print(f"d={d}:")
        print(f"  independent two-boundary count: {depth_independent(args.N, d)}")
        print(f"  identified boundary constraints: {depth_identified_boundaries(args.N, d)}")
        print(f"  no epsilon constraints: {depth_no_epsilon(args.N, d)}")
        print(f"  extra cross constraints: {depth_extra_cross(args.N, d)}")
        print()
    print("verdict:")
    print("  the successful 5/7 depths require independent core and outer non-scalar constraints")
    print("  identifying the two boundaries collapses the hierarchy")


if __name__ == "__main__":
    main()
