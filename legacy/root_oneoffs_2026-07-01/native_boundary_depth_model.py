"""Boundary-count candidate for cascade depths.

This tests a possible native rule for the cascade depth:

    n(d) = N + 2(d - 1)

where

    N       = epsilon dimension,
    2       = two radial ends of a finite negative-phi cell,
    d - 1   = angular degrees after removing the common scalar mode.

The rule is a candidate count, not a derivation. It is useful only if it
selects the same depths found by the diagnostic without reading off the
target masses.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


N = 3
ETA = 1.0 / 18.0
GAMMA = N * math.exp(-ETA / 2.0)
ELECTRON_MEV = 0.51099895


@dataclass(frozen=True)
class Sector:
    key: str
    dimension: int
    coeff: float
    note: str
    admissible: bool = True
    epsilon_unique: bool = False


SECTORS = [
    Sector("M1", 2, 1.1343262, "lowest compact-flux doublet"),
    Sector("M2", 3, 1.54635, "lowest compact-flux triplet", epsilon_unique=True),
    Sector("E1", 3, 2.10394, "ordinary ell=1 triplet; p=1/3", epsilon_unique=True),
]


def depth_for_dimension(dimension: int) -> int:
    return N + 2 * (dimension - 1)


def main() -> None:
    ae = SECTORS[0].coeff
    print("Boundary-count cascade-depth model")
    print("candidate rule: n(d)=N+2(d-1)")
    print(f"N={N}")
    print(f"eta={ETA:.12g}")
    print(f"gamma=N exp(-eta/2)={GAMMA:.12g}")
    print()
    print("electron anchor:")
    print("  sector M1, n=0, mass=0.51099895 MeV")
    print()
    for sector in SECTORS:
        n = depth_for_dimension(sector.dimension)
        ratio = (sector.coeff / ae) * GAMMA**n
        mass = ELECTRON_MEV * ratio
        flags = []
        if sector.epsilon_unique:
            flags.append("epsilon-unique")
        if sector.key == "E1":
            flags.append("p=1/3")
        print(f"{sector.key}: {sector.note}")
        print(f"  d={sector.dimension} -> n={n}")
        print(f"  ratio={ratio:.8g}")
        print(f"  mass_MeV={mass:.8g}")
        print(f"  flags={','.join(flags) if flags else 'none'}")
        print()

    print("candidate stable read:")
    print("  M1 cascade at d=2 gives a muon-like depth n=5")
    print("  E1 cascade at d=3 gives a tau-like depth n=7")
    print("  M2 is a competing d=3 compact-flux triplet and needs a native exclusion")
    print()
    print("verdict:")
    print("  the depth count can be stated without target masses")
    print("  but it still needs a derivation of why M2 is not the tau-like branch")


if __name__ == "__main__":
    main()
