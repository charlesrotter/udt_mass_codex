#!/usr/bin/env python3
"""Exact symbolic G174 calibrated-pair-germ ownership derivation."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import subprocess

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
FROZEN_SOURCE_COMMIT = "9e40a840"


def require(condition: bool, name: str, detail: object = "") -> dict[str, object]:
    if not condition:
        raise AssertionError(f"{name}: {detail}")
    return {"name": name, "passed": True, "detail": str(detail)}


A, r, v, b2, m = sp.symbols("A r v b2 m", positive=True, finite=True)
lam, c, m1, m2, n1, n2 = sp.symbols(
    "lambda c m1 m2 n1 n2", positive=True, finite=True
)
vr, va = sp.symbols("vr va", real=True, finite=True)

# A=exp(2 phi). The angular speed b2 is nonnegative in the geometric domain; using a
# positive symbol keeps the symbolic turning stratum regular. Pure-radial controls are
# substituted separately.
H = sp.simplify(A * v**2 + r**2 * b2)
h_sigma = sp.diag(-1 / A, H)
change_to_calibrated = sp.diag(1, 1 / m)
h_s = sp.simplify(change_to_calibrated.T * h_sigma * change_to_calibrated)
e4_phi_m = sp.simplify((-h_s.det()) / h_s[0, 0] ** 2)

checks: list[dict[str, object]] = []
checks.append(require(h_s[0, 0] == -1 / A, "calibrated_clock_entry", h_s))
checks.append(require(h_s[0, 1] == 0, "calibrated_time_orthogonal", h_s))
checks.append(require(sp.simplify(h_s[1, 1] - H / m**2) == 0, "calibrated_ruler_entry", h_s))
checks.append(require(sp.simplify(h_s.det() + H / (A * m**2)) == 0, "calibrated_determinant"))
checks.append(require(sp.simplify(e4_phi_m - A * H / m**2) == 0, "G173_Phi_m_recovered"))

# Auxiliary reparameterization: S_tilde=lambda S and m_tilde=lambda m. The physical
# ruler coordinate ds and calibrated tangent S/m are unchanged.
H_tilde = sp.simplify(A * (lam * v) ** 2 + r**2 * lam**2 * b2)
m_tilde = lam * m
e4_tilde = sp.simplify(A * H_tilde / m_tilde**2)
checks.append(require(sp.simplify(H_tilde - lam**2 * H) == 0, "auxiliary_tangent_weight"))
checks.append(require(sp.simplify(e4_tilde - e4_phi_m) == 0, "calibrated_scalar_reparam_invariant"))
checks.append(require(sp.simplify(lam * v / m_tilde - v / m) == 0, "radial_tangent_invariant"))
checks.append(require(sp.simplify(lam**2 * b2 / m_tilde**2 - b2 / m**2) == 0, "angular_speed_invariant"))

# Fixed calibrated vector uniqueness: if S=m R=n R and one component of R is nonzero,
# subtraction forces m=n. The two component displays cover radial and angular turns.
checks.append(require(sp.solve(sp.Eq(m * vr, n1 * vr), n1) == [m], "density_unique_radial_component"))
checks.append(require(sp.solve(sp.Eq(m * va, n1 * va), n1) == [m], "density_unique_angular_component"))

# G173 registered candidates. They define different calibrated vectors whenever their
# positive densities differ.
mA2 = sp.simplify(v**2 + r**2 * b2)
mP2 = sp.simplify(v**2 + r**2 * b2 / A)
e4_A = sp.simplify(A * H / mA2)
e4_P = sp.simplify(A * H / mP2)
checks.append(require(sp.simplify(e4_P - A**2) == 0, "mP_readout"))
checks.append(require(sp.simplify(e4_A.subs(v, 0) - A) == 0, "mA_turning_readout"))
checks.append(require(sp.simplify(e4_P.subs(v, 0) - A**2) == 0, "mP_turning_readout"))
checks.append(require(sp.simplify(mP2.subs(v, 0) - mA2.subs(v, 0) / A) == 0, "turning_density_ratio"))
checks.append(require(sp.simplify(mA2 - mP2) != 0, "candidate_calibrations_generic_difference"))

# Pure-radial overlap: both candidates reduce to the areal density |v|.
checks.append(require(sp.simplify(mA2.subs(b2, 0) - v**2) == 0, "mA_radial_density"))
checks.append(require(sp.simplify(mP2.subs(b2, 0) - v**2) == 0, "mP_radial_density"))
checks.append(require(sp.simplify(e4_A.subs(b2, 0) - A**2) == 0, "mA_radial_kernel"))
checks.append(require(sp.simplify(e4_P.subs(b2, 0) - A**2) == 0, "mP_radial_kernel"))

# Constant ruler-unit changes shift endpoint densities equally and cancel from directed
# response. A varying recalibration produces exactly the G173 endpoint transition.
e4_1 = A * H / m1**2
e4_2 = A * H / m2**2
e4_1_const = sp.simplify(e4_1 / c**2)
e4_2_const = sp.simplify(e4_2 / c**2)
checks.append(require(sp.simplify((e4_2_const / e4_1_const) - (e4_2 / e4_1)) == 0, "constant_unit_cancels"))
old_relative = sp.simplify(e4_2 / e4_1)
new_relative = sp.simplify((A * H / n2**2) / (A * H / n1**2))
transition = sp.simplify(new_relative / old_relative)
checks.append(require(sp.simplify(transition - (m2 * n1 / (m1 * n2)) ** 2) == 0, "variable_recalibration_transition"))

# Exact turning witness: same unparameterized tangent, distinct calibrated vectors.
A_w = sp.Integer(4)
r_w = sp.Integer(3)
b2_w = sp.Integer(1)
H_w = r_w**2 * b2_w
mA2_w = r_w**2 * b2_w
mP2_w = r_w**2 * b2_w / A_w
e4A_w = A_w * H_w / mA2_w
e4P_w = A_w * H_w / mP2_w
checks.append(require(mA2_w == 9, "turn_witness_mA_squared", mA2_w))
checks.append(require(mP2_w == sp.Rational(9, 4), "turn_witness_mP_squared", mP2_w))
checks.append(require(e4A_w == 4, "turn_witness_e4A", e4A_w))
checks.append(require(e4P_w == 16, "turn_witness_e4P", e4P_w))
checks.append(require(mA2_w != mP2_w and e4A_w != e4P_w, "turn_witness_distinct_germs"))

# The tensor/rank theorem is untouched.
det_sigma = sp.simplify(h_sigma.det())
checks.append(require(sp.simplify(det_sigma + H / A) == 0, "G173_tensor_retained"))
checks.append(require(sp.simplify(det_sigma.subs(v, 0) + r**2 * b2 / A) == 0, "turn_regular"))

source_rows = [
    row
    for row in csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t")
    if row.get("path")
]
source_failures: list[str] = []
for row in source_rows:
    sealed_source = ROOT / "sources" / row["path"]
    if sealed_source.is_file():
        frozen = sealed_source.read_bytes()
    else:
        frozen = subprocess.run(
            ["git", "show", f"{FROZEN_SOURCE_COMMIT}:{row['path']}"],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
    if hashlib.sha256(frozen).hexdigest() != row["sha256"]:
        source_failures.append(row["path"])
checks.append(require(len(source_rows) == 12, "source_count", len(source_rows)))
checks.append(require(not source_failures, "source_hashes_match", source_failures))
manifest_text = (HERE / "SOURCE_MANIFEST.tsv").read_text()
checks.append(require(all(f"udt_g{i}" not in manifest_text for i in range(142, 161)), "scaffold_sources_excluded"))

landing = (
    "CALIBRATED_GERM_OWNS_UNIQUE_SCALAR__UNCALIBRATED_LINE_RETAINS_ATLAS"
    "__G173_TENSOR_AND_RANK_THEOREM_RETAINED"
    "__M_IS_THE_JACOBIAN_FROM_AUXILIARY_PARAMETER_TO_SUPPLIED_RULER_COORDINATE"
    "__DISTINCT_M_DEFINE_DISTINCT_CALIBRATED_GERMS_UNLESS_IDENTICAL"
    "__CONSTANT_UNIT_RESCALE_CANCELS_FROM_ENDPOINT_DEPTH"
    "__PHYSICAL_CALIBRATION_AND_CARRY_OWNER_REMAIN_OPEN"
)

result = {
    "landing": landing,
    "status": "DERIVED_BOUNDED_AWAITING_EXTERNAL_REVIEW",
    "h_sigma": str(h_sigma),
    "h_calibrated": str(h_s),
    "H": str(H),
    "exp_4Phi_m": str(e4_phi_m),
    "m_A_squared": str(mA2),
    "m_P_squared": str(mP2),
    "constant_unit_relative_invariance": str(sp.simplify(e4_2_const / e4_1_const)),
    "variable_recalibration_factor": str(transition),
    "turning_witness": {
        "exp_2phi": 4,
        "r": 3,
        "v": 0,
        "b2": 1,
        "m_A_squared": str(mA2_w),
        "m_P_squared": str(mP2_w),
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
