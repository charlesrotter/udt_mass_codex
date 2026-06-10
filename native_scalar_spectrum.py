"""Native negative-phi scalar/angular spectrum probe.

This intentionally avoids Form-T, Dirac spinors, SM labels, fitted floor values,
and hard particle identifications. It solves the scalar/angular Sturm-Liouville
problem from negative_phi_native_geometry.md:

    -(r^2 f R')' + ell(ell+1) R = omega^2 (r^2/f) R

on finite boxes for the vacuum control f=1+a/r and a smooth regulated control.
If the low eigenvalues scale to zero as Rmax grows, the box is creating the
discreteness rather than the native negative-phi geometry.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh


@dataclass(frozen=True)
class Profile:
    name: str
    a: float = 2.0
    rho: float = 0.25
    charge: float = 1.0

    def f(self, r: np.ndarray) -> np.ndarray:
        if self.name == "vacuum":
            return 1.0 + self.a / r
        if self.name == "regulated":
            return 1.0 + self.a / np.sqrt(r * r + self.rho * self.rho)
        if self.name == "charged":
            return 1.0 + self.a / r + self.charge * self.charge / (r * r)
        raise ValueError(f"unknown profile: {self.name}")


def build_matrices(profile: Profile, ell: int, rmin: float, rmax: float, n: int):
    """Return sparse A, B for A R = omega^2 B R.

    Inner boundary: natural zero flux, p R' = 0.
    Outer boundary: Dirichlet control, R(rmax) = 0.
    """

    r = np.linspace(rmin, rmax, n)
    h = r[1] - r[0]

    r_half = 0.5 * (r[:-1] + r[1:])
    p_half = r_half * r_half * profile.f(r_half)
    p_left = np.zeros(n)
    p_right = np.zeros(n)
    p_left[1:] = p_half
    p_right[:-1] = p_half

    # Outer Dirichlet boundary contributes a final right flux using p(rmax).
    p_right[-1] = rmax * rmax * float(profile.f(np.array([rmax]))[0])

    q = float(ell * (ell + 1))
    main = (p_left + p_right) / (h * h) + q
    lower = -p_left[1:] / (h * h)
    upper = -p_right[:-1] / (h * h)

    weight = r * r / profile.f(r)
    A = diags([lower, main, upper], offsets=[-1, 0, 1], format="csr")
    B = diags(weight, offsets=0, format="csr")
    return A, B


def lowest_modes(profile: Profile, ell: int, rmax: float, n: int, k: int):
    rmin = 1.0e-4 if profile.name in {"vacuum", "charged"} else 0.0
    A, B = build_matrices(profile, ell, rmin, rmax, n)
    vals = eigsh(A, M=B, k=k, sigma=0.0, which="LM", return_eigenvectors=False)
    vals = np.sort(np.maximum(vals, 0.0))
    return np.sqrt(vals)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=1400)
    parser.add_argument("--k", type=int, default=4)
    parser.add_argument("--a", type=float, default=2.0)
    parser.add_argument("--rho", type=float, default=0.25)
    parser.add_argument("--charge", type=float, default=1.0)
    parser.add_argument("--rmax", type=float, nargs="+", default=[20.0, 40.0, 80.0])
    args = parser.parse_args()

    profiles = [
        Profile("vacuum", args.a, args.rho, args.charge),
        Profile("regulated", args.a, args.rho, args.charge),
        Profile("charged", args.a, args.rho, args.charge),
    ]
    ells = [0, 1, 2]

    print("Native scalar/angular finite-box spectrum")
    print("equation: -(r^2 f R')' + ell(ell+1)R = omega^2 (r^2/f)R")
    print("inner BC: natural zero flux; outer BC: Dirichlet finite-box control")
    print()

    for profile in profiles:
        print(
            f"profile={profile.name} a={profile.a:g} "
            f"rho={profile.rho:g} charge={profile.charge:g}"
        )
        for ell in ells:
            rows = []
            for rmax in args.rmax:
                modes = lowest_modes(profile, ell, rmax, args.n, args.k)
                rows.append((rmax, modes))
            print(f"  ell={ell}")
            for rmax, modes in rows:
                scaled = modes[0] * rmax
                mode_text = " ".join(f"{m:.6g}" for m in modes)
                print(f"    Rmax={rmax:6.1f} omega={mode_text}  omega1*Rmax={scaled:.6g}")
        print()


if __name__ == "__main__":
    main()
