"""Mass-ladder candidate with reduced postulate ledger.

This keeps the same numerical ladder but updates the dependency language:

    Pbundle0: primitive nontrivial compact U(1) line-bundle sector may be
              occupied by elementary negative-phi matter cells.

Given Pbundle0, M1 transport/primitive selection follows from topology and
flux-energy ordering.
"""

from __future__ import annotations

import math


N = 3
ETA = 1.0 / 18.0
GAMMA = N * math.exp(-ETA / 2.0)
ELECTRON_MEV = 0.51099895
M1 = 1.1343262
E1 = 2.10394
TARGET_MU = 105.6583755
TARGET_TAU = 1776.86


def main() -> None:
    mu = ELECTRON_MEV * GAMMA**5
    tau = ELECTRON_MEV * (E1 / M1) * GAMMA**7
    print("Reduced-postulate ladder")
    print("Pbundle0 + metric-derived ordinary frame + closure/depth/gamma candidate")
    print(f"gamma={GAMMA:.12g}")
    print()
    print("branches:")
    print("  electron: M1 primitive compact bundle |n|=1, anchored")
    print("  mu-like:  M1 primitive compact bundle, closure depth 5")
    print("  tau-like: E1 ordinary triplet, closure depth 7")
    print()
    print(f"mu-like mass={mu:.8g} MeV error={(mu / TARGET_MU - 1):+.3%}")
    print(f"tau-like mass={tau:.8g} MeV error={(tau / TARGET_TAU - 1):+.3%}")
    print()
    print("remaining postulates:")
    print("  Pbundle0: primitive compact bundle may be occupied")
    print("  Pepsilon/Punit: eta=1/(2N^2), unit transfer action eta/2")
    print("  Pdepth: closure constraints map to gamma transfers")


if __name__ == "__main__":
    main()
