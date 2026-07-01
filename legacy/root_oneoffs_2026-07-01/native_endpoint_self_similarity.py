"""Self-similar endpoint closure diagnostic.

For f=e^{-2phi} ~ r^-p, the C1 action density scales as r^(-2p), so the
near-endpoint action below a cutoff epsilon scales as

    S(0, epsilon) ~ epsilon^(1 - 2p).

A possible native closure condition is that the finite-action remainder scales
with the same exponent as the softened endpoint profile:

    1 - 2p = p.

This selects p=1/3. Combined with eta=1/18, it selects lambda=2.
"""

from __future__ import annotations

import argparse


def action_remainder_exponent(p: float) -> float:
    return 1.0 - 2.0 * p


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eta", type=float, default=1.0 / 18.0)
    parser.add_argument("--p", type=float, nargs="+", default=[0.059041448, 0.127322004, 1.0 / 3.0, 0.49])
    args = parser.parse_args()

    p_self = 1.0 / 3.0
    lambda_self = (p_self * (1.0 - p_self) / 2.0) / args.eta
    print("Endpoint self-similarity diagnostic")
    print("endpoint profile exponent: p")
    print("finite-action remainder exponent: 1-2p")
    print("self-similar closure condition: 1-2p = p")
    print(f"selected p={p_self:.12g}")
    print(f"with eta={args.eta:.12g}, selected lambda={lambda_self:.12g}")
    print()
    for p in args.p:
        rem = action_remainder_exponent(p)
        print(
            f"p={p:.10g}  remainder_exponent={rem:.10g}  "
            f"remainder/profile={rem / p if p != 0 else float('inf'):.10g}"
        )
    print()
    print("verdict:")
    print("  p=1/3 can be selected by endpoint action/profile self-similarity")
    print("  this is a closure principle, not yet a theorem from the variational problem")


if __name__ == "__main__":
    main()
