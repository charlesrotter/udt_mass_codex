"""Near-core scaling audit for negative-phi endpoints.

Let f=e^{-2 phi} ~ c r^-p as r -> 0. This covers:

    p=1: vacuum negative-mass Schwarzschild branch f~a/r
    p=2: radial flux back-reacted branch f~q^2/r^2

For the C1-like dilation action density used in the rebuild,

    S_phi density radial scaling ~ r^2 * e^{-2phi} * g^rr * (phi')^2
                                ~ r^2 * f * f * (phi')^2

and phi' ~ p/(2r), giving density ~ r^(-2p).

The radial integral int_0 r^(-2p) dr is finite only for p < 1/2.
"""

from __future__ import annotations

import argparse


def finite_action(p: float) -> bool:
    return p < 0.5


def integral_scaling(p: float, eps: float, rmax: float = 1.0) -> float:
    exponent = -2.0 * p
    if abs(exponent + 1.0) < 1.0e-12:
        import math

        return math.log(rmax / eps)
    return (rmax ** (exponent + 1.0) - eps ** (exponent + 1.0)) / (exponent + 1.0)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p", type=float, nargs="+", default=[0.25, 0.5, 1.0, 2.0])
    parser.add_argument("--eps", type=float, nargs="+", default=[1e-1, 1e-2, 1e-3, 1e-4])
    args = parser.parse_args()

    print("Negative-phi endpoint finite-action scaling")
    print("assume f=e^{-2phi} ~ c r^-p")
    print("C1 radial action density scales as r^(-2p)")
    print("finite near r=0 iff p < 1/2")
    print()
    for p in args.p:
        verdict = "finite" if finite_action(p) else "divergent"
        print(f"p={p:g} verdict={verdict}")
        values = [integral_scaling(p, eps) for eps in args.eps]
        for eps, value in zip(args.eps, values):
            print(f"  eps={eps:9.1e}  integral_scale={value:12.6g}")
        print()


if __name__ == "__main__":
    main()

