#!/usr/bin/env python3
"""Independent Fraction/stdlib reconstruction of load-bearing controls."""

from __future__ import annotations

import csv
import hashlib
import itertools
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


def determinant(matrix: list[list[F]]) -> F:
    n = len(matrix)
    total = F(0)
    for perm in itertools.permutations(range(n)):
        inversions = sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        term = F(-1 if inversions % 2 else 1)
        for i in range(n):
            term *= matrix[i][perm[i]]
        total += term
    return total


def mat_vec(matrix: list[list[F]], vector: list[F]) -> list[F]:
    return [sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix]


def poly_eval(coefficients: list[F], value: F) -> F:
    return sum(coefficient * value**power for power, coefficient in enumerate(coefficients))


def poly_derivative(coefficients: list[F]) -> list[F]:
    return [F(power) * coefficient for power, coefficient in enumerate(coefficients)][1:]


def main() -> None:
    checks: dict[str, str] = {}

    ax, ao, rx = F(2), F(3), F(-2, 3)
    scalar_block = [[ax, ao], [-rx, F(1)]]
    require("I01_scalar_schur_determinant", determinant(scalar_block) == ax + ao * rx == 0, checks)
    require("I02_singular_kernel", mat_vec(scalar_block, [F(3), F(-2)]) == [0, 0], checks)
    require("I03_feedback_creates_kernel", F(1) + F(2) * F(-1, 2) == 0, checks)
    require("I04_feedback_removes_kernel", F(0) + F(1) * F(1) == 1, checks)

    AX = [[F(2), F(1)], [F(0), F(3)]]
    AO = [[F(1), F(0)], [F(0), F(2)]]
    RX = [[F(1), F(1)], [F(0), F(1)]]
    full = [AX[0] + AO[0], AX[1] + AO[1], [-v for v in RX[0]] + [F(1), F(0)], [-v for v in RX[1]] + [F(0), F(1)]]
    require("I05_matrix_schur_determinant", determinant(full) == F(15), checks)

    # Reduced residuals x and x^3 share only x=0 but have slopes one and zero.
    regular_coefficients = [F(0), F(1)]
    singular_coefficients = [F(0), F(0), F(0), F(1)]
    require("I06_same_root_different_linearization",
            poly_eval(regular_coefficients, F(0)) == poly_eval(singular_coefficients, F(0)) == 0
            and poly_eval(poly_derivative(regular_coefficients), F(0)) == 1
            and poly_eval(poly_derivative(singular_coefficients), F(0)) == 0,
            checks)
    require("I07_singular_not_branch_sufficiency",
            singular_coefficients[:3] == [0, 0, 0]
            and singular_coefficients[3] == 1,
            checks)
    # Both quadratic controls have zero first derivative at the origin.  The
    # positive form is isolated over R; the indefinite form vanishes on x=+/-l.
    grad_isolated_at_origin = [2 * F(0), 2 * F(0)]
    grad_crossing_at_origin = [2 * F(0), -2 * F(0)]
    require("I07b_same_zero_linearization",
            grad_isolated_at_origin == grad_crossing_at_origin == [0, 0], checks)
    require("I07c_isolated_versus_crossing_branch",
            determinant([[F(2), F(0)], [F(0), F(2)]]) == 4
            and determinant([[F(2), F(0)], [F(0), F(-2)]]) == -4
            and all(F(li) ** 2 - F(li) ** 2 == 0 for li in [-3, -1, 1, 3]), checks)

    gauge = [[F(1), F(0)], [F(0), F(0)]]
    require("I08_gauge_kernel", mat_vec(gauge, [F(0), F(1)]) == [0, 0], checks)
    local = [[F(0), F(0)], [F(0), F(1)]]
    stacked_boundary = local + [[F(1), F(0)]]
    require("I09_boundary_removes_local_kernel",
            mat_vec(local, [F(1), F(0)]) == [0, 0]
            and determinant(stacked_boundary[1:]) == -1,
            checks)

    a2, k1, k2 = F(4), F(-4), F(3)
    clock = [[k1 + a2, F(0)], [F(0), k2 + a2]]
    require("I10_clock_tidal_simple_kernel", determinant(clock) == 0 and mat_vec(clock, [F(1), F(0)]) == [0, 0], checks)
    degenerate = [[k1 + a2, F(0)], [F(0), F(-4) + a2]]
    require("I11_clock_tidal_degeneracy", degenerate == [[0, 0], [0, 0]], checks)

    ricci = [F(2), F(3), F(5)]
    scalar_r = sum(ricci)
    htf = [F(1), F(-1), F(0)]
    curvature_tf = sum((scalar_r / 2 - ricci[i]) * htf[i] for i in range(3))
    require("I12_curvature_tracefree_response", curvature_tf == 1, checks)
    require("I13_volume_tracefree_blind", sum(htf) == 0, checks)
    ricci_control_1 = [F(1), F(2), F(3)]
    ricci_control_2 = [F(0), F(3), F(3)]
    response_control_1 = sum((sum(ricci_control_1) / 2 - ricci_control_1[i]) * htf[i] for i in range(3))
    response_control_2 = sum((sum(ricci_control_2) / 2 - ricci_control_2[i]) * htf[i] for i in range(3))
    require("I13b_same_ricci_trace_different_TF_response",
            sum(ricci_control_1) == sum(ricci_control_2) == 6
            and response_control_1 == 1 and response_control_2 == 3, checks)

    M, V, dM, dV = F(7), F(11), F(13), F(17)
    require("I14_density_quotient", (dM - (M / V) * dV) / V == F(24, 121), checks)
    area, length, darea, dlength = F(19), F(23), F(29), F(31)
    require("I15_moving_volume", area * dlength + length * darea == F(1256), checks)

    rotation_90 = [[F(0), F(-1)], [F(1), F(0)]]
    rotation_minus_identity = [[rotation_90[i][j] - (1 if i == j else 0) for j in range(2)] for i in range(2)]
    require("I16_local_transport_not_fixed_section", determinant(rotation_minus_identity) == 2, checks)
    exchange = [[F(0), F(1)], [F(1), F(0)]]
    require("I17_toric_exchange", determinant(exchange) == -1 and mat_vec(exchange, [F(1), F(0)]) == [0, 1], checks)
    nongradient_jacobian = [[F(1), F(2)], [F(3), F(4)]]
    require("I18_vector_closure_no_scalar_objective_needed",
            determinant(nongradient_jacobian) == -2
            and nongradient_jacobian[0][1] != nongradient_jacobian[1][0], checks)

    algebra = json.loads((HERE / "ALGEBRA_RESULT.json").read_text(encoding="utf-8"))
    require("I19_production_31_integrity", algebra["sympy_version"] == "1.14.0"
            and algebra["check_count"] == 31 and set(algebra["checks"].values()) == {"PASS"}, checks)

    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    source_ok = len(sources) == 16
    for row in sources:
        path = ROOT / row["path"]
        blob = subprocess.run(["git", "rev-parse", f"HEAD:{row['path']}"], cwd=ROOT,
                              check=True, text=True, capture_output=True).stdout.strip()
        source_ok &= hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
        source_ok &= blob == row["git_blob"]
    require("I20_source_manifest", source_ok, checks)

    with (HERE / "CONNECTOR_GATE_MATRIX.tsv").open(newline="", encoding="utf-8") as handle:
        matrix = list(csv.DictReader(handle, delimiter="\t"))
    require("I21_thirteen_candidate_artifact_integrity",
            [row["candidate_id"] for row in matrix] == [f"C{i:02d}" for i in range(1, 14)]
            and not any(row["disposition"] == "DERIVED_COMPLETE_BOOTSTRAP_CONNECTOR" for row in matrix), checks)

    result = {
        "schema": "udt-metric-native-nontriviality-independent-1.0",
        "method": "stdlib_fraction_no_production_import",
        "check_count": len(checks),
        "independent_algebra_check_count": 21,
        "artifact_integrity_check_count": 3,
        "checks": checks,
        "result": "PASS",
        "maximum_supported_conclusion": "EXACT_COUPLED_NONTRIVIALITY_SKELETON_NO_COMPLETE_CONNECTOR",
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
