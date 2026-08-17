#!/usr/bin/env python3
"""Exact production derivation for the bounded G147 pair-screen solder theorem."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def zero_matrix(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def matrix_strings(matrix: sp.Matrix) -> list[list[str]]:
    return [[str(sp.simplify(matrix[i, j])) for j in range(matrix.cols)] for i in range(matrix.rows)]


def main() -> None:
    checks: dict[str, bool] = {}

    # Coordinate-free pair-Gram identities.
    h00, h01, h11 = sp.symbols("h00 h01 h11", nonzero=True, real=True)
    h = sp.Matrix([[h00, h01], [h01, h11]])
    beta = sp.simplify(h01 / h00)
    r_coeff = sp.Matrix([-beta, 1])
    r2 = sp.simplify((r_coeff.T * h * r_coeff)[0])
    checks["abstract_clock_ruler_orthogonal"] = sp.simplify((sp.Matrix([1, 0]).T * h * r_coeff)[0]) == 0
    checks["abstract_ruler_norm_is_det_over_h00"] = sp.simplify(r2 - h.det() / h00) == 0
    checks["abstract_clock_normalizes_to_minus_one"] = sp.simplify(h00 / (-h00) + 1) == 0
    checks["abstract_ruler_normalizes_to_plus_one"] = sp.simplify(r2 / r2 - 1) == 0

    # Registered complete-coframe witness: every B,Q,S,Y,Z block is active.
    F = sp.Rational
    B = sp.Matrix([[2, F(1, 2)], [0, 3]])
    Q = sp.Matrix([[1, F(1, 3)], [0, 2]])
    S = sp.Matrix([[F(1, 5), -F(1, 7)], [F(1, 4), F(1, 6)]])
    Y = sp.eye(2)
    Z = sp.Matrix([[F(1, 10), -F(1, 8)], [-F(1, 12), F(1, 9)]])
    E = B.row_join(sp.zeros(2, 2)).col_join((Q * S).row_join(Q))
    eta = sp.diag(-1, 1, 1, 1)
    g = sp.simplify(E.T * eta * E)
    J = Y.col_join(Z)
    h_w = sp.simplify(J.T * g * J)
    J0, J1 = J[:, 0], J[:, 1]

    checks["registered_B_live"] = all(value != 0 for value in (B[0, 0], B[0, 1], B[1, 1]))
    checks["registered_Q_live"] = all(value != 0 for value in (Q[0, 0], Q[0, 1], Q[1, 1]))
    checks["registered_S_all_live"] = all(value != 0 for value in S
    )
    checks["registered_Y_rank_two"] = Y.rank() == 2
    checks["registered_Z_all_live"] = all(value != 0 for value in Z)
    checks["registered_g_lorentzian_via_congruence"] = E.det() != 0 and eta.det() == -1
    checks["registered_clock_timelike"] = h_w[0, 0] < 0
    checks["registered_pair_lorentzian"] = h_w.det() < 0

    T = sp.sqrt(-h_w[0, 0])
    beta_w = sp.simplify(h_w[0, 1] / h_w[0, 0])
    r = sp.simplify(J1 - beta_w * J0)
    L2 = sp.simplify((r.T * g * r)[0])
    L = sp.sqrt(L2)
    u = sp.simplify(J0 / T)
    n = sp.simplify(r / L)
    rho = F(2, 5)
    xi = sp.simplify(rho * n)

    checks["u_unit_timelike"] = sp.simplify((u.T * g * u)[0] + 1) == 0
    checks["n_unit_spacelike"] = sp.simplify((n.T * g * n)[0] - 1) == 0
    checks["u_n_orthogonal"] = sp.simplify((u.T * g * n)[0]) == 0
    checks["rho_nonzero_inside_ball"] = rho != 0 and abs(rho) < 1
    checks["xi_in_observer_rest"] = sp.simplify((u.T * g * xi)[0]) == 0
    checks["xi_norm_is_rho_squared"] = sp.simplify((xi.T * g * xi)[0] - rho**2) == 0
    checks["flag_span_equals_pair_span"] = sp.Matrix.hstack(u, n).row_join(J).rank() == 2

    identity = sp.eye(4)
    P_pair = sp.simplify(identity - J * h_w.inv() * J.T * g)
    P_flag = sp.simplify(identity + u * (u.T * g) - n * (n.T * g))
    checks["pair_and_directional_projectors_equal"] = zero_matrix(P_pair - P_flag)
    checks["screen_projector_idempotent"] = zero_matrix(P_pair * P_pair - P_pair)
    checks["screen_projector_metric_self_adjoint"] = zero_matrix(P_pair.T * g - g * P_pair)
    checks["screen_projector_annihilates_clock"] = zero_matrix(P_pair * u)
    checks["screen_projector_annihilates_ruler"] = zero_matrix(P_pair * n)
    checks["screen_projector_rank_two"] = P_pair.rank() == 2

    constraints_pair = sp.simplify(J.T * g)
    constraints_directional = sp.simplify(sp.Matrix.vstack(u.T * g, xi.T * g))
    stacked_constraints = constraints_pair.col_join(constraints_directional)
    checks["constraint_rowspaces_equal"] = (
        constraints_pair.rank() == 2
        and constraints_directional.rank() == 2
        and stacked_constraints.rank() == 2
    )
    checks["pair_screen_dimension_two"] = len(constraints_pair.nullspace()) == 2
    checks["directional_sphere_tangent_dimension_two"] = len(constraints_directional.nullspace()) == 2

    H_basis = sp.Matrix.hstack(*constraints_pair.nullspace())
    H_gram = sp.simplify(H_basis.T * g * H_basis)
    checks["screen_restriction_positive_first_minor"] = H_gram[0, 0] > 0
    checks["screen_restriction_positive_determinant"] = H_gram.det() > 0

    def witness_metric_and_projector(
        Bx: sp.Matrix, Qx: sp.Matrix, Sx: sp.Matrix, Yx: sp.Matrix, Zx: sp.Matrix
    ) -> tuple[sp.Matrix, sp.Matrix]:
        Ex = Bx.row_join(sp.zeros(2, 2)).col_join((Qx * Sx).row_join(Qx))
        gx = sp.simplify(Ex.T * eta * Ex)
        Jx = Yx.col_join(Zx)
        hx = sp.simplify(Jx.T * gx * Jx)
        px = sp.simplify(sp.eye(4) - Jx * hx.inv() * Jx.T * gx)
        return hx, px

    perturbations = {
        "B": (2 * B, Q, S, Y, Z),
        "Q": (B, 2 * Q, S, Y, Z),
        "S": (B, Q, 2 * S, Y, Z),
        "Y": (B, Q, S, 2 * Y, Z),
        "Z": (B, Q, S, Y, 2 * Z),
    }
    for name, values in perturbations.items():
        h_changed, p_changed = witness_metric_and_projector(*values)
        checks[f"{name}_sensitivity_changes_h"] = not zero_matrix(h_changed - h_w)
        checks[f"{name}_sensitivity_changes_screen_projector"] = not zero_matrix(p_changed - P_pair)

    # Ambient basis covariance: old components = A * new components.
    A = sp.Matrix([
        [1, F(1, 3), 0, 0],
        [0, 1, F(1, 5), 0],
        [0, 0, 1, F(1, 7)],
        [0, 0, 0, 1],
    ])
    g_new = sp.simplify(A.T * g * A)
    J_new = sp.simplify(A.inv() * J)
    h_new = sp.simplify(J_new.T * g_new * J_new)
    P_new = sp.simplify(sp.eye(4) - J_new * h_new.inv() * J_new.T * g_new)
    checks["ambient_basis_preserves_pair_metric"] = zero_matrix(h_new - h_w)
    checks["ambient_basis_covariant_projector"] = zero_matrix(P_new - A.inv() * P_pair * A)

    # Flag-preserving pair-domain change: positive diagonal keeps clock line and ruler orientation.
    R = sp.Matrix([[2, F(1, 3)], [0, F(3, 2)]])
    J_R = sp.simplify(J * R)
    h_R = sp.simplify(J_R.T * g * J_R)
    J0_R, J1_R = J_R[:, 0], J_R[:, 1]
    T_R = sp.sqrt(-h_R[0, 0])
    beta_R = sp.simplify(h_R[0, 1] / h_R[0, 0])
    r_R = sp.simplify(J1_R - beta_R * J0_R)
    L_R = sp.sqrt(sp.simplify((r_R.T * g * r_R)[0]))
    u_R = sp.simplify(J0_R / T_R)
    n_R = sp.simplify(r_R / L_R)
    P_R = sp.simplify(sp.eye(4) - J_R * h_R.inv() * J_R.T * g)
    checks["flag_preserving_domain_clock_unchanged"] = zero_matrix(u_R - u)
    checks["flag_preserving_domain_ruler_unchanged"] = zero_matrix(n_R - n)
    checks["flag_preserving_domain_screen_unchanged"] = zero_matrix(P_R - P_pair)

    # A general boost of the flag is not gauge for this theorem; it changes the query clock line.
    boost_like = sp.Matrix([[1, F(1, 2)], [F(1, 3), 1]])
    J_changed = sp.simplify(J * boost_like)
    checks["non_flag_preserving_change_changes_clock_line"] = sp.Matrix.hstack(J0, J_changed[:, 0]).rank() == 2

    # Frozen source scope.
    source_rows = []
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8") as handle:
        header = handle.readline().rstrip("\n").split("\t")
        for line in handle:
            values = line.rstrip("\n").split("\t")
            source_rows.append(dict(zip(header, values)))
    for index, row in enumerate(source_rows, start=1):
        digest = hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest()
        checks[f"source_{index}_hash"] = digest == row["sha256"]

    checks = {name: bool(passed) for name, passed in checks.items()}
    failures = [name for name, passed in checks.items() if not passed]
    result = {
        "landing": (
            "CONDITIONAL_QUERY_RELATIVE_REST_SPACE_IDENTITY__PHYSICAL_THREE_POSITION_LIFT_AND_CROSS_QUERY_CARRY_OPEN"
            if not failures
            else "PREREGISTERED_TEST_FAILURE"
        ),
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "failures": failures,
        "registered_witness": {
            "g": matrix_strings(g),
            "J": matrix_strings(J),
            "h": matrix_strings(h_w),
            "beta_pair": str(beta_w),
            "L_pair_squared": str(L2),
            "screen_gram": matrix_strings(H_gram),
            "screen_projector": matrix_strings(P_pair),
        },
        "scope": {
            "owned": "one supplied regular calibrated pair query plus a defined rest-space position lift at nonzero rho",
            "derived": "within that conditional lift the directional tangent equals the metric pair screen",
            "open": [
                "coincidence and degenerate or null pair strata",
                "cross-query middle-observer screen carry",
                "positional gyration versus metric U_gamma",
                "multidirectional ball-law selection and complete arrow reversal",
                "history X_max proper length dynamics and downstream physics",
            ],
        },
    }
    output = HERE / "DERIVATION_RESULT.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit(f"FAIL: {failures}")
    print(f"PASS: {result['passed']}/{result['total']} exact G147 production checks")


if __name__ == "__main__":
    main()
