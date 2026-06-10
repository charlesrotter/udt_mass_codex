"""Minimal epsilon transfer-matrix model.

If the epsilon sector supplies N equivalent transfer channels and the boundary
closure supplies a universal quadratic penalty eta/2 per transfer, the transfer
matrix is

    T = exp(-eta/2) I_N

and the effective step multiplier is

    gamma = tr(T) = N exp(-eta/2).

This is a compact model of the current ansatz, not a derivation from the UDT
action. It identifies the exact mathematical object the boundary calculation
would need to produce.
"""

from __future__ import annotations

import argparse
import math


def multiplier(n: int, eta: float, split: float) -> float:
    return n * math.exp(-split * eta)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, default=3)
    parser.add_argument("--eta", type=float, default=None)
    parser.add_argument("--splits", type=float, nargs="+", default=[0.0, 0.25, 0.5, 1.0])
    args = parser.parse_args()

    eta = args.eta if args.eta is not None else 1.0 / (2.0 * args.N * args.N)
    print("Minimal epsilon transfer-matrix model")
    print("T = exp(-s eta) I_N")
    print("gamma = tr(T) = N exp(-s eta)")
    print(f"N={args.N}")
    print(f"eta={eta:.12g}")
    print()
    for split in args.splits:
        gamma = multiplier(args.N, eta, split)
        print(f"s={split:.6g} gamma={gamma:.12g}")
    print()
    print("working case:")
    print(f"  s=1/2 -> gamma={multiplier(args.N, eta, 0.5):.12g}")
    print()
    print("required derivation:")
    print("  show boundary transfer space is exactly N-dimensional")
    print("  show the transfer matrix is proportional to identity at leading order")
    print("  show the universal exponent split is s=1/2")


if __name__ == "__main__":
    main()
