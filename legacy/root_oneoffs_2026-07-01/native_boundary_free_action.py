"""Boundary free-action ledger for cascade depths.

If gamma is a one-step partition trace,

    gamma = exp(log N - eta/2),

then a branch with closure depth n carries log amplification

    n(log N - eta/2)

plus any angular coefficient ratio. This script records the current branches in
that additive log language.
"""

from __future__ import annotations

import math


N = 3
ETA = 1.0 / 18.0
LOG_GAMMA = math.log(N) - ETA / 2.0
E1_RATIO = 2.10394 / 1.1343262


def main() -> None:
    branches = [
        ("electron", "M1", 0, 1.0),
        ("mu-like", "M1", 5, 1.0),
        ("tau-like", "E1", 7, E1_RATIO),
    ]

    print("Boundary free-action ledger")
    print(f"N={N}")
    print(f"eta={ETA:.12g}")
    print(f"log gamma=log N - eta/2={LOG_GAMMA:.12g}")
    print()
    for label, sector, depth, coeff in branches:
        log_ratio = math.log(coeff) + depth * LOG_GAMMA
        print(label)
        print(f"  sector={sector}")
        print(f"  depth={depth}")
        print(f"  log angular coeff={math.log(coeff):+.12g}")
        print(f"  boundary log contribution={depth * LOG_GAMMA:+.12g}")
        print(f"  total log ratio={log_ratio:+.12g}")
        print(f"  ratio={math.exp(log_ratio):.12g}")
        print()
    print("verdict:")
    print("  the ladder is additive in boundary free action")
    print("  deriving log gamma may be easier than deriving gamma directly")


if __name__ == "__main__":
    main()
