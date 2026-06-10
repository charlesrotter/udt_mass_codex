"""Scale-covariance audit for the native matter-cell scaffold.

Once the cell profile is solved in x=ln(r/R), the dimensionless spectrum and
dimensionless core/shell loads are fixed by angular labels and couplings. This
script shows how a change of cell radius R rescales classical energies.

If every term scales as coefficient/R, then one electron anchor fixes the scale
and no classical hierarchy can emerge from changing R unless different sectors
are assigned different radii by an additional dynamical rule.
"""

from __future__ import annotations

import argparse


REFERENCE = {
    "M1_flux": 1.13314,
    "M2_flux": 1.54289,
    "E1_flux": 2.08975,
    "M1_core": 0.000042276,
    "M2_core": 0.00019850,
    "E1_core": 0.0011849,
    "M1_shell": 0.000076074,
    "M2_shell": 0.00015943,
    "E1_shell": 0.00035730,
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--radii", type=float, nargs="+", default=[0.5, 1.0, 2.0, 10.0])
    parser.add_argument("--electron-mev", type=float, default=0.51099895)
    parser.add_argument("--electron-coeff", type=float, default=REFERENCE["M1_flux"])
    args = parser.parse_args()

    scale_at_r1 = args.electron_mev / args.electron_coeff
    print("Native matter-cell scale covariance audit")
    print("classical terms tested as E_i(R)=coefficient_i/R")
    print(
        f"electron anchor at R=1: coeff_e={args.electron_coeff:g}, "
        f"scale={scale_at_r1:.8g} MeV"
    )
    print()

    for radius in args.radii:
        print(f"R_cell={radius:g}")
        for key, coeff in REFERENCE.items():
            energy = scale_at_r1 * coeff / radius
            print(f"  {key:9s} coeff={coeff:12.6g} E={energy:12.6g} MeV")
        print()

    print("verdict:")
    print("  changing a common R rescales all classical terms together")
    print("  hierarchy requires sector-dependent radii, large coefficients,")
    print("  nonlinear/quantum running, or an additional field/probe mechanism")


if __name__ == "__main__":
    main()

