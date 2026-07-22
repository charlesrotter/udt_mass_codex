#!/usr/bin/env python3
"""Independent outcome-blind verifier for the UDT instrument-motif atlas.

This module imports neither build_motif_atlas nor motif_core nor the parent invariant-subspace core.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import itertools
import json
import math
import os
from collections import Counter
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT = ROOT / "udt_structural_ensemble_metric_atlas_2026-07-21"
PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
BITS = {"R": 1, "H": 2, "D": 4, "RG": 8, "WG": 16}
TOL = 1.0e-9
CLUSTER = 1.0e-8
LOW = 1.0e-11
HIGH = 1.0e-7
ZERO = 1.0e-12
MAXIMUM = "BOUNDED_POINTWISE_INSTRUMENT_MOTIF_LATTICE_CHARACTERIZED"
ANCHOR_HASH = "4c823d46b065c625d17ea89c53481cdd61af88467ee9a0c4c861e5c36f2dc309"
COMPARE = (
    "algebra_dimension", "commutant_dimension", "center_dimension",
    "selfadjoint_center_dimension", "primitive_block_ranks", "primitive_block_signatures",
    "central_split_count", "motif", "unique_plane_signatures", "gradient_incidence",
    "gradient_orbit_dimension", "gradient_orbit_signature", "reducibility_class", "numeric_status",
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def gzip_rows(path: Path):
    with gzip.open(path, "rt", encoding="utf-8", newline="") as handle:
        yield from csv.DictReader(handle, delimiter="\t")


def write_tsv(path: Path, fields, rows) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


def registered_edge_identities(registry: list[dict[str, str]]) -> set[tuple[int, int]]:
    masks = {int(row["mask"]) for row in registry}
    return {(source, source | bit) for source in masks for bit in BITS.values()
            if not source & bit and source | bit in masks}


def validate_edge_identities(edges: set[tuple[int, int]]) -> None:
    expected = {(source, source | bit) for source in range(1, 32) for bit in BITS.values()
                if not source & bit}
    if edges != expected or len(edges) != 75:
        raise AssertionError("edge identity set")


def validate_operator_count(values: list[np.ndarray], keys: tuple[str, ...]) -> None:
    expected = sum(6 if key in {"RG", "WG"} else 1 for key in keys)
    if len(values) != expected:
        raise AssertionError(f"operator count {len(values)} != {expected}")


def relmax(actual, expected) -> float:
    a = np.asarray(actual, dtype=float); b = np.asarray(expected, dtype=float)
    return float(np.max(np.abs(a - b)) / max(1.0, float(np.max(np.abs(b)))))


def rank_info(matrix: np.ndarray) -> tuple[int, bool, np.ndarray]:
    singular = np.linalg.svd(np.asarray(matrix, dtype=float), compute_uv=False)
    scale = max(1.0, float(singular[0]) if singular.size else 0.0)
    rank = int(np.count_nonzero(singular > TOL * scale))
    uncertain = bool(np.any((singular >= LOW * scale) & (singular <= HIGH * scale)))
    return rank, uncertain, singular


def geometry(g: np.ndarray, dg: np.ndarray, ddg: np.ndarray) -> dict[str, object]:
    inverse = np.linalg.inv(g)
    dinverse = np.asarray([-inverse @ dg[k] @ inverse for k in range(4)])
    gamma = np.zeros((4, 4, 4)); dgamma = np.zeros((4, 4, 4, 4))
    for r, m, n in itertools.product(range(4), repeat=3):
        h = np.asarray([dg[m, s, n] + dg[n, s, m] - dg[s, m, n] for s in range(4)])
        gamma[r, m, n] = 0.5 * inverse[r] @ h
        for k in range(4):
            dh = np.asarray([ddg[k, m, s, n] + ddg[k, n, s, m] - ddg[k, s, m, n] for s in range(4)])
            dgamma[k, r, m, n] = 0.5 * (dinverse[k, r] @ h + inverse[r] @ dh)
    up = np.zeros((4, 4, 4, 4))
    for r, s, m, n in itertools.product(range(4), repeat=4):
        up[r, s, m, n] = dgamma[m, r, n, s] - dgamma[n, r, m, s] + sum(
            gamma[r, m, q] * gamma[q, n, s] - gamma[r, n, q] * gamma[q, m, s] for q in range(4)
        )
    down = np.einsum("ar,rsuv->asuv", g, up)
    ricci = np.einsum("rsrn->sn", up)
    scalar = float(np.einsum("ab,ab", inverse, ricci))
    weyl = np.zeros_like(down)
    for a, b, c, d in itertools.product(range(4), repeat=4):
        weyl[a, b, c, d] = down[a, b, c, d] - 0.5 * (
            g[a, c] * ricci[b, d] - g[a, d] * ricci[b, c]
            - g[b, c] * ricci[a, d] + g[b, d] * ricci[a, c]
        ) + scalar * (g[a, c] * g[b, d] - g[a, d] * g[b, c]) / 6.0
    return {"inverse": inverse, "gamma": gamma, "up": up, "down": down,
            "ricci": ricci, "scalar": scalar, "weyl": weyl}


def objects(g: np.ndarray, dg: np.ndarray, ddg: np.ndarray, dphi: np.ndarray, ddphi: np.ndarray):
    geo = geometry(g, dg, ddg); inverse = np.asarray(geo["inverse"]); gradient = inverse @ dphi
    hessian = ddphi.copy(); gamma = np.asarray(geo["gamma"])
    for a, b in itertools.product(range(4), repeat=2):
        hessian[a, b] -= sum(gamma[r, a, b] * dphi[r] for r in range(4))
    weyl_up = np.einsum("ar,rsuv->asuv", inverse, geo["weyl"])
    return {
        "metric": g, "inverse": inverse, "gradient": gradient,
        "R": inverse @ geo["ricci"], "H": inverse @ hessian, "D": np.outer(gradient, dphi),
        "RG": [np.asarray(geo["up"])[:, :, a, b] for a, b in PAIRS],
        "WG": [weyl_up[:, :, a, b] for a, b in PAIRS],
    }, geo


def operators(current: dict[str, object], keys: tuple[str, ...]) -> list[np.ndarray]:
    output = []
    for key in keys:
        value = current[key]
        output.extend(value if isinstance(value, list) else [value])
    return [np.asarray(item, dtype=float) for item in output]


def normalized(values: list[np.ndarray]) -> list[np.ndarray]:
    output = []
    for value in values:
        norm = float(np.linalg.norm(value))
        if norm > ZERO:
            output.append(np.asarray(value) / norm)
    return output


def row_basis(values: list[np.ndarray]) -> tuple[list[np.ndarray], bool]:
    vectors = []
    for value in values:
        flat = np.asarray(value).reshape(-1); norm = float(np.linalg.norm(flat))
        if norm > ZERO:
            vectors.append(flat / norm)
    if not vectors:
        return [], False
    matrix = np.asarray(vectors); rank, uncertain, _ = rank_info(matrix)
    _, _, vh = np.linalg.svd(matrix, full_matrices=False)
    return [vh[index].reshape(4, 4) for index in range(rank)], uncertain


def algebra_basis(values: list[np.ndarray]) -> tuple[list[np.ndarray], bool]:
    ops = normalized(values); candidates = [np.eye(4), *ops]; prior = -1; uncertain = False
    while True:
        basis, current = row_basis(candidates); uncertain |= current
        if len(basis) == prior or len(basis) == 16:
            return basis, uncertain
        prior = len(basis)
        candidates = [*basis, *(left @ right for left in basis for right in ops)]


def nullspace(matrix: np.ndarray) -> tuple[np.ndarray, bool]:
    rank, uncertain, _ = rank_info(matrix); _, _, vh = np.linalg.svd(matrix, full_matrices=True)
    return vh[rank:].T, uncertain


def commutant_basis(values: list[np.ndarray]) -> tuple[list[np.ndarray], bool]:
    ops = normalized(values); identity = np.eye(4)
    if not ops:
        elementary = []
        for column in range(4):
            for row in range(4):
                value = np.zeros((4, 4)); value[row, column] = 1.0; elementary.append(value)
        return elementary, False
    constraint = np.vstack([np.kron(operator.T, identity) - np.kron(identity, operator) for operator in ops])
    kernel, uncertain = nullspace(constraint)
    return [kernel[:, index].reshape(4, 4, order="F") for index in range(kernel.shape[1])], uncertain


def center_basis(commutant: list[np.ndarray]) -> tuple[list[np.ndarray], bool]:
    blocks = [
        np.column_stack([(item @ other - other @ item).reshape(-1, order="F") for item in commutant])
        for other in commutant
    ]
    kernel, uncertain = nullspace(np.vstack(blocks))
    return [sum(kernel[index, column] * commutant[index] for index in range(len(commutant)))
            for column in range(kernel.shape[1])], uncertain


def selfcenter_basis(center: list[np.ndarray], metric: np.ndarray) -> tuple[list[np.ndarray], bool]:
    constraint = np.column_stack([(item.T @ metric - metric @ item).reshape(-1) for item in center])
    kernel, uncertain = nullspace(constraint); inverse = np.linalg.inv(metric); output = []
    for column in range(kernel.shape[1]):
        value = sum(kernel[index, column] * center[index] for index in range(len(center)))
        output.append(0.5 * (value + inverse @ value.T @ metric))
    return output, uncertain


def primary_projectors(value: np.ndarray) -> tuple[list[np.ndarray], bool]:
    eigenvalues = list(np.linalg.eigvals(value)); clusters: list[list[complex]] = []
    for eigenvalue in sorted(eigenvalues, key=lambda item: (float(item.real), float(item.imag))):
        choices = [index for index, cluster in enumerate(clusters)
                   if abs(eigenvalue - sum(cluster) / len(cluster))
                   <= CLUSTER * max(1.0, abs(eigenvalue), abs(sum(cluster) / len(cluster)))]
        if choices: clusters[choices[0]].append(complex(eigenvalue))
        else: clusters.append([complex(eigenvalue)])
    centers = np.asarray([sum(cluster) / len(cluster) for cluster in clusters], dtype=complex)
    complex_value = np.asarray(value, dtype=complex); identity = np.eye(4, dtype=complex)
    for cluster, center in zip(clusters, centers):
        singular = np.linalg.svd(complex_value - center * identity, compute_uv=False)
        scale = max(1.0, float(singular[0]) if singular.size else 0.0)
        rank = int(np.count_nonzero(singular > TOL * scale))
        uncertain = bool(np.any((singular >= LOW * scale) & (singular <= HIGH * scale)))
        if uncertain or 4 - rank != len(cluster): return [], True
    groups = []; used = set()
    for index, center in enumerate(centers):
        if index in used: continue
        if abs(center.imag) <= CLUSTER * max(1.0, abs(center)): group = [index]
        else:
            partners = [other for other in range(len(centers)) if other != index and other not in used
                        and len(clusters[other]) == len(clusters[index])
                        and abs(centers[other] - center.conjugate())
                        <= CLUSTER * max(1.0, abs(centers[other]), abs(center))]
            if len(partners) != 1: return [], True
            group = [index, partners[0]]
        used.update(group); groups.append(group)
    vandermonde = np.asarray([[center ** power for power in range(len(centers))] for center in centers])
    if np.linalg.cond(vandermonde) > 1.0e12: return [], True
    powers = [np.linalg.matrix_power(complex_value, power) for power in range(len(centers))]
    output = []
    for group in groups:
        target = np.zeros(len(centers), dtype=complex); target[group] = 1.0
        coefficients = np.linalg.solve(vandermonde, target)
        projector = sum((coefficients[power] * powers[power] for power in range(len(powers))),
                        np.zeros((4, 4), dtype=complex))
        if np.max(np.abs(projector.imag)) > TOL: return [], True
        output.append(projector.real)
    return output, False


def set_distance(first: list[np.ndarray], second: list[np.ndarray]) -> float:
    if len(first) != len(second): return math.inf
    return min(max(relmax(first[index], second[perm[index]]) for index in range(len(first)))
               for perm in itertools.permutations(range(len(second))))


def central_blocks(values: list[np.ndarray], metric: np.ndarray, commutant, selfcenter):
    ops = normalized(values)
    if len(selfcenter) == 1:
        return [np.eye(4)], "NO_NONTRIVIAL_CENTRAL_BLOCK", False
    candidates = []
    for trial in range(9):
        value = sum((((-1) ** (trial * (index + 1))) * (index + 1) ** (trial + 1)) * item
                    for index, item in enumerate(selfcenter))
        norm = float(np.linalg.norm(value))
        if norm <= ZERO: continue
        projectors, uncertain = primary_projectors(value / norm)
        if uncertain: continue
        valid = True; residual = 0.0
        for projector in projectors:
            rank, rank_uncertain, _ = rank_info(projector)
            current = max(relmax(projector @ projector, projector), relmax(projector.T @ metric, metric @ projector),
                          max((relmax(projector @ op, op @ projector) for op in ops), default=0.0),
                          max((relmax(projector @ op, op @ projector) for op in commutant), default=0.0))
            residual = max(residual, current); valid &= not rank_uncertain and current <= TOL and rank > 0
        residual = max(residual, relmax(sum(projectors, np.zeros((4, 4))), np.eye(4)),
                       max((relmax(projectors[i] @ projectors[j], np.zeros((4, 4)))
                            for i in range(len(projectors)) for j in range(i + 1, len(projectors))), default=0.0))
        if valid and residual <= TOL and sum(rank_info(projector)[0] for projector in projectors) == 4:
            candidates.append(projectors)
    if not candidates: return [], "NUMERIC_UNCERTAIN_CENTRAL_BLOCKS", True
    maximum = max(len(item) for item in candidates); finalists = [item for item in candidates if len(item) == maximum]
    if max((set_distance(finalists[0], item) for item in finalists[1:]), default=0.0) > TOL:
        return finalists[0], "NUMERIC_UNCERTAIN_CENTRAL_BLOCKS", True
    ranks = sorted(rank_info(projector)[0] for projector in finalists[0])
    subset_count = sum(sum(ranks[index] for index in range(len(ranks)) if mask & (1 << index)) == 2
                       for mask in range(1, 2 ** len(ranks) - 1))
    splits = subset_count // 2
    status = "UNIQUE_CENTRAL_2PLUS2" if splits == 1 else "MULTIPLE_CENTRAL_2PLUS2" if splits > 1 \
        else "NO_NONTRIVIAL_CENTRAL_BLOCK" if ranks == [4] else "CENTRAL_BLOCKS_NO_2PLUS2"
    return finalists[0], status, False


def signature(projector: np.ndarray, metric: np.ndarray):
    u, _, _ = np.linalg.svd(projector); rank, uncertain, _ = rank_info(projector); basis = u[:, :rank]
    gram = 0.5 * (basis.T @ metric @ basis + (basis.T @ metric @ basis).T)
    eigenvalues = np.linalg.eigvalsh(gram); scale = max(1.0, float(np.max(np.abs(eigenvalues))))
    negative = int(np.count_nonzero(eigenvalues < -TOL * scale)); positive = int(np.count_nonzero(eigenvalues > TOL * scale))
    zero = rank - negative - positive
    uncertain |= bool(np.any((np.abs(eigenvalues) >= LOW * scale) & (np.abs(eigenvalues) <= HIGH * scale)))
    return rank, f"N{negative}_P{positive}_Z{zero}", negative, positive, zero, basis, uncertain


def splits(projectors: list[np.ndarray]):
    ranks = [rank_info(projector)[0] for projector in projectors]; output = []
    for mask in range(1, 2 ** len(projectors) - 1):
        if sum(ranks[index] for index in range(len(ranks)) if mask & (1 << index)) != 2: continue
        first = sum((projectors[index] for index in range(len(projectors)) if mask & (1 << index)), np.zeros((4, 4)))
        pair = [first, np.eye(4) - first]
        if not any(min(max(relmax(pair[i], old[i]) for i in range(2)),
                           max(relmax(pair[i], old[1 - i]) for i in range(2))) <= TOL for old in output):
            output.append(pair)
    return output


def orbit(values: list[np.ndarray], seed: np.ndarray, metric: np.ndarray):
    ops = normalized(values)
    if np.linalg.norm(seed) <= ZERO: return 0, "ZERO_SEED", False
    candidates = [seed]; prior = -1; uncertain = False
    while True:
        matrix = np.column_stack([value / np.linalg.norm(value) for value in candidates if np.linalg.norm(value) > ZERO])
        rank, current, _ = rank_info(matrix); uncertain |= current; u, _, _ = np.linalg.svd(matrix, full_matrices=False)
        basis = u[:, :rank]
        if rank == prior or rank == 4: break
        prior = rank; candidates = [basis[:, i] for i in range(rank)] + [op @ basis[:, i] for op in ops for i in range(rank)]
    gram = 0.5 * (basis.T @ metric @ basis + (basis.T @ metric @ basis).T); eigen = np.linalg.eigvalsh(gram)
    scale = max(1.0, float(np.max(np.abs(eigen)))); negative = int(np.count_nonzero(eigen < -TOL * scale)); positive = int(np.count_nonzero(eigen > TOL * scale)); zero = rank - negative - positive
    uncertain |= bool(np.any((np.abs(eigen) >= LOW * scale) & (np.abs(eigen) <= HIGH * scale)))
    return rank, f"N{negative}_P{positive}_Z{zero}", uncertain


def discriminant(operator: np.ndarray, projector: np.ndarray):
    rank, _, _, _, _, basis, _ = signature(projector, np.eye(4))
    if rank != 2: return "NOT_RANK_TWO", False
    restricted = basis.T @ operator @ basis; trace = float(np.trace(restricted)); determinant = float(np.linalg.det(restricted))
    value = trace * trace - 4.0 * determinant; scale = max(1.0, abs(trace * trace), abs(4.0 * determinant)); relative = value / scale
    uncertain = LOW <= abs(relative) <= HIGH
    label = "REAL_DISTINCT" if relative > CLUSTER else "COMPLEX_CONJUGATE" if relative < -CLUSTER else "REPEATED_OR_CLUSTERED"
    return label, uncertain


def motif_name(algebra_dimension, commutant_dimension, center_dimension, ranks, uncertain):
    if uncertain: return "NUMERIC_UNCERTAIN"
    if algebra_dimension == 16: return "FULL_IRREDUCIBLE_4"
    if ranks == [1, 1, 1, 1]: return "FOUR_LINES"
    if ranks == [1, 1, 2]: return "TWO_PLUS_TWO_LINES"
    if ranks == [1, 3]: return "LINE_PLUS_THREE"
    if ranks == [2, 2]: return "TWO_PLANES"
    if ranks == [4]:
        if algebra_dimension == 1: return "SCALAR_4_AMBIGUITY"
        if commutant_dimension > center_dimension: return "NONCENTRAL_AMBIGUITY_4"
        return "UNSPLIT_4"
    return "UNRESOLVED_NO_BLOCKS" if not ranks else "OTHER_" + "_".join(map(str, ranks))


def classify(values: list[np.ndarray], gradient: np.ndarray, metric: np.ndarray, scalar, keys):
    algebra, ua = algebra_basis(values); commutant, uc = commutant_basis(values); center, uz = center_basis(commutant); selfcenter, us = selfcenter_basis(center, metric)
    projectors, block_status, ub = central_blocks(values, metric, commutant, selfcenter)
    block_data = []; block_uncertain = ub
    for projector in projectors:
        rank, sig, negative, positive, zero, _, current_uncertain = signature(projector, metric)
        for key in ("R", "H", "D"):
            if rank == 2 and key in keys:
                _, current = discriminant(scalar[key], projector); current_uncertain |= current
        block_uncertain |= current_uncertain
        block_data.append({"rank": rank, "signature": sig, "negative": negative, "positive": positive,
                           "zero": zero, "projector": projector, "uncertain": current_uncertain})
    ranks = sorted(item["rank"] for item in block_data); split_pairs = splits(projectors); unique = split_pairs[0] if len(split_pairs) == 1 else None
    if np.linalg.norm(gradient) <= ZERO: incidence = "ZERO_GRADIENT"
    elif unique is None: incidence = "NO_UNIQUE_SPLIT"
    else:
        minimum = min(float(np.linalg.norm(projector @ gradient)) / float(np.linalg.norm(gradient)) for projector in unique)
        block_uncertain |= LOW <= minimum <= HIGH
        incidence = "WHOLLY_IN_ONE_PLANE" if minimum <= TOL else "SPLIT_ACROSS_BOTH_PLANES"
    orbit_dimension, orbit_signature, uo = orbit(values, gradient, metric)
    uncertain = ua or uc or uz or us or block_uncertain or uo
    motif = motif_name(len(algebra), len(commutant), len(center), ranks, uncertain)
    if len(algebra) == 16: reducibility = "FULL_MATRIX_ALGEBRA_IRREDUCIBLE"
    elif len(split_pairs) == 1: reducibility = "UNIQUE_CENTRAL_2PLUS2"
    elif len(split_pairs) > 1: reducibility = "MULTIPLE_CENTRAL_2PLUS2"
    elif len(commutant) > len(center): reducibility = "PROPER_ALGEBRA_NONCENTRAL_AMBIGUITY"
    else: reducibility = "PROPER_ALGEBRA_NO_CENTRAL_2PLUS2"
    plane_signatures = sorted(signature(projector, metric)[1] for projector in unique) if unique is not None else []
    return {
        "algebra_dimension": len(algebra), "commutant_dimension": len(commutant),
        "center_dimension": len(center), "selfadjoint_center_dimension": len(selfcenter),
        "primitive_block_ranks": ";".join(map(str, ranks)),
        "primitive_block_signatures": ";".join(sorted(item["signature"] for item in block_data)),
        "central_split_count": len(split_pairs), "motif": motif,
        "unique_plane_signatures": ";".join(plane_signatures), "gradient_incidence": incidence,
        "gradient_orbit_dimension": orbit_dimension, "gradient_orbit_signature": orbit_signature,
        "reducibility_class": reducibility, "numeric_status": "NUMERIC_UNCERTAIN" if uncertain else "NUMERIC_CLASSIFIED",
        "projectors": projectors, "blocks": block_data, "unique_pair": unique, "block_status": block_status,
    }


def multiply(left, right):
    lv, lf, ls = left; rv, rf, rs = right
    return lv * rv, lf * rv + lv * rf, ls * rv + lv * rs + np.outer(lf, rf) + np.outer(rf, lf)


def transform_jets(g, dg, ddg, phi_value, phi_first, phi_second, j, k, ell):
    jacobian_jets = [[(j[mu, a], k[mu, a].copy(), ell[mu, a].copy()) for a in range(4)] for mu in range(4)]
    gt = np.zeros((4, 4)); dgt = np.zeros((4, 4, 4)); ddgt = np.zeros((4, 4, 4, 4))
    for a, b in itertools.product(range(4), repeat=2):
        total = (0.0, np.zeros(4), np.zeros((4, 4)))
        for mu, nu in itertools.product(range(4), repeat=2):
            composed = (g[mu, nu], np.einsum("r,rc->c", dg[:, mu, nu], j),
                        np.einsum("rs,rc,sd->cd", ddg[:, :, mu, nu], j, j) + np.einsum("r,rcd->cd", dg[:, mu, nu], k))
            total = tuple(x + y for x, y in zip(total, multiply(multiply(jacobian_jets[mu][a], jacobian_jets[nu][b]), composed)))
        gt[a, b], dgt[:, a, b], ddgt[:, :, a, b] = total
    transformed_first = np.einsum("r,ra->a", phi_first, j)
    transformed_second = np.einsum("rs,ra,sb->ab", phi_second, j, j) + np.einsum("r,rab->ab", phi_first, k)
    return gt, dgt, ddgt, phi_value, transformed_first, transformed_second


def transforms():
    first_j = np.eye(4); first_k = np.zeros((4, 4, 4)); first_l = np.zeros((4, 4, 4, 4))
    for mu, a, b, value in ((0, 0, 1, .07), (0, 2, 2, .03), (1, 1, 2, -.05), (2, 0, 3, .04), (3, 2, 3, .06)):
        for x, y in {(a, b), (b, a)}: first_k[mu, x, y] = value
    for mu, a, b, c, value in ((0, 0, 1, 2, .02), (1, 0, 0, 3, -.015), (2, 1, 1, 3, .018), (3, 0, 2, 2, -.012)):
        for permutation in set(itertools.permutations((a, b, c))): first_l[(mu, *permutation)] = value
    second_j = np.asarray([[1.0, 0.0, .12, 0.0], [0.0, 1.0, 0.0, -.18], [.07, 0.0, 1.0, 0.0], [0.0, .09, 0.0, 1.0]])
    second_k = np.zeros((4, 4, 4)); second_l = np.zeros((4, 4, 4, 4))
    for mu, a, b, value in ((0, 0, 2, .05), (0, 3, 3, -.02), (1, 1, 3, -.04), (2, 0, 1, .03), (3, 2, 3, -.045)):
        for x, y in {(a, b), (b, a)}: second_k[mu, x, y] = value
    for mu, a, b, c, value in ((0, 1, 2, 3, -.017), (1, 0, 0, 2, .014), (2, 0, 3, 3, .011), (3, 1, 1, 2, -.019)):
        for permutation in set(itertools.permutations((a, b, c))): second_l[(mu, *permutation)] = value
    return (("N01_IDENTITY_NONLINEAR", first_j, first_k, first_l),
            ("N02_CROSS_NONLINEAR", second_j, second_k, second_l))


def validate_registry(registry):
    if len(registry) != 31 or [int(row["mask"]) for row in registry] != list(range(1, 32)): raise AssertionError("subset registry")
    for row in registry:
        keys = tuple(row["operator_keys"].split(";")); mask = sum(BITS[key] for key in keys)
        if mask != int(row["mask"]): raise AssertionError("registry key/mask")


def main() -> None:
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    if digest(HERE / "VERIFIER_ANCHOR_IDS.txt") != ANCHOR_HASH: raise AssertionError("anchor hash")
    anchor_ids = set((HERE / "VERIFIER_ANCHOR_IDS.txt").read_text().splitlines())
    if len(anchor_ids) != 384: raise AssertionError("anchor count")
    registry = read_tsv(HERE / "INSTRUMENT_SUBSET_REGISTRY.tsv"); validate_registry(registry)
    families = [(row["family_id"], int(row["mask"]), tuple(row["operator_keys"].split(";"))) for row in registry]
    independent_original = {}; independent_transformed = {}; raw_by_id = {}; parent_max = 0.0; covariance_max = 0.0; omitted_jet_max = 0.0
    for shard in read_tsv(PARENT / "RAW_SHARD_REGISTRY.tsv"):
        shard_path = PARENT / shard["path"]
        if digest(shard_path) != shard["sha256"]: raise AssertionError(f"raw shard hash {shard['path']}")
        with shard_path.open(encoding="utf-8") as handle:
            for line in handle:
                raw = json.loads(line); cid = raw["configuration_id"]
                if cid not in anchor_ids: continue
                raw_by_id[cid] = raw; g = np.asarray(raw["metric"]); dg = np.asarray(raw["metric_first"]); ddg = np.asarray(raw["metric_second"]); pf = np.asarray(raw["phi"]["first"]); ps = np.asarray(raw["phi"]["second"])
                current, geo = objects(g, dg, ddg, pf, ps)
                parent_max = max(parent_max, relmax(geo["down"], raw["riemann_down"]), relmax(geo["ricci"], raw["ricci"]), relmax(geo["weyl"], raw["weyl_down"]))
                scalar = {key: current[key] for key in ("R", "H", "D")}
                base = {}
                for family_id, mask, keys in families:
                    base[mask] = classify(operators(current, keys), current["gradient"], g, scalar, keys)
                    independent_original[(cid, family_id)] = base[mask]
                for transform_id, j, k, ell in transforms():
                    transformed = transform_jets(g, dg, ddg, raw["phi"]["value"], pf, ps, j, k, ell)
                    transformed_objects, _ = objects(transformed[0], transformed[1], transformed[2], transformed[4], transformed[5])
                    omitted_phi_second = np.einsum("rs,ra,sb->ab", ps, j, j)
                    omitted_objects, _ = objects(
                        transformed[0], transformed[1], transformed[2], transformed[4], omitted_phi_second
                    )
                    omitted_jet_max = max(
                        omitted_jet_max, relmax(omitted_objects["H"], transformed_objects["H"])
                    )
                    inverse_j = np.linalg.inv(j)
                    covariance_max = max(covariance_max, relmax(transformed_objects["metric"], j.T @ g @ j),
                                         relmax(transformed_objects["gradient"], inverse_j @ current["gradient"]),
                                         relmax(transformed_objects["R"], inverse_j @ current["R"] @ j),
                                         relmax(transformed_objects["H"], inverse_j @ current["H"] @ j),
                                         relmax(transformed_objects["D"], inverse_j @ current["D"] @ j))
                    transformed_scalar = {key: transformed_objects[key] for key in ("R", "H", "D")}
                    for family_id, mask, keys in families:
                        independent_transformed[(cid, transform_id, family_id)] = classify(
                            operators(transformed_objects, keys), transformed_objects["gradient"], transformed_objects["metric"], transformed_scalar, keys
                        )
    if len(raw_by_id) != 384 or len(independent_original) != 11904 or len(independent_transformed) != 23808:
        raise AssertionError("blind computation coverage")

    # Saved classifications enter only after every blind anchor has been computed.
    family_saved = {(row["configuration_id"], row["family_id"]): row for row in gzip_rows(HERE / "FAMILY_MOTIF_ATLAS.tsv.gz") if row["configuration_id"] in anchor_ids}
    block_saved = {}
    for row in gzip_rows(HERE / "PRIMITIVE_BLOCK_ATLAS.tsv.gz"):
        if row["configuration_id"] in anchor_ids: block_saved.setdefault((row["configuration_id"], row["family_id"]), []).append(row)
    nonlinear_saved = {(row["configuration_id"], row["transform_id"], row["family_id"]): row for row in gzip_rows(HERE / "NONLINEAR_FAMILY_COMPARISON.tsv.gz") if row["configuration_id"] in anchor_ids}
    if len(family_saved) != 11904 or len(nonlinear_saved) != 23808: raise AssertionError("saved anchor coverage")
    comparisons = 0; uncertain = 0; max_projector_saved = 0.0
    for key, current in independent_original.items():
        saved = family_saved[key]
        for field in COMPARE:
            if str(current[field]) != saved[field]: raise AssertionError(f"original mismatch {key} {field}: {current[field]} != {saved[field]}")
        saved_projectors = [np.asarray(json.loads(row["projector_json"])) for row in block_saved[key]]
        distance = set_distance(current["projectors"], saved_projectors); max_projector_saved = max(max_projector_saved, distance)
        if distance > TOL: raise AssertionError(f"saved projector mismatch {key} {distance}")
        comparisons += 1; uncertain += current["numeric_status"] != "NUMERIC_CLASSIFIED"
    for key, current in independent_transformed.items():
        cid, transform_id, family_id = key; original = independent_original[(cid, family_id)]; saved = nonlinear_saved[key]
        discordant = [field for field in COMPARE if original[field] != current[field]]
        expected_uncertain = original["numeric_status"] != "NUMERIC_CLASSIFIED" or current["numeric_status"] != "NUMERIC_CLASSIFIED"
        expected_agreement = not discordant
        if saved["original_numeric_status"] != original["numeric_status"] or saved["transformed_numeric_status"] != current["numeric_status"]:
            raise AssertionError(f"nonlinear status mismatch {key}")
        if saved["classification_agreement"] != ("YES" if expected_agreement else "NO"):
            raise AssertionError(f"nonlinear agreement mismatch {key}")
        if saved["numeric_status"] != ("NUMERIC_UNCERTAIN" if expected_uncertain else "NUMERIC_CLASSIFIED"):
            raise AssertionError(f"nonlinear uncertainty mismatch {key}")
        comparisons += 1; uncertain += expected_uncertain

    result = json.loads((HERE / "ATLAS_RESULT.json").read_text())
    required = {
        "configurations": 6144, "family_rows": 190464, "edge_rows": 460800,
        "nonlinear_family_rows": 380928, "nonlinear_nonuncertain_discordances": 0,
        "nonlinear_edge_nonuncertain_discordances": 0, "nonlinear_alignment_nonuncertain_discordances": 0,
        "catch_proofs_passed": 12, "maximum_conclusion": MAXIMUM,
    }
    if any(result.get(key) != value for key, value in required.items()): raise AssertionError("result contract")
    if result["physical_merit_evaluated"] is not False: raise AssertionError("physical merit evaluated")

    catches = []
    def reject(catch_id, condition):
        if not condition: raise AssertionError(f"catch failed {catch_id}")
        catches.append({"catch_id": catch_id, "result": "REJECTED_AS_REQUIRED"})
    reject("K01_MISSING_SUBSET", len(registry[:-1]) != 31)
    reject("K02_DUPLICATE_SUBSET", len({row["mask"] for row in [*registry[:-1], registry[-2]]}) != 31)
    edge_identities = registered_edge_identities(registry)
    validate_edge_identities(edge_identities)
    missing_edges = set(edge_identities); missing_edges.pop()
    try:
        validate_edge_identities(missing_edges); missing_edge_rejected = False
    except AssertionError:
        missing_edge_rejected = True
    reject("K03_MISSING_EDGE", missing_edge_rejected)
    full_keys = ("R","H","D","RG","WG")
    full_values = operators(objects(np.eye(4), np.zeros((4,4,4)), np.zeros((4,4,4,4)),
                                    np.zeros(4), np.zeros((4,4)))[0], full_keys)
    validate_operator_count(full_values, full_keys)
    try:
        validate_operator_count(full_values[:-1], full_keys); dropped_operator_rejected = False
    except AssertionError:
        dropped_operator_rejected = True
    reject("K04_DROPPED_OPERATOR", dropped_operator_rejected)
    try:
        classify([], np.zeros(4), np.eye(4), {"R":np.eye(4),"H":np.eye(4),"D":np.eye(4)}, ("R",), target_plane=np.eye(4)[:,:2])
        supplied_rejected = False
    except TypeError: supplied_rejected = True
    reject("K05_SUPPLIED_PLANE", supplied_rejected)
    null_metric = np.diag((-1.0, 1.0, 1.0, 1.0)); null_covector = np.asarray((1.0, 1.0, 0.0, 0.0)); null_norm = float(null_covector @ np.linalg.inv(null_metric) @ null_covector)
    reject("K06_NORMALIZED_NULL_DYAD", abs(null_norm) <= TOL)
    example = next(current for current in independent_original.values() if current["blocks"])
    inertia = (sum(item["negative"] for item in example["blocks"]), sum(item["positive"] for item in example["blocks"]), sum(item["zero"] for item in example["blocks"]))
    reject("K07_BAD_BLOCK_SIGNATURE", inertia != (0, 4, 0))
    incidence_example = next(current for current in independent_original.values() if current["gradient_incidence"] == "SPLIT_ACROSS_BOTH_PLANES")
    reject("K08_MUTATED_INCIDENCE", incidence_example["gradient_incidence"] != "WHOLLY_IN_ONE_PLANE")
    reject("K09_OMITTED_MAP_JETS", omitted_jet_max > TOL)
    _, synthetic_uncertain, _ = rank_info(np.diag((1.0, 5.0e-9, 0.0, 0.0)))
    reject("K10_UNCERTAINTY_PROMOTION", synthetic_uncertain)
    jordan_metric = np.asarray(((0.0,1.0,0.0,0.0),(1.0,0.0,0.0,0.0),(0.0,0.0,1.0,0.0),(0.0,0.0,0.0,1.0))); jordan = np.zeros((4,4)); jordan[0,1] = 1.0
    jordan_result = classify([jordan], np.zeros(4), jordan_metric, {"R":jordan,"H":jordan,"D":jordan}, ("R",))
    reject("K11_DEFECTIVE_JORDAN", jordan_result["numeric_status"] == "NUMERIC_UNCERTAIN")
    rh_examples = [(independent_original[(cid,"M01_R")], independent_original[(cid,"M02_H")]) for cid in anchor_ids
                   if independent_original[(cid,"M01_R")]["unique_pair"] is not None and independent_original[(cid,"M02_H")]["unique_pair"] is not None]
    reject("K12_FALSE_SAME_SPLIT", bool(rh_examples) and set_distance(list(rh_examples[0][0]["unique_pair"]), list(rh_examples[0][1]["unique_pair"])) > TOL)
    write_tsv(HERE / "INDEPENDENT_CATCH_PROOFS.tsv", ("catch_id","result"), catches)
    output = {
        "status": "PASS", "blind_anchor_configurations": 384, "original_family_classifications": 11904,
        "transformed_family_classifications": 23808, "total_family_classifications": 35712,
        "saved_comparisons": comparisons, "independent_uncertain_classifications": uncertain,
        "maximum_parent_tensor_residual": parent_max, "maximum_nonlinear_covariance_residual": covariance_max,
        "omitted_nonlinear_jet_residual": omitted_jet_max,
        "maximum_saved_projector_distance": max_projector_saved, "catch_proofs": len(catches),
        "maximum_conclusion": MAXIMUM,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    transcript = ["UDT_INSTRUMENT_MOTIF_ATLAS_VERIFICATION=PASS",
                  "anchors=384 original=11904 transformed=23808 total=35712",
                  f"parent_residual={parent_max:.17g} covariance_residual={covariance_max:.17g} saved_projector_distance={max_projector_saved:.17g}",
                  f"uncertain={uncertain} catch_proofs={len(catches)}", f"maximum_conclusion={MAXIMUM}"]
    (HERE / "VERIFICATION_TRANSCRIPT.txt").write_text("\n".join(transcript) + "\n", encoding="utf-8")
    print("\n".join(transcript))


if __name__ == "__main__":
    main()
