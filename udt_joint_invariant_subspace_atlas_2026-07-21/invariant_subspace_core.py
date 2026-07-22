#!/usr/bin/env python3
"""Basis-covariant pointwise invariant-subspace tools for the preregistered atlas."""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass

import numpy as np


DIM = 4
PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
RANK_TOL = 1.0e-9
CLUSTER_TOL = 1.0e-8
UNCERTAINTY_LOW = 1.0e-11
UNCERTAINTY_HIGH = 1.0e-7
ZERO_TOL = 1.0e-12

FAMILY_REGISTRY = (
    ("F01_RICCI", ("R",)),
    ("F02_PHI_HESSIAN", ("H",)),
    ("F03_PHI_DYAD", ("D",)),
    ("F04_RICCI_HESSIAN", ("R", "H")),
    ("F05_RICCI_HESSIAN_DYAD", ("R", "H", "D")),
    ("F06_RIEMANN_GENERATORS", ("RG",)),
    ("F07_WEYL_GENERATORS", ("WG",)),
    ("F08_FULL_RIEMANN_JOINT", ("R", "H", "D", "RG")),
    ("F09_FULL_WEYL_JOINT", ("R", "H", "D", "WG")),
)


@dataclass(frozen=True)
class RankResult:
    rank: int
    singular_values: np.ndarray
    uncertain: bool
    smallest_retained: float
    largest_discarded: float


def relmax(actual, expected) -> float:
    a = np.asarray(actual, dtype=float)
    b = np.asarray(expected, dtype=float)
    return float(np.max(np.abs(a - b)) / max(1.0, float(np.max(np.abs(b)))))


def numerical_rank(matrix: np.ndarray, tolerance: float = RANK_TOL) -> RankResult:
    array = np.asarray(matrix, dtype=float)
    if not array.size:
        return RankResult(0, np.array([], dtype=float), False, 0.0, 0.0)
    singular = np.linalg.svd(array, compute_uv=False)
    scale = max(1.0, float(singular[0]) if singular.size else 0.0)
    threshold = tolerance * scale
    rank = int(np.count_nonzero(singular > threshold))
    uncertain = bool(np.any((singular >= UNCERTAINTY_LOW * scale) & (singular <= UNCERTAINTY_HIGH * scale)))
    retained = float(singular[rank - 1]) if rank else 0.0
    discarded = float(singular[rank]) if rank < len(singular) else 0.0
    return RankResult(rank, singular, uncertain, retained, discarded)


def normalized_rows(matrices: list[np.ndarray]) -> np.ndarray:
    rows = []
    for matrix in matrices:
        vector = np.asarray(matrix, dtype=float).reshape(-1)
        norm = float(np.linalg.norm(vector))
        if norm > ZERO_TOL:
            rows.append(vector / norm)
    return np.asarray(rows, dtype=float) if rows else np.zeros((0, DIM * DIM))


def span_basis(matrices: list[np.ndarray]) -> tuple[list[np.ndarray], RankResult]:
    rows = normalized_rows(matrices)
    if not len(rows):
        return [], numerical_rank(rows)
    _, _, vh = np.linalg.svd(rows, full_matrices=False)
    rank_result = numerical_rank(rows)
    return [vh[index].reshape(DIM, DIM) for index in range(rank_result.rank)], rank_result


def normalize_operators(operators: list[np.ndarray]) -> list[np.ndarray]:
    result = []
    for operator in operators:
        value = np.asarray(operator, dtype=float)
        norm = float(np.linalg.norm(value))
        if norm > ZERO_TOL:
            result.append(value / norm)
    return result


def associative_algebra(operators: list[np.ndarray]) -> tuple[list[np.ndarray], dict[str, object]]:
    ops = normalize_operators(operators)
    candidates = [np.eye(DIM), *ops]
    uncertain = False
    previous = -1
    iterations = 0
    while True:
        basis, rank_result = span_basis(candidates)
        uncertain |= rank_result.uncertain
        iterations += 1
        if len(basis) == previous or len(basis) == DIM * DIM:
            break
        previous = len(basis)
        candidates = [*basis, *(left @ right for left in basis for right in ops)]
    maximum_closure = 0.0
    if basis:
        flat = np.asarray([item.reshape(-1) for item in basis])
        for left in basis:
            for right in basis:
                product = (left @ right).reshape(-1)
                projection = flat.T @ (flat @ product)
                maximum_closure = max(maximum_closure, float(np.linalg.norm(product - projection)) / max(1.0, float(np.linalg.norm(product))))
    return basis, {
        "dimension": len(basis),
        "uncertain": uncertain,
        "iterations": iterations,
        "closure_residual": maximum_closure,
    }


def nullspace(matrix: np.ndarray) -> tuple[np.ndarray, RankResult]:
    array = np.asarray(matrix, dtype=float)
    if array.shape[0] == 0:
        return np.eye(array.shape[1]), RankResult(0, np.array([], dtype=float), False, 0.0, 0.0)
    _, _, vh = np.linalg.svd(array, full_matrices=True)
    rank_result = numerical_rank(array)
    return vh[rank_result.rank :].T, rank_result


def centralizer(operators: list[np.ndarray]) -> tuple[list[np.ndarray], RankResult, float]:
    ops = normalize_operators(operators)
    elementary = []
    for row in range(DIM):
        for column in range(DIM):
            value = np.zeros((DIM, DIM))
            value[row, column] = 1.0
            elementary.append(value)
    blocks = []
    for operator in ops:
        blocks.append(np.column_stack([(basis @ operator - operator @ basis).reshape(-1) for basis in elementary]))
    constraint = np.vstack(blocks) if blocks else np.zeros((0, DIM * DIM))
    coefficients, rank_result = nullspace(constraint)
    basis = [coefficients[:, index].reshape(DIM, DIM) for index in range(coefficients.shape[1])]
    residual = max((relmax(item @ operator, operator @ item) for item in basis for operator in ops), default=0.0)
    return basis, rank_result, residual


def center_of_commutant(commutant: list[np.ndarray]) -> tuple[list[np.ndarray], RankResult, float]:
    if not commutant:
        return [], numerical_rank(np.zeros((0, 0))), 0.0
    blocks = []
    for other in commutant:
        blocks.append(np.column_stack([(basis @ other - other @ basis).reshape(-1) for basis in commutant]))
    constraint = np.vstack(blocks)
    coefficients, rank_result = nullspace(constraint)
    center = [sum(coefficients[index, column] * commutant[index] for index in range(len(commutant))) for column in range(coefficients.shape[1])]
    residual = max((relmax(item @ other, other @ item) for item in center for other in commutant), default=0.0)
    return center, rank_result, residual


def selfadjoint_center(center: list[np.ndarray], metric: np.ndarray) -> tuple[list[np.ndarray], RankResult, float]:
    if not center:
        return [], numerical_rank(np.zeros((0, 0))), 0.0
    constraint = np.column_stack([(item.T @ metric - metric @ item).reshape(-1) for item in center])
    coefficients, rank_result = nullspace(constraint)
    result = []
    inverse = np.linalg.inv(metric)
    for column in range(coefficients.shape[1]):
        value = sum(coefficients[index, column] * center[index] for index in range(len(center)))
        value = 0.5 * (value + inverse @ value.T @ metric)
        result.append(value)
    residual = max((relmax(item.T @ metric, metric @ item) for item in result), default=0.0)
    return result, rank_result, residual


def projector_set_distance(first: list[np.ndarray], second: list[np.ndarray]) -> float:
    if len(first) != len(second):
        return float("inf")
    unused = set(range(len(second)))
    worst = 0.0
    for projector in first:
        choices = [(relmax(projector, second[index]), index) for index in unused]
        distance, chosen = min(choices)
        unused.remove(chosen)
        worst = max(worst, distance)
    return worst


def real_primary_projectors(value: np.ndarray) -> tuple[list[np.ndarray], bool]:
    """Return real primary projectors, grouping every complex-conjugate spectral pair."""
    eigenvalues = np.linalg.eigvals(value)
    ordered = sorted(eigenvalues, key=lambda item: (float(item.real), float(item.imag)))
    clusters: list[list[complex]] = []
    for eigenvalue in ordered:
        match = None
        for index, cluster in enumerate(clusters):
            reference = sum(cluster) / len(cluster)
            if abs(eigenvalue - reference) <= CLUSTER_TOL * max(1.0, abs(eigenvalue), abs(reference)):
                match = index
                break
        if match is None:
            clusters.append([complex(eigenvalue)])
        else:
            clusters[match].append(complex(eigenvalue))
    centers = [sum(cluster) / len(cluster) for cluster in clusters]
    # Lagrange product projectors are valid only for semisimple primary clusters.  A repeated
    # eigenvalue with a Jordan block would otherwise collapse to the identity projector and be
    # falsely reported as a resolved four-dimensional primary block.
    complex_value = np.asarray(value, dtype=complex)
    identity = np.eye(DIM, dtype=complex)
    for cluster, center in zip(clusters, centers):
        singular = np.linalg.svd(complex_value - center * identity, compute_uv=False)
        scale = max(1.0, float(singular[0]) if singular.size else 0.0)
        rank = int(np.count_nonzero(singular > RANK_TOL * scale))
        rank_uncertain = bool(np.any(
            (singular >= UNCERTAINTY_LOW * scale) & (singular <= UNCERTAINTY_HIGH * scale)
        ))
        geometric_multiplicity = DIM - rank
        if rank_uncertain or geometric_multiplicity != len(cluster):
            return [], True
    elementary: list[np.ndarray] = []
    for index, center in enumerate(centers):
        projector = identity.copy()
        for other_index, other in enumerate(centers):
            if other_index == index:
                continue
            denominator = center - other
            if abs(denominator) <= CLUSTER_TOL * max(1.0, abs(center), abs(other)):
                return [], True
            projector = projector @ ((complex_value - other * identity) / denominator)
        elementary.append(projector)
    grouped: list[np.ndarray] = []
    used: set[int] = set()
    for index, center in enumerate(centers):
        if index in used:
            continue
        if abs(center.imag) <= CLUSTER_TOL * max(1.0, abs(center)):
            group = [index]
        else:
            candidates = [
                other for other in range(len(centers)) if other not in used and other != index
                and len(clusters[other]) == len(clusters[index])
                and abs(centers[other] - center.conjugate())
                <= CLUSTER_TOL * max(1.0, abs(centers[other]), abs(center))
            ]
            if len(candidates) != 1:
                return [], True
            group = [index, candidates[0]]
        used.update(group)
        projector = sum((elementary[item] for item in group), np.zeros((DIM, DIM), dtype=complex))
        imaginary = float(np.max(np.abs(projector.imag)))
        if imaginary > RANK_TOL:
            return [], True
        grouped.append(projector.real)
    if len(used) != len(centers):
        return [], True
    return grouped, False


def central_block_decomposition(
    operators: list[np.ndarray],
    metric: np.ndarray,
    commutant: list[np.ndarray],
    center: list[np.ndarray],
    selfcenter: list[np.ndarray],
) -> dict[str, object]:
    ops = normalize_operators(operators)
    # A one-dimensional self-adjoint center contains only the scalar identity.  Diagonalizing its
    # floating SVD representative is actively harmful: an arbitrary eigenbasis inside the repeated
    # four-dimensional eigenspace can acquire tiny coordinate-dependent complex parts.
    if len(selfcenter) == 1:
        identity = np.eye(DIM)
        residual = max(
            relmax(identity.T @ metric, metric @ identity),
            max((relmax(identity @ operator, operator @ identity) for operator in ops), default=0.0),
        )
        return {
            "status": "NO_NONTRIVIAL_CENTRAL_BLOCK",
            "block_ranks": "4",
            "rank2_split_count": 0,
            "projector_residual": residual,
            "stability_residual": 0.0,
            "projectors": [identity],
        }
    successful: list[dict[str, object]] = []
    for trial in range(7):
        if not selfcenter:
            break
        coefficients = np.array([
            ((-1.0) ** (trial * (index + 1))) * (index + 1.0) ** (trial + 1)
            for index in range(len(selfcenter))
        ])
        value = sum(coefficients[index] * selfcenter[index] for index in range(len(selfcenter)))
        norm = float(np.linalg.norm(value))
        if norm <= ZERO_TOL:
            continue
        value /= norm
        projectors, spectral_uncertain = real_primary_projectors(value)
        if spectral_uncertain:
            continue
        maximum_residual = 0.0
        ranks = []
        valid = True
        for projector in projectors:
            rank_result = numerical_rank(projector)
            ranks.append(rank_result.rank)
            residual = max(
                relmax(projector @ projector, projector),
                relmax(projector.T @ metric, metric @ projector),
                max((relmax(projector @ operator, operator @ projector) for operator in ops), default=0.0),
                max((relmax(projector @ item, item @ projector) for item in commutant), default=0.0),
            )
            maximum_residual = max(maximum_residual, residual)
            valid &= residual <= RANK_TOL and not rank_result.uncertain
        completeness = relmax(sum(projectors, np.zeros((DIM, DIM))), np.eye(DIM))
        orthogonality = max(
            (relmax(projectors[first] @ projectors[second], np.zeros((DIM, DIM)))
             for first in range(len(projectors)) for second in range(first + 1, len(projectors))),
            default=0.0,
        )
        maximum_residual = max(maximum_residual, completeness, orthogonality)
        valid &= maximum_residual <= RANK_TOL
        if valid and sum(ranks) == DIM:
            successful.append({"projectors": projectors, "ranks": sorted(ranks), "residual": maximum_residual})
    if not successful:
        return {
            "status": "NUMERIC_UNCERTAIN_CENTRAL_BLOCKS",
            "block_ranks": "",
            "rank2_split_count": 0,
            "projector_residual": 0.0,
            "stability_residual": 0.0,
            "projectors": [],
        }
    maximum_blocks = max(len(item["ranks"]) for item in successful)
    candidates = [item for item in successful if len(item["ranks"]) == maximum_blocks]
    reference = candidates[0]
    stability = max((projector_set_distance(reference["projectors"], item["projectors"]) for item in candidates[1:]), default=0.0)
    ranks = reference["ranks"]
    subset_count = 0
    for mask in range(1, 2 ** len(ranks) - 1):
        if sum(ranks[index] for index in range(len(ranks)) if mask & (1 << index)) == 2:
            subset_count += 1
    split_count = subset_count // 2
    if stability > RANK_TOL:
        status = "NUMERIC_UNCERTAIN_CENTRAL_BLOCKS"
    elif split_count == 1:
        status = "UNIQUE_CENTRAL_2PLUS2"
    elif split_count > 1:
        status = "MULTIPLE_CENTRAL_2PLUS2"
    elif ranks == [4]:
        status = "NO_NONTRIVIAL_CENTRAL_BLOCK"
    else:
        status = "CENTRAL_BLOCKS_NO_2PLUS2"
    return {
        "status": status,
        "block_ranks": ";".join(map(str, ranks)),
        "rank2_split_count": split_count,
        "projector_residual": float(reference["residual"]),
        "stability_residual": stability,
        "projectors": reference["projectors"],
    }


def subspace_signature(basis: np.ndarray, metric: np.ndarray) -> tuple[int, int, int, np.ndarray]:
    gram = basis.T @ metric @ basis
    eigenvalues = np.linalg.eigvalsh(0.5 * (gram + gram.T))
    scale = max(1.0, float(np.max(np.abs(eigenvalues))) if eigenvalues.size else 0.0)
    negative = int(np.count_nonzero(eigenvalues < -RANK_TOL * scale))
    positive = int(np.count_nonzero(eigenvalues > RANK_TOL * scale))
    zero = len(eigenvalues) - negative - positive
    return negative, positive, zero, eigenvalues


def krylov_orbit(operators: list[np.ndarray], seed: np.ndarray, metric: np.ndarray) -> dict[str, object]:
    ops = normalize_operators(operators)
    vector = np.asarray(seed, dtype=float)
    if float(np.linalg.norm(vector)) <= ZERO_TOL:
        return {
            "dimension": 0, "signature": "ZERO_SEED", "metric_rank": 0,
            "uncertain": False, "closure_residual": 0.0, "projector_residual": 0.0,
        }
    candidates = [vector]
    previous = -1
    uncertain = False
    basis = np.zeros((DIM, 0))
    while True:
        columns = []
        for item in candidates:
            norm = float(np.linalg.norm(item))
            if norm > ZERO_TOL:
                columns.append(item / norm)
        matrix = np.column_stack(columns)
        u, _, _ = np.linalg.svd(matrix, full_matrices=False)
        rank_result = numerical_rank(matrix)
        uncertain |= rank_result.uncertain
        basis = u[:, : rank_result.rank]
        if rank_result.rank == previous or rank_result.rank == DIM:
            break
        previous = rank_result.rank
        candidates = [basis[:, index] for index in range(basis.shape[1])]
        candidates.extend(operator @ basis[:, index] for operator in ops for index in range(basis.shape[1]))
    closure = max((float(np.linalg.norm(operator @ basis - basis @ (basis.T @ operator @ basis))) for operator in ops), default=0.0)
    negative, positive, zero, gram_eigenvalues = subspace_signature(basis, metric)
    metric_rank = negative + positive
    signature = f"N{negative}_P{positive}_Z{zero}"
    projector_residual = 0.0
    if metric_rank == basis.shape[1]:
        gram = basis.T @ metric @ basis
        projector = basis @ np.linalg.inv(gram) @ basis.T @ metric
        projector_residual = max(
            relmax(projector @ projector, projector),
            relmax(projector.T @ metric, metric @ projector),
            max((relmax(projector @ operator, operator @ projector) for operator in ops), default=0.0),
        )
    scale = max(1.0, float(np.max(np.abs(gram_eigenvalues))) if gram_eigenvalues.size else 0.0)
    uncertain |= bool(np.any((np.abs(gram_eigenvalues) >= UNCERTAINTY_LOW * scale) & (np.abs(gram_eigenvalues) <= UNCERTAINTY_HIGH * scale)))
    return {
        "dimension": basis.shape[1], "signature": signature, "metric_rank": metric_rank,
        "uncertain": uncertain, "closure_residual": closure, "projector_residual": projector_residual,
    }


def classify_family(operators: list[np.ndarray], gradient: np.ndarray, metric: np.ndarray) -> dict[str, object]:
    algebra, algebra_info = associative_algebra(operators)
    commutant, commutant_rank, commutant_residual = centralizer(operators)
    center, center_rank, center_residual = center_of_commutant(commutant)
    selfcenter, selfcenter_rank, selfcenter_residual = selfadjoint_center(center, metric)
    blocks = central_block_decomposition(operators, metric, commutant, center, selfcenter)
    orbit = krylov_orbit(operators, gradient, metric)
    uncertain = bool(
        algebra_info["uncertain"] or commutant_rank.uncertain or center_rank.uncertain
        or selfcenter_rank.uncertain or orbit["uncertain"]
        or blocks["status"].startswith("NUMERIC_UNCERTAIN")
    )
    if algebra_info["dimension"] == DIM * DIM:
        reducibility = "FULL_MATRIX_ALGEBRA_IRREDUCIBLE"
    elif blocks["rank2_split_count"] == 1:
        reducibility = "UNIQUE_CENTRAL_2PLUS2"
    elif blocks["rank2_split_count"] > 1:
        reducibility = "MULTIPLE_CENTRAL_2PLUS2"
    elif len(commutant) > len(center):
        reducibility = "PROPER_ALGEBRA_NONCENTRAL_AMBIGUITY"
    else:
        reducibility = "PROPER_ALGEBRA_NO_CENTRAL_2PLUS2"
    return {
        "operator_count": len(operators),
        "nonzero_operator_count": len(normalize_operators(operators)),
        "algebra_dimension": algebra_info["dimension"],
        "algebra_iterations": algebra_info["iterations"],
        "algebra_closure_residual": algebra_info["closure_residual"],
        "commutant_dimension": len(commutant),
        "commutant_residual": commutant_residual,
        "commutant_center_dimension": len(center),
        "center_residual": center_residual,
        "selfadjoint_center_dimension": len(selfcenter),
        "selfadjoint_center_residual": selfcenter_residual,
        "central_block_ranks": blocks["block_ranks"],
        "central_rank2_split_count": blocks["rank2_split_count"],
        "central_block_status": blocks["status"],
        "central_projector_residual": blocks["projector_residual"],
        "central_projector_stability_residual": blocks["stability_residual"],
        "gradient_orbit_dimension": orbit["dimension"],
        "gradient_orbit_metric_rank": orbit["metric_rank"],
        "gradient_orbit_signature": orbit["signature"],
        "gradient_orbit_closure_residual": orbit["closure_residual"],
        "gradient_orbit_projector_residual": orbit["projector_residual"],
        "reducibility_class": reducibility,
        "numeric_status": "NUMERIC_UNCERTAIN" if uncertain else "NUMERIC_CLASSIFIED",
    }


def weyl_tensor(metric: np.ndarray, riemann: np.ndarray, ricci: np.ndarray, scalar: float) -> np.ndarray:
    result = np.zeros_like(riemann)
    for a, b, c, d in itertools.product(range(DIM), repeat=4):
        result[a, b, c, d] = (
            riemann[a, b, c, d]
            - 0.5 * (
                metric[a, c] * ricci[b, d] - metric[a, d] * ricci[b, c]
                - metric[b, c] * ricci[a, d] + metric[b, d] * ricci[a, c]
            )
            + scalar * (metric[a, c] * metric[b, d] - metric[a, d] * metric[b, c]) / 6.0
        )
    return result


def intrinsic_objects(geometry, phi_first: np.ndarray, phi_second: np.ndarray) -> dict[str, object]:
    metric = geometry.metric
    inverse = geometry.inverse
    dphi = np.asarray(phi_first, dtype=float)
    ddphi = np.asarray(phi_second, dtype=float)
    gradient = inverse @ dphi
    hessian = ddphi.copy()
    for a, b in itertools.product(range(DIM), repeat=2):
        hessian[a, b] -= sum(geometry.christoffel[rho, a, b] * dphi[rho] for rho in range(DIM))
    ricci_operator = inverse @ geometry.ricci
    hessian_operator = inverse @ hessian
    dyad = np.outer(gradient, dphi)
    weyl = weyl_tensor(metric, geometry.riemann_down, geometry.ricci, geometry.scalar_curvature)
    riemann_generators = [geometry.riemann_up[:, :, a, b].copy() for a, b in PAIRS]
    weyl_up_first = np.einsum("ar,rsuv->asuv", inverse, weyl)
    weyl_generators = [weyl_up_first[:, :, a, b].copy() for a, b in PAIRS]
    return {
        "metric": metric,
        "inverse": inverse,
        "gradient": gradient,
        "dphi": dphi,
        "hessian_cov": hessian,
        "R": ricci_operator,
        "H": hessian_operator,
        "D": dyad,
        "RG": riemann_generators,
        "WG": weyl_generators,
        "riemann_down": geometry.riemann_down,
        "weyl_down": weyl,
    }


def family_operators(objects: dict[str, object], keys: tuple[str, ...]) -> list[np.ndarray]:
    result: list[np.ndarray] = []
    for key in keys:
        value = objects[key]
        if isinstance(value, list):
            result.extend(value)
        else:
            result.append(np.asarray(value, dtype=float))
    return result


def bivector_operator(tensor_down: np.ndarray, inverse: np.ndarray) -> np.ndarray:
    raised = np.einsum("ae,bf,efcd->abcd", inverse, inverse, tensor_down)
    return np.asarray([[raised[a, b, c, d] for c, d in PAIRS] for a, b in PAIRS], dtype=float)


def bivector_matrix(vector: np.ndarray) -> np.ndarray:
    result = np.zeros((DIM, DIM))
    for value, (a, b) in zip(vector, PAIRS):
        result[a, b] = value
        result[b, a] = -value
    return result


def plane_projector(bivector: np.ndarray, metric: np.ndarray) -> tuple[np.ndarray | None, str, float]:
    u, singular, _ = np.linalg.svd(bivector)
    rank_result = numerical_rank(bivector)
    if rank_result.rank != 2:
        return None, "NOT_RANK_TWO", 0.0
    basis = u[:, :2]
    negative, positive, zero, eigenvalues = subspace_signature(basis, metric)
    signature = f"N{negative}_P{positive}_Z{zero}"
    if zero:
        return None, signature, float(np.min(np.abs(eigenvalues)))
    gram = basis.T @ metric @ basis
    projector = basis @ np.linalg.inv(gram) @ basis.T @ metric
    return projector, signature, float(np.min(np.abs(eigenvalues)))


def bivector_eigenplanes(
    tensor_name: str, tensor_down: np.ndarray, inverse: np.ndarray, metric: np.ndarray
) -> tuple[dict[str, object], list[dict[str, object]]]:
    operator = bivector_operator(tensor_down, inverse)
    eigenvalues, eigenvectors = np.linalg.eig(operator)
    used = set()
    clusters: list[list[int]] = []
    for start in range(len(eigenvalues)):
        if start in used:
            continue
        cluster = []
        for other in range(len(eigenvalues)):
            if other in used:
                continue
            scale = max(1.0, abs(eigenvalues[start]), abs(eigenvalues[other]))
            if abs(eigenvalues[start] - eigenvalues[other]) <= CLUSTER_TOL * scale:
                cluster.append(other)
        used.update(cluster)
        clusters.append(cluster)
    rows = []
    projectors = []
    repeated = 0
    complex_count = 0
    uncertain = False
    for cluster in clusters:
        if len(cluster) != 1:
            repeated += len(cluster)
            continue
        index = cluster[0]
        value = eigenvalues[index]
        vector = eigenvectors[:, index]
        gap = min(
            (abs(value - eigenvalues[other]) / max(1.0, abs(value), abs(eigenvalues[other])) for other in range(len(eigenvalues)) if other != index),
            default=float("inf"),
        )
        if abs(value.imag) > CLUSTER_TOL or np.max(np.abs(vector.imag)) > CLUSTER_TOL:
            complex_count += 1
            continue
        real = vector.real
        real /= max(float(np.linalg.norm(real)), ZERO_TOL)
        b01, b02, b03, b12, b13, b23 = real
        pfaffian = b01 * b23 - b02 * b13 + b03 * b12
        simplicity = abs(float(pfaffian)) / max(float(np.dot(real, real)), ZERO_TOL)
        if UNCERTAINTY_LOW <= simplicity <= UNCERTAINTY_HIGH or UNCERTAINTY_LOW <= gap <= UNCERTAINTY_HIGH:
            uncertain = True
        if simplicity > RANK_TOL:
            continue
        bivector = bivector_matrix(real)
        projector, signature, metric_margin = plane_projector(bivector, metric)
        if UNCERTAINTY_LOW <= metric_margin <= UNCERTAINTY_HIGH:
            uncertain = True
        row = {
            "tensor": tensor_name,
            "eigenvalue_real": float(value.real),
            "eigenvalue_gap": float(gap),
            "simplicity_residual": simplicity,
            "plane_signature": signature,
            "metric_margin": metric_margin,
            "projector_json": "" if projector is None else "[" + ",".join(f"{item:.17g}" for item in projector.reshape(-1)) + "]",
            "numeric_status": "NUMERIC_UNCERTAIN" if uncertain else "NUMERIC_CLASSIFIED",
        }
        rows.append(row)
        if projector is not None:
            projectors.append(projector)
    complementary_pairs = 0
    for first in range(len(projectors)):
        for second in range(first + 1, len(projectors)):
            if max(relmax(projectors[first] + projectors[second], np.eye(DIM)), relmax(projectors[first] @ projectors[second], np.zeros((DIM, DIM)))) <= RANK_TOL:
                complementary_pairs += 1
    summary = {
        "isolated_real_simple_eigenplanes": len(rows),
        "nondegenerate_simple_eigenplanes": len(projectors),
        "complementary_split_count": complementary_pairs,
        "repeated_eigenvalue_multiplicity": repeated,
        "complex_isolated_count": complex_count,
        "numeric_status": "NUMERIC_UNCERTAIN" if uncertain else "NUMERIC_CLASSIFIED",
    }
    return summary, rows


def set_symmetric_second(array: np.ndarray, mu: int, a: int, b: int, value: float) -> None:
    array[mu, a, b] = value
    array[mu, b, a] = value


def set_symmetric_third(array: np.ndarray, mu: int, a: int, b: int, c: int, value: float) -> None:
    for permutation in set(itertools.permutations((a, b, c))):
        array[(mu, *permutation)] = value


def nonlinear_transforms() -> list[dict[str, object]]:
    first_j = np.eye(DIM)
    first_k = np.zeros((DIM, DIM, DIM))
    first_l = np.zeros((DIM, DIM, DIM, DIM))
    for mu, a, b, value in ((0, 0, 1, .07), (0, 2, 2, .03), (1, 1, 2, -.05), (2, 0, 3, .04), (3, 2, 3, .06)):
        set_symmetric_second(first_k, mu, a, b, value)
    for mu, a, b, c, value in ((0, 0, 1, 2, .02), (1, 0, 0, 3, -.015), (2, 1, 1, 3, .018), (3, 0, 2, 2, -.012)):
        set_symmetric_third(first_l, mu, a, b, c, value)
    second_j = np.array([
        [1.0, 0.0, .12, 0.0], [0.0, 1.0, 0.0, -.18],
        [.07, 0.0, 1.0, 0.0], [0.0, .09, 0.0, 1.0],
    ])
    second_k = np.zeros((DIM, DIM, DIM))
    second_l = np.zeros((DIM, DIM, DIM, DIM))
    for mu, a, b, value in ((0, 0, 2, .05), (0, 3, 3, -.02), (1, 1, 3, -.04), (2, 0, 1, .03), (3, 2, 3, -.045)):
        set_symmetric_second(second_k, mu, a, b, value)
    for mu, a, b, c, value in ((0, 1, 2, 3, -.017), (1, 0, 0, 2, .014), (2, 0, 3, 3, .011), (3, 1, 1, 2, -.019)):
        set_symmetric_third(second_l, mu, a, b, c, value)
    return [
        {"id": "N01_IDENTITY_NONLINEAR", "J": first_j, "K": first_k, "L": first_l},
        {"id": "N02_CROSS_NONLINEAR", "J": second_j, "K": second_k, "L": second_l},
    ]


def nonlinear_transform_jets(
    metric: np.ndarray,
    metric_first: np.ndarray,
    metric_second: np.ndarray,
    phi_value: float,
    phi_first: np.ndarray,
    phi_second: np.ndarray,
    transform: dict[str, object],
    jet_type,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float, np.ndarray, np.ndarray]:
    j = np.asarray(transform["J"], dtype=float)
    k = np.asarray(transform["K"], dtype=float)
    ell = np.asarray(transform["L"], dtype=float)
    jacobian_jets = [[jet_type(j[mu, a], k[mu, a].copy(), ell[mu, a].copy()) for a in range(DIM)] for mu in range(DIM)]
    transformed_metric = np.zeros((DIM, DIM))
    transformed_first = np.zeros((DIM, DIM, DIM))
    transformed_second = np.zeros((DIM, DIM, DIM, DIM))
    for a, b in itertools.product(range(DIM), repeat=2):
        total = jet_type.constant(0.0)
        for mu, nu in itertools.product(range(DIM), repeat=2):
            composed_first = np.einsum("r,rc->c", metric_first[:, mu, nu], j)
            composed_second = np.einsum("rs,rc,sd->cd", metric_second[:, :, mu, nu], j, j) + np.einsum("r,rcd->cd", metric_first[:, mu, nu], k)
            composed = jet_type(metric[mu, nu], composed_first, composed_second)
            total = total + jacobian_jets[mu][a] * jacobian_jets[nu][b] * composed
        transformed_metric[a, b] = total.value
        transformed_first[:, a, b] = total.first
        transformed_second[:, :, a, b] = total.second
    transformed_phi_first = np.einsum("r,ra->a", phi_first, j)
    transformed_phi_second = np.einsum("rs,ra,sb->ab", phi_second, j, j) + np.einsum("r,rab->ab", phi_first, k)
    return transformed_metric, transformed_first, transformed_second, float(phi_value), transformed_phi_first, transformed_phi_second
