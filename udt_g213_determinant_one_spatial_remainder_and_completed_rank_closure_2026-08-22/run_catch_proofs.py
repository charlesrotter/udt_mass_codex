#!/usr/bin/env python3
"""Hostile algebraic and semantic catches for G213; writes no files."""

import json
from pathlib import Path
import subprocess
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parent
catches = {}


def catch(name, condition):
    value = bool(condition)
    catches[name] = value
    if not value:
        raise AssertionError(name)


gamma, w1, w2, s1, s2 = sp.symbols("gamma w1 w2 s1 s2")
coordinates = sp.Matrix([2*gamma, w1, w2, -gamma+s1, s2])
J = coordinates.jacobian([gamma, w1, w2, s1, s2])
catch("full_five_modes_rank_five", J.rank() == 5)
catch("deleting_grading_loses_rank", J[:, 1:].rank() == 4)
catch("deleting_one_mixer_loses_another_rank", J[:, [0, 2, 3, 4]].rank() == 4)
catch("deleting_one_screen_shape_loses_another_rank", J[:, [0, 1, 2, 3]].rank() == 4)

bad_grade = sp.diag(gamma, -gamma, -gamma)
catch("wrong_grading_trace_is_caught", sp.trace(bad_grade) != 0)
bad_screen = sp.diag(0, s1, s1)
catch("screen_trace_mode_is_not_determinant_one", sp.trace(bad_screen) != 0)
catch("good_grade_tracefree", sp.trace(sp.diag(2*gamma, -gamma, -gamma)) == 0)
catch("good_screen_tracefree", sp.trace(sp.diag(0, s1, -s1)) == 0)

T, L, beta, k = sp.symbols("T L beta k", positive=True)
h = sp.Matrix([[-T**2, -T**2*beta], [-T**2*beta, L**2-T**2*beta**2]])
m = T*L
good = sp.diag(1, m).inv().T * h * sp.diag(1, m).inv()
bad = sp.diag(1, k*m).inv().T * h * sp.diag(1, k*m).inv()
catch("good_density_gives_det_minus_one", sp.simplify(good.det() + 1) == 0)
catch("wrong_density_factor_is_caught", sp.simplify(bad.det() + 1) != 0)
catch("wrong_density_has_expected_error", sp.simplify(bad.det() + k**-2) == 0)
catch("good_roundtrip", sp.simplify(sp.diag(1, m).T * good * sp.diag(1, m) - h) == sp.zeros(2))
catch("wrong_jacobian_power_is_caught", sp.simplify(sp.diag(1, m**2).T * good * sp.diag(1, m**2) - h) != sp.zeros(2))

aa, bb, mm, lam = sp.symbols("aa bb mm lam", nonzero=True)
cc = (bb**2-mm**2)/aa
hs = sp.diag(1, mm).inv().T * sp.Matrix([[aa, bb], [bb, cc]]) * sp.diag(1, mm).inv()
hs_scaled = sp.diag(1, lam*mm).inv().T * sp.Matrix([[aa, lam*bb], [lam*bb, lam**2*cc]]) * sp.diag(1, lam*mm).inv()
catch("density_deletion_blind_family_survives", sp.simplify(hs_scaled-hs) == sp.zeros(2))
catch("blind_family_metrics_are_distinct", sp.simplify(lam*bb-bb) != 0)

directions_full = [(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1)]
directions_axial = directions_full[:3]


def design(directions):
    rows = []
    for x,y,z in directions:
        rows.extend([
            [1,0,0,0,0,0,0,0,0,0],
            [0,x,y,z,0,0,0,0,0,0],
            [0,0,0,0,x*x,2*x*y,2*x*z,y*y,2*y*z,z*z],
        ])
    return sp.Matrix(rows)


catch("full_design_rank_ten", design(directions_full).rank() == 10)
catch("axial_only_rank_seven", design(directions_axial).rank() == 7)
catch("remove_one_sum_plane_loses_rank", design(directions_full[:-1]).rank() < 10)

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
catch("independent_has_ten_thousand_cases", independent["cases"] == 10_000)
catch("independent_design_rank_ten", independent["g129_design_rank"] == 10)
catch("independent_blind_metrics_distinct", independent["changed_density_blind_metrics"] == 10_000)

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
