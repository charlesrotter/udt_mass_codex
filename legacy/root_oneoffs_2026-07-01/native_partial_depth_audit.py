"""Audit the absence of partial cascade depths.

The current model uses closure depths n=0, 5, and 7. If every intermediate
power of gamma were a stable branch, the model would predict extra light
charged lepton-like states. Therefore the depth rule must be a closure rule:
only complete boundary/epsilon cascades are admissible.
"""

from __future__ import annotations

import math


N = 3
ETA = 1.0 / 18.0
GAMMA = N * math.exp(-ETA / 2.0)
ELECTRON_MEV = 0.51099895
E1_RATIO = 2.10394 / 1.1343262


def main() -> None:
    print("Partial-depth audit")
    print(f"gamma={GAMMA:.12g}")
    print("If partial M1 depths were stable:")
    for n in range(0, 8):
        mass = ELECTRON_MEV * GAMMA**n
        marker = "allowed anchor" if n == 0 else ("allowed closure" if n == 5 else "must be forbidden/transient")
        print(f"  M1 n={n}: mass={mass:10.6g} MeV  {marker}")
    print()
    print("If partial E1 depths were stable:")
    for n in range(0, 8):
        mass = ELECTRON_MEV * E1_RATIO * GAMMA**n
        marker = "allowed closure" if n == 7 else "must be forbidden/transient"
        print(f"  E1 n={n}: mass={mass:10.6g} MeV  {marker}")
    print()
    print("verdict:")
    print("  Pdepth must be an admissibility/closure rule, not a free excitation ladder")
    print("  otherwise extra low-mass states appear immediately")


if __name__ == "__main__":
    main()
