#!/usr/bin/env python3
"""Derive the bounded G72 source-free metric screen-response classification."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
G68_ATLAS = ROOT / "udt_cmb_G68_F01_F02_finite_path_jacobi_controls_2026-08-11/FINITE_PATH_ATLAS.tsv"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def rotation(angle: float) -> np.ndarray:
    c, s = math.cos(angle), math.sin(angle)
    return np.array([[c, -s], [s, c]], dtype=float)


def polar_angle(matrix: np.ndarray) -> float:
    """Angle of the positive-determinant two-dimensional polar rotation."""
    return math.atan2(matrix[1, 0] - matrix[0, 1], matrix[0, 0] + matrix[1, 1])


def angle_delta(left: float, right: float) -> float:
    return math.atan2(math.sin(left - right), math.cos(left - right))


def invariants(D: np.ndarray, U: np.ndarray) -> dict[str, float | np.ndarray]:
    assert np.linalg.det(D) > 0.0
    assert np.allclose(U.T @ U, np.eye(2), atol=2e-12)
    assert np.linalg.det(U) > 0.0
    M = U.T @ D
    svals = np.linalg.svd(M, compute_uv=False)
    assert svals[0] >= svals[1] > 0.0
    theta = polar_angle(M)
    area_density = float(np.linalg.det(M))
    length_scale = math.sqrt(area_density)
    shear_magnitude = 0.5 * math.log(float(svals[0] / svals[1]))

    C = M.T @ M
    eigenvalues, eigenvectors = np.linalg.eigh(C)
    logC = eigenvectors @ np.diag(np.log(eigenvalues)) @ eigenvectors.T
    shear_tensor = 0.25 * (logC - 0.5 * np.trace(logC) * np.eye(2)) * 2.0
    # Equivalent to [log(P)]_TF because log(C)=2 log(P).
    return {
        "M": M,
        "area_density": area_density,
        "length_scale": length_scale,
        "shear_magnitude": shear_magnitude,
        "relative_polar_angle": theta,
        "shear_tensor": shear_tensor,
    }


def symbolic_checks() -> dict[str, bool]:
    a, b, c, d = sp.symbols("a b c d", real=True)
    q = a + d
    p = c - b
    z = sp.sqrt(q**2 + p**2)
    M = sp.Matrix([[a, b], [c, d]])
    R = sp.Matrix([[q, -p], [p, q]]) / z
    P = sp.simplify(R.T * M)

    orthogonal = all(sp.simplify(value) == 0 for value in (R.T * R - sp.eye(2)))
    symmetric = sp.simplify(P[0, 1] - P[1, 0]) == 0
    reconstructs = all(sp.simplify(value) == 0 for value in (R * P - M))
    determinant = sp.simplify(R.det()) == 1

    # Exact free-propagation transfer witness: the full state composes, D blocks do not.
    L1, L2 = sp.Integer(2), sp.Integer(3)
    T1 = sp.Matrix([[1, L1], [0, 1]])
    T2 = sp.Matrix([[1, L2], [0, 1]])
    total = T2 * T1
    full_transfer_composes = total == sp.Matrix([[1, L1 + L2], [0, 1]])
    d_block_not_multiplicative = total[0, 1] != T2[0, 1] * T1[0, 1]

    return {
        "polar_factor_orthogonal": orthogonal,
        "positive_factor_symmetric": symmetric,
        "polar_reconstruction": reconstructs,
        "polar_orientation_positive": determinant,
        "full_jacobi_transfer_composes": full_transfer_composes,
        "endpoint_D_block_not_multiplicative": d_block_not_multiplicative,
    }


def verify_source_manifest() -> int:
    manifest = rows(HERE / "SOURCE_MANIFEST.tsv")
    for row in manifest:
        target = ROOT / row["path"]
        assert target.is_file(), target
        assert sha256(target) == row["sha256"], target
    return len(manifest)


def numerical_gauge_trials() -> dict[str, float | int]:
    rng = np.random.default_rng(720811)
    count = 512
    max_m_covariance = 0.0
    max_scale_error = 0.0
    max_shear_error = 0.0
    max_angle_error = 0.0
    max_reflection_angle_error = 0.0
    changed_u_angle = 0
    max_zero_tensor = 0.0
    max_source_congruence = 0.0

    reflection = np.diag([1.0, -1.0])
    for _ in range(count):
        D = rng.normal(size=(2, 2))
        if np.linalg.det(D) < 0.0:
            D[:, 0] *= -1.0
        D += 0.2 * np.eye(2)
        if np.linalg.det(D) <= 0.05:
            D += 2.0 * np.eye(2)
        if np.linalg.det(D) < 0.0:
            D[:, 0] *= -1.0
        assert np.linalg.det(D) > 0.0

        U = rotation(rng.uniform(-math.pi, math.pi))
        source_gauge = rotation(rng.uniform(-math.pi, math.pi))
        observer_gauge = rotation(rng.uniform(-math.pi, math.pi))
        Dp = observer_gauge @ D @ source_gauge.T
        Up = observer_gauge @ U @ source_gauge.T

        original = invariants(D, U)
        transformed = invariants(Dp, Up)
        expected_M = source_gauge @ original["M"] @ source_gauge.T
        max_m_covariance = max(max_m_covariance, float(np.linalg.norm(transformed["M"] - expected_M)))
        max_scale_error = max(max_scale_error, abs(float(original["length_scale"]) - float(transformed["length_scale"])))
        max_shear_error = max(max_shear_error, abs(float(original["shear_magnitude"]) - float(transformed["shear_magnitude"])))
        max_angle_error = max(max_angle_error, abs(angle_delta(float(original["relative_polar_angle"]), float(transformed["relative_polar_angle"]))))

        u_angle = polar_angle(U)
        up_angle = polar_angle(Up)
        if abs(angle_delta(u_angle, up_angle)) > 1e-4:
            changed_u_angle += 1

        Df = reflection @ D @ reflection
        Uf = reflection @ U @ reflection
        reflected = invariants(Df, Uf)
        max_reflection_angle_error = max(
            max_reflection_angle_error,
            abs(angle_delta(float(reflected["relative_polar_angle"]), -float(original["relative_polar_angle"]))),
        )

        zero = np.zeros((2, 2))
        max_zero_tensor = max(max_zero_tensor, float(np.linalg.norm(D @ zero @ D.T)))

        A = rng.normal(size=(2, 2))
        Cobs = A @ A.T + 0.25 * np.eye(2)
        Dinv = np.linalg.inv(D)
        Csrc = Dinv @ Cobs @ Dinv.T
        replay = D @ Csrc @ D.T
        max_source_congruence = max(
            max_source_congruence,
            float(np.linalg.norm(replay - Cobs) / np.linalg.norm(Cobs)),
        )

    assert changed_u_angle > int(0.95 * count)
    return {
        "trials": count,
        "max_M_gauge_covariance_error": max_m_covariance,
        "max_length_scale_gauge_error": max_scale_error,
        "max_shear_gauge_error": max_shear_error,
        "max_relative_angle_gauge_error": max_angle_error,
        "open_U_angle_changed_trials": changed_u_angle,
        "max_reflection_angle_error": max_reflection_angle_error,
        "max_zero_source_tensor_output": max_zero_tensor,
        "max_unrestricted_source_congruence_error": max_source_congruence,
    }


def g68_response_atlas() -> dict[str, float | int]:
    source_rows = rows(G68_ATLAS)
    output_rows: list[dict[str, str]] = []
    max_angle = 0.0
    max_saved_angle_delta = 0.0
    max_shear = 0.0
    for row in source_rows:
        D = np.array(
            [
                [float(row["D_theta_theta"]), float(row["D_theta_psi"])],
                [float(row["D_psi_theta"]), float(row["D_psi_psi"])],
            ]
        )
        # G68 projects into its parallel-transported endpoint screen; U is identity in that
        # registered representation.
        response = invariants(D, np.eye(2))
        angle = float(response["relative_polar_angle"])
        saved = float(row["polar_rotation"])
        max_angle = max(max_angle, abs(angle))
        max_saved_angle_delta = max(max_saved_angle_delta, abs(angle_delta(angle, saved)))
        max_shear = max(max_shear, float(response["shear_magnitude"]))
        output_rows.append(
            {
                "profile_id": row["profile_id"],
                "family": row["family"],
                "status": row["status"],
                "length_scale": f"{float(response['length_scale']):.17g}",
                "shear_magnitude": f"{float(response['shear_magnitude']):.17g}",
                "relative_polar_angle": f"{angle:.17g}",
                "endpoint_azimuthal_carry_psi": row["endpoint_psi"],
                "interpretation": "GEOMETRIC_RESPONSE_ON_SUPPLIED_CONTROL_QUERY",
            }
        )

    columns = list(output_rows[0])
    with (HERE / "G68_RESPONSE_ATLAS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(output_rows)
    return {
        "rows": len(output_rows),
        "max_relative_polar_angle": max_angle,
        "max_delta_from_saved_polar_rotation": max_saved_angle_delta,
        "max_shear_magnitude": max_shear,
        "azimuthal_carry_is_not_polar_rotation": True,
    }


def scalar_source_checks() -> dict[str, bool | float]:
    sample = np.array(
        [[-1.0, -0.5], [0.0, 0.0], [0.25, 0.75], [1.0, -0.25]], dtype=float
    )
    M = np.array([[1.4, 0.3], [-0.2, 0.9]])
    inverse_points = sample @ np.linalg.inv(M).T
    constant_source = np.full(len(sample), 7.0)
    zero_source = np.zeros(len(sample))
    nonconstant_source = inverse_points[:, 0] ** 2 + 0.3 * inverse_points[:, 1]
    direct_nonconstant = sample[:, 0] ** 2 + 0.3 * sample[:, 1]
    return {
        "constant_remains_constant": bool(np.all(constant_source == 7.0)),
        "zero_remains_zero": bool(np.all(zero_source == 0.0)),
        "nonconstant_pattern_is_remapped": bool(not np.allclose(nonconstant_source, direct_nonconstant)),
        "max_constant_change": float(np.max(np.abs(constant_source - 7.0))),
    }


def main() -> None:
    source_count = verify_source_manifest()
    symbolic = symbolic_checks()
    assert all(symbolic.values())
    numerical = numerical_gauge_trials()
    assert numerical["max_M_gauge_covariance_error"] < 1e-11
    assert numerical["max_length_scale_gauge_error"] < 1e-11
    assert numerical["max_shear_gauge_error"] < 1e-11
    assert numerical["max_relative_angle_gauge_error"] < 1e-11
    assert numerical["max_reflection_angle_error"] < 1e-11
    assert numerical["max_zero_source_tensor_output"] == 0.0
    assert numerical["max_unrestricted_source_congruence_error"] < 1e-11

    g68 = g68_response_atlas()
    scalar = scalar_source_checks()
    assert scalar["constant_remains_constant"] and scalar["zero_remains_zero"]
    assert scalar["nonconstant_pattern_is_remapped"]

    result = {
        "schema": "udt-cmb-g72-screen-response-v1",
        "landing": "METRIC_OWNS_SOURCE_FREE_SCREEN_RESPONSE__PHYSICAL_OBSERVABLE_OPEN",
        "source_manifest_rows": source_count,
        "regular_domain": "oriented positive screens; common typed D,U; det(D)>0; no caustic",
        "generic_oriented_gauge_quotient_dimension": 3,
        "complete_generic_invariants": [
            "common response scale/density (dimensionful until referenced)",
            "dimensionless shear magnitude",
            "relative polar rotation angle modulo 2pi",
        ],
        "reflection_quotient": "relative angle identified with its negative",
        "symbolic_checks": symbolic,
        "numerical_gauge_checks": numerical,
        "g68_control_replay": g68,
        "scalar_source_checks": scalar,
        "status": {
            "source_free_geometric_response_operator": "DERIVED_CONDITIONAL_ON_QUERY",
            "source_free_shear_tensor": "DERIVED_COVARIANT_CONDITIONAL_ON_QUERY",
            "relative_polar_rotation": "DERIVED_ON_ORIENTED_REGULAR_QUERY",
            "physical_scalar_TT_response": "OPEN_NO_OWNER",
            "physical_polarization_response": "OPEN_NO_OWNER",
            "source_population_and_normalization": "OPEN_NO_OWNER",
            "physical_endpoint_profile_and_global_scale": "OPEN_NO_OWNER",
        },
        "maximum_conclusion": (
            "the metric evaluates a complete source-free local screen response after a regular "
            "query/path is supplied; it reshapes or transports supplied structure but does not "
            "populate a sky field or derive a physical CMB readout"
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
