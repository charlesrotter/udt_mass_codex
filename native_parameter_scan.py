"""Parameter sensitivity scan for the finite matter-cell scaffold.

Scans classical shape parameters:

    eta       angular-source coupling
    x_core    source location inside the cell
    width     source transition width

and reports the range of dimensionless flux-boundary ratios relative to the
M1 sector. This tests whether the classical scaffold can hide large hierarchy in
its continuous shape parameters.
"""

from __future__ import annotations

import argparse
import math

import numpy as np

from native_cell_spectrum import interp_profile, solve_cell_profile, spectrum
from native_core_solver import monopole_sector, ordinary_sector, p_roots


def sector_omega(sector, eta: float, x_core: float, width: float, xmin: float, ngrid: int):
    source = eta * sector.angular_lambda
    if p_roots(source) is None:
        return None
    x, f, _fx, _p = solve_cell_profile(source, x_core, width, xmin, 0.0)
    f_func = interp_profile(x, f)
    return float(spectrum(f_func, sector.angular_lambda, math.exp(xmin), ngrid, 1, "flux")[0])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--etas", type=float, nargs="+", default=[0.005, 0.01, 0.03, 0.05, 0.06])
    parser.add_argument("--x-cores", type=float, nargs="+", default=[-4.0, -2.5, -1.0, 0.0])
    parser.add_argument("--widths", type=float, nargs="+", default=[0.25, 0.5, 1.0])
    parser.add_argument("--xmin", type=float, default=-20.0)
    parser.add_argument("--ngrid", type=int, default=900)
    args = parser.parse_args()

    sectors = {
        "M1": monopole_sector(1),
        "M2": monopole_sector(2),
        "E1": ordinary_sector(1),
    }

    rows = []
    for eta in args.etas:
        for x_core in args.x_cores:
            for width in args.widths:
                omegas = {
                    key: sector_omega(sector, eta, x_core, width, args.xmin, args.ngrid)
                    for key, sector in sectors.items()
                }
                if any(value is None for value in omegas.values()):
                    continue
                m1 = float(omegas["M1"])
                rows.append(
                    {
                        "eta": eta,
                        "x_core": x_core,
                        "width": width,
                        "M1": m1,
                        "M2_M1": float(omegas["M2"]) / m1,
                        "E1_M1": float(omegas["E1"]) / m1,
                    }
                )

    print("Matter-cell classical parameter sensitivity")
    print("flux-boundary ground modes; ratios relative to M1")
    print(f"valid samples={len(rows)}")
    print()

    for ratio_key in ["M2_M1", "E1_M1"]:
        values = np.array([row[ratio_key] for row in rows])
        imin = int(np.argmin(values))
        imax = int(np.argmax(values))
        print(f"{ratio_key}: min={values[imin]:.8g} max={values[imax]:.8g}")
        for label, idx in [("min", imin), ("max", imax)]:
            row = rows[idx]
            print(
                f"  {label}: eta={row['eta']:g} x_core={row['x_core']:g} "
                f"width={row['width']:g} M1={row['M1']:.6g} "
                f"{ratio_key}={row[ratio_key]:.6g}"
            )
        print()

    print("sample rows:")
    for row in rows[: min(10, len(rows))]:
        print(
            f"  eta={row['eta']:g} x_core={row['x_core']:g} width={row['width']:g} "
            f"M1={row['M1']:.6g} M2/M1={row['M2_M1']:.6g} E1/M1={row['E1_M1']:.6g}"
        )


if __name__ == "__main__":
    main()

