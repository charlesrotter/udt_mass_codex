#!/usr/bin/env python3
"""Exact G170 endpoint-relative reciprocal response algebra."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import subprocess

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
FROZEN_SOURCE_COMMIT = "f9a6d1e6"
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
        actual = hashlib.sha256(frozen).hexdigest()
        if actual != row["sha256"]:
            failures.append(row["path"])
    return len(rows), failures


def pair_metric(T: sp.Expr, L: sp.Expr, beta: sp.Expr) -> sp.Matrix:
    return sp.Matrix(
        [
            [-T**2, -T**2 * beta],
            [-T**2 * beta, L**2 - T**2 * beta**2],
        ]
    )


def q_squared_from_h(h: sp.Matrix) -> sp.Expr:
    return sp.factor(h[0, 0] ** 2 / (-h.det()))


def chi_from_exp2_depth(exp2_depth: sp.Expr) -> sp.Expr:
    return sp.cancel((exp2_depth - 1) / (exp2_depth + 1))


# 1. General endpoint decomposition and terminal c_E readout, with live shift.
T_A, L_A, T_B, L_B = sp.symbols("T_A L_A T_B L_B", positive=True)
beta_A, beta_B = sp.symbols("beta_A beta_B", real=True)
h_A = pair_metric(T_A, L_A, beta_A)
h_B = pair_metric(T_B, L_B, beta_B)

check("endpoint_A_determinant", sp.factor(h_A.det()) == -T_A**2 * L_A**2, h_A.det())
check("endpoint_B_determinant", sp.factor(h_B.det()) == -T_B**2 * L_B**2, h_B.det())
check("endpoint_A_shift_live", h_A[0, 1].has(beta_A) and h_A[1, 1].has(beta_A))
check("endpoint_B_shift_live", h_B[0, 1].has(beta_B) and h_B[1, 1].has(beta_B))
check("endpoint_A_q2_from_metric", q_squared_from_h(h_A) == T_A**2 / L_A**2)
check("endpoint_B_q2_from_metric", q_squared_from_h(h_B) == T_B**2 / L_B**2)

w_plus_A = T_A / (L_A - T_A * beta_A)
w_minus_A = -T_A / (L_A + T_A * beta_A)
inverse_slope_A = sp.simplify((1 / w_plus_A - 1 / w_minus_A) / 2)
check("two_way_terminal_readout_removes_shift", inverse_slope_A == L_A / T_A)

Phi_A = sp.log(L_A / T_A) / 2
Phi_B = sp.log(L_B / T_B) / 2
q_A = T_A / L_A
q_B = T_B / L_B

# 2. The original terminal endpoint rule: directed depth is the ratio of endpoint ratios.
q_AB = sp.cancel(q_B / q_A)
q_BA = sp.cancel(q_A / q_B)
exp2_delta_AB = sp.cancel((L_B / T_B) / (L_A / T_A))
delta_AB_from_q = -sp.log(q_AB) / 2
delta_AB_endpoint = Phi_B - Phi_A
log_difference = sp.simplify(
    sp.expand_log(delta_AB_from_q, force=True)
    - sp.expand_log(delta_AB_endpoint, force=True)
)
check("relative_q_is_endpoint_ratio", q_AB == 1 / exp2_delta_AB)
check("relative_depth_is_endpoint_difference", log_difference == 0, log_difference)
check("relative_ceff_identity", sp.simplify(q_AB - sp.exp(-2 * delta_AB_endpoint)) == 0)

# 3. Reversal swaps the same endpoint data. No separately chosen negative depth enters.
delta_BA_endpoint = Phi_A - Phi_B
check("reversal_q", sp.cancel(q_AB * q_BA) == 1)
check("reversal_depth", sp.simplify(delta_AB_endpoint + delta_BA_endpoint) == 0)
chi_AB = chi_from_exp2_depth(exp2_delta_AB)
chi_BA = chi_from_exp2_depth(1 / exp2_delta_AB)
check("reversal_chi", sp.cancel(chi_AB + chi_BA) == 0)

# 4. G166 founded branch is the A-anchored special case.
d = sp.symbols("d", real=True)
pure_subs = {
    T_A: 1,
    L_A: 1,
    beta_A: 0,
    T_B: sp.exp(-d),
    L_B: sp.exp(d),
    beta_B: 0,
}
check("pure_branch_forward_q", sp.simplify(q_AB.subs(pure_subs) - sp.exp(-2 * d)) == 0)
check(
    "pure_branch_forward_depth",
    sp.simplify(sp.expand_log(delta_AB_endpoint.subs(pure_subs), force=True) - d) == 0,
)
check(
    "pure_branch_reverse_depth",
    sp.simplify(sp.expand_log(delta_BA_endpoint.subs(pure_subs), force=True) + d) == 0,
)

# 5. G169's same-boundary surface witness is an equal-endpoint control, not a reversal failure.
a = sp.symbols("a", real=True)
h_surface_A = sp.diag(-1, 1 + a**2)
h_surface_B = sp.diag(-1, 1 + a**2)
q2_surface_A = q_squared_from_h(h_surface_A)
q2_surface_B = q_squared_from_h(h_surface_B)
Phi_surface_A = sp.log(1 + a**2) / 4
Phi_surface_B = sp.log(1 + a**2) / 4
delta_surface_AB = sp.simplify(Phi_surface_B - Phi_surface_A)
delta_surface_BA = sp.simplify(Phi_surface_A - Phi_surface_B)
check("surface_endpoint_readouts_equal", sp.simplify(q2_surface_A - q2_surface_B) == 0)
check("surface_relative_depth_zero", delta_surface_AB == 0)
check("surface_reverse_relative_depth_zero", delta_surface_BA == 0)
check("surface_reversal_holds", sp.simplify(delta_surface_AB + delta_surface_BA) == 0)
check(
    "single_endpoint_quantity_is_not_arrow_depth",
    Phi_surface_A.subs(a, 1) != delta_surface_AB.subs(a, 1),
)

# 6. Two exact nonradial G167 endpoint pullbacks retain their angular Gram before differencing.
def primary_pullback(
    u: sp.Expr,
    radius: sp.Expr,
    sine: sp.Expr,
    J: sp.Matrix,
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    u = sp.sympify(u)
    radius = sp.sympify(radius)
    sine = sp.sympify(sine)
    g = sp.diag(-sp.Integer(1) / u**2, u**2, radius**2, radius**2 * sine**2)
    g_base = sp.diag(-sp.Integer(1) / u**2, u**2)
    q_screen = sp.diag(radius**2, radius**2 * sine**2)
    Y = J[:2, :]
    Z = J[2:, :]
    return (
        sp.simplify(J.T * g * J),
        sp.simplify(Y.T * g_base * Y),
        sp.simplify(Z.T * q_screen * Z),
    )


J_angular_A = sp.Matrix(
    [[4, 0], [0, sp.Rational(1, 2)], [sp.Rational(1, 10), sp.Rational(1, 5)], [0, sp.Rational(1, 3)]]
)
h_ang_A, h_base_A, P_A = primary_pullback(2, 3, sp.Rational(4, 5), J_angular_A)
J_angular_B = sp.Matrix(
    [
        [3, sp.Rational(1, 5)],
        [sp.Rational(1, 10), sp.Rational(2, 3)],
        [sp.Rational(1, 8), sp.Rational(1, 4)],
        [sp.Rational(1, 10), sp.Rational(1, 5)],
    ]
)
h_ang_B, h_base_B, P_B = primary_pullback(
    sp.Rational(3, 2), 4, sp.Rational(3, 5), J_angular_B
)
q2_ang_A = q_squared_from_h(h_ang_A)
q2_ang_B = q_squared_from_h(h_ang_B)
q2_base_A = q_squared_from_h(h_base_A)
q2_base_B = q_squared_from_h(h_base_B)
q2_relative_angular = sp.factor(q2_ang_B / q2_ang_A)
q2_relative_angular_reverse = sp.factor(q2_ang_A / q2_ang_B)

check("angular_A_pullback_identity", sp.simplify(h_ang_A - h_base_A - P_A) == sp.zeros(2))
check("angular_B_pullback_identity", sp.simplify(h_ang_B - h_base_B - P_B) == sp.zeros(2))
check("angular_A_regular", h_ang_A[0, 0] < 0 and h_ang_A.det() < 0)
check("angular_B_regular", h_ang_B[0, 0] < 0 and h_ang_B.det() < 0)
check("angular_A_shift_live", h_ang_A[0, 1] != 0)
check("angular_B_shift_live", h_ang_B[0, 1] != 0)
check("angular_A_changes_endpoint_readout", q2_ang_A != q2_base_A)
check("angular_B_changes_endpoint_readout", q2_ang_B != q2_base_B)
check("angular_relative_reversal", sp.factor(q2_relative_angular * q2_relative_angular_reverse) == 1)

# 7. Independent common scales cancel from both endpoint readouts and their ratio.
omega_A, omega_B = sp.symbols("omega_A omega_B", positive=True)
h_scaled_A = sp.simplify(omega_A**2 * h_ang_A)
h_scaled_B = sp.simplify(omega_B**2 * h_ang_B)
check("common_scale_A_cancels", q_squared_from_h(h_scaled_A) == q2_ang_A)
check("common_scale_B_cancels", q_squared_from_h(h_scaled_B) == q2_ang_B)
check(
    "common_scale_relative_ratio_cancels",
    sp.factor(q_squared_from_h(h_scaled_B) / q_squared_from_h(h_scaled_A))
    == q2_relative_angular,
)

# 8. Matched endpoint states telescope. An unmatched middle state leaves an exact residual.
q_C = sp.symbols("q_C", positive=True)
q_AB_general = sp.cancel(q_B / q_A)
q_BC_general = sp.cancel(q_C / q_B)
q_AC_general = sp.cancel(q_C / q_A)
check("matched_q_composition", sp.cancel(q_AB_general * q_BC_general - q_AC_general) == 0)

Phi_C = sp.symbols("Phi_C", real=True)
check(
    "matched_depth_telescopes",
    sp.simplify((Phi_B - Phi_A) + (Phi_C - Phi_B) - (Phi_C - Phi_A)) == 0,
)
Phi_B_left, Phi_B_right = sp.symbols("Phi_B_left Phi_B_right", real=True)
unmatched_residual = sp.simplify(
    (Phi_B_left - Phi_A) + (Phi_C - Phi_B_right) - (Phi_C - Phi_A)
)
check("unmatched_middle_residual_exposed", unmatched_residual == Phi_B_left - Phi_B_right)
check("unmatched_middle_not_forced_zero", unmatched_residual != 0)

# 9. A global reciprocal-origin change cancels; independent recalibration is physical input.
c = sp.symbols("c", real=True)
check(
    "shared_reciprocal_origin_cancels",
    sp.simplify(((Phi_B + c) - (Phi_A + c)) - (Phi_B - Phi_A)) == 0,
)
c_A, c_B = sp.symbols("c_A c_B", real=True)
check(
    "independent_recalibration_exposed",
    sp.simplify(((Phi_B + c_B) - (Phi_A + c_A)) - (Phi_B - Phi_A)) == c_B - c_A,
)

source_count, source_failures = source_hashes()
check("source_hashes_match", source_count == 12 and not source_failures, source_failures)

landing = (
    "ENDPOINT_RELATIVE_RECIPROCAL_DEPTH_DERIVED_FROM_TERMINAL_CEFF_RATIOS"
    "__WITHIN_ONE_CONSISTENT_RECIPROCAL_CALIBRATION_CLASS"
    "__BIDIRECTIONAL_REVERSAL_AND_MATCHED_COMPOSITION_AUTOMATIC"
    "__G169_SINGLE_ENDPOINT_REVERSAL_COUNTEREXAMPLE_RECLASSIFIED"
    "__COPRESENCE_NOT_LOAD_BEARING"
    "__CROSS_QUERY_AND_FULL_NONSCALAR_CARRY_REMAIN_OPEN"
)

result = {
    "landing": landing,
    "status": "DERIVED_BOUNDED_INTEGRATION_REPAIR",
    "checks_passed": sum(int(row["passed"]) for row in checks),
    "checks_total": len(checks),
    "checks": checks,
    "surface_regrade": {
        "endpoint_phi_A_at_a_1": "log(2)/4",
        "endpoint_phi_B_at_a_1": "log(2)/4",
        "relative_delta_AB": "0",
        "relative_delta_BA": "0",
    },
    "angular_endpoint_A": {
        "h": [[str(entry) for entry in row] for row in h_ang_A.tolist()],
        "P": [[str(entry) for entry in row] for row in P_A.tolist()],
        "q_squared": str(q2_ang_A),
        "base_q_squared": str(q2_base_A),
    },
    "angular_endpoint_B": {
        "h": [[str(entry) for entry in row] for row in h_ang_B.tolist()],
        "P": [[str(entry) for entry in row] for row in P_B.tolist()],
        "q_squared": str(q2_ang_B),
        "base_q_squared": str(q2_base_B),
    },
    "angular_relative_q_squared": str(q2_relative_angular),
    "unmatched_middle_residual": str(unmatched_residual),
    "source_count": source_count,
    "source_failures": source_failures,
}
(HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"landing": landing, "passed": result["checks_passed"], "total": len(checks)}, sort_keys=True))
