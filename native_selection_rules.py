"""Selection-rule layer for the native matter-cell scaffold.

This applies only the safe angular Layer C:

    ell=1 gives a three-dimensional angular space;
    Lambda^3 of a three-dimensional space has one antisymmetric singlet.

The script deliberately does not compute binding, confinement, or a color force.
It only records which cell sectors are eligible for the epsilon selection rule.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CellSector:
    name: str
    dimension: int
    source: str
    note: str


SECTORS = [
    CellSector("ordinary ell=0", 1, "S2", "scalar singlet by itself; no epsilon triple"),
    CellSector("monopole n=1 lowest", 2, "compact flux P2", "doublet; no unique epsilon triple"),
    CellSector("monopole n=2 lowest", 3, "compact flux P2", "triplet; epsilon triple eligible"),
    CellSector("ordinary ell=1", 3, "S2", "triplet; epsilon triple eligible"),
    CellSector("ordinary ell=2", 5, "S2", "five-dimensional; antisymmetric triples not unique"),
]


def antisymmetric_triple_count(dimension: int) -> int:
    if dimension < 3:
        return 0
    return dimension * (dimension - 1) * (dimension - 2) // 6


def main() -> None:
    print("Native angular selection rules")
    print("selection only: no binding, no color force, no confinement")
    print()
    for sector in SECTORS:
        count = antisymmetric_triple_count(sector.dimension)
        verdict = "unique epsilon eligible" if count == 1 else "not unique epsilon"
        print(f"{sector.name}")
        print(f"  dimension={sector.dimension} source={sector.source}")
        print(f"  Lambda^3 count={count} -> {verdict}")
        print(f"  note: {sector.note}")
        print()


if __name__ == "__main__":
    main()

