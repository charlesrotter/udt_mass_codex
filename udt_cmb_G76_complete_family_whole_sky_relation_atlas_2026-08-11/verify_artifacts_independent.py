#!/usr/bin/env python3
"""Fail-closed structural and numerical verification of the saved G76 atlas."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ATLAS = HERE / "WHOLE_SKY_RELATION_ATLAS.tsv"
MESH = HERE / "MESH_CONVERGENCE_ATLAS.tsv"
ENDPOINTS = HERE / "SKY_ENDPOINTS.npz"
RESULT = HERE / "DERIVATION_RESULT.json"
G75 = ROOT / "udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/PROFILE_ATLAS.tsv"
G74 = ROOT / "udt_cmb_G74_symbolic_sky_relation_topology_atlas_2026-08-11/SKY_ENDPOINTS.npz"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expected_class(row: dict[str, str]) -> str:
    resolved = (
        float(row["time_refinement_endpoint_max_chord"]) <= 5.0e-5
        and int(row["time_refinement_mask_mismatch"]) == 0
        and float(row["mesh_degree_drift_level3_to4"]) <= 5.0e-4
        and float(row["max_abs_hamiltonian"]) <= 1.0e-6
        and int(row["reflection_mask_mismatch"]) == 0
        and float(row["reflection_max_chord"]) <= 2.0e-5
    )
    if not resolved:
        return "NUMERICALLY_UNRESOLVED"
    if int(row["finest_missing_vertices"]) or int(row["finest_nonfinite_count"]):
        return "SAMPLED_MISSING_OR_MULTIBRANCH_CANDIDATE"
    if int(row["finest_negative_faces"]) or int(row["finest_negative_intrinsic_face_maps"]):
        return "SAMPLED_ORIENTATION_REVERSING_OR_FOLD_CANDIDATE"
    return "SAMPLED_COMPLETE_ORIENTATION_PRESERVING"


def verify_atlas(atlas: list[dict[str, str]], mesh: list[dict[str, str]]) -> dict[str, object]:
    expected_ids = [row["profile_id"] for row in rows(G75)]
    ids = [row["profile_id"] for row in atlas]
    assert len(ids) == len(set(ids)) == len(expected_ids) == 591
    assert set(ids) == set(expected_ids)
    assert all(row["sample_class"] == expected_class(row) for row in atlas)

    mesh_keys = Counter((row["profile_id"], int(row["level"]), int(row["steps"])) for row in mesh)
    expected_trials = {(level, step) for level, step in ((2, 1024), (3, 1024), (4, 512), (4, 1024))}
    assert len(mesh) == 2364 and all(value == 1 for value in mesh_keys.values())
    for profile_id in ids:
        assert {(level, step) for pid, level, step in mesh_keys if pid == profile_id} == expected_trials

    classes = Counter(row["sample_class"] for row in atlas)
    assert classes == Counter({"SAMPLED_COMPLETE_ORIENTATION_PRESERVING": 587, "NUMERICALLY_UNRESOLVED": 4})
    unresolved = {row["profile_id"] for row in atlas if row["sample_class"] == "NUMERICALLY_UNRESOLVED"}
    assert unresolved == {"G75_AM_S03_E100", "G75_A0_S03_E100", "G75_AP_S03_E100", "G75_AM_S24_E100"}
    assert all(
        float(row["time_refinement_endpoint_max_chord"]) > 5.0e-5
        and float(row["mesh_degree_drift_level3_to4"]) <= 5.0e-4
        and float(row["max_abs_hamiltonian"]) <= 1.0e-6
        and int(row["reflection_mask_mismatch"]) == 0
        for row in atlas if row["profile_id"] in unresolved
    )
    assert sum(int(row["finest_missing_vertices"]) for row in atlas) == 0
    assert sum(int(row["finest_nonfinite_count"]) for row in atlas) == 0
    assert sum(int(row["finest_negative_faces"]) for row in atlas) == 0
    assert sum(int(row["finest_negative_intrinsic_face_maps"]) for row in atlas) == 0
    assert sum(int(row["finest_near_area_1e2"]) for row in atlas) == 0
    assert all(abs(float(row["finest_degree_estimate"]) - 1.0) <= 5.0e-13 for row in atlas)
    return {"classes": dict(sorted(classes.items())), "unresolved": sorted(unresolved)}


def verify_endpoints(atlas: list[dict[str, str]]) -> dict[str, object]:
    saved = np.load(ENDPOINTS, allow_pickle=False)
    expected_keys = {"level4_directions", "level4_faces"}
    for row in atlas:
        pid = row["profile_id"]
        expected_keys.update(
            pid + suffix for suffix in ("__endpoint", "__endpoint_t", "__endpoint_affine", "__crossed", "__turns")
        )
    assert set(saved.files) == expected_keys
    directions = saved["level4_directions"]
    faces = saved["level4_faces"]
    assert directions.shape == (2562, 3) and faces.shape == (5120, 3)
    assert np.max(np.abs(np.linalg.norm(directions, axis=1) - 1.0)) <= 2.0e-15
    for row in atlas:
        pid = row["profile_id"]
        endpoint = saved[pid + "__endpoint"]
        crossed = saved[pid + "__crossed"]
        assert endpoint.shape == (2562, 3) and crossed.shape == (2562,)
        assert np.all(crossed) and np.all(np.isfinite(endpoint))
        assert np.max(np.abs(np.linalg.norm(endpoint, axis=1) - 1.0)) <= 3.0e-15
    return {"key_count": len(saved.files), "directions": len(directions), "faces": len(faces)}


def verify_g74(atlas: list[dict[str, str]]) -> dict[str, object]:
    current = np.load(ENDPOINTS, allow_pickle=False)
    frozen = np.load(G74, allow_pickle=False)
    replay = [row for row in atlas if row["G74_regression_profile"] != "-"]
    assert len(replay) == 9
    maximum = 0.0
    for row in replay:
        old_name = row["G74_regression_profile"]
        difference = np.linalg.norm(current[row["profile_id"] + "__endpoint"] - frozen[old_name + "__endpoint"], axis=1)
        value = float(np.max(difference))
        maximum = max(maximum, value)
        assert value <= 5.0e-6 and int(row["G74_regression_mask_mismatch"]) == 0
        assert math.isclose(value, float(row["G74_regression_max_chord"]), rel_tol=0.0, abs_tol=1.0e-15)
    return {"rows": len(replay), "maximum_chord": maximum}


def main() -> None:
    source_rows = rows(HERE / "SOURCE_MANIFEST.tsv")
    for row in source_rows:
        path = ROOT / row["path"]
        assert path.is_file() and sha256(path) == row["sha256"]
    atlas, mesh = rows(ATLAS), rows(MESH)
    atlas_result = verify_atlas(atlas, mesh)
    endpoint_result = verify_endpoints(atlas)
    g74_result = verify_g74(atlas)
    production = json.loads(RESULT.read_text(encoding="utf-8"))
    assert production["profile_count"] == 591 and production["mesh_trial_rows"] == 2364
    assert production["sample_class_counts"] == atlas_result["classes"]
    assert production["protected_draft_read"] is False
    assert production["physical_owner"] == "OPEN_NO_OWNER"
    checks = {
        "source_hashes": True,
        "profile_census_and_exact_classes": True,
        "mesh_trial_census": True,
        "endpoint_archive_shapes_and_norms": True,
        "four_unresolved_rows_not_promoted": True,
        "all_sampled_crossings_complete": True,
        "no_sampled_negative_or_near_zero_faces": True,
        "G74_nine_profile_replay": True,
        "no_physical_owner_claimed": True,
    }
    result = {
        "schema": "udt-cmb-g76-independent-artifact-verification-v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "atlas": atlas_result,
        "endpoints": endpoint_result,
        "G74": g74_result,
        "source_manifest_rows": len(source_rows),
    }
    (HERE / "ARTIFACT_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
