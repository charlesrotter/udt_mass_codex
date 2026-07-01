"""Epsilon-mediated angular constraint model.

This is a minimal model for why every closure unit, including angular endpoint
constraints, would carry the same log N degeneracy.

Assumption:
    each closure constraint is solved by choosing one of N transported epsilon
    frame labels, and each choice carries the same unit action eta/2.

Then every independent closure constraint contributes

    log Z_unit = log(sum_i exp(-eta/2)) = log N - eta/2.

This is still an assumption, but it is now explicit.
"""

from __future__ import annotations

import argparse
import math


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, default=3)
    parser.add_argument("--dimension", type=int, default=3)
    args = parser.parse_args()

    eta = 1.0 / (2.0 * args.N * args.N)
    unit_z = args.N * math.exp(-eta / 2.0)
    unit_log = math.log(unit_z)
    n_constraints = args.N + 2 * (args.dimension - 1)
    total_log = n_constraints * unit_log

    print("Epsilon-mediated constraint model")
    print(f"N={args.N}")
    print(f"d={args.dimension}")
    print(f"eta={eta:.12g}")
    print()
    print("unit closure constraint:")
    print("  choices=N transported epsilon labels")
    print("  action per choice=eta/2")
    print(f"  Z_unit=N exp(-eta/2)={unit_z:.12g}")
    print(f"  log Z_unit={unit_log:.12g}")
    print()
    print(f"independent closure constraints={n_constraints}")
    print(f"total log contribution={total_log:.12g}")
    print()
    print("verdict:")
    print("  this explains how angular constraints could inherit log N")
    print("  but it must be derived: angular closure must be epsilon-mediated")


if __name__ == "__main__":
    main()
