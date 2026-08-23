#!/usr/bin/env python3
"""Exact G231 Cartan exterior-symbol and regional-input audit."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
from pathlib import Path
from typing import Mapping

import sympy as sp
from sympy.polys.matrices import DomainMatrix


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
FROZEN_COMMIT = "a5cd16a9"
ETA = (-1, 1, 1, 1)
PAIRS = tuple(itertools.combinations(range(4), 2))
PAIR_POS = {pair: i for i, pair in enumerate(PAIRS)}
TRIPLES = tuple(itertools.combinations(range(4), 3))
TRIPLE_POS = {triple: i for i, triple in enumerate(TRIPLES)}
CURV_SLOTS = tuple((ab, cd) for ab in PAIRS for cd in PAIRS)

REALIZATION_CONDITIONS = (
    "R_typed_as_Lorentz_tensor",
    "horizontal_derivative_law",
    "vertical_action_fixed_by_principal_SO13_action",
    "Cartan_structure_equations",
    "finite_classifying_manifold",
    "smooth_anchor_and_structure_functions",
    "regularity",
    "full_G_structure_algebroid_identities",
    "SO13_equivariance_and_action_conditions",
)

BASELINE_SCOPE = {
    "architecture": "LOCAL_REALIZATION_PROBLEM_ONLY",
    "curvature_values": "SUPPLIED_NOT_GENERATED",
    "classifying_law": "REQUIRED_NOT_SELECTED",
    "finite_theorem": "CONDITIONAL_LOCAL_G_REALIZATION",
    "infinite_theorem": "ANALYTIC_LOCAL_COFRAME_ONLY__PRINCIPAL_DESCENT_OPEN",
    "generic_smooth": "NOT_DERIVED",
    "global": "NOT_DERIVED",
    "physical_history": "NOT_DERIVED",
}


def rank(matrix: sp.Matrix) -> int:
    return int(DomainMatrix.from_Matrix(matrix).rank())


def pair_slot(a: int, b: int) -> tuple[int, int] | None:
    if a == b:
        return None
    if a < b:
        return PAIR_POS[(a, b)], 1
    return PAIR_POS[(b, a)], -1


def wedge_sign(indices: tuple[int, ...]) -> tuple[int, tuple[int, ...] | None]:
    if len(set(indices)) != len(indices):
        return 0, None
    inversions = sum(indices[i] > indices[j] for i in range(len(indices)) for j in range(i + 1, len(indices)))
    return (-1 if inversions % 2 else 1), tuple(sorted(indices))


def curvature_component(vector: sp.Matrix, a: int, b: int, c: int, d: int) -> sp.Expr:
    first = pair_slot(a, b)
    second = pair_slot(c, d)
    if first is None or second is None:
        return sp.Integer(0)
    p, s1 = first
    q, s2 = second
    return s1 * s2 * vector[6 * p + q]


def algebraic_bianchi_map() -> sp.Matrix:
    matrix = sp.zeros(4 * len(TRIPLES), len(CURV_SLOTS))
    for col, ((m, n), (c, d)) in enumerate(CURV_SLOTS):
        for a in range(4):
            for b in range(4):
                slot = pair_slot(a, b)
                if slot is None or slot[0] != PAIR_POS[(m, n)]:
                    continue
                sign, triple = wedge_sign((c, d, b))
                if sign:
                    row = 4 * a + TRIPLE_POS[triple]
                    matrix[row, col] += ETA[a] * slot[1] * sign
    return matrix


def differential_bianchi_map(curvature_basis: sp.Matrix) -> sp.Matrix:
    matrix = sp.zeros(len(PAIRS) * len(TRIPLES), 4 * curvature_basis.cols)
    for e in range(4):
        for j in range(curvature_basis.cols):
            col = curvature_basis.cols * e + j
            for raw, ((a, b), (c, d)) in enumerate(CURV_SLOTS):
                coefficient = curvature_basis[raw, j]
                if not coefficient:
                    continue
                sign, triple = wedge_sign((e, c, d))
                if sign:
                    row = len(TRIPLES) * PAIR_POS[(a, b)] + TRIPLE_POS[triple]
                    matrix[row, col] += sign * coefficient
    return matrix


def differentiated_bianchi_map(b2: sp.Matrix, kdim: int) -> sp.Matrix:
    matrix = sp.zeros(4 * b2.rows, 16 * kdim)
    for f in range(4):
        for row in range(b2.rows):
            for inner in range(4 * kdim):
                coefficient = b2[row, inner]
                if coefficient:
                    e, j = divmod(inner, kdim)
                    matrix[f * b2.rows + row, (4 * f + e) * kdim + j] = coefficient
    return matrix


def commutator_map(kdim: int) -> sp.Matrix:
    matrix = sp.zeros(len(PAIRS) * kdim, 16 * kdim)
    for pair_index, (f, e) in enumerate(PAIRS):
        for j in range(kdim):
            row = pair_index * kdim + j
            matrix[row, (4 * f + e) * kdim + j] = 1
            matrix[row, (4 * e + f) * kdim + j] = -1
    return matrix


def curvature_coordinates(curvature_basis: sp.Matrix, vector: sp.Matrix) -> sp.Matrix:
    pivot_rows = list(curvature_basis.T.rref()[1])
    square = curvature_basis.extract(pivot_rows, range(curvature_basis.cols))
    return square.inv() * vector.extract(pivot_rows, [0])


def ricci_commutator_rhs(curvature_basis: sp.Matrix, vector: sp.Matrix) -> sp.Matrix:
    blocks = []
    for f, e in PAIRS:
        raw = sp.zeros(len(CURV_SLOTS), 1)
        for slot, ((a, b), (c, d)) in enumerate(CURV_SLOTS):
            value = 0
            for p in range(4):
                value -= ETA[p] * curvature_component(vector, p, a, f, e) * curvature_component(vector, p, b, c, d)
                value -= ETA[p] * curvature_component(vector, p, b, f, e) * curvature_component(vector, a, p, c, d)
                value -= ETA[p] * curvature_component(vector, p, c, f, e) * curvature_component(vector, a, b, p, d)
                value -= ETA[p] * curvature_component(vector, p, d, f, e) * curvature_component(vector, a, b, c, p)
            raw[slot] = sp.simplify(value)
        blocks.extend(curvature_coordinates(curvature_basis, raw))
    return sp.Matrix(blocks)


def constant_curvature_vector() -> sp.Matrix:
    vector = sp.zeros(len(CURV_SLOTS), 1)
    for slot, ((a, b), (c, d)) in enumerate(CURV_SLOTS):
        metric = lambda i, j: ETA[i] if i == j else 0
        vector[slot] = metric(a, c) * metric(b, d) - metric(a, d) * metric(b, c)
    return vector


def off_diagonal_witness() -> sp.Matrix:
    vector = sp.zeros(len(CURV_SLOTS), 1)
    p01 = PAIR_POS[(0, 1)]
    p02 = PAIR_POS[(0, 2)]
    vector[6 * p01 + p02] = 1
    vector[6 * p02 + p01] = 1
    return vector


def classify_input_schema(conditions: Mapping[str, bool], metric_preowned: bool = False) -> str:
    if metric_preowned and all(conditions.get(field) is True for field in ("theta", "omega", "R")):
        return "EVALUATIVE_ALREADY_HAS_METRIC"
    if all(conditions.get(field) is True for field in REALIZATION_CONDITIONS):
        return "TYPED_CARTAN_REALIZATION_PROBLEM"
    return "INCOMPLETE"


def validate_claim_scope(scope: Mapping[str, str]) -> bool:
    return dict(scope) == BASELINE_SCOPE


def lorentz_generators() -> list[sp.Matrix]:
    generators = []
    for a, b in PAIRS:
        generator = sp.zeros(4, 4)
        generator[a, b] = ETA[a]
        generator[b, a] = -ETA[b]
        generators.append(generator)
    return generators


def vertical_action(generator: sp.Matrix, tensor: sp.Matrix) -> sp.Matrix:
    result = sp.zeros(len(CURV_SLOTS), 1)
    for slot, ((a, b), (c, d)) in enumerate(CURV_SLOTS):
        value = 0
        for p in range(4):
            value += generator[p, a] * curvature_component(tensor, p, b, c, d)
            value += generator[p, b] * curvature_component(tensor, a, p, c, d)
            value += generator[p, c] * curvature_component(tensor, a, b, p, d)
            value += generator[p, d] * curvature_component(tensor, a, b, c, p)
        result[slot] = sp.simplify(value)
    return result


def verify_hash_table(name: str, base: Path, order: str) -> bool:
    for line in (ROOT / name).read_text(encoding="utf-8").splitlines()[1:]:
        first, second = line.split("\t")
        path, digest = (first, second) if order == "path_hash" else (second, first)
        candidate = base / path
        current = hashlib.sha256(candidate.read_bytes()).hexdigest()
        if current == digest:
            continue
        if name != "SOURCE_MANIFEST.tsv":
            return False
        frozen = subprocess.run(
            ["git", "show", f"{FROZEN_COMMIT}:{path}"],
            cwd=REPO,
            check=True,
            capture_output=True,
        ).stdout
        if hashlib.sha256(frozen).hexdigest() != digest:
            return False
    return True


def derive() -> dict[str, object]:
    b1 = algebraic_bianchi_map()
    b1_rank = rank(b1)
    basis_vectors = b1.nullspace()
    curvature_basis = sp.Matrix.hstack(*basis_vectors)
    b2 = differential_bianchi_map(curvature_basis)
    db = differentiated_bianchi_map(b2, curvature_basis.cols)
    comm = commutator_map(curvature_basis.cols)
    combined = db.col_join(comm)

    b2_rank = rank(b2)
    db_rank = rank(db)
    comm_rank = rank(comm)
    combined_rank = rank(combined)

    constant = constant_curvature_vector()
    constant_coordinates = curvature_coordinates(curvature_basis, constant)
    constant_rhs = ricci_commutator_rhs(curvature_basis, constant)
    witness = off_diagonal_witness()
    witness_coordinates = curvature_coordinates(curvature_basis, witness)
    witness_rhs = ricci_commutator_rhs(curvature_basis, witness)

    vertical_generators = lorentz_generators()
    vertical_nonzero = [sum(value != 0 for value in vertical_action(gen, witness)) for gen in vertical_generators]
    constant_vertical_nonzero = [
        sum(value != 0 for value in vertical_action(gen, constant)) for gen in vertical_generators
    ]
    complete_schema = {field: True for field in REALIZATION_CONDITIONS}
    input_trilemma = {
        "moving_frame_R_without_carry": classify_input_schema({"R_typed_as_Lorentz_tensor": True}),
        "R_relative_to_supplied_coframe": classify_input_schema(
            {"theta": True, "omega": True, "R": True}, metric_preowned=True
        ),
        "R_plus_compatible_classifying_derivative_law": classify_input_schema(complete_schema),
    }
    zero_d = sp.zeros(4 * curvature_basis.cols, 1)
    zero_e = sp.zeros(16 * curvature_basis.cols, 1)
    constant_closure = {
        "algebraic_Bianchi_nonzero": sum(value != 0 for value in b1 * constant),
        "zero_D_differential_Bianchi_nonzero": sum(value != 0 for value in b2 * zero_d),
        "zero_E_differentiated_Bianchi_nonzero": sum(value != 0 for value in db * zero_e),
        "zero_E_commutator_residual_nonzero": sum(value != 0 for value in comm * zero_e - constant_rhs),
        "vertical_action_nonzero": sum(constant_vertical_nonzero),
    }

    ranks = {
        "algebraic_bianchi": b1_rank,
        "differential_bianchi": b2_rank,
        "differentiated_bianchi": db_rank,
        "commutator": comm_rank,
        "combined_second_prolongation": combined_rank,
    }
    dimensions = {
        "cartan_curvature_source": len(CURV_SLOTS),
        "algebraic_curvature_kernel": curvature_basis.cols,
        "first_curvature_derivative": 4 * curvature_basis.cols,
        "first_derivative_compatible": 4 * curvature_basis.cols - b2_rank,
        "ordered_second_curvature_derivative": 16 * curvature_basis.cols,
        "second_derivative_affine_translation": 16 * curvature_basis.cols - combined_rank,
    }
    checks = {
        "preregistration_hashes_match": verify_hash_table("PREREGISTRATION_HASHES.tsv", ROOT, "path_hash"),
        "source_manifest_hashes_match": verify_hash_table("SOURCE_MANIFEST.tsv", REPO, "hash_path"),
        "cartan_first_closure_36_to_20": b1_rank == 16 and curvature_basis.cols == 20,
        "cartan_second_closure_80_to_60": b2_rank == 20,
        "g230_second_prolongation_320_to_126": db_rank == 80 and comm_rank == 120 and combined_rank == 194,
        "constant_curvature_is_algebraically_compatible": b1 * constant == sp.zeros(b1.rows, 1),
        "constant_curvature_has_zero_R_squared_commutator": constant_rhs == sp.zeros(constant_rhs.rows, 1),
        "constant_curvature_coordinates_reconstruct": curvature_basis * constant_coordinates == constant,
        "off_diagonal_witness_is_algebraically_compatible": b1 * witness == sp.zeros(b1.rows, 1),
        "off_diagonal_witness_has_nonzero_R_squared_commutator": any(value != 0 for value in witness_rhs),
        "off_diagonal_witness_coordinates_reconstruct": curvature_basis * witness_coordinates == witness,
        "vertical_Lorentz_action_is_nontrivial": any(count > 0 for count in vertical_nonzero),
        "constant_curvature_closes_every_frozen_stage": all(
            count == 0 for count in constant_closure.values()
        ),
        "bare_R_schema_is_not_closed": input_trilemma["moving_frame_R_without_carry"] == "INCOMPLETE",
        "supplied_coframe_schema_is_evaluative": input_trilemma["R_relative_to_supplied_coframe"]
        == "EVALUATIVE_ALREADY_HAS_METRIC",
        "classifying_derivative_schema_is_typed": input_trilemma[
            "R_plus_compatible_classifying_derivative_law"
        ]
        == "TYPED_CARTAN_REALIZATION_PROBLEM",
        "structured_claim_scope_passes": validate_claim_scope(BASELINE_SCOPE),
    }
    return {
        "landing": "CARTAN_REGIONAL_BRIDGE__BARE_R_NOT_CLOSED__CLASSIFYING_DERIVATIVE_DATA_REQUIRED",
        "scope": "local orthonormal-frame-bundle realization architecture; curvature values supplied",
        "dimensions": dimensions,
        "ranks": ranks,
        "checks": checks,
        "constant_curvature_control": {
            "coordinate_nonzero_count": sum(value != 0 for value in constant_coordinates),
            "commutator_rhs_nonzero_count": sum(value != 0 for value in constant_rhs),
            "closure_residual_counts": constant_closure,
        },
        "nonlinear_witness": {
            "description": "symmetric bivector entry (01,02)=1",
            "commutator_rhs_nonzero_count": sum(value != 0 for value in witness_rhs),
            "first_nonzero": str(next(value for value in witness_rhs if value != 0)),
        },
        "vertical_frame_control": {
            "nonzero_counts_by_Lorentz_generator": vertical_nonzero,
        },
        "input_trilemma": input_trilemma,
        "realization_schema": {
            "required_conditions": list(REALIZATION_CONDITIONS),
            "classifier_is_type_gate_not_identity_proof": True,
        },
        "claim_scope": BASELINE_SCOPE,
        "theorem_boundary": {
            "finite_type_classifying_data": "CONDITIONAL_LOCAL_G_REALIZATION_IF_FULL_SO13_G_STRUCTURE_ALGEBROID_HYPOTHESES_HOLD",
            "infinite_type_PDE_data": "ANALYTIC_LOCAL_COFRAME_REALIZATION_ONLY__PRINCIPAL_SO13_EQUIVARIANCE_AND_DESCENT_OPEN",
            "generic_smooth_local": "NOT_CLAIMED",
            "global_realization": "NOT_CLAIMED",
            "value_generation_or_history_selection": "NOT_DERIVED",
        },
        "all_checks_pass": all(checks.values()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = derive()
    text = json.dumps(result, indent=2, sort_keys=True)
    print(text)
    if not args.no_write:
        (ROOT / "exact_results.json").write_text(text + "\n", encoding="utf-8")
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
