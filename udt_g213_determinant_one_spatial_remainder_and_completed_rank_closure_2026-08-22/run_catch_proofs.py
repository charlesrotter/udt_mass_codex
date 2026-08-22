#!/usr/bin/env python3
"""Dependency-free hostile algebraic and semantic catches for G213; writes no files."""

from fractions import Fraction as F
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
catches = {}


def catch(name, condition):
    value = bool(condition)
    catches[name] = value
    if not value:
        raise AssertionError(name)


def rank(matrix):
    work = [[F(value) for value in row] for row in matrix]
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        lead = work[pivot_row][column]
        work[pivot_row] = [value / lead for value in work[pivot_row]]
        for row in range(len(work)):
            if row != pivot_row and work[row][column]:
                factor = work[row][column]
                work[row] = [left - factor * right for left, right in zip(work[row], work[pivot_row])]
        pivot_row += 1
    return pivot_row


mode_map = [
    [2, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [-1, 0, 0, 1, 0],
    [0, 0, 0, 0, 1],
]
catch("full_five_modes_rank_five", rank(mode_map) == 5)
catch("deleting_grading_loses_rank", rank([row[1:] for row in mode_map]) == 4)
catch("deleting_one_mixer_loses_another_rank", rank([[row[i] for i in [0, 2, 3, 4]] for row in mode_map]) == 4)
catch("deleting_one_screen_shape_loses_another_rank", rank([[row[i] for i in [0, 1, 2, 3]] for row in mode_map]) == 4)

catch("wrong_grading_trace_is_caught", 1 - 1 - 1 != 0)
catch("screen_trace_mode_is_not_determinant_one", 0 + 1 + 1 != 0)
catch("good_grade_tracefree", 2 - 1 - 1 == 0)
catch("good_screen_tracefree", 0 + 1 - 1 == 0)

T, length, beta, scale = F(2), F(3), F(1, 5), F(2)
h00 = -T**2
h01 = -T**2 * beta
h11 = length**2 - T**2 * beta**2
m = T * length
good = (h00, h01 / m, h11 / m**2)
bad = (h00, h01 / (scale * m), h11 / (scale * m) ** 2)
catch("good_density_gives_det_minus_one", good[0] * good[2] - good[1] ** 2 == -1)
catch("wrong_density_factor_is_caught", bad[0] * bad[2] - bad[1] ** 2 != -1)
catch("wrong_density_has_expected_error", bad[0] * bad[2] - bad[1] ** 2 == -scale**-2)
catch("good_roundtrip", (good[0], m * good[1], m**2 * good[2]) == (h00, h01, h11))
catch("wrong_jacobian_power_is_caught", (good[0], m**2 * good[1], m**4 * good[2]) != (h00, h01, h11))

aa, bb, mm, lam = F(-1), F(1, 3), F(4, 3), F(3, 2)
cc = (bb**2 - mm**2) / aa
completed = (aa, bb / mm, cc / mm**2)
completed_scaled = (aa, lam * bb / (lam * mm), lam**2 * cc / (lam * mm) ** 2)
catch("density_deletion_blind_family_survives", completed_scaled == completed)
catch("blind_family_metrics_are_distinct", lam * bb != bb or lam**2 * cc != cc)

directions_full = [(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1)]
directions_axial = directions_full[:3]


def design(directions):
    rows = []
    for x, y, z in directions:
        rows.extend([
            [1,0,0,0,0,0,0,0,0,0],
            [0,x,y,z,0,0,0,0,0,0],
            [0,0,0,0,x*x,2*x*y,2*x*z,y*y,2*y*z,z*z],
        ])
    return rows


catch("full_design_rank_ten", rank(design(directions_full)) == 10)
catch("axial_only_rank_seven", rank(design(directions_axial)) == 7)
catch("remove_one_sum_plane_loses_rank", rank(design(directions_full[:-1])) < 10)

production = json.loads(subprocess.run(
    [sys.executable, "-B", str(ROOT / "derive_spatial_remainder_and_rank.py")],
    check=True, capture_output=True, text=True,
).stdout)
independent = json.loads(subprocess.run(
    [sys.executable, "-B", str(ROOT / "verify_completed_rank_independent.py")],
    check=True, capture_output=True, text=True,
).stdout)
catch("production_landing_is_bounded", production["maximum_conclusion"] == "local_metric_decomposition_and_rank_reconstruction_only")
catch("production_reports_prior_rank_four", production["prior_tile_tangent_coverage"]["union"] == 4)
catch("production_is_dependency_free", production["method"].startswith("stdlib_fraction"))
catch("independent_has_ten_thousand_cases", independent["cases"] == 10_000)
catch("independent_design_rank_ten", independent["g129_design_rank"] == 10)
catch("independent_blind_metrics_distinct", independent["changed_density_blind_metrics"] == 10_000)
catch("independent_mode_rank_five", independent["mode_census_rank"] == 5)
catch("independent_prior_union_rank_four", independent["g207_g208_union_rank"] == 4)
catch("independent_grading_completion_rank_five", independent["grading_completion_rank"] == 5)

exact_text = (ROOT / "EXACT_DERIVATION.md").read_text()
report_text = (ROOT / "AUDIT_REPORT.md").read_text()
catch("exact_denies_value_generation", "does not generate the values" in exact_text)
catch("report_denies_physical_population", "no global pair population" in report_text)
catch("working_clarification_retained", "G176 working clarification" in exact_text)
catch("known_germ_premise_retained", "known pair germs" in exact_text)
catch("xmax_not_imported", "No source, action, `X_max`" in exact_text)

print(json.dumps({
    "audit": "G213",
    "status": "PASS",
    "catches": len(catches),
    "all_catches_pass": all(catches.values()),
    "checks": catches,
}, sort_keys=True))
