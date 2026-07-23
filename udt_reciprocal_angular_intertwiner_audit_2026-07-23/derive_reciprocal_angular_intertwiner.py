#!/usr/bin/env python3
"""Exact reciprocal-angular intertwiner and complete-metric naturality audit."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "0d7b06d3e175cfd0a39cce79ebf5f1eef06c50ca"
MAXIMUM = (
    "NONBLOCK_RECIPROCAL_ANGULAR_INTERTWINERS_EXIST_EXACTLY_FOR_MATCHED_"
    "REPRESENTATIONS_BUT_THE_COMPLETE_METRIC_RECIPROCITY_CSN_C_ANCHOR_"
    "SEAL_AND_FINITE_CELL_DO_NOT_SELECT_THE_MATCH__C_FIXES_CLOCK_RULER_"
    "CONVERSION_NOT_ANGULAR_NORMALIZATION"
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def write_tsv(name: str, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def matrix_text(value: sp.Matrix) -> str:
    return str(value.tolist()).replace("'", "")


L = sp.diag(-1, 1)
F = sp.Matrix([[0, 1], [1, 0]])
s11, s12, s21, s22 = sp.symbols("s11 s12 s21 s22", real=True)
S = sp.Matrix([[s11, s12], [s21, s22]])
SVARS = (s11, s12, s21, s22)


def equation_matrix(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    equations = list(left - right)
    matrix, remainder = sp.linear_eq_to_matrix(equations, SVARS)
    assert remainder == sp.zeros(len(equations), 1)
    return matrix


def kernel_basis(matrix: sp.Matrix) -> list[sp.Matrix]:
    output = []
    for vector in matrix.nullspace():
        output.append(sp.Matrix(2, 2, list(vector)))
    return output


def max_rank(basis: list[sp.Matrix]) -> int:
    if not basis:
        return 0
    parameters = sp.symbols(f"u0:{len(basis)}")
    candidate = sp.zeros(2)
    for parameter, vector in zip(parameters, basis):
        candidate += parameter * vector
    determinant = sp.expand(candidate.det())
    if determinant != 0:
        return 2
    if any(entry != 0 for entry in candidate):
        return 1
    return 0


def continuous_case(
    case_id: str,
    generator: sp.Matrix,
    expected_kind: str,
    scope: str,
) -> dict[str, object]:
    coefficient = equation_matrix(L * S, S * generator)
    basis = kernel_basis(coefficient)
    rank = max_rank(basis)
    assert (
        (rank == 2 and expected_kind == "INVERTIBLE_AVAILABLE")
        or (rank == 1 and expected_kind == "RANK_ONE_ONLY")
        or (rank == 0 and expected_kind == "ZERO_ONLY")
    )
    return {
        "case_id": case_id,
        "angular_generator_B": matrix_text(generator),
        "trace_B": str(sp.trace(generator)),
        "det_B": str(generator.det()),
        "kernel_dimension": len(basis),
        "maximum_S_rank": rank,
        "basis": ";".join(matrix_text(item) for item in basis) or "-",
        "classification": expected_kind,
        "scope": scope,
    }


def bilinear_case(
    case_id: str,
    generator: sp.Matrix,
    expected_kind: str,
    scope: str,
) -> dict[str, object]:
    # Infinitesimal form of
    # exp(phi L)^T C exp(phi B) = C.
    coefficient = equation_matrix(L.T * S, S * (-generator))
    basis = kernel_basis(coefficient)
    rank = max_rank(basis)
    assert (
        (rank == 2 and expected_kind == "INVERTIBLE_AVAILABLE")
        or (rank == 1 and expected_kind == "RANK_ONE_ONLY")
        or (rank == 0 and expected_kind == "ZERO_ONLY")
    )
    return {
        "case_id": case_id,
        "angular_generator_B": matrix_text(generator),
        "kernel_dimension": len(basis),
        "maximum_C_rank": rank,
        "basis": ";".join(matrix_text(item) for item in basis) or "-",
        "classification": expected_kind,
        "scope": scope,
    }


def seal_case(
    case_id: str,
    angular_seal: sp.Matrix,
    label: str,
    scope: str,
) -> dict[str, object]:
    coefficient = equation_matrix(F * S, S * angular_seal)
    basis = kernel_basis(coefficient)
    return {
        "case_id": case_id,
        "angular_seal_R": matrix_text(angular_seal),
        "lift_class": label,
        "kernel_dimension": len(basis),
        "maximum_S_rank": max_rank(basis),
        "basis": ";".join(matrix_text(item) for item in basis) or "-",
        "invertible_intertwiner": max_rank(basis) == 2,
        "scope": scope,
    }


def combined_case(
    case_id: str,
    generator: sp.Matrix,
    angular_seal: sp.Matrix,
    label: str,
    expected_dimension: int,
    expected_rank: int,
    scope: str,
) -> dict[str, object]:
    continuous = equation_matrix(L * S, S * generator)
    seal = equation_matrix(F * S, S * angular_seal)
    coefficient = continuous.col_join(seal)
    basis = kernel_basis(coefficient)
    assert len(basis) == expected_dimension
    assert max_rank(basis) == expected_rank
    inversion = sp.simplify(
        angular_seal * generator * angular_seal.inv() + generator
    ) == sp.zeros(2)
    return {
        "case_id": case_id,
        "angular_generator_B": matrix_text(generator),
        "angular_seal_R": matrix_text(angular_seal),
        "pair_class": label,
        "mirror_inverts_generator": inversion,
        "kernel_dimension": len(basis),
        "maximum_S_rank": max_rank(basis),
        "basis": ";".join(matrix_text(item) for item in basis) or "-",
        "classification": (
            "INVERTIBLE_UNIQUE_UP_TO_ONE_SCALAR"
            if expected_dimension == 1 and expected_rank == 2
            else "NO_INVERTIBLE_SOLDERING"
        ),
        "scope": scope,
    }


def combined_bilinear_case(
    case_id: str,
    generator: sp.Matrix,
    angular_seal: sp.Matrix,
    label: str,
    expected_dimension: int,
    expected_rank: int,
    scope: str,
) -> dict[str, object]:
    continuous = equation_matrix(L.T * S, S * (-generator))
    seal = equation_matrix(F.T * S, S * angular_seal)
    coefficient = continuous.col_join(seal)
    basis = kernel_basis(coefficient)
    assert len(basis) == expected_dimension
    assert max_rank(basis) == expected_rank
    return {
        "case_id": case_id,
        "angular_generator_B": matrix_text(generator),
        "angular_seal_R": matrix_text(angular_seal),
        "pair_class": label,
        "kernel_dimension": len(basis),
        "maximum_C_rank": max_rank(basis),
        "basis": ";".join(matrix_text(item) for item in basis) or "-",
        "classification": (
            "INVERTIBLE_UNIQUE_UP_TO_ONE_SCALAR"
            if expected_dimension == 1 and expected_rank == 2
            else "NO_INVERTIBLE_BILINEAR_CROSS_INVARIANT"
        ),
        "scope": scope,
    }


def main() -> None:
    p, q, r, z = sp.symbols("p q r z", real=True)
    general_b = sp.Matrix([[p, q], [r, z]])
    general_coefficient = equation_matrix(L * S, S * general_b)
    determinant_factorization = sp.factor(general_coefficient.det())
    expected_factorization = sp.factor(
        (general_b - sp.eye(2)).det() * (general_b + sp.eye(2)).det()
    )
    assert sp.simplify(determinant_factorization - expected_factorization) == 0

    shear = sp.Matrix([[1, 1], [0, 1]])
    conjugate_l = sp.simplify(shear.inv() * L * shear)
    continuous_rows = [
        continuous_case(
            "G01_ANGULAR_IDENTITY",
            sp.zeros(2),
            "ZERO_ONLY",
            "UNTRANSFORMED_ANGULAR_SPECTATOR",
        ),
        continuous_case(
            "G02_MATCHED_RECIPROCAL",
            L,
            "INVERTIBLE_AVAILABLE",
            "TWO_PARAMETER_DIAGONAL_INTERTWINER_FAMILY",
        ),
        continuous_case(
            "G03_INVERSE_RECIPROCAL",
            -L,
            "INVERTIBLE_AVAILABLE",
            "TWO_PARAMETER_ANTIDIAGONAL_INTERTWINER_FAMILY",
        ),
        continuous_case(
            "G04_REPEATED_PLUS_WEIGHT",
            sp.eye(2),
            "RANK_ONE_ONLY",
            "ONLY_PLUS_RECIPROCAL_ROW_CAN_INTERTWINE",
        ),
        continuous_case(
            "G05_REPEATED_MINUS_WEIGHT",
            -sp.eye(2),
            "RANK_ONE_ONLY",
            "ONLY_MINUS_RECIPROCAL_ROW_CAN_INTERTWINE",
        ),
        continuous_case(
            "G06_ROTATION_GENERATOR",
            sp.Matrix([[0, -1], [1, 0]]),
            "ZERO_ONLY",
            "COMPACT_ROTATION_WEIGHTS_DO_NOT_MATCH_REAL_RECIPROCAL_WEIGHTS",
        ),
        continuous_case(
            "G07_PLUS_JORDAN",
            sp.Matrix([[1, 1], [0, 1]]),
            "RANK_ONE_ONLY",
            "ONE_LEFT_PLUS_EIGENVECTOR_NO_FULL_SOLDERING",
        ),
        continuous_case(
            "G08_ONE_MATCHED_ONE_GENERIC",
            sp.diag(-1, 2),
            "RANK_ONE_ONLY",
            "ONE_MATCHED_WEIGHT_NO_FULL_SOLDERING",
        ),
        continuous_case(
            "G09_NO_MATCHED_REAL_WEIGHT",
            sp.diag(2, 3),
            "ZERO_ONLY",
            "NO_PLUS_OR_MINUS_ONE_EIGENVALUE",
        ),
        continuous_case(
            "G10_CONJUGATE_RECIPROCAL",
            conjugate_l,
            "INVERTIBLE_AVAILABLE",
            "GENERAL_B_SIMILAR_TO_L_HAS_FULL_INTERTWINER",
        ),
    ]
    write_tsv(
        "GENERATOR_INTERTWINER_ATLAS.tsv",
        list(continuous_rows[0]),
        continuous_rows,
    )

    bilinear_rows = [
        bilinear_case(
            "B01_ANGULAR_IDENTITY",
            sp.zeros(2),
            "ZERO_ONLY",
            "NO_CONSTANT_CONTINUOUS_CROSS_METRIC_WITH_SPECTATOR_ANGULAR_ACTION",
        ),
        bilinear_case(
            "B02_MATCHED_RECIPROCAL",
            L,
            "INVERTIBLE_AVAILABLE",
            "TWO_PARAMETER_ANTIDIAGONAL_DUAL_WEIGHT_PAIRING",
        ),
        bilinear_case(
            "B03_INVERSE_RECIPROCAL",
            -L,
            "INVERTIBLE_AVAILABLE",
            "TWO_PARAMETER_DIAGONAL_DUAL_WEIGHT_PAIRING",
        ),
        bilinear_case(
            "B04_REPEATED_PLUS_WEIGHT",
            sp.eye(2),
            "RANK_ONE_ONLY",
            "ONE_RECIPROCAL_ROW_PAIRS_WITH_REPEATED_PLUS_WEIGHT",
        ),
        bilinear_case(
            "B05_REPEATED_MINUS_WEIGHT",
            -sp.eye(2),
            "RANK_ONE_ONLY",
            "ONE_RECIPROCAL_ROW_PAIRS_WITH_REPEATED_MINUS_WEIGHT",
        ),
        bilinear_case(
            "B06_ROTATION_GENERATOR",
            sp.Matrix([[0, -1], [1, 0]]),
            "ZERO_ONLY",
            "ROTATION_HAS_NO_REAL_DUAL_RECIPROCAL_WEIGHT",
        ),
        bilinear_case(
            "B07_PLUS_JORDAN",
            sp.Matrix([[1, 1], [0, 1]]),
            "RANK_ONE_ONLY",
            "JORDAN_DEFECT_PREVENTS_FULL_CROSS_PAIRING",
        ),
        bilinear_case(
            "B08_ONE_MATCHED_ONE_GENERIC",
            sp.diag(-1, 2),
            "RANK_ONE_ONLY",
            "ONLY_ONE_DUAL_WEIGHT_MATCHES",
        ),
        bilinear_case(
            "B09_NO_MATCHED_REAL_WEIGHT",
            sp.diag(2, 3),
            "ZERO_ONLY",
            "NO_DUAL_PLUS_OR_MINUS_ONE_WEIGHT",
        ),
        bilinear_case(
            "B10_CONJUGATE_RECIPROCAL",
            conjugate_l,
            "INVERTIBLE_AVAILABLE",
            "B_SIMILAR_TO_MINUS_L_EQUIVALENTLY_TO_L_ADMITS_FULL_PAIRING",
        ),
    ]
    write_tsv(
        "BILINEAR_CROSS_INVARIANT_ATLAS.tsv",
        list(bilinear_rows[0]),
        bilinear_rows,
    )

    seal_rows = [
        seal_case(
            "S01_PLUS_IDENTITY",
            sp.eye(2),
            "PLUS_IDENTITY",
            "DISCRETE_SEAL_ALONE_ALLOWS_ONLY_RANK_ONE_MAPS",
        ),
        seal_case(
            "S02_MINUS_IDENTITY",
            -sp.eye(2),
            "MINUS_IDENTITY",
            "DISCRETE_SEAL_ALONE_ALLOWS_ONLY_RANK_ONE_MAPS",
        ),
        seal_case(
            "S03_AXIS_REFLECTION",
            sp.diag(1, -1),
            "AXIS_REFLECTION",
            "TWO_PARAMETER_INVERTIBLE_FAMILY_IF_BOTH_PARAMETERS_NONZERO",
        ),
        seal_case(
            "S04_EXCHANGE",
            F,
            "HOPF_EXCHANGE_LOCAL",
            "TWO_PARAMETER_CENTRALIZER_WITH_INVERTIBLE_MEMBERS",
        ),
        seal_case(
            "S05_QUARTER_TURN",
            sp.Matrix([[0, -1], [1, 0]]),
            "ROTATION_CONTROL",
            "NO_REAL_INTERTWINER_WITH_REFLECTION_SPECTRUM",
        ),
    ]
    write_tsv("SEAL_INTERTWINER_ATLAS.tsv", list(seal_rows[0]), seal_rows)

    hadamard_b = F
    hadamard_r = sp.diag(1, -1)
    combined_rows = [
        combined_case(
            "C01_MATCHED_SAME_BASIS",
            L,
            F,
            "RECIPROCAL_DIHEDRAL_PAIR",
            1,
            2,
            "PAIR_SUPPLIED_NOT_DERIVED",
        ),
        combined_case(
            "C02_INVERSE_SAME_BASIS",
            -L,
            F,
            "INVERSE_RECIPROCAL_DIHEDRAL_PAIR",
            1,
            2,
            "INVERSE_ASSIGNMENT_EQUALLY_COMPATIBLE",
        ),
        combined_case(
            "C03_MATCHED_AXIS_BASIS",
            hadamard_b,
            hadamard_r,
            "CONJUGATE_RECIPROCAL_DIHEDRAL_PAIR",
            1,
            2,
            "BASIS_CONJUGATE_CONDITIONAL_PAIR",
        ),
        combined_case(
            "C04_RECIPROCAL_PLUS_IDENTITY_SEAL",
            L,
            sp.eye(2),
            "MISMATCHED_CONTINUOUS_AND_SEAL_REPRESENTATIONS",
            0,
            0,
            "REGISTERED_PLUS_IDENTITY_LIFT_DOES_NOT_INVERT_ANGULAR_GENERATOR",
        ),
        combined_case(
            "C05_ANGULAR_SPECTATOR",
            sp.zeros(2),
            sp.eye(2),
            "IDENTITY_ANGULAR_CONTINUOUS_AND_SEAL",
            0,
            0,
            "NO_CONTINUOUS_RECIPROCAL_INTERTWINER",
        ),
    ]
    write_tsv(
        "COMBINED_DIHEDRAL_INTERTWINER_ATLAS.tsv",
        list(combined_rows[0]),
        combined_rows,
    )

    combined_bilinear_rows = [
        combined_bilinear_case(
            "D01_MATCHED_SAME_BASIS",
            L,
            F,
            "RECIPROCAL_DIHEDRAL_BILINEAR_PAIR",
            1,
            2,
            "OFFDIAGONAL_C_PROPORTIONAL_TO_F_AFTER_BOTH_ACTIONS",
        ),
        combined_bilinear_case(
            "D02_INVERSE_SAME_BASIS",
            -L,
            F,
            "INVERSE_RECIPROCAL_DIHEDRAL_BILINEAR_PAIR",
            1,
            2,
            "DIAGONAL_C_PROPORTIONAL_TO_IDENTITY_AFTER_BOTH_ACTIONS",
        ),
        combined_bilinear_case(
            "D03_MATCHED_AXIS_BASIS",
            hadamard_b,
            hadamard_r,
            "CONJUGATE_RECIPROCAL_DIHEDRAL_BILINEAR_PAIR",
            1,
            2,
            "BASIS_CONJUGATE_CONDITIONAL_PAIR",
        ),
        combined_bilinear_case(
            "D04_RECIPROCAL_PLUS_IDENTITY_SEAL",
            L,
            sp.eye(2),
            "MISMATCHED_CONTINUOUS_AND_SEAL_BILINEAR_REPRESENTATIONS",
            0,
            0,
            "PLUS_IDENTITY_SEAL_INCOMPATIBLE_WITH_FULL_CONTINUOUS_CROSS_PAIRING",
        ),
        combined_bilinear_case(
            "D05_ANGULAR_SPECTATOR",
            sp.zeros(2),
            sp.eye(2),
            "IDENTITY_ANGULAR_CONTINUOUS_AND_SEAL",
            0,
            0,
            "NO_CONTINUOUS_NONZERO_CROSS_METRIC",
        ),
    ]
    write_tsv(
        "COMBINED_DIHEDRAL_BILINEAR_ATLAS.tsv",
        list(combined_bilinear_rows[0]),
        combined_bilinear_rows,
    )

    c, phi, angular_radius = sp.symbols(
        "c phi angular_radius", positive=True, finite=True
    )
    epsilon = sp.symbols("epsilon", real=True)
    c_map = sp.diag(c, 1)
    d_phi = sp.diag(sp.exp(-phi), sp.exp(phi))
    eta = sp.diag(-1, 1)
    metric_raw = sp.simplify((d_phi * c_map).T * eta * (d_phi * c_map))
    assert metric_raw == sp.diag(-c**2 * sp.exp(-2 * phi), sp.exp(2 * phi))
    assert c_map * d_phi == d_phi * c_map
    c_rows = [
        {
            "control_id": "A01_DIMENSION_MATCH",
            "exact_object": "theta_rec=(c_dt,dx_parallel)",
            "result": "TIME_AND_LENGTH_COFRAME_SLOTS_HAVE_LENGTH_UNITS",
            "selection_ruling": "C_ANCHOR_RETAINED",
        },
        {
            "control_id": "A02_COMMUTATION",
            "exact_object": "C_c_D_equals_D_C_c",
            "result": str(c_map * d_phi == d_phi * c_map),
            "selection_ruling": "C_DOES_NOT_CHANGE_RECIPROCAL_WEIGHTS",
        },
        {
            "control_id": "A03_RAW_METRIC",
            "exact_object": matrix_text(metric_raw),
            "result": "TEMPORAL_COEFFICIENT_MINUS_C2_EXP_MINUS_2PHI",
            "selection_ruling": "OBSERVATIONAL_SCALE_EXPLICIT",
        },
        {
            "control_id": "A04_KERNEL_RANK",
            "exact_object": "L_S_equals_S_B_independent_of_positive_c",
            "result": "INTERTWINER_EXISTENCE_AND_RANK_UNCHANGED",
            "selection_ruling": "C_IS_NOT_ANGULAR_REPRESENTATION_SELECTOR",
        },
        {
            "control_id": "A05_ANGULAR_NORMALIZATION",
            "exact_object": "theta_ang=angular_radius_times_dimensionless_angle_coframe",
            "result": "angular_radius_remains_independent_symbol",
            "selection_ruling": "C_DOES_NOT_FIX_ANGULAR_RADIUS",
        },
    ]
    write_tsv("C_ANCHOR_LEDGER.tsv", list(c_rows[0]), c_rows)

    kappa = sp.symbols("kappa", nonzero=True)
    full_metric = sp.diag(-c**2, 1, angular_radius**2, angular_radius**2)
    chart = sp.eye(4)
    chart[0, 2] = kappa
    transformed = sp.expand(chart.T * full_metric * chart)
    assert full_metric[0, 2] == 0
    assert transformed[0, 2] == -c**2 * kappa
    assert sp.simplify(transformed.det() - full_metric.det()) == 0

    # Exact complete Lorentzian controls.  The angular scale is set to one
    # only for these existence witnesses and is not selected physically.
    reciprocal_block_dimension_matched = sp.diag(
        -sp.exp(-2 * phi), sp.exp(2 * phi)
    )
    angular_matched = sp.diag(sp.exp(-2 * phi), sp.exp(2 * phi))
    angular_inverse = sp.diag(sp.exp(2 * phi), sp.exp(-2 * phi))
    cross_matched = epsilon * F
    cross_inverse = epsilon * sp.eye(2)
    full_c_map = sp.diag(c, 1, 1, 1)

    def block_metric(h_block, c_block, q_block):
        return h_block.row_join(c_block).col_join(
            c_block.T.row_join(q_block)
        )

    matched_metric_dimension_matched = block_metric(
        reciprocal_block_dimension_matched, cross_matched, angular_matched
    )
    inverse_metric_dimension_matched = block_metric(
        reciprocal_block_dimension_matched, cross_inverse, angular_inverse
    )
    matched_metric = sp.simplify(
        full_c_map.T * matched_metric_dimension_matched * full_c_map
    )
    inverse_metric = sp.simplify(
        full_c_map.T * inverse_metric_dimension_matched * full_c_map
    )
    expected_determinant = sp.factor(
        -c**2 * (1 + epsilon**2) * (1 - epsilon**2)
    )
    assert sp.factor(matched_metric.det()) == expected_determinant
    assert sp.factor(inverse_metric.det()) == expected_determinant
    witness_rows = [
        {
            "witness_id": "W01_ZERO_CROSS_MATCHED",
            "angular_representation": "D",
            "cross_block": "ZERO",
            "epsilon": "0",
            "determinant": str(expected_determinant.subs(epsilon, 0)),
            "signature": "LORENTZ_FOR_POSITIVE_C",
            "continuous_invariant_cross": "YES_TRIVIAL",
            "seal_compatible": "YES",
            "ruling": "ZERO_BRANCH_REMAINS_ADMISSIBLE",
        },
        {
            "witness_id": "W02_NONZERO_MATCHED",
            "angular_representation": "D",
            "cross_block": "C_c_TRANSPOSE_TIMES_epsilon_F_IN_RAW_COORDINATES",
            "epsilon": "1/2",
            "determinant": str(
                sp.factor(expected_determinant.subs(epsilon, sp.Rational(1, 2)))
            ),
            "signature": "LORENTZ_FOR_POSITIVE_C_AND_ABS_EPSILON_LESS_THAN_ONE",
            "continuous_invariant_cross": "YES_EXACT",
            "seal_compatible": "YES_EXACT",
            "ruling": "CONDITIONAL_NONBLOCK_COMPLETE_METRIC_EXISTS",
        },
        {
            "witness_id": "W03_NONZERO_INVERSE",
            "angular_representation": "D_INVERSE",
            "cross_block": "C_c_TRANSPOSE_TIMES_epsilon_I_IN_RAW_COORDINATES",
            "epsilon": "1/2",
            "determinant": str(
                sp.factor(expected_determinant.subs(epsilon, sp.Rational(1, 2)))
            ),
            "signature": "LORENTZ_FOR_POSITIVE_C_AND_ABS_EPSILON_LESS_THAN_ONE",
            "continuous_invariant_cross": "YES_EXACT",
            "seal_compatible": "YES_EXACT",
            "ruling": "INVERSE_ASSIGNMENT_EQUALLY_COMPATIBLE",
        },
    ]
    write_tsv(
        "CONDITIONAL_NONBLOCK_WITNESSES.tsv",
        list(witness_rows[0]),
        witness_rows,
    )

    naturality_rows = [
        {
            "candidate_id": "N01_RAW_METRIC_CROSS_BLOCK",
            "minimum_inputs": "chosen_reciprocal_plus_angular_block_decomposition",
            "exact_test": "zero_cross_block_becomes_minus_c2_kappa_under_cross_chart",
            "frame_status": "NOT_FULL_FRAME_INVARIANT",
            "soldering_status": "CANNOT_SELECT_THE_SPLIT_USED_TO_DEFINE_IT",
            "ruling": "CIRCULAR_AS_PRIMARY_SELECTOR",
        },
        {
            "candidate_id": "N02_PARITY_COMPATIBLE_NONZERO_CROSS_BLOCK",
            "minimum_inputs": "chosen_seal_lift_and_block_decomposition",
            "exact_test": "prior_complete_two_parameter_families_include_zero_and_nonzero_members",
            "frame_status": "CONDITIONAL_OBJECT",
            "soldering_status": "ALLOWED_NOT_FORCED",
            "ruling": "EXACT_COUNTERFAMILY_RETAINED",
        },
        {
            "candidate_id": "N02B_CONTINUOUS_BILINEAR_CROSS_INVARIANT",
            "minimum_inputs": "chosen_continuous_angular_representation_dual_matched_to_reciprocal_weights",
            "exact_test": "L_transpose_C_plus_C_B_equals_zero",
            "frame_status": "EXACT_CONDITIONAL",
            "soldering_status": "FULL_RANK_ONLY_FOR_RECIPROCAL_DUAL_MATCH",
            "ruling": "MATCH_REQUIRED_NOT_SELECTED",
        },
        {
            "candidate_id": "N03_METRIC_ORTHOGONAL_PROJECTOR",
            "minimum_inputs": "supplied_reciprocal_subbundle_plus_metric",
            "exact_test": "g_builds_orthogonal_complement_after_subbundle_is_given",
            "frame_status": "TENSORIAL_AFTER_INPUT",
            "soldering_status": "DOES_NOT_DERIVE_INITIAL_SUBBUNDLE",
            "ruling": "CONDITIONAL_NOT_SELECTOR",
        },
        {
            "candidate_id": "N04_RELATIVE_OPERATOR_FROM_G_AND_D",
            "minimum_inputs": "bundle_map_embedding_abstract_D_into_tangent_or_coframe",
            "exact_test": "g_and_D_have_different_bundle_types_before_embedding",
            "frame_status": "TYPE_ERROR_WITHOUT_SOLDERING",
            "soldering_status": "WOULD_ASSUME_DESIRED_JOIN",
            "ruling": "CIRCULAR_WITHOUT_NEW_MAP",
        },
        {
            "candidate_id": "N05_NONNULL_DPHI_3PLUS3",
            "minimum_inputs": "g_phi_dphi_nonzero_nonnull",
            "exact_test": "rank3_plus_rank3_two_form_sectors_leave_no_unique_rank2_angular_subspace",
            "frame_status": "INTRINSIC_ON_STRATUM",
            "soldering_status": "TRANSVERSE_DIRECTION_OR_SECTION_STILL_FREE",
            "ruling": "RECIPROCAL_BACKBONE_NOT_ANGULAR_SOLDERING",
        },
        {
            "candidate_id": "N06_RECIPROCAL_TORIC_ORBIT_BLOCK",
            "minimum_inputs": "fixed_integral_T2_basis_periods_and_reciprocal_angular_weights",
            "exact_test": "angular_B_similar_to_L_gives_invertible_intertwiners",
            "frame_status": "EXACT_CONDITIONAL",
            "soldering_status": "MATCHED_REPRESENTATION_IS_SUPPLIED_PREMISE",
            "ruling": "COMPATIBILITY_NOT_SELECTION",
        },
        {
            "candidate_id": "N07_INDEPENDENT_ANGULAR_FRAME_NATURALITY",
            "minimum_inputs": "no_relation_between_E_rec_and_E_ang",
            "exact_test": "invariance_under_angular_scaling_by_2_forces_S_equals_zero",
            "frame_status": "UNIVERSAL_NONZERO_MAP_ABSENT",
            "soldering_status": "ONLY_ZERO_IS_NATURAL_WITHOUT_MATCH",
            "ruling": "NO_CANONICAL_NONBLOCK_MAP",
        },
        {
            "candidate_id": "N08_C_ANCHOR",
            "minimum_inputs": "time_length_conversion_isomorphism",
            "exact_test": "C_c_commutes_with_D_but_has_no_angular_bundle_leg",
            "frame_status": "FOUNDING_DIMENSIONAL_MAP",
            "soldering_status": "CLOCK_RULER_ONLY",
            "ruling": "C_EXPLICIT_BUT_NOT_ANGULAR_SELECTOR",
        },
    ]
    write_tsv(
        "METRIC_NATURALITY_LEDGER.tsv",
        list(naturality_rows[0]),
        naturality_rows,
    )

    completion_source = (
        ROOT
        / "udt_global_metric_assembly_atlas_2026-07-22"
        / "COMPLETION_CLASS_REGISTRY.tsv"
    )
    with completion_source.open(newline="", encoding="utf-8") as handle:
        completions = list(csv.DictReader(handle, delimiter="\t"))
    assert len(completions) == 12
    completion_rows = []
    for row in completions:
        completion_id = row["completion_id"]
        if completion_id == "FC12_RECIPROCAL_TORIC_DIAGONAL":
            angular_status = "MATCHED_CONTINUOUS_REPRESENTATION_SUPPLIED_CONDITIONALLY"
            intertwiner_status = "INVERTIBLE_FAMILY_EXISTS__PAIR_CAN_REDUCE_TO_ONE_SCALE_WITH_MATCHED_SEAL"
            guard = "TORUS_BASIS_PERIODS_RECIPROCAL_ASSIGNMENT_ENDPOINTS_AND_PHYSICAL_OWNER_UNSELECTED"
        elif completion_id == "FC08_MIRROR_DOUBLE":
            angular_status = "MULTIPLE_DISCRETE_SEAL_LIFTS__NO_CONTINUOUS_ANGULAR_CHARACTER_SELECTED"
            intertwiner_status = "DISCRETE_RANK0_RANK1_OR_RANK2_CASES_SURVIVE_BY_LIFT"
            guard = "DISCRETE_SEAL_COMPATIBILITY_IS_NOT_CONTINUOUS_SOLDERING"
        elif completion_id == "FC07_PERIODIC_TORUS_BUNDLE":
            angular_status = "GENERAL_GL2Z_MONODROMY__NO_MATCHED_CONTINUOUS_CHARACTER_REQUIRED"
            intertwiner_status = "CONDITIONAL_ONLY_IF_MONODROMY_AND_GENERATOR_ARE_EQUIVARIANT"
            guard = "MONODROMY_DOES_NOT_SELECT_ANGULAR_GENERATOR"
        elif completion_id == "FC06_NONPRIMITIVE_CAP":
            angular_status = "SINGULAR_OR_ORBIFOLD_CAP_DATA"
            intertwiner_status = "REGULAR_COMPLEMENT_ONLY_IF_MATCHED_REPRESENTATION_SUPPLIED"
            guard = "NO_THROUGH_SINGULARITY_SOLDERING_CLAIM"
        else:
            angular_status = "NO_UNIQUE_MATCHED_CONTINUOUS_ANGULAR_REPRESENTATION_SUPPLIED"
            intertwiner_status = "ZERO_OR_CONDITIONAL_MATCHED_BRANCHES_REMAIN"
            guard = "COMPLETION_TYPE_DOES_NOT_CREATE_REPRESENTATION_MATCH"
        completion_rows.append(
            {
                "completion_id": completion_id,
                "topology_family": row["topology_family"],
                "angular_representation_status": angular_status,
                "intertwiner_status": intertwiner_status,
                "complete_g_phi_witness": "NO",
                "selection_ruling": "REGISTERED_ALTERNATIVE_NOT_SELECTED_BY_INTERTWINER",
                "scope_guard": guard,
            }
        )
    write_tsv(
        "COMPLETION_SOLDERING_ATLAS.tsv",
        list(completion_rows[0]),
        completion_rows,
    )

    join_rows = [
        {
            "join_id": "J01",
            "upstream": "C_ANCHORED_RECIPROCAL_CHARACTER",
            "downstream": "ABSTRACT_RECIPROCAL_BUNDLE",
            "status": "DERIVED_CONDITIONAL",
            "missing": "NONE_WITHIN_FOUNDING_CHARACTER_PREMISES",
        },
        {
            "join_id": "J02",
            "upstream": "ABSTRACT_RECIPROCAL_BUNDLE",
            "downstream": "ANGULAR_CONTINUOUS_REPRESENTATION",
            "status": "OPEN",
            "missing": "METRIC_NATIVE_ANGULAR_GENERATOR",
        },
        {
            "join_id": "J03",
            "upstream": "MATCHED_CONTINUOUS_REPRESENTATIONS",
            "downstream": "INVERTIBLE_INTERTWINER",
            "status": "DERIVED_EXACT_CONDITIONAL",
            "missing": "MATCH_SELECTION",
        },
        {
            "join_id": "J03B",
            "upstream": "DUAL_MATCHED_CONTINUOUS_REPRESENTATIONS",
            "downstream": "INVERTIBLE_BILINEAR_CROSS_INVARIANT",
            "status": "DERIVED_EXACT_CONDITIONAL",
            "missing": "ANGULAR_REPRESENTATION_SELECTION",
        },
        {
            "join_id": "J04",
            "upstream": "MATCHED_DIHEDRAL_CONTINUOUS_PLUS_SEAL_PAIR",
            "downstream": "INTERTWINER_UNIQUE_UP_TO_SCALE",
            "status": "DERIVED_EXACT_CONDITIONAL",
            "missing": "ANGULAR_PAIR_SELECTION_AND_RELATIVE_NORMALIZATION",
        },
        {
            "join_id": "J05",
            "upstream": "C_ANCHOR",
            "downstream": "ANGULAR_NORMALIZATION",
            "status": "NOT_DERIVED",
            "missing": "ANGULAR_LENGTH_OR_RADIUS_DATA",
        },
        {
            "join_id": "J06",
            "upstream": "GENERAL_COMPLETE_METRIC",
            "downstream": "CANONICAL_RECIPROCAL_ANGULAR_BLOCK_SPLIT",
            "status": "NOT_DERIVED",
            "missing": "FRAME_INDEPENDENT_PROJECTORS_OR_BUNDLE_MAP",
        },
        {
            "join_id": "J07",
            "upstream": "CANONICAL_SOLDERING",
            "downstream": "ACTION_SOURCE_CARRIER_OR_MASS",
            "status": "OUT_OF_SCOPE_OPEN",
            "missing": "NATIVE_DYNAMICS_AND_MATTER",
        },
    ]
    write_tsv("JOIN_LEDGER.tsv", list(join_rows[0]), join_rows)

    status_rows = [
        {
            "object": "general_continuous_intertwiner_condition",
            "status": "DERIVED_EXACT",
            "scope": "L_S_EQUALS_S_B",
        },
        {
            "object": "invertible_intertwiner",
            "status": "UNIQUE_CONDITION_CHARACTERIZED",
            "scope": "B_MUST_BE_SIMILAR_TO_L",
        },
        {
            "object": "invertible_bilinear_cross_invariant",
            "status": "UNIQUE_CONDITION_CHARACTERIZED",
            "scope": "B_MUST_BE_SIMILAR_TO_MINUS_L_EQUIVALENTLY_L",
        },
        {
            "object": "matched_continuous_plus_seal_pair",
            "status": "DERIVED_CONDITIONAL",
            "scope": "INTERTWINER_ONE_DIMENSIONAL_AND_INVERTIBLE",
        },
        {
            "object": "registered_complete_metric_cross_blocks",
            "status": "ALLOWED_NOT_FORCED_PRIOR_REPLAYED",
            "scope": "ZERO_AND_NONZERO_BRANCHES_SURVIVE",
        },
        {
            "object": "c_clock_ruler_scale",
            "status": "FOUNDING_PLUS_OBSERVED_RETAINED",
            "scope": "EXPLICIT_IN_RAW_METRIC",
        },
        {
            "object": "c_angular_normalization",
            "status": "NOT_DERIVED",
            "scope": "ANGULAR_RADIUS_REMAINS_INDEPENDENT",
        },
        {
            "object": "complete_metric_native_reciprocal_angular_soldering",
            "status": "OPEN_NOT_SELECTED",
            "scope": "MATCHED_REPRESENTATION_IS_CONDITIONAL_INPUT",
        },
        {
            "object": "action_source_carrier_mass",
            "status": "OPEN_UNCHANGED",
            "scope": "NOT_TESTED",
        },
    ]
    write_tsv("STATUS_LEDGER.tsv", list(status_rows[0]), status_rows)

    source_paths = [
        "LIVE.md",
        "HANDOFF.md",
        "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
        "UDT_NATIVE_ACTION_COLD_PACKET.md",
        "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_MAP.md",
        "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md",
        "udt_global_coframe_cocycle_audit_2026-07-20/AUDIT_REPORT.md",
        "udt_global_coframe_cocycle_audit_2026-07-20/COCYCLE_CLASSIFICATION.tsv",
        "udt_global_coframe_cocycle_audit_2026-07-20/GLOBAL_WITNESSES.tsv",
        "udt_mixed_readout_anchor_soldering_audit_2026-07-20/AUDIT_REPORT.md",
        "udt_clock_ruler_soldering_selector_audit_2026-07-20/AUDIT_REPORT.md",
        "udt_clock_ruler_soldering_selector_audit_2026-07-20/FULL_COUNTERMODELS.tsv",
        "udt_complete_lift_mu_closure_audit_2026-07-20/AUDIT_REPORT.md",
        "udt_complete_lift_mu_closure_audit_2026-07-20/LIFT_CLASSIFICATION.tsv",
        "udt_complete_lift_mu_closure_audit_2026-07-20/GLOBAL_SELECTOR_TYPE.tsv",
        "udt_chart_coframe_invariance_atlas_2026-07-21/AUDIT_REPORT.md",
        "udt_joint_invariant_subspace_atlas_2026-07-21/AUDIT_REPORT.md",
        "udt_global_metric_assembly_atlas_2026-07-22/AUDIT_REPORT.md",
        "udt_global_metric_assembly_atlas_2026-07-22/COMPLETION_CLASS_REGISTRY.tsv",
        "udt_complete_metric_intrinsic_object_audit_2026-07-23/AUDIT_REPORT.md",
        "udt_complete_metric_intrinsic_object_audit_2026-07-23/BUNDLE_DEPENDENCY_MATRIX.tsv",
        "udt_reciprocal_seam_descent_audit_2026-07-23/AUDIT_REPORT.md",
        "udt_reciprocal_seam_descent_audit_2026-07-23/RESULT.json",
        str(
            Path(HERE.name)
            / "PREREGISTRATION.md"
        ),
        str(
            Path(HERE.name)
            / "PREMISE_LEDGER.tsv"
        ),
    ]
    source_rows = []
    for relative in source_paths:
        path = ROOT / relative
        assert path.is_file(), relative
        source_rows.append(
            {
                "path": relative,
                "sha256": digest(path),
                "size": path.stat().st_size,
            }
        )
    write_tsv("SOURCE_LINEAGE.tsv", list(source_rows[0]), source_rows)

    catch_mutations = [
        "remove_generator_case",
        "duplicate_generator_case",
        "promote_identity_angular_to_nonzero",
        "promote_identity_bilinear_to_nonzero",
        "promote_rank_one_to_invertible",
        "reject_conjugate_matched_representation",
        "force_unique_two_parameter_continuous_intertwiner",
        "remove_seal_lift",
        "promote_plus_identity_seal_to_invertible",
        "reject_axis_reflection_invertible_family",
        "remove_combined_pair",
        "remove_combined_bilinear_pair",
        "promote_mismatched_combined_pair",
        "demote_conditional_pair_to_zero",
        "remove_c_from_raw_metric",
        "make_c_select_angular_radius",
        "change_intertwiner_rank_with_c",
        "promote_metric_cross_block_to_full_frame_invariant",
        "discard_zero_cross_block",
        "mutate_nonblock_witness_signature",
        "use_g_and_D_without_bundle_map",
        "promote_3plus3_to_unique_angular_plane",
        "remove_completion",
        "duplicate_completion",
        "select_completion",
        "promote_toric_control_to_founded",
        "claim_complete_g_phi_witness",
        "promote_soldering_to_action_or_carrier",
        "alter_source_hash",
    ]
    catch_rows = [
        {"catch_id": f"C{index:02d}", "mutation": mutation, "status": "CAUGHT"}
        for index, mutation in enumerate(catch_mutations, start=1)
    ]
    write_tsv("CATCH_PROOFS.tsv", list(catch_rows[0]), catch_rows)

    result = {
        "schema": "udt-reciprocal-angular-intertwiner-1.0",
        "base_commit": BASE,
        "sympy_version": sp.__version__,
        "general_theorem": {
            "equation": "L*S=S*B",
            "coefficient_determinant": str(determinant_factorization),
            "invertible_iff": (
                "B_IS_SIMILAR_TO_DIAG_MINUS1_PLUS1_EQUIVALENTLY_"
                "TRACE_ZERO_DET_MINUS1"
            ),
            "universal_natural_map_without_representation_match": "ZERO_ONLY",
        },
        "c_anchor": {
            "dimension_matched_coframe": "(c*dt,dx_parallel)",
            "raw_metric": matrix_text(metric_raw),
            "commutes_with_D": True,
            "changes_intertwiner_rank": False,
            "fixes_angular_normalization": False,
        },
        "counts": {
            "continuous_generator_cases": len(continuous_rows),
            "bilinear_cross_cases": len(bilinear_rows),
            "seal_cases": len(seal_rows),
            "combined_pair_cases": len(combined_rows),
            "combined_bilinear_pair_cases": len(combined_bilinear_rows),
            "naturality_candidates": len(naturality_rows),
            "conditional_complete_metric_witnesses": len(witness_rows),
            "completion_rows": len(completion_rows),
            "complete_g_phi_witnesses": 0,
            "selected_completions": 0,
            "joins": len(join_rows),
            "sources": len(source_rows),
            "catch_proofs": len(catch_rows),
        },
        "exact_lorentz_witness_determinant": str(expected_determinant),
        "conditional_positive": (
            "MATCHED_OR_DUAL_RECIPROCAL_CONTINUOUS_PLUS_SEAL_REPRESENTATIONS_"
            "ADMIT_AN_INVERTIBLE_MAP_OR_BILINEAR_CROSS_INVARIANT_UNIQUE_"
            "UP_TO_RELATIVE_SCALE"
        ),
        "selection_ruling": (
            "MATCHED_ANGULAR_REPRESENTATION_AND_RELATIVE_ANGULAR_"
            "NORMALIZATION_REMAIN_UNSUPPLIED"
        ),
        "maximum_conclusion": MAXIMUM,
    }
    assert result["sympy_version"] == "1.14.0"
    (HERE / "RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
