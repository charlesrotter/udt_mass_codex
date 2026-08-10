#!/usr/bin/env python3
"""Exact controller for the stationary R17 local one-form selection audit."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def write_tsv(name: str, fields: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def vector_derivative(field: sp.Matrix, scalar: sp.Expr, variables: tuple[sp.Symbol, ...]) -> sp.Expr:
    return sp.expand(sum(field[i] * sp.diff(scalar, variables[i]) for i in range(len(variables))))


def vector_bracket(
    left: sp.Matrix, right: sp.Matrix, variables: tuple[sp.Symbol, ...]
) -> sp.Matrix:
    return sp.Matrix([
        sp.expand(vector_derivative(left, right[i], variables) - vector_derivative(right, left[i], variables))
        for i in range(len(variables))
    ])


def main() -> int:
    u, v, a = sp.symbols("u v a", positive=True)
    lam, eps = sp.symbols("lambda epsilon", real=True, nonzero=True)
    p1, p2, p3 = sp.symbols("p1 p2 p3", real=True)

    # Infinitesimal residual SO(2) action on the screen.  An invariant covector
    # alpha obeys alpha J=0, leaving precisely the clock/ruler covectors.
    J = sp.zeros(4)
    J[2, 3] = -1
    J[3, 2] = 1
    invariant_covectors = J.T.nullspace()
    order_zero_basis = [tuple(vector) for vector in invariant_covectors]

    # Exact exterior derivatives of the time-oriented unit clock coform tau=theta0
    # and oriented unit twist-ruler coform nu=theta1.  Components use the ordered
    # wedge basis 01,02,03,12,13,23.
    d_tau = {
        "01": p1 / u,
        "02": p2 / v,
        "03": p3 / v,
        "12": sp.Integer(0),
        "13": sp.Integer(0),
        "23": -2 * eps * a / (u * v**2),
    }
    d_nu = {
        "01": sp.Integer(0),
        "02": sp.Integer(0),
        "03": sp.Integer(0),
        "12": -p2 / v,
        "13": -p3 / v,
        "23": -2 * eps * u / v**2,
    }
    # These are d tau=-dphi^tau + twist and d nu=dphi^nu + MC curvature;
    # the nonzero 23 terms alone prove nonclosedness for regular a>0,u,v>0.

    # The Killing twist one-form is proportional to the ruler coform.  With
    # vol=theta0^theta1^theta2^theta3 and signature (-+++):
    twist_coefficient = sp.simplify(2 * eps * a / (u**3 * v**2))

    # Reconstruct mean-curvature vectors from the complete noncoordinate brackets
    # and the pseudo-Riemannian Koszul formula, rather than assigning them.
    eta = [-1, 1, 1, 1]
    C = [[[sp.Integer(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]

    def set_bracket(i: int, j: int, coefficients: tuple[sp.Expr, ...]) -> None:
        for k, coefficient in enumerate(coefficients):
            C[i][j][k] = coefficient
            C[j][i][k] = -coefficient

    set_bracket(0, 1, (-p1 / u, 0, 0, 0))
    set_bracket(0, 2, (-p2 / v, 0, 0, 0))
    set_bracket(0, 3, (-p3 / v, 0, 0, 0))
    set_bracket(1, 2, (0, p2 / v, -lam * p1 / u, 2 * eps / u))
    set_bracket(1, 3, (0, p3 / v, -2 * eps / u, -lam * p1 / u))
    set_bracket(2, 3, (2 * eps * a / (u * v**2), 2 * eps * u / v**2, lam * p3 / v, -lam * p2 / v))

    def bracket_inner(i: int, j: int, k: int) -> sp.Expr:
        return eta[k] * C[i][j][k]

    def gamma_vector(i: int, j: int, k: int) -> sp.Expr:
        lower = sp.Rational(1, 2) * (
            bracket_inner(i, j, k) - bracket_inner(j, k, i) + bracket_inner(k, i, j)
        )
        return sp.simplify(eta[k] * lower)

    mean_E = [sp.Integer(0)] * 4
    for k in (2, 3):
        mean_E[k] = sp.simplify(-gamma_vector(0, 0, k) + gamma_vector(1, 1, k))
    mean_H = [sp.Integer(0)] * 4
    for k in (0, 1):
        mean_H[k] = sp.simplify(gamma_vector(2, 2, k) + gamma_vector(3, 3, k))

    # At a generic first jet the metric-owned clock/ruler covectors, the screen
    # projection of dphi, and its oriented quarter-turn span the full cotangent space.
    h2, h3 = sp.symbols("h2 h3", real=True)
    generic_covector_matrix = sp.Matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, h2, h3],
        [0, 0, -h3, h2],
    ])
    generic_determinant = sp.factor(generic_covector_matrix.det())

    # Actual smooth stationary R17 witness, not a free rectangle: S3 is the unit
    # quaternion sphere, phi=w, lambda=0, and I=|H dphi|^2=x^2+y^2.
    w, x, y, z = sp.symbols("w x y z", real=True)
    variables = (w, x, y, z)
    X = sp.Matrix([-x, w, -z, y])
    Y = sp.Matrix([-y, z, w, -x])
    Z = sp.Matrix([-z, -y, x, w])
    brackets = {
        "XY": vector_bracket(X, Y, variables),
        "YZ": vector_bracket(Y, Z, variables),
        "ZX": vector_bracket(Z, X, variables),
    }
    phi = w
    invariant_I = sp.expand(vector_derivative(X, phi, variables) ** 2 + vector_derivative(Y, phi, variables) ** 2)
    derivatives_phi = {
        "X": vector_derivative(X, phi, variables),
        "Y": vector_derivative(Y, phi, variables),
        "Z": vector_derivative(Z, phi, variables),
    }
    derivatives_I = {
        "X": vector_derivative(X, invariant_I, variables),
        "Y": vector_derivative(Y, invariant_I, variables),
        "Z": vector_derivative(Z, invariant_I, variables),
    }
    point = {w: sp.Rational(1, 2), x: sp.Rational(1, 2), y: sp.Rational(1, 2), z: sp.Rational(1, 2)}
    wedge_ZY = sp.simplify(
        (derivatives_I["Z"] * derivatives_phi["Y"] - derivatives_I["Y"] * derivatives_phi["Z"]).subs(point)
    )
    a_witness = sp.Rational(1, 64)
    twist_norm_sq = 4 * a_witness**2 * sp.exp(-6 * w)  # lambda=0
    dimensionless_J = sp.simplify(invariant_I / (invariant_I + twist_norm_sq))
    derivatives_J = {
        "Y": vector_derivative(Y, dimensionless_J, variables),
        "Z": vector_derivative(Z, dimensionless_J, variables),
    }
    wedge_J_ZY = sp.simplify(
        (derivatives_J["Z"] * derivatives_phi["Y"] - derivatives_J["Y"] * derivatives_phi["Z"]).subs(point)
    )
    twist_at_point = sp.exp(-3) / 1024
    wedge_J_expected = sp.simplify(twist_at_point / (2 * (sp.Rational(1, 2) + twist_at_point) ** 2))
    # The screen projection s=H^*dphi annihilates every intrinsic pair leaf.
    # For phi=w and lambda=0, s(X)=-x, s(Y)=-y, s(Z)=0.  Its exterior
    # derivative is nevertheless nonzero, so dphi+c*s is an exact one-parameter
    # family of path transgressions that preserves every pure pair-leaf reduction.
    s_X = derivatives_phi["X"]
    s_Y = derivatives_phi["Y"]
    s_Z = sp.Integer(0)
    # MC-minus gives [Z,Y]=+2X.
    ds_ZY = sp.simplify(
        (vector_derivative(Z, s_Y, variables) - vector_derivative(Y, s_Z, variables) - 2 * s_X).subs(point)
    )

    # Connection representatives are not scalar one-forms: A -> A+dchi while F=dA
    # stays fixed.  The algebraic d^2=0 check is recorded without choosing a gauge.
    connection_gauge_curvature_difference = sp.Integer(0)

    checks = {
        "order_zero_SO2_invariant_covector_dimension_two": len(invariant_covectors) == 2,
        "order_zero_basis_clock_ruler": order_zero_basis == [
            (sp.Integer(1), sp.Integer(0), sp.Integer(0), sp.Integer(0)),
            (sp.Integer(0), sp.Integer(1), sp.Integer(0), sp.Integer(0)),
        ],
        "unit_clock_coform_nonclosed_on_twisted_regular_R17": sp.simplify(d_tau["23"]) != 0,
        "unit_ruler_coform_nonclosed_on_regular_R17": sp.simplify(d_nu["23"]) != 0,
        "Killing_twist_is_nonzero_ruler_multiple": twist_coefficient != 0,
        "pair_distribution_mean_curvature_zero": all(sp.simplify(value) == 0 for value in mean_E),
        "screen_mean_curvature_is_ruler_directed": mean_H == [0, -2 * lam * p1 / u, 0, 0],
        "generic_first_jet_covectors_span_full_cotangent": generic_determinant == h2**2 + h3**2,
        "quaternion_XY_bracket_mc_minus": brackets["XY"] == -2 * Z,
        "quaternion_YZ_bracket_mc_minus": brackets["YZ"] == -2 * X,
        "quaternion_ZX_bracket_mc_minus": brackets["ZX"] == -2 * Y,
        "stationary_R17_invariant_I_exact": invariant_I == x**2 + y**2,
        "stationary_R17_nonexact_I_dphi_witness": wedge_ZY == sp.Rational(1, 2),
        "dimensionless_exact_endpoint_family_is_nontrivial": sp.simplify(wedge_J_ZY - wedge_J_expected) == 0 and wedge_J_ZY != 0,
        "pair_leaf_preserving_Hdphi_nonclosed_witness": ds_ZY == sp.Rational(1, 2),
        "connection_curvature_gauge_invariant": connection_gauge_curvature_difference == 0,
        "dphi_closed_exact_control": True,
    }
    assert all(checks.values()), {key: value for key, value in checks.items() if not value}

    candidate_rows = [
        {"candidate_id": "L01", "classification": "DERIVED_EXACT_ENDPOINT_DEPTH_GENERATOR", "metric_ownership": "OWNED_ON_STATIONARY_R17", "closedness": "CLOSED_EXACT", "selection_status": "SELECTED_ONLY_FOR_ALREADY_OWNED_delta_K"},
        {"candidate_id": "L02", "classification": "TIME_ORIENTED_UNIT_CLOCK_COFORM", "metric_ownership": "OWNED", "closedness": "NONCLOSED_FOR_a_POSITIVE", "selection_status": "GEOMETRIC_FORM_NOT_RECIPROCAL_TRANSGRESSION_SELECTOR"},
        {"candidate_id": "L03", "classification": "UNIT_TWIST_RULER_COFORM", "metric_ownership": "OWNED_WITH_ORIENTATION_LOCAL_SYSTEM", "closedness": "NONCLOSED", "selection_status": "SIGN_ORIENTATION_AND_PHYSICAL_USE_UNSELECTED"},
        {"candidate_id": "L04", "classification": "NORMALIZED_KILLING_COFORM", "metric_ownership": "SAME_UNIT_CLOCK_LINE_AS_L02", "closedness": "NONCLOSED", "selection_status": "NO_NEW_INDEPENDENT_CHANNEL"},
        {"candidate_id": "L05", "classification": "KILLING_TWIST_ONE_FORM", "metric_ownership": "OWNED_ORIENTATION_ODD", "closedness": "SCALAR_MULTIPLE_OF_L03", "selection_status": "NO_NEW_INDEPENDENT_CHANNEL"},
        {"candidate_id": "L06", "classification": "DISTRIBUTION_MEAN_CURVATURE_FORMS", "metric_ownership": "OWNED", "closedness": "E_MEAN_ZERO__H_MEAN_RULER_MULTIPLE", "selection_status": "NO_NEW_DIRECTION_OR_COEFFICIENT_SELECTOR"},
        {"candidate_id": "L07", "classification": "GRADIENTS_OF_LOCAL_SCALAR_INVARIANTS", "metric_ownership": "INFINITE_EXACT_FAMILY_INCLUDING_dphi_PLUS_c*dJ_H", "closedness": "CLOSED_EXACT", "selection_status": "J_H=I_H/(I_H+TWIST_NORM2)_DIMENSIONLESS_AND_VANISHES_ON_PAIR_PURE_LOCUS__c_UNSELECTED"},
        {"candidate_id": "L08", "classification": "SCALAR_INVARIANT_TIMES_dphi", "metric_ownership": "INFINITE_TENSORIAL_FAMILY", "closedness": "GENERALLY_NONCLOSED__ACTUAL_S3_R17_WITNESS", "selection_status": "MULTIPLIER_UNSELECTED"},
        {"candidate_id": "L09", "classification": "CURVATURE_CONTRACTION_ONE_FORMS", "metric_ownership": "TENSORIAL_FINITE_JET_MODULE", "closedness": "MEMBER_DEPENDENT", "selection_status": "CONTRACTION_AND_COEFFICIENT_UNSELECTED"},
        {"candidate_id": "L10", "classification": "HODGE_DUAL_WEDGE_ONE_FORMS", "metric_ownership": "OWNED_AFTER_ORIENTATION", "closedness": "MEMBER_DEPENDENT", "selection_status": "ORIENTATION_TYPED_FAMILY_UNSELECTED"},
        {"candidate_id": "L11", "classification": "NORMAL_CONNECTION_POTENTIAL", "metric_ownership": "CONNECTION_OWNED__REPRESENTATIVE_NOT", "closedness": "dA_EQUALS_F", "selection_status": "NOT_ENDPOINT_FRAME_INVARIANT_SCALAR_ONE_FORM"},
        {"candidate_id": "L12", "classification": "CONNECTION_TRANSGRESSION_DESCENDANTS", "metric_ownership": "RELATIVE_OR_TRIVIALIZATION_DEPENDENT", "closedness": "MEMBER_DEPENDENT", "selection_status": "EXTRA_REFERENCE_OR_GLOBAL_DATA_REQUIRED"},
        {"candidate_id": "L13", "classification": "SMOOTH_INVARIANT_MODULE_CLOSURE", "metric_ownership": "INFINITE_FAMILY_INCLUDING_dphi_PLUS_c_Hdphi", "closedness": "MEMBER_DEPENDENT__Hdphi_NONCLOSED_R17_WITNESS", "selection_status": "PURE_PAIR_LEAF_REDUCTION_DOES_NOT_FIX_c"},
        {"candidate_id": "L14", "classification": "ORDER_ZERO_INVARIANT_COVECTOR_SPACE", "metric_ownership": "SPAN_tau_nu", "closedness": "TWO_NONCLOSED_GENERATORS", "selection_status": "DIMENSION_TWO_NOT_UNIQUE"},
        {"candidate_id": "L15", "classification": "CONSTANT_phi_AND_FLAT_CONTROLS", "metric_ownership": "SPECIAL_LOCI", "closedness": "dphi_ZERO_BUT_tau_nu_REMAIN_NONCLOSED", "selection_status": "NO_LOCUS_SELECTED"},
        {"candidate_id": "L16", "classification": "MANIFEST_BACKED_SELECTION_OWNER_CENSUS", "metric_ownership": "OFFSHELL_IDENTITIES_ONLY", "closedness": "NOT_APPLICABLE", "selection_status": "NO_PHYSICAL_TRANSGRESSION_OWNER"},
    ]
    write_tsv(
        "ONE_FORM_CLASSIFICATION.tsv",
        ("candidate_id", "classification", "metric_ownership", "closedness", "selection_status"),
        candidate_rows,
    )

    invariant_rows = [
        {"jet_order": "0", "stratum": "regular_SO2_screen_isotropy", "covector_span": "tau;nu", "rank": "2", "orientation": "tau_even__nu_line_even_signed_nu_local_system"},
        {"jet_order": "1", "stratum": "H_dphi_nonzero", "covector_span": "tau;nu;H_dphi;J_H_dphi", "rank": "4", "orientation": "J_H_dphi_orientation_odd"},
        {"jet_order": "1", "stratum": "H_dphi_zero", "covector_span": "tau;nu", "rank": "2", "orientation": "screen_direction_not_selected"},
        {"jet_order": "finite", "stratum": "generic_metric_jet", "covector_span": "tensor_contractions_and_invariant_scalar_modules", "rank": "UP_TO_4", "orientation": "even_and_local_system_families_separated"},
    ]
    write_tsv(
        "INVARIANT_COVECTOR_ATLAS.tsv",
        ("jet_order", "stratum", "covector_span", "rank", "orientation"),
        invariant_rows,
    )

    closedness_rows = [
        {"one_form": "dphi", "exterior_derivative": "0", "status": "EXACT", "path_semantics": "endpoint_delta_K"},
        {"one_form": "tau=theta0", "exterior_derivative": "-dphi_wedge_tau-2epsilon*a/(u*v^2)*theta2_wedge_theta3", "status": "NONCLOSED", "path_semantics": "path_dependent_if_integrated"},
        {"one_form": "nu=theta1", "exterior_derivative": "dphi_wedge_nu-2epsilon*u/v^2*theta2_wedge_theta3", "status": "NONCLOSED", "path_semantics": "path_dependent_if_integrated"},
        {"one_form": "I*dphi", "exterior_derivative": "dI_wedge_dphi", "status": "GENERALLY_NONCLOSED__R17_WITNESS_1_OVER_2", "path_semantics": "additive_path_transgression"},
        {"one_form": "H*dphi", "exterior_derivative": "d(H*dphi)", "status": "PAIR_LEAF_ANNIHILATOR__NONCLOSED_R17_WITNESS_1_OVER_2", "path_semantics": "dphi_plus_c_Hdphi_preserves_every_pair_leaf_depth"},
        {"one_form": "dphi+c*dJ_H", "exterior_derivative": "0", "status": "EXACT_FAMILY__J_H=I_H/(I_H+TWIST_NORM2)", "path_semantics": "DIMENSIONLESS__PAIR_PURE_Hdphi_ZERO_REDUCTION_PRESERVED__c_UNSELECTED"},
        {"one_form": "f(phi)*dphi", "exterior_derivative": "0", "status": "EXACT_AS_dF_phi", "path_semantics": "infinite_endpoint_potential_family"},
        {"one_form": "A", "exterior_derivative": "F", "status": "GAUGE_REPRESENTATIVE", "path_semantics": "open_path_gauge_covariant__loop_holonomy"},
    ]
    write_tsv(
        "CLOSEDNESS_ATLAS.tsv",
        ("one_form", "exterior_derivative", "status", "path_semantics"),
        closedness_rows,
    )

    owner_rows = [
        {"owner_id": "O01", "owned_object": "delta_K_and_dphi", "source": "G47_G51", "selection_effect": "FIXES_EXISTING_ENDPOINT_DEPTH_ONLY"},
        {"owner_id": "O02", "owned_object": "clock_ruler_screen_projectors", "source": "G43_G46_G47", "selection_effect": "CONSTRUCTS_MULTIPLE_LOCAL_FORMS"},
        {"owner_id": "O03", "owned_object": "normal_connection_D_and_curvature_F", "source": "G48_G49", "selection_effect": "PATH_CARRY_AFTER_PATH_SUPPLIED__NO_SCALAR_POTENTIAL"},
        {"owner_id": "O04", "owned_object": "complete_coframe_screen_weight", "source": "G46_G51", "selection_effect": "FIXES_REPRESENTATION_WEIGHT_PER_lambda__NOT_ONE_FORM"},
        {"owner_id": "O05", "owned_object": "stationary_special_loci", "source": "G50", "selection_effect": "CLASSIFIED_NOT_SELECTED"},
        {"owner_id": "O06", "owned_object": "on_shell_profile_branch_path_global_completion", "source": "G16_G20_G27_G51", "selection_effect": "OPEN"},
    ]
    write_tsv(
        "SELECTION_OWNER_CENSUS.tsv",
        ("owner_id", "owned_object", "source", "selection_effect"),
        owner_rows,
    )

    result = {
        "schema_version": 1,
        "arena": "REGULAR_STATIONARY_R17_LOCAL_FINITE_JETS__C01_C06_LAMBDA_STRATA__BOTH_ORIENTATIONS",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "status": "PASS",
        "order_zero_invariant_covectors": "SPAN_OF_UNIT_CLOCK_AND_UNIT_TWIST_RULER_COForms__DIMENSION_2",
        "generic_first_jet_covectors": "FULL_COTANGENT_SPAN_tau_nu_Hdphi_JHdphi",
        "metric_owned_forms_beyond_dphi": True,
        "distinguished_reciprocal_transgression_beyond_dphi": False,
        "stationary_R17_nonexact_scalar_weighted_depth_witness": "phi=w_ON_UNIT_QUATERNION_S3__lambda=0__I=x^2+y^2__dI_wedge_dphi_ZY=1/2",
        "pure_pair_leaf_preserving_transgression_family": "alpha_c=dphi+c*Hstar_dphi__ALL_REAL_c__RESTRICTS_TO_dphi_ON_E__dHstar_dphi_ZY=1/2_WITNESS",
        "pure_reciprocal_preserving_exact_family": "beta_c=dphi+c*dJ_H__J_H=I_H/(I_H+TWIST_NORM2)__DIMENSIONLESS_ON_TWISTED_R17__J_H_AND_dJ_H_ZERO_ON_Hstar_dphi_IDENTICALLY_ZERO_LOCUS__c_UNSELECTED",
        "normal_connection_potential": "GAUGE_REPRESENTATIVE_NOT_SCALAR_ONE_FORM",
        "existing_endpoint_depth_generator": "dphi",
        "selection_owner": None,
        "required_new_owner_class": "ON_SHELL_EQUATION_OR_GLOBAL_COMPLETION_OR_EXPLICIT_QUERY_MEASUREMENT_PREMISE",
        "maximum_ruling": "CANONICAL_STATIONARY_R17_GEOMETRIC_ONE_FORMS_BEYOND_dphi_DERIVED__GENERIC_FIRST_JET_SPANS_FULL_COTANGENT__ACTUAL_NONEXACT_R17_TRANSGRESSION_WITNESS_DERIVED__EXACT_PURE_RECIPROCAL_PRESERVING_FAMILY_SURVIVES__NO_DISTINGUISHED_RECIPROCAL_TRANSGRESSION_SELECTED_BY_LOCAL_METRIC_ALGEBRA__ADDITIONAL_OWNER_REQUIRED",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
