"""Closure-constraint count for admissible cascade depths.

This recasts the depth rule as a constraint count:

    n_close(d) = N + 2(d - 1)

where a closed finite matter cell must satisfy all closure constraints:

    N           epsilon orientation constraints,
    d - 1       non-scalar angular constraints at the core-side boundary,
    d - 1       non-scalar angular constraints at the phi=0 boundary.

Partial depths correspond to unclosed constraints and are therefore not
admissible elementary cells in this bookkeeping.
"""

from __future__ import annotations

import argparse


def closure_depth(n_epsilon: int, dimension: int) -> int:
    return n_epsilon + 2 * (dimension - 1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, default=3)
    parser.add_argument("--dimensions", type=int, nargs="+", default=[1, 2, 3, 5])
    args = parser.parse_args()

    print("Closure-constraint count")
    print("n_close(d)=N+2(d-1)")
    print(f"N={args.N}")
    print()
    for dimension in args.dimensions:
        epsilon = args.N
        core = dimension - 1
        outer = dimension - 1
        total = closure_depth(args.N, dimension)
        print(f"d={dimension}:")
        print(f"  epsilon constraints={epsilon}")
        print(f"  core boundary non-scalar constraints={core}")
        print(f"  phi=0 boundary non-scalar constraints={outer}")
        print(f"  total closure depth={total}")
        if dimension == 1:
            print("  caveat=formal scalar count only; no non-scalar matter-cell branch")
        print()
    print("verdict:")
    print("  partial depths are unclosed cells in this count")
    print("  the remaining question is why each constraint maps to one gamma transfer")


if __name__ == "__main__":
    main()
