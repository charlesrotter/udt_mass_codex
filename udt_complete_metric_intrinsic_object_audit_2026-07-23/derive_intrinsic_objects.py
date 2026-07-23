#!/usr/bin/env python3
"""Exact intrinsic-object census for the registered complete UDT metric.

This script classifies geometric object types.  It does not define an action,
field equation, carrier, boundary condition, topology, or physical dynamics.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def is_zero(value: sp.Expr | sp.MatrixBase) -> bool:
    if isinstance(value, sp.MatrixBase):
        return all(sp.simplify(item) == 0 for item in value)
    return sp.simplify(value) == 0


def matrix_commutant(generators: list[sp.Matrix]) -> tuple[sp.Matrix, list[sp.Symbol]]:
    n = generators[0].rows
    variables = list(sp.symbols(f"x0:{n*n}"))
    unknown = sp.Matrix(n, n, variables)
    equations: list[sp.Expr] = []
    for generator in generators:
        equations.extend(list(unknown * generator - generator * unknown))
    solution = next(iter(sp.linsolve(equations, variables)))
    return sp.Matrix(n, n, solution), variables


def linear_solution_dimension(expressions: list[sp.Expr], variables: list[sp.Symbol]) -> int:
    coefficient, _ = sp.linear_eq_to_matrix(expressions, variables)
    return len(variables) - coefficient.rank()


def lorentz_generators() -> list[sp.Matrix]:
    generators: list[sp.Matrix] = []
    for spatial in (1, 2, 3):
        boost = sp.zeros(4)
        boost[0, spatial] = 1
        boost[spatial, 0] = 1
        generators.append(boost)
    for left, right in ((1, 2), (1, 3), (2, 3)):
        rotation = sp.zeros(4)
        rotation[left, right] = -1
        rotation[right, left] = 1
        generators.append(rotation)
    return generators


PAIR_BASIS = ((0, 1), (0, 2), (0, 3), (2, 3), (3, 1), (1, 2))


def form_matrix(vector: sp.Matrix) -> sp.Matrix:
    result = sp.zeros(4)
    for coefficient, (left, right) in zip(vector, PAIR_BASIS):
        result[left, right] = coefficient
        result[right, left] = -coefficient
    return result


def form_vector(matrix: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([matrix[left, right] for left, right in PAIR_BASIS])


def induced_two_form_generator(generator: sp.Matrix) -> sp.Matrix:
    columns: list[sp.Matrix] = []
    for index in range(6):
        basis_vector = sp.eye(6)[:, index]
        two_form = form_matrix(basis_vector)
        variation = -(generator.T * two_form + two_form * generator)
        columns.append(form_vector(variation))
    return sp.Matrix.hstack(*columns)


def induced_two_form_group_action(group_element: sp.Matrix) -> sp.Matrix:
    """Finite pullback action of a Lorentz transformation on covariant 2-forms."""
    columns: list[sp.Matrix] = []
    for index in range(6):
        two_form = form_matrix(sp.eye(6)[:, index])
        transformed = group_element.T * two_form * group_element
        columns.append(form_vector(transformed))
    return sp.Matrix.hstack(*columns)


def induced_two_form_projector(projector: sp.Matrix) -> sp.Matrix:
    """Derivation induced by a rank-one tangent projector on covariant 2-forms."""
    columns: list[sp.Matrix] = []
    for index in range(6):
        basis_vector = sp.eye(6)[:, index]
        two_form = form_matrix(basis_vector)
        projected = projector.T * two_form + two_form * projector
        columns.append(form_vector(sp.simplify(projected)))
    return sp.Matrix.hstack(*columns)


def permutation_sign(values: tuple[int, int, int, int]) -> int:
    if len(set(values)) < 4:
        return 0
    inversions = sum(
        values[left] > values[right]
        for left in range(4)
        for right in range(left + 1, 4)
    )
    return -1 if inversions % 2 else 1


def hodge_star_two_forms(metric: sp.Matrix) -> sp.Matrix:
    inverse_metric = metric.inv()
    columns: list[sp.Matrix] = []
    for basis_index in range(6):
        covariant = form_matrix(sp.eye(6)[:, basis_index])
        contravariant = inverse_metric * covariant * inverse_metric
        dual = sp.zeros(4)
        for a in range(4):
            for b in range(4):
                dual[a, b] = sp.Rational(1, 2) * sum(
                    permutation_sign((a, b, c, d)) * contravariant[c, d]
                    for c in range(4)
                    for d in range(4)
                )
        columns.append(form_vector(dual))
    return sp.Matrix.hstack(*columns)


def invariant_idempotent_ranks(commutant: sp.Matrix) -> list[int]:
    free = sorted(
        set().union(*(entry.free_symbols for entry in commutant)),
        key=lambda item: item.name,
    )
    if len(free) != 2:
        raise AssertionError(f"expected two commutant parameters, found {free}")
    ranks: set[int] = set()
    for values in ((0, 0), (0, 1), (1, 0), (1, 1)):
        candidate = commutant.subs(dict(zip(free, values)))
        if is_zero(candidate**2 - candidate):
            ranks.add(int(candidate.rank()))
    return sorted(ranks)


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def object_rows() -> list[dict[str, str]]:
    return [
        {
            "id": "O01",
            "candidate": "conformal_metric_and_null_cone",
            "object_type": "conformal_structure",
            "frame_status": "INTRINSIC",
            "CSN_status": "INVARIANT",
            "definition_domain": "CONDITIONAL_4D_LORENTZIAN",
            "reciprocal_content": "COMPATIBLE_NOT_IDENTIFIED",
            "Hopf_content": "NONE",
            "foundation_selection": "DERIVED_CONDITIONAL",
            "ruling": "INTRINSIC_SCAFFOLD_NOT_RECIPROCAL_HOPF_OBJECT",
        },
        {
            "id": "O02",
            "candidate": "projectivized_future_null_cone",
            "object_type": "celestial_S2_bundle",
            "frame_status": "INTRINSIC_ASSOCIATED_BUNDLE",
            "CSN_status": "INVARIANT",
            "definition_domain": "LORENTZIAN_PLUS_TIME_COMPONENT",
            "reciprocal_content": "NO_SELECTED_CHARACTER_OR_PLANE",
            "Hopf_content": "S2_FIBER_ONLY",
            "foundation_selection": "DERIVED_CONDITIONAL_FIBER",
            "ruling": "BUNDLE_EXISTS_SECTION_AND_HOPF_CLASS_OPEN",
        },
        {
            "id": "O03",
            "candidate": "time_orientation",
            "object_type": "cone_component_reduction",
            "frame_status": "INTRINSIC_IF_SUPPLIED",
            "CSN_status": "INVARIANT",
            "definition_domain": "TIME_ORIENTABLE_COMPLETION",
            "reciprocal_content": "NONE",
            "Hopf_content": "NONE",
            "foundation_selection": "CHOSE_NOT_UNIVERSALLY_SUPPLIED",
            "ruling": "CONE_COMPONENT_NOT_CLOCK_VECTOR_OR_SECTION",
        },
        {
            "id": "O04",
            "candidate": "orientation_and_volume_form",
            "object_type": "top_form",
            "frame_status": "INTRINSIC_IF_ORIENTED",
            "CSN_status": "WEIGHTED_NOT_NEUTRAL",
            "definition_domain": "ORIENTED_METRIC_REPRESENTATIVE",
            "reciprocal_content": "NONE",
            "Hopf_content": "ORIENTATION_SIGN_ONLY",
            "foundation_selection": "ORIENTATION_NOT_UNIVERSALLY_SUPPLIED",
            "ruling": "NOT_A_PROPER_REDUCTION_SECTION_OR_HOPF_CLASS",
        },
        {
            "id": "O05",
            "candidate": "Lorentzian_Hodge_star_on_two_forms",
            "object_type": "real_complex_structure_on_Lambda2",
            "frame_status": "INTRINSIC_IF_ORIENTED",
            "CSN_status": "INVARIANT_IN_4D_ON_LAMBDA2",
            "definition_domain": "ORIENTED_4D_LORENTZIAN",
            "reciprocal_content": "NONE",
            "Hopf_content": "NONE",
            "foundation_selection": "DERIVED_CONDITIONAL_UNIVERSAL_GEOMETRY",
            "ruling": "STAR_SQUARED_MINUS_I_NO_REAL_PLUS_MINUS_REDUCTION",
        },
        {
            "id": "O06",
            "candidate": "complex_Hodge_chiral_pair_and_exp_phi_i_star",
            "object_type": "complex_rank3_bundle_split",
            "frame_status": "INTRINSIC_IF_ORIENTED_AND_COMPLEXIFIED",
            "CSN_status": "INVARIANT",
            "definition_domain": "ORIENTED_4D_LORENTZIAN_COMPLEXIFICATION",
            "reciprocal_content": "EXACT_E_PLUS_MINUS_PHI_ON_COMPLEX_CONJUGATE_SECTORS",
            "Hopf_content": "NONE",
            "foundation_selection": "NATURAL_CONSTRUCTION_AVAILABLE_ACTION_NOT_REGISTERED",
            "ruling": "EXACT_INTRINSIC_COMPLEX_RECIPROCAL_CANDIDATE_FAILS_REALITY_AND_SUPPLIES_NO_HOPF_SECTION",
        },
        {
            "id": "O07",
            "candidate": "Levi_Civita_connection",
            "object_type": "metric_connection",
            "frame_status": "INTRINSIC_PER_REPRESENTATIVE",
            "CSN_status": "CHANGES_UNDER_LOCAL_COMMON_SCALE",
            "definition_domain": "NONDEGENERATE_METRIC_REPRESENTATIVE",
            "reciprocal_content": "TRANSPORTS_SUPPLIED_OBJECTS_ONLY",
            "Hopf_content": "NONE_BY_ITSELF",
            "foundation_selection": "DERIVED_PER_REPRESENTATIVE",
            "ruling": "CONNECTION_DOES_NOT_GENERATE_REDUCTION_OR_SECTION",
        },
        {
            "id": "O08",
            "candidate": "complete_curvature_operator_algebra",
            "object_type": "intrinsic_local_tensor_algebra",
            "frame_status": "INTRINSIC_UP_TO_CONJUGACY",
            "CSN_status": "REPRESENTATION_DEPENDENT_EXCEPT_CONFORMAL_PARTS",
            "definition_domain": "REGISTERED_TWO_JET_ENSEMBLE",
            "reciprocal_content": "NO_UNIVERSAL_PROPER_SUBSPACE",
            "Hopf_content": "NONE",
            "foundation_selection": "OBSERVED_BOUNDED",
            "ruling": "METRIC_ACTIVE_FULL_IRREDUCIBLE_FLAT_ROWS_AMBIGUOUS",
        },
        {
            "id": "O09",
            "candidate": "Weyl_or_curvature_algebraic_null_directions",
            "object_type": "unordered_multisection_or_degenerate_data",
            "frame_status": "INTRINSIC_AS_UNORDERED_DATA_ON_REGULAR_STRATA",
            "CSN_status": "WEYL_TYPE_COMPATIBLE",
            "definition_domain": "REGULAR_NONFLAT_ALGEBRAIC_STRATA_ONLY",
            "reciprocal_content": "NO_BRANCH_PRIORITY",
            "Hopf_content": "NO_SELECTED_MAP_OR_SECONDARY_CLASS",
            "foundation_selection": "NOT_EVALUATED_AS_A_GLOBAL_SELECTED_SECTION",
            "ruling": "CANNOT_SUPPLY_UNIVERSAL_SECTION_ACROSS_FLAT_AND_DEGENERATE_STRATA",
        },
        {
            "id": "O10",
            "candidate": "Ricci_Hessian_or_spectral_split",
            "object_type": "spectral_line_or_plane_reduction",
            "frame_status": "INTRINSIC_ON_SIMPLE_SEMISIMPLE_STRATA",
            "CSN_status": "CANDIDATE_DEPENDENT",
            "definition_domain": "NONDEGENERATE_STRATA_ONLY",
            "reciprocal_content": "NO_REGISTERED_PRIORITY",
            "Hopf_content": "NONE",
            "foundation_selection": "OBSERVED_SMALLER_FAMILIES_ONLY",
            "ruling": "STRATUM_CONDITIONAL_AND_DESTROYED_OR_AMBIGUOUS_IN_COMPLETE_ORCHESTRA",
        },
        {
            "id": "O11",
            "candidate": "nonnull_dphi_line",
            "object_type": "rank1_tangent_or_cotangent_line",
            "frame_status": "INTRINSIC_ON_DOMAIN",
            "CSN_status": "LINE_PROJECTOR_INVARIANT",
            "definition_domain": "DPHI_NONZERO_AND_NONNULL",
            "reciprocal_content": "PHI_RELATED_BUT_NO_DUAL_PARTNER",
            "Hopf_content": "NO_TRANSVERSE_PHASE_OR_FIXED_TARGET",
            "foundation_selection": "LOCAL_STRATUM_ONLY",
            "ruling": "INTRINSIC_LINE_NOT_RECIPROCAL_PLANE_OR_HOPF_SECTION",
        },
        {
            "id": "O12",
            "candidate": "null_dphi_ray",
            "object_type": "celestial_section_on_null_gradient_region",
            "frame_status": "INTRINSIC_ON_DOMAIN",
            "CSN_status": "NULL_RAY_INVARIANT",
            "definition_domain": "DPHI_NONZERO_NULL_WITH_TIME_COMPONENT",
            "reciprocal_content": "PHI_RELATED",
            "Hopf_content": "NO_GLOBAL_HOPF_CLASS_DERIVED",
            "foundation_selection": "CAUSAL_TYPE_NOT_FORCED",
            "ruling": "CONDITIONAL_LOCAL_SECTION_NOT_UNIVERSAL_OR_HOPF_BEARING",
        },
        {
            "id": "O13",
            "candidate": "critical_or_zero_dphi_strata",
            "object_type": "scalar_only",
            "frame_status": "INTRINSIC_BUT_DIRECTIONLESS",
            "CSN_status": "INVARIANT",
            "definition_domain": "ADMITTED_INCLUDING_SEAL",
            "reciprocal_content": "SCALAR_VALUE_ONLY",
            "Hopf_content": "NONE",
            "foundation_selection": "REGISTERED_ADMITTED",
            "ruling": "DIRECTION_AND_SECTION_UNDEFINED_OR_AMBIGUOUS",
        },
        {
            "id": "O14",
            "candidate": "finite_cell_seal_normal",
            "object_type": "boundary_rank1_line",
            "frame_status": "INTRINSIC_IF_BOUNDARY_EMBEDDING_SUPPLIED",
            "CSN_status": "LINE_SURVIVES",
            "definition_domain": "SEAL_ONLY",
            "reciprocal_content": "NO_CLOCK_PARTNER",
            "Hopf_content": "NONE",
            "foundation_selection": "BOUNDARY_CONDITIONAL",
            "ruling": "NO_UNIVERSAL_RANK2_REDUCTION_AT_SEAL",
        },
        {
            "id": "O15",
            "candidate": "reflection_lift_screen_involution",
            "object_type": "screen_reduction_at_seal",
            "frame_status": "INTRINSIC_AFTER_LIFT_AND_ORIENTATION",
            "CSN_status": "INVARIANT",
            "definition_domain": "REFLECTION_LIFT_BRANCH_AT_SEAL",
            "reciprocal_content": "COMPLEMENT_UP_TO_SIGN",
            "Hopf_content": "NONE_WITHOUT_BULK_AND_GLOBAL_DATA",
            "foundation_selection": "DERIVED_CONDITIONAL_AT_SEAL",
            "ruling": "LIFT_UNSELECTED_AND_NO_BULK_CONTINUATION",
        },
        {
            "id": "O16",
            "candidate": "named_coframe_reciprocal_plane",
            "object_type": "rank2_plane",
            "frame_status": "FRAME_DEPENDENT",
            "CSN_status": "NOT_THE_DECISIVE_FAILURE",
            "definition_domain": "CHOSEN_COFRAME",
            "reciprocal_content": "EXACT_CHART_CHARACTER",
            "Hopf_content": "CONDITIONAL_COMPONENT_CROSSWALK",
            "foundation_selection": "NOT_DERIVED",
            "ruling": "FAILS_LOCAL_LORENTZ_DESCENT",
        },
        {
            "id": "O17",
            "candidate": "abstract_reciprocal_representation_Vrec",
            "object_type": "abstract_rank2_representation",
            "frame_status": "ABSTRACT_NOT_A_TANGENT_OBJECT",
            "CSN_status": "SCALE_FREE_CHARACTER",
            "definition_domain": "C0_C1_REPRESENTATION",
            "reciprocal_content": "DERIVED",
            "Hopf_content": "NONE_WITHOUT_SOLDERING",
            "foundation_selection": "DERIVED_ABSTRACTLY",
            "ruling": "PHYSICAL_SOLDERING_TYPE_GAP",
        },
        {
            "id": "O18",
            "candidate": "metric_derived_projector_motif",
            "object_type": "local_projector_family",
            "frame_status": "INTRINSIC_WHEN_TENSORIALLY_DEFINED",
            "CSN_status": "CANDIDATE_DEPENDENT",
            "definition_domain": "FIXED_RANK_STABLE_STRATA",
            "reciprocal_content": "NO_UNIVERSAL_OWNER",
            "Hopf_content": "MOTIF_COMPATIBILITY_ONLY",
            "foundation_selection": "OBSERVED_BOUNDED",
            "ruling": "NO_COMPLETE_ORCHESTRA_UNIVERSAL_PROPER_PROJECTOR",
        },
        {
            "id": "O19",
            "candidate": "projector_Kato_connection",
            "object_type": "connection_on_supplied_projector_bundles",
            "frame_status": "INTRINSIC_GIVEN_PROJECTORS",
            "CSN_status": "METRIC_COMPATIBLE",
            "definition_domain": "SMOOTH_FIXED_RANK_PROJECTOR_PATH",
            "reciprocal_content": "TRANSPORT_ONLY",
            "Hopf_content": "NO_TOPOLOGY_WITHOUT_CLOSED_GLUE",
            "foundation_selection": "DERIVED_GEOMETRIC_IDENTITY",
            "ruling": "TRANSPORTS_BUT_DOES_NOT_CREATE_OR_SELECT_PROJECTOR",
        },
        {
            "id": "O20",
            "candidate": "Levi_Civita_holonomy_conjugacy_class",
            "object_type": "global_connection_invariant",
            "frame_status": "INTRINSIC_PER_COMPLETED_METRIC_UP_TO_CONJUGACY",
            "CSN_status": "REPRESENTATIVE_DEPENDENT",
            "definition_domain": "SUPPLIED_COMPLETE_METRIC_AND_LOOPS",
            "reciprocal_content": "POSSIBLE_REDUCTION_ONLY_IF_PRESERVED",
            "Hopf_content": "NO_AUTOMATIC_HOPF_CLASS",
            "foundation_selection": "COMPLETE_METRIC_NOT_SELECTED",
            "ruling": "INTRINSIC_ON_SUPPLIED_COMPLETION_NOT_FOUNDATION_SELECTOR",
        },
        {
            "id": "O21",
            "candidate": "parallel_holonomy_preserved_subbundle",
            "object_type": "global_bundle_reduction",
            "frame_status": "INTRINSIC_IF_HOLONOMY_REDUCES",
            "CSN_status": "REPRESENTATIVE_DEPENDENT",
            "definition_domain": "REDUCED_HOLONOMY_COMPLETIONS",
            "reciprocal_content": "ONLY_IF_SEPARATELY_IDENTIFIED",
            "Hopf_content": "NONE_BY_REDUCTION_ALONE",
            "foundation_selection": "OPEN_CONDITIONAL_BRANCH",
            "ruling": "NOT_UNIVERSAL_IN_REGISTERED_ACTIVE_OR_FLAT_DICHOTOMY",
        },
        {
            "id": "O22",
            "candidate": "tangent_bundle_characteristic_classes",
            "object_type": "primary_topological_invariants",
            "frame_status": "INTRINSIC_TO_MANIFOLD_BUNDLE",
            "CSN_status": "INVARIANT",
            "definition_domain": "SUPPLIED_GLOBAL_MANIFOLD",
            "reciprocal_content": "NONE",
            "Hopf_content": "NOT_A_SELECTED_S3_TO_S2_SECONDARY_INVARIANT",
            "foundation_selection": "TOPOLOGY_NOT_SELECTED",
            "ruling": "GENUINE_GLOBAL_INVARIANTS_BUT_NOT_RECIPROCAL_HOPF_CARRIER",
        },
        {
            "id": "O23",
            "candidate": "celestial_S2_bundle_characteristic_data",
            "object_type": "associated_bundle_primary_invariants",
            "frame_status": "INTRINSIC_IF_GLOBAL_BUNDLE_SUPPLIED",
            "CSN_status": "INVARIANT",
            "definition_domain": "GLOBAL_LORENTZIAN_COMPLETION",
            "reciprocal_content": "NONE_WITHOUT_REDUCTION",
            "Hopf_content": "OBSTRUCTION_OR_BUNDLE_DATA_NOT_HOPF_MAP_CHARGE",
            "foundation_selection": "GLOBAL_COMPLETION_NOT_SELECTED",
            "ruling": "BUNDLE_INVARIANT_SURVIVES_BUT_DOES_NOT_SELECT_SECTION",
        },
        {
            "id": "O24",
            "candidate": "reciprocal_toric_principal_circle_class",
            "object_type": "principal_U1_bundle_c1_and_Hopf_readout",
            "frame_status": "INTRINSIC_AFTER_GLOBAL_TORIC_DATA",
            "CSN_status": "NORMALIZED_CONNECTION_INVARIANT",
            "definition_domain": "SUPPLIED_PERIODS_ACTION_CAPS_ORIENTATION_QUOTIENT",
            "reciprocal_content": "EXACT",
            "Hopf_content": "ABS_C1_EQUALS_ONE_CONDITIONAL",
            "foundation_selection": "GLOBAL_INPUTS_NOT_SELECTED",
            "ruling": "EXACT_CONDITIONAL_HOPF_BUNDLE_NOT_NATIVE_SELECTION",
        },
        {
            "id": "O25",
            "candidate": "bare_component_null_section_Hopf_charge",
            "object_type": "component_map",
            "frame_status": "FRAME_DEPENDENT",
            "CSN_status": "INSUFFICIENT",
            "definition_domain": "CHOSEN_TRIVIALIZATION",
            "reciprocal_content": "CONDITIONAL_CROSSWALK",
            "Hopf_content": "CAN_BE_CREATED_BY_WINDING_FRAME",
            "foundation_selection": "REFUTED_IN_REGISTERED_SCOPE",
            "ruling": "NOT_A_PHYSICAL_BUNDLE_INVARIANT",
        },
        {
            "id": "O26",
            "candidate": "nonlocal_spectral_or_geodesic_selector",
            "object_type": "global_nonlocal_construction",
            "frame_status": "POTENTIALLY_INTRINSIC_AFTER_FULL_DEFINITION",
            "CSN_status": "UNSPECIFIED",
            "definition_domain": "REQUIRES_OPERATOR_DOMAIN_BOUNDARY_AND_DEGENERACY_RULE",
            "reciprocal_content": "NO_REGISTERED_MAP",
            "Hopf_content": "NO_REGISTERED_OUTPUT",
            "foundation_selection": "ABSENT_FROM_CURRENT_FOUNDATION",
            "ruling": "TYPE_CLASS_OPEN_NOT_AN_EXISTING_SELECTOR",
        },
        {
            "id": "O27",
            "candidate": "global_boundary_or_stationarity_functional",
            "object_type": "realization_selector",
            "frame_status": "POTENTIALLY_INTRINSIC_IF_DERIVED",
            "CSN_status": "UNSPECIFIED",
            "definition_domain": "REQUIRES_ACTION_BOUNDARY_VARIATION_DOMAIN",
            "reciprocal_content": "NO_CURRENT_OPERATION",
            "Hopf_content": "NO_CURRENT_OUTPUT",
            "foundation_selection": "OPEN",
            "ruling": "NOT_PRESENT_IN_REGISTERED_FOUNDATION",
        },
        {
            "id": "O28",
            "candidate": "registered_bootstrap",
            "object_type": "on_shell_admissibility_language",
            "frame_status": "NOT_AN_OBJECT_CONSTRUCTION",
            "CSN_status": "QUALITATIVELY_COMPATIBLE",
            "definition_domain": "COMPLETED_SOLUTIONS_AS_YET_UNTYPED",
            "reciprocal_content": "NO_OPERATIONAL_REALIZATION_MAP",
            "Hopf_content": "NO_SECTION_OR_CLASS_OUTPUT",
            "foundation_selection": "INCOMPLETE",
            "ruling": "DOES_NOT_CURRENTLY_SELECT_INTRINSIC_OBJECT",
        },
        {
            "id": "O29",
            "candidate": "combined_registered_complete_metric_structure",
            "object_type": "whole_foundation",
            "frame_status": "ALL_INTRINSIC_SCAFFOLDS_RETAINED",
            "CSN_status": "PRE_AND_POST_SCALE_LAYERS_SEPARATED",
            "definition_domain": "BOUNDED_REGISTERED_SCOPE",
            "reciprocal_content": "ABSTRACT_AND_CHART_LEVEL_EXACT",
            "Hopf_content": "FIBER_AND_TORIC_CLASS_ONLY_CONDITIONAL",
            "foundation_selection": "NO_NATIVE_JOIN_FOUND",
            "ruling": "FIELD_ASSISTED_REAL_RECIPROCAL_REDUCTION_EXISTS_ONLY_ON_NONNULL_DPHI_STRATA__NO_GLOBAL_HOPF_SECTION_OR_SELECTED_BUNDLE_INVARIANT",
        },
        {
            "id": "O30",
            "candidate": "nonnull_dphi_induced_real_two_form_pair",
            "object_type": "real_rank3_plus_rank3_Lambda2_reduction",
            "frame_status": "INTRINSIC_TO_G_AND_PHI_ON_DOMAIN",
            "CSN_status": "INVARIANT_AS_SUBBUNDLE_SPLIT",
            "definition_domain": "DPHI_NONZERO_AND_NONNULL",
            "reciprocal_content": "EXACT_E_PLUS_MINUS_PHI_COMPATIBLE_REAL_ACTION",
            "Hopf_content": "HODGE_DUAL_S2_LIKE_FIBERS_POSSIBLE_BUT_NO_SELECTED_SECTION_OR_CLASS",
            "foundation_selection": "LOCAL_STRATUM_REDUCTION_DERIVED_RECIPROCAL_PHYSICAL_OWNERSHIP_OPEN",
            "ruling": "EXACT_FIELD_ASSISTED_REAL_RECIPROCAL_3PLUS3_REDUCTION_ON_NONNULL_STRATA__NOT_GLOBAL_OR_HOPF_BEARING",
        },
    ]


def main() -> None:
    eta = sp.diag(-1, 1, 1, 1)
    generators = lorentz_generators()

    tangent_commutant, _ = matrix_commutant(generators)
    tangent_free = set().union(*(entry.free_symbols for entry in tangent_commutant))
    tangent_commutant_dimension = len(tangent_free)

    vector_variables = list(sp.symbols("v0:4"))
    vector = sp.Matrix(vector_variables)
    invariant_vector_dimension = linear_solution_dimension(
        [entry for generator in generators for entry in generator * vector],
        vector_variables,
    )

    form_variables = list(sp.symbols("f0:6"))
    form = form_matrix(sp.Matrix(form_variables))
    invariant_form_equations = [
        entry
        for generator in generators
        for entry in (generator.T * form + form * generator)
    ]
    invariant_two_form_dimension = linear_solution_dimension(
        invariant_form_equations, form_variables
    )

    induced = [induced_two_form_generator(generator) for generator in generators]
    two_form_commutant, _ = matrix_commutant(induced)
    two_form_commutant_symbols = set().union(
        *(entry.free_symbols for entry in two_form_commutant)
    )
    two_form_commutant_dimension = len(two_form_commutant_symbols)
    hodge = hodge_star_two_forms(eta)
    commutant_columns = [
        sp.diff(two_form_commutant, symbol).reshape(36, 1)
        for symbol in sorted(two_form_commutant_symbols, key=lambda item: item.name)
    ]
    standard_span = sp.Matrix.hstack(sp.eye(6).reshape(36, 1), hodge.reshape(36, 1))
    commutant_span = sp.Matrix.hstack(*commutant_columns)
    orientation_reversal = sp.diag(1, -1, 1, 1)
    orientation_reversal_on_forms = induced_two_form_group_action(orientation_reversal)
    full_lorentz_commutant, _ = matrix_commutant(
        [*induced, orientation_reversal_on_forms]
    )
    full_lorentz_commutant_symbols = set().union(
        *(entry.free_symbols for entry in full_lorentz_commutant)
    )
    full_lorentz_commutant_dimension = len(full_lorentz_commutant_symbols)

    # The oriented Lorentzian Hodge structure has an exact but complex
    # reciprocal-shaped near realization.  K=i* is an involution on the
    # complexified two-form bundle, so exp(phi K) weights its two rank-three
    # eigenspaces reciprocally.  Unequal real weights do not preserve the
    # conjugacy/reality condition of a real two-form.
    complex_involution = sp.I * hodge
    complex_plus = sp.simplify((sp.eye(6) + complex_involution) / 2)
    complex_minus = sp.simplify((sp.eye(6) - complex_involution) / 2)
    reciprocal_scale = sp.symbols("t", positive=True)
    complex_reciprocal = sp.simplify(
        reciprocal_scale * complex_plus + reciprocal_scale**-1 * complex_minus
    )
    real_basis_form = sp.eye(6)[:, 0]
    real_descent_witness = sp.simplify(
        complex_reciprocal.subs(reciprocal_scale, 2) * real_basis_form
    )
    real_hodge_rotation = sp.simplify(
        sp.Rational(3, 5) * sp.eye(6) + sp.Rational(4, 5) * hodge
    )
    real_a, real_b = sp.symbols("a b", real=True)
    real_equivariant_endomorphism = real_a * sp.eye(6) + real_b * hodge
    real_equivariant_charpoly = real_equivariant_endomorphism.charpoly()
    eigenvalue = real_equivariant_charpoly.gen
    real_equivariant_characteristic = sp.factor(real_equivariant_charpoly.as_expr())

    # Spatial rotations have no common fixed point on the unit direction sphere.
    spatial_variables = list(sp.symbols("n1:4"))
    spatial = sp.Matrix(spatial_variables)
    rotations = generators[3:]
    fixed_spatial_dimension = linear_solution_dimension(
        [entry for rotation in rotations for entry in rotation[1:4, 1:4] * spatial],
        spatial_variables,
    )

    # Exact same-metric coframe witness.
    boost = sp.Matrix(
        [
            [sp.Rational(5, 4), sp.Rational(3, 4), 0, 0],
            [sp.Rational(3, 4), sp.Rational(5, 4), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    named_leg = sp.diag(1, 0, 0, 0)
    moved_leg = sp.simplify(boost * named_leg * boost.inv())

    # A nonnull scalar gradient supplies a conformally invariant line projector
    # only on its nonzero nonnull domain.
    covector = sp.Matrix([2, 1, 0, 0])
    raised = eta.inv() * covector
    norm = (covector.T * raised)[0]
    gradient_projector = sp.simplify(raised * covector.T / norm)
    omega = sp.symbols("Omega", positive=True)
    scaled_raised = (omega**2 * eta).inv() * covector
    scaled_norm = (covector.T * scaled_raised)[0]
    scaled_gradient_projector = sp.simplify(scaled_raised * covector.T / scaled_norm)
    null_covector = sp.Matrix([1, 1, 0, 0])
    null_raised = eta.inv() * null_covector
    null_norm = (null_covector.T * null_raised)[0]
    null_gradient_endomorphism = null_raised * null_covector.T
    gradient_two_form_plus = induced_two_form_projector(gradient_projector)
    gradient_two_form_minus = sp.eye(6) - gradient_two_form_plus
    gradient_two_form_involution = 2 * gradient_two_form_plus - sp.eye(6)
    gradient_two_form_reciprocal = sp.simplify(
        reciprocal_scale * gradient_two_form_plus
        + reciprocal_scale**-1 * gradient_two_form_minus
    )
    scaled_gradient_two_form_plus = induced_two_form_projector(
        scaled_gradient_projector
    )
    scaled_gradient_two_form_minus = sp.eye(6) - scaled_gradient_two_form_plus
    scaled_gradient_two_form_reciprocal = sp.simplify(
        reciprocal_scale * scaled_gradient_two_form_plus
        + reciprocal_scale**-1 * scaled_gradient_two_form_minus
    )
    null_gradient_two_form_endomorphism = induced_two_form_projector(
        null_gradient_endomorphism
    )
    spacelike_covector = sp.Matrix([1, 2, 0, 0])
    spacelike_raised = eta.inv() * spacelike_covector
    spacelike_norm = (spacelike_covector.T * spacelike_raised)[0]
    spacelike_projector = sp.simplify(
        spacelike_raised * spacelike_covector.T / spacelike_norm
    )
    spacelike_two_form_plus = induced_two_form_projector(spacelike_projector)

    # alpha=h dphi is hypersurface orthogonal for arbitrary first jets.
    p = list(sp.symbols("p0:4"))
    h = sp.symbols("h")
    dh = list(sp.symbols("h0:4"))
    dalpha = sp.Matrix(
        4,
        4,
        lambda i, j: sp.simplify(dh[i] * p[j] - dh[j] * p[i]),
    )

    def alpha_wedge_dalpha(i: int, j: int, k: int) -> sp.Expr:
        alpha = [h * component for component in p]
        return sp.simplify(
            alpha[i] * dalpha[j, k]
            + alpha[j] * dalpha[k, i]
            + alpha[k] * dalpha[i, j]
        )

    frobenius_components = [
        alpha_wedge_dalpha(i, j, k)
        for i, j, k in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))
    ]

    # Full connected seal stabilizer on the Lorentzian tangential 3-plane.
    seal_generators = [generators[1], generators[2], generators[5]]
    seal_commutant, _ = matrix_commutant(seal_generators)
    seal_idempotent_ranks = invariant_idempotent_ranks(seal_commutant)

    local_atlas = json.loads(
        (ROOT / "udt_local_selector_holonomy_closure_2026-07-22/ATLAS_RESULT.json").read_text(
            encoding="utf-8"
        )
    )
    joint_atlas = json.loads(
        (ROOT / "udt_joint_invariant_subspace_atlas_2026-07-21/ATLAS_RESULT.json").read_text(
            encoding="utf-8"
        )
    )
    global_atlas = json.loads(
        (ROOT / "udt_global_metric_assembly_atlas_2026-07-22/ATLAS_RESULT.json").read_text(
            encoding="utf-8"
        )
    )
    with (
        ROOT
        / "udt_structural_ensemble_metric_atlas_2026-07-21/CONFIGURATION_OBSERVATIONS.tsv"
    ).open(encoding="utf-8", newline="") as handle:
        registered_dphi_classes = Counter(
            row["dphi_class"] for row in csv.DictReader(handle, delimiter="\t")
        )

    checks = {
        "lorentz_generators_metric_skew": all(
            is_zero(generator.T * eta + eta * generator) for generator in generators
        ),
        "tangent_commutant_is_scalar": tangent_commutant_dimension == 1
        and tangent_commutant == sp.eye(4) * next(iter(tangent_free)),
        "no_invariant_tangent_vector": invariant_vector_dimension == 0,
        "no_invariant_real_two_form": invariant_two_form_dimension == 0,
        "connected_orientation_preserving_two_form_commutant_is_I_and_hodge": two_form_commutant_dimension == 2
        and commutant_span.rank() == 2
        and standard_span.rank() == 2
        and sp.Matrix.hstack(commutant_span, standard_span).rank() == 2,
        "full_orientation_reversing_Lorentz_two_form_commutant_is_scalar": (
            full_lorentz_commutant_dimension == 1
            and is_zero(
                full_lorentz_commutant
                - sp.eye(6)
                * next(iter(full_lorentz_commutant_symbols))
            )
        ),
        "Lorentzian_hodge_square_minus_identity": is_zero(hodge**2 + sp.eye(6)),
        "hodge_commutes_with_Lorentz_action": all(
            is_zero(hodge * generator - generator * hodge) for generator in induced
        ),
        "complex_i_hodge_is_involution": is_zero(complex_involution**2 - sp.eye(6)),
        "complex_Hodge_projectors_are_rank3": is_zero(complex_plus**2 - complex_plus)
        and is_zero(complex_minus**2 - complex_minus)
        and is_zero(complex_plus * complex_minus)
        and is_zero(complex_plus + complex_minus - sp.eye(6))
        and complex_plus.rank() == 3
        and complex_minus.rank() == 3,
        "complex_Hodge_weights_are_exactly_reciprocal": is_zero(
            complex_reciprocal * complex_plus - reciprocal_scale * complex_plus
        )
        and is_zero(
            complex_reciprocal * complex_minus
            - reciprocal_scale**-1 * complex_minus
        ),
        "unequal_complex_Hodge_weights_fail_real_descent": any(
            sp.simplify(sp.im(entry)) != 0 for entry in real_descent_witness
        ),
        "real_Hodge_flow_is_rotation_not_dilation": is_zero(
            real_hodge_rotation.T * real_hodge_rotation - sp.eye(6)
        ),
        "real_Lorentz_equivariant_two_form_maps_have_no_nontrivial_real_reciprocal_split": (
            sp.simplify(
                real_equivariant_characteristic
                - ((eigenvalue - real_a) ** 2 + real_b**2) ** 3
            )
            == 0
        ),
        "no_spatial_rotation_fixed_direction": fixed_spatial_dimension == 0,
        "same_metric_boost": is_zero(boost.T * eta * boost - eta),
        "named_leg_changes_under_same_metric_boost": not is_zero(moved_leg - named_leg),
        "nonnull_gradient_projector_valid": is_zero(gradient_projector**2 - gradient_projector)
        and gradient_projector.rank() == 1,
        "gradient_line_projector_CSN_invariant": is_zero(
            scaled_gradient_projector - gradient_projector
        ),
        "null_gradient_projector_denominator_zero": null_norm == 0,
        "null_gradient_replaces_projector_by_nonzero_nilpotent": (
            null_gradient_endomorphism.rank() == 1
            and not is_zero(null_gradient_endomorphism)
            and is_zero(null_gradient_endomorphism**2)
        ),
        "null_gradient_induced_two_form_map_is_rank2_nilpotent": (
            null_gradient_two_form_endomorphism.rank() == 2
            and not is_zero(null_gradient_two_form_endomorphism)
            and is_zero(null_gradient_two_form_endomorphism**2)
        ),
        "nonnull_gradient_induces_real_rank3_plus_rank3_two_form_split": (
            is_zero(gradient_two_form_plus**2 - gradient_two_form_plus)
            and is_zero(gradient_two_form_minus**2 - gradient_two_form_minus)
            and is_zero(gradient_two_form_plus * gradient_two_form_minus)
            and gradient_two_form_plus.rank() == 3
            and gradient_two_form_minus.rank() == 3
        ),
        "gradient_two_form_split_is_CSN_invariant": is_zero(
            scaled_gradient_two_form_plus - gradient_two_form_plus
        ),
        "full_gradient_reciprocal_operator_is_CSN_invariant": is_zero(
            scaled_gradient_two_form_reciprocal
            - gradient_two_form_reciprocal
        ),
        "gradient_two_form_split_is_Hodge_exchanged": is_zero(
            hodge * gradient_two_form_plus * hodge.inv()
            - gradient_two_form_minus
        ),
        "gradient_two_form_involution_is_real": is_zero(
            gradient_two_form_involution**2 - sp.eye(6)
        )
        and all(entry.is_real is not False for entry in gradient_two_form_involution),
        "gradient_two_form_weights_are_exactly_real_reciprocal": is_zero(
            gradient_two_form_reciprocal * gradient_two_form_plus
            - reciprocal_scale * gradient_two_form_plus
        )
        and is_zero(
            gradient_two_form_reciprocal * gradient_two_form_minus
            - reciprocal_scale**-1 * gradient_two_form_minus
        ),
        "Hodge_exchange_conjugates_reciprocal_operator_to_inverse": is_zero(
            hodge * gradient_two_form_reciprocal * hodge.inv()
            - (
                reciprocal_scale**-1 * gradient_two_form_plus
                + reciprocal_scale * gradient_two_form_minus
            )
        ),
        "spacelike_gradient_has_same_rank3_plus_rank3_Hodge_pair": spacelike_norm != 0
        and spacelike_two_form_plus.rank() == 3
        and is_zero(spacelike_two_form_plus**2 - spacelike_two_form_plus)
        and is_zero(
            hodge * spacelike_two_form_plus * hodge.inv()
            - (sp.eye(6) - spacelike_two_form_plus)
        ),
        "scalar_gradient_Frobenius_zero": all(
            is_zero(component) for component in frobenius_components
        ),
        "seal_stabilizer_no_rank2_projector": seal_idempotent_ranks == [0, 1, 3, 4],
        "registered_local_atlas_counts": local_atlas["q02"]["configurations"] == 6144
        and local_atlas["q02"]["final_class_counts"]
        == {
            "BASE_CURVATURE_FULL_IRREDUCIBLE__HIGHER_JETS_MONOTONE": 5376,
            "EXACT_CONSTANT_METRIC_FLAT__ALL_SUBSPACES_AMBIGUOUS": 768,
        },
        "registered_bivector_negative_replay": joint_atlas["configurations"] == 6144
        and joint_atlas["bivector_eigenplane_rows"] == 0
        and joint_atlas["unique_bivector_complementary_split_rows"] == 0,
        "registered_global_taxonomy_unselected": global_atlas["completion_class_count"] == 12
        and global_atlas["selected_global_quotient_classes"] == [],
        "registered_dphi_causal_census_replayed": registered_dphi_classes
        == Counter({"ZERO": 3072, "SPACELIKE": 2304, "TIMELIKE": 768}),
        "global_stage6_stage7_not_activated": global_atlas["stage_6_status"].startswith(
            "NOT_ACTIVATED"
        )
        and global_atlas["stage_7_status"].startswith("NOT_ACTIVATED"),
    }
    failed = [name for name, status in checks.items() if not status]
    if failed:
        raise AssertionError(f"failed checks: {failed}")

    rows = object_rows()
    if len(rows) != 30 or len({row["id"] for row in rows}) != 30:
        raise AssertionError("object census identity failure")
    write_tsv(
        HERE / "INTRINSIC_OBJECT_CENSUS.tsv",
        rows,
        [
            "id",
            "candidate",
            "object_type",
            "frame_status",
            "CSN_status",
            "definition_domain",
            "reciprocal_content",
            "Hopf_content",
            "foundation_selection",
            "ruling",
        ],
    )

    result = {
        "schema": "udt-complete-metric-intrinsic-object-audit-1.0",
        "status": "PASS",
        "sympy_version": sp.__version__,
        "exact_checks": checks,
        "counts": {
            "object_candidates": len(rows),
            "exact_checks": len(checks),
            "Lorentz_generators": len(generators),
            "tangent_commutant_dimension": tangent_commutant_dimension,
            "invariant_tangent_vector_dimension": invariant_vector_dimension,
            "invariant_real_two_form_dimension": invariant_two_form_dimension,
            "two_form_commutant_dimension": two_form_commutant_dimension,
            "full_orientation_reversing_Lorentz_two_form_commutant_dimension": (
                full_lorentz_commutant_dimension
            ),
            "complex_Hodge_projector_ranks": [
                int(complex_plus.rank()),
                int(complex_minus.rank()),
            ],
            "spatial_rotation_fixed_vector_dimension": fixed_spatial_dimension,
            "seal_invariant_projector_ranks": seal_idempotent_ranks,
            "registered_configurations": local_atlas["q02"]["configurations"],
            "registered_metric_active_full_irreducible": 5376,
            "registered_flat_ambiguous": 768,
            "registered_isolated_real_simple_curvature_eigenplanes": joint_atlas[
                "bivector_eigenplane_rows"
            ],
            "registered_global_completion_families": global_atlas["completion_class_count"],
            "registered_dphi_causal_classes": dict(
                sorted(registered_dphi_classes.items())
            ),
            "native_selected_reciprocal_Hopf_objects": 0,
            "intrinsic_complex_reciprocal_candidates": 1,
            "intrinsic_real_reciprocal_local_stratum_candidates": 1,
            "intrinsic_real_reciprocal_Hopf_objects": 0,
            "conditional_exact_toric_Hopf_objects": 1,
        },
        "positive_intrinsic_scaffolds": [
            "conformal_null_cone",
            "conditional_celestial_S2_bundle",
            "conditional_oriented_Lorentzian_Hodge_complex_structure_on_Lambda2",
            "conditional_complex_Hodge_chiral_reciprocal_candidate_with_failed_real_descent",
            "nonnull_dphi_induced_real_rank3_plus_rank3_two_form_reciprocal_candidate",
            "Levi_Civita_connection_and_holonomy_per_supplied_metric_representative",
            "primary_characteristic_data_per_supplied_global_bundle",
        ],
        "decisive_distinctions": [
            "bundle_is_not_section",
            "section_is_not_frame",
            "connection_is_not_topology",
            "completion_invariant_is_not_completion_selector",
            "S2_fiber_is_not_S3_to_S2_map",
            "primary_characteristic_class_is_not_Hopf_secondary_invariant",
            "abstract_reciprocal_representation_is_not_physical_soldering",
            "real_connected_orientation_preserving_Lorentz_equivariant_Lambda2_"
            "endomorphisms_are_aI_plus_bStar__full_orientation_reversing_"
            "commutant_is_scalar",
        ],
        "maximum_conclusion": (
            "EXACT_FRAME_INDEPENDENT_FIELD_ASSISTED_REAL_RECIPROCAL_3PLUS3_TWO_FORM_"
            "REDUCTION_IDENTIFIED_ON_NONNULL_DPHI_STRATA__HODGE_EXCHANGES_THE_SECTORS__"
            "GLOBAL_EXTENSION_PHYSICAL_OWNERSHIP_AND_HOPF_SECTION_REMAIN_OPEN"
        ),
        "scope": (
            "REGISTERED_OBJECT_TYPES_THROUGH_TWO_JETS_PLUS_TYPED_GLOBAL_HOLONOMY_"
            "CHARACTERISTIC_AND_NONLOCAL_CLASSES__NOT_ARBITRARY_FUTURE_HIGHER_JET_"
            "OR_NONLOCAL_UDT_LAWS"
        ),
    }
    (HERE / "RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
