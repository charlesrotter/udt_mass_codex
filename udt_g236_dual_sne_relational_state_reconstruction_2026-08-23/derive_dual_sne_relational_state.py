#!/usr/bin/env python3
"""G236 production reconstruction of a processed dual-SNe relational state."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
from pathlib import Path

import numpy as np
from scipy.linalg import cho_factor, cho_solve, solve_triangular


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
DES_ROOT = Path(os.environ["G236_DES_ROOT"]).resolve()
MANIFEST = PACKAGE / "SOURCE_MANIFEST.tsv"
OUT_JSON = PACKAGE / "PRODUCTION_RESULT.json"
OUT_TSV = PACKAGE / "STATE_RECONSTRUCTION.tsv"
P_TABLE = ROOT / "Data/Pantheon+SH0ES.dat"
P_COV = ROOT / "Data/Pantheon+SH0ES_STAT+SYS.cov"
DES_TABLE = DES_ROOT / "DES-Dovekie_HD.csv"
DES_PRECISION = DES_ROOT / "STAT+SYS.npz"
DES_README = DES_ROOT / "README.md"

K_VALUES = (8, 12, 16, 24)
PRIMARY_K = 12
EXPECTED_P = 768
EXPECTED_D = 1623
EXPECTED_DES_PHI_MIN = 0.07077528204904217
EXPECTED_DES_PHI_MAX = 0.7627571949083936


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def resolve_manifest_path(logical: str) -> Path:
    if logical == "external_data/README.md":
        return DES_README
    if logical == "external_data/DES-Dovekie_HD.csv":
        return DES_TABLE
    if logical == "external_data/STAT+SYS.npz":
        return DES_PRECISION
    return ROOT / logical


def verify_sources() -> dict[str, bool]:
    checks: dict[str, bool] = {}
    with MANIFEST.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            path = resolve_manifest_path(row["path"])
            checks[row["path"]] = path.is_file() and sha256(path) == row["sha256"]
    if not checks or not all(checks.values()):
        raise AssertionError(f"source hash failure: {checks}")
    return checks


def read_pantheon() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    table = np.genfromtxt(P_TABLE, names=True, dtype=None, encoding="utf-8")
    z = np.asarray(table["zCMB"], dtype=np.float64)
    magnitude = np.asarray(table["m_b_corr"], dtype=np.float64)
    calibrator = np.asarray(table["IS_CALIBRATOR"], dtype=np.int64)
    survey = np.asarray(table["IDSURVEY"], dtype=np.int64)
    cid = np.asarray(table["CID"], dtype=str)
    with P_COV.open() as handle:
        dimension = int(handle.readline())
        values = np.fromfile(handle, sep=" ")
    covariance = values.reshape(dimension, dimension)
    covariance = 0.5 * (covariance + covariance.T)
    return z, magnitude, covariance, calibrator, np.rec.fromarrays([cid, survey], names="cid,survey")


def read_des() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    names: list[str] | None = None
    rows: list[list[str]] = []
    with DES_TABLE.open() as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("VARNAMES:"):
                names = line.split()[1:]
                continue
            if names is None or not line.startswith("SN:"):
                raise ValueError("unexpected DES table format")
            rows.append(line.split()[1:])
    assert names is not None
    index = {name: i for i, name in enumerate(names)}
    cid = np.asarray([row[index["CID"]] for row in rows], dtype=str)
    survey = np.asarray([int(float(row[index["IDSURVEY"]])) for row in rows], dtype=np.int64)
    z = np.asarray([float(row[index["zHD"]]) for row in rows], dtype=np.float64)
    magnitude = np.asarray([float(row[index["MU"]]) for row in rows], dtype=np.float64)
    with np.load(DES_PRECISION, allow_pickle=False) as archive:
        dimension = int(archive["nsn"][0])
        packed = np.asarray(archive["cov"], dtype=np.float64)
    if dimension != len(rows):
        raise AssertionError((dimension, len(rows)))
    precision = np.zeros((dimension, dimension), dtype=np.float64)
    upper = np.triu_indices(dimension)
    precision[upper] = packed
    precision[(upper[1], upper[0])] = packed
    precision = 0.5 * (precision + precision.T)
    return z, magnitude, precision, survey, cid


def marginal_covariance_from_precision(precision: np.ndarray, keep: np.ndarray) -> np.ndarray:
    factor = cho_factor(precision, lower=True, check_finite=True)
    full_covariance = cho_solve(factor, np.eye(precision.shape[0]), check_finite=True)
    answer = full_covariance[np.ix_(keep, keep)]
    return 0.5 * (answer + answer.T)


def hat_basis(phi: np.ndarray, knots: np.ndarray) -> np.ndarray:
    if np.min(phi) < knots[0] - 1e-13 or np.max(phi) > knots[-1] + 1e-13:
        raise AssertionError("basis extrapolation attempted")
    n = phi.size
    k = knots.size
    basis = np.zeros((n, k), dtype=np.float64)
    segment = np.searchsorted(knots, phi, side="right") - 1
    segment = np.clip(segment, 0, k - 2)
    width = knots[segment + 1] - knots[segment]
    right = (phi - knots[segment]) / width
    basis[np.arange(n), segment] = 1.0 - right
    basis[np.arange(n), segment + 1] = right
    return basis


def fit_state(phi: np.ndarray, observed: np.ndarray, covariance: np.ndarray, knots: np.ndarray) -> dict:
    basis = hat_basis(phi, knots)
    design = np.column_stack([np.ones(phi.size), basis[:, 1:]])
    lower = np.linalg.cholesky(covariance)
    white_design = solve_triangular(lower, design, lower=True, check_finite=True)
    white_observed = solve_triangular(lower, observed, lower=True, check_finite=True)
    normal = white_design.T @ white_design
    rhs = white_design.T @ white_observed
    normal_factor = cho_factor(normal, lower=True, check_finite=True)
    coefficients = cho_solve(normal_factor, rhs, check_finite=True)
    covariance_coefficients = cho_solve(
        normal_factor, np.eye(normal.shape[0]), check_finite=True
    )
    residual_white = white_observed - white_design @ coefficients
    chi2 = float(residual_white @ residual_white)
    dof = int(phi.size - knots.size)
    ceiling = float(dof + 5.0 * math.sqrt(2.0 * dof))
    return {
        "n": int(phi.size),
        "dof": dof,
        "chi2": chi2,
        "ceiling": ceiling,
        "adequate": bool(chi2 <= ceiling),
        "offset": float(coefficients[0]),
        "theta": coefficients[1:],
        "theta_covariance": covariance_coefficients[1:, 1:],
    }


def compare_shapes(first: dict, second: dict, k: int) -> dict:
    difference = np.asarray(first["theta"]) - np.asarray(second["theta"])
    covariance = np.asarray(first["theta_covariance"]) + np.asarray(second["theta_covariance"])
    factor = cho_factor(covariance, lower=True, check_finite=True)
    chi2 = float(difference @ cho_solve(factor, difference, check_finite=True))
    dof = k - 1
    ceiling = float(dof + 5.0 * math.sqrt(2.0 * dof))
    return {
        "difference": difference,
        "difference_covariance": covariance,
        "chi2": chi2,
        "dof": dof,
        "ceiling": ceiling,
        "concordant": bool(chi2 <= ceiling),
    }


def serial_fit(fit: dict) -> dict:
    return {
        key: (value.tolist() if isinstance(value, np.ndarray) else value)
        for key, value in fit.items()
    }


def main() -> None:
    source_hashes = verify_sources()
    p_z_all, p_mag_all, p_cov_all, p_calibrator, p_id = read_pantheon()
    d_z_all, d_mag_all, d_precision, d_survey, d_cid = read_des()

    d_keep = np.flatnonzero(d_survey == 10)
    d_z = d_z_all[d_keep]
    d_mag = d_mag_all[d_keep]
    d_cov = marginal_covariance_from_precision(d_precision, d_keep)
    phi_min = float(np.log1p(np.min(d_z)))
    phi_max = float(np.log1p(np.max(d_z)))
    if not math.isclose(phi_min, EXPECTED_DES_PHI_MIN, rel_tol=0.0, abs_tol=1e-15):
        raise AssertionError(phi_min)
    if not math.isclose(phi_max, EXPECTED_DES_PHI_MAX, rel_tol=0.0, abs_tol=1e-15):
        raise AssertionError(phi_max)

    p_base = (
        (p_z_all > 0.023)
        & (p_calibrator == 0)
        & (p_id.survey != 10)
        & (np.log1p(p_z_all) >= phi_min)
        & (np.log1p(p_z_all) <= phi_max)
    )
    p_keep = np.flatnonzero(p_base)
    p_z = p_z_all[p_keep]
    p_mag = p_mag_all[p_keep]
    p_cov = p_cov_all[np.ix_(p_keep, p_keep)]
    if p_z.size != EXPECTED_P or d_z.size != EXPECTED_D:
        raise AssertionError((p_z.size, d_z.size))

    p_overlap_ids = set(p_id.cid[(p_z_all > 0.023) & (p_calibrator == 0) & (p_id.survey == 10)])
    d_ids = set(d_cid[d_keep])
    exact_overlap = len(p_overlap_ids & d_ids)
    if exact_overlap != 148:
        raise AssertionError(exact_overlap)

    p_phi = np.log1p(p_z)
    d_phi = np.log1p(d_z)
    p_y = p_mag - 10.0 * np.log10(1.0 + p_z)
    d_y = d_mag - 10.0 * np.log10(1.0 + d_z)

    resolutions: dict[str, dict] = {}
    tsv_rows: list[list[object]] = []
    for k in K_VALUES:
        knots = np.linspace(phi_min, phi_max, k)
        p_fit = fit_state(p_phi, p_y, p_cov, knots)
        d_fit = fit_state(d_phi, d_y, d_cov, knots)
        comparison = compare_shapes(p_fit, d_fit, k)
        classification = (
            f"PROCESSED_RELEASE_SHAPES_CONCORDANT_AT_RESOLUTION_{k}"
            if p_fit["adequate"] and d_fit["adequate"] and comparison["concordant"]
            else (
                f"PROCESSED_RELEASE_SHAPES_IN_TENSION_AT_RESOLUTION_{k}"
                if p_fit["adequate"] and d_fit["adequate"]
                else f"RECONSTRUCTION_INADEQUATE_AT_RESOLUTION_{k}"
            )
        )
        resolutions[str(k)] = {
            "knots": knots.tolist(),
            "pantheon": serial_fit(p_fit),
            "des": serial_fit(d_fit),
            "comparison": serial_fit(comparison),
            "classification": classification,
        }
        p_se = np.sqrt(np.diag(np.asarray(p_fit["theta_covariance"])))
        d_se = np.sqrt(np.diag(np.asarray(d_fit["theta_covariance"])))
        diff_se = np.sqrt(np.diag(np.asarray(comparison["difference_covariance"])))
        for j in range(1, k):
            tsv_rows.append(
                [
                    k,
                    j,
                    knots[j],
                    math.expm1(knots[j]),
                    p_fit["theta"][j - 1],
                    p_se[j - 1],
                    d_fit["theta"][j - 1],
                    d_se[j - 1],
                    comparison["difference"][j - 1],
                    diff_se[j - 1],
                ]
            )

    primary = resolutions[str(PRIMARY_K)]
    k12_knots = np.asarray(primary["knots"], dtype=np.float64)
    d_fit_raw = fit_state(d_phi, d_y, d_cov, k12_knots)
    duplicate = compare_shapes(d_fit_raw, d_fit_raw, PRIMARY_K)
    unit_depth = (d_phi - phi_min) / (phi_max - phi_min)
    d_fit_slope = fit_state(d_phi, d_y + 0.5 * unit_depth, d_cov, k12_knots)
    slope_comparison = compare_shapes(d_fit_raw, d_fit_slope, PRIMARY_K)

    order = np.argsort(d_phi)
    d_phi_sorted = d_phi[order]
    d_y_sorted = d_y[order]
    d_cov_sorted = d_cov[np.ix_(order, order)]
    d_fit_sorted = fit_state(d_phi_sorted, d_y_sorted, d_cov_sorted, k12_knots)
    d_phi_rolled = np.roll(d_phi_sorted, d_phi_sorted.size // 2)
    d_fit_rolled = fit_state(d_phi_rolled, d_y_sorted, d_cov_sorted, k12_knots)

    adequate = [entry for entry in resolutions.values() if entry["pantheon"]["adequate"] and entry["des"]["adequate"]]
    all_adequate_concordant = bool(adequate) and all(entry["comparison"]["concordant"] for entry in adequate)
    all_adequate_tension = bool(adequate) and all(not entry["comparison"]["concordant"] for entry in adequate)
    k12_adequate = bool(primary["pantheon"]["adequate"] and primary["des"]["adequate"])
    k24 = resolutions["24"]
    k24_adequate = bool(k24["pantheon"]["adequate"] and k24["des"]["adequate"])
    if k12_adequate and all_adequate_concordant:
        landing = "DUAL_SNE_RELATIONAL_STATE_CONCORDANCE_LEAD"
    elif k12_adequate and all_adequate_tension:
        landing = "DUAL_SNE_PROCESSED_STATE_TENSION"
    elif not k12_adequate and not k24_adequate:
        landing = "REGISTERED_RECONSTRUCTION_RESOLUTION_INADEQUATE"
    else:
        landing = "RESOLUTION_SENSITIVE_OR_INCONCLUSIVE"

    hostile = {
        "duplicate_shape_chi2": duplicate["chi2"],
        "duplicate_pass": bool(duplicate["chi2"] <= 1e-10),
        "slope_mutation_shape_chi2": slope_comparison["chi2"],
        "slope_mutation_ceiling": slope_comparison["ceiling"],
        "slope_mutation_pass": bool(slope_comparison["chi2"] > slope_comparison["ceiling"]),
        "roll_unmutated_chi2": d_fit_sorted["chi2"],
        "roll_mutated_chi2": d_fit_rolled["chi2"],
        "roll_ratio": float(d_fit_rolled["chi2"] / d_fit_sorted["chi2"]),
        "roll_mutation_pass": bool(d_fit_rolled["chi2"] > 2.0 * d_fit_sorted["chi2"]),
    }
    if not all(value for key, value in hostile.items() if key.endswith("_pass")):
        raise AssertionError(hostile)

    result = {
        "audit": "G236_PRODUCTION",
        "status": "PASS",
        "landing": landing,
        "question_type": "OBSERVATIONAL_PROCESSED_STATE_RECONSTRUCTION_NOT_PROFILE_LAW",
        "transformation": "phi=log(1+z); y=m-10log10(1+z)=5log10R(phi)+catalog_offset",
        "transfer_status": "IMPORTED_CONDITIONAL_eta_1_epsilon_1_over_Z",
        "samples": {
            "pantheon_non_des_common_support": int(p_z.size),
            "des_only": int(d_z.size),
            "excluded_pantheon_survey10": int(np.sum((p_z_all > 0.023) & (p_calibrator == 0) & (p_id.survey == 10))),
            "exact_cid_overlap": exact_overlap,
            "phi_min": phi_min,
            "phi_max": phi_max,
        },
        "source_hashes": source_hashes,
        "resolutions": resolutions,
        "hostile_controls": hostile,
        "checks": {
            "no_extrapolation": True,
            "p1_not_used": True,
            "xmax_not_used": True,
            "lcdm_distance_not_used": True,
            "no_profile_optimizer": True,
            "one_offset_per_catalog": True,
            "full_covariance_used": True,
            "processed_release_caveat_retained": True,
        },
        "maximum_conclusion": "bounded processed-release relative R(phi) state concordance or tension under the static central query and imported transfer only",
    }
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    with OUT_TSV.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(
            [
                "K",
                "knot_index",
                "phi",
                "z",
                "pantheon_relative_shape_mag",
                "pantheon_se",
                "des_relative_shape_mag",
                "des_se",
                "difference_mag",
                "difference_se",
            ]
        )
        writer.writerows(tsv_rows)
    print(json.dumps({"status": "PASS", "landing": landing, "hostile_controls": hostile}, indent=2))


if __name__ == "__main__":
    main()
