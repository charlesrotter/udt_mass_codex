"""Native angular invariant catalog.

This script intentionally avoids Standard Model labels. It catalogs angular
structures by UDT-native quantities:

    dimension/degeneracy,
    angular eigenvalue,
    epsilon eligibility,
    endpoint-softening source strength,
    minimal-subtraction determinant finite part relative to a reference.

The purpose is to surface native angular patterns that may not map cleanly onto
known physics labels.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

from native_angular_ms_subtraction import finite_part


@dataclass(frozen=True)
class NativeSector:
    key: str
    family: str
    parameter: int
    dimension: int
    angular_lambda: float


def ordinary_sector(ell: int) -> NativeSector:
    return NativeSector(
        key=f"O{ell}",
        family="ordinary",
        parameter=ell,
        dimension=2 * ell + 1,
        angular_lambda=float(ell * (ell + 1)),
    )


def monopole_sector(n: int, k: int = 0) -> NativeSector:
    spin = abs(n) / 2.0
    j = spin + k
    return NativeSector(
        key=f"M{n}_{k}",
        family="monopole",
        parameter=n,
        dimension=int(round(2.0 * j + 1.0)),
        angular_lambda=float(j * (j + 1.0) - spin * spin),
    )


def lambda3_count(dimension: int) -> int:
    if dimension < 3:
        return 0
    return dimension * (dimension - 1) * (dimension - 2) // 6


def p_soft(source: float) -> float | None:
    disc = 1.0 - 8.0 * source
    if disc < 0.0:
        return None
    return 0.5 * (1.0 - math.sqrt(disc))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eta", type=float, default=0.03)
    parser.add_argument("--mu2", type=float, default=1.0)
    parser.add_argument("--det-cutoff", type=int, default=30000)
    args = parser.parse_args()

    sectors = [
        ordinary_sector(0),
        ordinary_sector(1),
        ordinary_sector(2),
        ordinary_sector(3),
        monopole_sector(1),
        monopole_sector(2),
        monopole_sector(3),
        monopole_sector(4),
    ]

    print("Native angular invariant catalog")
    print("No SM labels; all quantities are angular/endpoint diagnostics.")
    print(
        f"eta={args.eta:g} mu2={args.mu2:g} "
        f"det_cutoff={args.det_cutoff}"
    )
    print()
    print(
        "key family    param dim lambda  Lambda3 source   p_soft   notes"
    )
    for sector in sectors:
        source = args.eta * sector.angular_lambda
        p = p_soft(source)
        count = lambda3_count(sector.dimension)
        notes = []
        if count == 1:
            notes.append("unique-epsilon")
        if p is None:
            notes.append("no-real-soft-core")
        if sector.dimension == 2:
            notes.append("doublet")
        if sector.dimension == 3:
            notes.append("triplet")
        print(
            f"{sector.key:3s} {sector.family:8s} {sector.parameter:5d} "
            f"{sector.dimension:3d} {sector.angular_lambda:6.2f} "
            f"{count:7d} {source:7.4f} "
            f"{p if p is not None else float('nan'):8.5f} "
            f"{','.join(notes)}"
        )

    print()
    print("minimal-subtraction determinant finite parts at selected references:")
    print(
        f"  monopole M2-M1: {finite_part('mono2-mono1', args.det_cutoff, args.mu2):.8g}"
    )
    print(
        f"  ordinary-M1:    {finite_part('ordinary-mono1', args.det_cutoff, args.mu2):.8g}"
    )
    print()
    print("interpretation:")
    print("  look for native patterns first; assign SM analogs only after a")
    print("  metric-native invariant proves load-bearing")


if __name__ == "__main__":
    main()

