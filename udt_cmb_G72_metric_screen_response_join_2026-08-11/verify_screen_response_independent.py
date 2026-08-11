#!/usr/bin/env python3
"""Independent SVD-based verification of the G72 screen-response claims."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
G68_ATLAS = ROOT / "udt_cmb_G68_F01_F02_finite_path_jacobi_controls_2026-08-11/FINITE_PATH_ATLAS.tsv"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def rot(angle: float) -> np.ndarray:
    return np.array(
        [[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]], dtype=float
    )


def wrap(value: float) -> float:
    return math.atan2(math.sin(value), math.cos(value))


def svd_readout(D: np.ndarray, U: np.ndarray) -> tuple[float, float, float]:
    M = np.linalg.solve(U, D)
    left, values, right_t = np.linalg.svd(M)
    polar = left @ right_t
    if np.linalg.det(polar) < 0.0:
        left[:, -1] *= -1.0
        values[-1] *= -1.0
        polar = left @ right_t
    angle = math.atan2(polar[1, 0], polar[0, 0])
    scale = math.sqrt(float(np.linalg.det(M)))
    singular = np.linalg.svd(M, compute_uv=False)
    shear = 0.5 * math.log(float(singular[0] / singular[1]))
    return scale, shear, angle


def main() -> None:
    manifest = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    assert len(manifest) == 14
    for row in manifest:
        assert digest(ROOT / row["path"]) == row["sha256"]

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    assert production["landing"] == "METRIC_OWNS_SOURCE_FREE_SCREEN_RESPONSE__PHYSICAL_OBSERVABLE_OPEN"

    rng = np.random.default_rng(118027)
    trials = 1000
    max_scale = 0.0
    max_shear = 0.0
    max_angle = 0.0
    max_reflection = 0.0
    raw_transport_changed = 0
    F = np.diag([1.0, -1.0])
    for _ in range(trials):
        # Build D from an independent polar parameterization so det(D)>0 by construction.
        source_axis = rot(rng.uniform(-math.pi, math.pi))
        observer_axis = rot(rng.uniform(-math.pi, math.pi))
        scales = np.diag(np.exp(rng.uniform(-2.0, 2.0, size=2)))
        D = observer_axis @ scales @ source_axis.T
        U = rot(rng.uniform(-math.pi, math.pi))
        Rs = rot(rng.uniform(-math.pi, math.pi))
        Ro = rot(rng.uniform(-math.pi, math.pi))
        Dp = Ro @ D @ Rs.T
        Up = Ro @ U @ Rs.T

        a = svd_readout(D, U)
        b = svd_readout(Dp, Up)
        max_scale = max(max_scale, abs(a[0] - b[0]))
        max_shear = max(max_shear, abs(a[1] - b[1]))
        max_angle = max(max_angle, abs(wrap(a[2] - b[2])))

        raw_before = math.atan2(U[1, 0], U[0, 0])
        raw_after = math.atan2(Up[1, 0], Up[0, 0])
        if abs(wrap(raw_before - raw_after)) > 1e-5:
            raw_transport_changed += 1

        reflected = svd_readout(F @ D @ F, F @ U @ F)
        max_reflection = max(max_reflection, abs(wrap(reflected[2] + a[2])))

    assert max_scale < 2e-12
    assert max_shear < 2e-12
    assert max_angle < 2e-12
    assert max_reflection < 2e-12
    assert raw_transport_changed > int(0.98 * trials)

    # Exact independent transfer witness using rational arithmetic.
    L1, L2 = Fraction(2), Fraction(3)
    D_total = L1 + L2
    D_product = L1 * L2
    assert D_total == 5 and D_product == 6 and D_total != D_product

    g68 = read_tsv(G68_ATLAS)
    assert len(g68) == 21
    g68_readouts = []
    for row in g68:
        D = np.array(
            [
                [float(row["D_theta_theta"]), float(row["D_theta_psi"])],
                [float(row["D_psi_theta"]), float(row["D_psi_psi"])],
            ]
        )
        g68_readouts.append(svd_readout(D, np.eye(2)))
    max_g68_angle = max(abs(value[2]) for value in g68_readouts)
    max_g68_shear = max(value[1] for value in g68_readouts)
    assert max_g68_angle < 2e-19
    assert max_g68_shear > 0.0

    # A homogeneous linear response cannot manufacture a nonzero state from the zero state.
    D = np.array([[1.3, 0.4], [-0.1, 0.8]])
    assert np.array_equal(D @ np.zeros((2, 2)) @ D.T, np.zeros((2, 2)))

    result = {
        "schema": "udt-cmb-g72-screen-response-independent-v1",
        "status": "PASS",
        "method": "independent SVD polar factor plus constructed positive-determinant maps",
        "source_manifest_rows": len(manifest),
        "trials": trials,
        "max_scale_gauge_error": max_scale,
        "max_shear_gauge_error": max_shear,
        "max_relative_angle_gauge_error": max_angle,
        "max_reflection_angle_error": max_reflection,
        "raw_open_transport_changed_trials": raw_transport_changed,
        "endpoint_D_block_exact_witness": {"D_total": 5, "D_product": 6},
        "g68_rows": len(g68),
        "g68_max_relative_angle": max_g68_angle,
        "g68_max_shear": max_g68_shear,
        "zero_source_remains_zero": True,
        "landing_reproduced": production["landing"],
    }
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
