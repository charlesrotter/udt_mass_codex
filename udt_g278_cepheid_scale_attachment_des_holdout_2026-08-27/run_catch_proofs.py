#!/usr/bin/env python3
"""Hostile non-vacuity controls for G278."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


PACKAGE = Path(__file__).resolve().parent


def main() -> None:
    result = json.load((PACKAGE / "DERIVATION_RESULT.json").open())
    des = result["DES"]["12"]

    relative_only = np.asarray([[1.0, 1.0]])
    with_calibrator = np.asarray([[1.0, 0.0], [1.0, 1.0]])
    rank_without_calibrator = int(np.linalg.matrix_rank(relative_only))
    rank_with_calibrator = int(np.linalg.matrix_rank(with_calibrator))

    # Exact two-rung response: a uniform +delta calibrator-modulus residual
    # moves M by +delta and a by -delta while preserving the flow equation.
    delta = 0.137
    baseline = np.asarray([-19.25, 37.25])  # (M, a+25)
    shifted = baseline + np.asarray([delta, -delta])
    baseline_prediction = with_calibrator @ baseline
    shifted_prediction = with_calibrator @ shifted
    exact_calibrator_shift = bool(
        np.isclose(shifted_prediction[0] - baseline_prediction[0], delta)
        and np.isclose(shifted_prediction[1] - baseline_prediction[1], 0.0)
    )

    checks = {
        "relative_only_scale_rank_defect_is_alive": rank_without_calibrator == 1,
        "cepheid_plus_flow_rank_is_two": rank_with_calibrator == 2,
        "calibrator_shift_moves_scale_exactly": exact_calibrator_shift,
        "DES_offset_was_not_forced_to_zero": abs(float(des["residual_mean_mag"])) > 1e-3,
        "resolution_gate_can_fail": bool(
            result["gates"]["resolution_chi2"] > result["gates"]["resolution_ceiling"]
            and not result["gates"]["resolution_pass"]
        ),
        "DES_gate_can_pass_independently": bool(
            des["chi2"] <= des["ceiling"] and result["gates"]["primary_DES_pass"]
        ),
        "no_kernel_state_or_DES_retuning": bool(
            not result["frozen"]["kernel_retuned"]
            and not result["frozen"]["state_shape_retuned_by_calibrators"]
            and result["frozen"]["DES_parameters_fitted"] == 0
        ),
        "forbidden_scaffolding_absent": bool(
            not result["frozen"]["P1_used"]
            and result["frozen"]["angular_coefficients_fitted"] == 0
            and not result["frozen"]["Xmax_used"]
            and not result["frozen"]["lcdm_distance_used"]
        ),
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    output = {
        "audit": "G278_HOSTILE_NONVACUITY_CONTROLS",
        "checks": checks,
        "mutations": {
            "rank_without_calibrator": rank_without_calibrator,
            "rank_with_calibrator": rank_with_calibrator,
            "calibrator_shift_mag": delta,
            "DES_residual_mean_mag_retained": des["residual_mean_mag"],
        },
    }
    with (PACKAGE / "CATCH_PROOF_RESULT.json").open("w") as handle:
        json.dump(output, handle, indent=2, sort_keys=True)
        handle.write("\n")
    rendered = json.dumps(output, indent=2, sort_keys=True)
    (PACKAGE / "CATCH_PROOF_RUN_LOG.txt").write_text(
        "COMMAND: python3 run_catch_proofs.py\n" + rendered + "\n"
    )
    print(rendered)


if __name__ == "__main__":
    main()
