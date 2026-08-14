#!/usr/bin/env python3
"""Assemble the preregistered R5 full-spectrum common-subspace atlas."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import resource
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
CELLS = Path("/media/udt-admin/ScratchDisk/Data/UDT_BOSS_R3_2026-08-14/R3_COVARIANCE_CELLS")
PARENT_HASHES = {
    "R2_CURVE_ATLAS.tsv": "32b592a85cbadbc080391353be6d0ee73a2d0d8a37c10aead28e041a7810f603",
    "R4_RELATION_ATLAS.tsv": "1badac0c2eeedb2932a8d53f6116d4bfa247774c76f5750ad652da9f35696184",
    "R4_VERIFICATION_RESULT.json": "1028f4f80578995c20e5f020db4fbfafc9b73e64589e2fd055f0f3763469b05b",
    "R3_OUTPUT_MANIFEST.tsv": "3a38784ac248997bd987598308b98edbf60566759e4fdc35d54d98b161a11cfa",
}
RELATION_TYPES = (
    "RANDOM_DENSITY",
    "WEIGHT_LANE",
    "CAP",
    "ADJACENT_SHELL",
    "COARSE_FINE_CONTAINMENT",
)
RELATION_COUNTS = {
    "RANDOM_DENSITY": 1552,
    "WEIGHT_LANE": 1746,
    "CAP": 1164,
    "ADJACENT_SHELL": 2184,
    "COARSE_FINE_CONTAINMENT": 2640,
}
TRANSFORMS = ("CENTERED_UNIT", "FIRST_DIFFERENCE_UNIT")
LANES = ("W0_UNIT", "W1_SPECTRO", "W2_IMAGING", "W3_OFFICIAL_OBS")
NSIDES = (4, 8, 16)
EPS = np.finfo(np.float64).eps
GAP_FLOOR = np.sqrt(EPS)
OUTPUTS = (
    "R5_VIEW_SPECTRA.tsv",
    "R5_RANKED_SUBSPACE_OVERLAPS.tsv",
    "R5_COVARIANCE_SUBSPACE_ATLAS.tsv",
    "R5_COVARIANCE_SUBSPACE_SUMMARY.tsv",
    "R5_RESULT.json",
    "R5_OUTPUT_MANIFEST.tsv",
)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def atomic_tsv(path: Path, rows, fieldnames) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temp, path)


def read_tsv(path: Path):
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def curve_key(row):
    return (
        row["sample"], row["cap"], int(row["factor"]), int(row["group"]),
        row["lane"], int(row["ratio"]),
    )


def parse_endpoint(text: str):
    sample, cap, factor, group, lane, ratio = text.split("|")
    return sample, cap, int(factor), int(group), lane, int(ratio)


def read_curves(path: Path):
    grouped = defaultdict(list)
    theta = defaultdict(list)
    ids = {}
    for row in read_tsv(path):
        key = curve_key(row)
        grouped[key].append(float(row["w_theta"]))
        theta[key].append((float(row["theta_lo_deg"]), float(row["theta_hi_deg"])))
        ids.setdefault(key, row["curve_id"])
        if ids[key] != row["curve_id"]:
            raise AssertionError(f"curve id changed within key {key}")
    if len(grouped) != 2328:
        raise AssertionError(f"curve count {len(grouped)}")
    reference_grid = None
    curves = {}
    for key in sorted(grouped):
        if len(grouped[key]) != 119:
            raise AssertionError(f"bin count {key}: {len(grouped[key])}")
        grid = tuple(theta[key])
        if reference_grid is None:
            reference_grid = grid
        if grid != reference_grid:
            raise AssertionError(f"theta grid mismatch {key}")
        vector = np.asarray(grouped[key], dtype=np.float64)
        if not np.all(np.isfinite(vector)):
            raise AssertionError(f"nonfinite curve {key}")
        curves[key] = vector
    return curves, reference_grid


def transformed(vector: np.ndarray, name: str):
    if name == "CENTERED_UNIT":
        out = vector - np.mean(vector)
    elif name == "FIRST_DIFFERENCE_UNIT":
        out = np.diff(vector)
    else:
        raise KeyError(name)
    norm = float(np.linalg.norm(out))
    if norm == 0.0:
        return np.zeros_like(out), 1
    return out / norm, 0


def linear_transform(name: str):
    if name == "CENTERED_UNIT":
        return np.eye(119) - np.ones((119, 119), dtype=np.float64) / 119.0
    if name == "FIRST_DIFFERENCE_UNIT":
        matrix = np.zeros((118, 119), dtype=np.float64)
        index = np.arange(118)
        matrix[index, index] = -1.0
        matrix[index, index + 1] = 1.0
        return matrix
    raise KeyError(name)


def selection_name(sample: str, cap: str, factor: int, group: int):
    return f"{sample}_{cap}_f{factor}_g{group:02d}"


def cell_path(selection: str):
    return CELLS / f"{selection}.npz"


def quantiles(values):
    array = np.asarray(values, dtype=np.float64)
    if array.size == 0 or not np.all(np.isfinite(array)):
        raise AssertionError("invalid summary values")
    qs = np.quantile(array, [0.0, 0.25, 0.5, 0.75, 0.9, 0.95, 1.0])
    return [float(value) for value in qs]


def main():
    start = time.time()
    for name in OUTPUTS:
        if (HERE / name).exists():
            raise FileExistsError(HERE / name)
    for name, expected in PARENT_HASHES.items():
        if digest(HERE / name) != expected:
            raise AssertionError(f"parent hash mismatch: {name}")

    curves, theta_grid = read_curves(HERE / "R2_CURVE_ATLAS.tsv")
    relations = read_tsv(HERE / "R4_RELATION_ATLAS.tsv")
    if len(relations) != 9286:
        raise AssertionError(f"relation count {len(relations)}")
    for index, row in enumerate(relations):
        if int(row["relation_id"]) != index:
            raise AssertionError(f"relation order {index}")
        if parse_endpoint(row["curve_a"]) not in curves or parse_endpoint(row["curve_b"]) not in curves:
            raise AssertionError(f"relation endpoint missing {index}")
    counts = Counter(row["relation_type"] for row in relations)
    if dict(counts) != RELATION_COUNTS:
        raise AssertionError(f"relation census {counts}")

    transformed_curves = {}
    degenerate_by_transform = {}
    for name in TRANSFORMS:
        cache = {}
        degenerate = 0
        for key, vector in curves.items():
            cache[key], flag = transformed(vector, name)
            degenerate += flag
        transformed_curves[name] = cache
        degenerate_by_transform[name] = degenerate

    spectra_rows = []
    overlap_rows = []
    bases = {}
    singular_values = {}
    max_orthonormality_error = 0.0
    global_keys = sorted(curves)

    relation_groups = {kind: [row for row in relations if row["relation_type"] == kind]
                       for kind in RELATION_TYPES}
    for transform_name in TRANSFORMS:
        cache = transformed_curves[transform_name]
        view_keys = {"GLOBAL": global_keys}
        for kind in RELATION_TYPES:
            view_keys[f"{kind}_A"] = [parse_endpoint(row["curve_a"]) for row in relation_groups[kind]]
            view_keys[f"{kind}_B"] = [parse_endpoint(row["curve_b"]) for row in relation_groups[kind]]
        for view_name, keys in view_keys.items():
            matrix = np.vstack([cache[key] for key in keys])
            _, singular, vt = np.linalg.svd(matrix, full_matrices=False)
            dimension = matrix.shape[1]
            if vt.shape != (dimension, dimension):
                raise AssertionError(f"basis shape {transform_name}/{view_name}: {vt.shape}")
            orth_error = float(np.max(np.abs(vt @ vt.T - np.eye(dimension))))
            max_orthonormality_error = max(max_orthonormality_error, orth_error)
            if orth_error > 5e-12:
                raise AssertionError(f"orthonormality {transform_name}/{view_name}: {orth_error}")
            if np.any(np.diff(singular) > 5e-12 * max(1.0, float(singular[0]))):
                raise AssertionError(f"spectrum ordering {transform_name}/{view_name}")
            bases[(transform_name, view_name)] = vt
            singular_values[(transform_name, view_name)] = singular
            total_energy = float(np.sum(singular * singular))
            cumulative = 0.0
            first = float(singular[0]) if singular.size else 0.0
            zero_rows = sum(float(np.linalg.norm(cache[key])) == 0.0 for key in keys)
            for mode_index, value in enumerate(singular, 1):
                fraction = float(value * value / total_energy) if total_energy > 0.0 else 0.0
                cumulative += fraction
                next_value = float(singular[mode_index]) if mode_index < dimension else 0.0
                gap = float(value - next_value)
                spectra_rows.append({
                    "transform": transform_name,
                    "view": view_name,
                    "row_count": len(keys),
                    "dimension": dimension,
                    "zero_row_count": zero_rows,
                    "mode_index": mode_index,
                    "singular_value": float(value),
                    "next_singular_value": next_value,
                    "boundary_absolute_gap": gap,
                    "boundary_relative_gap_to_first": float(gap / first) if first > 0.0 else 0.0,
                    "squared_energy_fraction": fraction,
                    "cumulative_squared_energy_fraction": cumulative,
                    "singular_relative_to_first": float(value / first) if first > 0.0 else 0.0,
                })

        pair_specs = []
        for kind in RELATION_TYPES:
            pair_specs.append((f"{kind}__A_VS_B", f"{kind}_A", f"{kind}_B"))
        for kind in RELATION_TYPES:
            pair_specs.append((f"GLOBAL_VS_{kind}_A", "GLOBAL", f"{kind}_A"))
            pair_specs.append((f"GLOBAL_VS_{kind}_B", "GLOBAL", f"{kind}_B"))
        if len(pair_specs) != 15:
            raise AssertionError("pair specification count")
        for pair_id, view_a, view_b in pair_specs:
            va = bases[(transform_name, view_a)]
            vb = bases[(transform_name, view_b)]
            gram = np.square(va @ vb.T)
            if not np.all(np.isfinite(gram)) or np.min(gram) < -5e-12 or np.max(gram) > 1.0 + 5e-12:
                raise AssertionError(f"cross gram {transform_name}/{pair_id}")
            dimension = va.shape[0]
            singular_a = singular_values[(transform_name, view_a)]
            singular_b = singular_values[(transform_name, view_b)]
            for rank in range(1, dimension + 1):
                overlap = float(np.sum(gram[:rank, :rank]) / rank)
                principal = np.linalg.svd(va[:rank] @ vb[:rank].T, compute_uv=False)
                smallest = float(principal[-1])
                chord = float(np.sqrt(max(0.0, 1.0 - overlap)))
                next_a = float(singular_a[rank]) if rank < dimension else 0.0
                next_b = float(singular_b[rank]) if rank < dimension else 0.0
                gap_a = float(singular_a[rank - 1] - next_a)
                gap_b = float(singular_b[rank - 1] - next_b)
                if not (-5e-12 <= overlap <= 1.0 + 5e-12):
                    raise AssertionError(f"overlap {transform_name}/{pair_id}/{rank}: {overlap}")
                overlap_rows.append({
                    "transform": transform_name,
                    "pair_id": pair_id,
                    "view_a": view_a,
                    "view_b": view_b,
                    "dimension": dimension,
                    "rank": rank,
                    "projector_overlap": overlap,
                    "normalized_chord_distance": chord,
                    "smallest_principal_cosine": smallest,
                    "view_a_boundary_absolute_gap": gap_a,
                    "view_b_boundary_absolute_gap": gap_b,
                    "view_a_boundary_relative_gap_to_first": (
                        float(gap_a / singular_a[0]) if singular_a[0] > 0.0 else 0.0
                    ),
                    "view_b_boundary_relative_gap_to_first": (
                        float(gap_b / singular_b[0]) if singular_b[0] > 0.0 else 0.0
                    ),
                })
            if abs(float(np.sum(gram)) / dimension - 1.0) > 5e-12:
                raise AssertionError(f"full-rank overlap {transform_name}/{pair_id}")
    if len(spectra_rows) != 2607 or len(overlap_rows) != 3555:
        raise AssertionError(f"spectra/overlap census {len(spectra_rows)}/{len(overlap_rows)}")

    atomic_tsv(HERE / "R5_VIEW_SPECTRA.tsv", spectra_rows, list(spectra_rows[0]))
    atomic_tsv(HERE / "R5_RANKED_SUBSPACE_OVERLAPS.tsv", overlap_rows, list(overlap_rows[0]))

    cap_ratio20 = {}
    for row in relation_groups["CAP"]:
        if int(row["ratio_a"]) != 20 or int(row["ratio_b"]) != 20:
            continue
        key = (row["sample"], int(row["factor_a"]), int(row["group_a"]), row["lane_a"])
        if key in cap_ratio20:
            raise AssertionError(f"duplicate cap context {key}")
        cap_ratio20[key] = (parse_endpoint(row["curve_a"]), parse_endpoint(row["curve_b"]))
    if len(cap_ratio20) != 388:
        raise AssertionError(f"cap ratio20 contexts {len(cap_ratio20)}")

    cov_fields = [
        "covariance_id", "sample", "factor", "group", "lane", "nside", "transform",
        "rank", "dimension", "transformed_rank", "transformed_tau",
        "global_boundary_absolute_gap", "global_boundary_relative_gap_to_first",
        "covariance_range_relative_gap_to_threshold", "covariance_range_owned",
        "global_subspace_owned", "range_overlap_owned",
        "subspace_covariance_trace", "covariance_trace_per_rank", "subspace_range_overlap",
        "difference_projection_norm", "projection_norm_to_trace_sd", "trace_sd_degenerate",
    ]
    cov_temp = HERE / "R5_COVARIANCE_SUBSPACE_ATLAS.tsv.tmp"
    summary_values = defaultdict(list)
    rank_values = defaultdict(list)
    covariance_row_count = 0
    resolved_range_overlap_row_count = 0
    unresolved_range_overlap_row_count = 0
    with cov_temp.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=cov_fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        grouped_contexts = defaultdict(list)
        for key, endpoints in cap_ratio20.items():
            grouped_contexts[key[:3]].append((key[3], endpoints))
        if len(grouped_contexts) != 97:
            raise AssertionError(f"selection context count {len(grouped_contexts)}")
        for (sample, factor, group), lane_entries in sorted(grouped_contexts.items()):
            if len(lane_entries) != 4:
                raise AssertionError(f"lane context count {(sample, factor, group)}")
            north_name = selection_name(sample, "North", factor, group)
            south_name = selection_name(sample, "South", factor, group)
            with np.load(cell_path(north_name), allow_pickle=False) as nc, np.load(cell_path(south_name), allow_pickle=False) as sc:
                if json.loads(str(nc["metadata"].item()))["selection_key"] != north_name:
                    raise AssertionError(f"north cell owner {north_name}")
                if json.loads(str(sc["metadata"].item()))["selection_key"] != south_name:
                    raise AssertionError(f"south cell owner {south_name}")
                for lane, (north_key, south_key) in sorted(lane_entries):
                    lane_index = LANES.index(lane)
                    difference = curves[north_key] - curves[south_key]
                    for nside in NSIDES:
                        covariance = np.asarray(nc[f"covariance_n{nside}"][lane_index], dtype=np.float64)
                        covariance += np.asarray(sc[f"covariance_n{nside}"][lane_index], dtype=np.float64)
                        for transform_name in TRANSFORMS:
                            operator = linear_transform(transform_name)
                            transformed_difference = operator @ difference
                            transformed_covariance = operator @ covariance @ operator.T
                            transformed_covariance = 0.5 * (transformed_covariance + transformed_covariance.T)
                            eigenvalues, eigenvectors = np.linalg.eigh(transformed_covariance)
                            dimension = transformed_covariance.shape[0]
                            largest = max(0.0, float(eigenvalues[-1]))
                            tau = dimension * np.finfo(np.float64).eps * largest
                            if float(eigenvalues[0]) < -100.0 * tau:
                                raise AssertionError(
                                    f"transformed covariance PSD {(sample, factor, group, lane, nside, transform_name)}"
                                )
                            positive = eigenvalues > tau
                            rank = int(np.sum(positive))
                            if rank in (0, dimension):
                                covariance_range_relative_gap = 1.0
                                covariance_range_owned = 1
                            else:
                                positive_min = float(eigenvalues[-rank])
                                nonpositive_max = float(eigenvalues[-rank - 1])
                                covariance_range_relative_gap = (
                                    min(positive_min - tau, tau - nonpositive_max)
                                    / max(largest, EPS)
                                )
                                covariance_range_owned = int(
                                    covariance_range_relative_gap >= GAP_FLOOR
                                )
                            rank_values[(transform_name, nside)].append(float(rank))
                            basis = bases[(transform_name, "GLOBAL")]
                            variances = np.maximum(
                                np.einsum("ij,jk,ik->i", basis, transformed_covariance, basis), 0.0
                            )
                            projection_squares = np.square(basis @ transformed_difference)
                            if rank:
                                range_components = np.sum(
                                    np.square(basis @ eigenvectors[:, positive]), axis=1
                                )
                            else:
                                range_components = np.zeros(dimension, dtype=np.float64)
                            cumulative_variance = np.cumsum(variances)
                            cumulative_projection_square = np.cumsum(projection_squares)
                            cumulative_range = np.cumsum(range_components)
                            global_singular = singular_values[(transform_name, "GLOBAL")]
                            for rank_offset in range(dimension):
                                subspace_rank = rank_offset + 1
                                covariance_trace = float(cumulative_variance[rank_offset])
                                trace_sd = float(np.sqrt(covariance_trace))
                                projection_norm = float(np.sqrt(cumulative_projection_square[rank_offset]))
                                range_overlap = float(cumulative_range[rank_offset] / subspace_rank)
                                degenerate = int(trace_sd == 0.0)
                                ratio = float(projection_norm / trace_sd) if trace_sd > 0.0 else 0.0
                                next_singular = (
                                    float(global_singular[subspace_rank])
                                    if subspace_rank < dimension else 0.0
                                )
                                boundary_gap = float(global_singular[rank_offset] - next_singular)
                                boundary_relative_gap = (
                                    float(boundary_gap / global_singular[0])
                                    if global_singular[0] > 0.0 else 0.0
                                )
                                global_subspace_owned = int(
                                    subspace_rank == dimension
                                    or boundary_relative_gap >= GAP_FLOOR
                                )
                                range_overlap_owned = int(
                                    bool(global_subspace_owned) and bool(covariance_range_owned)
                                )
                                resolved_range_overlap_row_count += range_overlap_owned
                                unresolved_range_overlap_row_count += 1 - range_overlap_owned
                                values = {
                                    "covariance_trace_per_rank": covariance_trace / subspace_rank,
                                    "subspace_range_overlap": range_overlap,
                                    "difference_projection_norm": projection_norm,
                                    "projection_norm_to_trace_sd": ratio,
                                }
                                for metric, value in values.items():
                                    if not np.isfinite(value):
                                        raise AssertionError(f"nonfinite covariance subspace {metric}")
                                    if metric == "subspace_range_overlap":
                                        ownership_status = (
                                            "OWNED" if range_overlap_owned
                                            else "UNRESOLVED_NUMERICAL"
                                        )
                                    else:
                                        ownership_status = (
                                            "OWNED" if global_subspace_owned
                                            else "UNRESOLVED_NUMERICAL"
                                        )
                                    summary_values[
                                        (transform_name, nside, subspace_rank, metric, ownership_status)
                                    ].append(value)
                                writer.writerow({
                                    "covariance_id": covariance_row_count,
                                    "sample": sample,
                                    "factor": factor,
                                    "group": group,
                                    "lane": lane,
                                    "nside": nside,
                                    "transform": transform_name,
                                    "rank": subspace_rank,
                                    "dimension": dimension,
                                    "transformed_rank": rank,
                                    "transformed_tau": tau,
                                    "global_boundary_absolute_gap": boundary_gap,
                                    "global_boundary_relative_gap_to_first": boundary_relative_gap,
                                    "covariance_range_relative_gap_to_threshold": (
                                        covariance_range_relative_gap
                                    ),
                                    "covariance_range_owned": covariance_range_owned,
                                    "global_subspace_owned": global_subspace_owned,
                                    "range_overlap_owned": range_overlap_owned,
                                    "subspace_covariance_trace": covariance_trace,
                                    "covariance_trace_per_rank": covariance_trace / subspace_rank,
                                    "subspace_range_overlap": range_overlap,
                                    "difference_projection_norm": projection_norm,
                                    "projection_norm_to_trace_sd": ratio,
                                    "trace_sd_degenerate": degenerate,
                                })
                                covariance_row_count += 1
    os.replace(cov_temp, HERE / "R5_COVARIANCE_SUBSPACE_ATLAS.tsv")
    if covariance_row_count != 275868:
        raise AssertionError(f"covariance subspace census {covariance_row_count}")

    summary_rows = []
    for (transform_name, nside, rank_index, metric, ownership_status), values in sorted(
        summary_values.items()
    ):
        q = quantiles(values)
        summary_rows.append({
            "summary_type": "SUBSPACE",
            "transform": transform_name,
            "nside": nside,
            "rank": rank_index,
            "metric": metric,
            "ownership_status": ownership_status,
            "count": len(values),
            "min": q[0], "q25": q[1], "median": q[2], "q75": q[3],
            "q90": q[4], "q95": q[5], "max": q[6],
        })
    for (transform_name, nside), values in sorted(rank_values.items()):
        q = quantiles(values)
        summary_rows.append({
            "summary_type": "RANK",
            "transform": transform_name,
            "nside": nside,
            "rank": 0,
            "metric": "transformed_rank",
            "ownership_status": "NUMERICAL_BOOKKEEPING",
            "count": len(values),
            "min": q[0], "q25": q[1], "median": q[2], "q75": q[3],
            "q90": q[4], "q95": q[5], "max": q[6],
        })
    if len(summary_rows) != 2850:
        raise AssertionError(f"summary census {len(summary_rows)}")
    atomic_tsv(HERE / "R5_COVARIANCE_SUBSPACE_SUMMARY.tsv", summary_rows, list(summary_rows[0]))

    result = {
        "status": "ASSEMBLED__INDEPENDENT_VERIFICATION_PENDING",
        "scope": "bounded R5 data-only full-spectrum common-subspace atlas",
        "parent_curve_count": len(curves),
        "relation_count": len(relations),
        "view_spectrum_row_count": len(spectra_rows),
        "ranked_overlap_row_count": len(overlap_rows),
        "covariance_subspace_row_count": covariance_row_count,
        "covariance_summary_row_count": len(summary_rows),
        "resolved_range_overlap_row_count": resolved_range_overlap_row_count,
        "unresolved_range_overlap_row_count": unresolved_range_overlap_row_count,
        "degenerate_curve_counts": degenerate_by_transform,
        "max_basis_orthonormality_error": max_orthonormality_error,
        "theta_bin_count": len(theta_grid),
        "elapsed_seconds": time.time() - start,
        "max_rss_gib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024.0 * 1024.0),
    }
    temp_result = HERE / "R5_RESULT.json.tmp"
    temp_result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temp_result, HERE / "R5_RESULT.json")

    manifest_names = OUTPUTS[:-1]
    manifest_rows = []
    for name in manifest_names:
        path = HERE / name
        manifest_rows.append({"artifact": name, "bytes": path.stat().st_size, "sha256": digest(path)})
    atomic_tsv(HERE / "R5_OUTPUT_MANIFEST.tsv", manifest_rows, ["artifact", "bytes", "sha256"])
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
