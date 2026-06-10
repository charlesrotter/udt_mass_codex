"""Interpret gamma as a one-step partition trace.

If the boundary transfer is a short Euclidean/thermal step, the scalar weight is
naturally a trace over the boundary Hilbert/label space:

    Z_step = Tr exp(-S_step).

For N degenerate transported labels with S_step=eta/2, this gives

    Z_step = N exp(-eta/2).

This is not a proof that the UDT boundary action is a partition trace, but it
is a cleaner interpretation than treating gamma as a dominant eigenvalue.
"""

from __future__ import annotations

import math


N = 3
ETA = 1.0 / 18.0


def main() -> None:
    weights = [math.exp(-ETA / 2.0) for _ in range(N)]
    z_step = sum(weights)
    free_action = -math.log(z_step)

    print("Partition-trace interpretation")
    print(f"N={N}")
    print(f"eta={ETA:.12g}")
    print()
    print("per-label action S_i=eta/2")
    print(f"per-label weight={weights[0]:.12g}")
    print(f"Z_step=sum_i exp(-S_i)={z_step:.12g}")
    print(f"-log Z_step={free_action:.12g}")
    print()
    print("interpretation:")
    print("  gamma is a one-step partition trace over degenerate transported labels")
    print("  log gamma = log N - eta/2")
    print()
    print("verdict:")
    print("  trace interpretation explains why N labels add")
    print("  UDT still must derive the boundary partition/trace structure")


if __name__ == "__main__":
    main()
