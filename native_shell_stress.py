"""Idealized phi=0 shell stress for the Matter Cell Postulate.

At the finite cell boundary, the interior profile is normalized so f(R)=1.
The exterior flat closure has f_out=1 and f_x(out)=0. The only geometric jump is
therefore in f_x.

For a static spherical shell with f_in(R)=f_out(R)=1, the Israel junction
bookkeeping gives, up to sign convention for the normal:

    surface energy density sigma = 0
    tangential pressure P = (f_x(out)-f_x(in)) / (16 pi R)

with R=1 in the dimensionless cell units used here.

This script reports the required pressure-like shell load for each angular
sector in the current localized angular-source model.
"""

from __future__ import annotations

import argparse
import math

from native_cell_spectrum import solve_cell_profile
from native_core_solver import monopole_sector, ordinary_sector, p_roots


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--eta", type=float, default=0.03)
    parser.add_argument("--x-core", type=float, default=-2.5)
    parser.add_argument("--width", type=float, default=0.5)
    parser.add_argument("--xmin", type=float, default=-20.0)
    args = parser.parse_args()

    sectors = [
        monopole_sector(1),
        monopole_sector(2),
        ordinary_sector(1),
        ordinary_sector(2),
    ]

    print("Idealized phi=0 shell stress")
    print("R_cell=1, f_in=f_out=1, f_x(out)=0")
    print("sigma=0, P=(f_x(out)-f_x(in))/(16*pi)")
    print(
        f"eta={args.eta:g} x_core={args.x_core:g} "
        f"width={args.width:g} xmin={args.xmin:g}"
    )
    print()

    for sector in sectors:
        source = args.eta * sector.angular_lambda
        if p_roots(source) is None:
            print(f"{sector.label}: source={source:g} no real softened core")
            continue
        _x, _f, fx, p_soft = solve_cell_profile(
            source, args.x_core, args.width, args.xmin, 0.0
        )
        fx_in = float(fx[-1])
        jump = -fx_in
        pressure = jump / (16.0 * math.pi)
        print(
            f"{sector.label}: lambda={sector.angular_lambda:g} "
            f"deg={sector.degeneracy} source={source:g} p={p_soft:.6g}"
        )
        print(
            f"  f_x(in)={fx_in:.8g} jump={jump:.8g} "
            f"P_shell={pressure:.8g}"
        )
        print()


if __name__ == "__main__":
    main()

