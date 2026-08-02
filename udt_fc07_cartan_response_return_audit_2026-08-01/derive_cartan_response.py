#!/usr/bin/env python3
"""Exact Cartan, curvature, projector-response, and Hodge-return audit for FC07."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
HALF = sp.Rational(1, 2)
MATRICES = (
    ("W01", "M_IDENTITY", sp.eye(2), "ORIENTABLE"),
    ("W02", "M_MINUS_IDENTITY", -sp.eye(2), "ORIENTABLE"),
    ("W03", "M_ORDER4_ROTATION", sp.Matrix([[0, -1], [1, 0]]), "ORIENTABLE"),
    ("W04", "M_ORDER6_ELLIPTIC", sp.Matrix([[0, -1], [1, 1]]), "ORIENTABLE"),
    ("W05", "M_PARABOLIC", sp.Matrix([[1, 1], [0, 1]]), "ORIENTABLE"),
    ("W06", "M_HYPERBOLIC", sp.Matrix([[2, 1], [1, 1]]), "ORIENTABLE"),
    ("W07", "M_EXCHANGE", sp.Matrix([[0, 1], [1, 0]]), "NONORIENTABLE"),
    ("W08", "M_ORIENTATION_REVERSING_GLIDE", sp.Matrix([[1, 1], [0, -1]]), "NONORIENTABLE"),
)
FORCED = {"M_PARABOLIC", "M_HYPERBOLIC"}


def simp(value: sp.Expr | sp.MatrixBase) -> sp.Expr | sp.MatrixBase:
    return value.applyfunc(sp.factor) if isinstance(value, sp.MatrixBase) else sp.factor(value)


def zero(value: sp.Expr | sp.MatrixBase) -> bool:
    if isinstance(value, sp.MatrixBase):
        return all(sp.simplify(item) == 0 for item in value)
    return sp.simplify(value) == 0


def write_tsv(name: str, rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def serial(value: object) -> object:
    if isinstance(value, sp.MatrixBase):
        return [[str(sp.factor(value[i, j])) for j in range(value.cols)] for i in range(value.rows)]
    if isinstance(value, sp.Basic):
        return str(sp.factor(value))
    if isinstance(value, dict):
        return {str(key): serial(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(item) for item in value]
    return value


def general_coordinate_algebra(checks: dict[str, str]) -> dict[str, object]:
    h11, h12, h22 = sp.symbols("h11 h12 h22", real=True)
    d11, d12, d22 = sp.symbols("d11 d12 d22", real=True)
    e11, e12, e22 = sp.symbols("e11 e12 e22", real=True)
    H = sp.Matrix([[h11, h12], [h12, h22]])
    D = sp.Matrix([[d11, d12], [d12, d22]])
    E = sp.Matrix([[e11, e12], [e12, e22]])
    A = sp.simplify(H.inv() * D)
    K = sp.simplify(A / 2)
    Kdot = sp.simplify(H.inv() * E / 2 - A * A / 2)
    T = sp.simplify(Kdot + K * K)
    radial_lower = sp.simplify(-H * T)
    second_fundamental = D / 2
    tangent_component = sp.factor(-(d11 * d22 - d12**2) / 4)
    ric_rr = sp.factor(-sp.trace(T))
    ric_screen_endomorphism = sp.simplify(-(Kdot + sp.trace(K) * K))
    scalar = sp.factor(-2 * sp.trace(Kdot) - sp.trace(K * K) - sp.trace(K) ** 2)

    # Independent component construction in the coordinate basis (r,y1,y2).
    g = sp.diag(1, 1, 1)
    g[1:3, 1:3] = H
    ginv = sp.simplify(g.inv())
    dg = [sp.zeros(3), sp.zeros(3), sp.zeros(3)]
    dg[0][1:3, 1:3] = D
    gamma = [[[sp.Integer(0) for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for upper in range(3):
        for left in range(3):
            for right in range(3):
                gamma[upper][left][right] = sp.simplify(
                    sum(
                        ginv[upper, q]
                        * (dg[left][q, right] + dg[right][q, left] - dg[q][left, right])
                        / 2
                        for q in range(3)
                    )
                )

    derivative_map = {h11: d11, h12: d12, h22: d22, d11: e11, d12: e12, d22: e22}

    def dr(expr: sp.Expr) -> sp.Expr:
        return sp.simplify(sum(sp.diff(expr, symbol) * value for symbol, value in derivative_map.items()))

    riemann_up = [[[[sp.Integer(0) for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
    for upper in range(3):
        for acted in range(3):
            for left in range(3):
                for right in range(3):
                    derivative = (dr(gamma[upper][right][acted]) if left == 0 else 0) - (
                        dr(gamma[upper][left][acted]) if right == 0 else 0
                    )
                    products = sum(
                        gamma[upper][left][mid] * gamma[mid][right][acted]
                        - gamma[upper][right][mid] * gamma[mid][left][acted]
                        for mid in range(3)
                    )
                    riemann_up[upper][acted][left][right] = sp.simplify(derivative + products)

    def rlower(first: int, acted: int, left: int, right: int) -> sp.Expr:
        return sp.simplify(sum(g[first, upper] * riemann_up[upper][acted][left][right] for upper in range(3)))

    radial_direct = sp.Matrix(2, 2, lambda i, j: rlower(0, i + 1, 0, j + 1))
    assert zero(radial_direct - radial_lower)
    checks["coordinate_radial_Riemann_equals_matrix_formula"] = "PASS"
    assert zero(rlower(1, 2, 1, 2) - tangent_component)
    checks["coordinate_tangent_Riemann_equals_Gauss_formula"] = "PASS"
    mixed = [rlower(0, a, b, c) for a in (1, 2) for b in (1, 2) for c in (1, 2)]
    assert all(zero(item) for item in mixed)
    checks["all_radial_screen_mixed_Riemann_components_zero"] = "PASS"
    ricci_direct = sp.Matrix(
        3,
        3,
        lambda acted, right: sp.simplify(
            sum(riemann_up[upper][acted][upper][right] for upper in range(3))
        ),
    )
    expected_ricci = sp.zeros(3)
    expected_ricci[0, 0] = ric_rr
    expected_ricci[1:3, 1:3] = sp.simplify(H * ric_screen_endomorphism)
    assert zero(ricci_direct - expected_ricci)
    checks["coordinate_Ricci_equals_matrix_formula"] = "PASS"
    assert zero(sp.simplify(sum(ginv[i, j] * ricci_direct[i, j] for i in range(3) for j in range(3))) - scalar)
    checks["coordinate_scalar_equals_matrix_formula"] = "PASS"

    # Orthonormal Cartan connection and full rank-one response.
    s11, s12, s22, omega = sp.symbols("s11 s12 s22 omega", real=True)
    S = sp.Matrix([[s11, s12], [s12, s22]])
    W = sp.Matrix([[0, -omega], [omega, 0]])
    connection = [sp.zeros(3) for _ in range(3)]
    connection[0][1:3, 1:3] = -W
    for direction in range(2):
        for screen in range(2):
            connection[direction + 1][screen + 1, 0] = S[screen, direction]
            connection[direction + 1][0, screen + 1] = -S[screen, direction]
    assert all(zero(matrix + matrix.T) for matrix in connection)
    checks["Cartan_connection_metric_skew"] = "PASS"
    P = sp.diag(1, 0, 0)
    Q = sp.eye(3) - P
    DP = [sp.simplify(matrix * P - P * matrix) for matrix in connection]
    response = sp.simplify(Q * (DP[1] * DP[2] - DP[2] * DP[1]) * Q)
    assert zero(DP[0])
    assert zero(response[1:3, 1:3] - sp.det(S) * sp.Matrix([[0, 1], [-1, 0]]))
    checks["full_projector_response_equals_det_shape_operator"] = "PASS"
    checks["base_direction_projector_derivative_zero"] = "PASS"
    assert zero(sp.det(K) - sp.det(D) / (4 * sp.det(H)))
    checks["coordinate_response_scalar_equals_detD_over_four_detH"] = "PASS"
    reflection = sp.diag(-1, 1)
    assert zero(sp.det(reflection * S * reflection) - sp.det(S))
    checks["response_scalar_reflection_invariant"] = "PASS"
    radius = sp.symbols("r", real=True)
    constant = sp.symbols("C", real=True)
    volume_factor = sp.Function("J", positive=True)(radius)
    harmonic_coefficient = constant / volume_factor
    assert sp.simplify(sp.diff(volume_factor * harmonic_coefficient, radius)) == 0
    checks["base_form_coclosed_when_sqrt_detH_times_coefficient_constant"] = "PASS"

    return {
        "screen_metric": H,
        "screen_first_jet": D,
        "screen_second_jet": E,
        "shape_operator_K": K,
        "shape_derivative_Kdot": Kdot,
        "radial_tidal_operator_T": T,
        "radial_Riemann_lower": radial_lower,
        "tangent_Riemann_component": tangent_component,
        "Ricci_rr": ric_rr,
        "Ricci_screen_endomorphism": ric_screen_endomorphism,
        "scalar_curvature": scalar,
        "orthonormal_screen_shape_S": S,
        "orthonormal_screen_gauge_W": W,
        "relative_projector_curvature": response,
        "relative_projector_scalar": sp.det(S),
    }


def monodromy_algebra(checks: dict[str, str]) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    a, b, d = sp.symbols("a b d", real=True)
    H = sp.Matrix([[a, b], [b, d]])
    H0 = sp.Matrix([[sp.Rational(2), sp.Rational(1, 3)], [sp.Rational(1, 3), sp.Rational(5)]])
    response_rows: list[dict[str, object]] = []
    hodge_rows: list[dict[str, object]] = []
    selection_rows: list[dict[str, object]] = []
    holonomy_rows: list[dict[str, object]] = []
    varying_generic = 0
    unique_h1 = 0
    forced_nonidentity = 0
    constant_unique_pair_planes = 0
    for wid, name, M, orientation in MATRICES:
        H1 = sp.simplify(M.T * H * M)
        Delta = sp.simplify(H1 - H)
        det_delta = sp.factor(Delta.det())
        normalized_endpoint = sp.simplify(H.inv() * H1)
        assert zero(det_delta - sp.det(H) * (2 - sp.trace(normalized_endpoint)))
        checks[f"{wid}_unimodular_endpoint_detDelta_identity"] = "PASS"
        fixed_dim = 3 - sp.linear_eq_to_matrix(list(Delta), (a, b, d))[0].rank()
        ker_one = 2 - (M.T - sp.eye(2)).rank()
        ker_vector_one = 2 - (M - sp.eye(2)).rank()
        assert ker_vector_one == ker_one
        b1 = 1 + ker_one
        generic_H1 = M.T * H0 * M
        generic_delta = sp.simplify(generic_H1 - H0)
        generic_mid = sp.simplify((H0 + generic_H1) / 2)
        # At the flat-step midpoint chi'=2/ell. Set ell=1, so K=H_mid^-1 Delta.
        Kmid = sp.simplify(generic_mid.inv() * generic_delta)
        det_k = sp.factor(Kmid.det())
        trace_k = sp.factor(sp.trace(Kmid))
        assert zero(trace_k)
        assert zero(Kmid * Kmid + det_k * sp.eye(2))
        checks[f"{wid}_symmetric_midpoint_shape_traceless"] = "PASS"
        checks[f"{wid}_symmetric_midpoint_shape_square_is_scalar"] = "PASS"
        for basis_index, basis in enumerate((sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[1, 1], [0, 1]])), start=1):
            transformed_M = basis.inv() * M * basis
            transformed_H0 = basis.T * H0 * basis
            transformed_H1 = transformed_M.T * transformed_H0 * transformed_M
            transformed_mid = (transformed_H0 + transformed_H1) / 2
            transformed_K = sp.simplify(transformed_mid.inv() * (transformed_H1 - transformed_H0))
            assert zero(transformed_K - basis.inv() * Kmid * basis)
            assert zero(sp.det(transformed_K) - det_k)
            checks[f"{wid}_basis_{basis_index}_shape_conjugacy_and_response_invariance"] = "PASS"
        response = "ZERO_CONSTANT_CONTROL" if zero(generic_delta) else "NONZERO_EVERY_INTERIOR_POINT_GENERIC_CONTROL"
        if not zero(generic_delta):
            varying_generic += 1
            assert det_k < 0
            checks[f"{wid}_generic_endpoint_change_has_negative_detDelta"] = "PASS"
            checks[f"{wid}_midpoint_spatial_curvature_operator_invertible"] = "PASS"
        else:
            checks[f"{wid}_generic_constant_screen_zero_shape"] = "PASS"
        spatial_curvature_det = sp.factor(-det_k**3)
        scalar_mid = sp.factor(2 * (sp.trace(Kmid * Kmid) - det_k))
        forced = name in FORCED
        if forced:
            forced_nonidentity += 1
        h1_unique = b1 == 1
        unique_h1 += int(h1_unique)
        if h1_unique and not zero(generic_delta):
            projector_class = "METRIC_INTRINSIC_GLOBAL_ON_REGISTERED_PRODUCT"
            reason = "CURVATURE_NULLITY_SELECTS_CLOCK_AT_MIDPOINT_AND_UNIQUE_HARMONIC_H1_SELECTS_RULER_GLOBALLY"
        elif h1_unique:
            projector_class = "METRIC_INTRINSIC_SET_VALUED_OR_DEGENERATE"
            reason = "UNIQUE_SPATIAL_HARMONIC_CLASS_BUT_FLAT_FULL_METRIC_RETAINS_OBSERVER_RECIPROCAL_PLANE_NOT_UNIQUE_CLOCK_AXIS"
        elif not zero(generic_delta):
            projector_class = "BUNDLE_RELATIVE_CONDITIONAL"
            reason = "CLOCK_CERTIFIED_BY_CURVATURE_BUT_HARMONIC_H1_DIMENSION_EXCEEDS_ONE"
        else:
            projector_class = "NOT_AVAILABLE"
            reason = "FLAT_IDENTITY_CONTROL_AND_HARMONIC_H1_DIMENSION_EXCEEDS_ONE"
        response_rows.append(
            {
                "candidate_id": wid,
                "monodromy_id": name,
                "det_M": int(M.det()),
                "orientation": orientation,
                "b1_mapping_torus": b1,
                "symmetric_fixed_dimension": fixed_dim,
                "det_Delta_symbolic": str(det_delta),
                "generic_det_K_mid_ell2": str(det_k),
                "generic_tr_K_mid_ell": str(trace_k),
                "generic_spatial_curvature_operator_det_ell6": str(spatial_curvature_det),
                "generic_scalar_curvature_mid_ell2": str(scalar_mid),
                "generic_midpoint_spatial_curvature_pattern": "ZERO_FLAT" if zero(generic_delta) else "ISOTROPIC_POSITIVE_ALL_THREE_SECTIONAL_CURVATURES_EQUAL_MINUS_detK",
                "screen_response": response,
                "variation_scope": "FORCED_ALL_SPD" if forced else ("ZERO_ALL_SPD" if name in {"M_IDENTITY", "M_MINUS_IDENTITY"} else "OPTIONAL_FIXED_SUBFAMILY_EXISTS"),
                "intrinsic_projector_class": projector_class,
                "intrinsic_reason": reason,
                "physical_selection": "NONE",
            }
        )
        hodge_rows.append(
            {
                "candidate_id": wid,
                "monodromy_id": name,
                "ker_Mt_minus_I": ker_one,
                "b1": b1,
                "unique_harmonic_line": "YES" if h1_unique else "NO_HARMONIC_SPACE_DIMENSION_GT_1",
                "unit_period_base_form": "alpha=dr/(I_h*sqrt(det(h(r))));I_h=int_cell dr/sqrt(det(h(r)))",
                "local_depends_on_global_integral": "YES_IF_BASE_CLASS_SELECTED",
                "selection_status": "INTRINSIC_UNIQUE_CLASS" if h1_unique else "FIBRATION_CLASS_REQUIRED",
                "channel_type": "NONIDENTITY_FOR_VARYING_h" if not zero(generic_delta) else "IDENTITY_CONSTANT_CONTROL",
                "bootstrap_status": "GEOMETRIC_GLOBAL_TO_LOCAL_CHANNEL_NOT_BOOTSTRAP_CLOSURE" if h1_unique else "SET_VALUED_OR_BUNDLE_RELATIVE_CHANNEL",
            }
        )
        constant_exists = name not in FORCED
        full_fixed_dimension = 2 + ker_vector_one
        if constant_exists and full_fixed_dimension == 2:
            holonomy_ruling = "UNIQUE_HOLONOMY_FIXED_LORENTZIAN_RECIPROCAL_TWO_PLANE"
            axis_ruling = "NO_UNIQUE_CLOCK_RULER_AXES_OBSERVER_FRAME_FAMILY_RETAINED"
            constant_unique_pair_planes += 1
        elif constant_exists and full_fixed_dimension == 3:
            holonomy_ruling = "FIXED_THREE_SPACE_NO_UNIQUE_RECIPROCAL_TWO_PLANE"
            axis_ruling = "NO_UNIQUE_AXES"
        elif constant_exists:
            holonomy_ruling = "TRIVIAL_HOLONOMY_NO_PROPER_PLANE_SELECTION"
            axis_ruling = "NO_UNIQUE_AXES"
        else:
            holonomy_ruling = "NO_CONSTANT_POSITIVE_SCREEN_SUBFAMILY"
            axis_ruling = "NOT_APPLICABLE"
        holonomy_rows.append(
            {
                "candidate_id": wid,
                "monodromy_id": name,
                "constant_positive_screen_subfamily": "YES" if constant_exists else "NO",
                "screen_fixed_vector_dimension": ker_vector_one,
                "full_spacetime_holonomy_fixed_dimension": full_fixed_dimension if constant_exists else "NOT_APPLICABLE",
                "holonomy_ruling": holonomy_ruling,
                "axis_ruling": axis_ruling,
                "relative_response": "ZERO_CONSTANT_SCREEN",
                "physical_observer_selection": "NONE",
            }
        )
        selection_rows.extend(
            [
                {
                    "candidate_id": wid,
                    "object": "timelike_clock_line",
                    "classification": "METRIC_INTRINSIC_GLOBAL" if not zero(generic_delta) else "METRIC_INTRINSIC_SET_VALUED_OR_DEGENERATE",
                    "gate": "spatial_curvature_operator_invertible_at_midpoint_then_parallel_continuation" if not zero(generic_delta) else "flat_holonomy_control",
                },
                {
                    "candidate_id": wid,
                    "object": "spacelike_ruler_projector",
                    "classification": projector_class,
                    "gate": reason,
                },
                {
                    "candidate_id": wid,
                    "object": "relative_projector_response",
                    "classification": (
                        "NONZERO_SOMEWHERE_STRATIFIED" if h1_unique and not zero(generic_delta)
                        else ("ZERO_RESPONSE_CONTROL" if zero(generic_delta) else "UNDEFINED_SELECTION_GATE_FAILED")
                    ),
                    "gate": "det(K)=chi_prime^2*det(Delta)/(4*ell^2*det(h))",
                },
            ]
        )
    assert varying_generic == 6
    assert unique_h1 == 4
    assert forced_nonidentity == 2
    assert constant_unique_pair_planes == 3
    checks["generic_varying_witness_count_six"] = "PASS"
    checks["unique_H1_completion_count_four"] = "PASS"
    checks["forced_varying_completion_count_two"] = "PASS"
    checks["constant_subfamily_unique_reciprocal_pair_plane_count_three"] = "PASS"
    return response_rows, hodge_rows, selection_rows, holonomy_rows


def main() -> int:
    checks: dict[str, str] = {}
    general = general_coordinate_algebra(checks)
    response_rows, hodge_rows, selection_rows, holonomy_rows = monodromy_algebra(checks)
    write_tsv("MONODROMY_CARTAN_RESPONSE_ATLAS.tsv", response_rows)
    write_tsv("HODGE_RETURN_CHANNEL.tsv", hodge_rows)
    write_tsv("INTRINSIC_SELECTION_ATLAS.tsv", selection_rows)
    write_tsv("CONSTANT_SCREEN_HOLONOMY_ATLAS.tsv", holonomy_rows)
    xmax_rows = [
        {
            "gate": "c_E_scale",
            "input": "measured_c_E",
            "derived_here": "constant_timelike_calibration_only",
            "ruling": "DOES_NOT_CREATE_DISTANCE_ASYMPTOTE",
        },
        {
            "gate": "proper_base_scale",
            "input": "ell=L*exp(phi0)",
            "derived_here": "free_witness_circumference",
            "ruling": "CHOSE_NOT_XMAX",
        },
        {
            "gate": "observer_pair_dilation",
            "input": "phi=phi0_constant",
            "derived_here": "no_position_dependent_clock_ratio",
            "ruling": "XMAX_ENDPOINT_NOT_AVAILABLE_IN_THIS_BOUNDED_FAMILY",
        },
        {
            "gate": "Hodge_capacity",
            "input": "I_h=int_cell_dr/sqrt(det(h))",
            "derived_here": "completion_dependent_global_modulus_and_local_harmonic_amplitude",
            "ruling": "POSSIBLE_FUTURE_INPUT_NOT_OBSERVER_PAIR_ENDPOINT",
        },
        {
            "gate": "bootstrap",
            "input": "harmonic_global_to_local_map",
            "derived_here": "nonidentity_geometric_channel_on_varying_unique_H1_strata",
            "ruling": "NO_NATIVE_EQUATION_FEEDBACK_OR_SAME_SOLUTION_CLOSURE",
        },
    ]
    write_tsv("XMAX_AND_BOOTSTRAP_TYPE_GATE.tsv", xmax_rows)
    (HERE / "GENERAL_CARTAN_FORMULAS.json").write_text(
        json.dumps(serial(general), indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    maximum = (
        "FC07_FULL_SCREEN_CARTAN_AND_CURVATURE_DERIVED__ALL_NONCONSTANT_REGISTERED_INTERPOLATIONS_HAVE_"
        "NONZERO_BUNDLE_RELATIVE_PROJECTOR_RESPONSE__THREE_VARYING_UNIQUE_H1_CLASSES_HAVE_A_METRIC_"
        "INTRINSIC_GLOBAL_HARMONIC_RULER_CHANNEL__ONE_FORCED_HYPERBOLIC_INSTANCE__THREE_CONSTANT_"
        "SUBFAMILIES_HAVE_A_HOLONOMY_FIXED_RECIPROCAL_PLANE_WITHOUT_SELECTED_AXES__NO_UNIVERSAL_"
        "PROJECTOR_BOOTSTRAP_CLOSURE_XMAX_SELECTION_DYNAMICS_OR_MATTER"
    )
    result = {
        "schema": "udt.fc07_cartan_response_return.derivation.v1",
        "status": "PASS",
        "sympy_version": sp.__version__,
        "exact_checks": len(checks),
        "checks": checks,
        "monodromy_controls": 8,
        "generic_varying_controls": 6,
        "generic_constant_controls": 2,
        "unique_H1_completions": 4,
        "varying_unique_H1_intrinsic_ruler_channels": 3,
        "constant_subfamily_unique_reciprocal_pair_planes": 3,
        "forced_varying_unique_H1_channels": ["M_HYPERBOLIC"],
        "forced_varying_ambiguous_H1_channels": ["M_PARABOLIC"],
        "universal_metric_ruler_projector": False,
        "native_bootstrap_return": False,
        "Xmax_derived": False,
        "physical_selection": False,
        "maximum_conclusion": maximum,
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
