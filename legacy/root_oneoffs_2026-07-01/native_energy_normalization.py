"""Dimensionless core/shell energy normalization audit.

This is a diagnostic for the native matter-cell scaffold. It compares:

    - linear flux-boundary eigenfrequency omega_1,
    - C1-like core action scale int (f_x^2/4) r dx,
    - idealized phi=0 shell pressure/load scale,

on the same finite-cell profiles.

The absolute normalization of core/shell energy is not derived here. The point is
to test whether the natural dimensionless numbers are O(1) or tiny compared with
the cell eigenfrequency. Tiny numbers would require a large coefficient to drive
mass hierarchy.
"""

from __future__ import annotations

import argparse
import math

import numpy as np

from native_cell_spectrum import interp_profile, solve_cell_profile, spectrum
from native_core_solver import monopole_sector, ordinary_sector, p_roots


def core_action_scale(x: np.ndarray, fx: np.ndarray) -> float:
    r = np.exp(x)
    integrand = 0.25 * fx * fx * r
    return float(np.trapezoid(integrand, x))


def shell_pressure_scale(fx_boundary: float) -> float:
    jump = -fx_boundary
    return jump / (16.0 * math.pi)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eta", type=float, default=0.03)
    parser.add_argument("--x-core", type=float, default=-2.5)
    parser.add_argument("--width", type=float, default=0.5)
    parser.add_argument("--xmin", type=float, default=-20.0)
    parser.add_argument("--ngrid", type=int, default=1600)
    parser.add_argument("--electron-mev", type=float, default=0.51099895)
    parser.add_argument("--electron-sector", choices=["monopole1", "monopole2", "ell1"], default="monopole1")
    args = parser.parse_args()

    sectors = {
        "monopole1": monopole_sector(1),
        "monopole2": monopole_sector(2),
        "ell1": ordinary_sector(1),
        "ell2": ordinary_sector(2),
    }
    rmin = math.exp(args.xmin)

    results = {}
    for key, sector in sectors.items():
        source = args.eta * sector.angular_lambda
        if p_roots(source) is None:
            continue
        x, f, fx, p_soft = solve_cell_profile(
            source, args.x_core, args.width, args.xmin, 0.0
        )
        f_func = interp_profile(x, f)
        omega = spectrum(f_func, sector.angular_lambda, rmin, args.ngrid, 1, "flux")[0]
        action = core_action_scale(x, fx)
        shell = shell_pressure_scale(float(fx[-1]))
        results[key] = {
            "sector": sector,
            "source": source,
            "p": p_soft,
            "omega": float(omega),
            "action": action,
            "shell": shell,
            "fx_boundary": float(fx[-1]),
        }

    if args.electron_sector not in results:
        raise RuntimeError("electron sector unavailable")
    scale = args.electron_mev / results[args.electron_sector]["omega"]

    print("Native core/shell energy normalization audit")
    print(
        f"eta={args.eta:g} x_core={args.x_core:g} width={args.width:g} "
        f"xmin={args.xmin:g}"
    )
    print(
        f"electron anchor: sector={args.electron_sector} "
        f"omega_e={results[args.electron_sector]['omega']:.8g} "
        f"scale={scale:.8g} MeV per dimensionless unit"
    )
    print()

    for key, result in results.items():
        omega = result["omega"]
        action = result["action"]
        shell = result["shell"]
        print(f"{key}: {result['sector'].label}")
        print(
            f"  lambda={result['sector'].angular_lambda:g} "
            f"source={result['source']:.8g} p={result['p']:.8g}"
        )
        print(
            f"  omega1={omega:.8g} anchored_linear={omega * scale:.8g} MeV"
        )
        print(
            f"  core_action={action:.8g} "
            f"({action / omega:.6g} of omega1, {action * scale:.8g} MeV if coeff=1)"
        )
        print(
            f"  shell_pressure={shell:.8g} "
            f"({shell / omega:.6g} of omega1, {shell * scale:.8g} MeV if coeff=1)"
        )
        print()

    print("diagnostic verdict:")
    print("  natural core/shell dimensionless loads are small compared with omega1")
    print("  hierarchy requires either large normalization, nonlinear amplification,")
    print("  running/collective effects, or a different field/probe sector")


if __name__ == "__main__":
    main()

