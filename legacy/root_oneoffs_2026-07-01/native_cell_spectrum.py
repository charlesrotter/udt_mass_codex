"""Dimensionless finite-cell spectra under the Matter Cell Postulate.

This script assumes the candidate postulate:

    finite-action negative-phi core + compact angular source + phi=0 cell boundary

Operationally:
    - Solve f_xx + f_x + 2 s W(x) f = 0 inside a cell.
    - Normalize f(R_cell)=1, i.e. phi=0 at the cell boundary.
    - The boundary layer/shell is not modeled; its job is to cancel the exterior
      tail and handle the derivative mismatch.
    - Compute scalar/angular Sturm-Liouville spectra on the finite cell.

The output is dimensionless omega*R_cell. Absolute masses would still require
a scale anchor or a derivation of R_cell.
"""

from __future__ import annotations

import argparse
import math

import numpy as np
from scipy.integrate import solve_ivp
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh

from native_core_solver import monopole_sector, ordinary_sector, p_roots, window


def solve_cell_profile(source: float, x_core: float, width: float, xmin: float, xb: float):
    roots = p_roots(source)
    if roots is None:
        raise ValueError("source exceeds real-root limit")
    p_soft, _ = roots

    def rhs(x, y):
        f, fx = y
        return [fx, -fx - 2.0 * source * window(float(x), x_core, width) * f]

    sol = solve_ivp(
        rhs,
        (xmin, xb),
        [1.0, -p_soft],
        rtol=1.0e-10,
        atol=1.0e-12,
        max_step=0.03,
    )
    if not sol.success:
        raise RuntimeError(sol.message)
    x = sol.t
    f = sol.y[0]
    fx = sol.y[1]
    f_boundary = f[-1]
    return x, f / f_boundary, fx / f_boundary, p_soft


def interp_profile(x: np.ndarray, f: np.ndarray):
    def interp(r: np.ndarray) -> np.ndarray:
        return np.interp(np.log(r), x, f)

    return interp


def build_matrices(
    f_func,
    angular_lambda: float,
    rmin: float,
    rmax: float,
    ngrid: int,
    outer_bc: str,
):
    r = np.linspace(rmin, rmax, ngrid)
    h = r[1] - r[0]
    r_half = 0.5 * (r[:-1] + r[1:])
    p_half = r_half * r_half * f_func(r_half)

    left = np.zeros(ngrid)
    right = np.zeros(ngrid)
    left[1:] = p_half
    right[:-1] = p_half

    if outer_bc == "dirichlet":
        right[-1] = rmax * rmax * float(f_func(np.array([rmax]))[0])
    elif outer_bc == "flux":
        right[-1] = 0.0
    else:
        raise ValueError("outer_bc must be dirichlet or flux")

    main = (left + right) / (h * h) + angular_lambda
    lower = -left[1:] / (h * h)
    upper = -right[:-1] / (h * h)
    weight = r * r / f_func(r)
    return (
        diags([lower, main, upper], [-1, 0, 1], format="csr"),
        diags(weight, 0, format="csr"),
    )


def spectrum(f_func, angular_lambda: float, rmin: float, ngrid: int, modes: int, outer_bc: str):
    A, B = build_matrices(f_func, angular_lambda, rmin, 1.0, ngrid, outer_bc)
    vals = eigsh(A, M=B, k=modes, sigma=0.0, which="LM", return_eigenvectors=False)
    vals = np.sort(np.maximum(vals, 0.0))
    return np.sqrt(vals)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eta", type=float, default=0.03)
    parser.add_argument("--x-core", type=float, default=-2.5)
    parser.add_argument("--width", type=float, default=0.5)
    parser.add_argument("--xmin", type=float, default=-20.0)
    parser.add_argument("--ngrid", type=int, default=1800)
    parser.add_argument("--modes", type=int, default=4)
    parser.add_argument("--electron-mev", type=float, default=0.51099895)
    parser.add_argument(
        "--electron-sector",
        choices=["monopole1", "monopole2", "ell1"],
        default="monopole1",
    )
    parser.add_argument(
        "--electron-bc",
        choices=["dirichlet", "flux"],
        default="flux",
    )
    args = parser.parse_args()

    sectors = {
        "monopole1": monopole_sector(1),
        "monopole2": monopole_sector(2),
        "ell1": ordinary_sector(1),
        "ell2": ordinary_sector(2),
    }
    rmin = math.exp(args.xmin)
    xb = 0.0  # R_cell = exp(0) = 1

    print("Dimensionless finite-cell spectra")
    print("R_cell=1, f(R_cell)=1; boundary layer not modeled")
    print(
        f"eta={args.eta:g} x_core={args.x_core:g} "
        f"width={args.width:g} xmin={args.xmin:g}"
    )
    print()

    sector_results = {}
    for key, sector in sectors.items():
        source = args.eta * sector.angular_lambda
        if p_roots(source) is None:
            print(f"{sector.label}: source={source:g} no real softened core")
            continue
        x, f, fx, p_soft = solve_cell_profile(
            source, args.x_core, args.width, args.xmin, xb
        )
        f_func = interp_profile(x, f)
        phi_inner = -0.5 * math.log(float(f[0]))
        boundary_slope = float(fx[-1])
        print(
            f"{sector.label}: lambda={sector.angular_lambda:g} deg={sector.degeneracy} "
            f"source={source:g} p={p_soft:.6g}"
        )
        print(
            f"  phi_inner={phi_inner:.6g} boundary_fx={boundary_slope:.6g} "
            f"f_max={float(np.max(f)):.6g}"
        )
        for bc in ["dirichlet", "flux"]:
            omega = spectrum(
                f_func, sector.angular_lambda, rmin, args.ngrid, args.modes, bc
            )
            sector_results[(key, bc)] = omega
            text = " ".join(f"{w:.6g}" for w in omega)
            print(f"  outer_bc={bc:9s} omega*R={text}")
        print()

    anchor_key = (args.electron_sector, args.electron_bc)
    if anchor_key not in sector_results:
        print("electron anchor unavailable for selected sector/bc")
        return

    omega_e = float(sector_results[anchor_key][0])
    scale_mev = args.electron_mev / omega_e
    print("Electron-anchor conversion")
    print(
        f"anchor sector={args.electron_sector} bc={args.electron_bc} "
        f"omega_e={omega_e:.8g}"
    )
    print(f"scale = m_e / omega_e = {scale_mev:.8g} MeV per dimensionless omega")
    print("anchored masses from same run:")
    for key, sector in sectors.items():
        for bc in ["dirichlet", "flux"]:
            omega = sector_results.get((key, bc))
            if omega is None:
                continue
            masses = omega * scale_mev
            text = " ".join(f"{m:.6g}" for m in masses)
            print(f"  {key:9s} {bc:9s} MeV={text}")


if __name__ == "__main__":
    main()
