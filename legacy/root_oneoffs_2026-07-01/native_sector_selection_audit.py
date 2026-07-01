"""Audit sector-selection rules for the cascade model.

The boundary-count rule gives d=3 -> n=7 for both M2 and E1. This script
separates possible native filters that could select E1 as the stable triplet
branch without using the target mass.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


ETA = 1.0 / 18.0
N = 3


@dataclass(frozen=True)
class Sector:
    key: str
    family: str
    flux: int
    ell: int | None
    dimension: int
    lam: float
    coeff: float


SECTORS = [
    Sector("M1", "compact-flux", 1, None, 2, 0.5, 1.1343262),
    Sector("M2", "compact-flux", 2, None, 3, 1.0, 1.54635),
    Sector("E1", "ordinary", 0, 1, 3, 2.0, 2.10394),
]


def p_soft(lam: float) -> float:
    disc = 1.0 - 8.0 * ETA * lam
    if disc < 0.0:
        return float("nan")
    return 0.5 * (1.0 - math.sqrt(disc))


def lambda3_count(dimension: int) -> int:
    if dimension < 3:
        return 0
    return dimension * (dimension - 1) * (dimension - 2) // 6


def main() -> None:
    print("Cascade sector-selection audit")
    print(f"N={N}")
    print(f"eta={ETA:.12g}")
    print()
    print("sector invariants")
    for sector in SECTORS:
        p = p_soft(sector.lam)
        print(f"{sector.key}:")
        print(f"  family={sector.family}")
        print(f"  flux={sector.flux}")
        print(f"  dimension={sector.dimension}")
        print(f"  lambda={sector.lam:g}")
        print(f"  p={p:.8g}")
        print(f"  Lambda3_count={lambda3_count(sector.dimension)}")
        print(f"  primitive_flux={sector.flux in (0, 1)}")
        print(f"  endpoint_matches_1/N={abs(p - 1/N) < 1e-10}")
        print()

    filters = [
        (
            "Fprimitive",
            "allow only zero flux or minimal compact flux",
            lambda s: s.flux in (0, 1),
        ),
        (
            "Fendpoint",
            "for d=3 stable branch require p=1/N",
            lambda s: s.dimension != 3 or abs(p_soft(s.lam) - 1.0 / N) < 1e-10,
        ),
        (
            "Fepsilon",
            "for triplet branch require unique epsilon",
            lambda s: s.dimension != 3 or lambda3_count(s.dimension) == 1,
        ),
    ]

    print("filter effects")
    for name, description, predicate in filters:
        kept = [sector.key for sector in SECTORS if predicate(sector)]
        print(f"  {name}: {description}")
        print(f"    kept={', '.join(kept)}")
    print()

    combined = [
        sector.key
        for sector in SECTORS
        if sector.flux in (0, 1)
        and (sector.dimension != 3 or abs(p_soft(sector.lam) - 1.0 / N) < 1e-10)
    ]
    print("combined primitive + d=3 endpoint filter")
    print(f"  kept={', '.join(combined)}")
    print()
    print("verdict:")
    print("  M2 can be excluded by either primitive-flux or p=1/N triplet selection")
    print("  both filters are native-looking but neither is derived yet")


if __name__ == "__main__":
    main()
