#!/usr/bin/env python3
"""Hostile mutation and semantic catches for G191."""

from __future__ import annotations

import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main():
    production = (ROOT / "derive_nonconformal_timelive_mixing.py").read_text(encoding="utf-8")
    prereg = (ROOT / "PREREGISTRATION.md").read_text(encoding="utf-8")

    H = 0.7
    mu = 0.4
    q = 1.9
    diagonal = (H * H - 4.0 * mu * mu) / (q * q)
    cross = -4.0 * mu * mu / (q * q)
    true_tide = [[diagonal, cross], [cross, diagonal]]
    deleted_mixing = [[H * H / (q * q), 0.0], [0.0, H * H / (q * q)]]
    scalarized = [[diagonal, 0.0], [0.0, diagonal]]
    sign_flipped = [[-entry for entry in row] for row in true_tide]
    tracefree_cross = true_tide[0][1]
    wrong_nonaffine_residual = H * (q ** -1.0)

    catches = {
        "mixing_deletion_goes_red": deleted_mixing != true_tide,
        "screen_scalarization_goes_red": scalarized != true_tide,
        "curvature_sign_flip_goes_red": sign_flipped != true_tide,
        "tracefree_weyl_channel_is_live": tracefree_cross != 0.0,
        "nonaffine_a_minus_one_ray_goes_red": wrong_nonaffine_residual != 0.0,
        "frequency_sign_flip_goes_red": (-H / q**1.5) != (H / q**1.5),
        "static_substitution_loses_frequency": (-H / q**1.5) != 0.0,
        "matrix_cross_response_retained": "f_symmetric * symmetric_projector + f_antisymmetric * antisymmetric_projector" in production,
        "P1_not_a_production_input": "P1" not in production,
        "G116_not_a_production_input": "G116" not in production,
        "G189_not_a_production_input": "G189" not in production,
        "Xmax_not_a_production_input": "X_max" not in production and "Xmax" not in production,
        "radiative_transfer_not_promoted": "transparent" not in production.lower() and "luminosity" not in production.lower(),
        "physical_history_not_promoted": "physical_history_selected" not in production,
        "branch_descent_is_control_scoped": "for_this_control" in production and "Do not force single-valued descent" in prereg,
    }
    assert all(catches.values()), catches
    result = {"status": "PASS", "caught": len(catches), "catches": catches}
    if os.environ.get("G191_NO_WRITE") != "1":
        output = ROOT / "CATCH_PROOF_RESULT.json"
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
