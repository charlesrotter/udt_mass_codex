"""Audit route: eta fixed by the unique epsilon triplet.

Hypothesis:

    The endpoint angular-source coupling is global because only a 3-dimensional
    angular sector has a unique antisymmetric triple. Therefore the source
    normalization uses N=3, giving eta=1/(2N^2)=1/18.

This script checks the combinatoric facts and the resulting admissibility cap.
It cannot prove the physical step "epsilon uniqueness fixes eta"; it identifies
the exact remaining assumption.
"""

from __future__ import annotations

import math


def lambda3_count(n: int) -> int:
    if n < 3:
        return 0
    return n * (n - 1) * (n - 2) // 6


def p_soft(source: float):
    disc = 1.0 - 8.0 * source
    if disc < 0.0:
        return None
    return 0.5 * (1.0 - math.sqrt(disc))


def main() -> None:
    print("Eta epsilon-route audit")
    print("Hypothesis: unique Lambda^3 V singlet fixes global N=3 source dimension")
    print()
    for n in range(1, 8):
        count = lambda3_count(n)
        eta = 1.0 / (2.0 * n * n)
        cap = 1.0 / (8.0 * eta)
        unique = count == 1
        print(
            f"N={n} Lambda3_count={count:2d} unique={unique!s:5s} "
            f"eta_N={eta:.8g} lambda_cap={cap:.6g}"
        )
    print()

    eta = 1.0 / 18.0
    print("If unique epsilon fixes N=3 globally:")
    print(f"  eta={eta:.12g}")
    for label, lam in [("ordinary ell=1", 2.0), ("ordinary ell=2", 6.0)]:
        source = eta * lam
        print(
            f"  {label:16s} lambda={lam:g} source={source:.8g} "
            f"p={p_soft(source)} allowed={source < 1/8}"
        )
    print()
    print("audit verdict:")
    print("  combinatorics uniquely picks N=3, but the physical rule")
    print("  'global eta is fixed by the unique epsilon sector' remains an")
    print("  additional postulate unless derived from the boundary/source action")


if __name__ == "__main__":
    main()

