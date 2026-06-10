"""Softened negative-phi endpoint audit.

Use the one-parameter family

    f(r) = 1 + (a/r)^p

so phi -> -infinity at r -> 0 for p > 0, but the C1-like dilation
action is finite only for p < 1/2.

This script reports local source/curvature scalings and repeats the
scalar/angular finite-box test for softened p values.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh


@dataclass(frozen=True)
class PowerProfile:
    p: float
    a: float = 1.0

    def f(self, r: np.ndarray) -> np.ndarray:
        return 1.0 + (self.a / r) ** self.p

    def vacuum_residual_power(self) -> str:
        # f'' + 2f'/r ~ c p(p-1) r^(-p-2)
        coeff = self.p * (self.p - 1.0)
        return f"{coeff:+.6g} * r^(-{self.p + 2.0:.6g})"

    def gtt_power(self) -> str:
        # G^t_t = (r f' + f - 1)/r^2 ~ c(1-p) r^(-p-2)
        coeff = 1.0 - self.p
        return f"{coeff:+.6g} * r^(-{self.p + 2.0:.6g})"

    def ricci_power(self) -> str:
        # R ~ -c(p-1)(p-2) r^(-p-2)
        coeff = -(self.p - 1.0) * (self.p - 2.0)
        return f"{coeff:+.6g} * r^(-{self.p + 2.0:.6g})"


def finite_c1_action(p: float) -> bool:
    return 0.0 <= p < 0.5


def build_matrices(profile: PowerProfile, ell: int, rmin: float, rmax: float, n: int):
    r = np.linspace(rmin, rmax, n)
    h = r[1] - r[0]
    r_half = 0.5 * (r[:-1] + r[1:])
    p_half = r_half * r_half * profile.f(r_half)

    left = np.zeros(n)
    right = np.zeros(n)
    left[1:] = p_half
    right[:-1] = p_half
    right[-1] = rmax * rmax * float(profile.f(np.array([rmax]))[0])

    q = float(ell * (ell + 1))
    main = (left + right) / (h * h) + q
    lower = -left[1:] / (h * h)
    upper = -right[:-1] / (h * h)
    weight = r * r / profile.f(r)
    return (
        diags([lower, main, upper], [-1, 0, 1], format="csr"),
        diags(weight, 0, format="csr"),
    )


def lowest(profile: PowerProfile, ell: int, rmax: float, n: int, k: int):
    A, B = build_matrices(profile, ell, 1.0e-5, rmax, n)
    vals = eigsh(A, M=B, k=k, sigma=0.0, which="LM", return_eigenvectors=False)
    vals = np.sort(np.maximum(vals, 0.0))
    return np.sqrt(vals)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--powers", type=float, nargs="+", default=[0.25, 0.49, 1.0])
    parser.add_argument("--a", type=float, default=1.0)
    parser.add_argument("--rmax", type=float, nargs="+", default=[40.0, 80.0, 160.0])
    parser.add_argument("--n", type=int, default=1400)
    parser.add_argument("--k", type=int, default=3)
    args = parser.parse_args()

    print("Softened negative-phi endpoint audit")
    print("profile: f=1+(a/r)^p")
    print("C1 finite action iff p < 1/2")
    print()

    for p in args.powers:
        profile = PowerProfile(p=p, a=args.a)
        print(f"p={p:g} a={args.a:g} finite_C1_action={finite_c1_action(p)}")
        print(f"  vacuum residual f''+2f'/r ~ {profile.vacuum_residual_power()}")
        print(f"  Einstein G^t_t=G^r_r       ~ {profile.gtt_power()}")
        print(f"  Ricci scalar R              ~ {profile.ricci_power()}")
        for ell in [0, 1, 2]:
            print(f"  ell={ell}")
            for rmax in args.rmax:
                modes = lowest(profile, ell, rmax, args.n, args.k)
                text = " ".join(f"{m:.6g}" for m in modes)
                print(
                    f"    Rmax={rmax:6.1f} omega={text} "
                    f"omega1*Rmax={modes[0] * rmax:.6g}"
                )
        print()


if __name__ == "__main__":
    main()

