"""Audit the formal scalar d=1 closure branch.

The closure count n=N+2(d-1) gives n=3 for d=1. If allowed with the same
transfer multiplier, this would predict a scalar-like branch near 12.7 MeV.

The current elementary matter-cell frame excludes it because d=1 has no
non-scalar angular boundary data and no epsilon triplet structure. This script
keeps that exclusion explicit.
"""

from __future__ import annotations

import math


N = 3
ETA = 1.0 / 18.0
GAMMA = N * math.exp(-ETA / 2.0)
ELECTRON_MEV = 0.51099895


def main() -> None:
    n_scalar = N
    mass_scalar = ELECTRON_MEV * GAMMA**n_scalar
    print("Formal scalar-branch audit")
    print(f"N={N}")
    print(f"gamma={GAMMA:.12g}")
    print(f"formal d=1 closure depth={n_scalar}")
    print(f"formal mass={mass_scalar:.8g} MeV")
    print()
    print("native exclusion candidates:")
    print("  d=1 has no non-scalar angular boundary constraints")
    print("  d=1 has no unique epsilon triplet selection")
    print("  d=1 is a scalar cell/background mode, not an elementary matter branch")
    print("  clean dilaton/scalar sector is gapless continuum in the canonical rebuild")
    print()
    print("verdict:")
    print("  scalar d=1 must be explicitly excluded or reclassified")
    print("  otherwise the cascade predicts a low scalar-like state")


if __name__ == "__main__":
    main()
