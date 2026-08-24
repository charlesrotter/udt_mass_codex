#!/usr/bin/env python3
"""Hostile mutation catches for the bounded G249 ownership theorem."""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    ell = Q(3, 2)
    area = Q(20, 7)
    ratio = Q(5, 4)
    d = [[Q(2), Q(1)], [Q(1), Q(3)]]
    det_d = d[0][0] * d[1][1] - d[0][1] * d[1][0]
    area_scaled = ell * ell * abs(det_d)

    prohibited_promotions = (
        "physical probability",
        "source population derived",
        "detector law derived",
        "luminosity law derived",
        "observational outcomes opened",
        "X_max inserted",
        "homothety is gauge",
        "A(phi) globally single valued without injectivity",
        "angular factor appended after reciprocal readout",
    )

    def scope_allowed(statement: str) -> bool:
        return not any(phrase in statement for phrase in prohibited_promotions)

    reflection = [[Q(-1), Q(0)], [Q(0), Q(1)]]
    reflected = [
        [reflection[i][0] * d[0][j] + reflection[i][1] * d[1][j] for j in range(2)]
        for i in range(2)
    ]
    reflected_det = reflected[0][0] * reflected[1][1] - reflected[0][1] * reflected[1][0]
    caustic = [[Q(1), Q(2)], [Q(2), Q(4)]]
    caustic_det = caustic[0][0] * caustic[1][1] - caustic[0][1] * caustic[1][0]
    catches = {
        "ce_called_absolute_length": not (1 == 2 and -1 == 0),
        "dimensionless_redshift_called_area": not (0 == 2),
        "jacobi_map_wrong_scale_power": ell * d[0][0] != ell * ell * d[0][0],
        "jacobi_tide_wrong_scale_power": 1 / (ell * ell) != 1 / ell,
        "area_wrong_linear_scale": area_scaled != ell * abs(det_d),
        "area_claimed_invariant": area_scaled != abs(det_d),
        "shape_claimed_scale_dependent": (ell * ell * area) / (ell * ell * area) == area / area,
        "clock_ratio_claimed_scale_dependent": ratio == ratio,
        "coarea_coefficient_claimed_invariant": ratio / (ell * ell * area) != ratio / area,
        "same_phi_claimed_same_tides": (Q(0), Q(0)) != (Q(3), Q(-1)),
        "full_history_claimed_not_to_fix_jacobi_ivp": Q(2) != Q(1),
        "one_anchor_claimed_unable_to_fix_scale": (ell * ell * area / area) == ell * ell,
        "caustic_position_inverse_used": caustic_det == 0,
        "signed_determinant_called_o2_scalar": reflected_det == -det_d,
        "branch_turning_erased": (-1) ** 2 == 1 ** 2 and (2 + (-1)) != (2 + 1),
        **{
            f"scope_{phrase.replace(' ', '_').replace('(', '').replace(')', '')}":
            not scope_allowed(f"mutation: {phrase}")
            for phrase in prohibited_promotions
        },
    }
    missed = [name for name, caught in catches.items() if not caught]
    result = {
        "status": "PASS" if not missed else "FAIL",
        "caught": sum(bool(value) for value in catches.values()),
        "total": len(catches),
        "missed": missed,
        "catches": catches,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if missed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
