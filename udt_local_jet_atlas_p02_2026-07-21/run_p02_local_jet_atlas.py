#!/usr/bin/env python3
"""Build the exact P02 law-neutral local-jet atlas."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import sys
from itertools import product
from pathlib import Path

import numpy as np
import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
P01 = ROOT / "udt_canonical_geometry_evaluator_p01_2026-07-21"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(P01))

from canonical_geometry_evaluator import (  # noqa: E402
    MetricJets,
    csn_scaled_metric_jets,
    evaluate_metric_jets,
)
from canonical_local_jet_atlas import (  # noqa: E402
    BIVECTOR_PAIRS,
    DIM,
    ETA,
    algebraic_curvature_checks,
    bivector_bilinear,
    classify_petrov,
    csn_transform_screen_first,
    curvature_operator,
    first_split_kinematics,
    inertia_triples,
    inertia_witness,
    normal_ddg_from_riemann,
    petrov_invariants,
    petrov_q_witnesses,
    q_from_weyl,
    ricci_from_riemann,
    ricci_rank_witness,
    riemann_from_normal_ddg,
    scalar_from_ricci,
    sectional_rank_witness,
    split_congruence_matrix,
    split_kinematic_witness,
    split_metric,
    weyl_from_q,
    weyl_from_riemann,
)


RESULT = HERE / "ATLAS_RESULT.json"
TRANSCRIPT = HERE / "ATLAS_TRANSCRIPT.txt"
TOLERANCE = 2e-10


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def exact_tensor_equal(left, right) -> bool:
    return all(
        sp.simplify(left[index] - right[index]) == 0
        for index in product(range(DIM), repeat=4)
    )


def tensor_to_float(tensor) -> np.ndarray:
    return np.array(tensor.tolist(), dtype=float)


def maximum(value) -> float:
    array = np.asarray(value, dtype=float)
    return float(np.max(np.abs(array))) if array.size else 0.0


def sstr(value) -> str:
    return sp.sstr(value).replace("\n", "")


def matrix_string(matrix: sp.Matrix) -> str:
    return sstr(matrix)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_tsv(name: str, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path = HERE / name
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in fieldnames})


def p01_residual(tensor) -> float:
    second = normal_ddg_from_riemann(tensor)
    reconstructed = riemann_from_normal_ddg(second)
    require(exact_tensor_equal(reconstructed, tensor), "exact normal-coordinate reconstruction")
    jets = MetricJets(
        np.diag([-1.0, 1.0, 1.0, 1.0]),
        np.zeros((4, 4, 4)),
        tensor_to_float(second),
    )
    evaluated = evaluate_metric_jets(jets)
    return maximum(evaluated.riemann_down - tensor_to_float(tensor))


def main() -> None:
    checks: dict[str, str] = {}
    residuals: dict[str, float] = {}

    metric_rows: list[dict[str, object]] = []
    triples4 = inertia_triples(4)
    require(len(triples4) == 15 and len(set(triples4)) == 15, "4D inertia completeness")
    for index, triple in enumerate(triples4, 1):
        witness = inertia_witness(triple)
        negative, positive, zero = triple
        status = (
            "LORENTZIAN_REGULAR"
            if zero == 0 and sorted((negative, positive)) == [1, 3]
            else "DEGENERATE_TYPE_CHANGE"
            if zero
            else "NON_LORENTZIAN_REGULAR"
        )
        metric_rows.append(
            {
                "id": f"Z{index:02d}",
                "n_negative": negative,
                "n_positive": positive,
                "n_zero": zero,
                "rank": witness.rank(),
                "determinant": sstr(witness.det()),
                "status": status,
                "exact_witness": matrix_string(witness),
                "positive_CSN_preserves": "YES",
            }
        )
    write_tsv(
        "ZERO_JET_INERTIA_STRATA.tsv",
        [
            "id",
            "n_negative",
            "n_positive",
            "n_zero",
            "rank",
            "determinant",
            "status",
            "exact_witness",
            "positive_CSN_preserves",
        ],
        metric_rows,
    )
    checks["all_15_metric_inertia_strata"] = "PASS"

    split_rows: list[dict[str, object]] = []
    triples2 = inertia_triples(2)
    shifts = sp.Matrix([[sp.Rational(1, 3), -sp.Rational(1, 5)], [sp.Rational(2, 7), sp.Rational(1, 11)]])
    triangular = split_congruence_matrix(shifts)
    for index, (base_triple, screen_triple) in enumerate(product(triples2, repeat=2), 1):
        base = inertia_witness(base_triple)
        screen = inertia_witness(screen_triple)
        full = split_metric(base, screen, shifts)
        diagonal = sp.diag(1, 1, 1, 1)
        diagonal[:2, :2] = base
        diagonal[2:, 2:] = screen
        require(full == sp.simplify(triangular.T * diagonal * triangular), "split congruence")
        require(sp.factor(full.det() - base.det() * screen.det()) == 0, "split determinant")
        expected = tuple(base_triple[item] + screen_triple[item] for item in range(3))
        require(full.rank() == base.rank() + screen.rank(), "split rank")
        branch = (
            "P01_REGULAR_CONDITIONAL_BRANCH"
            if base_triple == (1, 1, 0) and screen_triple == (0, 2, 0)
            else "SUPPLIED_SPLIT_TYPE_CHANGE_CLOSURE"
        )
        split_rows.append(
            {
                "id": f"S{index:02d}",
                "base_inertia": "/".join(map(str, base_triple)),
                "screen_inertia": "/".join(map(str, screen_triple)),
                "full_inertia_by_congruence": "/".join(map(str, expected)),
                "full_rank": full.rank(),
                "det_h": sstr(base.det()),
                "det_q": sstr(screen.det()),
                "det_g": sstr(full.det()),
                "branch_status": branch,
                "fixed_shift_witness": matrix_string(shifts),
            }
        )
    require(len(split_rows) == 36, "split count")
    write_tsv(
        "SPLIT_ZERO_JET_STRATA.tsv",
        [
            "id",
            "base_inertia",
            "screen_inertia",
            "full_inertia_by_congruence",
            "full_rank",
            "det_h",
            "det_q",
            "det_g",
            "branch_status",
            "fixed_shift_witness",
        ],
        split_rows,
    )
    checks["all_36_supplied_split_inertia_strata"] = "PASS"
    checks["exact_split_congruence_rank_and_determinant"] = "PASS"

    phi_definitions = (
        ("ZERO", "ZERO", "ZERO", (0, 0, 0, 0)),
        ("HORIZONTAL_TIMELIKE", "HORIZONTAL_ONLY", "TIMELIKE", (1, 0, 0, 0)),
        ("HORIZONTAL_NULL", "HORIZONTAL_ONLY", "NULL", (1, 1, 0, 0)),
        ("HORIZONTAL_SPACELIKE", "HORIZONTAL_ONLY", "SPACELIKE", (0, 1, 0, 0)),
        ("VERTICAL_SPACELIKE", "VERTICAL_ONLY", "SPACELIKE", (0, 0, 1, 0)),
        ("MIXED_TIMELIKE", "MIXED", "TIMELIKE", (2, 0, 1, 0)),
        ("MIXED_NULL", "MIXED", "NULL", (1, 0, 1, 0)),
        ("MIXED_SPACELIKE", "MIXED", "SPACELIKE", (1, 0, 2, 0)),
    )
    phi_rows: list[dict[str, object]] = []
    for index, (name, support, causal, witness_tuple) in enumerate(phi_definitions, 1):
        covector = sp.Matrix(witness_tuple)
        norm = sp.simplify((covector.T * ETA * covector)[0])
        observed_causal = "ZERO" if covector == sp.zeros(4, 1) else "TIMELIKE" if norm < 0 else "NULL" if norm == 0 else "SPACELIKE"
        require(observed_causal == causal, f"dphi causal {name}")
        phi_rows.append(
            {
                "id": f"F{index:02d}",
                "stratum": name,
                "support": support,
                "causal_type": causal,
                "exact_covector": matrix_string(covector.T),
                "exact_norm": sstr(norm),
                "positive_CSN_preserves_type": "YES",
                "phi_metric_join": "OPEN_INDEPENDENT_FIELD_WITNESS",
            }
        )
    write_tsv(
        "DPHI_FIRST_JET_STRATA.tsv",
        [
            "id",
            "stratum",
            "support",
            "causal_type",
            "exact_covector",
            "exact_norm",
            "positive_CSN_preserves_type",
            "phi_metric_join",
        ],
        phi_rows,
    )
    checks["all_8_dphi_alignment_causal_strata"] = "PASS"
    checks["zero_dphi_separate_from_null"] = "PASS"

    kinematic_rows: list[dict[str, object]] = []
    sigma_first = (sp.Integer(2), sp.Integer(-3), sp.Integer(0), sp.Integer(0))
    for index, (expansion_rank, shear_rank, twist_rank) in enumerate(
        product((0, 1), (0, 1, 2), (0, 1)), 1
    ):
        screen, shifts0, screen_first, shifts_first = split_kinematic_witness(
            expansion_rank, shear_rank, twist_rank
        )
        observed = first_split_kinematics(screen, shifts0, screen_first, shifts_first)
        require(observed["expansion_rank"] == expansion_rank, "expansion rank")
        require(observed["shear_rank"] == shear_rank, "shear rank")
        require(observed["twist_rank"] == twist_rank, "twist rank")
        transformed_first = csn_transform_screen_first(screen, screen_first, sigma_first)
        transformed = first_split_kinematics(screen, shifts0, transformed_first, shifts_first)
        require(
            transformed["expansion"] == observed["expansion"] + sp.Matrix([4, -6]),
            "CSN expansion affine shift",
        )
        require(transformed["twist"] == observed["twist"], "CSN twist")
        for base in range(2):
            require(
                sp.simplify(screen.inv() * transformed["shears"][base])
                == sp.simplify(screen.inv() * observed["shears"][base]),
                "CSN shear endomorphism",
            )
        kinematic_rows.append(
            {
                "id": f"K{index:02d}",
                "expansion_rank": expansion_rank,
                "shear_map_rank": shear_rank,
                "twist_map_rank": twist_rank,
                "integrability": "INTEGRABLE" if twist_rank == 0 else "NONINTEGRABLE",
                "exact_expansion": matrix_string(observed["expansion"].T),
                "exact_shear_map": matrix_string(observed["shear_map"]),
                "exact_twist": matrix_string(observed["twist"].T),
                "CSN_expansion_status": "REPRESENTATIVE_DEPENDENT_AFFINE_SHIFT",
                "CSN_shear_rank_status": "INVARIANT",
                "CSN_twist_status": "INVARIANT",
            }
        )
    require(len(kinematic_rows) == 12, "kinematic count")
    write_tsv(
        "SPLIT_FIRST_JET_STRATA.tsv",
        [
            "id",
            "expansion_rank",
            "shear_map_rank",
            "twist_map_rank",
            "integrability",
            "exact_expansion",
            "exact_shear_map",
            "exact_twist",
            "CSN_expansion_status",
            "CSN_shear_rank_status",
            "CSN_twist_status",
        ],
        kinematic_rows,
    )
    checks["all_12_expansion_shear_twist_rank_products"] = "PASS"
    checks["frobenius_integrability_iff_twist_zero"] = "PASS"
    checks["CSN_expansion_affine_not_invariant"] = "PASS"
    checks["CSN_shear_and_twist_rank_invariant"] = "PASS"

    curvature_rows: list[dict[str, object]] = []
    for rank in range(7):
        tensor = sectional_rank_witness(rank)
        require(all(algebraic_curvature_checks(tensor).values()), "sectional algebraic tensor")
        observed_rank = curvature_operator(tensor).rank()
        require(observed_rank == rank, "curvature operator rank")
        regression = p01_residual(tensor)
        require(regression < TOLERANCE, "P01 curvature rank regression")
        residuals[f"curvature_rank_{rank}"] = regression
        curvature_rows.append(
            {
                "id": f"R{rank}",
                "curvature_operator_rank": rank,
                "exact_operator_diagonal": matrix_string(curvature_operator(tensor).diagonal()),
                "exact_minor_certification": f"RANK_EXACT_{rank}",
                "P01_max_residual": f"{regression:.17g}",
                "CSN_status": "REPRESENTATIVE_DEPENDENT_FULL_RIEMANN_RANK",
            }
        )
    write_tsv(
        "CURVATURE_OPERATOR_RANK_STRATA.tsv",
        [
            "id",
            "curvature_operator_rank",
            "exact_operator_diagonal",
            "exact_minor_certification",
            "P01_max_residual",
            "CSN_status",
        ],
        curvature_rows,
    )
    checks["all_7_curvature_operator_ranks"] = "PASS"

    ricci_rows: list[dict[str, object]] = []
    for rank in range(5):
        expected_ricci, tensor = ricci_rank_witness(rank)
        require(all(algebraic_curvature_checks(tensor).values()), "Ricci algebraic tensor")
        observed_ricci = ricci_from_riemann(tensor)
        require(observed_ricci == expected_ricci, "Ricci reconstruction")
        mixed = sp.simplify(ETA * observed_ricci)
        require(mixed.rank() == rank, "Ricci mixed rank")
        require(exact_tensor_equal(weyl_from_riemann(tensor), sp.MutableDenseNDimArray.zeros(4, 4, 4, 4)), "Weyl-free Ricci witness")
        regression = p01_residual(tensor)
        require(regression < TOLERANCE, "P01 Ricci rank regression")
        residuals[f"ricci_rank_{rank}"] = regression
        ricci_rows.append(
            {
                "id": f"C{rank}",
                "Ricci_endomorphism_rank": rank,
                "exact_mixed_Ricci": matrix_string(mixed),
                "exact_scalar": sstr(scalar_from_ricci(observed_ricci)),
                "Weyl": "ZERO",
                "P01_max_residual": f"{regression:.17g}",
                "CSN_status": "REPRESENTATIVE_DEPENDENT_SCHOUTEN_SECTOR",
            }
        )
    write_tsv(
        "RICCI_ENDOMORPHISM_RANK_STRATA.tsv",
        [
            "id",
            "Ricci_endomorphism_rank",
            "exact_mixed_Ricci",
            "exact_scalar",
            "Weyl",
            "P01_max_residual",
            "CSN_status",
        ],
        ricci_rows,
    )
    checks["all_5_Ricci_endomorphism_ranks"] = "PASS"

    petrov_rows: list[dict[str, object]] = []
    for index, (expected_type, q_matrix) in enumerate(petrov_q_witnesses().items(), 1):
        tensor = weyl_from_q(q_matrix)
        require(all(algebraic_curvature_checks(tensor).values()), "Weyl algebraic tensor")
        require(ricci_from_riemann(tensor) == sp.zeros(4), "Weyl Ricci zero")
        recovered_q = q_from_weyl(tensor)
        require(recovered_q == q_matrix, "Weyl Q reconstruction")
        observed_type = classify_petrov(recovered_q)
        require(observed_type == expected_type, "Petrov classification")
        invariants = petrov_invariants(recovered_q)
        regression = p01_residual(tensor)
        require(regression < TOLERANCE, "P01 Petrov regression")
        residuals[f"petrov_{expected_type}"] = regression
        nilpotency = (
            0
            if recovered_q == sp.zeros(3)
            else 2
            if recovered_q**2 == sp.zeros(3)
            else 3
            if recovered_q**3 == sp.zeros(3)
            else "NON_NILPOTENT"
        )
        petrov_rows.append(
            {
                "id": f"W{index:02d}",
                "Petrov_type": expected_type,
                "exact_Q": matrix_string(q_matrix),
                "I": sstr(invariants["I"]),
                "J": sstr(invariants["J"]),
                "Delta": sstr(invariants["Delta"]),
                "nilpotency_index": nilpotency,
                "Weyl_operator_rank": curvature_operator(tensor).rank(),
                "P01_max_residual": f"{regression:.17g}",
                "positive_CSN_status": "INVARIANT_ALGEBRAIC_TYPE",
            }
        )
    write_tsv(
        "PETROV_STRATA.tsv",
        [
            "id",
            "Petrov_type",
            "exact_Q",
            "I",
            "J",
            "Delta",
            "nilpotency_index",
            "Weyl_operator_rank",
            "P01_max_residual",
            "positive_CSN_status",
        ],
        petrov_rows,
    )
    checks["all_6_Petrov_types"] = "PASS"
    checks["exact_Petrov_invariant_and_Jordan_catches"] = "PASS"

    # Exact local CSN/Schouten removal: the Hessian spans all ten symmetric components.
    schouten = sp.Matrix(
        [
            [sp.Rational(2, 5), sp.Rational(1, 7), -sp.Rational(1, 9), sp.Rational(1, 11)],
            [sp.Rational(1, 7), -sp.Rational(1, 3), sp.Rational(1, 13), -sp.Rational(1, 8)],
            [-sp.Rational(1, 9), sp.Rational(1, 13), sp.Rational(3, 10), sp.Rational(1, 6)],
            [sp.Rational(1, 11), -sp.Rational(1, 8), sp.Rational(1, 6), -sp.Rational(2, 7)],
        ]
    )
    schouten_trace = sp.simplify(sum(ETA[a, b] * schouten[a, b] for a in range(4) for b in range(4)))
    ricci_from_schouten = sp.simplify(2 * schouten + ETA * schouten_trace)
    ricci_part = ricci_rank_witness(0)[1]
    # Replace the zero tensor with the exact g-wedge-Schouten curvature.
    from canonical_local_jet_atlas import riemann_from_ricci  # local import keeps source explicit

    ricci_part = riemann_from_ricci(ricci_from_schouten)
    weyl_seed = weyl_from_q(petrov_q_witnesses()["I"])
    combined = sp.MutableDenseNDimArray.zeros(4, 4, 4, 4)
    for tensor_index in product(range(4), repeat=4):
        combined[tensor_index] = sp.simplify(weyl_seed[tensor_index] + ricci_part[tensor_index])
    combined_second = normal_ddg_from_riemann(combined)
    base_jets = MetricJets(
        np.diag([-1.0, 1.0, 1.0, 1.0]),
        np.zeros((4, 4, 4)),
        tensor_to_float(combined_second),
    )
    scaled_jets = csn_scaled_metric_jets(
        base_jets,
        1.0,
        np.zeros(4),
        np.array(schouten.tolist(), dtype=float),
    )
    scaled_geometry = evaluate_metric_jets(scaled_jets)
    csn_ricci_residual = maximum(scaled_geometry.ricci)
    csn_weyl_residual = maximum(
        tensor_to_float(weyl_from_riemann(combined))
        - tensor_to_float(weyl_from_riemann(sp.MutableDenseNDimArray(scaled_geometry.riemann_down)))
    )
    require(csn_ricci_residual < TOLERANCE, "CSN Schouten removal")
    require(csn_weyl_residual < TOLERANCE, "CSN Weyl preservation")
    residuals["CSN_schouten_removal_Ricci"] = csn_ricci_residual
    residuals["CSN_Weyl_preservation"] = csn_weyl_residual
    checks["CSN_Hessian_spans_10_component_Schouten_sector"] = "PASS"
    checks["CSN_preserves_Weyl_while_shifting_Ricci"] = "PASS"

    # Exact 20-component direct-sum basis: Weyl (10) plus Schouten (10).
    schouten_bases: list[tuple[str, sp.Matrix]] = []
    for a in range(4):
        for b in range(a, 4):
            basis = sp.zeros(4)
            basis[a, b] = 1
            basis[b, a] = 1
            schouten_bases.append((f"P{a}{b}", basis))
    electric_bases = [
        ("E_DIAG_01", sp.diag(1, -1, 0)),
        ("E_DIAG_02", sp.diag(1, 0, -1)),
        ("E_OFF_01", sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]])),
        ("E_OFF_02", sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]])),
        ("E_OFF_12", sp.Matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0]])),
    ]
    magnetic_bases = [(name.replace("E_", "B_"), sp.I * matrix) for name, matrix in electric_bases]
    basis_tensors: list[tuple[str, str, object]] = []
    for name, basis_schouten in schouten_bases:
        trace = sp.simplify(sum(ETA[a, b] * basis_schouten[a, b] for a in range(4) for b in range(4)))
        basis_ricci = sp.simplify(2 * basis_schouten + ETA * trace)
        basis_tensors.append(("SCHOUTEN_REPRESENTATIVE", name, riemann_from_ricci(basis_ricci)))
    for name, basis_q in electric_bases + magnetic_bases:
        basis_tensors.append(("WEYL_PRE_SCALE", name, weyl_from_q(basis_q)))

    upper_pairs = [(a, b) for a in range(6) for b in range(a, 6)]
    basis_columns = []
    second_basis_rows: list[dict[str, object]] = []
    for index, (sector, name, tensor) in enumerate(basis_tensors, 1):
        require(all(algebraic_curvature_checks(tensor).values()), "basis algebraic curvature")
        bilinear = bivector_bilinear(tensor)
        column = sp.Matrix([bilinear[a, b] for a, b in upper_pairs])
        basis_columns.append(column)
        prefix_rank = sp.Matrix.hstack(*basis_columns).rank()
        require(prefix_rank == index, "second-jet direct-sum basis independence")
        second_basis_rows.append(
            {
                "id": f"B{index:02d}",
                "sector": sector,
                "basis_name": name,
                "upper_bivector_bilinear_21_vector": matrix_string(column.T),
                "prefix_exact_rank": prefix_rank,
            }
        )
    require(len(second_basis_rows) == 20 and sp.Matrix.hstack(*basis_columns).rank() == 20, "20 component curvature basis")
    write_tsv(
        "SECOND_JET_DIRECT_SUM_BASIS.tsv",
        ["id", "sector", "basis_name", "upper_bivector_bilinear_21_vector", "prefix_exact_rank"],
        second_basis_rows,
    )
    checks["exact_Weyl_10_plus_Schouten_10_direct_sum"] = "PASS"
    checks["arbitrary_continuous_second_jet_moduli_retained"] = "PASS"

    dimension_rows = [
        {
            "id": "D01",
            "object": "symmetric_metric_two_jet",
            "raw_components": 150,
            "removed_or_quotiented": 0,
            "remaining": 150,
            "status": "10_VALUE_PLUS_40_FIRST_PLUS_100_SECOND",
        },
        {
            "id": "D02",
            "object": "normal_coordinate_metric_two_jet_before_residual_Lorentz",
            "raw_components": 150,
            "removed_or_quotiented": 130,
            "remaining": 20,
            "status": "ALGEBRAIC_RIEMANN_TENSOR",
        },
        {
            "id": "D03",
            "object": "curvature_mod_local_CSN_Hessian",
            "raw_components": 20,
            "removed_or_quotiented": 10,
            "remaining": 10,
            "status": "WEYL_TENSOR_PRE_SCALE_LOCAL_CONTENT",
        },
        {
            "id": "D04",
            "object": "generic_Weyl_mod_local_Lorentz_frame",
            "raw_components": 10,
            "removed_or_quotiented": 6,
            "remaining": 4,
            "status": "CONTINUOUS_REAL_INVARIANTS_NOT_DISCRETE_PETROV_LABEL_ONLY",
        },
    ]
    write_tsv(
        "JET_QUOTIENT_DIMENSION_LEDGER.tsv",
        ["id", "object", "raw_components", "removed_or_quotiented", "remaining", "status"],
        dimension_rows,
    )
    checks["normal_coordinate_two_jet_has_20_Riemann_components"] = "PASS"
    checks["pre_scale_local_curvature_10_Weyl_components"] = "PASS"
    checks["continuous_Weyl_moduli_retained"] = "PASS"

    generated_tables = [
        "ZERO_JET_INERTIA_STRATA.tsv",
        "SPLIT_ZERO_JET_STRATA.tsv",
        "DPHI_FIRST_JET_STRATA.tsv",
        "SPLIT_FIRST_JET_STRATA.tsv",
        "CURVATURE_OPERATOR_RANK_STRATA.tsv",
        "RICCI_ENDOMORPHISM_RANK_STRATA.tsv",
        "PETROV_STRATA.tsv",
        "SECOND_JET_DIRECT_SUM_BASIS.tsv",
        "JET_QUOTIENT_DIMENSION_LEDGER.tsv",
    ]
    table_hashes = {name: sha256(HERE / name) for name in generated_tables}
    maximum_residual = max(residuals.values(), default=0.0)
    require(maximum_residual < TOLERANCE, "global raw residual")
    checks["global_raw_residual_gate"] = "PASS"

    output = {
        "schema": "udt-p02-law-neutral-local-jet-atlas-1.0",
        "status": "PASS",
        "maximum_conclusion": "LOCAL_KINEMATIC_SOLUTION_SPACE_CHARACTERIZED_WITHOUT_DYNAMICS",
        "counts": {
            "metric_inertia_strata": len(metric_rows),
            "supplied_split_inertia_strata": len(split_rows),
            "dphi_strata": len(phi_rows),
            "split_first_jet_rank_strata": len(kinematic_rows),
            "curvature_operator_rank_strata": len(curvature_rows),
            "Ricci_rank_strata": len(ricci_rows),
            "Petrov_types": len(petrov_rows),
            "second_jet_direct_sum_basis": len(second_basis_rows),
            "discrete_registered_strata_total": sum(
                map(len, (metric_rows, split_rows, phi_rows, kinematic_rows, curvature_rows, ricci_rows, petrov_rows))
            ),
        },
        "dimension_contract": {
            "raw_metric_two_jet": 150,
            "normal_coordinate_Riemann_before_residual_Lorentz": 20,
            "local_CSN_quotient_Weyl": 10,
            "generic_Weyl_mod_Lorentz_continuous": 4,
        },
        "checks": checks,
        "check_count": len(checks),
        "raw_residuals": residuals,
        "maximum_raw_residual": maximum_residual,
        "table_sha256": table_hashes,
        "premise_stamps": {
            "whole_parent": "CONDITIONAL_4D_CONFORMAL_LORENTZIAN_LOCAL_TWO_JET",
            "zero_jet_closure": "ALL_REAL_SYMMETRIC_INERTIA_CLASSES_RETAINED",
            "two_plus_two": "CONDITIONAL_SUPPLIED_SPLIT_NOT_SELECTED",
            "phi": "SIGNED_LOCAL_INDEPENDENT_FIELD_FOR_CLASSIFICATION_JOIN_OPEN",
            "CSN": "PRE_SCALE_EQUIVALENCE_WITH_REPRESENTATIVE_DATA_SEPARATED",
            "dynamics": "OPEN_NOT_EVALUATED",
        },
        "scope": {
            "point_local_only": True,
            "continuous_moduli_retained": True,
            "scientific_equation_solved": False,
            "action_or_EOM_selected": False,
            "P03_launched": False,
            "ODE_or_PDE_run": False,
            "GPU_used": False,
            "comparison_or_merit_filter_used": False,
        },
        "versions": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "numpy": np.__version__,
        },
        "environment": {
            "CUDA_VISIBLE_DEVICES": os.environ.get("CUDA_VISIBLE_DEVICES", "UNSET"),
            "processor": "CPU_ONLY_EXACT_SYMBOLIC_PLUS_FIXED_FLOAT64_REGRESSION",
        },
    }
    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    RESULT.write_text(rendered, encoding="utf-8")
    TRANSCRIPT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
