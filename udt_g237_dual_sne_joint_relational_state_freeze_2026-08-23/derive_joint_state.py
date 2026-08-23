#!/usr/bin/env python3
"""Construct the preregistered G237 joint state from frozen G236 estimates."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import cho_factor, cho_solve


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
SOURCE = ROOT / "udt_g236_dual_sne_relational_state_reconstruction_2026-08-23/PRODUCTION_RESULT.json"
MANIFEST = PACKAGE / "SOURCE_MANIFEST.tsv"
OUT = PACKAGE / "JOINT_STATE_RESULT.json"
TABLE = PACKAGE / "JOINT_STATE.tsv"
FREEZE = PACKAGE / "FROZEN_PRIMARY_K12_STATE.json"
K_VALUES = (8, 12, 16, 24)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_sources() -> dict[str, bool]:
    checks: dict[str, bool] = {}
    with MANIFEST.open(newline="") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            path = ROOT / row["path"]
            checks[row["path"]] = path.is_file() and sha256(path) == row["sha256"]
    if not checks or not all(checks.values()):
        raise AssertionError(f"source hash failure: {checks}")
    return checks


def precision(covariance: np.ndarray) -> np.ndarray:
    factor = cho_factor(covariance, lower=True, check_finite=True)
    return cho_solve(factor, np.eye(covariance.shape[0]), check_finite=True)


def combine(first: dict, second: dict) -> dict:
    theta_p = np.asarray(first["theta"], dtype=np.float64)
    theta_d = np.asarray(second["theta"], dtype=np.float64)
    covariance_p = np.asarray(first["theta_covariance"], dtype=np.float64)
    covariance_d = np.asarray(second["theta_covariance"], dtype=np.float64)
    precision_p = precision(covariance_p)
    precision_d = precision(covariance_d)
    total_precision = precision_p + precision_d
    total_factor = cho_factor(total_precision, lower=True, check_finite=True)
    joint_covariance = cho_solve(
        total_factor, np.eye(total_precision.shape[0]), check_finite=True
    )
    joint_theta = cho_solve(
        total_factor, precision_p @ theta_p + precision_d @ theta_d, check_finite=True
    )
    residual_p = theta_p - joint_theta
    residual_d = theta_d - joint_theta
    quadratic = float(residual_p @ precision_p @ residual_p + residual_d @ precision_d @ residual_d)
    relative_r = np.power(10.0, joint_theta / 5.0)
    jacobian = np.diag((math.log(10.0) / 5.0) * relative_r)
    relative_r_covariance = jacobian @ joint_covariance @ jacobian
    return {
        "theta": joint_theta,
        "theta_covariance": joint_covariance,
        "theta_se": np.sqrt(np.diag(joint_covariance)),
        "relative_R": relative_r,
        "relative_R_covariance_delta_method": relative_r_covariance,
        "relative_R_se_delta_method": np.sqrt(np.diag(relative_r_covariance)),
        "two_estimate_quadratic": quadratic,
    }


def serial(value):
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, dict):
        return {key: serial(item) for key, item in value.items()}
    return value


def main() -> None:
    source_hashes = verify_sources()
    g236 = json.loads(SOURCE.read_text())
    if g236["status"] != "PASS" or g236["landing"] != "DUAL_SNE_RELATIONAL_STATE_CONCORDANCE_LEAD":
        raise AssertionError("G236 landing changed")
    resolutions: dict[str, dict] = {}
    rows: list[dict] = []
    controls: dict[str, bool | float] = {}
    for k in K_VALUES:
        source = g236["resolutions"][str(k)]
        joint = combine(source["pantheon"], source["des"])
        knots = np.asarray(source["knots"], dtype=np.float64)
        expected_shape = float(source["comparison"]["chi2"])
        identity_residual = abs(joint["two_estimate_quadratic"] - expected_shape)
        joint_raw_chi2 = float(
            source["pantheon"]["chi2"] + source["des"]["chi2"] + joint["two_estimate_quadratic"]
        )
        dof = int(source["pantheon"]["n"] + source["des"]["n"] - (k + 1))
        ceiling = float(dof + 5.0 * math.sqrt(2.0 * dof))

        duplicate = combine(source["pantheon"], source["pantheon"])
        duplicate_theta_error = float(
            np.max(np.abs(np.asarray(duplicate["theta"]) - np.asarray(source["pantheon"]["theta"])))
        )
        duplicate_covariance_error = float(
            np.max(
                np.abs(
                    np.asarray(duplicate["theta_covariance"])
                    - 0.5 * np.asarray(source["pantheon"]["theta_covariance"])
                )
            )
        )
        swapped = combine(source["des"], source["pantheon"])
        swap_error = float(np.max(np.abs(np.asarray(swapped["theta"]) - joint["theta"])))
        weak_des = dict(source["des"])
        weak_des["theta_covariance"] = (
            1.0e12 * np.asarray(source["des"]["theta_covariance"], dtype=np.float64)
        ).tolist()
        limiting = combine(source["pantheon"], weak_des)
        weak_limit_error = float(
            np.max(np.abs(np.asarray(limiting["theta"]) - np.asarray(source["pantheon"]["theta"])))
        )
        controls[f"K{k}_identity_residual"] = identity_residual
        controls[f"K{k}_duplicate_theta_error"] = duplicate_theta_error
        controls[f"K{k}_duplicate_covariance_error"] = duplicate_covariance_error
        controls[f"K{k}_swap_error"] = swap_error
        controls[f"K{k}_weak_limit_error"] = weak_limit_error
        controls[f"K{k}_joint_raw_adequate"] = bool(joint_raw_chi2 <= ceiling)
        resolutions[str(k)] = serial(
            {
                "knots": knots,
                **joint,
                "shape_identity_residual": identity_residual,
                "joint_raw_chi2": joint_raw_chi2,
                "joint_raw_dof": dof,
                "joint_raw_ceiling": ceiling,
                "joint_raw_adequate": bool(joint_raw_chi2 <= ceiling),
            }
        )
        for index in range(1, k):
            rows.append(
                {
                    "K": k,
                    "knot_index": index,
                    "phi": knots[index],
                    "z": math.expm1(knots[index]),
                    "joint_relative_shape_mag": joint["theta"][index - 1],
                    "joint_shape_se": joint["theta_se"][index - 1],
                    "relative_R": joint["relative_R"][index - 1],
                    "relative_R_se_delta_method": joint["relative_R_se_delta_method"][index - 1],
                }
            )
    boolean_gates = [value for value in controls.values() if isinstance(value, bool)]
    numeric_gates = [
        value <= 1.0e-8
        for key, value in controls.items()
        if isinstance(value, float) and not key.endswith("weak_limit_error")
    ]
    weak_gates = [
        value <= 1.0e-8 for key, value in controls.items() if key.endswith("weak_limit_error")
    ]
    status = "PASS" if all(boolean_gates + numeric_gates + weak_gates) else "FAIL"
    result = {
        "audit": "G237_JOINT_STATE_PRODUCTION",
        "status": status,
        "landing": "JOINT_DUAL_SNE_RELATIVE_STATE_FROZEN_WITH_CAVEATS",
        "question_type": "OBSERVATIONAL_STATE_ASSEMBLY_NOT_PROFILE_LAW",
        "cross_release_covariance": "CHOSE_ZERO_AFTER_EXACT_CID_DEOVERLAP__UNKNOWN_SHARED_SYSTEMATICS_OPEN",
        "source_hashes": source_hashes,
        "controls": controls,
        "resolutions": resolutions,
        "primary_resolution": 12,
        "state_rows": len(rows),
        "maximum_conclusion": "joint finite-resolution processed SNe relative state under the bounded query and chosen cross-release covariance only",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    with TABLE.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    primary = {
        "freeze": "G237_PRIMARY_K12_RELATIVE_STATE__NO_REFIT_ON_HELDOUT_QUERY",
        "epistemic_grade": "OBSERVED_PROCESSED_CONDITIONAL",
        "cross_release_covariance": result["cross_release_covariance"],
        "query": "STATIC_CENTRAL_PLUS_IMPORTED_TRANSPARENT_TRANSFER",
        "phi_anchor": resolutions["12"]["knots"][0],
        "theta_anchor": 0.0,
        "resolution": 12,
        "state": resolutions["12"],
        "forbidden_use": "NO_PROFILE_LAW_INTERPOLATION_REFIT_P1_XMAX_LCDM_DISTANCE_OR_UDT_VALIDATION",
    }
    FREEZE.write_text(json.dumps(primary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
