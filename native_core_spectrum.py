"""Scalar/angular spectrum on the localized angular-source softened core.

This tests whether the first constructive ensemble background changes the
previous box-controlled spectrum result.

Background:
    f_xx + f_x + 2 s W(x) f = 0, x=ln r

Probe:
    -(r^2 f R')' + Lambda R = omega^2 (r^2/f) R

where Lambda can be ordinary ell(ell+1) or a monopole angular eigenvalue.
"""

from __future__ import annotations

import argparse
import math

import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh

from native_core_solver import (
    monopole_sector,
    ordinary_sector,
    p_roots,
    solve_profile,
)


def f_interpolator(source: float, x_core: float, width: float, xmin: float, xmax: float):
    profile = solve_profile(source, x_core, width, xmin, xmax)
    x = profile["x"]
    f = profile["f"]

    def interp(r: np.ndarray) -> np.ndarray:
        xr = np.log(r)
        values = np.interp(xr, x, f)
        # For r beyond solved range, use normalized exterior f=1+a/r.
        high = xr > x[-1]
        if np.any(high):
            values[high] = 1.0 + profile["a_tail"] / r[high]
        return values

    return interp, profile


def build_matrices(f_func, angular_lambda: float, rmin: float, rmax: float, ngrid: int):
    r = np.linspace(rmin, rmax, ngrid)
    h = r[1] - r[0]
    r_half = 0.5 * (r[:-1] + r[1:])
    p_half = r_half * r_half * f_func(r_half)

    left = np.zeros(ngrid)
    right = np.zeros(ngrid)
    left[1:] = p_half
    right[:-1] = p_half
    right[-1] = rmax * rmax * float(f_func(np.array([rmax]))[0])

    main = (left + right) / (h * h) + angular_lambda
    lower = -left[1:] / (h * h)
    upper = -right[:-1] / (h * h)
    weight = r * r / f_func(r)
    return (
        diags([lower, main, upper], [-1, 0, 1], format="csr"),
        diags(weight, 0, format="csr"),
    )


def lowest_modes(f_func, angular_lambda: float, rmin: float, rmax: float, ngrid: int, k: int):
    A, B = build_matrices(f_func, angular_lambda, rmin, rmax, ngrid)
    vals = eigsh(A, M=B, k=k, sigma=0.0, which="LM", return_eigenvectors=False)
    vals = np.sort(np.maximum(vals, 0.0))
    return np.sqrt(vals)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eta", type=float, default=0.03)
    parser.add_argument("--x-core", type=float, default=0.0)
    parser.add_argument("--width", type=float, default=0.5)
    parser.add_argument("--xmin", type=float, default=-20.0)
    parser.add_argument("--rmax", type=float, nargs="+", default=[40.0, 80.0, 160.0])
    parser.add_argument("--ngrid", type=int, default=1400)
    parser.add_argument("--modes", type=int, default=3)
    args = parser.parse_args()

    sectors = [
        monopole_sector(1),
        monopole_sector(2),
        ordinary_sector(1),
    ]
    xmax = math.log(max(args.rmax)) + 2.0
    rmin = math.exp(args.xmin)

    print("Spectrum on localized angular-source softened core")
    print(f"eta={args.eta:g} x_core={args.x_core:g} width={args.width:g}")
    print()
    for sector in sectors:
        source = args.eta * sector.angular_lambda
        if p_roots(source) is None:
            print(f"{sector.label}: no real softened core")
            continue
        f_func, profile = f_interpolator(source, args.x_core, args.width, args.xmin, xmax)
        print(
            f"{sector.label}: lambda={sector.angular_lambda:g} deg={sector.degeneracy} "
            f"source={source:g} p={profile['p_soft']:.6g} a_tail={profile['a_tail']:.6g}"
        )
        for rmax in args.rmax:
            omega = lowest_modes(
                f_func, sector.angular_lambda, rmin, rmax, args.ngrid, args.modes
            )
            text = " ".join(f"{x:.6g}" for x in omega)
            print(
                f"  Rmax={rmax:6.1f} omega={text} "
                f"omega1*Rmax={omega[0] * rmax:.6g}"
            )
        print()


if __name__ == "__main__":
    main()

