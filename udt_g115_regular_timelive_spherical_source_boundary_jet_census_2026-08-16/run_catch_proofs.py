#!/usr/bin/env python3
"""Hostile mutations for the G115 load-bearing claims."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
TOL = 3.0e-3


def relative(observed: float, expected: float) -> float:
    return abs(observed - expected) / max(1.0e-12, abs(expected))


def main() -> None:
    evidence = json.loads((HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text())
    obs = evidence["observed_coefficients"]
    w = evidence["witness"]

    correct_phi = evidence["expected_coefficients"]["phi_R2"]
    omit_time_live = correct_phi + w["b_T"] / 4.0
    omit_celestial_drift = correct_phi - 0.5 * (w["w"][0] ** 2 + w["w"][1] ** 2)
    omit_source_motion = w["b"]

    catches = {
        "omitting_b_T_from_phi_is_rejected": relative(obs["phi_R2"], omit_time_live) > TOL,
        "omitting_celestial_drift_from_fixed_label_phi_is_rejected": relative(
            obs["phi_R2"], omit_celestial_drift
        )
        > TOL,
        "identifying_source_frequency_with_quadratic_phi_is_rejected": abs(
            obs["logfreq_R1"]
        )
        > 0.1,
        "omitting_source_congruence_from_frequency_is_rejected": relative(
            obs["logfreq_R1"], omit_source_motion
        )
        > TOL,
        "rank_one_is_not_rank_two": evidence["intersection_ranks"]["graph_rank_1"] == 1,
        "position_caustic_does_not_delete_phase": (
            evidence["intersection_ranks"]["point_vertical_caustic"] == 2
            and evidence["checks"]["caustic_phase_invertible"]
        ),
    }
    result = {
        "status": "PASS" if all(catches.values()) else "FAIL",
        "mutations": catches,
        "mutant_predictions": {
            "phi_without_b_T": omit_time_live,
            "phi_without_celestial_drift": omit_celestial_drift,
            "frequency_without_source_motion_linear": omit_source_motion,
            "frequency_as_terminal_phi_linear": 0.0,
        },
    }
    (HERE / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
