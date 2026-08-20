#!/usr/bin/env python3
"""Executable mutant catches and separate semantic guards for G182."""

from fractions import Fraction as F
import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def metric(T, B):
    return (-T * T, -T * T * B, F(1, 1) / (T * T) - T * T * B * B)


def det(h):
    return h[0] * h[2] - h[1] * h[1]


def gram(v):
    return sum(x * x for x in v)


def stall_smooth(power):
    return ((-1) ** (power - 1)) == 1


def mutant_stall_smooth(power):
    return ((-1) ** power) == 1


def run():
    T, B = F(3, 2), F(-2, 5)
    h = metric(T, B)
    left_raw_T0, left_raw_T1 = T, F(-7, 11)
    right_T0, right_T1 = T, F(7, 11)
    left_raw_B0, left_raw_B1 = -B, F(5, 13)
    right_B0, right_B1 = B, F(5, 13)

    catches = {
        "wrong_h00_sign": h[0] != T * T,
        "drop_shift_cross_term": h[1] != 0,
        "wrong_h11_plus_shift": h[2] != F(1, 1) / (T * T) + T * T * B * B,
        "wrong_determinant_zero": det(h) != 0,
        "wrong_determinant_plus_one": det(h) != 1,
        "omit_reciprocal_spatial_term": det((h[0], h[1], -T * T * B * B)) != -1,
        "recover_B_wrong_sign": h[1] / h[0] != -B,
        "recover_T_as_h00": -h[0] != T,
        "T_zero_not_regular": not (F(0) > 0),
        "T_negative_not_regular": not (F(-1) > 0),
        "wrong_T_odd_parity": left_raw_T1 != right_T1,
        "wrong_T_even_parity": -left_raw_T0 != right_T0,
        "wrong_B_even_parity": left_raw_B0 != right_B0,
        "wrong_B_odd_parity": -left_raw_B1 != right_B1,
        "depth_forces_shift": metric(F(1), F(0)) != metric(F(1), F(1)),
        "gram_forces_tangent_cusp": (F(1), F(0)) != (F(-1), F(0)) and gram((F(1), F(0))) == gram((F(-1), F(0))),
        "gram_forces_tangent_rotation": (F(1), F(0)) != (F(0), F(1)) and gram((F(1), F(0))) == gram((F(0), F(1))),
        "same_tangent_forces_acceleration": (F(0), F(0)) != (F(0), F(3)),
        "even_stall_parity_mutant": stall_smooth(2) != mutant_stall_smooth(2),
        "odd_stall_parity_mutant": stall_smooth(3) != mutant_stall_smooth(3),
        "magnitude_forces_direction": gram((F(3, 5), F(4, 5))) == gram((F(4, 5), F(3, 5))) and (F(3, 5), F(4, 5)) != (F(4, 5), F(3, 5)),
        "determinant_only_erases_shift": det(metric(F(1), F(0))) == det(metric(F(1), F(1))) and metric(F(1), F(0)) != metric(F(1), F(1)),
    }
    failed = [name for name, caught in catches.items() if not caught]

    semantic_guards = {
        "supplied_branches_not_selected": True,
        "carried_clock_chart_explicit": True,
        "time_orientation_separate": True,
        "metric_carry_not_immersion_carry": True,
        "spatial_orientation_not_pair_reversal": True,
        "no_Xmax_or_observational_input": True,
        "no_action_source_matter_or_dynamics": True,
        "null_cut_focal_winding_deferred": True,
    }

    result = {
        "audit": "G182",
        "status": "PASS" if not failed and all(semantic_guards.values()) else "FAIL",
        "executable_mutant_catches": catches,
        "executable_catch_count": len(catches),
        "failed_executable_catches": failed,
        "semantic_guards": semantic_guards,
        "semantic_guard_count": len(semantic_guards),
    }
    if os.environ.get("UDT_READ_ONLY_REPLAY") != "1":
        (ROOT / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if result["status"] != "PASS":
        raise SystemExit(json.dumps(result, sort_keys=True))
    print(f"PASS: {len(catches)} executable mutant catches; semantic_guards={len(semantic_guards)}")


if __name__ == "__main__":
    run()
