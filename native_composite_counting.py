"""Composite counting under safe angular Layer-C selection rules.

This is kinematic bookkeeping only. It asks:

    given one-particle matter-cell sectors with dimensions d,
    which three-cell combinations are eligible for the unique epsilon rule?

No binding, confinement, mass addition rule, or color force is assumed.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import combinations_with_replacement


@dataclass(frozen=True)
class Sector:
    key: str
    dimension: int
    kind: str
    omega_flux: float | None
    note: str


# Reference eta=0.03, x_core=-2.5, flux-boundary modes from native_cell_spectrum.py.
SECTORS = [
    Sector("M1", 2, "monopole n=1 lowest", 1.13314, "doublet; electron-anchor candidate"),
    Sector("M2", 3, "monopole n=2 lowest", 1.54289, "triplet; epsilon eligible"),
    Sector("E1", 3, "ordinary ell=1", 2.08975, "triplet; epsilon eligible"),
]


def epsilon_unique(sector: Sector) -> bool:
    return sector.dimension == 3


def combo_label(combo: tuple[Sector, ...]) -> str:
    return "+".join(sector.key for sector in combo)


def naive_sum(combo: tuple[Sector, ...]) -> float | None:
    if any(sector.omega_flux is None for sector in combo):
        return None
    return sum(float(sector.omega_flux) for sector in combo)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--electron-mev", type=float, default=0.51099895)
    parser.add_argument("--electron-omega", type=float, default=1.13314)
    parser.add_argument("--m1-omega", type=float, default=1.13314)
    parser.add_argument("--m2-omega", type=float, default=1.54289)
    parser.add_argument("--e1-omega", type=float, default=2.08975)
    args = parser.parse_args()
    scale = args.electron_mev / args.electron_omega

    sectors = [
        Sector("M1", 2, "monopole n=1 lowest", args.m1_omega, "doublet; electron-anchor candidate"),
        Sector("M2", 3, "monopole n=2 lowest", args.m2_omega, "triplet; epsilon eligible"),
        Sector("E1", 3, "ordinary ell=1", args.e1_omega, "triplet; epsilon eligible"),
    ]

    print("Native composite counting, Layer-C only")
    print("No binding, no confinement, no mass rule; naive sums are diagnostics only.")
    print(
        f"electron anchor diagnostic: scale={scale:.8g} MeV per omega "
        f"(omega_e={args.electron_omega:g})"
    )
    print()

    print("single-cell sectors:")
    for sector in sectors:
        print(
            f"  {sector.key}: dim={sector.dimension} {sector.kind}, "
            f"omega={sector.omega_flux}, epsilon_eligible={epsilon_unique(sector)}"
        )
    print()

    print("three-cell same-sector epsilon eligibility:")
    for sector in sectors:
        count = 1 if epsilon_unique(sector) else 0
        omega = 3.0 * float(sector.omega_flux) if sector.omega_flux is not None else None
        mev = omega * scale if omega is not None else None
        print(
            f"  {sector.key}+{sector.key}+{sector.key}: "
            f"epsilon_count={count} naive_sum_omega={omega:.6g} "
            f"anchor_MeV={mev:.6g}"
        )
    print()

    print("three-cell mixed combinations:")
    for combo in combinations_with_replacement(sectors, 3):
        same = len({sector.key for sector in combo}) == 1
        if same:
            continue
        eligible = all(epsilon_unique(sector) for sector in combo) and len(
            {sector.key for sector in combo}
        ) == 1
        print(
            f"  {combo_label(combo):8s} epsilon_unique={eligible} "
            f"naive_sum_omega={naive_sum(combo):.6g} "
            f"anchor_MeV={naive_sum(combo) * scale:.6g}"
        )


if __name__ == "__main__":
    main()
