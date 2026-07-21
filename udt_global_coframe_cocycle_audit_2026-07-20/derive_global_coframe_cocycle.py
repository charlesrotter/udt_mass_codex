#!/usr/bin/env python3
"""Exact algebra for the global reciprocal-coframe cocycle audit."""

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


def symmetric_tangent_dimensions(transform: sp.Matrix) -> dict[str, int]:
    variables = sp.symbols("h0:10")
    perturbation = sp.zeros(4)
    index = 0
    for row in range(4):
        for column in range(row, 4):
            perturbation[row, column] = variables[index]
            perturbation[column, row] = variables[index]
            index += 1
    dimensions: dict[str, int] = {}
    for label, sign in (("even", 1), ("odd", -1)):
        equations = list(transform.T * perturbation * transform - sign * perturbation)
        matrix, _ = sp.linear_eq_to_matrix(equations, variables)
        dimensions[label] = len(variables) - matrix.rank()
    return dimensions


def main() -> None:
    checks: dict[str, str] = {}
    b, c, a, d, z = sp.symbols("b c a d z", real=True, nonzero=True)
    A, B, C, phi = sp.symbols("A B C phi", real=True, nonzero=True)
    omega = sp.symbols("omega", positive=True)
    theta, psi = sp.symbols("theta psi", real=True)

    def F(value):
        return sp.Matrix([[0, value], [1 / value, 0]])

    def G(value):
        return sp.diag(value, 1 / value)

    reciprocal = sp.diag(1 / z, z)
    dual_metric = sp.Matrix([[0, 1], [1, 0]])
    diagonal_readout = sp.diag(-1, 1)
    reciprocal_metric_K = sp.simplify(reciprocal.T * dual_metric * reciprocal)
    reciprocal_metric_eta = sp.simplify(reciprocal.T * diagonal_readout * reciprocal)

    # Local reciprocal group and its Z2 grading.
    require_zero("F_is_involution", F(b) * F(b) - sp.eye(2), checks)
    require_zero(
        "F_inverts_reciprocal_character",
        F(b) * reciprocal * F(b) - reciprocal.inv(),
        checks,
    )
    require_zero("G_group_law", G(a) * G(d) - G(a * d), checks)
    require_zero("F_F_is_preserving", F(b) * F(c) - G(b / c), checks)
    require_zero("G_F_is_inverting", G(a) * F(b) - F(a * b), checks)
    require_zero("F_G_is_inverting", F(b) * G(a) - F(b / a), checks)
    require_zero("three_inversions_remain_inverting", F(b) * F(c) * F(d) - F(b * d / c), checks)
    require_zero(
        "valid_triple_cocycle_needs_preserving_third_transition",
        F(b) * F(c) * G(c / b) - sp.eye(2),
        checks,
    )
    require(
        "three_inverting_overlap_maps_cannot_multiply_to_identity",
        (F(b) * F(c) * F(d))[0, 0] == 0 and (F(b) * F(c) * F(d))[0, 1] != 0,
        checks,
    )
    require_zero(
        "four_inversion_loop_constraint",
        F(b) * F(c) * F(d) * F(a) - G(b * d / (c * a)),
        checks,
    )

    # Readout and conjugacy classification.
    require_zero("dual_metric_preserved_by_F", F(b).T * dual_metric * F(b) - dual_metric, checks)
    require_zero("dual_metric_preserved_by_G", G(a).T * dual_metric * G(a) - dual_metric, checks)
    require_zero(
        "K_readout_makes_reciprocal_character_metric_invisible",
        reciprocal_metric_K - dual_metric,
        checks,
    )
    require_zero(
        "eta_readout_retains_reciprocal_metric_dilation",
        reciprocal_metric_eta - sp.diag(-(z**-2), z**2),
        checks,
    )
    require_zero(
        "balanced_swap_is_anti_isometry_between_eta_mirror_representatives",
        F(1).T * reciprocal_metric_eta.subs(z, 1 / z) * F(1) + reciprocal_metric_eta,
        checks,
    )
    diagonal_pullback = sp.simplify(F(b).T * diagonal_readout * F(b))
    require_zero(
        "diagonal_pullback_exact",
        diagonal_pullback - sp.diag(b ** -2, -(b**2)),
        checks,
    )
    require(
        "no_positive_CSN_diagonal_readout_isometry",
        sp.sign(diagonal_pullback[0, 0]) == 1
        and sp.sign(omega**2 * diagonal_readout[0, 0]) == -1,
        checks,
    )
    # Complete constant symmetric readout family compatible with the F_b mirror.
    # For a general H0=[[A,B],[B,C]], the off-diagonal mirror equation forces
    # Omega^2=1 when B!=0, and the diagonal equations then force C=A*b^2.
    reciprocal_operator = sp.diag(sp.exp(-phi), sp.exp(phi))
    mirror_scale_squared = sp.symbols("mirror_scale_squared", positive=True)
    general_readout = sp.Matrix([[A, B], [B, C]])
    general_metric = sp.simplify(
        reciprocal_operator.T * general_readout * reciprocal_operator
    )
    general_mirror_equations = sp.simplify(
        F(b).T * general_metric.subs(phi, -phi) * F(b)
        - mirror_scale_squared * general_metric
    )
    require_zero(
        "general_mirror_equation_classification",
        general_mirror_equations
        - sp.Matrix(
            [
                [
                    sp.exp(-2 * phi)
                    * (C / b**2 - mirror_scale_squared * A),
                    B * (1 - mirror_scale_squared),
                ],
                [
                    B * (1 - mirror_scale_squared),
                    sp.exp(2 * phi)
                    * (A * b**2 - mirror_scale_squared * C),
                ],
            ]
        ),
        checks,
    )
    require(
        "nonzero_cross_term_forces_unit_mirror_scale",
        sp.solve(general_mirror_equations[0, 1], mirror_scale_squared) == [1],
        checks,
    )
    require_zero(
        "unit_mirror_scale_forces_C_equals_A_b_squared",
        general_mirror_equations.subs(
            {mirror_scale_squared: 1, C: A * b**2}
        ),
        checks,
    )
    require(
        "zero_cross_term_cannot_give_Lorentz_mirror_family",
        general_readout.det().subs({B: 0, C: A * b**2}) == A**2 * b**2,
        checks,
    )
    mixed_readout = sp.Matrix([[A, B], [B, A * b**2]])
    mixed_metric = sp.simplify(reciprocal_operator.T * mixed_readout * reciprocal_operator)
    require_zero(
        "mixed_readout_exact_mirror_isometry",
        F(b).T * mixed_metric.subs(phi, -phi) * F(b) - mixed_metric,
        checks,
    )
    require_zero(
        "mixed_readout_constant_determinant",
        mixed_metric.det() - (A**2 * b**2 - B**2),
        checks,
    )
    require(
        "mixed_readout_lorentz_witness",
        mixed_readout.subs({A: 1, B: -2, b: 1}).det() == -3,
        checks,
    )
    require(
        "mixed_readout_phi_visible_when_A_nonzero",
        sp.diff(mixed_metric, phi) != sp.zeros(2),
        checks,
    )
    require_zero(
        "pure_K_is_phi_invisible_limit",
        mixed_metric.subs(A, 0) - sp.Matrix([[0, B], [B, 0]]),
        checks,
    )
    common_scale = sp.symbols("common_scale", positive=True)
    transformed_readout = sp.simplify(
        common_scale**2 * G(a).T * mixed_readout * G(a)
    )
    mixed_modulus = sp.simplify(B**2 / (mixed_readout[0, 0] * mixed_readout[1, 1]))
    transformed_modulus = sp.simplify(
        transformed_readout[0, 1] ** 2
        / (transformed_readout[0, 0] * transformed_readout[1, 1])
    )
    require_zero(
        "mixed_readout_modulus_CSN_and_diagonal_gauge_invariant",
        transformed_modulus - mixed_modulus,
        checks,
    )
    hadamard = sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2)
    spatial_mirror_readout = mixed_readout.subs({A: 1, B: -2, b: 1})
    require_zero(
        "mixed_readout_anchor_diagonalizes_to_Lorentz_form",
        hadamard.T * spatial_mirror_readout * hadamard - sp.diag(-1, 3),
        checks,
    )
    require_zero(
        "mixed_readout_seal_becomes_standard_spatial_reflection",
        hadamard.T * F(1) * hadamard - sp.diag(1, -1),
        checks,
    )
    full_mirror_plus_angular = sp.diag(1, 1, 1, 1)
    full_mirror_plus_angular[:2, :2] = F(1)
    mixed_full_witnesses: dict[str, dict[str, object]] = {}
    for label, cross_term in (("MU4", -2), ("MU9", -3)):
        witness_readout = mixed_readout.subs({A: 1, B: cross_term, b: 1})
        witness_metric = mixed_metric.subs({A: 1, B: cross_term, b: 1})
        full_metric = sp.diag(1, 1, 1, 1)
        full_metric[:2, :2] = witness_metric
        require_zero(
            f"{label}_full_four_metric_mirror_isometry",
            full_mirror_plus_angular.T
            * full_metric.subs(phi, -phi)
            * full_mirror_plus_angular
            - full_metric,
            checks,
        )
        require(
            f"{label}_full_four_metric_Lorentz_signature_witness",
            witness_readout.det() < 0 and full_metric.det() < 0,
            checks,
        )
        mixed_full_witnesses[label] = {
            "A": 1,
            "B": cross_term,
            "b": 1,
            "mu": cross_term**2,
            "angular_lift": "+I",
            "mirror_isometry": True,
            "Lorentz_determinant_at_seal": int(witness_readout.det()),
        }
    require(
        "mixed_readout_modulus_survives_full_direct_extension",
        {row["mu"] for row in mixed_full_witnesses.values()} == {4, 9},
        checks,
    )
    conjugated = sp.simplify(G(a) * F(b) * G(a).inv())
    require_zero("boost_conjugates_F_magnitude", conjugated - F(a**2 * b), checks)

    fixed_vector = sp.Matrix([b, 1])
    antifixed_vector = sp.Matrix([-b, 1])
    require_zero("F_fixed_vector", F(b) * fixed_vector - fixed_vector, checks)
    require_zero("F_antifixed_vector", F(b) * antifixed_vector + antifixed_vector, checks)
    fixed_norm = sp.simplify((fixed_vector.T * dual_metric * fixed_vector)[0])
    antifixed_norm = sp.simplify((antifixed_vector.T * dual_metric * antifixed_vector)[0])
    require_zero("F_fixed_norm", fixed_norm - 2 * b, checks)
    require_zero("F_antifixed_norm", antifixed_norm + 2 * b, checks)

    # Angular involutions and corner products.
    def rotation(angle):
        return sp.Matrix(
            [[sp.cos(angle), -sp.sin(angle)], [sp.sin(angle), sp.cos(angle)]]
        )

    def angular_reflection(angle):
        return sp.simplify(rotation(angle) * sp.diag(1, -1) * rotation(angle).T)

    angular_theta = angular_reflection(theta)
    angular_psi = angular_reflection(psi)
    require_zero("angular_reflection_involution", angular_theta**2 - sp.eye(2), checks)
    require_zero("angular_reflection_orientation", angular_theta.det() + 1, checks)
    require_zero(
        "angular_reflection_product_rotation",
        angular_theta * angular_psi - rotation(2 * (theta - psi)),
        checks,
    )
    commutator = sp.simplify(angular_theta * angular_psi - angular_psi * angular_theta)
    require_zero(
        "angular_reflection_commutator_formula",
        commutator
        - sp.Matrix(
            [
                [0, -2 * sp.sin(2 * (theta - psi))],
                [2 * sp.sin(2 * (theta - psi)), 0],
            ]
        ),
        checks,
    )
    require_zero(
        "same_axis_reflections_commute",
        commutator.subs({theta: 0, psi: 0}),
        checks,
    )
    require_zero(
        "perpendicular_axis_reflections_commute",
        commutator.subs({theta: 0, psi: sp.pi / 2}),
        checks,
    )
    require(
        "oblique_axis_reflections_do_not_commute",
        commutator.subs({theta: 0, psi: sp.pi / 6}) != sp.zeros(2),
        checks,
    )
    require_zero(
        "order_three_angular_corner_witness",
        (angular_theta * angular_psi).subs({theta: 0, psi: -sp.pi / 3}) ** 3
        - sp.eye(2),
        checks,
    )
    require_zero("same_parameter_base_corner", F(2) * F(2) - sp.eye(2), checks)
    require_zero("opposite_parameter_even_corner", (F(2) * F(-2)) ** 2 - sp.eye(2), checks)
    require(
        "generic_base_corner_has_infinite_order",
        (F(2) * F(1)) ** 4 != sp.eye(2),
        checks,
    )

    # Full 4-coframe classes, orientation, and induced metric-tangent dimensions.
    angular_classes = {
        "ANGULAR_PLUS_IDENTITY": sp.eye(2),
        "ANGULAR_MINUS_IDENTITY": -sp.eye(2),
        "ANGULAR_AXIS_REFLECTION": sp.diag(1, -1),
    }
    full_classes: dict[str, dict[str, object]] = {}
    for name, angular in angular_classes.items():
        transform = sp.diag(1, 1, 1, 1)
        transform[:2, :2] = F(1)
        transform[2:, 2:] = angular
        require_zero(f"{name}_full_involution", transform**2 - sp.eye(4), checks)
        fixed_dimension = 4 - (transform - sp.eye(4)).rank()
        antifixed_dimension = 4 - (transform + sp.eye(4)).rank()
        tangent_dimensions = symmetric_tangent_dimensions(transform)
        require(
            f"{name}_dimension_partition",
            fixed_dimension + antifixed_dimension == 4
            and tangent_dimensions["even"] + tangent_dimensions["odd"] == 10,
            checks,
        )
        full_classes[name] = {
            "determinant": int(transform.det()),
            "coframe_fixed_dimension": fixed_dimension,
            "coframe_antifixed_dimension": antifixed_dimension,
            "symmetric_metric_even_dimension": tangent_dimensions["even"],
            "symmetric_metric_odd_dimension": tangent_dimensions["odd"],
            "trace": int(transform.trace()),
        }
    require(
        "full_class_invariants_are_distinct",
        len(
            {
                (
                    row["determinant"],
                    row["coframe_fixed_dimension"],
                    row["symmetric_metric_even_dimension"],
                )
                for row in full_classes.values()
            }
        )
        == 3,
        checks,
    )
    require(
        "static_delta_phi_is_not_complete_metric_tangent_rule",
        10 - 1
        not in {
            row["symmetric_metric_even_dimension"] for row in full_classes.values()
        },
        checks,
    )

    # Primitive mirror-compatible cap lattices retain multiple global topologies.
    cap_pairs = {
        "SAME_CYCLE_P0": ((1, 1), (1, 1)),
        "AXIS_EXCHANGE_P1": ((1, 0), (0, 1)),
        "MIRROR_LENS_P3": ((2, 1), (1, 2)),
        "MIRROR_LENS_P5": ((3, 2), (2, 3)),
    }
    cap_results: dict[str, dict[str, object]] = {}
    for name, (left, right) in cap_pairs.items():
        left_gcd = sp.gcd(abs(left[0]), abs(left[1]))
        right_gcd = sp.gcd(abs(right[0]), abs(right[1]))
        determinant = abs(left[0] * right[1] - left[1] * right[0])
        require(f"{name}_primitive", left_gcd == 1 and right_gcd == 1, checks)
        cap_results[name] = {
            "left_cycle": list(left),
            "right_cycle": list(right),
            "absolute_determinant": determinant,
            "primitive": True,
        }
    require(
        "primitive_mirror_caps_do_not_select_one_lattice",
        {row["absolute_determinant"] for row in cap_results.values()} == {0, 1, 3, 5},
        checks,
    )

    outcome = {
        "schema": "udt-global-coframe-cocycle-audit-1.0",
        "result": "PASS",
        "checks": checks,
        "reciprocal_transition_group": {
            "preserving_component": "G_a=diag(a,1/a)",
            "inverting_component": "F_b=[[0,b],[1/b,0]]",
            "grading": "Z2; odd=inverting; every closed cocycle has even inversion parity",
            "triple_overlap": (
                "three inverting transitions cannot close; two inverting transitions require a "
                "preserving third transition"
            ),
            "conjugacy": (
                "G_a F_b G_a^-1=F_(a^2 b); magnitude is gauge-conjugate inside each sign, "
                "while sign(b) remains a real conjugacy invariant"
            ),
        },
        "readout_ruling": {
            "diagonal_clock_radial": "NO_CONSTANT_POSITIVE_CSN_ISOMETRIC_INVERTING_LIFT",
            "dual_K_as_physical_null_metric": "CONDITIONAL_O11_LIFT_FAMILY",
            "readout_tradeoff": {
                "K": "P^T K P=K, so isolated reciprocal phi is metric-invisible/pure frame boost",
                "eta": "P^T eta P=diag(-z^-2,z^2), so phi is metric-visible but the balanced mirror swap is an anti-isometry",
                "required_join": "a source-authorized full-metric soldering/readout that retains physical reciprocal dilation and closes the seal",
            },
            "mixed_readout_family": {
                "H0": "[[A,B],[B,A*b^2]]",
                "g_phi": "[[A*exp(-2phi),B],[B,A*b^2*exp(2phi)]]",
                "Lorentz_condition": "B^2>A^2*b^2",
                "mirror": "F_b^T g(-phi) F_b=g(phi)",
                "phi_visible_condition": "A!=0",
                "pure_K_limit": "A=0",
                "dimensionless_unselected_modulus": "mu=B^2/(A^2*b^2)>1",
                "conditional_spatial_witness": "A=1; B=-2; b=1 diagonalizes to diag(-1,3) while F becomes diag(1,-1)",
                "status": "EXACT_CONDITIONAL_FAMILY_NOT_SELECTED",
            },
            "K_fixed_norm": str(fixed_norm),
            "K_antifixed_norm": str(antifixed_norm),
            "conditional_sign_interpretation": {
                "b_negative": "fixed line timelike and anti-fixed line spacelike in K convention",
                "b_positive": "fixed line spacelike and anti-fixed line timelike in K convention",
            },
            "status": "MIXED_READOUT_FAMILY_EXISTS; PHYSICAL_SOLDERING_AND_MODULUS_SELECTION_OPEN",
        },
        "full_local_lift_classes": full_classes,
        "mixed_readout_full_witnesses": mixed_full_witnesses,
        "corner_ruling": {
            "commuting_base_reflections": "requires c=+b or c=-b",
            "commuting_angular_axis_reflections": "requires same or perpendicular axes modulo pi",
            "finite_order_base_product": "requires b/c=1, or b/c=-1 with even order",
            "finite_order_angular_product": "requires theta-psi=pi*k/m for declared order m",
            "status": "REDUCES_AFTER_CORNER_ORDER_AND_INCIDENCE_ARE_SUPPLIED; DOES_NOT_SELECT_THEM",
        },
        "cap_lattice_witnesses": cap_results,
        "boundary_tangent_ruling": {
            "full_symmetric_metric_dimension": 10,
            "static_delta_phi_zero_removes": 1,
            "remaining_after_static_phi_only": 9,
            "involution_even_dimensions": {
                name: row["symmetric_metric_even_dimension"] for name, row in full_classes.items()
            },
            "involution_odd_dimensions": {
                name: row["symmetric_metric_odd_dimension"] for name, row in full_classes.items()
            },
            "polarization": "NOT_SELECTED_BY_INVOLUTION; conditional C2 delta-h/delta-K choices remain",
        },
        "outcomes": [
            "MULTIPLE_GLOBAL_COMPLETIONS_SURVIVE_CONDITIONALLY",
            "COCYCLE_CONSISTENCY_REDUCES_BUT_DOES_NOT_SELECT",
            "GLOBAL_COCYCLE_CANNOT_BE_POSED_WITHOUT_OPEN_TOPOLOGY_OR_COVER",
            "BOUNDARY_TANGENT_SPACE_REMAINS_POLARIZATION_DEPENDENT",
            "CURRENT_DATA_DEFINE_ONLY_LOCAL_OR_SECTORWISE_INVOLUTIONS",
        ],
        "outcome_not_earned": "UNIQUE_GLOBAL_COFRAME_AND_TANGENT_COMPLETION_IN_AUDITED_CLASS",
        "smallest_local_gate": (
            "source-authorized physical soldering/slot map and selection of the mixed-readout "
            "modulus compatible with the observational clock/ruler anchor"
        ),
        "smallest_global_gate_after_local_readout": (
            "a founded chart/corner/cap incidence structure carrying the Z2 reciprocal transition "
            "cocycle"
        ),
        "maximum_conclusion": "UDT_GLOBAL_COFRAME_COCYCLE_STATUS_CHARACTERIZED",
        "compute": {"cpu_only": True, "gpu_used": False, "sympy": sp.__version__},
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(outcome, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "result": outcome["result"],
                "checks": len(checks),
                "outcomes": len(outcome["outcomes"]),
                "unique": False,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
