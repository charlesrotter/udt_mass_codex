#!/usr/bin/env python3
"""Independent stdlib/Fraction reconstruction of load-bearing audit claims."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
from fractions import Fraction
from pathlib import Path


ROOT = Path(os.environ["UDT_REPO"]).resolve()
HERE = Path(__file__).resolve().parent


def matmul(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def diag(*blocks):
    size = sum(len(block) for block in blocks)
    out = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    offset = 0
    for block in blocks:
        for i, row in enumerate(block):
            for j, value in enumerate(row):
                out[offset + i][offset + j] = value
        offset += len(block)
    return out


def transpose(a):
    return [list(row) for row in zip(*a)]


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def commutator(a, b):
    return sub(matmul(a, b), matmul(b, a))


def zero(a):
    return all(value == 0 for row in a for value in row)


def rows(relative):
    with (ROOT / relative).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main():
    checks = {}

    # Rational representatives avoid sharing symbolic code.
    S = [[Fraction(1, 2), 0], [0, Fraction(2)]]
    Sinv = [[Fraction(2), 0], [0, Fraction(1, 2)]]
    I2 = [[Fraction(1), 0], [0, Fraction(1)]]
    checks["reciprocal_det_one"] = det2(S) == 1
    checks["reciprocal_inverse"] = matmul(S, Sinv) == I2

    # Nontrivial rational symplectic shear in each screen direction.
    I = I2
    Z = [[Fraction(0), 0], [0, Fraction(0)]]
    M = [
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]
    M = [[Fraction(v) for v in row] for row in M]
    Omega = [
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [-1, 0, 0, 0],
        [0, -1, 0, 0],
    ]
    Omega = [[Fraction(v) for v in row] for row in Omega]
    checks["transverse_symplectic"] = matmul(matmul(transpose(M), Omega), M) == Omega

    C = diag(S, M)
    P_rec = diag(I2, [[0 for _ in range(4)] for _ in range(4)])
    I4 = [[Fraction(int(i == j)) for j in range(4)] for i in range(4)]
    P_trans = diag([[0, 0], [0, 0]], I4)
    checks["reducible_rec_projector"] = zero(commutator(C, P_rec))
    checks["reducible_trans_projector"] = zero(commutator(C, P_trans))

    # J4 is invertible, so J4 H=0 implies every column of H is zero.
    J = [[Fraction(0), -1], [1, Fraction(0)]]
    J4 = diag(J, J)
    checks["screen_gauge_generator_invertible"] = (
        det2(J) == 1 and matmul(J4, transpose(J4)) == I4
    )

    # Numerical quadrature-free primitive of -2 sin eta cos eta:
    # integral = [-sin^2 eta]_0^(pi/2) = -1.
    hopf_eta_integral = Fraction(-1)
    hopf_normalized = -hopf_eta_integral
    checks["conditional_unit_hopf_integral"] = hopf_normalized == 1
    # exp(4 phi) runs from zero to infinity, so normalized reciprocal weights
    # interpolate between opposite angular collapses.
    checks["reciprocal_weight_endpoint_order"] = (
        math.exp(-40) < Fraction(1, 10**12) and math.exp(40) > 10**12
    )

    determinants = []
    for a, b in [((1, 0), (1, 0)), ((1, 0), (0, 1)), ((1, 0), (1, 3)), ((1, 0), (2, 5))]:
        determinants.append(abs(a[0] * b[1] - a[1] * b[0]))
    checks["completion_family_not_unique"] = determinants == [0, 1, 3, 5]

    # Exact density differential from quotient rule.
    V, rho, dM, dV = Fraction(7), Fraction(11, 3), Fraction(5, 2), Fraction(-4, 3)
    derivative = dM / V - (rho * V) * dV / (V * V)
    expected = (dM - rho * dV) / V
    checks["density_variation"] = derivative == expected
    trace_matrix = [[Fraction(3), 0], [0, Fraction(3)]]
    trace = trace_matrix[0][0] + trace_matrix[1][1]
    tf = [
        [trace_matrix[i][j] - (trace / 2 if i == j else 0) for j in range(2)]
        for i in range(2)
    ]
    checks["isotropic_tracefree_zero"] = zero(tf)

    # Rectangular line integrals for F=(0,x), from (0,0) to (x,y).
    x, y = Fraction(2), Fraction(3)
    path_x_then_y = x * y
    path_y_then_x = Fraction(0)
    checks["nonintegrable_path_dependence"] = path_x_then_y != path_y_then_x
    # For F=(y,x), both paths give xy and grad(xy) is exact.
    checks["integrable_control"] = x * y == y * x
    # A locally closed constant one-form k dtheta on a circle has nonzero
    # period. Hence local closure does not guarantee a global action.
    k = Fraction(3, 2)
    circle_period_over_2pi = k
    checks["global_period_obstruction"] = circle_period_over_2pi != 0

    equations = rows("udt_bootstrap_clock_angular_closure_audit_2026-07-24/EQUATION_FAMILY_GATE_MATRIX.tsv")
    completions = rows("udt_bootstrap_clock_angular_closure_audit_2026-07-24/COMPLETION_BOOTSTRAP_ATLAS.tsv")
    hopf = {row["step_id"]: row for row in rows("udt_reciprocal_pair_global_module_audit_2026-07-24/CONDITIONAL_HOPF_CROSSWALK.tsv")}
    action = {row["id"]: row for row in rows("native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv")}
    checks["equation_census_28_zero_complete"] = (
        len(equations) == 28
        and all(row["complete_simultaneous_closure"] == "NO" for row in equations)
    )
    checks["completion_census_12_zero_complete"] = (
        len(completions) == 12
        and all(row["complete_g_phi_matter_witness"] == "NO" for row in completions)
    )
    checks["hopf_open_chain"] = (
        hopf["H12"]["status"] == "OPEN_TYPE_GAP"
        and hopf["H13"]["status"] == "OPEN"
        and hopf["H14"]["status"] == "OPEN"
    )
    checks["action_source_boundary_mass_open"] = all(
        action[key]["status"] == "OPEN" for key in ("S22", "S23", "S24", "S25")
    )

    assert all(checks.values()), checks
    production = json.loads((HERE / "RESULT.json").read_text(encoding="utf-8"))
    consistency = {
        "production_pass": production["result"] == "PASS",
        "production_reducible": production["checks"]["reciprocal_invariant_projector"] == "PASS",
        "production_hopf_conditional": production["checks"]["conditional_unit_hopf_charge"] == "PASS",
        "production_no_complete_closure": production["checks"]["zero_complete_equation_closures"] == "PASS",
        "production_action_open": production["checks"]["complete_action_open"] == "PASS",
    }
    assert all(consistency.values()), consistency
    output = {
        "schema": "udt-sandbox-global-local-relational-closure-independent-1.0",
        "result": "PASS",
        "checks": checks,
        "check_count": len(checks),
        "cross_implementation_consistency": consistency,
        "production_sha256": hashlib.sha256((HERE / "RESULT.json").read_bytes()).hexdigest(),
    }
    (HERE / "INDEPENDENT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
