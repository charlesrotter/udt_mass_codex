"""Generic radius-flow models for matter cells.

This tests whether simple UDT-native energy scalings can generate sector-
dependent radii.

Base finite-cell energy scales like A/R. A stationary radius needs at least one
opposing positive-power term:

    E(R) = A/R + B R^q.

Then

    R_* = (A/(B q))^(1/(q+1)).

If B is common, sector radius ratios are only (A_i/A_e)^(1/(q+1)), too small to
make hierarchy from O(1) A_i. Hierarchy requires sector-dependent B, a running B,
or a non-power law.
"""

from __future__ import annotations

import argparse
import math


COEFFS = {
    "M1": 1.1343262,
    "M2": 1.54635,
    "E1": 2.10394,
}


def radius_ratio(a_i: float, a_e: float, q: float, b_ratio: float = 1.0) -> float:
    # R_i/R_e = [(A_i/A_e)/(B_i/B_e)]^(1/(q+1)).
    return ((a_i / a_e) / b_ratio) ** (1.0 / (q + 1.0))


def required_b_ratio(a_i: float, a_e: float, q: float, target_radius_ratio: float) -> float:
    # B_i/B_e = (A_i/A_e)/(R_i/R_e)^(q+1)
    return (a_i / a_e) / (target_radius_ratio ** (q + 1.0))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--powers", type=float, nargs="+", default=[1.0, 2.0, 3.0])
    parser.add_argument("--targets", type=float, nargs="+", default=[206.768283, 3477.15])
    args = parser.parse_args()

    a_e = COEFFS["M1"]
    print("Generic matter-cell radius-flow model")
    print("E(R)=A/R + B R^q")
    print("common B gives R_i/R_e=(A_i/A_e)^(1/(q+1))")
    print()

    for q in args.powers:
        print(f"q={q:g}")
        for key, coeff in COEFFS.items():
            rr = radius_ratio(coeff, a_e, q)
            print(f"  common B {key}: R_i/R_e={rr:.8g} mass_ratio_from_R={1/rr:.8g}")
        print("  required B_i/B_e for lepton-like target mass ratios:")
        for target in args.targets:
            print(f"    target M/M_e={target:g}")
            for key, coeff in COEFFS.items():
                # target mass ratio M_i/M_e = (A_i/A_e)/(R_i/R_e),
                # so target R_i/R_e = (A_i/A_e)/target.
                target_rr = (coeff / a_e) / target
                br = required_b_ratio(coeff, a_e, q, target_rr)
                print(f"      {key}: target_R={target_rr:.6g} B_i/B_e={br:.6g}")
        print()

    print("verdict:")
    print("  simple power-law radius stabilization with common coefficients")
    print("  cannot create hierarchy from O(1) A_i")
    print("  sector-dependent or running B is the real missing mechanism")


if __name__ == "__main__":
    main()

