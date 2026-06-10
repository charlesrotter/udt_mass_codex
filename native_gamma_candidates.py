"""Native candidates for the epsilon-cascade scale factor.

This collects simple dimensionless quantities already present in the
eta=1/18 negative-phi/angular frame and compares them with the hierarchy-fit
gamma from native_epsilon_cascade.py.
"""

from __future__ import annotations

import math


ETA = 1.0 / 18.0
N = 3.0
LAMBDA_ELL1 = 2.0
TARGET_GAMMA = 2.92451


def endpoint_p(eta: float, lam: float) -> float:
    # p(1-p)/2 = eta lambda; finite-action branch uses p <= 1/2.
    disc = 1.0 - 8.0 * eta * lam
    if disc < 0:
        return float("nan")
    return (1.0 - math.sqrt(disc)) / 2.0


def main() -> None:
    p = endpoint_p(ETA, LAMBDA_ELL1)
    candidates = [
        ("epsilon dimension N", N),
        ("inverse ell=1 endpoint exponent 1/p", 1.0 / p),
        ("N * exp(-eta/2)", N * math.exp(-ETA / 2.0)),
        ("N * (1 - eta/2)", N * (1.0 - ETA / 2.0)),
        ("N * exp(-eta)", N * math.exp(-ETA)),
        ("N * (1 - eta)", N * (1.0 - ETA)),
        ("N - eta", N - ETA),
        ("N - 1/(2N^2)", N - ETA),
        ("N - 1/(2N)", N - 1.0 / (2.0 * N)),
    ]

    print("Native gamma candidates")
    print(f"eta={ETA:.12g}")
    print(f"ell=1 lambda={LAMBDA_ELL1:g}")
    print(f"ell=1 endpoint p={p:.12g}")
    print(f"hierarchy-fit gamma={TARGET_GAMMA:.6g}")
    print()
    for name, value in candidates:
        print(
            f"{name:40s} gamma={value:.8g} "
            f"log_error_vs_fit={math.log(value / TARGET_GAMMA):+.6f}"
        )
    print()
    print("verdict:")
    print("  gamma=3 is native in two independent ways: N=3 and ell=1 p=1/3")
    print("  the fitted gamma is close to a small eta/2 correction of 3")
    print("  no correction rule is derived yet")


if __name__ == "__main__":
    main()
