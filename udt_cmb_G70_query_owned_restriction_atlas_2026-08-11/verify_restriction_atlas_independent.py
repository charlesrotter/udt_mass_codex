#!/usr/bin/env python3
"""Independent SciPy-logm replay of the G70 restriction atlas."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.linalg import expm, logm


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
G69 = ROOT / "udt_cmb_G69_profile_endpoint_source_identifiability_2026-08-11"
CONTROLS = {
    "IDENTITY": np.eye(2),
    "DIAGONAL_2_1": np.diag([2.0, 1.0]),
    "CORRELATED": np.array([[2.0, 1.0 / 3.0], [1.0 / 3.0, 1.0]]),
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def relative(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.linalg.norm(left - right) / max(1.0, np.linalg.norm(left), np.linalg.norm(right)))


def D(row: dict[str, str]) -> np.ndarray:
    return np.array([[float(row["D00"]), float(row["D01"])],
                     [float(row["D10"]), float(row["D11"])]])


def coordinates(row: dict[str, str], source: np.ndarray, area: bool) -> tuple[np.ndarray, float]:
    covariance = D(row) @ source @ D(row).T
    logarithm = np.real_if_close(logm(covariance), tol=1000).astype(float)
    residual = relative(expm(logarithm), covariance)
    shape = np.array([0.5 * (logarithm[0, 0] - logarithm[1, 1]), logarithm[0, 1]])
    if area:
        return np.concatenate(([0.5 * np.linalg.slogdet(covariance)[1]], shape)), residual
    return shape, residual


def source_for(variant: str) -> np.ndarray:
    return CONTROLS["IDENTITY"] if variant == "ISOTROPIC" else CONTROLS[variant]


def value(row: dict[str, str], model: str, variant: str) -> tuple[np.ndarray, float]:
    if model == "R00_UNRESTRICTED_SPD":
        return np.empty(0), 0.0
    if model == "R01_ISOTROPIC_UNKNOWN_AMPLITUDE":
        return coordinates(row, CONTROLS["IDENTITY"], False)
    if model == "R02_FIXED_SHAPE_UNKNOWN_AMPLITUDE":
        return coordinates(row, CONTROLS[variant], False)
    if model == "R03_KNOWN_SOURCE_COVARIANCE":
        return coordinates(row, CONTROLS[variant], True)
    if model == "R04_UNKNOWN_AMPLITUDE_PLUS_CARRY":
        base, residual = coordinates(row, source_for(variant), False)
        return np.concatenate((base, [float(row["endpoint_psi"])])), residual
    if model == "R05_KNOWN_SOURCE_PLUS_CARRY":
        base, residual = coordinates(row, CONTROLS[variant], True)
        return np.concatenate((base, [float(row["endpoint_psi"])])), residual
    if model == "R06_TWO_FIXED_SHAPE_CHANNELS":
        left_name, right_name = variant.split("+", 1)
        left, left_residual = coordinates(row, CONTROLS[left_name], False)
        right, right_residual = coordinates(row, CONTROLS[right_name], False)
        return np.concatenate((left, right)), max(left_residual, right_residual)
    if model == "R07_UNRESTRICTED_SPD_PLUS_CARRY":
        return np.array([float(row["endpoint_psi"])]), 0.0
    raise ValueError((model, variant))


def stencil(lookup, shape: str, x: float, model: str, variant: str) -> tuple[np.ndarray, float]:
    endpoint, lapse, residuals = [], [], []
    for epsilon in (0.05, 0.20):
        plus, residual = value(lookup[(shape, 0.0, epsilon, round(x + 0.05, 2))], model, variant)
        residuals.append(residual)
        minus, residual = value(lookup[(shape, 0.0, epsilon, round(x - 0.05, 2))], model, variant)
        residuals.append(residual)
        endpoint.append((plus - minus) / 0.10)
        plus, residual = value(lookup[(shape, 0.25, epsilon, round(x, 2))], model, variant)
        residuals.append(residual)
        minus, residual = value(lookup[(shape, -0.25, epsilon, round(x, 2))], model, variant)
        residuals.append(residual)
        lapse.append((plus - minus) / 0.50)
    high, residual = value(lookup[(shape, 0.0, 0.20, round(x, 2))], model, variant)
    residuals.append(residual)
    low, residual = value(lookup[(shape, 0.0, 0.05, round(x, 2))], model, variant)
    residuals.append(residual)
    matrix = np.column_stack((0.5 * (endpoint[0] + endpoint[1]),
                              0.5 * (lapse[0] + lapse[1]), (high - low) / 0.15))
    return matrix, max(residuals, default=0.0)


def classification(matrix: np.ndarray) -> tuple[float, str]:
    n = matrix.shape[1]
    if matrix.shape[0] == 0:
        singular = np.zeros(n)
    else:
        norms = np.linalg.norm(matrix, axis=0)
        normalized = np.zeros_like(matrix)
        nonzero = norms > 0.0
        normalized[:, nonzero] = matrix[:, nonzero] / norms[nonzero]
        raw = np.linalg.svd(normalized, compute_uv=False)
        singular = np.pad(raw, (0, n - len(raw)))
    ratio = float(singular[-1] / singular[0]) if singular[0] > 0.0 else 0.0
    if ratio >= 1.0e-6:
        return ratio, "FULL_RANK_OBSERVED"
    if ratio <= 1.0e-8:
        return ratio, "RANK_DEFICIENT_OBSERVED"
    return ratio, "RANK_NUMERICALLY_UNRESOLVED"


def main() -> None:
    manifest = table(HERE / "SOURCE_MANIFEST.tsv")
    assert len(manifest) == 9 and all(digest(ROOT / row["path"]) == row["sha256"] for row in manifest)
    cells = table(G69 / "CELL_ATLAS.tsv")
    atlas = table(HERE / "RESTRICTION_RANK_ATLAS.tsv")
    lookup = {
        (row["shape"], float(row["lapse_a"]), float(row["epsilon"]), round(float(row["endpoint_x"]), 2)): row
        for row in cells if row["family"] == "F02"
    }
    max_matrix_relative = 0.0
    max_ratio_absolute = 0.0
    max_log_residual = 0.0
    reproduced = Counter()
    pair_reproduced = {"x_a": Counter(), "x_epsilon": Counter(), "a_epsilon": Counter()}
    for row in atlas:
        matrix, residual = stencil(lookup, row["shape"], float(row["endpoint_x"]), row["model_id"], row["variant"])
        recorded = np.asarray(json.loads(row["matrix_json"]), dtype=float)
        if matrix.shape[0] == 0:
            recorded = recorded.reshape(0, 3)
        max_matrix_relative = max(max_matrix_relative, relative(matrix, recorded))
        ratio, rank_class = classification(matrix)
        max_ratio_absolute = max(max_ratio_absolute, abs(ratio - float(row["sigma_ratio"])))
        assert rank_class == row["classification"]
        reproduced[rank_class] += 1
        for label, columns in {"x_a": (0, 1), "x_epsilon": (0, 2), "a_epsilon": (1, 2)}.items():
            _, pair_class = classification(matrix[:, columns])
            assert pair_class == row[label + "_classification"]
            pair_reproduced[label][pair_class] += 1
        max_log_residual = max(max_log_residual, residual)

    assert len(cells) == 315 and len(atlas) == 285
    assert max_matrix_relative <= 2.0e-10
    assert max_ratio_absolute <= 2.0e-10
    assert max_log_residual <= 2.0e-12
    assert reproduced == Counter({"RANK_DEFICIENT_OBSERVED": 224, "FULL_RANK_OBSERVED": 46,
                                  "RANK_NUMERICALLY_UNRESOLVED": 15})
    r05 = [row for row in atlas if row["model_id"] == "R05_KNOWN_SOURCE_PLUS_CARRY"]
    assert len(r05) == 45 and all(row["classification"] == "FULL_RANK_OBSERVED" for row in r05)

    # Independent exact congruence and positivity controls on deterministic nonsymmetric D values.
    covariance = CONTROLS["CORRELATED"]
    congruence_error = 0.0
    min_source_eigenvalue = math.inf
    for index in range(1, 101):
        transfer = np.array([[1.0 + index / 101.0, (-1) ** index / (17.0 + index)],
                             [index / 211.0, 1.0 + index / 157.0]])
        observed = np.array([[2.0 + index / 200.0, 0.2], [0.2, 1.0 + index / 300.0]])
        inverse = np.linalg.inv(transfer)
        source = inverse @ observed @ inverse.T
        congruence_error = max(congruence_error, relative(transfer @ source @ transfer.T, observed))
        min_source_eigenvalue = min(min_source_eigenvalue, float(np.linalg.eigvalsh(source)[0]))
    assert congruence_error <= 2.0e-12 and min_source_eigenvalue > 0.0

    result = {
        "schema": "udt-cmb-g70-independent-v1",
        "status": "PASS",
        "source_manifest_rows": len(manifest),
        "input_cells": len(cells),
        "atlas_rows": len(atlas),
        "rank_counts": dict(reproduced),
        "pair_rank_counts": {key: dict(value) for key, value in pair_reproduced.items()},
        "R05_full_rank_rows": len(r05),
        "maximum_matrix_relative": max_matrix_relative,
        "maximum_sigma_ratio_absolute": max_ratio_absolute,
        "maximum_logm_expm_reconstruction_relative": max_log_residual,
        "congruence_control_maximum_relative": congruence_error,
        "congruence_control_minimum_source_eigenvalue": min_source_eigenvalue,
        "imports_production_builder": False,
        "new_ODE_solves": 0,
    }
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
