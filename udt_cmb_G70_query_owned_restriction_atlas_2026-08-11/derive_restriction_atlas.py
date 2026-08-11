#!/usr/bin/env python3
"""Build the preregistered G70 source-restriction and channel-rank atlas."""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
G69 = ROOT / "udt_cmb_G69_profile_endpoint_source_identifiability_2026-08-11"
SHAPES = ("PERSISTENT", "TAPERED", "SIGN_CHANGING")
CENTERS = (0.35, 0.50, 0.65, 0.80, 0.95)
EPSILONS = (0.05, 0.20)
SOURCE_CONTROLS = {
    "IDENTITY": np.eye(2, dtype=np.float64),
    "DIAGONAL_2_1": np.diag([2.0, 1.0]).astype(np.float64),
    "CORRELATED": np.array([[2.0, 1.0 / 3.0], [1.0 / 3.0, 1.0]], dtype=np.float64),
}
THRESHOLD_FULL = 1.0e-6
THRESHOLD_DEFICIENT = 1.0e-8


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def relative(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.linalg.norm(left - right) / max(1.0, np.linalg.norm(left), np.linalg.norm(right)))


def matrix_from_row(row: dict[str, str]) -> np.ndarray:
    return np.array(
        [[float(row["D00"]), float(row["D01"])], [float(row["D10"]), float(row["D11"])]],
        dtype=np.float64,
    )


def log_spd(matrix: np.ndarray) -> tuple[np.ndarray, float]:
    symmetric = 0.5 * (matrix + matrix.T)
    values, vectors = np.linalg.eigh(symmetric)
    if not np.all(values > 0.0):
        raise ValueError(f"non-positive covariance eigenvalues: {values}")
    logarithm = (vectors * np.log(values)) @ vectors.T
    log_values, log_vectors = np.linalg.eigh(0.5 * (logarithm + logarithm.T))
    reconstructed = (log_vectors * np.exp(log_values)) @ log_vectors.T
    return logarithm, relative(reconstructed, symmetric)


def covariance_coordinates(row: dict[str, str], source: np.ndarray, include_area: bool) -> tuple[np.ndarray, float]:
    D = matrix_from_row(row)
    covariance = D @ source @ D.T
    logarithm, residual = log_spd(covariance)
    shape = np.array(
        [0.5 * (logarithm[0, 0] - logarithm[1, 1]), logarithm[0, 1]], dtype=np.float64
    )
    if include_area:
        area = 0.5 * float(np.linalg.slogdet(covariance)[1])
        return np.concatenate(([area], shape)), residual
    return shape, residual


def classify(matrix: np.ndarray) -> dict[str, object]:
    parameter_count = matrix.shape[1]
    if parameter_count == 0:
        raise ValueError("parameterless rank request")
    if matrix.shape[0] == 0:
        singular = np.zeros(parameter_count, dtype=np.float64)
        norms = np.zeros(parameter_count, dtype=np.float64)
    else:
        norms = np.linalg.norm(matrix, axis=0)
        if np.any(norms == 0.0):
            normalized = np.zeros_like(matrix)
            nonzero = norms > 0.0
            normalized[:, nonzero] = matrix[:, nonzero] / norms[nonzero]
        else:
            normalized = matrix / norms
        singular_raw = np.linalg.svd(normalized, compute_uv=False)
        singular = np.pad(singular_raw, (0, parameter_count - len(singular_raw)))
    sigma_max = float(singular[0]) if len(singular) else 0.0
    sigma_min = float(singular[-1]) if len(singular) else 0.0
    ratio = sigma_min / sigma_max if sigma_max > 0.0 else 0.0
    condition = sigma_max / sigma_min if sigma_min > 0.0 else math.inf
    if ratio >= THRESHOLD_FULL:
        classification = "FULL_RANK_OBSERVED"
    elif ratio <= THRESHOLD_DEFICIENT:
        classification = "RANK_DEFICIENT_OBSERVED"
    else:
        classification = "RANK_NUMERICALLY_UNRESOLVED"
    return {
        "column_norms": norms,
        "singular": singular,
        "sigma_ratio": ratio,
        "condition": condition,
        "classification": classification,
    }


def finite_difference(
    lookup: dict[tuple[str, float, float, float], dict[str, str]],
    shape: str,
    x: float,
    readout,
) -> tuple[np.ndarray, float]:
    endpoint_columns = []
    lapse_columns = []
    residuals = []
    for epsilon in EPSILONS:
        plus, residual = readout(lookup[(shape, 0.0, epsilon, round(x + 0.05, 2))])
        residuals.append(residual)
        minus, residual = readout(lookup[(shape, 0.0, epsilon, round(x - 0.05, 2))])
        residuals.append(residual)
        endpoint_columns.append((plus - minus) / 0.10)
        plus, residual = readout(lookup[(shape, 0.25, epsilon, round(x, 2))])
        residuals.append(residual)
        minus, residual = readout(lookup[(shape, -0.25, epsilon, round(x, 2))])
        residuals.append(residual)
        lapse_columns.append((plus - minus) / 0.50)
    high, residual = readout(lookup[(shape, 0.0, 0.20, round(x, 2))])
    residuals.append(residual)
    low, residual = readout(lookup[(shape, 0.0, 0.05, round(x, 2))])
    residuals.append(residual)
    amplitude_column = (high - low) / 0.15
    matrix = np.column_stack(
        (0.5 * (endpoint_columns[0] + endpoint_columns[1]),
         0.5 * (lapse_columns[0] + lapse_columns[1]),
         amplitude_column)
    )
    return matrix, max(residuals, default=0.0)


def append_psi(readout):
    def combined(row: dict[str, str]) -> tuple[np.ndarray, float]:
        value, residual = readout(row)
        return np.concatenate((value, [float(row["endpoint_psi"])])), residual
    return combined


def shape_readout(source: np.ndarray):
    return lambda row: covariance_coordinates(row, source, False)


def full_readout(source: np.ndarray):
    return lambda row: covariance_coordinates(row, source, True)


def paired_shape_readout(first: np.ndarray, second: np.ndarray):
    def combined(row: dict[str, str]) -> tuple[np.ndarray, float]:
        left, left_residual = covariance_coordinates(row, first, False)
        right, right_residual = covariance_coordinates(row, second, False)
        return np.concatenate((left, right)), max(left_residual, right_residual)
    return combined


def json_array(array: np.ndarray) -> str:
    return json.dumps(np.asarray(array, dtype=float).tolist(), separators=(",", ":"))


def main() -> None:
    source_manifest = rows(HERE / "SOURCE_MANIFEST.tsv")
    if len(source_manifest) != 9:
        raise AssertionError("source manifest census")
    if not all(digest(ROOT / row["path"]) == row["sha256"] for row in source_manifest):
        raise AssertionError("source manifest hash mismatch")

    cells = rows(G69 / "CELL_ATLAS.tsv")
    keys = {(row["profile_id"], row["endpoint_x"]) for row in cells}
    if len(cells) != len(keys) != 315:
        raise AssertionError("cell census")
    if len(cells) != 315 or len(keys) != 315:
        raise AssertionError("cell census")
    lookup = {
        (row["shape"], float(row["lapse_a"]), float(row["epsilon"]), round(float(row["endpoint_x"]), 2)): row
        for row in cells if row["family"] == "F02"
    }
    expected_lookup = 3 * 3 * 2 * 15
    if len(lookup) != expected_lookup:
        raise AssertionError(("F02 lookup census", len(lookup), expected_lookup))

    psi_values = np.array([float(row["endpoint_psi"]) for row in cells], dtype=np.float64)
    psi_span = float(np.max(psi_values) - np.min(psi_values))
    if psi_span >= math.pi:
        raise AssertionError("psi chart crosses a possible wrap")

    models: list[tuple[str, str, object | None, str]] = [
        ("R00_UNRESTRICTED_SPD", "UNRESTRICTED_SPD", None, "SOURCE_PROFILED_EXACTLY"),
        ("R01_ISOTROPIC_UNKNOWN_AMPLITUDE", "IDENTITY", shape_readout(SOURCE_CONTROLS["IDENTITY"]), "SOURCE_SHAPE_SUPPLIED"),
    ]
    for name, source in SOURCE_CONTROLS.items():
        models.append(("R02_FIXED_SHAPE_UNKNOWN_AMPLITUDE", name, shape_readout(source), "SOURCE_SHAPE_SUPPLIED"))
        models.append(("R03_KNOWN_SOURCE_COVARIANCE", name, full_readout(source), "SOURCE_COVARIANCE_SUPPLIED"))
    carry_sources = [("ISOTROPIC", SOURCE_CONTROLS["IDENTITY"]), *SOURCE_CONTROLS.items()]
    for name, source in carry_sources:
        models.append(("R04_UNKNOWN_AMPLITUDE_PLUS_CARRY", name, append_psi(shape_readout(source)), "SOURCE_SHAPE_AND_CARRY_SUPPLIED"))
    for name, source in SOURCE_CONTROLS.items():
        models.append(("R05_KNOWN_SOURCE_PLUS_CARRY", name, append_psi(full_readout(source)), "SOURCE_COVARIANCE_AND_CARRY_SUPPLIED"))
    for left, right in itertools.combinations(SOURCE_CONTROLS, 2):
        models.append(("R06_TWO_FIXED_SHAPE_CHANNELS", left + "+" + right,
                       paired_shape_readout(SOURCE_CONTROLS[left], SOURCE_CONTROLS[right]),
                       "TWO_SOURCE_SHAPES_SUPPLIED"))
    models.append(("R07_UNRESTRICTED_SPD_PLUS_CARRY", "UNRESTRICTED_SPD", append_psi(lambda row: (np.empty(0), 0.0)),
                   "SOURCE_PROFILED_CARRY_SUPPLIED"))

    atlas = []
    max_log_residual = 0.0
    for model_id, variant, readout, premise in models:
        for shape in SHAPES:
            for x in CENTERS:
                if readout is None:
                    matrix = np.zeros((0, 3), dtype=np.float64)
                    residual = 0.0
                else:
                    matrix, residual = finite_difference(lookup, shape, x, readout)
                max_log_residual = max(max_log_residual, residual)
                full = classify(matrix)
                pair_results = {}
                for label, columns in {
                    "x_a": (0, 1), "x_epsilon": (0, 2), "a_epsilon": (1, 2)
                }.items():
                    pair_results[label] = classify(matrix[:, columns])
                atlas.append(
                    {
                        "model_id": model_id,
                        "variant": variant,
                        "premise": premise,
                        "shape": shape,
                        "endpoint_x": x,
                        "matrix": matrix,
                        "full": full,
                        "pairs": pair_results,
                        "log_residual": residual,
                    }
                )

    atlas_fields = [
        "model_id", "variant", "premise", "shape", "endpoint_x", "output_dimension",
        "matrix_json", "column_norms_json", "singular_values_json", "sigma_ratio", "condition",
        "classification", "x_a_ratio", "x_a_classification", "x_epsilon_ratio",
        "x_epsilon_classification", "a_epsilon_ratio", "a_epsilon_classification",
        "matrix_log_reconstruction_relative",
    ]
    with (HERE / "RESTRICTION_RANK_ATLAS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=atlas_fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in atlas:
            full = row["full"]
            pairs = row["pairs"]
            condition = full["condition"]
            writer.writerow(
                {
                    "model_id": row["model_id"], "variant": row["variant"], "premise": row["premise"],
                    "shape": row["shape"], "endpoint_x": row["endpoint_x"],
                    "output_dimension": row["matrix"].shape[0], "matrix_json": json_array(row["matrix"]),
                    "column_norms_json": json_array(full["column_norms"]),
                    "singular_values_json": json_array(full["singular"]),
                    "sigma_ratio": full["sigma_ratio"], "condition": condition if math.isfinite(condition) else "inf",
                    "classification": full["classification"],
                    "x_a_ratio": pairs["x_a"]["sigma_ratio"],
                    "x_a_classification": pairs["x_a"]["classification"],
                    "x_epsilon_ratio": pairs["x_epsilon"]["sigma_ratio"],
                    "x_epsilon_classification": pairs["x_epsilon"]["classification"],
                    "a_epsilon_ratio": pairs["a_epsilon"]["sigma_ratio"],
                    "a_epsilon_classification": pairs["a_epsilon"]["classification"],
                    "matrix_log_reconstruction_relative": row["log_residual"],
                }
            )

    grouped: dict[tuple[str, str], list[dict[str, object]]] = {}
    for row in atlas:
        grouped.setdefault((str(row["model_id"]), str(row["variant"])), []).append(row)
    summary_fields = [
        "model_id", "variant", "rows", "full_rank", "rank_deficient", "unresolved",
        "min_sigma_ratio", "max_condition", "x_a_full", "x_epsilon_full", "a_epsilon_full",
        "ownership_status",
    ]
    summaries = []
    for (model_id, variant), group in sorted(grouped.items()):
        classifications = [str(row["full"]["classification"]) for row in group]
        ratios = [float(row["full"]["sigma_ratio"]) for row in group]
        conditions = [float(row["full"]["condition"]) for row in group]
        summary = {
            "model_id": model_id,
            "variant": variant,
            "rows": len(group),
            "full_rank": classifications.count("FULL_RANK_OBSERVED"),
            "rank_deficient": classifications.count("RANK_DEFICIENT_OBSERVED"),
            "unresolved": classifications.count("RANK_NUMERICALLY_UNRESOLVED"),
            "min_sigma_ratio": min(ratios),
            "max_condition": max(conditions),
            "x_a_full": sum(row["pairs"]["x_a"]["classification"] == "FULL_RANK_OBSERVED" for row in group),
            "x_epsilon_full": sum(row["pairs"]["x_epsilon"]["classification"] == "FULL_RANK_OBSERVED" for row in group),
            "a_epsilon_full": sum(row["pairs"]["a_epsilon"]["classification"] == "FULL_RANK_OBSERVED" for row in group),
            "ownership_status": "OPEN_NOT_CURRENTLY_UDT_OWNED",
        }
        summaries.append(summary)
    with (HERE / "MODEL_SUMMARY.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=summary_fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(summaries)

    full_rows = sum(row["full"]["classification"] == "FULL_RANK_OBSERVED" for row in atlas)
    unresolved_rows = sum(row["full"]["classification"] == "RANK_NUMERICALLY_UNRESOLVED" for row in atlas)
    helpful_models = sorted({row["model_id"] for row in atlas if row["full"]["classification"] == "FULL_RANK_OBSERVED"})
    if unresolved_rows:
        landing = "IDENTIFIABILITY_NUMERICALLY_UNRESOLVED"
    elif helpful_models:
        landing = "ALGEBRAIC_RESTRICTIONS_WORK__OWNERSHIP_REMAINS_OPEN"
    else:
        landing = "NO_TESTED_RESTRICTION_RESTORES_LOCAL_RANK"
    result = {
        "schema": "udt-cmb-g70-restriction-atlas-v1",
        "primary_landing": landing,
        "source_manifest_rows": len(source_manifest),
        "input_cells": len(cells),
        "sensitivity_centers": len(SHAPES) * len(CENTERS),
        "model_variants": len(models),
        "atlas_rows": len(atlas),
        "full_rank_rows": full_rows,
        "rank_unresolved_rows": unresolved_rows,
        "full_rank_model_ids": helpful_models,
        "maximum_matrix_log_reconstruction_relative": max_log_residual,
        "psi_span": psi_span,
        "new_ODE_solves": 0,
        "observational_anchors_used": 0,
        "current_query_owned_identifiability_restrictions": 0,
        "maximum_conclusion": "bounded algebraic restriction efficacy plus current ownership census only",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
