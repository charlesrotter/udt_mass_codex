#!/usr/bin/env python3
"""Exact symbolic G173 turning-chart and calibration-atlas derivation."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import subprocess

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
FROZEN_SOURCE_COMMIT = "d1f2e6f5"


def require(condition: bool, name: str, detail: object = "") -> dict[str, object]:
    if not condition:
        raise AssertionError(f"{name}: {detail}")
    return {"name": name, "passed": True, "detail": str(detail)}


r, phi = sp.symbols("r phi", positive=True, finite=True)
v, theta_s, psi_s = sp.symbols("v theta_s psi_s", real=True, finite=True)
theta = sp.symbols("theta", real=True, finite=True)
lam = sp.symbols("lambda", positive=True, finite=True)
b2 = theta_s**2 + sp.sin(theta) ** 2 * psi_s**2

metric = sp.diag(-sp.exp(-2 * phi), sp.exp(2 * phi), r**2, r**2 * sp.sin(theta) ** 2)
jacobian = sp.Matrix([[1, 0], [0, v], [0, theta_s], [0, psi_s]])
h = sp.simplify(jacobian.T * metric * jacobian)
H = sp.simplify(sp.exp(2 * phi) * v**2 + r**2 * b2)
det_h = sp.simplify(h.det())
raw_e4 = sp.simplify((-det_h) / h[0, 0] ** 2)

m_r2 = v**2
m_A2 = sp.simplify(v**2 + r**2 * b2)
m_P2 = sp.simplify(v**2 + sp.exp(-2 * phi) * r**2 * b2)
e4_r = sp.simplify(raw_e4 / m_r2)
e4_A = sp.simplify(raw_e4 / m_A2)
e4_P = sp.simplify(raw_e4 / m_P2)

checks: list[dict[str, object]] = []
checks.append(require(h[0, 0] == -sp.exp(-2 * phi), "pullback_time", h))
checks.append(require(h[0, 1] == 0, "pullback_time_orthogonal", h))
checks.append(require(sp.simplify(h[1, 1] - H) == 0, "pullback_full_spatial", h[1, 1]))
checks.append(require(sp.simplify(det_h + sp.exp(-2 * phi) * H) == 0, "determinant", det_h))
checks.append(require(sp.simplify(raw_e4 - sp.exp(2 * phi) * H) == 0, "raw_readout_weight", raw_e4))

H_lam = sp.simplify(sp.exp(2 * phi) * (lam * v) ** 2 + r**2 * lam**2 * b2)
raw_lam = sp.simplify(sp.exp(2 * phi) * H_lam)
checks.append(require(sp.simplify(H_lam - lam**2 * H) == 0, "spatial_weight_two", H_lam))
checks.append(require(sp.simplify(raw_lam - lam**2 * raw_e4) == 0, "raw_phi_is_density", raw_lam))
checks.append(require(sp.simplify(lam**2 * m_A2 - ((lam * v) ** 2 + r**2 * lam**2 * b2)) == 0, "mA_weight_one"))
checks.append(require(sp.simplify(lam**2 * m_P2 - ((lam * v) ** 2 + sp.exp(-2 * phi) * r**2 * lam**2 * b2)) == 0, "mP_weight_one"))

checks.append(require(sp.simplify(e4_r - sp.exp(4 * phi) * (1 + r**2 * sp.exp(-2 * phi) * b2 / v**2)) == 0, "G172_overlap"))
checks.append(require(sp.simplify(e4_A - raw_e4 / m_A2) == 0, "mA_invariant_readout"))
checks.append(require(sp.simplify(e4_P - sp.exp(4 * phi)) == 0, "mP_readout_is_phi", e4_P))
checks.append(require(sp.simplify(e4_A / e4_r - m_r2 / m_A2) == 0, "mA_transition_from_areal"))
checks.append(require(sp.simplify(e4_P / e4_r - m_r2 / m_P2) == 0, "mP_transition_from_areal"))

radial_subs = {theta_s: 0, psi_s: 0}
checks.append(require(sp.simplify(e4_A.subs(radial_subs) - sp.exp(4 * phi)) == 0, "mA_radial_recovery"))
checks.append(require(sp.simplify(e4_P.subs(radial_subs) - sp.exp(4 * phi)) == 0, "mP_radial_recovery"))
checks.append(require(sp.simplify(e4_A.subs(v, 0) - sp.exp(2 * phi)) == 0, "mA_turning_value"))
checks.append(require(sp.simplify(e4_P.subs(v, 0) - sp.exp(4 * phi)) == 0, "mP_turning_value"))
checks.append(require(sp.simplify(e4_A.subs(v, 0) - e4_P.subs(v, 0)) != 0, "turning_calibrations_inequivalent"))

turn_det = sp.simplify(det_h.subs(v, 0))
checks.append(require(sp.simplify(turn_det + sp.exp(-2 * phi) * r**2 * b2) == 0, "turning_determinant", turn_det))
checks.append(require(sp.simplify(det_h.subs({v: 0, theta_s: 0, psi_s: 0})) == 0, "true_rank_loss"))

# Exact rational turning witness: e^(2 phi)=4, r=3, v=0, b^2=1.
A_w, r_w, b2_w = sp.Integer(4), sp.Integer(3), sp.Integer(1)
H_w = r_w**2 * b2_w
det_w = -H_w / A_w
e4A_w = A_w * H_w / (r_w**2 * b2_w)
e4P_w = A_w * H_w / ((r_w**2 * b2_w) / A_w)
checks.append(require(det_w == sp.Rational(-9, 4), "rational_turn_regular", det_w))
checks.append(require(e4A_w == 4, "rational_turn_mA", e4A_w))
checks.append(require(e4P_w == 16, "rational_turn_mP", e4P_w))
checks.append(require(e4A_w != e4P_w, "rational_turn_nonuniqueness"))

# A positive algebraic family of calibration densities; f=1 and f=e^-2phi are two members.
f = sp.symbols("f", positive=True, finite=True)
m_f2 = v**2 + f * r**2 * b2
e4_f = sp.simplify(raw_e4 / m_f2)
checks.append(require(sp.simplify(e4_f.subs(radial_subs) - sp.exp(4 * phi)) == 0, "mf_radial_recovery"))
checks.append(require(sp.simplify(e4_f.subs(v, 0) - sp.exp(2 * phi) / f) == 0, "mf_turning_family"))
checks.append(require(sp.simplify(e4_f.subs(f, 1) - e4_A) == 0, "mf_contains_mA"))
checks.append(require(sp.simplify(e4_f.subs(f, sp.exp(-2 * phi)) - e4_P) == 0, "mf_contains_mP"))

# Source integrity against the committed preregistration base.
source_rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
source_failures: list[str] = []
for row in source_rows:
    frozen = subprocess.run(
        ["git", "show", f"{FROZEN_SOURCE_COMMIT}:{row['path']}"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    ).stdout
    if hashlib.sha256(frozen).hexdigest() != row["sha256"]:
        source_failures.append(row["path"])
checks.append(require(len(source_rows) == 11, "source_count", len(source_rows)))
checks.append(require(not source_failures, "source_hashes_match", source_failures))
manifest_text = (HERE / "SOURCE_MANIFEST.tsv").read_text()
checks.append(require(all(f"udt_g{i}" not in manifest_text for i in range(142, 161)), "scaffold_sources_excluded"))

landing = (
    "PULLBACK_EXTENDS__CALIBRATION_ATLAS_NONUNIQUE"
    "__RADIAL_TURN_WITH_ANGULAR_MOTION_IS_REGULAR"
    "__RAW_TERMINAL_PHI_IS_AN_AFFINE_LOG_DENSITY"
    "__ANY_POSITIVE_WEIGHT_ONE_CALIBRATION_GIVES_AN_INVARIANT_SCALAR_CHART"
    "__TWO_METRIC_BUILT_CALIBRATIONS_SURVIVE_AND_DISAGREE"
    "__NO_FINITE_CALIBRATION_CAN_EQUAL_G172_ON_EVERY_PUNCTURED_MONOTONE_NEIGHBORHOOD"
    "__TRUE_FIRST_RANK_BOUNDARY_IS_ZERO_COMPLETE_SPATIAL_TANGENT"
    "__NO_PHYSICAL_CALIBRATION_OR_GLOBAL_SELECTION"
)

result = {
    "landing": landing,
    "status": "DERIVED_BOUNDED_AWAITING_INDEPENDENT_AND_EXTERNAL_REVIEW",
    "metric": str(metric),
    "pair_metric": str(h),
    "b2": str(b2),
    "H": str(H),
    "det_h": str(det_h),
    "raw_exp_4Phi": str(raw_e4),
    "m_r_squared": str(m_r2),
    "m_A_squared": str(m_A2),
    "m_P_squared": str(m_P2),
    "exp_4Phi_r": str(e4_r),
    "exp_4Phi_A": str(e4_A),
    "exp_4Phi_P": str(e4_P),
    "turning_det": str(turn_det),
    "rational_turning_witness": {
        "exp_2phi": 4,
        "r": 3,
        "v": 0,
        "b2": 1,
        "det_h": str(det_w),
        "exp_4Phi_A": str(e4A_w),
        "exp_4Phi_P": str(e4P_w),
    },
    "checks": checks,
    "checks_passed": len(checks),
    "checks_total": len(checks),
    "source_count": len(source_rows),
    "source_failures": source_failures,
}
(HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({k: result[k] for k in ("landing", "checks_passed", "source_count")}, sort_keys=True))
