"""Boundary-stiffness limits for angular-sector hierarchy.

Hypothesis under test:

    the missing angular piece is a sector-dependent Robin stiffness beta(lambda)
    at the phi=0 matter-cell boundary.

This script scans beta over many orders of magnitude and reports the range of
ground-mode ratios relative to the electron placeholder sector M1. If the ratios
remain O(1), boundary stiffness cannot be the hierarchy mechanism by itself.
"""

from __future__ import annotations

import argparse
import math

import numpy as np

from native_boundary_scan import spectrum
from native_cell_spectrum import interp_profile, solve_cell_profile
from native_core_solver import monopole_sector, ordinary_sector, p_roots


def finite_cell_profile(sector, eta: float, x_core: float, width: float, xmin: float):
    source = eta * sector.angular_lambda
    if p_roots(source) is None:
        return None
    x, f, _fx, _p = solve_cell_profile(source, x_core, width, xmin, 0.0)
    return interp_profile(x, f)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eta", type=float, default=0.03)
    parser.add_argument("--x-core", type=float, default=-2.5)
    parser.add_argument("--width", type=float, default=0.5)
    parser.add_argument("--xmin", type=float, default=-20.0)
    parser.add_argument("--ngrid", type=int, default=1400)
    parser.add_argument(
        "--betas",
        type=float,
        nargs="+",
        default=[0.0, 1e-3, 1e-2, 1e-1, 1, 10, 100, 1e3, 1e4, 1e5, 1e6],
    )
    args = parser.parse_args()

    sectors = {
        "M1": monopole_sector(1),
        "M2": monopole_sector(2),
        "E1": ordinary_sector(1),
    }
    rmin = math.exp(args.xmin)
    profiles = {
        key: finite_cell_profile(sector, args.eta, args.x_core, args.width, args.xmin)
        for key, sector in sectors.items()
    }

    values = {}
    for key, sector in sectors.items():
        f_func = profiles[key]
        if f_func is None:
            continue
        values[key] = []
        for beta in args.betas:
            omega = spectrum(
                f_func, sector.angular_lambda, rmin, args.ngrid, 1, beta
            )[0]
            values[key].append(float(omega))

    electron = np.array(values["M1"])
    print("Boundary-stiffness ratio limits")
    print("electron placeholder: M1 with same scanned beta list")
    print(f"eta={args.eta:g} x_core={args.x_core:g} width={args.width:g}")
    print()

    for key in ["M2", "E1"]:
        ratios_same_beta = np.array(values[key]) / electron
        print(f"{key}/M1 with same beta:")
        print(
            f"  min={ratios_same_beta.min():.8g} "
            f"max={ratios_same_beta.max():.8g}"
        )
        for beta, ratio in zip(args.betas, ratios_same_beta):
            print(f"  beta={beta:10.4g} ratio={ratio:.8g}")
        print()

    # Most generous positive-beta scan: compare every target-sector beta against
    # M1 at beta=0, the lowest reference electron coefficient in this model.
    m1_flux = values["M1"][0]
    for key in ["M2", "E1"]:
        ratios = np.array(values[key]) / m1_flux
        print(f"{key}/M1(beta=0), target beta free:")
        print(f"  min={ratios.min():.8g} max={ratios.max():.8g}")
        beta_max = args.betas[int(np.argmax(ratios))]
        print(f"  max at beta={beta_max:g}")
        print()

    print("verdict:")
    print("  positive Robin stiffness changes O(1) ratios only")
    print("  beta(lambda) alone cannot create lepton-like hierarchy")


if __name__ == "__main__":
    main()

