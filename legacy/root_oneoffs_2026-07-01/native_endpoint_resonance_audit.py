"""Endpoint-resonance audit for the triplet cascade branch.

The endpoint softening equation is

    p(1-p)/2 = eta * lambda.

With the working epsilon normalization eta=1/(2N^2), the condition p=1/N
requires

    lambda = N - 1.

For N=3, this selects lambda=2, the ordinary ell=1 angular sector. This gives a
native reason to prefer E1 over the compact-flux M2 triplet, whose shifted
monopole lambda is 1.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


N = 3
ETA = 1.0 / (2.0 * N * N)


@dataclass(frozen=True)
class Sector:
    key: str
    family: str
    dimension: int
    lam: float


SECTORS = [
    Sector("O0", "ordinary", 1, 0.0),
    Sector("M1", "compact-flux", 2, 0.5),
    Sector("M2", "compact-flux", 3, 1.0),
    Sector("E1", "ordinary", 3, 2.0),
    Sector("O2", "ordinary", 5, 6.0),
]


def p_soft(lam: float) -> float | None:
    disc = 1.0 - 8.0 * ETA * lam
    if disc < 0.0:
        return None
    return 0.5 * (1.0 - math.sqrt(disc))


def main() -> None:
    p_res = 1.0 / N
    lambda_res = (p_res * (1.0 - p_res) / 2.0) / ETA
    print("Endpoint-resonance audit")
    print(f"N={N}")
    print(f"eta=1/(2N^2)={ETA:.12g}")
    print(f"resonant endpoint p=1/N={p_res:.12g}")
    print(f"required lambda={lambda_res:.12g}")
    print()
    print("sector check")
    for sector in SECTORS:
        p = p_soft(sector.lam)
        p_text = "no real finite-action branch" if p is None else f"{p:.10g}"
        resonance = p is not None and abs(p - p_res) < 1e-10
        print(f"{sector.key}:")
        print(f"  family={sector.family}")
        print(f"  dimension={sector.dimension}")
        print(f"  lambda={sector.lam:g}")
        print(f"  p={p_text}")
        print(f"  p=1/N resonance={resonance}")
        print()
    print("verdict:")
    print("  eta=1/(2N^2) plus p=1/N selects lambda=N-1")
    print("  for N=3 this selects ordinary ell=1, not compact-flux M2")


if __name__ == "__main__":
    main()
