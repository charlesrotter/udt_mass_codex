#!/usr/bin/env python3
"""Exact algebra for metric-native and seal-native two-pair selector candidates."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def require(name: str, condition, checks: dict[str, str]) -> None:
    if not bool(condition):
        raise AssertionError(name)
    checks[name] = "PASS"


def require_zero(name: str, expression, checks: dict[str, str]) -> None:
    value = sp.simplify(expression)
    if isinstance(value, sp.MatrixBase):
        good = value == sp.zeros(*value.shape)
    else:
        good = value == 0
    require(name, good, checks)


def flatten(matrices):
    return [entry for matrix in matrices for entry in list(matrix)]


def linear_ranks(expressions, variables):
    coefficients, rhs = sp.linear_eq_to_matrix(expressions, variables)
    return coefficients.rank(), coefficients.row_join(rhs).rank(), len(variables) - coefficients.rank()


def block_diagonal(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    output = sp.zeros(left.rows + right.rows)
    output[: left.rows, : left.cols] = left
    output[left.rows :, left.cols :] = right
    return output


def full_metric(base: sp.Matrix, cross: sp.Matrix, angular: sp.Matrix) -> sp.Matrix:
    return base.row_join(cross).col_join(cross.T.row_join(angular))


def oriented_complex_structure(metric: sp.Matrix) -> sp.Matrix:
    a, b, d = metric[0, 0], metric[0, 1], metric[1, 1]
    return sp.Matrix([[-b, -d], [a, b]]) / sp.sqrt(sp.det(metric))


def weyl_difference(metric: sp.Matrix, one_form: sp.Matrix, direction: int) -> sp.Matrix:
    inverse = metric.inv()
    raised = inverse * one_form
    output = sp.zeros(4)
    for upper in range(4):
        for lower in range(4):
            output[upper, lower] = (
                (1 if upper == direction else 0) * one_form[lower]
                + (1 if upper == lower else 0) * one_form[direction]
                - metric[direction, lower] * raised[upper]
            )
    return output


def levi_civita_at_point(metric: sp.Matrix, derivatives: list[sp.Matrix]) -> list[sp.Matrix]:
    inverse = metric.inv()
    output = []
    for direction in range(4):
        connection = sp.zeros(4)
        for upper in range(4):
            for lower in range(4):
                connection[upper, lower] = sp.Rational(1, 2) * sum(
                    inverse[upper, d]
                    * (
                        derivatives[direction][d, lower]
                        + derivatives[lower][d, direction]
                        - derivatives[d][direction, lower]
                    )
                    for d in range(4)
                )
        output.append(sp.simplify(connection))
    return output


def covariant_endomorphism(
    levi_civita: list[sp.Matrix], metric: sp.Matrix, one_form: sp.Matrix, endomorphism: sp.Matrix
) -> list[sp.Matrix]:
    return [
        sp.simplify(
            (levi_civita[a] + weyl_difference(metric, one_form, a)) * endomorphism
            - endomorphism * (levi_civita[a] + weyl_difference(metric, one_form, a))
        )
        for a in range(4)
    ]


def main() -> None:
    checks: dict[str, str] = {}
    identity2 = sp.eye(2)
    zero2 = sp.zeros(2)
    j_euclidean = sp.Matrix([[0, -1], [1, 0]])
    reflection = sp.diag(1, -1)
    exchange = sp.Matrix([[0, 1], [1, 0]])

    # Metric (plus orientation) alone cannot select a real angular reciprocal
    # involution. The complete self-adjoint O(2)-commutant is scalar.
    x11, x12, x21, x22 = sp.symbols("x11 x12 x21 x22", real=True)
    x = sp.Matrix([[x11, x12], [x21, x22]])
    metric_only_equations = list(x * j_euclidean - j_euclidean * x) + list(x.T - x)
    metric_rank, metric_augmented, metric_nullity = linear_ranks(
        metric_only_equations, (x11, x12, x21, x22)
    )
    require(
        "O2_natural_self_adjoint_endomorphism_is_scalar",
        (metric_rank, metric_augmented, metric_nullity) == (3, 3, 1),
        checks,
    )
    metric_tracefree = metric_only_equations + [sp.trace(x)]
    require(
        "O2_natural_tracefree_self_adjoint_endomorphism_is_zero",
        linear_ranks(metric_tracefree, (x11, x12, x21, x22)) == (4, 4, 0),
        checks,
    )
    require_zero("orientation_complex_structure_squares_minus_identity", j_euclidean**2 + identity2, checks)

    # A supplied longitudinal plane leaves an O(2) stabilizer on its positive
    # complement. A scalar or a non-null gradient can select at most a 1+3
    # split unless a non-isotropic screen tensor is additionally supplied.
    eta = sp.diag(-1, 1, 1, 1)
    screen_rotation = block_diagonal(identity2, j_euclidean)
    y_symbols = sp.symbols("y0:16", real=True)
    y = sp.Matrix(4, 4, y_symbols)
    screen_commutant_equations = list(y * screen_rotation - screen_rotation * y)
    screen_self_adjoint_equations = list(y.T * eta - eta * y)
    rank_screen, _, nullity_screen = linear_ranks(
        screen_commutant_equations + screen_self_adjoint_equations, y_symbols
    )
    require("longitudinal_plane_plus_metric_retains_screen_symmetry", nullity_screen > 1, checks)
    require("longitudinal_plane_commutant_rank_recorded", rank_screen + nullity_screen == 16, checks)

    # A trace-free symmetric screen tensor gives a unique normalized local
    # involution wherever it is nonzero, but fails on the isotropic stratum.
    a, b = sp.symbols("a b", real=True)
    shear = sp.Matrix([[a, b], [b, -a]])
    shear_norm_sq = a**2 + b**2
    require_zero("screen_shear_square", shear**2 - shear_norm_sq * identity2, checks)
    require_zero("screen_shear_trace", sp.trace(shear), checks)
    shear_z = sp.diag(1, -1)
    shear_x = exchange
    require_zero("shear_z_normalized", shear_z**2 - identity2, checks)
    require_zero("shear_x_normalized", shear_x**2 - identity2, checks)
    require("independent_screen_tensors_select_different_axes", shear_z not in (shear_x, -shear_x), checks)
    require("isotropic_screen_tensor_has_zero_norm", shear_norm_sq.subs({a: 0, b: 0}) == 0, checks)

    # Projected trace-free Hessian is conformally natural on a screen on which
    # dphi vanishes: a conformal Hessian correction is pure trace there.
    scale, pure_trace = sp.symbols("scale pure_trace", positive=True)
    hessian_screen = shear_z + pure_trace * identity2
    tracefree_original = hessian_screen - sp.trace(hessian_screen) * identity2 / 2
    scaled_metric = scale**2 * identity2
    scaled_endomorphism = scaled_metric.inv() * tracefree_original
    scaled_norm = sp.sqrt(sp.trace(scaled_endomorphism**2) / 2)
    require_zero(
        "normalized_projected_Hessian_is_CSN_invariant",
        scaled_endomorphism / scaled_norm - shear_z,
        checks,
    )

    # Seal-local theorem. On a positive oriented two-plane, a q-orthogonal
    # reflection R determines M=J_q R. It is a normalized self-adjoint
    # complementary reflection and is unique up to orientation/sign.
    q1, q2 = sp.symbols("q1 q2", positive=True)
    q_axis = sp.diag(q1, q2)
    j_axis = oriented_complex_structure(q_axis)
    m_axis = sp.simplify(j_axis * reflection)
    require_zero("axis_J_square", j_axis**2 + identity2, checks)
    require_zero("axis_reflection_isometry", reflection.T * q_axis * reflection - q_axis, checks)
    require_zero("axis_M_normalized", m_axis**2 - identity2, checks)
    require_zero("axis_M_tracefree", sp.trace(m_axis), checks)
    require_zero("axis_M_self_adjoint", m_axis.T * q_axis - q_axis * m_axis, checks)
    require_zero("axis_M_anticommutes_with_seal", reflection * m_axis * reflection + m_axis, checks)

    seal_equations = list(reflection * x * reflection + x) + list(x.T * q_axis - q_axis * x)
    seal_rank, _, seal_nullity = linear_ranks(seal_equations, (x11, x12, x21, x22))
    require("reflection_self_adjoint_anticommutant_is_one_dimensional", (seal_rank, seal_nullity) == (3, 1), checks)
    require_zero("reflection_orientation_flip_exchanges_M_sign", (-j_axis) * reflection + m_axis, checks)

    # Without the metric-derived J/self-adjoint relation, seal inversion alone
    # leaves a continuous normalized family.
    u = sp.symbols("u", nonzero=True, real=True)
    seal_only_family = sp.Matrix([[0, u], [1 / u, 0]])
    require_zero("seal_only_family_normalized", seal_only_family**2 - identity2, checks)
    require_zero(
        "seal_only_family_anticommutes", reflection * seal_only_family * reflection + seal_only_family, checks
    )

    # The +/- identity angular lifts cannot support any nonzero normalized
    # anticommuting angular generator.
    for name, angular_seal in (("PLUS_IDENTITY", identity2), ("MINUS_IDENTITY", -identity2)):
        equations = list(angular_seal * x * angular_seal + x)
        rank_value, _, nullity_value = linear_ranks(equations, (x11, x12, x21, x22))
        require(f"{name}_anticommutant_zero", (rank_value, nullity_value) == (4, 0), checks)

    # Hopf exchange is the same local reflection conjugacy class. Its complete
    # invariant positive metric has equal diagonal entries.
    qa, qb = sp.symbols("qa qb", real=True)
    q_hopf = sp.Matrix([[qa, qb], [qb, qa]])
    j_hopf = oriented_complex_structure(q_hopf)
    m_hopf = sp.simplify(j_hopf * exchange)
    require_zero("Hopf_exchange_metric_isometry", exchange.T * q_hopf * exchange - q_hopf, checks)
    require_zero("Hopf_J_square", j_hopf**2 + identity2, checks)
    require_zero("Hopf_M_normalized", m_hopf**2 - identity2, checks)
    require_zero("Hopf_M_self_adjoint", m_hopf.T * q_hopf - q_hopf * m_hopf, checks)
    require_zero("Hopf_M_anticommutes", exchange * m_hopf * exchange + m_hopf, checks)

    # Nonzero base-angular coupling does not spoil the seal-local theorem. Use
    # the exact Schur complement/orthogonal screen in both registered mu
    # witnesses of the orientation-preserving axis-reflection lift.
    epsilon = sp.Rational(1, 10)
    l_base = sp.diag(-1, 1)
    cross = sp.Matrix([[epsilon, epsilon], [epsilon, -epsilon]])
    angular_identity = identity2
    u_base = sp.Matrix.vstack(identity2, zero2)
    cross_witnesses = {}
    for k in (2, 3):
        base = sp.Matrix([[1, -k], [-k, 1]])
        metric4 = full_metric(base, cross, angular_identity)
        screen_metric = sp.simplify(angular_identity - cross.T * base.inv() * cross)
        screen_embedding = sp.Matrix.vstack(-base.inv() * cross, identity2)
        split_frame = u_base.row_join(screen_embedding)
        full_seal = block_diagonal(exchange, reflection)
        j_screen = oriented_complex_structure(screen_metric)
        m_screen = sp.simplify(j_screen * reflection)
        l_full = sp.simplify(split_frame * block_diagonal(l_base, m_screen) * split_frame.inv())
        require_zero(f"MU{k*k}_orthogonal_split", u_base.T * metric4 * screen_embedding, checks)
        require_zero(f"MU{k*k}_screen_metric_pullback", screen_embedding.T * metric4 * screen_embedding - screen_metric, checks)
        require(f"MU{k*k}_screen_positive_first_minor", screen_metric[0, 0] > 0, checks)
        require(f"MU{k*k}_screen_positive_determinant", sp.det(screen_metric) > 0, checks)
        require_zero(f"MU{k*k}_seal_isometry", full_seal.T * metric4 * full_seal - metric4, checks)
        require_zero(f"MU{k*k}_screen_seal_isometry", reflection.T * screen_metric * reflection - screen_metric, checks)
        require_zero(f"MU{k*k}_screen_M_normalized", m_screen**2 - identity2, checks)
        require_zero(f"MU{k*k}_full_L_normalized", l_full**2 - sp.eye(4), checks)
        require_zero(f"MU{k*k}_full_L_tracefree", sp.trace(l_full), checks)
        require_zero(f"MU{k*k}_full_seal_inverts_L", full_seal * l_full * full_seal + l_full, checks)
        require_zero(
            f"MU{k*k}_split_frame_recovers_base_and_screen_generators",
            split_frame.inv() * l_full * split_frame - block_diagonal(l_base, m_screen),
            checks,
        )
        cross_witnesses[f"MU{k*k}"] = {
            "mu": k**2,
            "screen_metric": str(screen_metric),
            "screen_generator": str(m_screen),
            "result": "SEAL_LOCAL_COMPLEMENTARY_PAIR_EXISTS_UP_TO_SIGN",
        }

    # Bulk continuation has a curvature/holonomy integrability gate. A
    # rotation holonomy does not preserve a reflection M.
    theta = sp.pi / 4
    rotation = sp.Matrix([[sp.cos(theta), -sp.sin(theta)], [sp.sin(theta), sp.cos(theta)]])
    require("quarter_rotation_changes_reflection", sp.simplify(rotation * shear_z * rotation.T) != shear_z, checks)
    require_zero("full_turn_preserves_reflection", (-identity2) * shear_z * (-identity2) - shear_z, checks)
    require("curvature_rotation_fails_commutant", j_euclidean * shear_z - shear_z * j_euclidean != zero2, checks)

    # Exact product with a curved round angular screen. At sin(theta)=3/5,
    # cos(theta)=4/5, neither full two-pair orientation admits a torsion-free
    # Weyl one-form preserving fixed angular reciprocal axes. The direct
    # transverse-zero generator remains compatible at constant phi.
    round_metric = sp.diag(-1, 1, 1, sp.Rational(9, 25))
    round_derivatives = [sp.zeros(4) for _ in range(4)]
    round_derivatives[2][3, 3] = sp.Rational(24, 25)
    round_lc = levi_civita_at_point(round_metric, round_derivatives)
    one_form = sp.Matrix(sp.symbols("A0:4", real=True))
    direct_l = sp.diag(-1, 1, 0, 0)
    full_plus = sp.diag(-1, 1, -1, 1)
    full_minus = sp.diag(-1, 1, 1, -1)
    round_results = {}
    for name, generator, expected in (
        ("DIRECT_TRANSVERSE_ZERO", direct_l, (4, 4, 0)),
        ("FULL_PLUS", full_plus, (4, 5, 0)),
        ("FULL_MINUS", full_minus, (4, 5, 0)),
    ):
        equations = flatten(covariant_endomorphism(round_lc, round_metric, one_form, generator))
        ranks = linear_ranks(equations, tuple(one_form))
        require(f"round_screen_{name}_rank", ranks == expected, checks)
        round_results[name] = {
            "coefficient_rank": ranks[0],
            "augmented_rank": ranks[1],
            "status": "COMPATIBLE" if ranks[0] == ranks[1] else "INTRINSIC_ANGULAR_OBSTRUCTION",
        }

    # Flat angular screens give positive local witnesses but do not select an
    # axis: every reflected axis angle is equally metric-compatible.
    alpha = sp.symbols("alpha", real=True)
    rotation_alpha = sp.Matrix([[sp.cos(alpha), -sp.sin(alpha)], [sp.sin(alpha), sp.cos(alpha)]])
    reflection_family = sp.simplify(rotation_alpha * shear_z * rotation_alpha.T)
    require_zero("flat_reflection_family_normalized", reflection_family**2 - identity2, checks)
    require_zero("flat_reflection_family_tracefree", sp.trace(reflection_family), checks)
    require("flat_metric_has_continuous_axis_family", reflection_family.subs(alpha, 0) != reflection_family.subs(alpha, sp.pi / 4), checks)

    # Global round-screen diagnostic. A self-adjoint involution would split
    # TS2 into real eigenline bundles. The exact Euler number is nonzero, so
    # the standard line-field obstruction applies; the flat torus control has
    # zero Euler number but still retains a continuous axis family.
    theta_symbol, psi_symbol = sp.symbols("theta_symbol psi_symbol", real=True)
    sphere_curvature_integral = sp.integrate(
        sp.integrate(sp.sin(theta_symbol), (psi_symbol, 0, 2 * sp.pi)),
        (theta_symbol, 0, sp.pi),
    )
    require_zero("unit_sphere_Gauss_Bonnet_integral", sphere_curvature_integral - 4 * sp.pi, checks)
    require_zero("unit_sphere_Euler_number_two", sphere_curvature_integral / (2 * sp.pi) - 2, checks)

    output = {
        "schema": "udt-metric-native-two-pair-selector-derivation-1.0",
        "maximum_conclusion": "UDT_METRIC_NATIVE_TWO_PAIR_SELECTOR_STATUS_CHARACTERIZED",
        "check_count": len(checks),
        "checks": dict(sorted(checks.items())),
        "outcomes": [
            "NO_UNCONDITIONAL_METRIC_NATIVE_TWO_PAIR_SELECTOR_IN_AUDITED_CLASS",
            "METRIC_ORIENTATION_ALONE_DOES_NOT_SELECT_ANGULAR_RECIPROCAL_AXES",
            "HESSIAN_OR_CURVATURE_ANISOTROPY_SELECTS_ONLY_ON_NONDEGENERATE_STRATA",
            "ANGULAR_REFLECTION_SEAL_PLUS_SCREEN_METRIC_SELECTS_COMPLEMENTARY_PAIR_UP_TO_SIGN_AT_SEAL",
            "IDENTITY_ANGULAR_SEAL_LIFTS_FORBID_A_NONZERO_ANTICOMMUTING_SECOND_PAIR",
            "COMPLETE_ANGULAR_SEAL_LIFT_REMAINS_UNSELECTED",
            "BULK_PARALLEL_EXTENSION_REQUIRES_UNSELECTED_HOLONOMY_REDUCTION",
            "ROUND_INTRINSIC_ANGULAR_SCREEN_OBSTRUCTS_FIXED_FULL_TWO_PAIR_WEYL_TRANSPORT_IN_PRODUCT_CLASS",
            "ROUND_S2_SCREEN_HAS_GLOBAL_EIGENLINE_OBSTRUCTION",
            "DIRECT_TRANSVERSE_ZERO_AND_FULL_TWO_PAIR_REALIZATIONS_REMAIN_INEQUIVALENT",
            "CONDITIONAL_SEAL_TO_BULK_JOIN_SHARPENED",
        ],
        "metric_naturality": {
            "metric_plus_orientation": "only scalar self-adjoint tangent endomorphisms; Hodge J squares to -I",
            "longitudinal_pair_plus_metric": "retains O(2) screen stabilizer and no reciprocal screen axes",
            "tracefree_screen_tensor": "normalized involution wherever nonzero; undefined on isotropic stratum",
            "multiple_tensor_candidates": "can select inequivalent axes with no current priority rule",
        },
        "seal_local_theorem": {
            "premises": "positive screen metric q and q-orthogonal orientation-reversing angular seal R",
            "construction": "M=J_q R",
            "properties": "M^2=I; tr(M)=0; M is q-self-adjoint; RMR=-M",
            "uniqueness": "up to global orientation/sign exchange",
            "identity_lifts": "no nonzero anticommuting M",
            "authority": "CONDITIONAL_ON_UNSELECTED_COMPLETE_ANGULAR_SEAL_LIFT_AND_SEAL_LOCAL_ONLY",
            "nonzero_cross_witnesses": cross_witnesses,
        },
        "bulk_continuation": {
            "necessary_condition": "[Omega,L]=0 for every curvature/holonomy generator when nabla L=0",
            "generic_rotation_holonomy": "does not preserve a reciprocal reflection",
            "round_screen_product": round_results,
            "flat_screen": "admits a continuous family and therefore does not select one without seal/framing data",
            "authority": "RECIPROCAL_PARALLELISM_AND_HOLONOMY_REDUCTION_NOT_CURRENTLY_DERIVED",
        },
        "smallest_missing_join": {
            "first": "select the orientation-preserving complete seal class whose angular action is a reflection",
            "second": "derive a bulk continuation/holonomy-reduction law for the seal-local reciprocal pair",
            "combined_question": "Does complete Reciprocity require the finite-cell seal to seed a globally integrable two-pair reduction?",
            "status": "OPEN",
        },
        "scope": {
            "complete": "enumerated local metric/phi Hessian curvature-eigensplitting and registered seal classes through the declared second-derivative algebra",
            "not_covered": [
                "arbitrary higher jets and nonlocal spectral constructions",
                "torsionful or non-Weyl connection families",
                "derived selection of complete angular seal lift",
                "global cover periods caps topology and boundary dynamics",
                "action field equations bootstrap functional carrier source mass and canonization",
            ],
        },
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
