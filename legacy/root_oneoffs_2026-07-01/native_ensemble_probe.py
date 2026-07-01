"""Minimal native ensemble probe.

Combines two non-Dirac instruments:

1. softened negative-phi radial geometry: f=1+(a/r)^p with p<1/2;
2. angular/topological monopole sectors on S^2:
      lambda = j(j+1) - (n/2)^2, j=|n|/2+k.

It still uses the scalar Sturm-Liouville radial operator. The test is whether
the combined radial+angular+topological structure creates non-box-controlled
low modes. If omega scales as 1/Rmax, the linear scalar ensemble is still not
the particle sector.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh


@dataclass(frozen=True)
class Sector:
    label: str
    angular_lambda: float
    degeneracy: int


def ordinary_sector(ell: int) -> Sector:
    return Sector(f"ordinary ell={ell}", float(ell * (ell + 1)), 2 * ell + 1)


def monopole_sector(n: int, k: int = 0) -> Sector:
    s = abs(n) / 2.0
    j = s + k
    lam = j * (j + 1.0) - s * s
    return Sector(f"monopole n={n} k={k} j={j:g}", lam, int(round(2.0 * j + 1.0)))


def f_power(r: np.ndarray, p: float, a: float) -> np.ndarray:
    return 1.0 + (a / r) ** p


def build_matrices(sector: Sector, p: float, a: float, rmax: float, ngrid: int):
    r = np.linspace(1.0e-5, rmax, ngrid)
    h = r[1] - r[0]
    r_half = 0.5 * (r[:-1] + r[1:])
    p_half = r_half * r_half * f_power(r_half, p, a)

    left = np.zeros(ngrid)
    right = np.zeros(ngrid)
    left[1:] = p_half
    right[:-1] = p_half
    right[-1] = rmax * rmax * float(f_power(np.array([rmax]), p, a)[0])

    main = (left + right) / (h * h) + sector.angular_lambda
    lower = -left[1:] / (h * h)
    upper = -right[:-1] / (h * h)
    weight = r * r / f_power(r, p, a)

    A = diags([lower, main, upper], [-1, 0, 1], format="csr")
    B = diags(weight, 0, format="csr")
    return A, B


def modes(sector: Sector, p: float, a: float, rmax: float, ngrid: int, k: int):
    A, B = build_matrices(sector, p, a, rmax, ngrid)
    vals = eigsh(A, M=B, k=k, sigma=0.0, which="LM", return_eigenvectors=False)
    vals = np.sort(np.maximum(vals, 0.0))
    return np.sqrt(vals)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--powers", type=float, nargs="+", default=[0.25, 0.49])
    parser.add_argument("--a", type=float, default=1.0)
    parser.add_argument("--rmax", type=float, nargs="+", default=[40.0, 80.0, 160.0])
    parser.add_argument("--ngrid", type=int, default=1400)
    parser.add_argument("--modes", type=int, default=3)
    args = parser.parse_args()

    sectors = [
        ordinary_sector(0),
        ordinary_sector(1),
        ordinary_sector(2),
        monopole_sector(1),
        monopole_sector(2),
    ]

    print("Minimal native ensemble probe")
    print("radial: f=1+(a/r)^p, using finite-action p<1/2")
    print("angular: ordinary and monopole S^2 sectors")
    print()
    for p in args.powers:
        print(f"p={p:g} a={args.a:g}")
        for sector in sectors:
            print(
                f"  {sector.label}, lambda={sector.angular_lambda:g}, "
                f"degeneracy={sector.degeneracy}"
            )
            for rmax in args.rmax:
                omega = modes(sector, p, args.a, rmax, args.ngrid, args.modes)
                text = " ".join(f"{x:.6g}" for x in omega)
                print(
                    f"    Rmax={rmax:6.1f} omega={text} "
                    f"omega1*Rmax={omega[0] * rmax:.6g}"
                )
        print()


if __name__ == "__main__":
    main()

