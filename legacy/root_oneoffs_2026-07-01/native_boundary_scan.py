"""Boundary-layer audit for the finite matter-cell scaffold.

The Matter Cell Postulate currently hides the phi=0 boundary layer. This script
exposes two things:

1. The geometric derivative jump required to match the interior finite-action
   core to an exterior flat cell boundary.
2. The dependence of the finite-cell spectrum on a Robin boundary condition
   at R_cell=1:

       p(R) R'(R) + beta R(R) = 0

   beta=0 is natural zero-flux. Large beta approaches Dirichlet.

If spectra/ratios move substantially with beta, then the boundary layer is a
load-bearing postulate, not a harmless technical boundary condition.
"""

from __future__ import annotations

import argparse
import math

import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh

from native_cell_spectrum import interp_profile, solve_cell_profile
from native_core_solver import monopole_sector, ordinary_sector, p_roots


def build_matrices(f_func, angular_lambda: float, rmin: float, ngrid: int, beta: float):
    rmax = 1.0
    r = np.linspace(rmin, rmax, ngrid)
    h = r[1] - r[0]
    r_half = 0.5 * (r[:-1] + r[1:])
    p_half = r_half * r_half * f_func(r_half)

    left = np.zeros(ngrid)
    right = np.zeros(ngrid)
    left[1:] = p_half
    right[:-1] = p_half

    # Robin boundary contributes beta * R(R)^2 to the quadratic form.
    main = (left + right) / (h * h) + angular_lambda
    main[-1] += beta

    lower = -left[1:] / (h * h)
    upper = -right[:-1] / (h * h)
    weight = r * r / f_func(r)
    return (
        diags([lower, main, upper], [-1, 0, 1], format="csr"),
        diags(weight, 0, format="csr"),
    )


def spectrum(f_func, angular_lambda: float, rmin: float, ngrid: int, modes: int, beta: float):
    A, B = build_matrices(f_func, angular_lambda, rmin, ngrid, beta)
    vals = eigsh(A, M=B, k=modes, sigma=0.0, which="LM", return_eigenvectors=False)
    vals = np.sort(np.maximum(vals, 0.0))
    return np.sqrt(vals)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eta", type=float, default=0.03)
    parser.add_argument("--x-core", type=float, default=-2.5)
    parser.add_argument("--width", type=float, default=0.5)
    parser.add_argument("--xmin", type=float, default=-20.0)
    parser.add_argument("--ngrid", type=int, default=1600)
    parser.add_argument("--modes", type=int, default=4)
    parser.add_argument("--betas", type=float, nargs="+", default=[0, 0.1, 1, 10, 100])
    args = parser.parse_args()

    sectors = [
        ("monopole1", monopole_sector(1)),
        ("monopole2", monopole_sector(2)),
        ("ell1", ordinary_sector(1)),
    ]
    rmin = math.exp(args.xmin)

    print("Matter-cell boundary-layer Robin scan")
    print("R_cell=1, f(R)=1, exterior flat requires f_x(out)=0")
    print(f"eta={args.eta:g} x_core={args.x_core:g} width={args.width:g}")
    print()

    for key, sector in sectors:
        source = args.eta * sector.angular_lambda
        if p_roots(source) is None:
            print(f"{key}: no real softened core")
            continue

        x, f, fx, p_soft = solve_cell_profile(
            source, args.x_core, args.width, args.xmin, 0.0
        )
        f_func = interp_profile(x, f)
        boundary_fx = float(fx[-1])
        # If outside is exactly flat, f_x jumps from boundary_fx to 0.
        jump_fx = -boundary_fx
        phi_x_inside = -boundary_fx / 2.0
        print(
            f"{key}: lambda={sector.angular_lambda:g} deg={sector.degeneracy} "
            f"source={source:g} p={p_soft:.6g}"
        )
        print(
            f"  boundary f_x(in)={boundary_fx:.8g} "
            f"jump_to_flat={jump_fx:.8g} phi_x(in)={phi_x_inside:.8g}"
        )
        print("  beta scan:")
        for beta in args.betas:
            omega = spectrum(f_func, sector.angular_lambda, rmin, args.ngrid, args.modes, beta)
            ratios = omega / omega[0]
            omega_text = " ".join(f"{w:.6g}" for w in omega)
            ratio_text = " ".join(f"{q:.5g}" for q in ratios[: min(3, len(ratios))])
            print(
                f"    beta={beta:9.4g} omega={omega_text} "
                f"ratios={ratio_text}"
            )
        print()


if __name__ == "__main__":
    main()

