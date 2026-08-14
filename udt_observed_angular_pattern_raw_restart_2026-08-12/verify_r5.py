#!/usr/bin/env python3
"""Independent SciPy replay of the corrected R5 subspace atlas."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy import linalg


HERE = Path(__file__).resolve().parent
CELLS = Path("/media/udt-admin/ScratchDisk/Data/UDT_BOSS_R3_2026-08-14/R3_COVARIANCE_CELLS")
PARENT_HASHES = {
    "R2_CURVE_ATLAS.tsv": "32b592a85cbadbc080391353be6d0ee73a2d0d8a37c10aead28e041a7810f603",
    "R4_RELATION_ATLAS.tsv": "1badac0c2eeedb2932a8d53f6116d4bfa247774c76f5750ad652da9f35696184",
    "R4_VERIFICATION_RESULT.json": "1028f4f80578995c20e5f020db4fbfafc9b73e64589e2fd055f0f3763469b05b",
    "R3_OUTPUT_MANIFEST.tsv": "3a38784ac248997bd987598308b98edbf60566759e4fdc35d54d98b161a11cfa",
}
RELATION_TYPES = (
    "RANDOM_DENSITY", "WEIGHT_LANE", "CAP", "ADJACENT_SHELL", "COARSE_FINE_CONTAINMENT"
)
RELATION_COUNTS = {
    "RANDOM_DENSITY": 1552, "WEIGHT_LANE": 1746, "CAP": 1164,
    "ADJACENT_SHELL": 2184, "COARSE_FINE_CONTAINMENT": 2640,
}
TRANSFORMS = ("CENTERED_UNIT", "FIRST_DIFFERENCE_UNIT")
LANES = ("W0_UNIT", "W1_SPECTRO", "W2_IMAGING", "W3_OFFICIAL_OBS")
NSIDES = (4, 8, 16)
EPS = np.finfo(np.float64).eps
GAP_FLOOR = np.sqrt(EPS)
OUTPUTS = (
    "R5_VIEW_SPECTRA.tsv", "R5_RANKED_SUBSPACE_OVERLAPS.tsv",
    "R5_COVARIANCE_SUBSPACE_ATLAS.tsv", "R5_COVARIANCE_SUBSPACE_SUMMARY.tsv",
    "R5_RESULT.json",
)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def rows(path: Path):
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def curve_key(row):
    return row["sample"], row["cap"], int(row["factor"]), int(row["group"]), row["lane"], int(row["ratio"])


def endpoint(text: str):
    sample, cap, factor, group, lane, ratio = text.split("|")
    return sample, cap, int(factor), int(group), lane, int(ratio)


def load_curves():
    grouped = defaultdict(list)
    grids = defaultdict(list)
    with (HERE / "R2_CURVE_ATLAS.tsv").open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            key = curve_key(row)
            grouped[key].append(float(row["w_theta"]))
            grids[key].append((float(row["theta_lo_deg"]), float(row["theta_hi_deg"])))
    assert len(grouped) == 2328
    canonical = None
    out = {}
    for key in sorted(grouped):
        assert len(grouped[key]) == 119
        grid = tuple(grids[key])
        canonical = grid if canonical is None else canonical
        assert grid == canonical
        out[key] = np.array(grouped[key], dtype=np.float64)
        assert np.all(np.isfinite(out[key]))
    return out


def transform(vector, name):
    value = vector - np.mean(vector) if name == "CENTERED_UNIT" else np.diff(vector)
    norm = linalg.norm(value)
    return np.zeros_like(value) if norm == 0.0 else value / norm


def operator(name):
    if name == "CENTERED_UNIT":
        return np.eye(119) - np.ones((119, 119)) / 119.0
    matrix = np.zeros((118, 119))
    index = np.arange(118)
    matrix[index, index] = -1.0
    matrix[index, index + 1] = 1.0
    return matrix


def selection(sample, cap, factor, group):
    return f"{sample}_{cap}_f{factor}_g{group:02d}"


def close(saved, expected, label, atol=5e-12, rtol=5e-11):
    if not np.isclose(saved, expected, atol=atol, rtol=rtol):
        raise AssertionError(f"{label}: saved={saved!r} expected={expected!r} atol={atol} rtol={rtol}")


def boundary(singular, rank):
    dimension = len(singular)
    if rank == dimension:
        gap = float(singular[-1])
        return gap, float(gap / singular[0]) if singular[0] > 0 else 0.0, True
    gap = float(singular[rank - 1] - singular[rank])
    relative = float(gap / singular[0]) if singular[0] > 0 else 0.0
    return gap, relative, relative >= GAP_FLOOR


def conditioned_tolerance(*relative_gaps):
    positive = [gap for gap in relative_gaps if gap > 0.0]
    if not positive:
        return 1.0
    return max(2e-10, 8192.0 * EPS / min(positive))


def summary_quantiles(values):
    return np.quantile(np.asarray(values, dtype=np.float64), [0, .25, .5, .75, .9, .95, 1])


def main():
    output = HERE / "R5_VERIFICATION_RESULT.json"
    if output.exists():
        raise FileExistsError(output)
    for name, expected in PARENT_HASHES.items():
        assert digest(HERE / name) == expected, name

    curves = load_curves()
    relations = rows(HERE / "R4_RELATION_ATLAS.tsv")
    assert len(relations) == 9286
    assert Counter(row["relation_type"] for row in relations) == Counter(RELATION_COUNTS)
    for index, row in enumerate(relations):
        assert int(row["relation_id"]) == index
        assert endpoint(row["curve_a"]) in curves and endpoint(row["curve_b"]) in curves
    groups = {kind: [row for row in relations if row["relation_type"] == kind] for kind in RELATION_TYPES}
    cache = {name: {key: transform(value, name) for key, value in curves.items()} for name in TRANSFORMS}

    saved_spectra_rows = rows(HERE / "R5_VIEW_SPECTRA.tsv")
    assert len(saved_spectra_rows) == 2607
    saved_spectra = {
        (row["transform"], row["view"], int(row["mode_index"])): row for row in saved_spectra_rows
    }
    assert len(saved_spectra) == 2607
    global_keys = sorted(curves)
    bases = {}
    singulars = {}
    max_singular_difference = 0.0
    for transform_name in TRANSFORMS:
        view_keys = {"GLOBAL": global_keys}
        for kind in RELATION_TYPES:
            view_keys[f"{kind}_A"] = [endpoint(row["curve_a"]) for row in groups[kind]]
            view_keys[f"{kind}_B"] = [endpoint(row["curve_b"]) for row in groups[kind]]
        for view_name, keys in view_keys.items():
            matrix = np.vstack([cache[transform_name][key] for key in keys])
            _, singular, vt = linalg.svd(matrix, full_matrices=False, lapack_driver="gesvd")
            bases[(transform_name, view_name)] = vt
            singulars[(transform_name, view_name)] = singular
            energy = np.sum(singular * singular)
            cumulative = 0.0
            for offset, value in enumerate(singular):
                mode = offset + 1
                row = saved_spectra[(transform_name, view_name, mode)]
                assert int(row["row_count"]) == len(keys)
                assert int(row["dimension"]) == matrix.shape[1]
                next_value = float(singular[mode]) if mode < len(singular) else 0.0
                gap = float(value - next_value)
                fraction = float(value * value / energy)
                cumulative += fraction
                max_singular_difference = max(max_singular_difference, abs(float(row["singular_value"]) - value))
                close(float(row["singular_value"]), value, f"spectrum/{transform_name}/{view_name}/{mode}")
                close(float(row["next_singular_value"]), next_value, "next singular")
                close(float(row["boundary_absolute_gap"]), gap, "spectrum gap")
                close(float(row["boundary_relative_gap_to_first"]), gap / singular[0], "relative gap")
                close(float(row["squared_energy_fraction"]), fraction, "energy fraction")
                close(float(row["cumulative_squared_energy_fraction"]), cumulative, "cumulative energy")
                close(float(row["singular_relative_to_first"]), value / singular[0], "relative singular")

    saved_overlap_rows = rows(HERE / "R5_RANKED_SUBSPACE_OVERLAPS.tsv")
    assert len(saved_overlap_rows) == 3555
    saved_overlaps = {
        (row["transform"], row["pair_id"], int(row["rank"])): row for row in saved_overlap_rows
    }
    assert len(saved_overlaps) == 3555
    resolved_overlap_rows = 0
    unresolved_overlap_rows = 0
    max_resolved_overlap_difference = 0.0
    max_overlap_tolerance = 0.0
    for transform_name in TRANSFORMS:
        specs = []
        for kind in RELATION_TYPES:
            specs.append((f"{kind}__A_VS_B", f"{kind}_A", f"{kind}_B"))
        for kind in RELATION_TYPES:
            specs.append((f"GLOBAL_VS_{kind}_A", "GLOBAL", f"{kind}_A"))
            specs.append((f"GLOBAL_VS_{kind}_B", "GLOBAL", f"{kind}_B"))
        for pair_id, view_a, view_b in specs:
            va = bases[(transform_name, view_a)]
            vb = bases[(transform_name, view_b)]
            gram = np.square(va @ vb.T)
            sa = singulars[(transform_name, view_a)]
            sb = singulars[(transform_name, view_b)]
            dimension = len(sa)
            for rank in range(1, dimension + 1):
                row = saved_overlaps[(transform_name, pair_id, rank)]
                assert row["view_a"] == view_a and row["view_b"] == view_b
                gap_a, relative_a, owned_a = boundary(sa, rank)
                gap_b, relative_b, owned_b = boundary(sb, rank)
                close(float(row["view_a_boundary_absolute_gap"]), gap_a, "view A gap")
                close(float(row["view_b_boundary_absolute_gap"]), gap_b, "view B gap")
                close(float(row["view_a_boundary_relative_gap_to_first"]), relative_a, "view A rel gap")
                close(float(row["view_b_boundary_relative_gap_to_first"]), relative_b, "view B rel gap")
                saved_overlap = float(row["projector_overlap"])
                saved_chord = float(row["normalized_chord_distance"])
                saved_smallest = float(row["smallest_principal_cosine"])
                assert np.isfinite([saved_overlap, saved_chord, saved_smallest]).all()
                assert -5e-12 <= saved_overlap <= 1.0 + 5e-12
                close(
                    saved_chord,
                    float(np.sqrt(max(0.0, 1.0 - saved_overlap))),
                    f"saved chord transform/{transform_name}/{pair_id}/{rank}",
                    atol=5e-15,
                    rtol=5e-13,
                )
                if rank == dimension:
                    close(saved_overlap, 1.0, "full overlap", atol=5e-12, rtol=0.0)
                if owned_a and owned_b:
                    overlap = float(np.sum(gram[:rank, :rank]) / rank)
                    smallest = float(linalg.svdvals(va[:rank] @ vb[:rank].T)[-1])
                    tolerance = conditioned_tolerance(relative_a, relative_b)
                    max_overlap_tolerance = max(max_overlap_tolerance, tolerance)
                    max_resolved_overlap_difference = max(
                        max_resolved_overlap_difference,
                        abs(saved_overlap - overlap), abs(saved_smallest - smallest),
                    )
                    close(saved_overlap, overlap, "resolved overlap", atol=tolerance, rtol=tolerance)
                    close(saved_smallest, smallest, "resolved smallest cosine", atol=tolerance, rtol=tolerance)
                    resolved_overlap_rows += 1
                else:
                    unresolved_overlap_rows += 1

    cap20 = {}
    for row in groups["CAP"]:
        if int(row["ratio_a"]) == 20 and int(row["ratio_b"]) == 20:
            key = (row["sample"], int(row["factor_a"]), int(row["group_a"]), row["lane_a"])
            assert key not in cap20
            cap20[key] = endpoint(row["curve_a"]), endpoint(row["curve_b"])
    assert len(cap20) == 388
    context_groups = defaultdict(list)
    for key, value in cap20.items():
        context_groups[key[:3]].append((key[3], value))
    assert len(context_groups) == 97

    saved_summary_values = defaultdict(list)
    saved_rank_values = defaultdict(list)
    covariance_core_resolved = 0
    covariance_core_unresolved = 0
    range_resolved = 0
    range_unresolved = 0
    max_resolved_covariance_difference = 0.0
    max_covariance_tolerance = 0.0
    covariance_count = 0
    with (HERE / "R5_COVARIANCE_SUBSPACE_ATLAS.tsv").open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for (sample, factor, group), lane_entries in sorted(context_groups.items()):
            north_name = selection(sample, "North", factor, group)
            south_name = selection(sample, "South", factor, group)
            with np.load(CELLS / f"{north_name}.npz", allow_pickle=False) as nc, np.load(
                CELLS / f"{south_name}.npz", allow_pickle=False
            ) as sc:
                assert json.loads(str(nc["metadata"].item()))["selection_key"] == north_name
                assert json.loads(str(sc["metadata"].item()))["selection_key"] == south_name
                for lane, (north_key, south_key) in sorted(lane_entries):
                    lane_index = LANES.index(lane)
                    difference = curves[north_key] - curves[south_key]
                    for nside in NSIDES:
                        covariance = np.array(nc[f"covariance_n{nside}"][lane_index], dtype=np.float64, copy=True)
                        covariance += np.array(sc[f"covariance_n{nside}"][lane_index], dtype=np.float64, copy=False)
                        for transform_name in TRANSFORMS:
                            linear = operator(transform_name)
                            transformed_difference = linear @ difference
                            transformed_covariance = linear @ covariance @ linear.T
                            transformed_covariance = (transformed_covariance + transformed_covariance.T) / 2.0
                            eigenvalues, eigenvectors = linalg.eigh(transformed_covariance, driver="evr")
                            dimension = len(eigenvalues)
                            largest = max(0.0, float(eigenvalues[-1]))
                            tau = dimension * EPS * largest
                            positive = eigenvalues > tau
                            covariance_rank = int(np.sum(positive))
                            if covariance_rank in (0, dimension):
                                range_owned = True
                                range_relative_gap = 1.0
                            else:
                                positive_min = float(eigenvalues[-covariance_rank])
                                nonpositive_max = float(eigenvalues[-covariance_rank - 1])
                                range_relative_gap = min(positive_min - tau, tau - nonpositive_max) / max(largest, EPS)
                                range_owned = range_relative_gap >= GAP_FLOOR
                            basis = bases[(transform_name, "GLOBAL")]
                            singular = singulars[(transform_name, "GLOBAL")]
                            variances = np.maximum(
                                np.einsum("ij,jk,ik->i", basis, transformed_covariance, basis), 0.0
                            )
                            projection_squares = np.square(basis @ transformed_difference)
                            range_components = (
                                np.sum(np.square(basis @ eigenvectors[:, positive]), axis=1)
                                if covariance_rank else np.zeros(dimension)
                            )
                            cumulative_variance = np.cumsum(variances)
                            cumulative_projection = np.cumsum(projection_squares)
                            cumulative_range = np.cumsum(range_components)
                            for offset in range(dimension):
                                rank = offset + 1
                                row = next(reader, None)
                                assert row is not None
                                assert int(row["covariance_id"]) == covariance_count
                                assert (row["sample"], int(row["factor"]), int(row["group"]), row["lane"], int(row["nside"]), row["transform"], int(row["rank"])) == (
                                    sample, factor, group, lane, nside, transform_name, rank
                                )
                                assert int(row["dimension"]) == dimension
                                assert int(row["transformed_rank"]) == covariance_rank
                                close(float(row["transformed_tau"]), tau, "transformed tau", atol=5e-12, rtol=5e-11)
                                gap, relative_gap, globally_owned = boundary(singular, rank)
                                close(float(row["global_boundary_absolute_gap"]), gap, "global covariance gap")
                                close(float(row["global_boundary_relative_gap_to_first"]), relative_gap, "global rel gap")
                                trace = float(cumulative_variance[offset])
                                trace_per_rank = trace / rank
                                projection_norm = float(np.sqrt(cumulative_projection[offset]))
                                range_overlap_value = float(cumulative_range[offset] / rank)
                                trace_sd = float(np.sqrt(trace))
                                ratio = projection_norm / trace_sd if trace_sd > 0.0 else 0.0
                                saved = {
                                    "subspace_covariance_trace": float(row["subspace_covariance_trace"]),
                                    "covariance_trace_per_rank": float(row["covariance_trace_per_rank"]),
                                    "subspace_range_overlap": float(row["subspace_range_overlap"]),
                                    "difference_projection_norm": float(row["difference_projection_norm"]),
                                    "projection_norm_to_trace_sd": float(row["projection_norm_to_trace_sd"]),
                                }
                                assert np.isfinite(list(saved.values())).all()
                                assert -5e-12 <= saved["subspace_range_overlap"] <= 1.0 + 5e-12
                                for metric in (
                                    "covariance_trace_per_rank", "subspace_range_overlap",
                                    "difference_projection_norm", "projection_norm_to_trace_sd",
                                ):
                                    saved_summary_values[(transform_name, nside, rank, metric)].append(saved[metric])
                                if rank == 1:
                                    saved_rank_values[(transform_name, nside)].append(float(covariance_rank))
                                if globally_owned:
                                    tolerance = conditioned_tolerance(relative_gap)
                                    max_covariance_tolerance = max(max_covariance_tolerance, tolerance)
                                    direct_expected = {
                                        "subspace_covariance_trace": trace,
                                        "covariance_trace_per_rank": trace_per_rank,
                                        "difference_projection_norm": projection_norm,
                                        "projection_norm_to_trace_sd": ratio,
                                    }
                                    for metric, expected in direct_expected.items():
                                        max_resolved_covariance_difference = max(
                                            max_resolved_covariance_difference, abs(saved[metric] - expected)
                                        )
                                        close(saved[metric], expected, f"resolved covariance/{metric}",
                                              atol=tolerance, rtol=tolerance)
                                    covariance_core_resolved += 1
                                else:
                                    covariance_core_unresolved += 1
                                if globally_owned and range_owned:
                                    tolerance = conditioned_tolerance(relative_gap, range_relative_gap)
                                    max_covariance_tolerance = max(max_covariance_tolerance, tolerance)
                                    max_resolved_covariance_difference = max(
                                        max_resolved_covariance_difference,
                                        abs(saved["subspace_range_overlap"] - range_overlap_value),
                                    )
                                    close(saved["subspace_range_overlap"], range_overlap_value,
                                          "resolved range overlap", atol=tolerance, rtol=tolerance)
                                    range_resolved += 1
                                else:
                                    range_unresolved += 1
                                assert int(row["trace_sd_degenerate"]) == int(trace_sd == 0.0)
                                covariance_count += 1
        assert next(reader, None) is None
    assert covariance_count == 275868

    saved_summary_rows = rows(HERE / "R5_COVARIANCE_SUBSPACE_SUMMARY.tsv")
    assert len(saved_summary_rows) == 2850
    expected_summaries = {}
    for key, values in saved_summary_values.items():
        expected_summaries[("SUBSPACE", key[0], key[1], key[2], key[3])] = (len(values), summary_quantiles(values))
    for key, values in saved_rank_values.items():
        expected_summaries[("RANK", key[0], key[1], 0, "transformed_rank")] = (
            len(values), summary_quantiles(values)
        )
    assert len(expected_summaries) == 2850
    summary_fields = ("min", "q25", "median", "q75", "q90", "q95", "max")
    for row in saved_summary_rows:
        key = (row["summary_type"], row["transform"], int(row["nside"]), int(row["rank"]), row["metric"])
        count, expected = expected_summaries.pop(key)
        assert int(row["count"]) == count
        for field, value in zip(summary_fields, expected):
            close(float(row[field]), float(value), f"summary/{key}/{field}", atol=5e-14, rtol=5e-13)
    assert not expected_summaries

    manifest_rows = rows(HERE / "R5_OUTPUT_MANIFEST.tsv")
    assert len(manifest_rows) == len(OUTPUTS)
    assert {row["artifact"] for row in manifest_rows} == set(OUTPUTS)
    for row in manifest_rows:
        path = HERE / row["artifact"]
        assert path.stat().st_size == int(row["bytes"])
        assert digest(path) == row["sha256"]
    result = json.loads((HERE / "R5_RESULT.json").read_text())
    assert result["status"] == "ASSEMBLED__INDEPENDENT_VERIFICATION_PENDING"
    assert result["view_spectrum_row_count"] == 2607
    assert result["ranked_overlap_row_count"] == 3555
    assert result["covariance_subspace_row_count"] == 275868
    assert result["covariance_summary_row_count"] == 2850

    payload = {
        "status": "PASS",
        "verifier": "independent scipy-gesvd/scipy-evr replay with gap-conditioned projector ownership",
        "view_spectrum_row_count": 2607,
        "ranked_overlap_row_count": 3555,
        "covariance_subspace_row_count": 275868,
        "covariance_summary_row_count": 2850,
        "resolved_overlap_row_count": resolved_overlap_rows,
        "unresolved_overlap_row_count": unresolved_overlap_rows,
        "resolved_covariance_core_row_count": covariance_core_resolved,
        "unresolved_covariance_core_row_count": covariance_core_unresolved,
        "resolved_range_overlap_row_count": range_resolved,
        "unresolved_range_overlap_row_count": range_unresolved,
        "max_singular_value_abs_difference": max_singular_difference,
        "max_resolved_overlap_field_abs_difference": max_resolved_overlap_difference,
        "max_resolved_covariance_field_abs_difference": max_resolved_covariance_difference,
        "max_gap_conditioned_overlap_tolerance": max_overlap_tolerance,
        "max_gap_conditioned_covariance_tolerance": max_covariance_tolerance,
        "gap_floor": float(GAP_FLOOR),
        "scope": "bounded R5 data-only atlas; ambiguous spectral boundaries retained but not independently certified",
    }
    temp = output.with_suffix(".json.tmp")
    temp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temp, output)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
