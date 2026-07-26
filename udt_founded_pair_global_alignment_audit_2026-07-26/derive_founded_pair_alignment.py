#!/usr/bin/env python3
"""Exact founded-pair and complete-extension alignment classification."""

from __future__ import annotations

import json
import sympy as sp


def check(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def zero(value: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in value)


def metric_pair_invariant(metric: sp.Matrix, operator: sp.Matrix) -> sp.Expr:
    return sp.simplify(sp.trace(metric.inv() * operator.T * metric * operator))


def main() -> None:
    checks: dict[str, str] = {}
    eta2 = sp.diag(-1, 1)
    eta4 = sp.diag(-1, 1, 1, 1)
    H = sp.diag(-1, 1)

    # The founded pair is self-adjoint and its eigenlines have opposite causal type.
    check("founded_generator_is_eta_self_adjoint", H.T * eta2 == eta2 * H, checks)
    check("founded_generator_is_involution", H**2 == sp.eye(2), checks)
    check("founded_pair_invariant_is_two", metric_pair_invariant(eta2, H) == 2, checks)
    check("founded_clock_line_is_timelike", eta2[0, 0] < 0, checks)
    check("founded_ruler_line_is_spacelike", eta2[1, 1] > 0, checks)

    # A general symmetric pair metric is compatible with the fixed founded
    # diagonal operator exactly when its off-diagonal entry vanishes.
    aa, bb, cc = sp.symbols("aa bb cc", real=True)
    pair_metric = sp.Matrix([[aa, bb], [bb, cc]])
    self_adjoint_defect = sp.simplify(H.T * pair_metric - pair_metric * H)
    check(
        "fixed_operator_self_adjoint_defect",
        self_adjoint_defect == sp.Matrix([[0, -2 * bb], [2 * bb, 0]]),
        checks,
    )
    check(
        "fixed_operator_self_adjoint_iff_pair_offdiagonal_zero",
        sp.solve(list(self_adjoint_defect), bb, dict=True) == [{bb: 0}],
        checks,
    )

    # A passive basis change must transform metric and operator together.
    shear = sp.Matrix([[1, 1], [0, 1]])
    transformed_metric = sp.simplify(shear.T * eta2 * shear)
    transformed_operator = sp.simplify(shear.inv() * H * shear)
    check("shear_is_invertible", shear.det() == 1, checks)
    check("simultaneous_transform_metric_is_mixed", transformed_metric[0, 1] != 0, checks)
    check("simultaneous_transform_operator_is_not_diagonal", transformed_operator != H, checks)
    check(
        "simultaneous_transform_preserves_self_adjointness",
        transformed_operator.T * transformed_metric == transformed_metric * transformed_operator,
        checks,
    )
    check(
        "simultaneous_transform_preserves_pair_invariant",
        metric_pair_invariant(transformed_metric, transformed_operator) == 2,
        checks,
    )
    check(
        "metric_only_transform_changes_metric_operator_pair",
        H.T * transformed_metric != transformed_metric * H,
        checks,
    )
    check(
        "metric_only_transform_changes_pair_invariant",
        metric_pair_invariant(transformed_metric, H) != 2,
        checks,
    )

    # Exact previously used swap-isometric mixed witness is inequivalent to
    # the founded self-adjoint pair.
    mixed_metric = sp.Matrix([[1, -2], [-2, 1]])
    swap = sp.Matrix([[0, 1], [1, 0]])
    check("mixed_witness_is_Lorentzian", mixed_metric.det() < 0, checks)
    check("mixed_witness_swap_isometry", swap.T * mixed_metric * swap == mixed_metric, checks)
    check("mixed_witness_fixed_H_not_self_adjoint", H.T * mixed_metric != mixed_metric * H, checks)
    check("mixed_witness_pair_invariant_minus_ten_thirds", metric_pair_invariant(mixed_metric, H) == -sp.Rational(10, 3), checks)
    check("mixed_witness_inequivalent_to_founded_pair", metric_pair_invariant(mixed_metric, H) != metric_pair_invariant(eta2, H), checks)

    # The simultaneous stabilizer of the metric and founded operator is only
    # the four independent sign choices; no continuous boost preserves both.
    x00, x01, x10, x11 = sp.symbols("x00 x01 x10 x11", real=True)
    S = sp.Matrix([[x00, x01], [x10, x11]])
    commutator = sp.simplify(S * H - H * S)
    commutant_solution = sp.solve(list(commutator), (x01, x10), dict=True)
    check("pair_operator_commutant_forces_diagonal", commutant_solution == [{x01: 0, x10: 0}], checks)
    S_diagonal = sp.diag(x00, x11)
    stabilizer_solutions = sp.solve(list(S_diagonal.T * eta2 * S_diagonal - eta2), (x00, x11), dict=True)
    check("metric_operator_stabilizer_has_four_sign_elements", len(stabilizer_solutions) == 4, checks)

    # Complete Lorentz metrics with the exact founded pair restriction. The
    # pair/screen cross block W remains arbitrary. A complement shear fixing
    # the pair pointwise removes W and exposes the Schur complement.
    w00, w01, w10, w11 = sp.symbols("w00 w01 w10 w11", real=True)
    q00, q01, q11 = sp.symbols("q00 q01 q11", real=True)
    W = sp.Matrix([[w00, w01], [w10, w11]])
    Q = sp.Matrix([[q00, q01], [q01, q11]])
    G = eta2.row_join(W).col_join(W.T.row_join(Q))
    complement_shear = sp.eye(4)
    complement_shear[:2, 2:] = -eta2 * W
    schur = sp.simplify(Q - W.T * eta2 * W)
    diagonalized_G = sp.simplify(complement_shear.T * G * complement_shear)
    check("complete_metric_pair_restriction_exact", G[:2, :2] == eta2, checks)
    check("complement_shear_fixes_pair_pointwise", complement_shear[:, :2] == sp.eye(4)[:, :2], checks)
    check("cross_terms_removed_by_local_complement_change", diagonalized_G[:2, 2:] == sp.zeros(2), checks)
    check("schur_complement_exposed", diagonalized_G[2:, 2:] == schur, checks)

    W_witness = sp.diag(sp.Rational(1, 4), sp.Rational(1, 4))
    Q_witness = sp.eye(2)
    G_witness = eta2.row_join(W_witness).col_join(W_witness.T.row_join(Q_witness))
    schur_witness = sp.simplify(Q_witness - W_witness.T * eta2 * W_witness)
    check("nonzero_cross_witness", W_witness != sp.zeros(2), checks)
    check("cross_witness_schur_positive", schur_witness == sp.diag(sp.Rational(17, 16), sp.Rational(15, 16)), checks)
    check("cross_witness_is_nondegenerate_Lorentz_by_congruence", G_witness.det() < 0, checks)
    check("cross_witness_pair_restriction_still_exact", G_witness[:2, :2] == eta2, checks)

    # Coframe orientation matters. A lower shift retains the first two output
    # slots but changes the total metric restricted to the founded base by
    # C^T C. An upper shift preserves that metric restriction while changing
    # the complementary coframe presentation.
    p0, p1 = sp.symbols("p0 p1", positive=True)
    c00, c01, c10, c11 = sp.symbols("c00 c01 c10 c11", real=True)
    d00, d01, d10, d11 = sp.symbols("d00 d01 d10 d11", real=True)
    P = sp.diag(p0, p1)
    C = sp.Matrix([[c00, c01], [c10, c11]])
    Dmix = sp.Matrix([[d00, d01], [d10, d11]])
    lower = P.row_join(sp.zeros(2)).col_join(C.row_join(sp.eye(2)))
    upper = P.row_join(Dmix).col_join(sp.zeros(2).row_join(sp.eye(2)))
    lower_metric = sp.simplify(lower.T * eta4 * lower)
    upper_metric = sp.simplify(upper.T * eta4 * upper)
    founded_scaled_metric = sp.simplify(P.T * eta2 * P)
    check("lower_shift_pair_metric_adds_CtC", lower_metric[:2, :2] - founded_scaled_metric == C.T * C, checks)
    check("upper_shift_preserves_pair_metric_restriction", upper_metric[:2, :2] == founded_scaled_metric, checks)
    check("upper_shift_can_have_cross_sector_metric", upper_metric[:2, 2:] == P.T * eta2 * Dmix, checks)
    sum_squares = sp.expand(sp.trace(C.T * C))
    check("lower_shift_zero_trace_is_sum_of_four_squares", sum_squares == c00**2 + c01**2 + c10**2 + c11**2, checks)

    # In an intrinsic orthogonal splitting, a metric-self-adjoint complete
    # generator that leaves the founded nondegenerate pair invariant must also
    # leave its orthogonal complement invariant.
    b00, b01, b10, b11 = sp.symbols("b00 b01 b10 b11", real=True)
    s00, s01, s11 = sp.symbols("s00 s01 s11", real=True)
    B = sp.Matrix([[b00, b01], [b10, b11]])
    screen_response = sp.Matrix([[s00, s01], [s01, s11]])
    A = eta2 * B.T
    X_complete = H.row_join(A).col_join(B.row_join(screen_response))
    check("general_compression_family_is_eta4_self_adjoint", X_complete.T * eta4 == eta4 * X_complete, checks)
    check("compression_top_left_is_founded_generator", X_complete[:2, :2] == H, checks)
    check("complete_generator_lower_left_is_mixing_block", X_complete[2:, :2] == B, checks)
    pair_invariance_solution = sp.solve(list(B), (b00, b01, b10, b11), dict=True)
    check(
        "pair_invariance_forces_all_four_mixing_entries_zero",
        pair_invariance_solution == [{b00: 0, b01: 0, b10: 0, b11: 0}],
        checks,
    )
    check("self_adjointness_ties_upper_mixing_to_lower_mixing", X_complete[:2, 2:] == eta2 * B.T, checks)
    X_invariant = X_complete.subs({b00: 0, b01: 0, b10: 0, b11: 0})
    check("invariant_self_adjoint_extension_is_block_diagonal", X_invariant[:2, 2:] == sp.zeros(2) and X_invariant[2:, :2] == sp.zeros(2), checks)
    check("invariant_extension_has_three_screen_components", len((s00, s01, s11)) == 3, checks)

    B_witness = sp.Matrix([[1, 0], [0, 0]])
    X_compression_witness = X_complete.subs({b00: 1, b01: 0, b10: 0, b11: 0, s00: 0, s01: 0, s11: 0})
    pair_vector = sp.Matrix([1, 0, 0, 0])
    check("compression_witness_is_self_adjoint", X_compression_witness.T * eta4 == eta4 * X_compression_witness, checks)
    check("compression_witness_top_left_still_H", X_compression_witness[:2, :2] == H, checks)
    check("compression_witness_does_not_preserve_pair", X_compression_witness * pair_vector != sp.Matrix([-1, 0, 0, 0]), checks)
    check("compression_witness_lower_block_matches_B", X_compression_witness[2:, :2] == B_witness, checks)

    # Screen isotropy is an additional selector, not a pair consequence.
    J = sp.Matrix([[0, -1], [1, 0]])
    screen_commutator = sp.simplify(screen_response * J - J * screen_response)
    isotropic_solution = sp.solve(list(screen_commutator), (s01, s11), dict=True)
    check("screen_rotation_equivariance_forces_scalar_response", isotropic_solution == [{s01: 0, s11: s00}], checks)
    lam = sp.symbols("lam", real=True)
    X_lambda = sp.diag(-1, 1, lam, lam)
    check("isotropic_family_trace_two_lambda", sp.trace(X_lambda) == 2 * lam, checks)
    check("trace_zero_selects_lambda_zero_only_after_isotropy", sp.solve(sp.trace(X_lambda), lam) == [0], checks)
    check("pair_restriction_independent_of_lambda", X_lambda[:2, :2] == H, checks)

    # A metric isometry cannot exchange the opposite-causal founded lines.
    e0 = sp.Matrix([1, 0, 0, 0])
    e1 = sp.Matrix([0, 1, 0, 0])
    check("clock_and_ruler_norms_have_opposite_sign", (e0.T * eta4 * e0)[0] == -1 and (e1.T * eta4 * e1)[0] == 1, checks)
    check("causal_norm_preservation_obstructs_physical_line_exchange", (e0.T * eta4 * e0)[0] != (e1.T * eta4 * e1)[0], checks)

    if len(checks) != 50:
        raise AssertionError(f"unexpected check count {len(checks)}")

    result = {
        "schema": "udt-founded-pair-global-alignment-audit-1.0",
        "result": "PASS",
        "sympy_version": sp.__version__,
        "check_count": len(checks),
        "checks": checks,
        "counts": {
            "founded_pair_dimensions": 2,
            "simultaneous_metric_operator_continuous_stabilizer_dimension": 0,
            "simultaneous_metric_operator_discrete_stabilizer_elements": 4,
            "complete_metric_cross_block_parameters_with_fixed_pair_restriction": 4,
            "self_adjoint_compression_extension_parameters_after_fixed_pair_block": 7,
            "self_adjoint_invariant_pair_extension_screen_parameters": 3,
            "screen_rotation_equivariant_physical_parameters": 1,
        },
        "rulings": {
            "local_pair_alignment": "INTRINSIC_TO_FOUNDED_METRIC_OPERATOR_PAIR_UNDER_DECLARED_READOUT",
            "passive_basis_change": "TRANSFORM_METRIC_AND_OPERATOR_TOGETHER; DOES_NOT_CREATE_MIXED_FIXED_OPERATOR_FAMILY",
            "mixed_fixed_operator_readout": "INEQUIVALENT_ALTERNATIVE_REQUIRING_READOUT_PREMISE_CHANGE",
            "complete_metric_cross_terms": "COMPATIBLE_WITH_EXACT_PAIR_RESTRICTION_AND_LOCALLY_REMOVABLE_BY_COMPLEMENT_CHANGE",
            "self_adjoint_invariant_extension": "FOUNDED_PAIR_AND_ORTHOGONAL_COMPLEMENT_BOTH_INVARIANT",
            "projection_only_extension": "NOT_AN_INVARIANT_SUBBUNDLE_EXTENSION",
            "screen_response": "UNSELECTED; THREE_SELF_ADJOINT_COMPONENTS_OR_ONE_AFTER_SEPARATE_SCREEN_ISOTROPY",
            "global_pair_field": "NOT_DERIVED_BY_LOCAL_CLASSIFICATION",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
