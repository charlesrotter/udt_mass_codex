#!/usr/bin/env python3
"""Independently reproduce the load-bearing G76 external-review claims."""

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


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def solid_angle(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    numerator = np.einsum("ij,ij->i", a, np.cross(b, c))
    denominator = (
        1.0 + np.einsum("ij,ij->i", a, b)
        + np.einsum("ij,ij->i", b, c)
        + np.einsum("ij,ij->i", c, a)
    )
    return 2.0 * np.arctan2(numerator, denominator)


def bases(center: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    reference = np.zeros_like(center)
    reference[:, 2] = 1.0
    reference[np.abs(center[:, 2]) > 0.85] = np.array([0.0, 1.0, 0.0])
    e1 = np.cross(reference, center)
    e1 /= np.linalg.norm(e1, axis=1)[:, None]
    return e1, np.cross(center, e1)


def projected_face_values(vertices: np.ndarray, faces: np.ndarray, endpoint: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    source, target = vertices[faces], endpoint[faces]
    source_center, target_center = source.sum(axis=1), target.sum(axis=1)
    source_center /= np.linalg.norm(source_center, axis=1)[:, None]
    target_center /= np.linalg.norm(target_center, axis=1)[:, None]
    s1, s2 = bases(source_center)
    t1, t2 = bases(target_center)
    source_projection = source - np.einsum("fvi,fi->fv", source, source_center)[:, :, None] * source_center[:, None, :]
    target_projection = target - np.einsum("fvi,fi->fv", target, target_center)[:, :, None] * target_center[:, None, :]
    source_xy = np.stack((np.einsum("fvi,fi->fv", source_projection, s1), np.einsum("fvi,fi->fv", source_projection, s2)), axis=2)
    target_xy = np.stack((np.einsum("fvi,fi->fv", target_projection, t1), np.einsum("fvi,fi->fv", target_projection, t2)), axis=2)
    source_edges = np.stack((source_xy[:, 1] - source_xy[:, 0], source_xy[:, 2] - source_xy[:, 0]), axis=2)
    target_edges = np.stack((target_xy[:, 1] - target_xy[:, 0], target_xy[:, 2] - target_xy[:, 0]), axis=2)
    maps = target_edges @ np.linalg.inv(source_edges)
    return np.linalg.det(maps), np.linalg.svd(maps, compute_uv=False)


def main() -> None:
    manifest = rows(HERE / "REVIEW_MANIFEST.tsv")
    for row in manifest:
        path = ROOT / row["path"]
        assert path.is_file() and path.stat().st_size == int(row["size"]) and digest(path) == row["sha256"]
    atlas = rows(HERE / "WHOLE_SKY_RELATION_ATLAS.tsv")
    mesh = rows(HERE / "MESH_CONVERGENCE_ATLAS.tsv")
    saved = np.load(HERE / "SKY_ENDPOINTS.npz", allow_pickle=False)
    vertices, faces = saved["level4_directions"], saved["level4_faces"]
    input_area = solid_angle(vertices[faces[:, 0]], vertices[faces[:, 1]], vertices[faces[:, 2]])
    assert np.all(input_area > 0.0)

    degree, area_ratios, smax_values, smin_values = [], [], [], []
    negative_faces = negative_projected = near_area = 0
    for row in atlas:
        endpoint = saved[row["profile_id"] + "__endpoint"]
        output_area = solid_angle(endpoint[faces[:, 0]], endpoint[faces[:, 1]], endpoint[faces[:, 2]])
        ratio = output_area / input_area
        determinant, singular = projected_face_values(vertices, faces, endpoint)
        degree.append(float(output_area.sum() / (4.0 * math.pi)))
        area_ratios.extend((float(ratio.min()), float(ratio.max())))
        smax_values.append(float(singular[:, 0].max()))
        smin_values.append(float(singular[:, 1].min()))
        negative_faces += int(np.count_nonzero(ratio < 0.0))
        negative_projected += int(np.count_nonzero(determinant < 0.0))
        near_area += int(np.count_nonzero(np.abs(ratio) < 1.0e-2))

    classes = Counter(row["sample_class"] for row in atlas)
    unresolved = sorted(row["profile_id"] for row in atlas if row["sample_class"] == "NUMERICALLY_UNRESOLVED")
    expected_unresolved = ["G75_A0_S03_E100", "G75_AM_S03_E100", "G75_AM_S24_E100", "G75_AP_S03_E100"]
    checks = {
        "sealed_38_hashes_reproduced": len(manifest) == 38,
        "profile_and_mesh_census": len(atlas) == 591 and len(mesh) == 2364,
        "class_census": classes == Counter({"SAMPLED_COMPLETE_ORIENTATION_PRESERVING": 587, "NUMERICALLY_UNRESOLVED": 4}),
        "four_unresolved_identities": unresolved == expected_unresolved,
        "direct_area_orientation": negative_faces == 0 and near_area == 0,
        "independent_projected_tangent_orientation": negative_projected == 0,
        "degree_range_reproduced": min(degree) == 0.9999999999999999 and max(degree) == 1.0000000000000002,
        "raw_review_landing_present": "VERIFIED_WITH_CAVEATS__FULL_FAMILY_CENSUS_CONFIRMED__FOUR_ROWS_REMAIN_NUMERICALLY_UNRESOLVED" in (HERE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8"),
        "current_contract_replaces_obsolete_F01_gate": any(row["gate"] == "F01_G74_replay" for row in rows(HERE / "CURRENT_FALSIFICATION_CONTRACT.tsv")),
    }
    result = {
        "schema": "udt-cmb-g76-external-review-local-reproduction-v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "class_counts": dict(sorted(classes.items())),
        "unresolved": unresolved,
        "degree_range": [min(degree), max(degree)],
        "signed_area_ratio_range": [min(area_ratios), max(area_ratios)],
        "independent_projected_singular_value_range": [min(smin_values), max(smax_values)],
        "negative_faces": negative_faces,
        "negative_projected_face_maps": negative_projected,
        "near_area_1e2": near_area,
        "external_raw_sha256": digest(HERE / "EXTERNAL_REVIEW_RAW.md"),
        "external_transcript_sha256": digest(HERE / "EXTERNAL_REVIEW_TRANSCRIPT.txt"),
    }
    (HERE / "EXTERNAL_REVIEW_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
