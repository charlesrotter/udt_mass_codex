#!/usr/bin/env python3
"""Independent reconstruction of G69 cells without importing its production builder."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.interpolate import CubicSpline


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
G68 = ROOT / "udt_cmb_G68_F01_F02_finite_path_jacobi_controls_2026-08-11"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse(value: str) -> float:
    if "/" in value:
        a, b = value.split("/", 1)
        return float(a) / float(b)
    return float(value)


def load_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def metric(row: dict[str, str], state: np.ndarray) -> np.ndarray:
    _, r, theta, _ = state[:4]
    a = parse(row["lapse_a"])
    epsilon = parse(row["mix_epsilon"])
    A = 1.0 + a * r * r
    shape = row["mix_shape"]
    if row["metric_family"] == "F01" or shape == "ZERO":
        h = 0.0
    elif shape == "PERSISTENT":
        h = epsilon * r**2
    elif shape == "TAPERED":
        h = epsilon * r**2 * (1.0 - r) ** 2
    elif shape == "SIGN_CHANGING":
        h = epsilon * r**2 * (1.0 - 2.0 * r)
    else:
        raise AssertionError(shape)
    sine2 = math.sin(theta) ** 2
    g = np.zeros((4, 4))
    g[0, 0], g[1, 1], g[2, 2], g[3, 3] = -A, 1.0 / A, r * r, r * r * sine2
    g[0, 3] = g[3, 0] = h * sine2
    return g


def D_from_state(row: dict[str, str], state: np.ndarray) -> np.ndarray:
    E = state[8:16].reshape(2, 4)
    J = state[16:24].reshape(2, 4)
    return E @ metric(row, state) @ J.T


def relative(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b) / max(1.0, np.linalg.norm(a), np.linalg.norm(b)))


def main() -> None:
    source_rows = load_tsv(HERE / "SOURCE_MANIFEST.tsv")
    source_mismatches = [row["path"] for row in source_rows if digest(ROOT / row["path"]) != row["sha256"]]
    assert not source_mismatches

    profiles = {row["profile_id"]: row for row in load_tsv(G68 / "PROFILE_UNIVERSE.tsv")}
    cells = load_tsv(HERE / "CELL_ATLAS.tsv")
    assert len(profiles) == 21 and len(cells) == 315
    archive = np.load(G68 / "FINITE_PATH_SAMPLES.npz")
    maxima = []
    for cell in cells:
        profile_id = cell["profile_id"]
        row = profiles[profile_id]
        states = np.asarray(archive[profile_id + "__state"], dtype=np.float64)
        radii = states[1]
        independent_state = np.asarray(CubicSpline(radii, states.T, axis=0)(float(cell["endpoint_x"])))
        independent_D = D_from_state(row, independent_state)
        production_D = np.array(
            [[float(cell["D00"]), float(cell["D01"])], [float(cell["D10"]), float(cell["D11"])]],
            dtype=np.float64,
        )
        maxima.append(relative(independent_D, production_D))
    max_interpolation_relative = max(maxima)
    assert max_interpolation_relative <= 2.0e-7

    covariance_controls = {
        "IDENTITY": np.eye(2),
        "DIAGONAL_2_1": np.diag([2.0, 1.0]),
        "CORRELATED": np.array([[2.0, 1.0 / 3.0], [1.0 / 3.0, 1.0]]),
    }
    covariance_rows = load_tsv(HERE / "SOURCE_DEGENERACY_ATLAS.tsv")
    assert len(covariance_rows) == 945
    max_covariance_error = 0.0
    min_source_eigenvalue = math.inf
    cell_lookup = {(row["profile_id"], row["endpoint_x"]): row for row in cells}
    for row in covariance_rows:
        cell = cell_lookup[(row["profile_id"], row["endpoint_x"])]
        D = np.array([[float(cell["D00"]), float(cell["D01"])], [float(cell["D10"]), float(cell["D11"])]])
        observed = covariance_controls[row["covariance_id"]]
        source = np.linalg.inv(D) @ observed @ np.linalg.inv(D).T
        recorded = np.array(
            [[float(row["Csrc00"]), float(row["Csrc01"])], [float(row["Csrc10"]), float(row["Csrc11"])]],
        )
        assert relative(source, recorded) <= 2.0e-12
        max_covariance_error = max(max_covariance_error, relative(D @ source @ D.T, observed))
        min_source_eigenvalue = min(min_source_eigenvalue, float(np.linalg.eigvalsh(source)[0]))
    assert max_covariance_error <= 2.0e-10 and min_source_eigenvalue > 0.0

    sensitivities = load_tsv(HERE / "SENSITIVITY_ATLAS.tsv")
    assert len(sensitivities) == 15
    rank_counts: dict[str, int] = {}
    for row in sensitivities:
        matrix = np.array([[float(row[f"m{i}{j}"]) for j in range(3)] for i in range(3)])
        norms = np.linalg.norm(matrix, axis=0)
        assert np.all(norms > 0.0)
        singular = np.linalg.svd(matrix / norms, compute_uv=False)
        ratio = float(singular[-1] / singular[0])
        if ratio >= 1.0e-6:
            classification = "FULL_RANK_OBSERVED"
        elif ratio <= 1.0e-8:
            classification = "RANK_DEFICIENT_OBSERVED"
        else:
            classification = "RANK_NUMERICALLY_UNRESOLVED"
        assert classification == row["classification"]
        rank_counts[classification] = rank_counts.get(classification, 0) + 1

    result = {
        "schema": "udt-cmb-g69-independent-v1",
        "status": "PASS",
        "source_manifest_rows": len(source_rows),
        "source_mismatches": source_mismatches,
        "profiles": len(profiles),
        "cells": len(cells),
        "max_PCHIP_CubicSpline_D_relative": max_interpolation_relative,
        "source_covariance_cells": len(covariance_rows),
        "max_covariance_reconstruction_relative": max_covariance_error,
        "minimum_source_eigenvalue": min_source_eigenvalue,
        "sensitivity_cells": len(sensitivities),
        "rank_counts": rank_counts,
        "imports_production_builder": False,
        "new_ODE_solves": 0,
    }
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (HERE / "INDEPENDENT_VERIFICATION_STDOUT.txt").write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
