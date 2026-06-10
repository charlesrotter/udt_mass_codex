"""Derive the scalar d=1 exclusion from endpoint softening.

The formal closure count gives n=N for d=1, but the ordinary scalar sector has

    lambda = 0.

The endpoint softening equation

    p(1-p)/2 = eta lambda

then gives p=0 on the finite-action branch. That is not a negative-phi matter
endpoint; it is the trivial/no-angular-source case. So the d=1 formal closure
count is not an elementary matter-cell branch.
"""

from __future__ import annotations

import math


N = 3
ETA = 1.0 / 18.0


def p_soft(lam: float) -> float:
    source = ETA * lam
    disc = 1.0 - 8.0 * source
    if disc < 0.0:
        return float("nan")
    return 0.5 * (1.0 - math.sqrt(disc))


def main() -> None:
    sectors = [
        ("O0 scalar", 1, 0.0),
        ("M1 doublet", 2, 0.5),
        ("M2 triplet", 3, 1.0),
        ("E1 ordinary triplet", 3, 2.0),
        ("O2 ordinary quintet", 5, 6.0),
    ]
    print("Scalar exclusion derivation")
    print("endpoint equation: p(1-p)/2 = eta lambda")
    print(f"eta={ETA:.12g}")
    print()
    for label, dimension, lam in sectors:
        p = p_soft(lam)
        print(f"{label}:")
        print(f"  dimension={dimension}")
        print(f"  lambda={lam:g}")
        print(f"  p_soft={p:.10g}")
        print(f"  negative_phi_endpoint={p > 0.0 and p < 0.5}")
        print()
    print("verdict:")
    print("  d=1/lambda=0 gives p=0, so it does not form a negative-phi matter endpoint")
    print("  the formal scalar closure depth is reclassified as non-matter/background")


if __name__ == "__main__":
    main()
