"""Current native mass-ladder candidate.

This script is a diagnostic summary, not a canonized model.

Inputs still not fully derived:

    Pepsilon: eta = 1/(2N^2), N=3
    Pgamma:   gamma = N exp(-eta/2)
    Pdepth:   n(d) = N + 2(d - 1)
    Pselect:  primitive compact-flux doublet plus self-similar ordinary triplet
    F:        electron mass anchor

The point is to keep the current working chain auditable and target-visible.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


N = 3
ETA = 1.0 / (2.0 * N * N)
GAMMA = N * math.exp(-ETA / 2.0)
ELECTRON_MEV = 0.51099895

TARGETS = {
    "electron": ELECTRON_MEV,
    "mu_like": 105.6583755,
    "tau_like": 1776.86,
}


@dataclass(frozen=True)
class Branch:
    label: str
    sector: str
    dimension: int
    coeff: float
    depth: int
    note: str


BRANCHES = [
    Branch("electron_anchor", "M1", 2, 1.1343262, 0, "electron anchor, primitive compact flux"),
    Branch("mu_like", "M1", 2, 1.1343262, N + 2 * (2 - 1), "same primitive branch at d=2 cascade depth"),
    Branch("tau_like", "E1", 3, 2.10394, N + 2 * (3 - 1), "ordinary ell=1, self-similar p=1/3 branch"),
]


def main() -> None:
    anchor_coeff = BRANCHES[0].coeff
    print("Native mass-ladder candidate diagnostic")
    print(f"N={N}")
    print(f"eta=1/(2N^2)={ETA:.12g}")
    print(f"gamma=N exp(-eta/2)={GAMMA:.12g}")
    print(f"electron anchor={ELECTRON_MEV:.8g} MeV")
    print()
    print("branch predictions")
    for branch in BRANCHES:
        ratio = (branch.coeff / anchor_coeff) * GAMMA**branch.depth
        mass = ELECTRON_MEV * ratio
        target = TARGETS.get(branch.label)
        print(f"{branch.label}:")
        print(f"  sector={branch.sector}")
        print(f"  dimension={branch.dimension}")
        print(f"  depth={branch.depth}")
        print(f"  coeff_ratio={branch.coeff / anchor_coeff:.10g}")
        print(f"  predicted_ratio={ratio:.10g}")
        print(f"  predicted_mass_MeV={mass:.10g}")
        if target is not None:
            print(f"  diagnostic_target_MeV={target:.10g}")
            print(f"  fractional_error={(mass / target - 1.0):+.4%}")
        print(f"  note={branch.note}")
        print()
    print("verdict:")
    print("  the chain is compact and native-looking but still ansatz-bearing")
    print("  the next required work is deriving Pdepth/Pgamma from the cell action")


if __name__ == "__main__":
    main()
