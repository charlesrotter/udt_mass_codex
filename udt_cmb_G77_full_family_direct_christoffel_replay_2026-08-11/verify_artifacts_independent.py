#!/usr/bin/env python3
"""Independent raw-artifact reconstruction for the G77 direct replay."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
G75 = ROOT / "udt_cmb_G75_center_regular_axial_profile_family_2026-08-11"
G76 = ROOT / "udt_cmb_G76_complete_family_whole_sky_relation_atlas_2026-08-11"
EXPECTED_UNRESOLVED = {
    "G75_A0_S03_E100",
    "G75_AM_S03_E100",
    "G75_AM_S24_E100",
    "G75_AP_S03_E100",
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def digest(path: Path) -> str:
    block = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            block.update(chunk)
    return block.hexdigest()


def solid_angle(triangles: np.ndarray) -> np.ndarray:
    a, b, c = triangles[:, 0], triangles[:, 1], triangles[:, 2]
    triple = np.sum(a * np.cross(b, c), axis=1)
    base = 1.0 + np.sum(a * b, axis=1) + np.sum(b * c, axis=1) + np.sum(c * a, axis=1)
    return 2.0 * np.arctan2(triple, base)


def projected_ratios(source: np.ndarray, target: np.ndarray, faces: np.ndarray) -> np.ndarray:
    src, dst = source[faces], target[faces]
    src_center = np.sum(src, axis=1)
    dst_center = np.sum(dst, axis=1)
    src_center /= np.linalg.norm(src_center, axis=1)[:, None]
    dst_center /= np.linalg.norm(dst_center, axis=1)[:, None]
    src_edges = src[:, 1:] - src[:, :1]
    dst_edges = dst[:, 1:] - dst[:, :1]
    src_edges -= np.einsum("fji,fi->fj", src_edges, src_center)[:, :, None] * src_center[:, None]
    dst_edges -= np.einsum("fji,fi->fj", dst_edges, dst_center)[:, :, None] * dst_center[:, None]
    src_det = np.einsum("fi,fi->f", src_center, np.cross(src_edges[:, 0], src_edges[:, 1]))
    dst_det = np.einsum("fi,fi->f", dst_center, np.cross(dst_edges[:, 0], dst_edges[:, 1]))
    return dst_det / src_det


def expected_class(chord: float, mismatch: int, null_error: float, degree_difference: float) -> str:
    if mismatch or not math.isfinite(chord) or chord > 5.0e-5 or null_error > 2.0e-7 or degree_difference > 5.0e-4:
        return "CROSS_METHOD_NUMERICALLY_UNRESOLVED"
    if chord <= 2.0e-5:
        return "STRONG_DIRECT_AGREEMENT"
    return "REGISTERED_DIRECT_AGREEMENT"


def validate_atlas(atlas: list[dict[str, str]], expected_ids: list[str]) -> bool:
    ids = [row["profile_id"] for row in atlas]
    if ids != expected_ids or len(ids) != len(set(ids)) != 591:
        return False
    for row in atlas:
        expected = expected_class(
            float(row["direct_G76_max_chord"]),
            int(row["crossing_mask_mismatch"]),
            float(row["maximum_null_backward_error"]),
            float(row["G76_degree_difference"]),
        )
        if row["direct_class"] != expected:
            return False
    return True


def main() -> None:
    for row in read_tsv(HERE / "SOURCE_MANIFEST.tsv"):
        target = ROOT / row["path"]
        assert target.is_file() and digest(target) == row["sha256"]

    expected_ids = [row["profile_id"] for row in read_tsv(G75 / "PROFILE_ATLAS.tsv")]
    atlas = read_tsv(HERE / "DIRECT_CHRISTOFFEL_ATLAS.tsv")
    assert validate_atlas(atlas, expected_ids)
    row_by_id = {row["profile_id"]: row for row in atlas}
    reference_rows = {row["profile_id"]: row for row in read_tsv(G76 / "WHOLE_SKY_RELATION_ATLAS.tsv")}
    reference = np.load(G76 / "SKY_ENDPOINTS.npz", allow_pickle=False)
    directions = reference["level4_directions"]
    faces = reference["level4_faces"]
    endpoints = np.load(HERE / "DIRECT_ENDPOINTS.npy", mmap_mode="r")
    crossed = np.load(HERE / "DIRECT_CROSSED.npy", mmap_mode="r")
    completed = np.load(HERE / "DIRECT_COMPLETED.npy", mmap_mode="r")
    null_max = np.load(HERE / "DIRECT_NULL_MAX.npy", mmap_mode="r")
    nonfinite = np.load(HERE / "DIRECT_NONFINITE.npy", mmap_mode="r")
    active = np.load(HERE / "DIRECT_ACTIVE_REMAINING.npy", mmap_mode="r")
    assert endpoints.shape == (591, 2562, 3)
    assert crossed.shape == (591, 2562)
    assert np.all(completed) and np.all(crossed)
    assert np.all(nonfinite == 0) and np.all(active == 0)
    assert np.all(np.isfinite(endpoints))
    assert float(np.max(np.abs(np.linalg.norm(endpoints, axis=2) - 1.0))) <= 4.0e-15

    input_area = solid_angle(directions[faces])
    recomputed_classes = Counter()
    maximum_chord = 0.0
    maximum_degree_difference = 0.0
    negative_faces = 0
    negative_projected = 0
    near_area = 0
    for index, profile_id in enumerate(expected_ids):
        target = np.asarray(endpoints[index])
        target_mask = np.asarray(crossed[index])
        old_target = reference[profile_id + "__endpoint"]
        old_mask = reference[profile_id + "__crossed"]
        mismatch = int(np.count_nonzero(target_mask != old_mask))
        chord = float(np.max(np.linalg.norm(target - old_target, axis=1)))
        output_area = solid_angle(target[faces])
        ratios = output_area / input_area
        degree = float(np.sum(output_area) / (4.0 * math.pi))
        degree_difference = abs(degree - float(reference_rows[profile_id]["finest_degree_estimate"]))
        projection = projected_ratios(directions, target, faces)
        classification = expected_class(chord, mismatch, float(null_max[index]), degree_difference)
        recomputed_classes[classification] += 1
        maximum_chord = max(maximum_chord, chord)
        maximum_degree_difference = max(maximum_degree_difference, degree_difference)
        negative_faces += int(np.count_nonzero(ratios < 0.0))
        negative_projected += int(np.count_nonzero(projection < 0.0))
        near_area += int(np.count_nonzero(np.abs(ratios) < 1.0e-2))
        row = row_by_id[profile_id]
        assert row["direct_class"] == classification
        assert mismatch == int(row["crossing_mask_mismatch"])
        assert math.isclose(chord, float(row["direct_G76_max_chord"]), rel_tol=0.0, abs_tol=3.0e-15)
        assert math.isclose(degree, float(row["degree"]), rel_tol=0.0, abs_tol=3.0e-15)
        assert int(row["negative_faces"]) == int(np.count_nonzero(ratios < 0.0))
        assert int(row["negative_projected_face_maps"]) == int(np.count_nonzero(projection < 0.0))

    assert recomputed_classes == Counter({"STRONG_DIRECT_AGREEMENT": 590, "REGISTERED_DIRECT_AGREEMENT": 1})
    assert negative_faces == negative_projected == near_area == 0
    assert maximum_chord <= 5.0e-5 and maximum_degree_difference <= 5.0e-4

    refinement = read_tsv(HERE / "UNRESOLVED_REFINEMENT_ATLAS.tsv")
    assert {row["profile_id"] for row in refinement} == EXPECTED_UNRESOLVED
    refinement_saved = np.load(HERE / "UNRESOLVED_REFINEMENT_ENDPOINTS.npz", allow_pickle=False)
    index_by_id = {key: index for index, key in enumerate(expected_ids)}
    for row in refinement:
        profile_id = row["profile_id"]
        index = index_by_id[profile_id]
        endpoint_1024 = refinement_saved[profile_id + "__endpoint_1024"]
        crossed_1024 = refinement_saved[profile_id + "__crossed_1024"]
        endpoint_4096 = refinement_saved[profile_id + "__endpoint_4096"]
        crossed_4096 = refinement_saved[profile_id + "__crossed_4096"]
        assert np.all(crossed_1024) and np.all(crossed_4096)
        chord_a = float(np.max(np.linalg.norm(endpoint_1024 - endpoints[index], axis=1)))
        chord_b = float(np.max(np.linalg.norm(endpoints[index] - endpoint_4096, axis=1)))
        assert math.isclose(chord_a, float(row["direct_1024_2048_max_chord"]), rel_tol=0.0, abs_tol=3.0e-15)
        assert math.isclose(chord_b, float(row["direct_2048_4096_max_chord"]), rel_tol=0.0, abs_tol=3.0e-15)
        assert chord_b <= 5.0e-5 and row["G77_refinement_status"] == "DIRECT_TIME_REFINEMENT_RESOLVED"

    script_tree = ast.parse((HERE / "run_direct_christoffel_replay.py").read_text(encoding="utf-8"))
    imported_modules = {
        node.module
        for node in ast.walk(script_tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert "solve_complete_family" not in imported_modules

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    assert production["class_counts"] == dict(recomputed_classes)
    assert production["refinement_counts"] == {"DIRECT_TIME_REFINEMENT_RESOLVED": 4}
    result = {
        "schema": "udt-cmb-g77-independent-artifact-verification-v1",
        "status": "PASS",
        "checks": {
            "source_hashes": True,
            "exact_profile_order_and_census": True,
            "raw_checkpoint_complete": True,
            "all_1514142_rays_crossed": True,
            "all_endpoint_norms": True,
            "complete_cross_method_chord_reconstruction": True,
            "complete_face_and_projected_orientation_reconstruction": True,
            "four_row_refinement_reconstruction": True,
            "production_Hamiltonian_not_imported": True,
            "G76_history_unchanged": True,
        },
        "class_counts": dict(sorted(recomputed_classes.items())),
        "maximum_direct_G76_chord": maximum_chord,
        "maximum_degree_difference": maximum_degree_difference,
        "negative_faces_total": negative_faces,
        "negative_projected_face_maps_total": negative_projected,
        "near_area_1e2_total": near_area,
        "refined_G76_unresolved": sorted(EXPECTED_UNRESOLVED),
    }
    (HERE / "ARTIFACT_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
