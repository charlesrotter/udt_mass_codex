"""Elementary branch filter for the current negative-phi matter-cell frame."""

from __future__ import annotations

import math
from dataclasses import dataclass


N = 3
ETA = 1.0 / 18.0


@dataclass(frozen=True)
class Sector:
    key: str
    family: str
    dimension: int
    lam: float
    flux: int
    note: str


SECTORS = [
    Sector("O0", "ordinary", 1, 0.0, 0, "scalar/background"),
    Sector("M1", "compact-flux", 2, 0.5, 1, "primitive compact-flux doublet"),
    Sector("M2", "compact-flux", 3, 1.0, 2, "nonprimitive compact-flux triplet"),
    Sector("E1", "ordinary", 3, 2.0, 0, "ordinary ell=1 self-similar triplet"),
    Sector("O2", "ordinary", 5, 6.0, 0, "ordinary ell=2/quintet"),
]


def p_soft(lam: float) -> float | None:
    source = ETA * lam
    disc = 1.0 - 8.0 * source
    if disc < 0.0:
        return None
    return 0.5 * (1.0 - math.sqrt(disc))


def lambda3_count(dimension: int) -> int:
    if dimension < 3:
        return 0
    return dimension * (dimension - 1) * (dimension - 2) // 6


def verdict(sector: Sector) -> tuple[str, list[str]]:
    reasons: list[str] = []
    p = p_soft(sector.lam)
    if p is None:
        return "excluded", ["no real finite-action softened endpoint"]
    if p <= 0.0:
        return "excluded", ["p=0; no negative-phi matter endpoint"]
    if p >= 0.5:
        return "excluded", ["infinite-action endpoint"]

    primitive_flux = sector.flux in (0, 1)
    endpoint_resonant = abs(p - 1.0 / N) < 1e-10
    epsilon_unique = lambda3_count(sector.dimension) == 1

    if sector.key == "M1":
        if primitive_flux:
            reasons.append("primitive compact-flux doublet")
            reasons.append("nontrivial finite-action endpoint")
            return "elementary anchor candidate", reasons
    if sector.key == "E1":
        if primitive_flux and epsilon_unique and endpoint_resonant:
            reasons.append("zero-flux ordinary triplet")
            reasons.append("unique epsilon eligible")
            reasons.append("endpoint resonance p=1/N")
            return "elementary cascade candidate", reasons
    if not primitive_flux:
        reasons.append("nonprimitive compact flux")
    if sector.dimension == 3 and not endpoint_resonant:
        reasons.append("triplet but not p=1/N endpoint")
    if not reasons:
        reasons.append("no elementary selection rule")
    return "diagnostic/non-elementary", reasons


def main() -> None:
    print("Elementary branch filter")
    print(f"N={N}")
    print(f"eta={ETA:.12g}")
    print()
    for sector in SECTORS:
        p = p_soft(sector.lam)
        status, reasons = verdict(sector)
        print(f"{sector.key}: {sector.note}")
        print(f"  family={sector.family} dimension={sector.dimension} flux={sector.flux}")
        print(f"  lambda={sector.lam:g} p={p if p is not None else 'no-real-branch'}")
        print(f"  status={status}")
        for reason in reasons:
            print(f"    - {reason}")
        print()
    print("verdict:")
    print("  current elementary branches are M1 anchor and E1 cascade")
    print("  O0/O2 are excluded; M2 remains diagnostic/non-elementary")


if __name__ == "__main__":
    main()
