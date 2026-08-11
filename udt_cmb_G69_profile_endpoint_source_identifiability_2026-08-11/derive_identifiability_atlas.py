#!/usr/bin/env python3
"""Build the preregistered G69 identifiability atlas from frozen G68 path samples."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy.interpolate import PchipInterpolator


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
G68 = ROOT / "udt_cmb_G68_F01_F02_finite_path_jacobi_controls_2026-08-11"
ENDPOINTS = np.round(np.arange(0.30, 1.0001, 0.05), 2)
SENSITIVITY_ENDPOINTS = (0.35, 0.50, 0.65, 0.80, 0.95)
SHAPES = ("PERSISTENT", "TAPERED", "SIGN_CHANGING")
COVARIANCES = {
    "IDENTITY": np.eye(2),
    "DIAGONAL_2_1": np.diag([2.0, 1.0]),
    "CORRELATED": np.array([[2.0, 1.0 / 3.0], [1.0 / 3.0, 1.0]]),
}


def parse_fraction(value: str) -> float:
    if "/" in value:
        left, right = value.split("/", 1)
        return float(left) / float(right)
    return float(value)


def load_profiles() -> list[dict[str, object]]:
    with (G68 / "PROFILE_UNIVERSE.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    profiles = []
    for row in rows:
        profiles.append(
            {
                "profile_id": row["profile_id"],
                "family": row["metric_family"],
                "lapse_a": parse_fraction(row["lapse_a"]),
                "shape": row["mix_shape"],
                "epsilon": parse_fraction(row["mix_epsilon"]),
            }
        )
    assert len(profiles) == len({row["profile_id"] for row in profiles}) == 21
    return profiles


def h_value(profile: dict[str, object], r: float) -> float:
    epsilon = float(profile["epsilon"])
    shape = str(profile["shape"])
    if profile["family"] == "F01" or shape == "ZERO":
        return 0.0
    if shape == "PERSISTENT":
        return epsilon * r**2
    if shape == "TAPERED":
        return epsilon * r**2 * (1.0 - r) ** 2
    if shape == "SIGN_CHANGING":
        return epsilon * r**2 * (1.0 - 2.0 * r)
    raise ValueError(shape)


def metric(profile: dict[str, object], position: np.ndarray) -> np.ndarray:
    _, r, theta, _ = position
    r = float(r)
    sine2 = math.sin(float(theta)) ** 2
    A = 1.0 + float(profile["lapse_a"]) * r * r
    h = h_value(profile, r)
    g = np.zeros((4, 4), dtype=np.float64)
    g[0, 0] = -A
    g[1, 1] = 1.0 / A
    g[2, 2] = r * r
    g[3, 3] = r * r * sine2
    g[0, 3] = g[3, 0] = h * sine2
    return g


def jacobi_map(profile: dict[str, object], state: np.ndarray) -> np.ndarray:
    position = state[0:4]
    screen = state[8:16].reshape(2, 4)
    jacobi = state[16:24].reshape(2, 4)
    return screen @ metric(profile, position) @ jacobi.T


def relative(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.linalg.norm(left - right) / max(1.0, np.linalg.norm(left), np.linalg.norm(right)))


def official_endpoints() -> dict[str, np.ndarray]:
    with (G68 / "FINITE_PATH_ATLAS.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    return {
        row["profile_id"]: np.array(
            [
                [float(row["D_theta_theta"]), float(row["D_theta_psi"])],
                [float(row["D_psi_theta"]), float(row["D_psi_psi"])],
            ]
        )
        for row in rows
    }


def interpolate_cells(profiles: list[dict[str, object]]) -> list[dict[str, object]]:
    archive = np.load(G68 / "FINITE_PATH_SAMPLES.npz")
    official = official_endpoints()
    rows: list[dict[str, object]] = []
    for profile in profiles:
        profile_id = str(profile["profile_id"])
        affine_saved = np.asarray(archive[profile_id + "__s"], dtype=np.float64)
        state_saved = np.asarray(archive[profile_id + "__state"], dtype=np.float64)
        radius_saved = state_saved[1]
        assert np.all(np.diff(radius_saved) > 0.0)
        state_interp = PchipInterpolator(radius_saved, state_saved.T, axis=0)
        affine_interp = PchipInterpolator(radius_saved, affine_saved)
        for x in ENDPOINTS:
            state = np.asarray(state_interp(float(x)), dtype=np.float64)
            affine = float(affine_interp(float(x)))
            D = jacobi_map(profile, state)
            singular = np.linalg.svd(D, compute_uv=False)
            polar_u, _, polar_vt = np.linalg.svd(D)
            polar = polar_u @ polar_vt
            rows.append(
                {
                    **profile,
                    "endpoint_x": float(x),
                    "affine": affine,
                    "endpoint_psi": float(state[3]),
                    "D": D,
                    "det_D": float(np.linalg.det(D)),
                    "sigma_max": float(singular[0]),
                    "sigma_min": float(singular[-1]),
                    "anisotropy_log": float(math.log(singular[0] / singular[-1])),
                    "polar_rotation": float(math.atan2(float(polar[1, 0]), float(polar[0, 0]))),
                    "x1_official_relative": relative(D, official[profile_id]) if x == 1.0 else math.nan,
                }
            )
    f01_affine = {
        (float(row["lapse_a"]), float(row["endpoint_x"])): float(row["affine"])
        for row in rows
        if row["family"] == "F01"
    }
    for row in rows:
        reference = f01_affine[(float(row["lapse_a"]), float(row["endpoint_x"]))]
        ratio = float(row["det_D"]) / (reference * reference)
        row["area_ratio_vs_F01"] = ratio
        row["area_log_vs_F01"] = float(math.log(ratio))
    return rows


def readout(row: dict[str, object]) -> np.ndarray:
    return np.array(
        [float(row["area_log_vs_F01"]), float(row["anisotropy_log"]), float(row["endpoint_psi"])],
        dtype=np.float64,
    )


def sensitivity_rows(cells: list[dict[str, object]]) -> list[dict[str, object]]:
    lookup = {
        (
            str(row["shape"]),
            float(row["lapse_a"]),
            float(row["epsilon"]),
            round(float(row["endpoint_x"]), 2),
        ): row
        for row in cells
        if row["family"] == "F02"
    }
    outputs = []
    for shape in SHAPES:
        for x in SENSITIVITY_ENDPOINTS:
            endpoint_columns = []
            lapse_columns = []
            for epsilon in (0.05, 0.20):
                endpoint_columns.append(
                    (readout(lookup[(shape, 0.0, epsilon, round(x + 0.05, 2))])
                     - readout(lookup[(shape, 0.0, epsilon, round(x - 0.05, 2))]))
                    / 0.10
                )
                lapse_columns.append(
                    (readout(lookup[(shape, 0.25, epsilon, round(x, 2))])
                     - readout(lookup[(shape, -0.25, epsilon, round(x, 2))]))
                    / 0.50
                )
            endpoint_column = 0.5 * (endpoint_columns[0] + endpoint_columns[1])
            lapse_column = 0.5 * (lapse_columns[0] + lapse_columns[1])
            amplitude_column = (
                readout(lookup[(shape, 0.0, 0.20, round(x, 2))])
                - readout(lookup[(shape, 0.0, 0.05, round(x, 2))])
            ) / 0.15
            matrix = np.column_stack((endpoint_column, lapse_column, amplitude_column))
            norms = np.linalg.norm(matrix, axis=0)
            if np.any(norms == 0.0):
                normalized = np.zeros_like(matrix)
                singular = np.array([math.inf, 0.0, 0.0])
                condition = math.inf
                ratio = 0.0
            else:
                normalized = matrix / norms
                singular = np.linalg.svd(normalized, compute_uv=False)
                condition = float(singular[0] / singular[-1])
                ratio = float(singular[-1] / singular[0])
            if ratio >= 1.0e-6:
                classification = "FULL_RANK_OBSERVED"
            elif ratio <= 1.0e-8:
                classification = "RANK_DEFICIENT_OBSERVED"
            else:
                classification = "RANK_NUMERICALLY_UNRESOLVED"
            outputs.append(
                {
                    "shape": shape,
                    "endpoint_x": x,
                    "matrix": matrix,
                    "determinant": float(np.linalg.det(matrix)),
                    "column_norms": norms,
                    "normalized_singular_values": singular,
                    "normalized_condition": condition,
                    "sigma_ratio": ratio,
                    "classification": classification,
                }
            )
    return outputs


def covariance_rows(cells: list[dict[str, object]]) -> list[dict[str, object]]:
    outputs = []
    for row in cells:
        D = np.asarray(row["D"], dtype=np.float64)
        inverse = np.linalg.inv(D)
        for covariance_id, observed in COVARIANCES.items():
            source = inverse @ observed @ inverse.T
            reconstructed = D @ source @ D.T
            outputs.append(
                {
                    "profile_id": row["profile_id"],
                    "endpoint_x": row["endpoint_x"],
                    "covariance_id": covariance_id,
                    "source": source,
                    "reconstruction_relative": relative(reconstructed, observed),
                    "source_min_eigenvalue": float(np.linalg.eigvalsh(source)[0]),
                }
            )
    return outputs


def write_cell_atlas(rows: list[dict[str, object]]) -> None:
    fields = [
        "profile_id", "family", "lapse_a", "shape", "epsilon", "endpoint_x", "affine",
        "endpoint_psi", "D00", "D01", "D10", "D11", "det_D", "sigma_max", "sigma_min",
        "anisotropy_log", "polar_rotation", "area_ratio_vs_F01", "area_log_vs_F01",
        "x1_official_relative",
    ]
    with (HERE / "CELL_ATLAS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            D = np.asarray(row["D"])
            out = {key: row[key] for key in fields if key not in {"D00", "D01", "D10", "D11"}}
            out.update(D00=D[0, 0], D01=D[0, 1], D10=D[1, 0], D11=D[1, 1])
            writer.writerow(out)


def write_sensitivity_atlas(rows: list[dict[str, object]]) -> None:
    fields = [
        "shape", "endpoint_x", "m00", "m01", "m02", "m10", "m11", "m12", "m20", "m21",
        "m22", "determinant", "column_norm_x", "column_norm_a", "column_norm_epsilon",
        "normalized_sigma_max", "normalized_sigma_mid", "normalized_sigma_min",
        "normalized_condition", "sigma_ratio", "classification",
    ]
    with (HERE / "SENSITIVITY_ATLAS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            matrix = np.asarray(row["matrix"])
            singular = np.asarray(row["normalized_singular_values"])
            norms = np.asarray(row["column_norms"])
            out = {"shape": row["shape"], "endpoint_x": row["endpoint_x"]}
            out.update({f"m{i}{j}": matrix[i, j] for i in range(3) for j in range(3)})
            out.update(
                determinant=row["determinant"],
                column_norm_x=norms[0], column_norm_a=norms[1], column_norm_epsilon=norms[2],
                normalized_sigma_max=singular[0], normalized_sigma_mid=singular[1],
                normalized_sigma_min=singular[2], normalized_condition=row["normalized_condition"],
                sigma_ratio=row["sigma_ratio"], classification=row["classification"],
            )
            writer.writerow(out)


def write_covariance_atlas(rows: list[dict[str, object]]) -> None:
    fields = [
        "profile_id", "endpoint_x", "covariance_id", "Csrc00", "Csrc01", "Csrc10", "Csrc11",
        "reconstruction_relative", "source_min_eigenvalue",
    ]
    with (HERE / "SOURCE_DEGENERACY_ATLAS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            source = np.asarray(row["source"])
            writer.writerow(
                {
                    "profile_id": row["profile_id"], "endpoint_x": row["endpoint_x"],
                    "covariance_id": row["covariance_id"], "Csrc00": source[0, 0],
                    "Csrc01": source[0, 1], "Csrc10": source[1, 0], "Csrc11": source[1, 1],
                    "reconstruction_relative": row["reconstruction_relative"],
                    "source_min_eigenvalue": row["source_min_eigenvalue"],
                }
            )


def main() -> None:
    profiles = load_profiles()
    cells = interpolate_cells(profiles)
    sensitivities = sensitivity_rows(cells)
    covariances = covariance_rows(cells)
    write_cell_atlas(cells)
    write_sensitivity_atlas(sensitivities)
    write_covariance_atlas(covariances)

    endpoint_error = max(float(row["x1_official_relative"]) for row in cells if row["endpoint_x"] == 1.0)
    f01_anisotropy = max(float(row["anisotropy_log"]) for row in cells if row["family"] == "F01")
    f01_rotation = max(abs(float(row["polar_rotation"])) for row in cells if row["family"] == "F01")
    min_sigma = min(float(row["sigma_min"]) for row in cells)
    source_error = max(float(row["reconstruction_relative"]) for row in covariances)
    source_min_eigenvalue = min(float(row["source_min_eigenvalue"]) for row in covariances)
    rank_counts: dict[str, int] = {}
    for row in sensitivities:
        rank_counts[str(row["classification"])] = rank_counts.get(str(row["classification"]), 0) + 1

    if endpoint_error > 2.0e-8 or f01_anisotropy > 2.0e-10 or f01_rotation > 2.0e-10:
        landing = "SAVED_FIELD_OR_QUERY_FAILURE"
    elif min_sigma <= 0.0:
        landing = "SINGULAR_MAPS_BLOCK_GENERIC_COVARIANCE_INVERSION"
    elif source_error > 2.0e-10 or source_min_eigenvalue <= 0.0:
        landing = "IDENTIFIABILITY_NUMERICALLY_UNRESOLVED"
    elif rank_counts.get("RANK_NUMERICALLY_UNRESOLVED", 0):
        landing = "IDENTIFIABILITY_NUMERICALLY_UNRESOLVED"
    elif rank_counts.get("RANK_DEFICIENT_OBSERVED", 0):
        landing = "PROFILE_ENDPOINT_GEOMETRIC_DEGENERACY_OBSERVED"
    else:
        landing = "GEOMETRICALLY_SEPARATING__OBSERVATIONALLY_SOURCE_DEGENERATE"

    result = {
        "schema": "udt-cmb-g69-identifiability-v1",
        "primary_landing": landing,
        "profiles": len(profiles),
        "endpoints": len(ENDPOINTS),
        "cells": len(cells),
        "sensitivity_cells": len(sensitivities),
        "source_covariance_cells": len(covariances),
        "rank_counts": rank_counts,
        "max_x1_D_relative_error": endpoint_error,
        "max_F01_anisotropy": f01_anisotropy,
        "max_F01_polar_rotation": f01_rotation,
        "minimum_D_singular_value": min_sigma,
        "area_log_range": [min(float(row["area_log_vs_F01"]) for row in cells), max(float(row["area_log_vs_F01"]) for row in cells)],
        "anisotropy_log_range": [min(float(row["anisotropy_log"]) for row in cells), max(float(row["anisotropy_log"]) for row in cells)],
        "psi_range": [min(float(row["endpoint_psi"]) for row in cells), max(float(row["endpoint_psi"]) for row in cells)],
        "source_max_reconstruction_relative": source_error,
        "source_min_eigenvalue": source_min_eigenvalue,
        "observational_anchors_used": 0,
        "new_ODE_solves": 0,
        "maximum_conclusion": "bounded control-tile geometric sensitivity and exact unrestricted-source covariance nonidentifiability only",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (HERE / "DERIVATION_STDOUT.txt").write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
