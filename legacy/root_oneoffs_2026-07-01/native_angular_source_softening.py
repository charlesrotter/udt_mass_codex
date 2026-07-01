"""Angular-source softening map for negative phi.

The C1 vacuum equation is

    phi'' + 2 phi'/r - 2(phi')^2 = 0.

For a softened endpoint

    f=e^{-2phi} ~ r^-p,  phi ~ -(p/2) ln r,

the left side becomes

    p(1-p) / (2 r^2).

Angular gradients on S^2 naturally scale like 1/r^2. This script maps an
effective angular source strength s=lambda*g into the two possible endpoint
powers:

    p(1-p)/2 = s.

The finite-action branch is the lower root p<1/2.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class AngularSector:
    label: str
    lam: float
    degeneracy: int


def ordinary(ell: int) -> AngularSector:
    return AngularSector(f"ell={ell}", float(ell * (ell + 1)), 2 * ell + 1)


def monopole(n: int, k: int = 0) -> AngularSector:
    s = abs(n) / 2.0
    j = s + k
    lam = j * (j + 1.0) - s * s
    return AngularSector(
        f"monopole n={n} k={k} j={j:g}", lam, int(round(2.0 * j + 1.0))
    )


def roots_for_source(source: float):
    disc = 1.0 - 8.0 * source
    if disc < 0.0:
        return None
    root = math.sqrt(max(disc, 0.0))
    return (0.5 * (1.0 - root), 0.5 * (1.0 + root))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--couplings", type=float, nargs="+", default=[0.01, 0.03, 0.06, 0.1])
    args = parser.parse_args()

    sectors = [
        ordinary(0),
        monopole(1),
        monopole(2),
        ordinary(1),
        ordinary(2),
    ]

    print("Angular-source softening map")
    print("equation: p(1-p)/2 = source = coupling * angular_lambda")
    print("finite C1 action branch requires p < 1/2")
    print("real softened roots require source <= 1/8")
    print()

    for coupling in args.couplings:
        print(f"coupling={coupling:g}")
        for sector in sectors:
            source = coupling * sector.lam
            roots = roots_for_source(source)
            if roots is None:
                print(
                    f"  {sector.label:24s} lambda={sector.lam:5.2f} "
                    f"source={source:8.5f}  no real p"
                )
                continue
            p_soft, p_hard = roots
            print(
                f"  {sector.label:24s} lambda={sector.lam:5.2f} "
                f"deg={sector.degeneracy:2d} source={source:8.5f} "
                f"p_soft={p_soft:8.5f} p_hard={p_hard:8.5f}"
            )
        print()


if __name__ == "__main__":
    main()

