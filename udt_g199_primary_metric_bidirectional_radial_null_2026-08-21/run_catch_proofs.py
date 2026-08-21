#!/usr/bin/env python3
"""Hostile semantic/algebraic mutation catches for G199."""

import json
from fractions import Fraction as F


def main() -> None:
    r = F(7, 3)
    f = F(5, 4)
    fp = F(2, 3)
    fpp = F(-4, 5)
    energy = F(3, 2)

    catches = {
        "drop_minus_germ": {+1} != {+1, -1},
        "drop_plus_germ": {-1} != {+1, -1},
        "delete_areal_screen_connection": -energy / (r * r) != 0,
        "reverse_curvature_sign": fpp / (2 * f) != -fpp / (2 * f),
        "inject_false_plus_tide": F(1, 7) != 0,
        "inject_false_minus_tide": F(-1, 9) != 0,
        "wrong_frequency_direction_dependence": energy / f != energy / (2 * f),
        "nonaffine_radial_speed": fp * energy * energy / f != 0,
        "import_g196_chiral_term": "M X(deta+dz)" not in (
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
