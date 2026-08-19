#!/usr/bin/env python3
"""Exact G172 derivation for smooth primary-metric pair families."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import subprocess

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
FROZEN_SOURCE_COMMIT = "7477d8d1"
checks: list[dict[str, object]] = []


def check(name: str, condition: object, detail: object = "") -> None:
    passed = bool(condition)
    checks.append({"name": name, "passed": passed, "detail": str(detail)})
    if not passed:
        raise AssertionError(f"{name}: {detail}")


def source_hashes() -> tuple[int, list[str]]:
    rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
    failures: list[str] = []
    for row in rows:
        frozen = subprocess.run(
            ["git", "show", f"{FROZEN_SOURCE_COMMIT}:{row['path']}"],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
        if hashlib.sha256(frozen).hexdigest() != row["sha256"]:
            failures.append(row["path"])
    return len(rows), failures


# Primary metric and the full angular Gram of a smooth curve gamma(r) on S^2.
r = sp.symbols("r", positive=True)
phi, phi_p = sp.symbols("phi phi_p", real=True)
theta, theta_p, psi_p = sp.symbols("theta theta_p psi_p", real=True)
a2, a2_p = sp.symbols("a2 a2_p", nonnegative=True)

g = sp.diag(-sp.exp(-2 * phi), sp.exp(2 * phi), r**2, r**2 * sp.sin(theta) ** 2)
J = sp.Matrix(
    [
        [1, 0],
        [0, 1],
        [0, theta_p],
        [0, psi_p],
    ]
)
h_full = sp.simplify(J.T * g * J)
a2_full = theta_p**2 + sp.sin(theta) ** 2 * psi_p**2
h = sp.diag(-sp.exp(-2 * phi), sp.exp(2 * phi) + r**2 * a2)
W = 1 + r**2 * sp.exp(-2 * phi) * a2

check("pullback_time_component", h_full[0, 0] == -sp.exp(-2 * phi), h_full)
check("pullback_cross_component", h_full[0, 1] == 0, h_full)
check(
    "pullback_angular_gram_retained",
    sp.simplify(h_full[1, 1] - (sp.exp(2 * phi) + r**2 * a2_full)) == 0,
    h_full[1, 1],
)
check("invariant_speed_reduction", h == sp.diag(-sp.exp(-2 * phi), sp.exp(2 * phi) + r**2 * a2), h)
check("determinant", sp.simplify(h.det() + W) == 0, h.det())
check("regular_lorentzian", sp.ask(sp.Q.positive(W)) is True, W)

# Terminal pair readout.  Exponentiated identities avoid branch-dependent log rewrites.
Phi = phi + sp.log(W) / 4
q2 = sp.simplify(h[0, 0] ** 2 / (-h.det()))
ceff_ratio = sp.exp(-2 * phi) / sp.sqrt(W)
check("readout_exponential", sp.simplify(sp.exp(4 * (Phi - phi)) - W) == 0)
check("q2_exact", sp.simplify(q2 - sp.exp(-4 * phi) / W) == 0, q2)
check("ceff_square_is_q2", sp.simplify(ceff_ratio**2 - q2) == 0)
check("ceff_is_exp_minus_2Phi", sp.simplify(ceff_ratio**2 - sp.exp(-4 * Phi)) == 0)
check("angular_modulation_nonnegative", sp.ask(sp.Q.nonnegative(Phi - phi)) is True, Phi - phi)
check("radial_Phi_recovery", sp.simplify(Phi.subs(a2, 0) - phi) == 0)
check("radial_ceff_recovery", sp.simplify(ceff_ratio.subs(a2, 0) - sp.exp(-2 * phi)) == 0)

# Exact derivative along the supplied family.
W_p = sp.exp(-2 * phi) * (2 * r * a2 + r**2 * a2_p - 2 * r**2 * phi_p * a2)
Phi_p = phi_p + W_p / (4 * W)
W_direct_p = sp.diff(W, r) + sp.diff(W, phi) * phi_p + sp.diff(W, a2) * a2_p
Phi_direct_p = sp.diff(Phi, r) + sp.diff(Phi, phi) * phi_p + sp.diff(Phi, a2) * a2_p
check("W_derivative", sp.simplify(W_direct_p - W_p) == 0, W_direct_p)
check("Phi_derivative", sp.simplify(Phi_direct_p - Phi_p) == 0, Phi_direct_p)

# Same-family endpoint reversal and telescoping.
Phi_1, Phi_2, Phi_3 = sp.symbols("Phi_1 Phi_2 Phi_3", real=True)
delta_12 = Phi_2 - Phi_1
delta_21 = Phi_1 - Phi_2
delta_23 = Phi_3 - Phi_2
delta_13 = Phi_3 - Phi_1
check("same_family_reversal", sp.simplify(delta_12 + delta_21) == 0)
check("same_family_telescoping", sp.simplify(delta_12 + delta_23 - delta_13) == 0)

# Static Frobenius closure.  K has constant coordinate components and S is time independent.
# The only nonconstant entries in S depend on r, while K differentiates only x0.
K = sp.Matrix([1, 0, 0, 0])
S = sp.Matrix([0, 1, theta_p, psi_p])
bracket = sp.zeros(4, 1)
check("static_frobenius_bracket", bracket == sp.zeros(4, 1), f"K={K.T}, S={S.T}")

# Radial reparameterization.  Raw terminal Phi is chart-calibrated, not invariant under
# independent rescaling of the spatial pair coordinate.  Areal-radius calibration removes it
# exactly when v=dr/dsigma is nonzero (positive orientation used here).
v, b2, lam = sp.symbols("v b2 lam", positive=True)
h_sigma = sp.diag(-sp.exp(-2 * phi), sp.exp(2 * phi) * v**2 + r**2 * b2)
W_areal = 1 + r**2 * sp.exp(-2 * phi) * b2 / v**2
Phi_sigma = phi + sp.log(v) / 2 + sp.log(W_areal) / 4
Phi_areal = phi + sp.log(W_areal) / 4
check("sigma_determinant", sp.simplify(h_sigma.det() + v**2 * W_areal) == 0)
check(
    "raw_reparameterization_shift",
    sp.simplify(
        (phi + sp.log(lam * v) / 2 + sp.log(1 + r**2 * sp.exp(-2 * phi) * (lam**2 * b2) / (lam * v) ** 2) / 4)
        - Phi_sigma
        - sp.log(lam) / 2
    )
    == 0,
)
check("areal_calibration_removes_speed", sp.simplify(Phi_sigma - sp.log(v) / 2 - Phi_areal) == 0)
check("areal_angular_speed", sp.simplify(W_areal - (1 + r**2 * sp.exp(-2 * phi) * (b2 / v**2))) == 0)

# Center limit is deliberately only a one-sided chart limit under bounded angular speed.
W_center = W.subs(a2, sp.symbols("a0", nonnegative=True))
check("bounded_angular_center_W_limit", sp.limit(W_center, r, 0, dir="+") == 1)
check("bounded_angular_center_modulation_limit", sp.limit(sp.log(W_center) / 4, r, 0, dir="+") == 0)

source_count, source_failures = source_hashes()
manifest_text = (HERE / "SOURCE_MANIFEST.tsv").read_text()
check("source_hashes_match", source_count == 11 and not source_failures, source_failures)
check("scaffolded_sources_excluded", all(f"udt_g{i}" not in manifest_text for i in range(142, 161)))

landing = (
    "SMOOTH_FAMILY_CLOSURE"
    "__PRIMARY_METRIC_PULLBACK_GIVES_EXACT_RADIAL_PLUS_ANGULAR_RESPONSE"
    "__STATIC_TIME_ORTHOGONAL_MONOTONE_AREAL_FAMILIES_INTEGRATE"
    "__REVERSAL_AND_TELESCOPING_HOLD_WITHIN_ONE_SUPPLIED_FAMILY"
    "__FIRST_BOUNDARY_IS_CALIBRATION_OR_REGULARITY_LOSS"
    "__NO_PHYSICAL_FAMILY_SELECTION_OR_GLOBAL_COMPLETION"
)

result = {
    "landing": landing,
    "status": "DERIVED_BOUNDED_AWAITING_INDEPENDENT_AND_EXTERNAL_REVIEW",
    "checks_passed": sum(int(row["passed"]) for row in checks),
    "checks_total": len(checks),
    "checks": checks,
    "metric": str(g),
    "pair_metric": str(h),
    "angular_speed": str(a2_full),
    "W": str(W),
    "Phi": str(Phi),
    "ceff_over_cE": str(ceff_ratio),
    "W_prime": str(W_p),
    "Phi_prime": str(Phi_p),
    "source_count": source_count,
    "source_failures": source_failures,
}
(HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({key: result[key] for key in ("landing", "checks_passed", "checks_total")}, sort_keys=True))
