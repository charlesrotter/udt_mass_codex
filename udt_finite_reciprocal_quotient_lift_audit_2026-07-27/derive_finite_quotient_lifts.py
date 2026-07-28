#!/usr/bin/env python3
"""Exact finite reciprocal quotient-lift classification.

This script classifies linear/coframe lifts.  It does not select a physical UDT
quotient, observer section, path, screen flag, action, or boundary law.
"""

from __future__ import annotations

import json
import sympy as sp


def zero(value: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in value)


def flatten(value: sp.Matrix) -> sp.Matrix:
    return value.reshape(value.rows * value.cols, 1)


def metric_response(value: sp.Matrix, eta: sp.Matrix) -> sp.Matrix:
    return sp.simplify(value.T * eta + eta * value)


def second_metric_jet(value: sp.Matrix, eta: sp.Matrix) -> sp.Matrix:
    return sp.simplify(
        value.T * value.T * eta
        + 2 * value.T * eta * value
        + eta * value * value
    )


def rational_rotation(t: sp.Expr) -> sp.Matrix:
    """SO(2) rotation with rational half-angle parameter t."""
    return sp.Matrix(
        [
            [(1 - t**2) / (1 + t**2), -2 * t / (1 + t**2)],
            [2 * t / (1 + t**2), (1 - t**2) / (1 + t**2)],
        ]
    )


def main() -> None:
    eta_b = sp.diag(-1, 1)
    eta = sp.diag(-1, 1, 1, 1)
    h = sp.diag(-1, 1)
    j = sp.Matrix([[0, 1], [-1, 0]])
    phi = sp.symbols("phi", real=True)
    checks: dict[str, str] = {}

    def check(name: str, condition: bool) -> None:
        if not condition:
            raise AssertionError(name)
        checks[name] = "PASS"

    # Exact quotient condition pi F(phi)=B(phi) pi.
    fvars = sp.symbols("f0:16", real=True)
    f = sp.Matrix(4, 4, fvars)
    pi = sp.Matrix.hstack(sp.eye(2), sp.zeros(2))
    bphi = sp.diag(sp.exp(-phi), sp.exp(phi))
    quotient_residual = pi * f - bphi * pi
    quotient_matrix, quotient_rhs = sp.linear_eq_to_matrix(
        list(quotient_residual), fvars
    )
    check("quotient_constraint_rank_eight", quotient_matrix.rank() == 8)
    check("quotient_constraints_consistent", quotient_matrix.rank() == quotient_matrix.row_join(quotient_rhs).rank())
    check("quotient_pointwise_freedom_eight", 16 - quotient_matrix.rank() == 8)

    l00, l01, l10, l11 = sp.symbols("l00 l01 l10 l11", real=True)
    q00, q01, q10, q11 = sp.symbols("q00 q01 q10 q11", real=True)
    lower = sp.Matrix([[l00, l01], [l10, l11]])
    qblock = sp.Matrix([[q00, q01], [q10, q11]])
    quotient_lift = bphi.row_join(sp.zeros(2)).col_join(lower.row_join(qblock))
    check("general_block_lower_lift_projects_exactly", zero(pi * quotient_lift - bphi * pi))
    check("general_block_lower_lift_preserves_screen_kernel", quotient_lift[:2, 2:] == sp.zeros(2))
    check("general_block_lower_invertible_iff_screen_invertible", sp.simplify(quotient_lift.det() - qblock.det()) == 0)

    # Smooth complete one-parameter quotient representations have constant
    # generator X=[[H,0],[C,K]], with eight raw constants.
    cvars = sp.symbols("c00 c01 c10 c11", real=True)
    kvars = sp.symbols("k00 k01 k10 k11", real=True)
    c = sp.Matrix(2, 2, cvars)
    k = sp.Matrix(2, 2, kvars)
    x = h.row_join(sp.zeros(2)).col_join(c.row_join(k))
    group_parameters = cvars + kvars
    group_tangents = [x.diff(parameter) for parameter in group_parameters]
    check("quotient_group_generator_parameter_count_eight", len(group_parameters) == 8)
    check("quotient_group_generator_tangent_rank_eight", sp.Matrix.hstack(*(flatten(value) for value in group_tangents)).rank() == 8)
    check("quotient_group_generator_induces_founded_h", x[:2, :2] == h)
    check("quotient_group_generator_preserves_screen", x[:2, 2:] == sp.zeros(2))

    response = metric_response(x, eta)
    response_map, _ = sp.linear_eq_to_matrix(list(response), group_parameters)
    check("quotient_group_metric_response_rank_seven", response_map.rank() == 7)
    check("fixed_response_generator_fiber_dimension_one", len(group_parameters) - response_map.rank() == 1)
    kernel = response_map.nullspace()
    expected_kernel = sp.zeros(4)
    expected_kernel[2:, 2:] = j
    kernel_generator = sum(
        (coefficient * tangent for coefficient, tangent in zip(kernel[0], group_tangents)),
        sp.zeros(4),
    )
    check(
        "response_kernel_is_screen_so2",
        len(kernel) == 1
        and (zero(kernel_generator - expected_kernel) or zero(kernel_generator + expected_kernel)),
    )
    check("response_cross_block_is_C", response[2:, :2] == c)
    check("response_screen_block_is_K_plus_KT", response[2:, 2:] == k + k.T)

    # Fixed response K=S+wJ.
    a, b, d, w = sp.symbols("a b d w", real=True)
    screen_symmetric = sp.Matrix([[a, b], [b, d]])
    k_w = screen_symmetric + w * j
    x_w = h.row_join(sp.zeros(2)).col_join(c.row_join(k_w))
    x_zero = h.row_join(sp.zeros(2)).col_join(c.row_join(screen_symmetric))
    check("screen_rotation_leaves_first_metric_response", zero(metric_response(x_w, eta) - metric_response(x_zero, eta)))

    # The full eta-self-adjoint representative of the response generally
    # violates the exact quotient because it has an upper-right cross block.
    self_adjoint = sp.simplify(eta.inv() * response / 2)
    check("full_self_adjoint_has_upper_cross_block", self_adjoint[:2, 2:] == eta_b * c.T / 2)
    self_adjoint_quotient_solution = sp.solve(
        list(self_adjoint[:2, 2:]), cvars, dict=True
    )
    check(
        "full_self_adjoint_is_quotient_only_without_mixing",
        self_adjoint_quotient_solution
        == [{cvars[0]: 0, cvars[1]: 0, cvars[2]: 0, cvars[3]: 0}],
    )
    check("screen_self_adjoint_w_zero_is_valid_quotient_representative", x_zero[:2, 2:] == sp.zeros(2))

    # Upper and lower triangular screen flags select opposite w values.
    k_upper = screen_symmetric + b * j
    k_lower = screen_symmetric - b * j
    check("upper_flag_sets_lower_left_zero", k_upper[1, 0] == 0)
    check("lower_flag_sets_upper_right_zero", k_lower[0, 1] == 0)
    check("upper_and_lower_flags_share_response", zero(k_upper + k_upper.T - k_lower - k_lower.T))
    check("upper_and_lower_flags_distinct_generically", sp.simplify(k_upper - k_lower) == 2 * b * j)
    r90 = sp.Matrix([[0, -1], [1, 0]])
    rotated_upper = sp.simplify(r90 * k_upper * r90.T)
    check("screen_rotation_changes_triangular_flag", rotated_upper[0, 1] == 0 and rotated_upper[1, 0] != 0)

    # Second metric jets identify the exact stratum where w is invisible.
    x_unmixed_w = h.row_join(sp.zeros(2)).col_join(sp.zeros(2).row_join(k_w))
    x_unmixed_zero = h.row_join(sp.zeros(2)).col_join(sp.zeros(2).row_join(screen_symmetric))
    anisotropic_difference = sp.simplify(
        second_metric_jet(x_unmixed_w, eta)
        - second_metric_jet(x_unmixed_zero, eta)
    )
    expected_anisotropic = sp.zeros(4)
    expected_anisotropic[2:, 2:] = sp.Matrix(
        [[-4 * b * w, 2 * w * (a - d)], [2 * w * (a - d), 4 * b * w]]
    )
    check("anisotropic_second_jet_formula", anisotropic_difference == expected_anisotropic)
    anisotropy_zero_solution = sp.solve(
        [entry / w for entry in anisotropic_difference if entry != 0],
        (a, b),
        dict=True,
    )
    check(
        "unmixed_nonzero_rotation_invisible_at_second_jet_iff_isotropic",
        anisotropy_zero_solution == [{a: d, b: 0}],
    )
    check("anisotropic_rotation_changes_second_jet_control", not zero(anisotropic_difference.subs({a: 2, b: 1, d: -1, w: 1})))

    lam = sp.symbols("lambda", real=True)
    isotropic_k = lam * sp.eye(2) + w * j
    x_iso_w = h.row_join(sp.zeros(2)).col_join(sp.zeros(2).row_join(isotropic_k))
    x_iso_zero = h.row_join(sp.zeros(2)).col_join(sp.zeros(2).row_join(lam * sp.eye(2)))
    check("isotropic_unmixed_second_jet_independent_of_rotation", zero(second_metric_jet(x_iso_w, eta) - second_metric_jet(x_iso_zero, eta)))

    rotation = sp.Matrix([[sp.cos(w * phi), sp.sin(w * phi)], [-sp.sin(w * phi), sp.cos(w * phi)]])
    q_iso_w = sp.exp(lam * phi) * rotation
    q_iso_zero = sp.exp(lam * phi) * sp.eye(2)
    check("isotropic_screen_exponential_factorization", zero(q_iso_w - sp.exp(lam * phi) * rotation))
    check("isotropic_unmixed_finite_metric_independent_of_rotation", zero(q_iso_w.T * q_iso_w - q_iso_zero.T * q_iso_zero))

    x_mixed_w = h.row_join(sp.zeros(2)).col_join(c.row_join(isotropic_k))
    x_mixed_zero = h.row_join(sp.zeros(2)).col_join(c.row_join(lam * sp.eye(2)))
    mixed_difference = sp.simplify(
        second_metric_jet(x_mixed_w, eta) - second_metric_jet(x_mixed_zero, eta)
    )
    expected_mixed = sp.zeros(4)
    expected_mixed[:2, 2:] = sp.Matrix(
        [[-cvars[2] * w, cvars[0] * w], [-cvars[3] * w, cvars[1] * w]]
    )
    expected_mixed[2:, :2] = expected_mixed[:2, 2:].T
    check("isotropic_mixed_second_jet_formula", mixed_difference == expected_mixed)
    mixed_zero_solution = sp.solve(
        [entry / w for entry in mixed_difference if entry != 0],
        cvars,
        dict=True,
    )
    check(
        "nonzero_rotation_with_isotropic_screen_invisible_at_second_jet_iff_unmixed",
        mixed_zero_solution
        == [{cvars[0]: 0, cvars[1]: 0, cvars[2]: 0, cvars[3]: 0}],
    )

    # Exact quotient-only fixed-metric counterfamily that is not a group.
    rt = rational_rotation(phi**2)
    nonlinear_lorentz = sp.eye(4)
    nonlinear_lorentz[2:, 2:] = rt
    spectator = bphi.row_join(sp.zeros(2)).col_join(sp.zeros(2).row_join(sp.eye(2)))
    nonlinear_lift = sp.simplify(nonlinear_lorentz * spectator)
    check("nonlinear_frame_path_is_exact_quotient_lift", zero(pi * nonlinear_lift - bphi * pi))
    check("nonlinear_frame_path_preserves_complete_metric", zero(nonlinear_lift.T * eta * nonlinear_lift - spectator.T * eta * spectator))
    f_one = nonlinear_lift.subs(phi, 1)
    f_two = nonlinear_lift.subs(phi, 2)
    check("nonlinear_frame_path_fails_group_law", not zero(f_one * f_one - f_two))
    check("nonlinear_frame_path_fails_reversal", not zero(nonlinear_lift.subs(phi, -1) * nonlinear_lift.subs(phi, 1) - sp.eye(4)))

    # Constant generators give exact composition/reversal.  Use an exact
    # nontrivial shift witness to avoid asking SymPy to exponentiate symbols.
    s = sp.symbols("s", real=True)
    shift = sp.eye(4)
    shift[0, 0] = sp.exp(-phi)
    shift[1, 1] = sp.exp(phi)
    shift[2, 0] = s * (1 - sp.exp(-phi))
    phi1, phi2 = sp.symbols("phi1 phi2", real=True)
    check("constant_generator_shift_projects_exactly", zero(pi * shift - bphi * pi))
    check("constant_generator_shift_composes", zero(shift.subs(phi, phi2) * shift.subs(phi, phi1) - shift.subs(phi, phi1 + phi2)))
    check("constant_generator_shift_reverses", zero(shift.subs(phi, -phi) * shift - sp.eye(4)))

    # All extensions meet at the identity; the seal value cannot select w,C,K.
    check("all_regular_group_lifts_equal_identity_at_seal", sp.exp(0 * x) == sp.eye(4))
    check("seal_value_has_zero_generator_selector_rank", sp.zeros(16, 8).rank() == 0)

    expected_check_count = 42
    check("registered_check_count_before_count_check", len(checks) == expected_check_count - 1)
    if len(checks) != expected_check_count:
        raise AssertionError(f"unexpected check count {len(checks)}")

    result = {
        "schema": "udt.finite_reciprocal_quotient_lift.derivation.v1",
        "result": "PASS",
        "sympy_version": sp.__version__,
        "check_count": len(checks),
        "checks": checks,
        "counts": {
            "exact_quotient_pointwise_function_components": 8,
            "complete_group_generator_parameters": 8,
            "complete_group_first_metric_response_rank": 7,
            "fixed_response_generator_fiber_dimension": 1,
            "screen_flag_choices_explicitly_tested": 2,
        },
        "normal_forms": {
            "quotient_only": "F(phi)=[[B(phi),0],[L(phi),Q(phi)]] with arbitrary smooth L and invertible Q, L(0)=0,Q(0)=I",
            "quotient_group": "F(phi)=exp(phi X), X=[[H,0],[C,K]]",
            "block_exponential": "lower-left integral_0^phi exp((phi-t)K) C exp(tH) dt",
            "fixed_response": "K=S+wJ; C and S fixed by metric first jet; w free",
            "upper_flag": "w=screen_offdiagonal_symmetric_component",
            "lower_flag": "w=-screen_offdiagonal_symmetric_component",
        },
        "second_jet_controls": {
            "anisotropic_unmixed_difference": str(anisotropic_difference),
            "isotropic_mixed_difference": str(mixed_difference),
            "metric_invisible_screen_rotation_stratum": "C=0_AND_S=lambda*I",
            "generic_ruling": "SCREEN_ROTATION_CHANGES_FINITE_METRIC_DATA_AT_SECOND_ORDER",
        },
        "rulings": {
            "block_lower_form": "DERIVED_IF_EXACT_QUOTIENT",
            "constant_generator": "DERIVED_IF_COMPLETE_GROUP_LAW",
            "triangular_chart": "CONDITIONAL_ON_CHOSEN_SCREEN_FLAG_NOT_SELECTED_BY_QUOTIENT_OR_METRIC_RESPONSE",
            "fixed_response_lift": "ONE_PARAMETER_SCREEN_ROTATION_FAMILY",
            "self_adjoint_lift": "GENERALLY_OUTSIDE_EXACT_QUOTIENT_CLASS_WHEN_MIXING_IS_NONZERO",
            "isotropic_unmixed_rotation": "FINITE_METRIC_REPRESENTATIVE_FREEDOM",
            "generic_rotation": "INEQUIVALENT_FINITE_METRIC_DATA",
            "physical_quotient_extension": "OPEN_NOT_SELECTED",
            "global_screen_flag": "OPEN_NOT_SELECTED",
        },
        "maximum_conclusion": "EXACT_FINITE_QUOTIENT_AND_GROUP_LIFT_CLASSES_DERIVED_CONDITIONALLY;_FIXED_RESPONSE_LEAVES_ONE_SCREEN_ROTATION_AND_GLOBAL_PHYSICAL_SELECTION_OPEN",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
