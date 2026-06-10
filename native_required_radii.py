"""Required sector-dependent radii for target mass ratios.

Given dimensionless cell coefficients c_i and an electron anchor c_e, a target
mass ratio M_i/M_e requires

    R_i/R_e = (c_i/c_e) / (M_i/M_e).

This script does not claim any assignment is correct. It quantifies how extreme
sector-dependent radii would have to be if the classical cell scaffold were used
to represent heavier particles.
"""

from __future__ import annotations

import argparse


COEFFS = {
    # eta=0.03, x_core=-2.5, flux-boundary modes from native_cell_spectrum.py.
    "M1_1": 1.13314,
    "M1_2": 5.05625,
    "M1_3": 8.31705,
    "M2_1": 1.54289,
    "M2_2": 5.43846,
    "M2_3": 8.73016,
    "E1_1": 2.08975,
    "E1_2": 6.01677,
    "E1_3": 9.37339,
}

TARGETS = {
    "muon": 206.768283,
    "tau": 3477.15,
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--electron-coeff", default="M1_1")
    args = parser.parse_args()

    c_e = COEFFS[args.electron_coeff]
    print("Required sector-dependent radii")
    print(f"electron anchor coefficient {args.electron_coeff}={c_e:g}")
    print("formula: R_i/R_e = (c_i/c_e)/(M_i/M_e)")
    print()
    for target, ratio in TARGETS.items():
        print(f"target={target} M/M_e={ratio:g}")
        for label, coeff in COEFFS.items():
            radius_ratio = (coeff / c_e) / ratio
            inverse = 1.0 / radius_ratio
            print(
                f"  {label:5s} coeff_ratio={coeff / c_e:9.5g} "
                f"R_i/R_e={radius_ratio:12.6g} R_e/R_i={inverse:12.6g}"
            )
        print()

    print("verdict:")
    print("  classical coefficients are O(1-10), so lepton-like mass ratios")
    print("  require cell radii smaller by roughly 10^2-10^3 unless another")
    print("  mechanism supplies the hierarchy")


if __name__ == "__main__":
    main()

