#!/usr/bin/env python3
"""Exact GR-subtraction and reciprocal-compatible conformal-connection algebra."""

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


def full_metric(base: sp.Matrix, cross: sp.Matrix, angular: sp.Matrix) -> sp.Matrix:
    return base.row_join(cross).col_join(cross.T.row_join(angular))


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
    b = sp.Matrix(sp.symbols("b0:4", real=True))
    expressions = []
    for direction in range(4):
        c = weyl_difference(metric, b, direction)
        expressions.extend(list(c * endomorphism - endomorphism * c))
    coefficients, _ = sp.linear_eq_to_matrix(expressions, tuple(b))
    return coefficients.rank()


def main() -> None:
    checks: dict[str, str] = {}
    eta = sp.diag(-1, 1, 1, 1)
    identity4 = sp.eye(4)
    swap = sp.Matrix([[0, 1], [1, 0]])
    l_direct = sp.diag(-1, 1, 0, 0)
    p_direct = l_direct**2

    # GR subtraction: a torsion-free metric-compatible connection difference
    # vanishes; a torsion-free conformal-compatible difference is exactly C(A).
    symmetric_pairs = [(b, c) for b in range(4) for c in range(b, 4)]
    difference_symbols = sp.symbols("c0:40", real=True)
    difference = [sp.zeros(4) for _ in range(4)]
    cursor = 0
    for upper in range(4):
        for b, c in symmetric_pairs:
            difference[b][upper, c] = difference_symbols[cursor]
            difference[c][upper, b] = difference_symbols[cursor]
            cursor += 1
    metric_equations = []
    for a in range(4):
        for b in range(4):
            for c in range(b, 4):
                metric_equations.append(
                    sum(difference[a][d, b] * eta[d, c] for d in range(4))
                    + sum(difference[a][d, c] * eta[b, d] for d in range(4))
                )
    metric_rank, metric_augmented, metric_nullity = linear_ranks(metric_equations, difference_symbols)
    require(
        "torsion_free_metric_connection_difference_zero",
        (metric_rank, metric_augmented, metric_nullity) == (40, 40, 0),
        checks,
    )

    a_symbols = sp.Matrix(sp.symbols("A0:4", real=True))
    weyl_differences = [weyl_difference(eta, a_symbols, direction) for direction in range(4)]
    for direction in range(4):
        c = weyl_differences[direction]
        for other in range(4):
            for upper in range(4):
                require_zero(
                    f"weyl_difference_torsion_free_{direction}_{other}_{upper}",
                    c[upper, other] - weyl_differences[other][upper, direction],
                    checks,
                )
        metric_derivative = -(c.T * eta + eta * c)
        require_zero(
            f"weyl_metric_compatibility_{direction}",
            metric_derivative + 2 * a_symbols[direction] * eta,
            checks,
        )
    sigma_gradient = sp.Matrix(sp.symbols("s0:4", real=True))
    for direction in range(4):
        require_zero(
            f"CSN_weyl_shift_{direction}",
            weyl_difference(eta, a_symbols, direction)
            - weyl_difference(eta, sigma_gradient, direction)
            - weyl_difference(eta, a_symbols - sigma_gradient, direction),
            checks,
        )

    # Conditional uniqueness of a conformal connection preserving the direct
    # normalized reciprocal generator or only its reciprocal-plane projector.
    require(
        "canonical_direct_L_difference_map_full_rank",
        connection_difference_rank(eta, l_direct) == 4,
        checks,
    )
    require(
        "canonical_direct_P_difference_map_full_rank",
        connection_difference_rank(eta, p_direct) == 4,
        checks,
    )

    recurrence = sp.symbols("rho0:4", real=True)
    recurrent_expressions = []
    for direction in range(4):
        c = weyl_difference(eta, a_symbols, direction)
        recurrent_expressions.extend(
            list(c * l_direct - l_direct * c - recurrence[direction] * l_direct)
        )
    recurrent_rank, recurrent_augmented, recurrent_nullity = linear_ranks(
        recurrent_expressions, tuple(a_symbols) + recurrence
    )
    require(
        "recurrent_normalized_L_collapses_to_exact",
        (recurrent_rank, recurrent_augmented, recurrent_nullity) == (8, 8, 0),
        checks,
    )
    require(
        "normalized_L_trace_square_nonzero",
        sp.trace(l_direct**2) == 2,
        checks,
    )

    # Repeat conditional uniqueness on every registered nonzero-cross full
    # metric witness. This checks that angular coupling does not create a
    # hidden Weyl one-form freedom.
    k = sp.symbols("k", real=True)
    epsilon = sp.Rational(1, 10)
    h_base = sp.Matrix([[1, -k], [-k, 1]])
    lifts = {
        "PLUS_IDENTITY": {
            "A": sp.eye(2),
            "C": sp.Matrix([[epsilon, epsilon], [epsilon, epsilon]]),
        },
        "MINUS_IDENTITY": {
            "A": -sp.eye(2),
            "C": sp.Matrix([[epsilon, epsilon], [-epsilon, -epsilon]]),
        },
        "AXIS_REFLECTION": {
            "A": sp.diag(1, -1),
            "C": sp.Matrix([[epsilon, epsilon], [epsilon, -epsilon]]),
        },
        "HOPF_EXCHANGE_LOCAL": {
            "A": swap,
            "C": sp.Matrix([[epsilon, epsilon], [epsilon, epsilon]]),
        },
    }
    uniqueness_witnesses = {}
    for name, data in lifts.items():
        seal = block_diagonal(swap, data["A"])
        metric_template = full_metric(h_base, data["C"], sp.eye(2))
        require_zero(f"{name}_seal_inverts_direct_L", seal * l_direct * seal + l_direct, checks)
        for kval in (2, 3):
            metric = metric_template.subs(k, kval)
            rank_l = connection_difference_rank(metric, l_direct)
            rank_p = connection_difference_rank(metric, p_direct)
            require(f"{name}_MU{kval**2}_L_uniqueness", rank_l == 4, checks)
            require(f"{name}_MU{kval**2}_P_uniqueness", rank_p == 4, checks)
            uniqueness_witnesses[f"{name}_MU{kval**2}"] = {
                "lift": name,
                "mu": kval**2,
                "nonzero_cross": "u=v=1/10",
                "L_difference_rank": rank_l,
                "P_difference_rank": rank_p,
                "result": "UNIQUE_IF_COMPATIBLE_NOT_EXISTENCE",
            }

    # Static reciprocal jet. At the normalized point, p=d(phi)/dr and h2,h3
    # are transverse coframe logarithmic rates. No representative or EOM is
    # selected by this local calculation.
    p, h2, h3 = sp.symbols("p h2 h3", real=True)
    derivatives = [sp.zeros(4) for _ in range(4)]
    derivatives[1] = sp.diag(2 * p, 2 * p, 2 * h2, 2 * h3)
    levi_civita = levi_civita_at_point(eta, derivatives)

    direct_solution = sp.Matrix([0, p, 0, 0])
    direct_general_residual = covariant_endomorphism(levi_civita, eta, a_symbols, l_direct)
    direct_residual = covariant_endomorphism(levi_civita, eta, direct_solution, l_direct)
    for direction, residual in enumerate(direct_residual):
        require_zero(
            f"direct_L_static_solution_{direction}",
            residual.subs({h2: -p, h3: -p}),
            checks,
        )

    direct_equations = flatten(direct_general_residual)
    direct_solutions = sp.solve(direct_equations, list(a_symbols) + [h2, h3], dict=True)
    require(
        "direct_L_static_solution_unique_form",
        direct_solutions
        == [{a_symbols[0]: 0, a_symbols[1]: p, a_symbols[2]: 0, a_symbols[3]: 0, h2: -p, h3: -p}],
        checks,
    )

    splitting_equations = flatten(covariant_endomorphism(levi_civita, eta, a_symbols, p_direct))
    splitting_solutions = sp.solve(splitting_equations, list(a_symbols) + [h2], dict=True)
    require(
        "splitting_preservation_solution",
        splitting_solutions
        == [{a_symbols[0]: 0, a_symbols[1]: -h3, a_symbols[2]: 0, a_symbols[3]: 0, h2: h3}],
        checks,
    )
    require(
        "splitting_preservation_leaves_phi_rate_free",
        p not in set().union(*(solution.keys() for solution in splitting_solutions)),
        checks,
    )

    # Direct founding extension with a locally nonexpanding transverse block is
    # inconsistent for p!=0: one equation requires A_r=p while transverse
    # comparison requires A_r=0.
    direct_flat_angular = [expression.subs({p: 1, h2: 0, h3: 0}) for expression in direct_equations]
    obstruction_rank, obstruction_augmented, _ = linear_ranks(direct_flat_angular, tuple(a_symbols))
    require(
        "direct_static_nonzero_phi_obstruction",
        (obstruction_rank, obstruction_augmented) == (4, 5),
        checks,
    )
    require_zero(
        "direct_obstruction_clock_equation",
        direct_general_residual[0][0, 1] - (2 * a_symbols[1] - 2 * p),
        checks,
    )
    require_zero(
        "direct_obstruction_transverse_equation",
        direct_general_residual[2][1, 2] - (a_symbols[1] + h2),
        checks,
    )

    # The complete seal classes allow a nonzero angular reciprocal generator
    # only when the angular seal itself has one + and one - eigendirection.
    m11, m12, m21, m22 = sp.symbols("m11 m12 m21 m22", real=True)
    m = sp.Matrix([[m11, m12], [m21, m22]])
    extension_results = {}
    for name, data in lifts.items():
        angular = data["A"]
        equations = list(angular * m * angular + m)
        solution = sp.solve(equations, [m11, m12, m21, m22], dict=True)
        if name in ("PLUS_IDENTITY", "MINUS_IDENTITY"):
            require(f"{name}_angular_generator_only_zero", solution == [{m11: 0, m12: 0, m21: 0, m22: 0}], checks)
            extension_results[name] = {
                "angular_generator_family": "ZERO_ONLY",
                "normalized_full_rank_example": "NONE",
                "status": "DIRECT_TRANSVERSE_IDENTITY_ONLY",
            }
        elif name == "AXIS_REFLECTION":
            require(f"{name}_angular_generator_offdiagonal", solution == [{m11: 0, m22: 0}], checks)
            m_example = swap
            require_zero(f"{name}_angular_generator_normalized", m_example**2 - sp.eye(2), checks)
            extension_results[name] = {
                "angular_generator_family": "[[0,a],[b,0]] with ab=1 after normalization",
                "normalized_full_rank_example": "J",
                "status": "CONDITIONAL_FULL_TWO_PAIR_EXTENSION_AVAILABLE",
            }
        else:
            require(f"{name}_angular_generator_traceless_family", solution == [{m11: -m22, m12: -m21}], checks)
            m_example = sp.diag(-1, 1)
            require_zero(f"{name}_angular_generator_normalized", m_example**2 - sp.eye(2), checks)
            extension_results[name] = {
                "angular_generator_family": "[[a,b],[-b,-a]] with a^2-b^2=1 after normalization",
                "normalized_full_rank_example": "diag(-1,+1)",
                "status": "CONDITIONAL_FULL_TWO_PAIR_EXTENSION_AVAILABLE",
            }

    # Conditional full two-pair completion in the Hopf-exchange basis.
    l_full_plus = sp.diag(-1, 1, -1, 1)
    l_full_minus = sp.diag(-1, 1, 1, -1)
    hopf_seal = block_diagonal(swap, swap)
    require_zero("Hopf_seal_inverts_full_L_plus", hopf_seal * l_full_plus * hopf_seal + l_full_plus, checks)
    require_zero("Hopf_seal_inverts_full_L_minus", hopf_seal * l_full_minus * hopf_seal + l_full_minus, checks)
    require("full_L_plus_difference_map_full_rank", connection_difference_rank(eta, l_full_plus) == 4, checks)
    require("full_L_minus_difference_map_full_rank", connection_difference_rank(eta, l_full_minus) == 4, checks)

    full_plus_equations = flatten(covariant_endomorphism(levi_civita, eta, a_symbols, l_full_plus))
    full_plus_solutions = sp.solve(full_plus_equations, list(a_symbols) + [h2], dict=True)
    require(
        "full_L_plus_static_solution",
        full_plus_solutions
        == [{a_symbols[0]: 0, a_symbols[1]: p, a_symbols[2]: 0, a_symbols[3]: 0, h2: -p}],
        checks,
    )
    full_minus_equations = flatten(covariant_endomorphism(levi_civita, eta, a_symbols, l_full_minus))
    full_minus_solutions = sp.solve(full_minus_equations, list(a_symbols) + [h3], dict=True)
    require(
        "full_L_minus_static_solution",
        full_minus_solutions
        == [{a_symbols[0]: 0, a_symbols[1]: p, a_symbols[2]: 0, a_symbols[3]: 0, h3: -p}],
        checks,
    )
    require_zero(
        "angular_reciprocity_completes_plus_weights",
        (h2 + h3).subs({h2: -p, h3: p}),
        checks,
    )
    require_zero(
        "angular_reciprocity_completes_minus_weights",
        (h2 + h3).subs({h2: p, h3: -p}),
        checks,
    )

    # Exact all-profile witness in the preferred reciprocal representative.
    z = sp.symbols("z", positive=True)
    profile_metric = sp.diag(-z**-2, z**2, z**-2, z**2)
    profile_derivatives = [sp.zeros(4) for _ in range(4)]
    profile_derivatives[1] = sp.diag(2 * p * z**-2, 2 * p * z**2, -2 * p * z**-2, 2 * p * z**2)
    profile_lc = levi_civita_at_point(profile_metric, profile_derivatives)
    profile_residual = covariant_endomorphism(profile_lc, profile_metric, direct_solution, l_full_plus)
    for direction, residual in enumerate(profile_residual):
        require_zero(f"full_two_pair_exact_profile_{direction}", residual, checks)

    # Reciprocal character derivative. Parallel normalized L does not freeze
    # phi; it gives the exact group current D^-1 nabla D=d(phi)L.
    phi, dphi = sp.symbols("phi dphi", real=True)
    character_direct = sp.diag(sp.exp(-phi), sp.exp(phi), 1, 1)
    require_zero(
        "direct_character_current",
        character_direct.inv() * sp.diff(character_direct, phi) * dphi - dphi * l_direct,
        checks,
    )
    character_full = sp.diag(sp.exp(-phi), sp.exp(phi), sp.exp(-phi), sp.exp(phi))
    require_zero(
        "full_character_current",
        character_full.inv() * sp.diff(character_full, phi) * dphi - dphi * l_full_plus,
        checks,
    )

    # Exact CSN-invariant weight statement: common coframe scale shifts clock
    # and angular log-rates equally, leaving their difference unchanged.
    common_rate = sp.symbols("common_rate", real=True)
    require_zero(
        "clock_angular_weight_equality_CSN_invariant",
        ((-p + common_rate) - (h2 + common_rate)).subs(h2, -p),
        checks,
    )
    require_zero(
        "angular_reciprocal_sum_removes_common_rate_after_quotient",
        ((h2 + common_rate) - common_rate + (h3 + common_rate) - common_rate).subs({h2: -p, h3: p}),
        checks,
    )

    output = {
        "schema": "udt-gr-subtraction-reciprocal-connection-derivation-1.0",
        "maximum_conclusion": "UDT_GR_SUBTRACTION_RECIPROCAL_CONNECTION_STATUS_CHARACTERIZED",
        "check_count": len(checks),
        "checks": dict(sorted(checks.items())),
        "outcomes": [
            "RECIPROCAL_COMPATIBILITY_UNIQUE_IF_IT_EXISTS",
            "RECURRENT_NORMALIZED_RECIPROCITY_COLLAPSES_TO_EXACT_PARALLELISM",
            "SPLITTING_PRESERVATION_IS_STRICTLY_WEAKER",
            "DIRECT_TRANSVERSE_IDENTITY_STATIC_JET_HAS_NONZERO_INTRINSIC_OBSTRUCTION",
            "CONDITIONAL_FULL_TWO_PAIR_EXTENSION_REMOVES_LOCAL_OBSTRUCTION",
            "CONDITIONAL_FULL_TWO_PAIR_PLUS_ANGULAR_RECIPROCITY_YIELDS_HOPF_ORBIT_WEIGHTS",
            "SEAL_OR_FINITE_CELL_DOES_NOT_CURRENTLY_SUPPLY_BULK_CONNECTION_EXISTENCE",
            "CONNECTION_UNIQUENESS_WITH_EXISTENCE_OPEN",
            "CONDITIONAL_HOPF_STRUCTURE_DIAGNOSES_BUT_DOES_NOT_SELECT_CONNECTION",
        ],
        "gr_subtraction": {
            "torsion_free_metric_compatible_difference": "ZERO_UNIQUE",
            "torsion_free_conformal_difference": "ONE_FORM_A",
            "CSN_change": "g->exp(2sigma)g; A->A-dsigma; affine connection unchanged",
            "field_equations_used": False,
        },
        "conditional_uniqueness_witnesses": uniqueness_witnesses,
        "direct_extension": {
            "generator": "diag(-1,+1,0,0)",
            "difference_map_rank": 4,
            "static_compatibility": "A_r=dphi; h2=h3=-dphi",
            "locally_constant_transverse_block_with_nonzero_dphi": "INCONSISTENT_RANK_4_AUGMENTED_5",
            "areal_gauge_condition": "d log(R_angular)=-dphi",
            "status": "UNIQUE_IF_EXISTS_BUT_GENERIC_FOUNDING_ANGULAR_READOUT_OBSTRUCTED",
        },
        "splitting_only": {
            "projector": "L^2=diag(1,1,0,0)",
            "static_compatibility": "h2=h3=h; A_r=-h; dphi free",
            "status": "STRICTLY_WEAKER_THAN_NORMALIZED_GENERATOR_PRESERVATION",
        },
        "angular_generator_extensions": extension_results,
        "conditional_full_two_pair": {
            "generator_plus": "diag(-1,+1,-1,+1)",
            "generator_minus": "diag(-1,+1,+1,-1)",
            "seal": "diag(J,J)",
            "connection": "unique torsion-free Weyl connection if compatible; A=dphi in reciprocal representative",
            "plus_compatibility": "h2=-dphi; h3 unrestricted before angular reciprocity",
            "minus_compatibility": "h3=-dphi; h2 unrestricted before angular reciprocity",
            "angular_reciprocity": "h2+h3=0",
            "completed_orbit_weights": "diag(exp(-2phi),exp(+2phi)) up to exchange and positive common scale",
            "prior_match": "exact conditional Hopf orbit block",
            "foundation_status": "CONDITIONAL_TRANSVERSE_REALIZATION_NOT_DERIVED",
        },
        "smallest_missing_principle": {
            "question": "Does UDT reciprocity remain one longitudinal dual pair or extend as a complete two-pair reduction of the four-dimensional conformal frame bundle?",
            "direct_extension": "foundation-default faithful vector extension leaves transverse identity",
            "full_extension": "coherent with connection compatibility and conditional Hopf weights but not selected",
            "selection_status": "OPEN",
        },
        "scope": {
            "complete": "torsion-free conformal connection difference algebra and registered local lift/jet classes",
            "not_covered": [
                "derivation of transverse physical reciprocal realization",
                "torsion or non-Weyl nonmetricity",
                "global cover periods caps and boundary functional",
                "action field equations physical evolution and bootstrap selector",
                "carrier emergence soliton stability mass scale and canonization",
            ],
        },
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
