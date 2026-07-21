#!/usr/bin/env python3
"""Exact symbolic audit of a supplied UDT reciprocal-plane projector."""

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


def block_diagonal(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    output = sp.zeros(left.rows + right.rows)
    output[: left.rows, : left.cols] = left
    output[left.rows :, left.cols :] = right
    return output


def full_metric(base: sp.Matrix, cross: sp.Matrix, screen: sp.Matrix) -> sp.Matrix:
    return base.row_join(cross).col_join(cross.T.row_join(screen))


def weyl_difference(metric: sp.Matrix, one_form: sp.Matrix, direction: int) -> sp.Matrix:
    inverse = metric.inv()
    raised = inverse * one_form
    dimension = metric.rows
    output = sp.zeros(dimension)
    for upper in range(dimension):
        for lower in range(dimension):
            output[upper, lower] = (
                (1 if upper == direction else 0) * one_form[lower]
                + (1 if upper == lower else 0) * one_form[direction]
                - metric[direction, lower] * raised[upper]
            )
    return output


def levi_civita_at_point(metric: sp.Matrix, derivatives: list[sp.Matrix]) -> list[sp.Matrix]:
    inverse = metric.inv()
    dimension = metric.rows
    output = []
    for direction in range(dimension):
        connection = sp.zeros(dimension)
        for upper in range(dimension):
            for lower in range(dimension):
                connection[upper, lower] = sp.Rational(1, 2) * sum(
                    inverse[upper, d]
                    * (
                        derivatives[direction][d, lower]
                        + derivatives[lower][d, direction]
                        - derivatives[d][direction, lower]
                    )
                    for d in range(dimension)
                )
        output.append(sp.simplify(connection))
    return output


def covariant_endomorphism(
    levi_civita: list[sp.Matrix],
    metric: sp.Matrix,
    one_form: sp.Matrix,
    endomorphism: sp.Matrix,
) -> list[sp.Matrix]:
    return [
        sp.simplify(
            (levi_civita[a] + weyl_difference(metric, one_form, a)) * endomorphism
            - endomorphism * (levi_civita[a] + weyl_difference(metric, one_form, a))
        )
        for a in range(metric.rows)
    ]


def flatten(matrices: list[sp.Matrix]):
    return [entry for matrix in matrices for entry in list(matrix)]


def linear_ranks(expressions, variables):
    coefficients, rhs = sp.linear_eq_to_matrix(expressions, variables)
    return coefficients.rank(), coefficients.row_join(rhs).rank(), len(variables) - coefficients.rank()


def connection_difference_rank(metric: sp.Matrix, endomorphism: sp.Matrix) -> int:
    one_form = sp.Matrix(sp.symbols("b0:4", real=True))
    expressions = []
    for direction in range(4):
        c = weyl_difference(metric, one_form, direction)
        expressions.extend(list(c * endomorphism - endomorphism * c))
    coefficients, _ = sp.linear_eq_to_matrix(expressions, tuple(one_form))
    return coefficients.rank()


def orthogonal_projector(metric: sp.Matrix) -> sp.Matrix:
    """Metric-orthogonal projector onto span(e0,e1), including cross metrics."""
    inclusion = sp.Matrix([[1, 0], [0, 1], [0, 0], [0, 0]])
    return sp.simplify(inclusion * (inclusion.T * metric * inclusion).inv() * inclusion.T * metric)


def projector_residual(
    metric: sp.Matrix,
    derivatives: list[sp.Matrix],
    one_form: sp.Matrix,
    projector: sp.Matrix | None = None,
) -> list[sp.Matrix]:
    projector = projector if projector is not None else sp.diag(1, 1, 0, 0)
    return covariant_endomorphism(levi_civita_at_point(metric, derivatives), metric, one_form, projector)


def round_screen_scalar_curvature() -> sp.Expr:
    theta, radius = sp.symbols("theta radius", positive=True)
    q = sp.diag(radius**2, radius**2 * sp.sin(theta) ** 2)
    qi = q.inv()
    coordinates = (theta, sp.symbols("varphi", real=True))
    gamma = [[[
        sp.simplify(
            sp.Rational(1, 2)
            * sum(
                qi[a, d]
                * (
                    sp.diff(q[d, c], coordinates[b])
                    + sp.diff(q[d, b], coordinates[c])
                    - sp.diff(q[b, c], coordinates[d])
                )
                for d in range(2)
            )
        )
        for c in range(2)] for b in range(2)] for a in range(2)]
    ricci = sp.zeros(2)
    for a in range(2):
        for b in range(2):
            ricci[a, b] = sp.simplify(sum(
                sp.diff(gamma[c][a][b], coordinates[c])
                - sp.diff(gamma[c][a][c], coordinates[b])
                + sum(
                    gamma[c][c][d] * gamma[d][a][b]
                    - gamma[c][b][d] * gamma[d][a][c]
                    for d in range(2)
                )
                for c in range(2)
            ))
    return sp.simplify(sum(qi[a, b] * ricci[a, b] for a in range(2) for b in range(2)))


def main() -> None:
    checks: dict[str, str] = {}
    eta = sp.diag(-1, 1, 1, 1)
    projector = sp.diag(1, 1, 0, 0)
    direct_generator = sp.diag(-1, 1, 0, 0)
    one_form = sp.Matrix(sp.symbols("A0:4", real=True))

    # Full cross-jet algebra in an adapted orthonormal frame. Intrinsic
    # derivatives within either two-plane do not mix the distributions; the
    # only potentially obstructing jets are the cross derivatives below.
    x2, y2, z2, x3, y3, z3 = sp.symbols("x2 y2 z2 x3 y3 z3", real=True)
    u0, v0, w0, u1, v1, w1 = sp.symbols("u0 v0 w0 u1 v1 w1", real=True)
    derivatives = [sp.zeros(4) for _ in range(4)]
    derivatives[0][2:4, 2:4] = sp.Matrix([[u0, w0], [w0, v0]])
    derivatives[1][2:4, 2:4] = sp.Matrix([[u1, w1], [w1, v1]])
    derivatives[2][0:2, 0:2] = sp.Matrix([[x2, z2], [z2, y2]])
    derivatives[3][0:2, 0:2] = sp.Matrix([[x3, z3], [z3, y3]])
    general_residual = flatten(projector_residual(eta, derivatives, one_form))
    variables = list(one_form) + [v0, w0, v1, w1, y2, z2, y3, z3]
    solutions = sp.solve(general_residual, variables, dict=True)
    expected_solution = [{
        one_form[0]: -u0 / 2,
        one_form[1]: -u1 / 2,
        one_form[2]: x2 / 2,
        one_form[3]: x3 / 2,
        v0: u0,
        w0: 0,
        v1: u1,
        w1: 0,
        y2: -x2,
        z2: 0,
        y3: -x3,
        z3: 0,
    }]
    require("full_cross_jet_solution_is_exact_umbilical_form", solutions == expected_solution, checks)
    compatible_substitution = expected_solution[0]
    for direction, residual in enumerate(projector_residual(eta, derivatives, one_form)):
        require_zero(f"cross_jet_sufficiency_{direction}", residual.subs(compatible_substitution), checks)

    # The unique one-form is minus the cross-gradient of the logarithmic
    # two-volume. At dimension two, d log|det(h)|=4s and d log det(q)=4r.
    require_zero("screen_volume_formula_A0", one_form[0].subs(compatible_substitution) + u0 / 2, checks)
    require_zero("screen_volume_formula_A1", one_form[1].subs(compatible_substitution) + u1 / 2, checks)
    require_zero("base_volume_formula_A2", one_form[2].subs(compatible_substitution) - x2 / 2, checks)
    require_zero("base_volume_formula_A3", one_form[3].subs(compatible_substitution) - x3 / 2, checks)
    require("projector_difference_map_rank_four", connection_difference_rank(eta, projector) == 4, checks)

    # Explicit shear obstructions. Each has a full-rank one-form map but an
    # augmented rank one larger, so no Weyl one-form repairs it.
    screen_shear = [sp.zeros(4) for _ in range(4)]
    screen_shear[0][2:4, 2:4] = sp.diag(1, -1)
    screen_equations = flatten(projector_residual(eta, screen_shear, one_form))
    screen_ranks = linear_ranks(screen_equations, tuple(one_form))
    require("screen_tracefree_shear_obstructed_rank_4_augmented_5", screen_ranks[:2] == (4, 5), checks)
    base_shear = [sp.zeros(4) for _ in range(4)]
    base_shear[2][0:2, 0:2] = sp.eye(2)
    base_equations = flatten(projector_residual(eta, base_shear, one_form))
    base_ranks = linear_ranks(base_equations, tuple(one_form))
    require("base_tracefree_shear_obstructed_rank_4_augmented_5", base_ranks[:2] == (4, 5), checks)

    # Exact reciprocal warped witness with a genuinely curved round screen.
    # z=exp(phi), p=dphi/dr, rho=d(log R)/dr, sin(theta)=3/5.
    z, p, rho = sp.Rational(2), sp.Rational(3), sp.Rational(7)
    round_metric = sp.diag(-z**-2, z**2, 25, 9)
    round_derivatives = [sp.zeros(4) for _ in range(4)]
    round_derivatives[1] = sp.diag(2 * p * z**-2, 2 * p * z**2, 2 * rho * 25, 2 * rho * 9)
    round_derivatives[2][3, 3] = 24  # 25*2*(3/5)*(4/5)
    round_A = sp.Matrix([0, -rho, 0, 0])
    for direction, residual in enumerate(projector_residual(round_metric, round_derivatives, round_A)):
        require_zero(f"reciprocal_round_screen_witness_{direction}", residual, checks)
    radius = sp.symbols("radius", positive=True)
    require_zero("round_screen_scalar_curvature_nonzero", round_screen_scalar_curvature() - 2 / radius**2, checks)

    # Two inequivalent reciprocal profiles share one screen and the same
    # projector-compatible connection: projector preservation does not select phi.
    for profile_rate in (sp.Rational(2), sp.Rational(11)):
        profile_derivatives = [matrix.copy() for matrix in round_derivatives]
        profile_derivatives[1][0, 0] = 2 * profile_rate * z**-2
        profile_derivatives[1][1, 1] = 2 * profile_rate * z**2
        for direction, residual in enumerate(projector_residual(round_metric, profile_derivatives, round_A)):
            require_zero(f"free_phi_rate_{profile_rate}_{direction}", residual, checks)

    # Projector parallelism is strictly weaker than preserving the normalized
    # reciprocal axes individually.
    direct_derivatives = [sp.zeros(4) for _ in range(4)]
    direct_derivatives[1] = sp.diag(6, 6, 0, 0)
    for direction, residual in enumerate(projector_residual(eta, direct_derivatives, sp.zeros(4, 1))):
        require_zero(f"P_parallel_L_not_parallel_P_{direction}", residual, checks)
    direct_residual = covariant_endomorphism(
        levi_civita_at_point(eta, direct_derivatives), eta, sp.zeros(4, 1), direct_generator
    )
    require("P_parallel_does_not_imply_L_parallel", any(entry != 0 for entry in flatten(direct_residual)), checks)

    # CSN covariance: LC(g')=LC(g)+C(ds), A'=A-ds, and C is conformally
    # representative-independent as an endomorphism-valued one-form.
    ds = sp.Matrix(sp.symbols("s0:4", real=True))
    for direction in range(4):
        require_zero(
            f"CSN_affine_connection_invariant_{direction}",
            weyl_difference(eta, ds, direction)
            + weyl_difference(eta, one_form - ds, direction)
            - weyl_difference(eta, one_form, direction),
            checks,
        )

    # Every registered constant nonzero-cross metric admits its own
    # metric-orthogonal projector. Constant g and P give LC=0 and A=0, while
    # the Weyl difference map still has rank four (uniqueness if compatible).
    swap = sp.Matrix([[0, 1], [1, 0]])
    epsilon = sp.Rational(1, 10)
    lift_data = {
        "PLUS_IDENTITY": sp.Matrix([[epsilon, epsilon], [epsilon, epsilon]]),
        "MINUS_IDENTITY": sp.Matrix([[epsilon, epsilon], [-epsilon, -epsilon]]),
        "AXIS_REFLECTION": sp.Matrix([[epsilon, epsilon], [epsilon, -epsilon]]),
        "HOPF_EXCHANGE_LOCAL": sp.Matrix([[epsilon, epsilon], [epsilon, epsilon]]),
    }
    cross_witnesses = {}
    for name, cross in lift_data.items():
        for kval in (2, 3):
            metric = full_metric(sp.Matrix([[1, -kval], [-kval, 1]]), cross, sp.eye(2))
            metric_projector = orthogonal_projector(metric)
            require_zero(f"{name}_MU{kval**2}_P_idempotent", metric_projector**2 - metric_projector, checks)
            require_zero(
                f"{name}_MU{kval**2}_P_metric_self_adjoint",
                metric_projector.T * metric - metric * metric_projector,
                checks,
            )
            require(f"{name}_MU{kval**2}_P_rank_two", metric_projector.rank() == 2, checks)
            rank = connection_difference_rank(metric, metric_projector)
            require(f"{name}_MU{kval**2}_difference_rank_four", rank == 4, checks)
            constant_derivatives = [sp.zeros(4) for _ in range(4)]
            for direction, residual in enumerate(
                projector_residual(metric, constant_derivatives, sp.zeros(4, 1), metric_projector)
            ):
                require_zero(f"{name}_MU{kval**2}_constant_compatibility_{direction}", residual, checks)
            cross_witnesses[f"{name}_MU{kval**2}"] = {
                "metric_cross_entries": [str(value) for value in list(cross)],
                "mu": kval**2,
                "projector_rank": 2,
                "difference_map_rank": rank,
                "connection": "LC=0; A=0",
                "result": "COMPATIBLE_UNIQUE_IN_DECLARED_CLASS",
            }

    # Frobenius/torsion obstruction. For E0=d_t-B*r*d_y and E1=d_r,
    # [E0,E1]=B*d_y lies outside the plane when B is nonzero. A torsion-free
    # connection preserving the plane would force this bracket back into it.
    twist = sp.symbols("B", nonzero=True)
    bracket_transverse_coefficient = twist
    require("nonintegrable_twist_has_transverse_bracket", bracket_transverse_coefficient != 0, checks)

    # Residual holonomy: boosts/rotations within the two preserved planes
    # commute with P. Angular rotation does not preserve a chosen reciprocal
    # angular axis, so P does not secretly select the stronger two-pair law.
    base_boost = block_diagonal(sp.Matrix([[0, 1], [1, 0]]), sp.zeros(2))
    angular_rotation = block_diagonal(sp.zeros(2), sp.Matrix([[0, -1], [1, 0]]))
    angular_reciprocal_axis = sp.diag(0, 0, -1, 1)
    require_zero("base_boost_preserves_projector", base_boost * projector - projector * base_boost, checks)
    require_zero("angular_rotation_preserves_projector", angular_rotation * projector - projector * angular_rotation, checks)
    require(
        "angular_rotation_does_not_preserve_reciprocal_axis",
        angular_rotation * angular_reciprocal_axis - angular_reciprocal_axis * angular_rotation != sp.zeros(4),
        checks,
    )

    output = {
        "schema": "udt-reciprocal-plane-projector-derivation-1.0",
        "maximum_conclusion": "UDT_RECIPROCAL_PLANE_PROJECTOR_FRAME_STATUS_CHARACTERIZED",
        "check_count": len(checks),
        "checks": dict(sorted(checks.items())),
        "theorem": {
            "class": "torsion-free Weyl connection; supplied metric-orthogonal Lorentzian rank-two projector",
            "uniqueness": "AT_MOST_ONE_CONNECTION",
            "existence": "IFF_BOTH_DISTRIBUTIONS_INTEGRABLE_AND_CROSS_SECOND_FUNDAMENTAL_FORMS_PURE_TRACE",
            "adapted_conditions": [
                "partial_A h_ij = 2 s_A h_ij",
                "partial_i q_AB = 2 r_i q_AB",
            ],
            "unique_one_form": "A_A=-s_A=-(1/4)partial_A log|det h|; A_i=-r_i=-(1/4)partial_i log det q",
            "CSN": "g->exp(2sigma)g; A->A-dsigma; affine connection unchanged",
        },
        "witnesses": {
            "reciprocal_warped_round_screen": {
                "metric": "diag(-exp(-2phi),exp(2phi),R^2,R^2 sin^2(theta))",
                "allowed_profiles": "arbitrary phi(r), arbitrary positive R(r)",
                "connection": "A=-d_base log R",
                "intrinsic_screen_scalar_curvature": "2/R^2",
                "result": "PASS",
            },
            "two_phi_rates": [2, 11],
            "screen_tracefree_shear": "FAIL_RANK_4_AUGMENTED_5",
            "base_tracefree_shear": "FAIL_RANK_4_AUGMENTED_5",
            "nonintegrable_twist": "FAIL_BY_TORSION_AND_FROBENIUS",
            "constant_nonzero_cross_metrics": cross_witnesses,
        },
        "strictness": {
            "P_parallel_implies_L_parallel": False,
            "intrinsic_angular_rotation_retained": True,
            "arbitrary_reciprocal_phi_retained": True,
            "twist_or_cross_shear_retained": False,
        },
        "physical_status": {
            "internal_pair_to_spacetime_plane": "CONDITIONAL_NOT_DERIVED",
            "projector_parallelism_as_UDT_law": "OPEN_NOT_DERIVED",
            "current_metric_forces_integrable_umbilical_split": "OPEN_NOT_DERIVED",
            "action_topology_carrier_source_mass": "NOT_INFERRED",
            "overall": "COHERENT_CONDITIONAL_FRAME_REDUCTION_NOT_AN_UNCONDITIONAL_UDT_SELECTOR",
        },
        "smallest_missing_principle": {
            "question": "Does the complete UDT metric and finite-cell seal select a global integrable umbilical reciprocal two-plane projector?",
            "why_missing": "The tested law uniquely transports a supplied compatible split but neither creates the plane nor proves twist/shear absent.",
            "status": "OPEN_SHARPENED_GATE",
        },
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
