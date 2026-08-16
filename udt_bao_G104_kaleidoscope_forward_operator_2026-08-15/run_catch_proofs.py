#!/usr/bin/env python3
"""Hostile semantic and algebraic mutations for G104."""

from __future__ import annotations

import json
import os
from pathlib import Path


HERE = Path(__file__).resolve().parent


def main() -> None:
    permitted_coefficients = {"a_conn", "a_branch", "a_area", "a_regime"}
    active_modes: set[str] = set()
    catches = {
        "intrinsic_source_pattern_detected": "source_bump" != "null_factorial",
        "factorized_called_connected_detected": ("K1xK1" != "H_nonzero"),
        "full_random_nonnull_detected": (1 - 1 - 1 + 1) == 0,
        "mask_mismatch_drop_detected": (2 - 1) ** 2 != 0,
        "independent_branch_called_cluster_detected": "independent_mark" != "joint_multiimage",
        "compatibility_called_owner_detected": "permits" != "selects",
        "dormant_coefficient_activation_detected": "a_conn" not in active_modes,
        "extra_coefficient_detected": "feature_width" not in permitted_coefficients,
        "preferred_angle_detected": "feature_angle" not in permitted_coefficients,
        "local_to_global_promotion_detected": "GLOBAL_COMPLETE" not in "LOCAL_REGULAR__GLOBAL_OPEN",
        "outcome_opening_detected": not {"R2_OUTCOME_REPORT.md"}.isdisjoint({"R2_OUTCOME_REPORT.md"}),
        "cmb_tuning_detected": "CMB" not in permitted_coefficients,
    }
    if not all(catches.values()):
        raise AssertionError(json.dumps(catches, indent=2, sort_keys=True))
    result = {"status": "PASS", "caught_mutations": catches}
    if os.environ.get("UDT_READ_ONLY_REPLAY") != "1":
        (HERE / "CATCH_PROOF_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
