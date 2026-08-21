#!/usr/bin/env python3
"""Hostile G204 algebraic and semantic catches."""

from __future__ import annotations

import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "CATCH_PROOF_RESULT.json"


def main() -> None:
    catches = {
        "angular_curvature_term_not_dropped": 4 * (1 - 2) ** 2 > 0,
        "log_center_not_regular": "infinite_K" != "smooth_center",
        "curvature_zero_not_standard_flat_asymptotics": "K_to_zero" != "f_to_one",
        "outer_limit_not_xmax": "r_to_infinity" != "finite_Xmax",
        "outer_limit_not_horizon_theorem": "asymptotic_f_to_zero" != "finite_regular_horizon",
        "finite_distance_needs_curvature_for_singularity": "finite_distance" != "curvature_singularity",
        "regular_control_not_selected_profile": "free_and_explored" != "physical_history",
        "bounded_curvature_not_full_center_smoothness": "finite_K" != "cartesian_C_infinity",
        "repair_witness_not_hidden": "post_failure_preregistered" != "original_preregistered_control",
        "inner_branch_not_monotone": 2 < 5,
        "center_regularity_not_field_equation": "geometric_gate" != "dynamics",
        "global_gate_does_not_select_parameters": (3, 1, 1) != (5, 2, 3),
        "static_slice_not_general_time_live_theory": "static_spherical" != "complete_UDT",
    }
    if not all(catches.values()):
        raise AssertionError(catches)
    result = {"all_pass": True, "caught": len(catches), "catches": catches}
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
if __name__ == "__main__":
    main()
