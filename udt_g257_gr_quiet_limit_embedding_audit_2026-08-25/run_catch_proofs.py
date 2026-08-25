#!/usr/bin/env python3
"""Hostile semantic catches for the bounded G257 formulas."""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path


OUT = Path(__file__).with_name("CATCH_PROOF_RESULT.json")


def main() -> None:
    r = F(7, 2)
    c = F(-3, 5)
    f = 1 + c / r
    fp = -c / r**2
    fpp = 2 * c / r**3
    u = -c / r
    p = -u / (2 * (1 - u))
    zeta = u * (2 - u) / (2 * (1 - u) ** 2)
    f_a, f_b, f_c = F(2, 3), F(3, 4), F(4, 5)
    fp_off, fpp_off = F(2, 7), F(-1, 9)

    catches = {
        "deleted_f_minus_one_term": r * fp + f != 0,
        "corrupted_angular_component": r * fp - r**2 * fpp / 2 != 0,
        "wrong_residual_dependence_factor": (2 * fp_off + r * fpp_off)
        != (r * fp_off + r**2 * fpp_off / 2) / r,
        "wrong_parallel_sign": f * (2 * p**2 + p - zeta) != 3 * u / 2,
        "wrong_perp_sign": 1 - f * (1 + p) != -3 * u / 2,
        "inverted_pair_ratio": f_b / f_a != f_a / f_b,
        "broken_pair_composition": (f_b / f_a) * (f_c / f_b) != f_a / f_c,
    }
    assert all(catches.values())
    result = {"status": "PASS", "caught": catches, "caught_count": len(catches)}
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
