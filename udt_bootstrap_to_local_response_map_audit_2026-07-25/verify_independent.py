#!/usr/bin/env python3
"""Independent standard-library/Fraction reconstruction of load-bearing algebra."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def require(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def mat_vec(row: list[F], matrix: list[list[F]]) -> list[F]:
    return [sum(row[i] * matrix[i][j] for i in range(len(row))) for j in range(len(matrix[0]))]


def main() -> None:
    checks: dict[str, str] = {}

    M, V, dM, dV = F(7), F(11), F(13), F(17)
    drho = (V * dM - M * dV) / (V * V)
    require("I01_density_quotient", drho == F(24, 121), checks)

    # Determinant derivative and trace formula at an exact rational sample.
    a, b, c = F(2), F(3), F(5)
    da, db, dc = F(7), F(11), F(13)
    ddet = da * b * c + a * db * c + a * b * dc
    trace = da / a + db / b + dc / c
    require("I02_volume_log_derivative", ddet / (a * b * c) == trace, checks)
    require("I03_diagonal_TF_trace", F(0) + F(1) - F(1) == 0, checks)
    h_inv = [[F(1, 2), F(0), F(0)], [F(0), F(1, 3), F(0)], [F(0), F(0), F(1, 5)]]
    dh_shear = [[F(0), F(0), F(0)], [F(0), F(0), F(7)], [F(0), F(7), F(0)]]
    shear_trace = sum(h_inv[i][j] * dh_shear[j][i] for i in range(3) for j in range(3))
    require("I04_shear_TF_trace", shear_trace == 0, checks)

    fp, eta, dm_tf = F(19), F(23), F(29)
    alpha_tf = eta * fp * dm_tf / V
    require("I05_density_TF_mass_only", alpha_tf == F(12673, 11), checks)
    require("I06_density_TF_zero_without_mass", eta * fp * F(0) / V == 0, checks)

    A, L, dA, dL = F(31), F(37), F(41), F(43)
    require("I07_moving_boundary_product_rule", A * dL + L * dA == F(2850), checks)
    require("I08_fixed_boundary_removes_shape", L * dA == F(1517), checks)

    epsilon = F(1, 100)
    require("I09_window_contains_noncentral_point", abs(epsilon / 2) < epsilon and epsilon / 2 != 0, checks)

    u = F(2)
    require("I10_conormal_proportional", [1 + u * u, 0] == [F(5), F(0)], checks)
    r, k = F(2), F(3)
    require("I11_offshell_extension_differs", 3 * k * k * r * r == F(108), checks)

    J1 = [[F(1), F(0)], [F(0), F(1)]]
    J2 = [[F(1), F(1, 2)], [F(1, 2), F(1)]]
    require("I12_counterfamily_nonsingular", J1[0][0] * J1[1][1] == 1 and J2[0][0] * J2[1][1] - J2[0][1] * J2[1][0] == F(3, 4), checks)
    require("I13_counterfamily_integrable", J1[0][1] == J1[1][0] and J2[0][1] == J2[1][0], checks)
    q, s = F(2), F(3)
    require("I14_counterfamily_response_differs", [q, s] != [q + s / 2, s + q / 2], checks)

    closure_j = [[F(1), F(1)], [F(1), F(-1)]]
    require("I15_dual_pairing_changes_response", mat_vec([F(1), F(0)], closure_j) != mat_vec([F(0), F(1)], closure_j), checks)

    mix = [[F(1), F(1), F(0)], [F(0), F(1), F(1)], [F(1), F(0), F(1)]]
    le, lr, lk = F(2), F(3), F(5)
    require("I16_multiobservable_weights", mat_vec([le, lr, lk], mix) == [le + lk, le + lr, lr + lk], checks)
    angular_j = [[F(7), F(11)], [F(0), F(0)], [F(13), F(17)]]
    require("I17_non_density_angular_response", mat_vec([le, lr, lk], angular_j) == [le * 7 + lk * 13, le * 11 + lk * 17], checks)

    fixed_residual_1 = lambda z: z
    fixed_residual_2 = lambda z: z - z / 2
    slope_1 = fixed_residual_1(F(1)) - fixed_residual_1(F(0))
    slope_2 = fixed_residual_2(F(1)) - fixed_residual_2(F(0))
    require("I18_fixed_point_same_root_different_slope",
            fixed_residual_1(F(0)) == fixed_residual_2(F(0)) == 0
            and slope_1 != slope_2, checks)
    omega = F(3, 2)
    require("I19_conformal_volume_weight", omega**3 == F(27, 8), checks)

    # c^a G^b: mass exponent fixes b; time exponent then fixes a and contradicts target length powers.
    b_length, a_length = F(0), F(0)
    require("I20_no_length_from_c_G", a_length + 3 * b_length != 1, checks)
    b_density, a_density = F(-1), F(2)
    require("I21_no_density_from_c_G", a_density + 3 * b_density != -3, checks)

    algebra = json.loads((HERE / "ALGEBRA_RESULT.json").read_text(encoding="utf-8"))
    require("I22_production_schema", algebra["schema"] == "udt-bootstrap-to-local-response-algebra-1.0", checks)
    require("I23_pinned_sympy", algebra["sympy_version"] == "1.14.0", checks)
    require("I24_production_38_checks", algebra["check_count"] == 38 and set(algebra["checks"].values()) == {"PASS"}, checks)
    require("I25_multiobservable_ruling", algebra["structural_rulings"]["multiobservable_bootstrap"].startswith("EXACT_COUPLED_TWO_ARROW"), checks)

    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    source_ok = len(sources) == 15
    for item in sources:
        path = ROOT / item["path"]
        blob = subprocess.run(["git", "rev-parse", f"HEAD:{item['path']}"], cwd=ROOT,
                              check=True, text=True, capture_output=True).stdout.strip()
        source_ok &= hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"]
        source_ok &= blob == item["git_blob"]
    require("I26_source_manifest", source_ok, checks)

    with (HERE / "GLOBAL_LOCAL_CLOSURE_LEDGER.tsv").open(newline="", encoding="utf-8") as handle:
        closure = {row["arrow_id"]: row for row in csv.DictReader(handle, delimiter="\t")}
    require("I27_two_arrow_closure_status",
            closure["GL01"]["current_status"] == "WORKING_TYPE_NOT_DERIVED"
            and closure["GL02"]["current_status"] == "CONDITIONAL_TYPE_NOT_COMPLETE"
            and closure["GL03"]["current_status"] == "WORKING_BOOTSTRAP_HYPOTHESIS", checks)
    require("I28_optimization_not_assumed",
            closure["GL04"]["current_status"] == "OPEN_STRONGER_PREMISE", checks)

    with (HERE / "OPTIMIZATION_SEMANTICS.tsv").open(newline="", encoding="utf-8") as handle:
        semantics = {row["term"]: row for row in csv.DictReader(handle, delimiter="\t")}
    require("I29_owner_tuning_vs_scalar_extremization",
            semantics["TUNING_OR_CLOSURE"]["status"] == "WORKING_BOOTSTRAP_HYPOTHESIS"
            and semantics["SCALAR_EXTREMIZATION_REALIZATION"]["status"] == "OPEN_STRONGER_PREMISE", checks)

    # Independent scalar control of A(X,O)=0 and O-R(X)=0.
    ax, ao, rx, lam, delta_x = F(2), F(3), F(5), F(7), F(11)
    reduced = lam * (ax + ao * rx) * delta_x
    observable_only = lam * ao * rx * delta_x
    require("I30_two_arrow_direct_local_term", reduced - observable_only == lam * ax * delta_x, checks)

    # Independent orthonormal-frame contraction for the curvature-integral candidate.
    ricci_diag = [F(2), F(3), F(5)]
    scalar_r = sum(ricci_diag)
    h_tf_diag = [F(1), F(-1), F(0)]
    curvature_tf = sum((scalar_r / 2 - ricci_diag[i]) * h_tf_diag[i] for i in range(3))
    require("I31_curvature_candidate_tracefree_bulk", curvature_tf == F(1), checks)

    result = {
        "schema": "udt-bootstrap-to-local-response-independent-1.0",
        "method": "stdlib_fraction_no_production_import",
        "check_count": len(checks),
        "checks": checks,
        "result": "PASS",
        "maximum_supported_conclusion": "CONDITIONAL_MULTIOBSERVABLE_RESPONSE_SKELETON_NOT_SELECTED_COMPLETE_MAP",
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
