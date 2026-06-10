"""Catalog of angular operator eigenvalue growth.

This checks whether a missing angular *kinematic* operator could create large
hierarchy. Standard scalar/vector/tensor spherical operators grow polynomially
with ell, so large ratios require large ell unless a new selection rule picks
special high-ell sectors.
"""

from __future__ import annotations

import argparse
import math


def scalar_lambda(ell: int) -> int:
    return ell * (ell + 1)


def vector_axial_lambda(ell: int) -> int:
    # Typical vector spherical harmonic Laplacian shift.
    return ell * (ell + 1) - 1


def tensor_tt_lambda(ell: int) -> int:
    # Typical spin-2/tensor harmonic shift on S2.
    return ell * (ell + 1) - 2


def rank_k_estimate(ell: int, rank: int) -> int:
    # Generic shifted polynomial placeholder for rank-k angular operators.
    return max(0, ell * (ell + 1) - rank)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ell-max", type=int, default=20)
    parser.add_argument("--targets", type=float, nargs="+", default=[206.768283, 3477.15])
    args = parser.parse_args()

    print("Angular operator eigenvalue growth catalog")
    print("These are kinematic growth laws, not dynamics.")
    print()
    print("ell  scalar  sqrt(scalar)  vector  tensor")
    for ell in range(0, args.ell_max + 1):
        scalar = scalar_lambda(ell)
        vector = vector_axial_lambda(ell) if ell >= 1 else None
        tensor = tensor_tt_lambda(ell) if ell >= 2 else None
        print(
            f"{ell:3d} {scalar:7d} {math.sqrt(scalar) if scalar else 0:12.6g} "
            f"{str(vector):>7s} {str(tensor):>7s}"
        )

    print()
    print("ell required if mass ratio came directly from sqrt(ell(ell+1)):")
    for target in args.targets:
        # solve ell(ell+1) ~= target^2
        ell = int(math.ceil((-1.0 + math.sqrt(1.0 + 4.0 * target * target)) / 2.0))
        print(f"  target ratio {target:g}: ell ~= {ell}")

    print()
    print("verdict:")
    print("  ordinary angular operators can make large numbers only by selecting")
    print("  very high ell; no current native rule selects ell~200 or ell~3500")


if __name__ == "__main__":
    main()

