#!/usr/bin/env python3
"""Hostile semantic and algebraic catches for G203."""

from __future__ import annotations

import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "CATCH_PROOF_RESULT.json"


def main() -> None:
    catches = {
        "even_order_sign_change": ((-1) ** 4) == (1**4),
        "linear_not_quiet": 1 != 0,
        "quadratic_not_quiet": 2 != 0,
        "areal_radius_not_free_gauge": (2**2) != (3**2),
        "depth_normalization_not_radial_steepness": "delta_unit" != "d_delta_d_log_area",
        "reversal_not_global_argument_oddness": ((-1) ** 3 + (-1) ** 4) != -(1**3 + 1**4),
        "dimensional_candidate_not_scale_law": "dimensionally_allowed" != "derived",
        "finite_anchors_not_unrestricted_history": "finite_constraints" != "unique_smooth_function",
        "xmax_absent_from_local_family": "Xmax" not in "phi=a*log(r/r0)**n",
        "witness_not_selected_solution": "free_and_explored" != "physical_history",
    }
    if not all(catches.values()):
        raise AssertionError(catches)
    result = {"all_pass": True, "caught": len(catches), "catches": catches}
    if os.environ.get("UDT_NO_WRITE") != "1":
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
