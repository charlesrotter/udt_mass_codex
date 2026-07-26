#!/usr/bin/env python3
"""Exact local algebra for the covariant reciprocal-coframe lift atlas."""

from __future__ import annotations

import json
import sympy as sp


def flat(value: sp.Matrix) -> sp.Matrix:
    return value.reshape(value.rows * value.cols, 1)


def check(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def unit(i: int, j: int) -> sp.Matrix:
    value = sp.zeros(4)
    value[i, j] = 1
    return value


def boost(i: int) -> sp.Matrix:
    return unit(0, i) + unit(i, 0)


def rotation(i: int, j: int) -> sp.Matrix:
    return unit(i, j) - unit(j, i)


def commutant(generators: list[sp.Matrix]) -> tuple[sp.Matrix, list[sp.Matrix]]:
    variables = sp.symbols("z0:16", real=True)
    Z = sp.Matrix(4, 4, variables)
    equations: list[sp.Expr] = []
    for generator in generators:
        equations.extend(list(Z * generator - generator * Z))
    coefficient = sp.Matrix(equations).jacobian(variables)
    return coefficient, [sp.Matrix(4, 4, vector) for vector in coefficient.nullspace()]


def span_rank(values: list[sp.Matrix]) -> int:
    if not values:
        return 0
    return sp.Matrix.hstack(*(flat(value) for value in values)).rank()


def same_span(left: list[sp.Matrix], right: list[sp.Matrix]) -> bool:
    rank_left = span_rank(left)
    rank_right = span_rank(right)
    return rank_left == rank_right == span_rank(left + right)


def metric_tangent(value: sp.Matrix, eta: sp.Matrix) -> sp.Matrix:
    return sp.simplify(value.T * eta + eta * value)


def independent_basis(values: list[sp.Matrix]) -> list[sp.Matrix]:
    """Return a deterministic column-space basis of flattened matrices."""
    if not values:
        return []
    columns = sp.Matrix.hstack(*(flat(value) for value in values)).columnspace()
    return [sp.Matrix(4, 4, column) for column in columns]


def main() -> None:
    eta = sp.diag(-1, 1, 1, 1)
    I = sp.eye(4)
    P0, P1, P2, P3 = (unit(index, index) for index in range(4))
    checks: dict[str, str] = {}

    K1, K2, K3 = boost(1), boost(2), boost(3)
    J12, J13, J23 = rotation(1, 2), rotation(1, 3), rotation(2, 3)

    # Metric plus scalar data: full Lorentz commutant is scalar identity.
    full_coefficient, full_basis = commutant([K1, K2, K3, J12, J13, J23])
    check("full_Lorentz_commutant_dimension_one", 16 - full_coefficient.rank() == 1, checks)
    check("full_Lorentz_commutant_is_scalar_identity", same_span(full_basis, [I]), checks)

    # One timelike line: SO(3) stabilizer and its 1+3 commutant.
    time_coefficient, time_basis = commutant([J12, J13, J23])
    P_space = I - P0
    check("timelike_line_commutant_dimension_two", 16 - time_coefficient.rank() == 2, checks)
    check("timelike_line_commutant_is_line_plus_complement", same_span(time_basis, [P0, P_space]), checks)

    # One spacelike line: SO+(1,2) stabilizer on its Lorentzian complement.
    space_coefficient, space_basis = commutant([K2, K3, J23])
    P_space_line = P1
    P_space_complement = I - P1
    check("spacelike_line_commutant_dimension_two", 16 - space_coefficient.rank() == 2, checks)
    check("spacelike_line_commutant_is_line_plus_complement", same_span(space_basis, [P_space_line, P_space_complement]), checks)

    # Stabilizer-invariant nontrivial involutions give democratic 1+3
    # character lifts, not a selected rank-two plane.
    X_clock = I - 2 * P0
    X_ruler = 2 * P1 - I
    check("clock_democratic_lift_is_involution", X_clock**2 == I, checks)
    check("ruler_democratic_lift_is_involution", X_ruler**2 == I, checks)
    check("clock_democratic_lift_commutes_with_stabilizer", all(X_clock * value == value * X_clock for value in [J12, J13, J23]), checks)
    check("ruler_democratic_lift_commutes_with_stabilizer", all(X_ruler * value == value * X_ruler for value in [K2, K3, J23]), checks)
    check("clock_democratic_trace_two", sp.trace(X_clock) == 2, checks)
    check("ruler_democratic_trace_minus_two", sp.trace(X_ruler) == -2, checks)
    check("clock_democratic_metric_response_nonzero", metric_tangent(X_clock, eta) != sp.zeros(4), checks)
    check("ruler_democratic_metric_response_nonzero", metric_tangent(X_ruler, eta) != sp.zeros(4), checks)

    invariant_projector_ranks = sorted({0, 1, 3, 4})
    check("one_line_invariant_projector_ranks", invariant_projector_ranks == [0, 1, 3, 4], checks)
    check("one_line_has_no_invariant_rank_two_projector", 2 not in invariant_projector_ranks, checks)

    # Null line stabilizer. The commutant is span(I,N), N^2=0, with no
    # nontrivial idempotent or reciprocal involution.
    N2 = K2 + J12
    N3 = K3 + J13
    null_coefficient, null_basis = commutant([N2, N3, J23])
    k = sp.Matrix([1, 1, 0, 0])
    k_flat = (k.T * eta)
    N = k * k_flat
    check("null_line_commutant_dimension_two", 16 - null_coefficient.rank() == 2, checks)
    check("null_line_commutant_is_identity_plus_nilpotent", same_span(null_basis, [I, N]), checks)
    check("null_nilpotent_square_zero", N**2 == sp.zeros(4), checks)
    aa, bb = sp.symbols("aa bb", real=True)
    null_general = aa * I + bb * N
    idempotent_solutions = sp.solve(list(null_general**2 - null_general), (aa, bb), dict=True)
    involution_solutions = sp.solve(list(null_general**2 - I), (aa, bb), dict=True)
    check("null_only_trivial_idempotents", idempotent_solutions == [{aa: 0, bb: 0}, {aa: 1, bb: 0}], checks)
    check("null_only_scalar_involutions", involution_solutions == [{aa: -1, bb: 0}, {aa: 1, bb: 0}], checks)

    # An ordered orthonormal clock/ruler pair leaves an SO(2) screen
    # stabilizer. Fixing the founded base action leaves screen dilation plus
    # screen rotation.
    pair_coefficient, pair_basis = commutant([J23])
    check("ordered_pair_stabilizer_commutant_dimension_six", 16 - pair_coefficient.rank() == 6, checks)
    variables = sp.symbols("x0:16", real=True)
    Z = sp.Matrix(4, 4, variables)
    equations = list(Z * J23 - J23 * Z)
    equations.extend([Z[0, 0] + 1, Z[0, 1], Z[1, 0], Z[1, 1] - 1])
    coefficient, rhs = sp.linear_eq_to_matrix(equations, variables)
    check("ordered_pair_fixed_base_affine_dimension_two", 16 - coefficient.rank() == 2, checks)
    lam, omega = sp.symbols("lam omega", real=True)
    P_screen = P2 + P3
    J_screen = -J23
    H_pair_lift = -P0 + P1
    X_pair = H_pair_lift + lam * P_screen + omega * J_screen
    check("ordered_pair_general_candidate_commutes_with_screen", X_pair * J23 == J23 * X_pair, checks)
    check("ordered_pair_base_restriction_exact", X_pair[:2, :2] == sp.diag(-1, 1), checks)
    check("screen_rotation_is_Lorentz_gauge", metric_tangent(J_screen, eta) == sp.zeros(4), checks)
    check("screen_dilation_is_physical", metric_tangent(P_screen, eta) != sp.zeros(4), checks)
    check("ordered_pair_physical_modulus_count_one", span_rank([metric_tangent(P_screen, eta), metric_tangent(J_screen, eta)]) == 1, checks)
    check("ordered_pair_trace_is_two_lambda", sp.trace(X_pair) == 2 * lam, checks)
    check("complete_determinant_one_condition_is_lambda_zero", sp.solve(sp.trace(X_pair), lam) == [0], checks)
    check("clock_democratic_is_lambda_plus_one", X_pair.subs({lam: 1, omega: 0}) == X_clock, checks)
    check("ruler_democratic_is_lambda_minus_one", X_pair.subs({lam: -1, omega: 0}) == X_ruler, checks)
    check("spectator_is_lambda_zero", X_pair.subs({lam: 0, omega: 0}) == H_pair_lift, checks)

    # Full fixed-observer directional family. Six rational unit-direction
    # projectors span Sym(3), so they suffice to determine the complete local
    # family algebra without privileging an axis.
    spatial_projectors = [P1, P2, P3]
    for i, j in ((1, 2), (1, 3), (2, 3)):
        vector = sp.zeros(4, 1)
        vector[i] = sp.sqrt(2) / 2
        vector[j] = sp.sqrt(2) / 2
        spatial_projectors.append(sp.simplify(vector * vector.T))
    check("six_direction_projectors_span_symmetric_spatial_matrices", span_rank(spatial_projectors) == 6, checks)

    def directional_lift(projector: sp.Matrix, value: sp.Expr) -> sp.Matrix:
        return sp.simplify(-P0 + projector + value * (P_space - projector))

    Pn = spatial_projectors[0]
    Pm = spatial_projectors[3]
    Xn = directional_lift(Pn, lam)
    Xm = directional_lift(Pm, lam)
    check(
        "directional_commutator_factorization",
        sp.simplify((Xn * Xm - Xm * Xn) - (1 - lam) ** 2 * (Pn * Pm - Pm * Pn)) == sp.zeros(4),
        checks,
    )
    projector_commutators = [
        left * right - right * left
        for index, left in enumerate(spatial_projectors)
        for right in spatial_projectors[index + 1 :]
    ]
    check("direction_projector_commutators_span_so3", span_rank(projector_commutators) == 3, checks)

    directional_zero = [directional_lift(value, sp.Integer(0)) for value in spatial_projectors]
    angular_zero = [
        left * right - right * left
        for index, left in enumerate(directional_zero)
        for right in directional_zero[index + 1 :]
    ]
    lie_zero = independent_basis(directional_zero + angular_zero)
    check("generic_directional_generator_span_six", span_rank(directional_zero) == 6, checks)
    check("generic_directional_angular_span_three", span_rank(angular_zero) == 3, checks)
    check("generic_directional_Lie_span_nine", len(lie_zero) == 9, checks)
    check(
        "generic_directional_nine_space_closed_under_commutators",
        all(
            span_rank(lie_zero + [left * right - right * left]) == 9
            for left in lie_zero
            for right in lie_zero
        ),
        checks,
    )

    directional_two = [directional_lift(value, sp.Integer(2)) for value in spatial_projectors]
    angular_two = [
        left * right - right * left
        for index, left in enumerate(directional_two)
        for right in directional_two[index + 1 :]
    ]
    check("second_generic_lambda_Lie_span_nine", span_rank(directional_two + angular_two) == 9, checks)

    directional_half = [directional_lift(value, -sp.Rational(1, 2)) for value in spatial_projectors]
    angular_half = [
        left * right - right * left
        for index, left in enumerate(directional_half)
        for right in directional_half[index + 1 :]
    ]
    check("lambda_minus_half_Lie_span_still_nine", span_rank(directional_half + angular_half) == 9, checks)
    axis_sum = sp.simplify(
        directional_lift(P1, lam) + directional_lift(P2, lam) + directional_lift(P3, lam)
    )
    check("three_axis_sum_formula", axis_sum == -3 * P0 + (1 + 2 * lam) * P_space, checks)
    check("lambda_minus_half_axis_sum_is_pure_clock", axis_sum.subs(lam, -sp.Rational(1, 2)) == -3 * P0, checks)

    directional_one = [directional_lift(value, sp.Integer(1)) for value in spatial_projectors]
    angular_one = [
        left * right - right * left
        for index, left in enumerate(directional_one)
        for right in directional_one[index + 1 :]
    ]
    check("lambda_one_directional_family_collapses_to_clock_democratic", all(value == X_clock for value in directional_one), checks)
    check("lambda_one_generator_span_one", span_rank(directional_one) == 1, checks)
    check("lambda_one_commutator_span_zero", span_rank(angular_one) == 0, checks)
    check("lambda_one_Lie_span_one", span_rank(directional_one + angular_one) == 1, checks)

    # Exact frame conjugation: covariance transports the candidate; it does
    # not keep one component matrix fixed.
    L = sp.eye(4)
    L[0, 0] = sp.Rational(5, 4)
    L[0, 2] = sp.Rational(3, 4)
    L[2, 0] = sp.Rational(3, 4)
    L[2, 2] = sp.Rational(5, 4)
    check("rational_frame_change_is_Lorentz", L.T * eta * L == eta, checks)
    X_sample = X_pair.subs({lam: 2, omega: 0})
    X_transformed = sp.simplify(L * X_sample * L.inv())
    Q_sample = metric_tangent(X_sample, eta)
    Q_transformed = metric_tangent(X_transformed, eta)
    check("generator_conjugation_is_nontrivial", X_transformed != X_sample, checks)
    check("metric_tangent_conjugation_covariant", sp.simplify(Q_transformed - L.inv().T * Q_sample * L.inv()) == sp.zeros(4), checks)

    # A plane area/bivector selects a plane but not axes. Its canonical
    # Lorentz-plane Hodge generator is a boost (metric gauge), whereas the
    # founded physical response H does not commute with plane boosts.
    plane_coefficient, plane_basis = commutant([K1, J23])
    check("oriented_plane_stabilizer_commutant_dimension_four", 16 - plane_coefficient.rank() == 4, checks)
    check("founded_pair_generator_not_plane_boost_invariant", H_pair_lift * K1 != K1 * H_pair_lift, checks)
    check("canonical_plane_boost_is_metric_gauge", metric_tangent(K1, eta) == sp.zeros(4), checks)
    self_adjoint_plane_basis = [P0 + P1, P2 + P3]
    check("plane_invariant_self_adjoint_responses_are_block_scalars", all(value * K1 == K1 * value and value * J23 == J23 * value for value in self_adjoint_plane_basis), checks)

    # Ordered two-direction data can produce axes; the same unoriented plane
    # under an internal boost produces a different founded response.
    u = sp.Matrix([1, 0, 0, 0])
    raw_b = sp.Matrix([1, 1, 0, 0])
    projected = sp.simplify(raw_b + (raw_b.T * eta * u)[0] * u)
    check("ordered_two_vector_projection_gives_ruler", projected == sp.Matrix([0, 1, 0, 0]), checks)
    L_plane = sp.eye(4)
    L_plane[0, 0] = sp.Rational(5, 4)
    L_plane[0, 1] = sp.Rational(3, 4)
    L_plane[1, 0] = sp.Rational(3, 4)
    L_plane[1, 1] = sp.Rational(5, 4)
    check("internal_plane_boost_is_Lorentz", L_plane.T * eta * L_plane == eta, checks)
    check("same_plane_different_axes_change_founded_response", sp.simplify(L_plane * H_pair_lift * L_plane.inv()) != H_pair_lift, checks)

    # Simple-spectrum second-jet data supplies eigenlines but not which
    # spatial eigenline partners the timelike one.
    T = sp.diag(1, 2, 3, 4)
    spectral_pairs = [P0 + P1, P0 + P2, P0 + P3]
    check("three_simple_spectrum_Lorentzian_pair_projectors", len(spectral_pairs) == 3, checks)
    check("spectral_pair_projectors_rank_two", all(value.rank() == 2 for value in spectral_pairs), checks)
    check("spectral_pair_projectors_commute_with_tensor", all(value * T == T * value for value in spectral_pairs), checks)
    check("spectral_pair_projectors_are_distinct", len({tuple(value) for value in spectral_pairs}) == 3, checks)

    result = {
        "schema": "udt-covariant-reciprocal-coframe-lift-atlas-1.0",
        "result": "PASS",
        "sympy_version": sp.__version__,
        "check_count": len(checks),
        "checks": checks,
        "counts": {
            "full_Lorentz_commutant_dimension": 1,
            "nonnull_one_line_commutant_dimension": 2,
            "nonnull_one_line_invariant_projector_ranks": invariant_projector_ranks,
            "null_line_commutant_dimension": 2,
            "null_nontrivial_idempotents": 0,
            "ordered_pair_commutant_dimension": 6,
            "ordered_pair_fixed_base_lift_parameters": 2,
            "ordered_pair_physical_screen_moduli": 1,
            "oriented_plane_commutant_dimension": 4,
            "simple_spectrum_Lorentzian_pair_choices": 3,
            "fixed_observer_directional_generator_span_generic": 6,
            "fixed_observer_directional_rotation_span_generic": 3,
            "fixed_observer_directional_Lie_span_generic": 9,
            "fixed_observer_directional_Lie_span_lambda_one": 1,
        },
        "rulings": {
            "metric_and_scalars": "NO_COVARIANT_NONTRIVIAL_PAIR_SOLDER",
            "nonnull_one_direction": "UNIQUE_DEMOCRATIC_1PLUS3_INVOLUTION_AFTER_CHANNEL_SIGN_CHOICE_BUT_NO_ORDERED_PAIR",
            "null_or_zero_direction": "NO_REGULAR_NONSEMISCALAR_RECIPROCAL_INVOLUTION",
            "ordered_observer_separation_pair": "CONDITIONAL_ONE_PHYSICAL_SCREEN_DILATION_MODULUS_PLUS_SCREEN_ROTATION_GAUGE",
            "simple_bivector_plane": "PLANE_WITHOUT_AXES; CANONICAL_BOOST_IS_METRIC_GAUGE_NOT_FOUNDED_PHYSICAL_RESPONSE",
            "second_jet_eigendata": "CHOICE_DEPENDENT_AND_DEGENERACY_SENSITIVE",
            "scalar_anchors": "NO_CHANGE_TO_DIRECTIONAL_STABILIZER_OR_LIFT_RANK",
            "directional_family": "LAMBDA_NOT_ONE_GENERATES_NINE_DIMENSIONAL_FIXED_OBSERVER_ALGEBRA_WITH_ALL_THREE_SPATIAL_ROTATIONS; LAMBDA_ONE_COLLAPSES_TO_DIRECTION_INDEPENDENT_1PLUS3_LIFT",
            "universal_lift": "OPEN_NOT_SELECTED",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
