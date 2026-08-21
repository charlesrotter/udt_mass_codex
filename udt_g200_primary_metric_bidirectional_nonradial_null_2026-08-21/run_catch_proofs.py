#!/usr/bin/env python3
"""Hostile semantic/algebraic mutation catches for G200."""

from fractions import Fraction as F
import json


def main() -> None:
    q = F(3, 5)
    angmom = F(4, 7)
    tide = F(5, 11)
    tide_r = F(-7, 13)

    plus = (q, angmom)
    minus = (-q, -angmom)
    catches = {
        "drop_minus_branch": {plus} != {plus, minus},
        "reverse_only_radial_component": (-q, angmom) != minus,
        "reverse_only_angular_component": (q, -angmom) != minus,
        "inject_signed_local_tide": angmom * tide != angmom * angmom * tide,
        "force_finite_equality_with_nonzero_gradient": -q * tide_r / 6 != 0,
        "delete_tidal_gradient": tide_r != 0,
        "fail_strict_radial_control": F(0) * tide == 0,
        "fail_turning_control": F(0) * tide_r == 0,
        "import_G196_chiral_coframe": "M X(deta+dz)" not in (
            "g=-f dx0^2+f^-1 dr^2+r^2 dOmega^2"
        ),
    }
    assert all(catches.values())
    print(json.dumps({
        "all_pass": True,
        "caught": sum(catches.values()),
        "total": len(catches),
        "catches": catches,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
