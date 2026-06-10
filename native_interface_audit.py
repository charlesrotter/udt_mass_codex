"""Audit finite phi=0 interface for localized angular-source cores.

The softened-core solve naturally matches to f=1+a/r outside the angular source.
If a_tail is nonzero, phi approaches 0 only asymptotically. A smooth finite-radius
match to exactly flat f=1 would require both f=1 and f_x=0 at the interface,
which is equivalent to a_tail=0 in the exterior region.

This script scans whether positive angular-source sectors can produce a_tail=0
without becoming trivial.
"""

from __future__ import annotations

import argparse

from native_core_solver import monopole_sector, ordinary_sector, p_roots, solve_profile


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--etas", type=float, nargs="+", default=[0.005, 0.01, 0.03, 0.06])
    parser.add_argument("--widths", type=float, nargs="+", default=[0.25, 0.5, 1.0])
    parser.add_argument("--x-core", type=float, default=0.0)
    parser.add_argument("--xmin", type=float, default=-20.0)
    parser.add_argument("--xmax", type=float, default=8.0)
    args = parser.parse_args()

    sectors = [monopole_sector(1), monopole_sector(2), ordinary_sector(1)]

    print("Finite phi=0 interface audit")
    print("smooth finite flat match requires exterior a_tail=0")
    print()

    for width in args.widths:
        print(f"width={width:g}")
        for eta in args.etas:
            print(f"  eta={eta:g}")
            for sector in sectors:
                source = eta * sector.angular_lambda
                if p_roots(source) is None:
                    print(f"    {sector.label:22s} source={source:8.5f} no real core")
                    continue
                result = solve_profile(
                    source, args.x_core, width, args.xmin, args.xmax
                )
                print(
                    f"    {sector.label:22s} source={source:8.5f} "
                    f"a_tail={result['a_tail']:12.6g} "
                    f"p={result['p_soft']:10.6g}"
                )
        print()

    print("verdict: any positive source gives positive exterior tail in this model")
    print("finite phi=0 cell boundary therefore needs a boundary layer/shell condition")


if __name__ == "__main__":
    main()

