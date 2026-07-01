"""Log-scale requirements for hierarchy via sector-dependent radii.

If mass hierarchy is carried by cell radii,

    M_i/M_e = (c_i/c_e) * (R_e/R_i)

then

    Delta_i = ln(R_e/R_i)

is the logarithmic scale separation a running/collective mechanism would need
to generate. This script reports Delta for candidate assignments.
"""

from __future__ import annotations

import argparse
import math

from native_required_radii import COEFFS, TARGETS


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--electron-coeff", default="M1_1")
    args = parser.parse_args()

    c_e = COEFFS[args.electron_coeff]
    print("Running/log-scale requirements")
    print(f"electron coefficient {args.electron_coeff}={c_e:g}")
    print("Delta = ln(R_e/R_i) = ln((M_i/M_e)/(c_i/c_e))")
    print()
    for target, mass_ratio in TARGETS.items():
        print(f"target={target} mass_ratio={mass_ratio:g}")
        for label, coeff in COEFFS.items():
            coeff_ratio = coeff / c_e
            delta = math.log(mass_ratio / coeff_ratio)
            print(
                f"  {label:5s} coeff_ratio={coeff_ratio:9.5g} "
                f"Delta={delta:9.5f}"
            )
        print()

    print("verdict:")
    print("  lepton-like hierarchy requires log separations of order 3-8")
    print("  this is not produced by the classical cell spectrum, but is plausible")
    print("  territory for a true running/collective mechanism if UDT has one")


if __name__ == "__main__":
    main()

