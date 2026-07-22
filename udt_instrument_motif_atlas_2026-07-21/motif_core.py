#!/usr/bin/env python3
"""Motif and interaction classifiers for the preregistered UDT instrument lattice."""

from __future__ import annotations

import itertools
import json
import math
import sys
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT = ROOT / "udt_joint_invariant_subspace_atlas_2026-07-21"
sys.path.insert(0, str(PARENT))

from invariant_subspace_core import (  # noqa: E402
    CLUSTER_TOL,
    DIM,
    RANK_TOL,
    UNCERTAINTY_HIGH,
    UNCERTAINTY_LOW,
    ZERO_TOL,
    associative_algebra,
    central_block_decomposition,
    centralizer,
    center_of_commutant,
    krylov_orbit,
    normalize_operators,
    numerical_rank,
    relmax,
    selfadjoint_center,
    subspace_signature,
)


GROUP_BITS = {"R": 1, "H": 2, "D": 4, "RG": 8, "WG": 16}
SCALAR_KEYS = ("R", "H", "D")


def image_basis(projector: np.ndarray) -> tuple[np.ndarray, object]:
    """Return an orthonormal Euclidean basis only as numerical coordinates for an image."""
    value = np.asarray(projector, dtype=float)
    u, _, _ = np.linalg.svd(value, full_matrices=False)
    rank = numerical_rank(value)
    return u[:, : rank.rank], rank


def signature_record(projector: np.ndarray, metric: np.ndarray) -> dict[str, object]:
    basis, rank_result = image_basis(projector)
    negative, positive, zero, eigenvalues = subspace_signature(basis, metric)
    scale = max(1.0, float(np.max(np.abs(eigenvalues))) if eigenvalues.size else 0.0)
    uncertain = rank_result.uncertain or bool(np.any(
        (np.abs(eigenvalues) >= UNCERTAINTY_LOW * scale)
        & (np.abs(eigenvalues) <= UNCERTAINTY_HIGH * scale)
    ))
    margin = float(np.min(np.abs(eigenvalues))) if eigenvalues.size else 0.0
    return {
        "rank": rank_result.rank,
        "signature": f"N{negative}_P{positive}_Z{zero}",
        "negative": negative,
        "positive": positive,
        "zero": zero,
        "metric_margin": margin,
        "uncertain": uncertain,
        "basis": basis,
    }


def restricted_discriminant(operator: np.ndarray, projector: np.ndarray) -> tuple[str, float, bool]:
    info = signature_record(projector, np.eye(DIM))
    if info["rank"] != 2:
        return "NOT_RANK_TWO", math.nan, False
    basis = np.asarray(info["basis"])
    restricted = basis.T @ np.asarray(operator, dtype=float) @ basis
    trace = float(np.trace(restricted))
    determinant = float(np.linalg.det(restricted))
    discriminant = trace * trace - 4.0 * determinant
    scale = max(1.0, abs(trace * trace), abs(4.0 * determinant))
    relative = discriminant / scale
    uncertain = UNCERTAINTY_LOW <= abs(relative) <= UNCERTAINTY_HIGH
    if relative > CLUSTER_TOL:
        label = "REAL_DISTINCT"
    elif relative < -CLUSTER_TOL:
        label = "COMPLEX_CONJUGATE"
    else:
        label = "REPEATED_OR_CLUSTERED"
    return label, relative, uncertain


def motif_label(
    algebra_dimension: int,
    commutant_dimension: int,
    center_dimension: int,
    block_status: str,
    ranks: list[int],
    uncertain: bool,
) -> str:
    if uncertain or block_status.startswith("NUMERIC_UNCERTAIN"):
        return "NUMERIC_UNCERTAIN"
    if algebra_dimension == DIM * DIM:
        return "FULL_IRREDUCIBLE_4"
    if ranks == [1, 1, 1, 1]:
        return "FOUR_LINES"
    if ranks == [1, 1, 2]:
        return "TWO_PLUS_TWO_LINES"
    if ranks == [1, 3]:
        return "LINE_PLUS_THREE"
    if ranks == [2, 2]:
        return "TWO_PLANES"
    if ranks == [4]:
        if algebra_dimension == 1:
            return "SCALAR_4_AMBIGUITY"
        if commutant_dimension > center_dimension:
            return "NONCENTRAL_AMBIGUITY_4"
        return "UNSPLIT_4"
    if ranks:
        return "OTHER_" + "_".join(map(str, ranks))
    return "UNRESOLVED_NO_BLOCKS"


def complementary_rank_two_splits(projectors: list[np.ndarray]) -> list[tuple[np.ndarray, np.ndarray]]:
    ranks = [numerical_rank(projector).rank for projector in projectors]
    candidates: list[tuple[np.ndarray, np.ndarray]] = []
    for mask in range(1, 2 ** len(projectors) - 1):
        if sum(ranks[index] for index in range(len(projectors)) if mask & (1 << index)) != 2:
            continue
        first = sum(
            (projectors[index] for index in range(len(projectors)) if mask & (1 << index)),
            np.zeros((DIM, DIM)),
        )
        second = np.eye(DIM) - first
        pair = [first, second]
        if not any(projector_pair_distance(pair, list(existing)) <= RANK_TOL for existing in candidates):
            candidates.append((first, second))
    return candidates


def projector_pair_distance(first: list[np.ndarray], second: list[np.ndarray]) -> float:
    if len(first) != len(second):
        return math.inf
    direct = max(relmax(first[index], second[index]) for index in range(len(first)))
    if len(first) == 2:
        swapped = max(relmax(first[index], second[1 - index]) for index in range(2))
        return min(direct, swapped)
    return direct


def projector_set_distance(first: list[np.ndarray], second: list[np.ndarray]) -> float:
    if len(first) != len(second):
        return math.inf
    best = math.inf
    for permutation in itertools.permutations(range(len(second))):
        best = min(best, max(relmax(first[index], second[permutation[index]]) for index in range(len(first))))
    return best


def gradient_incidence(pair: tuple[np.ndarray, np.ndarray] | None, gradient: np.ndarray) -> tuple[str, float, bool]:
    value = np.asarray(gradient, dtype=float)
    norm = float(np.linalg.norm(value))
    if norm <= ZERO_TOL:
        return "ZERO_GRADIENT", 0.0, False
    if pair is None:
        return "NO_UNIQUE_SPLIT", 0.0, False
    fractions = [float(np.linalg.norm(projector @ value)) / norm for projector in pair]
    minimum = min(fractions)
    uncertain = UNCERTAINTY_LOW <= minimum <= UNCERTAINTY_HIGH
    if minimum <= RANK_TOL:
        return "WHOLLY_IN_ONE_PLANE", minimum, uncertain
    return "SPLIT_ACROSS_BOTH_PLANES", minimum, uncertain


def classify_motif_family(
    operators: list[np.ndarray],
    gradient: np.ndarray,
    metric: np.ndarray,
    scalar_operators: dict[str, np.ndarray],
    included_keys: tuple[str, ...],
) -> dict[str, object]:
    algebra, algebra_info = associative_algebra(operators)
    commutant, commutant_rank, commutant_residual = centralizer(operators)
    center, center_rank, center_residual = center_of_commutant(commutant)
    selfcenter, selfcenter_rank, selfcenter_residual = selfadjoint_center(center, metric)
    blocks = central_block_decomposition(operators, metric, commutant, center, selfcenter)
    orbit = krylov_orbit(operators, gradient, metric)
    block_records = []
    block_uncertain = False
    for index, projector in enumerate(blocks["projectors"]):
        signature = signature_record(projector, metric)
        discriminants = {}
        discriminant_uncertain = False
        if signature["rank"] == 2:
            for key in SCALAR_KEYS:
                if key in included_keys:
                    label, relative, current_uncertain = restricted_discriminant(scalar_operators[key], projector)
                    discriminants[key] = {"class": label, "relative": relative}
                    discriminant_uncertain |= current_uncertain
        block_uncertain |= bool(signature["uncertain"] or discriminant_uncertain)
        block_records.append({
            "block_index": index,
            "rank": signature["rank"],
            "signature": signature["signature"],
            "negative": signature["negative"],
            "positive": signature["positive"],
            "zero": signature["zero"],
            "metric_margin": signature["metric_margin"],
            "projector": np.asarray(projector, dtype=float),
            "discriminants": discriminants,
            "numeric_uncertain": bool(signature["uncertain"] or discriminant_uncertain),
        })
    ranks = sorted(record["rank"] for record in block_records)
    splits = complementary_rank_two_splits([record["projector"] for record in block_records])
    split_count_matches = len(splits) == int(blocks["rank2_split_count"])
    unique_pair = splits[0] if len(splits) == 1 else None
    incidence, incidence_residual, incidence_uncertain = gradient_incidence(unique_pair, gradient)
    plane_signatures: list[str] = []
    if unique_pair is not None:
        plane_signatures = sorted(signature_record(projector, metric)["signature"] for projector in unique_pair)
    uncertain = bool(
        algebra_info["uncertain"] or commutant_rank.uncertain or center_rank.uncertain
        or selfcenter_rank.uncertain or orbit["uncertain"] or block_uncertain or incidence_uncertain
        or blocks["status"].startswith("NUMERIC_UNCERTAIN") or not split_count_matches
    )
    if algebra_info["dimension"] == DIM * DIM:
        reducibility = "FULL_MATRIX_ALGEBRA_IRREDUCIBLE"
    elif len(splits) == 1:
        reducibility = "UNIQUE_CENTRAL_2PLUS2"
    elif len(splits) > 1:
        reducibility = "MULTIPLE_CENTRAL_2PLUS2"
    elif len(commutant) > len(center):
        reducibility = "PROPER_ALGEBRA_NONCENTRAL_AMBIGUITY"
    else:
        reducibility = "PROPER_ALGEBRA_NO_CENTRAL_2PLUS2"
    motif = motif_label(
        int(algebra_info["dimension"]), len(commutant), len(center), str(blocks["status"]), ranks, uncertain
    )
    return {
        "operator_count": len(operators),
        "nonzero_operator_count": len(normalize_operators(operators)),
        "algebra_dimension": int(algebra_info["dimension"]),
        "algebra_iterations": int(algebra_info["iterations"]),
        "algebra_closure_residual": float(algebra_info["closure_residual"]),
        "commutant_dimension": len(commutant),
        "commutant_residual": float(commutant_residual),
        "center_dimension": len(center),
        "center_residual": float(center_residual),
        "selfadjoint_center_dimension": len(selfcenter),
        "selfadjoint_center_residual": float(selfcenter_residual),
        "primitive_block_ranks": ";".join(map(str, ranks)),
        "primitive_block_signatures": ";".join(sorted(record["signature"] for record in block_records)),
        "primitive_block_count": len(block_records),
        "central_split_count": len(splits),
        "central_block_status": str(blocks["status"]),
        "central_projector_residual": float(blocks["projector_residual"]),
        "central_projector_stability_residual": float(blocks["stability_residual"]),
        "motif": motif,
        "unique_plane_signatures": ";".join(plane_signatures),
        "gradient_incidence": incidence,
        "gradient_incidence_residual": incidence_residual,
        "gradient_orbit_dimension": int(orbit["dimension"]),
        "gradient_orbit_signature": str(orbit["signature"]),
        "reducibility_class": reducibility,
        "numeric_status": "NUMERIC_UNCERTAIN" if uncertain else "NUMERIC_CLASSIFIED",
        "block_records": block_records,
        "projectors": [record["projector"] for record in block_records],
        "unique_pair": unique_pair,
    }


def projectors_covariance_distance(
    original: list[np.ndarray], transformed: list[np.ndarray], jacobian: np.ndarray
) -> float:
    inverse = np.linalg.inv(jacobian)
    expected = [inverse @ projector @ jacobian for projector in original]
    return projector_set_distance(expected, transformed)


def _coarsening_partition(source: list[np.ndarray], destination: list[np.ndarray]) -> bool:
    if not source or not destination or len(destination) > len(source):
        return False
    full_mask = (1 << len(source)) - 1
    candidates: list[list[int]] = []
    for target in destination:
        target_candidates = []
        for mask in range(1, full_mask + 1):
            value = sum(
                (source[index] for index in range(len(source)) if mask & (1 << index)),
                np.zeros((DIM, DIM)),
            )
            if relmax(value, target) <= RANK_TOL:
                target_candidates.append(mask)
        candidates.append(target_candidates)
    for assignment in itertools.product(*candidates):
        if sum(mask.bit_count() for mask in assignment) != len(source):
            continue
        if math.prod(1 for _ in assignment) and all(
            assignment[first] & assignment[second] == 0
            for first in range(len(assignment)) for second in range(first + 1, len(assignment))
        ) and sum(assignment) == full_mask:
            return True
    return False


def projector_relation(source: dict[str, object], destination: dict[str, object]) -> str:
    first = list(source["projectors"])
    second = list(destination["projectors"])
    if source["numeric_status"] != "NUMERIC_CLASSIFIED" or destination["numeric_status"] != "NUMERIC_CLASSIFIED":
        return "NUMERIC_UNCERTAIN"
    if projector_set_distance(first, second) <= RANK_TOL:
        return "SAME_PRIMITIVE_PROJECTORS"
    if _coarsening_partition(first, second):
        return "DESTINATION_COARSENS_SOURCE"
    if _coarsening_partition(second, first):
        return "DESTINATION_REFINES_SOURCE"
    return "NONNESTED_OR_AMBIGUOUS"


def edge_transition(source: dict[str, object], destination: dict[str, object]) -> tuple[str, str]:
    relation = projector_relation(source, destination)
    source_motif = str(source["motif"])
    destination_motif = str(destination["motif"])
    if "UNCERTAIN" in relation or source["numeric_status"] != "NUMERIC_CLASSIFIED" or destination["numeric_status"] != "NUMERIC_CLASSIFIED":
        return "NUMERIC_UNCERTAIN", relation
    if destination_motif == "FULL_IRREDUCIBLE_4" and source_motif != "FULL_IRREDUCIBLE_4":
        return "MIXES_TO_FULL_ALGEBRA", relation
    if source_motif == destination_motif == "FULL_IRREDUCIBLE_4":
        return "FULL_ALGEBRA_REMAINS_FULL", relation
    if relation == "SAME_PRIMITIVE_PROJECTORS":
        return "PRIMITIVE_BLOCKS_PRESERVED", relation
    if relation == "DESTINATION_COARSENS_SOURCE":
        return "PRIMITIVE_BLOCKS_MERGED", relation
    ambiguous = {"SCALAR_4_AMBIGUITY", "NONCENTRAL_AMBIGUITY_4", "UNSPLIT_4"}
    structured = {"FOUR_LINES", "TWO_PLUS_TWO_LINES", "LINE_PLUS_THREE", "TWO_PLANES"}
    if source_motif in ambiguous and destination_motif in structured:
        return "AMBIGUITY_TO_CERTIFIED_MOTIF", relation
    if source_motif in structured and destination_motif in ambiguous:
        return "CERTIFIED_MOTIF_TO_AMBIGUITY", relation
    if source_motif in ambiguous and destination_motif in ambiguous:
        return "AMBIGUITY_CHANGES_OR_REMAINS", relation
    return "OTHER_RETAINED_TRANSITION", relation


def alignment_record(first: dict[str, object], second: dict[str, object]) -> dict[str, object]:
    if first["numeric_status"] != "NUMERIC_CLASSIFIED" or second["numeric_status"] != "NUMERIC_CLASSIFIED":
        return {"alignment_class": "NUMERIC_UNCERTAIN", "split_distance": math.inf,
                "commutator_rank": -1, "commutator_uncertain": True,
                "intersection_dimensions": "", "trace_invariants": ""}
    pair_first = first["unique_pair"]
    pair_second = second["unique_pair"]
    if pair_first is None or pair_second is None:
        return {"alignment_class": "NOT_BOTH_UNIQUE", "split_distance": math.inf,
                "commutator_rank": -1, "commutator_uncertain": False,
                "intersection_dimensions": "", "trace_invariants": ""}
    p, pc = pair_first
    q, qc = pair_second
    distance = projector_pair_distance([p, pc], [q, qc])
    commutator = p @ q - q @ p
    commutator_rank = numerical_rank(commutator)
    intersections = []
    traces = []
    for left in (p, pc):
        left_basis, left_rank = image_basis(left)
        for right in (q, qc):
            right_basis, right_rank = image_basis(right)
            joined = np.column_stack((left_basis, right_basis))
            joined_rank = numerical_rank(joined)
            intersections.append(left_rank.rank + right_rank.rank - joined_rank.rank)
            traces.append(float(np.trace(left @ right)))
    if distance <= RANK_TOL:
        label = "SAME_UNORDERED_SPLIT"
    elif commutator_rank.rank == 0:
        label = "COMMUTING_CROSSING_SPLITS"
    else:
        label = "NONCOMMUTING_CROSSING_SPLITS"
    return {
        "alignment_class": label,
        "split_distance": distance,
        "commutator_rank": commutator_rank.rank,
        "commutator_uncertain": commutator_rank.uncertain,
        "intersection_dimensions": ";".join(map(str, sorted(intersections))),
        "trace_invariants": json.dumps(sorted(traces), separators=(",", ":")),
    }


def public_family_row(result: dict[str, object]) -> dict[str, object]:
    return {key: value for key, value in result.items() if key not in {"block_records", "projectors", "unique_pair"}}

