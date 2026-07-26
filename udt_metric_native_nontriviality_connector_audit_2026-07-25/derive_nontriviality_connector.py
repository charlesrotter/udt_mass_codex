#!/usr/bin/env python3
"""Exact CPU algebra for the metric-native nontriviality connector audit."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def require(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not bool(condition):
        raise AssertionError(name)
    checks[name] = "PASS"


def main() -> None:
    checks: dict[str, str] = {}

    # Scalar two-arrow closure and Schur complement.
    ax, ao, rx = sp.symbols("A_X A_O R_X")
    J = sp.Matrix([[ax, ao], [-rx, 1]])
    S = sp.expand(ax + ao * rx)
    require("scalar_block_determinant_is_reduced_tuning_operator",
            sp.expand(J.det()) == S, checks)

    # Exact singular and regular controls.
    J_singular = J.subs({ax: 2, ao: 3, rx: sp.Rational(-2, 3)})
    kernel = sp.Matrix([3, -2])
    require("singular_feedback_kernel_reconstructs", J_singular * kernel == sp.zeros(2, 1), checks)
    require("singular_feedback_rank_one", J_singular.rank() == 1, checks)
    J_regular = J.subs({ax: 2, ao: 3, rx: 1})
    require("regular_feedback_full_rank", J_regular.det() == 5 and J_regular.rank() == 2, checks)

    # Feedback can create or remove infinitesimal nontriviality.
    require("feedback_can_create_kernel_from_regular_local_operator",
            ax.subs(ax, 1) != 0 and S.subs({ax: 1, ao: 2, rx: sp.Rational(-1, 2)}) == 0, checks)
    require("feedback_can_remove_local_kernel",
            ax.subs(ax, 0) == 0 and S.subs({ax: 0, ao: 1, rx: 1}) == 1, checks)

    # A complete two-dimensional matrix control.
    AX = sp.Matrix([[2, 1], [0, 3]])
    AO = sp.Matrix([[1, 0], [0, 2]])
    RX = sp.Matrix([[1, 1], [0, 1]])
    I2 = sp.eye(2)
    full = AX.row_join(AO).col_join((-RX).row_join(I2))
    schur = AX + AO * RX
    require("matrix_schur_determinant_agrees", full.det() == schur.det() == 15, checks)
    require("matrix_schur_reduction_exact", schur == sp.Matrix([[3, 2], [0, 5]]), checks)
    AX_graph = sp.eye(2)
    AO_graph = sp.eye(2)
    RX_graph = sp.diag(-1, 0)
    S_graph = AX_graph + AO_graph * RX_graph
    J_graph = AX_graph.row_join(AO_graph).col_join((-RX_graph).row_join(sp.eye(2)))
    xi_graph = sp.Matrix([1, 0])
    graph_kernel = xi_graph.col_join(RX_graph * xi_graph)
    require("kernel_graph_isomorphic_to_reduced_kernel",
            S_graph * xi_graph == sp.zeros(2, 1)
            and J_graph * graph_kernel == sp.zeros(4, 1)
            and len(S_graph.nullspace()) == len(J_graph.nullspace()) == 1,
            checks)

    # Same realized root, different regular/singular response.
    x, o = sp.symbols("x o", real=True)
    R = -x
    A_regular = 2 * x + o
    A_singular = x + o + x**3
    reduced_regular = sp.expand(A_regular.subs(o, R))
    reduced_singular = sp.expand(A_singular.subs(o, R))
    require("same_unique_root_counterfamily",
            sp.solve(reduced_regular, x) == [0] and sp.solve(reduced_singular, x) == [0], checks)
    require("same_root_different_linearization",
            sp.diff(reduced_regular, x).subs(x, 0) == 1
            and sp.diff(reduced_singular, x).subs(x, 0) == 0, checks)
    require("singular_linearization_not_nonlinear_branch_sufficiency",
            reduced_singular == x**3 and sp.solve(reduced_singular, x) == [0], checks)

    # The same zero linearization can underlie either an isolated real root or
    # crossing nonzero branches.  Linear singularity alone cannot decide.
    lam = sp.symbols("lambda", real=True)
    isolated_quadratic = x**2 + lam**2
    crossing_quadratic = x**2 - lam**2
    origin_gradient_isolated = sp.Matrix([
        sp.diff(isolated_quadratic, x), sp.diff(isolated_quadratic, lam)
    ]).subs({x: 0, lam: 0})
    origin_gradient_crossing = sp.Matrix([
        sp.diff(crossing_quadratic, x), sp.diff(crossing_quadratic, lam)
    ]).subs({x: 0, lam: 0})
    require("same_singular_linearization_different_nonlinear_models",
            origin_gradient_isolated == origin_gradient_crossing == sp.zeros(2, 1), checks)
    require("isolated_versus_crossing_real_branch_control",
            sp.hessian(isolated_quadratic, (x, lam)) == sp.diag(2, 2)
            and sp.hessian(crossing_quadratic, (x, lam)) == sp.diag(2, -2)
            and sp.factor(crossing_quadratic) == (x - lam) * (x + lam)
            and sp.expand(isolated_quadratic.subs(x, lam)) == 2 * lam**2,
            checks)

    # Pure-gauge kernel and boundary-incompatible local kernel controls.
    gauge_operator = sp.Matrix([[1, 0], [0, 0]])
    require("gauge_kernel_exists_but_physical_coordinate_fixed",
            gauge_operator.nullspace() == [sp.Matrix([0, 1])], checks)
    local_operator = sp.Matrix([[0, 0], [0, 1]])
    boundary_row = sp.Matrix([[1, 0]])
    stacked = local_operator.col_join(boundary_row)
    require("local_kernel_removed_by_boundary_domain",
            local_operator.nullspace() == [sp.Matrix([1, 0])] and stacked.rank() == 2, checks)

    # Clock-screen tidal kernel and intrinsic projector control.
    a, k1, k2 = sp.symbols("a k1 k2", real=True)
    T = sp.diag(k1, k2)
    clock_tidal = T + a**2 * sp.eye(2)
    require("clock_screen_kernel_determinant",
            sp.factor(clock_tidal.det()) == (a**2 + k1) * (a**2 + k2), checks)
    matched = clock_tidal.subs({k1: -a**2})
    P_clock = sp.simplify(sp.eye(2) - matched / (sp.trace(T.subs(k1, -a**2)) + 2 * a**2))
    require("clock_screen_simple_kernel_projector",
            P_clock == sp.diag(1, 0) and matched * sp.Matrix([1, 0]) == sp.zeros(2, 1), checks)
    require("clock_screen_simple_spectrum_required",
            matched.subs(k2, -a**2) == sp.zeros(2) and (k2 + a**2).subs(k2, -a**2) == 0, checks)

    # Curvature candidate has a trace-free angular bulk channel; volume does not.
    r1, r2, r3 = sp.symbols("r1 r2 r3")
    scalar_r = r1 + r2 + r3
    Ric = sp.diag(r1, r2, r3)
    Htf = sp.diag(1, -1, 0)
    curvature_tf = sp.simplify(sp.trace((sp.Rational(1, 2) * scalar_r * sp.eye(3) - Ric) * Htf))
    require("curvature_candidate_tracefree_bulk_response", curvature_tf == -r1 + r2, checks)
    require("proper_volume_tracefree_bulk_blind", sp.trace(Htf) == 0, checks)
    ricci_control_1 = (1, 2, 3)
    ricci_control_2 = (0, 3, 3)
    response_1 = curvature_tf.subs({r1: ricci_control_1[0], r2: ricci_control_1[1], r3: ricci_control_1[2]})
    response_2 = curvature_tf.subs({r1: ricci_control_2[0], r2: ricci_control_2[1], r3: ricci_control_2[2]})
    require("same_ricci_trace_counterfamily",
            sum(ricci_control_1) == sum(ricci_control_2) == 6, checks)
    require("same_ricci_trace_different_tracefree_response",
            response_1 == 1 and response_2 == 3, checks)

    # Density and moving finite-cell volume response.
    M, V, dM, dV, rho = sp.symbols("M V dM dV rho", nonzero=True)
    density_variation = sp.simplify((dM - (M / V) * dV) / V)
    require("density_variation_exact",
            density_variation == (V * dM - M * dV) / V**2, checks)
    area, length, darea, dlength = sp.symbols("area length delta_area delta_length")
    moving_volume = sp.expand(area * dlength + length * darea)
    require("moving_boundary_volume_has_shape_channel",
            moving_volume.coeff(dlength) == area and moving_volume.coeff(darea) == length, checks)

    # Local transport does not imply a globally descending fixed vector.
    theta = sp.symbols("theta", real=True)
    holonomy = sp.Matrix([[sp.cos(theta), -sp.sin(theta)], [sp.sin(theta), sp.cos(theta)]])
    fixed_determinant = sp.trigsimp((holonomy - sp.eye(2)).det())
    require("holonomy_fixed_vector_condition",
            sp.trigsimp(fixed_determinant - 4 * sp.sin(theta / 2)**2) == 0, checks)
    require("local_transport_not_global_fixed_section",
            (holonomy - sp.eye(2)).subs(theta, sp.pi / 2).det() == 2, checks)

    # The full toric module can descend while an individual character is exchanged.
    exchange = sp.Matrix([[0, 1], [1, 0]])
    e1, e2 = sp.Matrix([1, 0]), sp.Matrix([0, 1])
    require("toric_exchange_preserves_module_not_line",
            abs(exchange.det()) == 1 and exchange * e1 == e2 and exchange * e1 != e1, checks)

    # Mutual vector closure does not require scalar extremization.
    u, v = sp.symbols("u v")
    vector_closure = sp.Matrix([u + 2 * v, 3 * u + 4 * v])
    vector_jacobian = vector_closure.jacobian([u, v])
    require("vector_tuning_closure_full_rank_nongradient",
            vector_jacobian.det() == -2
            and sp.diff(vector_closure[0], v) == 2
            and sp.diff(vector_closure[1], u) == 3,
            checks)

    # c and G are calibration anchors, not enough to select a length or density.
    ac, bg = sp.symbols("a_c b_G")
    length_solution = sp.solve(
        [sp.Eq(ac + 3 * bg, 1), sp.Eq(-bg, 0), sp.Eq(-ac - 2 * bg, 0)],
        [ac, bg], dict=True,
    )
    density_solution = sp.solve(
        [sp.Eq(ac + 3 * bg, -3), sp.Eq(-bg, 1), sp.Eq(-ac - 2 * bg, 0)],
        [ac, bg], dict=True,
    )
    require("c_G_do_not_select_length", length_solution == [], checks)
    require("c_G_do_not_select_density", density_solution == [], checks)

    result = {
        "schema": "udt-metric-native-nontriviality-connector-algebra-1.0",
        "sympy_version": sp.__version__,
        "check_count": len(checks),
        "checks": checks,
        "exact_objects": {
            "coupled_linearization": "[[A_X,A_O],[-R_X,I]]",
            "reduced_tuning_operator": str(S),
            "matrix_schur_control": [[str(item) for item in row] for row in schur.tolist()],
            "singular_kernel_control": [str(item) for item in kernel],
            "regular_reduced_root": str(reduced_regular),
            "singular_reduced_root": str(reduced_singular),
            "isolated_quadratic_control": str(isolated_quadratic),
            "crossing_quadratic_control": str(crossing_quadratic),
            "clock_tidal_determinant": str(sp.factor(clock_tidal.det())),
            "clock_projector": [[str(item) for item in row] for row in P_clock.tolist()],
            "curvature_TF_response": str(curvature_tf),
            "same_ricci_trace_response_pair": [str(response_1), str(response_2)],
            "density_variation": str(density_variation),
            "moving_volume_variation": str(moving_volume),
            "holonomy_fixed_determinant": str(fixed_determinant),
        },
        "structural_rulings": {
            "two_arrow_nontriviality": "KERNEL_OF_A_X_PLUS_A_O_R_X_IS_EXACT_NECESSARY_INFINITESIMAL_CONDITION",
            "feedback": "GLOBAL_LOCAL_FEEDBACK_CAN_CREATE_OR_REMOVE_AN_INFINITESIMAL_KERNEL",
            "kernel_scope": "KERNEL_IS_NOT_MATTER_WITHOUT_GAUGE_BOUNDARY_DESCENT_AND_NONLINEAR_CONTINUATION",
            "root_scope": "REALIZED_ROOT_DOES_NOT_SELECT_REGULAR_OR_SINGULAR_LINEARIZATION",
            "clock_curvature": "EXACT_LOCAL_KERNEL_CANDIDATE_WITH_GLOBAL_BRANCH_AND_FEEDBACK_OPEN",
            "curvature": "TRACEFREE_LOCAL_AND_GLOBAL_INTEGRAL_CANDIDATE_NOT_SELECTED_CLOSURE",
            "scalar_bootstrap_insufficiency": "DENSITY_AND_SCALAR_CURVATURE_TRACE_DO_NOT_DETERMINE_POINTWISE_TRACEFREE_RICCI_RESPONSE",
            "density": "VOLUME_CHANNEL_TRACE_ONLY_AND_NATIVE_MASS_RESPONSE_MISSING",
            "holonomy": "LOCAL_TRANSPORT_DOES_NOT_IMPLY_GLOBAL_DESCENDING_SECTION",
            "minimum_missing_object": "COMPLETE_SAME_BRANCH_A_AND_R_MAPS_WITH_GAUGE_BOUNDARY_DESCENT_AND_NONLINEAR_DOMAIN",
        },
    }
    (HERE / "ALGEBRA_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
