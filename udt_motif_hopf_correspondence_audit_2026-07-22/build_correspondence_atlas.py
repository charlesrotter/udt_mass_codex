#!/usr/bin/env python3
"""Build the preregistered coherent metric-motif continuation/distribution atlas."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import itertools
import json
import math
import multiprocessing as mp
import os
import sys
from collections import Counter
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
STRUCTURAL = ROOT / "udt_structural_ensemble_metric_atlas_2026-07-21"
VOLUME = ROOT / "udt_amplitude_volume_metric_atlas_2026-07-21"
INDEPENDENT = ROOT / "udt_independent_amplitude_metric_atlas_2026-07-21"
CONSTRUCTIVE = ROOT / "udt_constructive_metric_family_atlas_2026-07-21"
EVALUATOR = ROOT / "udt_canonical_geometry_evaluator_p01_2026-07-21"
JOINT = ROOT / "udt_joint_invariant_subspace_atlas_2026-07-21"
MOTIF = ROOT / "udt_instrument_motif_atlas_2026-07-21"
for path in (STRUCTURAL, VOLUME, INDEPENDENT, CONSTRUCTIVE, EVALUATOR, JOINT, MOTIF):
    sys.path.insert(0, str(path))

import build_structural_ensemble_atlas as structural  # noqa: E402
import build_amplitude_volume_atlas as volume  # noqa: E402
from canonical_geometry_evaluator import evaluate_metric_jets  # noqa: E402
from invariant_subspace_core import family_operators, intrinsic_objects, relmax  # noqa: E402
from motif_core import (  # noqa: E402
    GROUP_BITS,
    classify_motif_family,
    complementary_rank_two_splits,
    public_family_row,
)


SCHEMA = "udt-motif-hopf-correspondence-atlas-1.0"
PATH_NODES = 17
H_STEPS = (1.0e-4, 5.0e-5)
DERIVATIVE_CONVERGENCE = 5.0e-3
FROBENIUS_INTEGRABLE = 1.0e-7
FROBENIUS_NONINTEGRABLE = 1.0e-5
PROJECTOR_GATE = 1.0e-9
SOURCE_HASHES = {
    "udt_amplitude_volume_metric_atlas_2026-07-21/SHA256SUMS.txt": "5182486f4a87080096532d9fe5ba999837ac79fac979c5694f216209ae41c112",
    "udt_joint_invariant_subspace_atlas_2026-07-21/SHA256SUMS.txt": "973dcc8bb297fad8358087318b24e5db9d1179e8b6a51a2535a0110e30c108c2",
    "udt_instrument_motif_atlas_2026-07-21/SHA256SUMS.txt": "97dac2c32317deb603a054cffd3d2162f537d8bc7806d2276fa7e8544dd22ed5",
    "udt_structural_ensemble_metric_atlas_2026-07-21/SHA256SUMS.txt": "3d569ed31506f5f7ce44beac30e8419571f734b3973dcc34d6c474bf78636757",
    "udt_canonical_geometry_evaluator_p01_2026-07-21/SHA256SUMS.txt": "b7d8917cb27627c7ad7767fcffbd5b5d7a9dc6da2171b2d8fba329d04014ffad",
    "null_section_hopfion_metric_audit_2026-07-19/SHA256SUMS.txt": "e195d14349407c23e4a050628ec84298d3d35e23e2c25b5cf285a5c81f8e989b",
    "angular_toric_closure_selector_2026-07-19/SHA256SUMS.txt": "64d664a76a28c170cdc293626cd6a5011755ee4eeaa414a303ace7b6eec9ec50",
    "native_hopfion_topology_audit_2026-07-19/SHA256SUMS.txt": "6f03f82d485d4a20c2d2bfc13dc8979c1b229bf92c53f0eb36831abf3d75febc",
    "noNull_energy.py": "53110844b3925b9b46bb48a3865f1bf9f60290efdd01a5830e0e388aeb477444",
    "noNull_resolve.py": "995df0c30e1595a83d1335050be8e3fbbfb22f02b6b5d6643787048cc2d7aa2b",
}
DIRECT_PRODUCTION_SOURCE_MANIFESTS = {
    "udt_amplitude_volume_metric_atlas_2026-07-21/SHA256SUMS.txt",
    "udt_joint_invariant_subspace_atlas_2026-07-21/SHA256SUMS.txt",
}
POINT_PAIRS = {0: ("P0", "P4"), 1: ("P1", "P5"), 2: ("P2", "P6"), 3: ("P3", "P7")}

PATH_FIELDS = (
    "identity_id", "configuration_id", "bank", "carrier_id", "mask_id", "path_node", "t",
    "family_id", "family_mask", "instrument_groups", "motif", "primitive_block_ranks",
    "primitive_block_signatures", "algebra_dimension", "central_split_count", "numeric_status",
    "projector_set_sha256", "projector_validation_residual",
)
SUMMARY_FIELDS = (
    "identity_id", "bank", "carrier_id", "mask_id", "family_id", "family_mask", "nodes",
    "distinct_motifs", "motif_transitions", "classified_nodes", "stable_projector_path",
    "matched_edges", "unmatched_edges", "max_adjacent_projector_distance",
    "endpoint_transport_sha256", "holonomy_status",
)
DISTRIBUTION_FIELDS = (
    "identity_id", "bank", "carrier_id", "mask_id", "family_id", "family_mask", "motif",
    "distribution_id", "distribution_kind", "rank", "signature", "stencil_status",
    "derivative_convergence_residual", "frobenius_obstruction_h", "frobenius_obstruction_h2",
    "frobenius_class", "orientation_status", "global_status",
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def canonical_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fields, rows) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def source_lineage_rows() -> list[dict[str, str]]:
    return [
        {
            "path": source,
            "sha256": expected,
            "role": (
                "DIRECT_PRODUCTION_SOURCE_MANIFEST"
                if source in DIRECT_PRODUCTION_SOURCE_MANIFESTS
                else "FROZEN_SOURCE"
            ),
        }
        for source, expected in SOURCE_HASHES.items()
    ]


def family_registry() -> list[dict[str, object]]:
    rows = read_tsv(MOTIF / "INSTRUMENT_SUBSET_REGISTRY.tsv")
    return [
        {
            "family_id": row["family_id"],
            "mask": int(row["mask"]),
            "keys": tuple(row["operator_keys"].split(";")),
        }
        for row in rows
    ]


FAMILIES = family_registry()


def identities() -> list[dict[str, object]]:
    carrier_rows = read_tsv(STRUCTURAL / "CARRIER_VECTOR_REGISTRY.tsv")
    rows = []
    order = 0
    for bank in range(4):
        start_id, end_id = POINT_PAIRS[bank]
        start = np.asarray(volume.previous.parent.POINTS[start_id], dtype=float)
        end = np.asarray(volume.previous.parent.POINTS[end_id], dtype=float)
        for carrier in carrier_rows:
            full = np.asarray([float(carrier[name]) for name in structural.PARAMETERS], dtype=float)
            for mask in range(16):
                amplitudes = structural.mask_vector(full, mask)
                rows.append({
                    "identity_order": order,
                    "identity_id": f"B{bank}_{carrier['carrier_id']}_M{mask:X}",
                    "bank": bank,
                    "carrier_id": carrier["carrier_id"],
                    "mask": mask,
                    "start_point": start.tolist(),
                    "end_point": end.tolist(),
                    "amplitudes": amplitudes.tolist(),
                })
                order += 1
    return rows


def block_labels(result: dict[str, object]) -> list[tuple[int, str]]:
    return [(int(record["rank"]), str(record["signature"])) for record in result["block_records"]]


def projector_validation(result: dict[str, object], objects: dict[str, object], keys: tuple[str, ...]) -> float:
    projectors = [np.asarray(item, dtype=float) for item in result["projectors"]]
    if not projectors:
        return math.inf
    metric = np.asarray(objects["metric"], dtype=float)
    operators = family_operators(objects, keys)
    residuals = [relmax(sum(projectors, np.zeros((4, 4))), np.eye(4))]
    for index, projector in enumerate(projectors):
        residuals.append(relmax(projector @ projector, projector))
        residuals.append(relmax(projector.T @ metric, metric @ projector))
        for operator in operators:
            residuals.append(relmax(projector @ operator, operator @ projector))
        for other in projectors[index + 1:]:
            residuals.append(relmax(projector @ other, np.zeros((4, 4))))
            residuals.append(relmax(other @ projector, np.zeros((4, 4))))
    return max(residuals, default=0.0)


def classify_point(bank: int, amplitudes: np.ndarray, point: np.ndarray) -> tuple[object, dict[int, dict[str, object]]]:
    family = volume.previous.regular_family(bank, amplitudes, point)
    geometry = evaluate_metric_jets(family["metric_jets"])
    phi = family["phi"]
    objects = intrinsic_objects(geometry, np.asarray(phi.first), np.asarray(phi.second))
    scalar = {key: objects[key] for key in ("R", "H", "D")}
    results = {}
    for record in FAMILIES:
        keys = record["keys"]
        result = classify_motif_family(
            family_operators(objects, keys), objects["gradient"], objects["metric"], scalar, keys
        )
        result["projector_validation_residual"] = projector_validation(result, objects, keys)
        results[int(record["mask"])] = result
    return geometry, results


def matched_projectors(reference: dict[str, object], current: dict[str, object]):
    labels_first = block_labels(reference)
    labels_second = block_labels(current)
    if Counter(labels_first) != Counter(labels_second):
        return None, None, math.inf
    first = [np.asarray(item, dtype=float) for item in reference["projectors"]]
    second = [np.asarray(item, dtype=float) for item in current["projectors"]]
    best = None
    best_perm = None
    best_distance = math.inf
    for permutation in itertools.permutations(range(len(second))):
        if any(labels_first[index] != labels_second[permutation[index]] for index in range(len(first))):
            continue
        ordered = [second[permutation[index]] for index in range(len(first))]
        distance = max((relmax(first[index], ordered[index]) for index in range(len(first))), default=0.0)
        if distance < best_distance:
            best = ordered
            best_perm = permutation
            best_distance = distance
    return best, best_perm, best_distance


def projector_digest(projectors) -> str:
    values = [[[float(value) for value in row] for row in np.asarray(projector)] for projector in projectors]
    return canonical_hash(values)


def covariant_projector_derivative(projector: np.ndarray, partial: np.ndarray, gamma: np.ndarray) -> np.ndarray:
    result = np.asarray(partial, dtype=float).copy()
    for rho, nu, beta, sigma in itertools.product(range(4), repeat=4):
        result[rho, nu, beta] += (
            gamma[nu, rho, sigma] * projector[sigma, beta]
            - gamma[sigma, rho, beta] * projector[nu, sigma]
        )
    return result


def frobenius_obstruction(projector: np.ndarray, partial: np.ndarray, gamma: np.ndarray) -> float:
    nabla = covariant_projector_derivative(projector, partial, gamma)
    term = np.zeros((4, 4, 4))
    for nu, alpha, beta, rho in itertools.product(range(4), repeat=4):
        term[nu, alpha, beta] += (
            projector[rho, alpha] * nabla[rho, nu, beta]
            - projector[rho, beta] * nabla[rho, nu, alpha]
        )
    complement = np.eye(4) - projector
    obstruction = np.einsum("mn,nab->mab", complement, term)
    return float(np.linalg.norm(obstruction) / max(np.linalg.norm(nabla), 1.0e-30))


def obstruction_class(value: float, convergence: float) -> str:
    if convergence > DERIVATIVE_CONVERGENCE:
        return "NUMERIC_UNCERTAIN_DERIVATIVE"
    if value <= FROBENIUS_INTEGRABLE:
        return "NUMERICALLY_INTEGRABLE_LOCAL"
    if value >= FROBENIUS_NONINTEGRABLE:
        return "NUMERICALLY_NONINTEGRABLE_LOCAL"
    return "NUMERIC_UNCERTAIN_OBSTRUCTION"


def distribution_rows_for_family(identity, mask, center_geometry, center, stencil):
    base = {
        "identity_id": identity["identity_id"],
        "bank": f"B{identity['bank']}",
        "carrier_id": identity["carrier_id"],
        "mask_id": f"M{identity['mask']:X}",
        "family_id": next(item["family_id"] for item in FAMILIES if item["mask"] == mask),
        "family_mask": mask,
        "motif": center["motif"],
    }
    all_results = [center]
    for step in H_STEPS:
        for axis in range(4):
            all_results.extend((stencil[(step, axis, -1)][mask], stencil[(step, axis, 1)][mask]))
    stable = (
        center["numeric_status"] == "NUMERIC_CLASSIFIED"
        and all(result["numeric_status"] == "NUMERIC_CLASSIFIED" for result in all_results)
        and all(Counter(block_labels(result)) == Counter(block_labels(center)) for result in all_results)
    )
    if not stable:
        return [{
            **base,
            "distribution_id": "UNSTABLE_PROJECTOR_SET",
            "distribution_kind": "UNRESOLVED",
            "rank": "-",
            "signature": "-",
            "stencil_status": "DEGENERATE_OR_UNCERTAIN_RETAINED",
            "derivative_convergence_residual": "nan",
            "frobenius_obstruction_h": "nan",
            "frobenius_obstruction_h2": "nan",
            "frobenius_class": "NOT_CLASSIFIED",
            "orientation_status": "NOT_SELECTED",
            "global_status": "GLOBAL_DATA_ABSENT",
        }]

    center_projectors = [np.asarray(item, dtype=float) for item in center["projectors"]]
    derivatives = {}
    for step in H_STEPS:
        step_derivatives = [np.zeros((4, 4, 4)) for _ in center_projectors]
        for axis in range(4):
            minus, _, _ = matched_projectors(center, stencil[(step, axis, -1)][mask])
            plus, _, _ = matched_projectors(center, stencil[(step, axis, 1)][mask])
            if minus is None or plus is None:
                return [{
                    **base,
                    "distribution_id": "FAILED_PROJECTOR_MATCH",
                    "distribution_kind": "UNRESOLVED",
                    "rank": "-", "signature": "-",
                    "stencil_status": "MATCH_FAILED_RETAINED",
                    "derivative_convergence_residual": "nan",
                    "frobenius_obstruction_h": "nan",
                    "frobenius_obstruction_h2": "nan",
                    "frobenius_class": "NOT_CLASSIFIED",
                    "orientation_status": "NOT_SELECTED",
                    "global_status": "GLOBAL_DATA_ABSENT",
                }]
            for index in range(len(center_projectors)):
                step_derivatives[index][axis] = (plus[index] - minus[index]) / (2.0 * step)
        derivatives[step] = step_derivatives

    labels = block_labels(center)
    candidates = []
    for index, (rank, signature) in enumerate(labels):
        candidates.append((f"PRIMITIVE_{index}", "PRIMITIVE_BLOCK", [index], rank, signature))
    splits = complementary_rank_two_splits(center_projectors)
    for split_index, pair in enumerate(splits):
        for side, projector in enumerate(pair):
            members = [index for index, item in enumerate(center_projectors) if relmax(projector @ item, item) <= 1.0e-8]
            signature = "COMPOSITE_RANK2"
            candidates.append((f"SPLIT_{split_index}_SIDE_{side}", "COMPLEMENTARY_RANK2", members, 2, signature))

    rows = []
    gamma = np.asarray(center_geometry.christoffel, dtype=float)
    for distribution_id, kind, members, rank, signature in candidates:
        projector = sum((center_projectors[index] for index in members), np.zeros((4, 4)))
        partial_h = sum((derivatives[H_STEPS[0]][index] for index in members), np.zeros((4, 4, 4)))
        partial_h2 = sum((derivatives[H_STEPS[1]][index] for index in members), np.zeros((4, 4, 4)))
        convergence = float(np.linalg.norm(partial_h - partial_h2) / max(np.linalg.norm(partial_h2), 1.0))
        if rank == 1:
            obstruction_h = 0.0
            obstruction_h2 = 0.0
            classification = "LOCALLY_INTEGRABLE_BY_RANK_ONE"
        elif rank == 4:
            obstruction_h = 0.0
            obstruction_h2 = 0.0
            classification = "WHOLE_TANGENT_SPACE"
        else:
            obstruction_h = frobenius_obstruction(projector, partial_h, gamma)
            obstruction_h2 = frobenius_obstruction(projector, partial_h2, gamma)
            classification = obstruction_class(obstruction_h2, convergence)
        rows.append({
            **base,
            "distribution_id": distribution_id,
            "distribution_kind": kind,
            "rank": rank,
            "signature": signature,
            "stencil_status": "STABLE_CLASSIFIED",
            "derivative_convergence_residual": f"{convergence:.17g}",
            "frobenius_obstruction_h": f"{obstruction_h:.17g}",
            "frobenius_obstruction_h2": f"{obstruction_h2:.17g}",
            "frobenius_class": classification,
            "orientation_status": "PROJECTOR_ONLY_UNORIENTED",
            "global_status": "GLOBAL_DATA_ABSENT",
        })
    return rows


def process_identity(identity):
    bank = int(identity["bank"])
    amplitudes = np.asarray(identity["amplitudes"], dtype=float)
    start = np.asarray(identity["start_point"], dtype=float)
    end = np.asarray(identity["end_point"], dtype=float)
    path_results = []
    path_geometries = []
    for node in range(PATH_NODES):
        t = node / (PATH_NODES - 1)
        point = (1.0 - t) * start + t * end
        geometry, results = classify_point(bank, amplitudes, point)
        path_geometries.append(geometry)
        path_results.append(results)

    path_rows = []
    summary_rows = []
    for family in FAMILIES:
        mask = int(family["mask"])
        results = [item[mask] for item in path_results]
        motifs = [str(item["motif"]) for item in results]
        permutations = []
        distances = []
        unmatched = 0
        for left, right in zip(results[:-1], results[1:]):
            _matched, permutation, distance = matched_projectors(left, right)
            if permutation is None:
                unmatched += 1
                permutations.append("-")
            else:
                permutations.append(",".join(map(str, permutation)))
                distances.append(distance)
        stable = (
            all(item["numeric_status"] == "NUMERIC_CLASSIFIED" for item in results)
            and len(set(motifs)) == 1
            and unmatched == 0
        )
        for node, result in enumerate(results):
            t = node / (PATH_NODES - 1)
            public = public_family_row(result)
            config_id = f"{identity['carrier_id']}_M{identity['mask']:X}_B{bank}_T{node:02d}"
            path_rows.append({
                "identity_id": identity["identity_id"],
                "configuration_id": config_id,
                "bank": f"B{bank}",
                "carrier_id": identity["carrier_id"],
                "mask_id": f"M{identity['mask']:X}",
                "path_node": node,
                "t": f"{t:.17g}",
                "family_id": family["family_id"],
                "family_mask": mask,
                "instrument_groups": ";".join(family["keys"]),
                "motif": public["motif"],
                "primitive_block_ranks": public["primitive_block_ranks"],
                "primitive_block_signatures": public["primitive_block_signatures"],
                "algebra_dimension": public["algebra_dimension"],
                "central_split_count": public["central_split_count"],
                "numeric_status": public["numeric_status"],
                "projector_set_sha256": projector_digest(result["projectors"]),
                "projector_validation_residual": f"{result['projector_validation_residual']:.17g}",
            })
        summary_rows.append({
            "identity_id": identity["identity_id"],
            "bank": f"B{bank}",
            "carrier_id": identity["carrier_id"],
            "mask_id": f"M{identity['mask']:X}",
            "family_id": family["family_id"],
            "family_mask": mask,
            "nodes": PATH_NODES,
            "distinct_motifs": ";".join(sorted(set(motifs))),
            "motif_transitions": sum(left != right for left, right in zip(motifs[:-1], motifs[1:])),
            "classified_nodes": sum(item["numeric_status"] == "NUMERIC_CLASSIFIED" for item in results),
            "stable_projector_path": "YES" if stable else "NO",
            "matched_edges": PATH_NODES - 1 - unmatched,
            "unmatched_edges": unmatched,
            "max_adjacent_projector_distance": f"{max(distances, default=0.0):.17g}",
            "endpoint_transport_sha256": canonical_hash(permutations),
            "holonomy_status": "NOT_TESTED_BY_OPEN_PATH",
        })

    midpoint = (start + end) / 2.0
    center_geometry = path_geometries[PATH_NODES // 2]
    center = path_results[PATH_NODES // 2]
    stencil = {}
    for step in H_STEPS:
        for axis in range(4):
            for sign in (-1, 1):
                point = midpoint.copy()
                point[axis] += sign * step
                _geometry, result = classify_point(bank, amplitudes, point)
                stencil[(step, axis, sign)] = result
    distribution_rows = []
    for family in FAMILIES:
        distribution_rows.extend(
            distribution_rows_for_family(identity, int(family["mask"]), center_geometry, center[int(family["mask"])], stencil)
        )
    return path_rows, summary_rows, distribution_rows


class DeterministicGzipTsvWriter:
    def __init__(self, path: Path, fields) -> None:
        self.raw = path.open("wb")
        self.compressed = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        self.text = io.TextIOWrapper(self.compressed, encoding="utf-8", newline="")
        self.writer = csv.DictWriter(
            self.text, fieldnames=list(fields), delimiter="\t", lineterminator="\n"
        )
        self.writer.writeheader()

    def writerows(self, rows) -> None:
        self.writer.writerows(rows)

    def close(self) -> None:
        self.text.flush()
        self.text.close()
        self.raw.close()


def build(workers: int) -> None:
    for source, expected in SOURCE_HASHES.items():
        actual = digest(ROOT / source)
        if actual != expected:
            raise AssertionError(f"source hash mismatch {source} {actual}")
    source_rows = source_lineage_rows()
    write_tsv(HERE / "SOURCE_LINEAGE.tsv", ("path", "sha256", "role"), source_rows)

    all_identities = identities()
    if len(all_identities) != 3072 or len({row["identity_id"] for row in all_identities}) != 3072:
        raise AssertionError("identity coverage")
    registry_rows = [{
        "identity_order": row["identity_order"],
        "identity_id": row["identity_id"],
        "bank": f"B{row['bank']}",
        "carrier_id": row["carrier_id"],
        "mask_id": f"M{row['mask']:X}",
        "start_point": json.dumps(row["start_point"], separators=(",", ":")),
        "end_point": json.dumps(row["end_point"], separators=(",", ":")),
        "global_domain_status": "LOCAL_ANALYTIC_CHART_ONLY",
    } for row in all_identities]
    write_tsv(HERE / "COHERENT_IDENTITY_REGISTRY.tsv", tuple(registry_rows[0]), registry_rows)

    path_file = HERE / "PATH_FAMILY_ATLAS.tsv.gz"
    summary_file = HERE / "PATH_CONTINUATION_SUMMARY.tsv.gz"
    distribution_file = HERE / "DISTRIBUTION_ATLAS.tsv.gz"
    path_writer = DeterministicGzipTsvWriter(path_file, PATH_FIELDS)
    summary_writer = DeterministicGzipTsvWriter(summary_file, SUMMARY_FIELDS)
    distribution_writer = DeterministicGzipTsvWriter(distribution_file, DISTRIBUTION_FIELDS)

    context = mp.get_context("fork")
    completed = 0
    try:
        with context.Pool(processes=workers) as pool:
            for path_rows, summary_rows, distribution_rows in pool.imap(process_identity, all_identities, chunksize=1):
                path_writer.writerows(path_rows)
                summary_writer.writerows(summary_rows)
                distribution_writer.writerows(distribution_rows)
                completed += 1
                if completed % 32 == 0 or completed == len(all_identities):
                    print(f"completed {completed}/{len(all_identities)}", flush=True)
    finally:
        path_writer.close()
        summary_writer.close()
        distribution_writer.close()

    result = summarize_outputs()
    (HERE / "ATLAS_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def gzip_rows(path: Path):
    with gzip.open(path, "rt", encoding="utf-8", newline="") as handle:
        yield from csv.DictReader(handle, delimiter="\t")


def summarize_outputs() -> dict[str, object]:
    path_count = 0
    motif_census = Counter()
    numeric_census = Counter()
    max_validation = 0.0
    for row in gzip_rows(HERE / "PATH_FAMILY_ATLAS.tsv.gz"):
        path_count += 1
        motif_census[row["motif"]] += 1
        numeric_census[row["numeric_status"]] += 1
        max_validation = max(max_validation, float(row["projector_validation_residual"]))
    summary_count = 0
    stable_paths = 0
    transition_census = Counter()
    for row in gzip_rows(HERE / "PATH_CONTINUATION_SUMMARY.tsv.gz"):
        summary_count += 1
        stable_paths += row["stable_projector_path"] == "YES"
        transition_census[int(row["motif_transitions"])] += 1
    distribution_count = 0
    distribution_census = Counter()
    stencil_census = Counter()
    max_convergence = 0.0
    for row in gzip_rows(HERE / "DISTRIBUTION_ATLAS.tsv.gz"):
        distribution_count += 1
        distribution_census[row["frobenius_class"]] += 1
        stencil_census[row["stencil_status"]] += 1
        value = row["derivative_convergence_residual"]
        if value != "nan":
            max_convergence = max(max_convergence, float(value))
    expected_paths = 3072 * PATH_NODES * 31
    expected_summaries = 3072 * 31
    if path_count != expected_paths:
        raise AssertionError(f"path count {path_count} != {expected_paths}")
    if summary_count != expected_summaries:
        raise AssertionError(f"summary count {summary_count} != {expected_summaries}")
    return {
        "schema": SCHEMA,
        "coherent_identities": 3072,
        "path_nodes": PATH_NODES,
        "metric_phi_twojets": 3072 * PATH_NODES,
        "path_family_rows": path_count,
        "path_summary_rows": summary_count,
        "stable_projector_paths": int(stable_paths),
        "motif_census": dict(sorted(motif_census.items())),
        "numeric_status_census": dict(sorted(numeric_census.items())),
        "motif_transition_count_census": {str(key): value for key, value in sorted(transition_census.items())},
        "distribution_rows": distribution_count,
        "distribution_class_census": dict(sorted(distribution_census.items())),
        "stencil_status_census": dict(sorted(stencil_census.items())),
        "max_projector_validation_residual": max_validation,
        "max_derivative_convergence_residual": max_convergence,
        "global_hopf_eligible_local_identities": 0,
        "global_status": "GLOBAL_DATA_ABSENT_FOR_ALL_LOCAL_ANALYTIC_IDENTITIES",
        "holonomy_status": "NOT_TESTED_BY_OPEN_PATH",
        "maximum_conclusion": "BOUNDED_COHERENT_LOCAL_MOTIF_CONTINUATION_AND_DISTRIBUTIONS_CHARACTERIZED",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=min(16, os.cpu_count() or 1))
    args = parser.parse_args()
    if args.workers < 1 or args.workers > 32:
        raise SystemExit("workers must be in 1..32")
    build(args.workers)


if __name__ == "__main__":
    main()
