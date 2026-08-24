#!/usr/bin/env python3
"""Production G243 SNe-only radial spline representation."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.interpolate import BSpline
from scipy.linalg import cho_factor, cho_solve, solve_triangular


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
DES_ROOT = Path(os.environ["G243_DES_ROOT"]).resolve()
P_TABLE = ROOT / "Data/Pantheon+SH0ES.dat"
P_COV = ROOT / "Data/Pantheon+SH0ES_STAT+SYS.cov"
DES_TABLE = DES_ROOT / "DES-Dovekie_HD.csv"
DES_PRECISION = DES_ROOT / "STAT+SYS.npz"
MANIFEST = PACKAGE / "SOURCE_MANIFEST.tsv"
RESULT_PATH = PACKAGE / "DERIVATION_RESULT.json"
CENSUS_PATH = PACKAGE / "CANDIDATE_CENSUS.tsv"
REPRESENTATION_PATH = PACKAGE / "RADIAL_REPRESENTATION.npz"

BASIS_COUNTS = (16, 24, 32, 48, 64)
LOG10_ALPHA = np.arange(-12.0, 12.0000001, 0.25, dtype=np.float64)
EXPECTED_P = 768
EXPECTED_D = 1623
EXPECTED_PHI_MIN = 0.07077528204904217
EXPECTED_PHI_MAX = 0.7627571949083936


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def preregistration_registry_digest(path: Path) -> str:
    """Retain preregistration lineage after the append-only G243 bank."""
    lines = path.read_bytes().splitlines(keepends=True)
    g243_rows = [line for line in lines if line.startswith(b"G243\t")]
    if not g243_rows:
        return sha256(path)
    if len(g243_rows) != 1:
        raise RuntimeError("registry may contain at most one G243 row")
    historical = b"".join(line for line in lines if not line.startswith(b"G243\t"))
    return hashlib.sha256(historical).hexdigest()


def resolve_manifest_path(logical: str) -> Path:
    if logical == "external_data/DES-Dovekie_HD.csv":
        return DES_TABLE
    if logical == "external_data/STAT+SYS.npz":
        return DES_PRECISION
    return ROOT / logical


def verify_manifest() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with MANIFEST.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            source = resolve_manifest_path(row["path"])
            actual = (
                preregistration_registry_digest(source)
                if row["path"] == "CURRENT_SCIENTIFIC_PREMISES.tsv"
                else sha256(source)
            )
            if actual != row["sha256"]:
                raise RuntimeError(f"source hash mismatch: {row['path']}")
            rows.append({"path": row["path"], "role": row["role"], "sha256": actual})
    if len(rows) != 8:
        raise RuntimeError("unexpected G243 source count")
    return rows


def read_pantheon() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
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
    return z, magnitude, covariance, calibrator, survey, cid


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
    if names is None:
        raise RuntimeError("missing DES VARNAMES")
    index = {name: i for i, name in enumerate(names)}
    cid = np.asarray([row[index["CID"]] for row in rows], dtype=str)
    survey = np.asarray([int(float(row[index["IDSURVEY"]])) for row in rows], dtype=np.int64)
    z = np.asarray([float(row[index["zHD"]]) for row in rows], dtype=np.float64)
    magnitude = np.asarray([float(row[index["MU"]]) for row in rows], dtype=np.float64)
    with np.load(DES_PRECISION, allow_pickle=False) as archive:
        dimension = int(archive["nsn"][0])
        packed = np.asarray(archive["cov"], dtype=np.float64)
    if dimension != len(rows):
        raise RuntimeError("DES precision dimension mismatch")
    precision = np.zeros((dimension, dimension), dtype=np.float64)
    upper = np.triu_indices(dimension)
    precision[upper] = packed
    precision[(upper[1], upper[0])] = packed
    precision = 0.5 * (precision + precision.T)
    return z, magnitude, precision, survey, cid


def marginal_covariance_from_precision(precision: np.ndarray, keep: np.ndarray) -> np.ndarray:
    factor = cho_factor(precision, lower=True, check_finite=True)
    columns = np.zeros((precision.shape[0], keep.size), dtype=np.float64)
    columns[keep, np.arange(keep.size)] = 1.0
    selected_columns = cho_solve(factor, columns, check_finite=True)
    covariance = selected_columns[keep, :]
    return 0.5 * (covariance + covariance.T)


def load_release_state() -> dict[str, np.ndarray | int | float]:
    p_z_all, p_mag_all, p_cov_all, p_calibrator, p_survey, p_cid = read_pantheon()
    d_z_all, d_mag_all, d_precision, d_survey, d_cid = read_des()
    d_keep = np.flatnonzero(d_survey == 10)
    d_z = d_z_all[d_keep]
    d_mag = d_mag_all[d_keep]
    d_cov = marginal_covariance_from_precision(d_precision, d_keep)
    phi_min = float(np.log1p(np.min(d_z)))
    phi_max = float(np.log1p(np.max(d_z)))
    if not math.isclose(phi_min, EXPECTED_PHI_MIN, rel_tol=0.0, abs_tol=1.0e-15):
        raise RuntimeError("unexpected minimum depth")
    if not math.isclose(phi_max, EXPECTED_PHI_MAX, rel_tol=0.0, abs_tol=1.0e-15):
        raise RuntimeError("unexpected maximum depth")
    p_keep = np.flatnonzero(
        (p_z_all > 0.023)
        & (p_calibrator == 0)
        & (p_survey != 10)
        & (np.log1p(p_z_all) >= phi_min)
        & (np.log1p(p_z_all) <= phi_max)
    )
    p_z = p_z_all[p_keep]
    p_mag = p_mag_all[p_keep]
    p_cov = p_cov_all[np.ix_(p_keep, p_keep)]
    if p_z.size != EXPECTED_P or d_z.size != EXPECTED_D:
        raise RuntimeError("unexpected release counts")
    overlap_pool = set(p_cid[(p_z_all > 0.023) & (p_calibrator == 0) & (p_survey == 10)])
    if len(overlap_pool & set(d_cid[d_keep])) != 148:
        raise RuntimeError("unexpected exact-CID overlap count")
    return {
        "p_phi": np.log1p(p_z),
        "p_y": p_mag - 10.0 * np.log10(1.0 + p_z),
        "p_cov": p_cov,
        "d_phi": np.log1p(d_z),
        "d_y": d_mag - 10.0 * np.log10(1.0 + d_z),
        "d_cov": d_cov,
        "phi_min": phi_min,
        "phi_max": phi_max,
    }


def spline_system(phi_min: float, phi_max: float, basis_count: int) -> tuple[BSpline, np.ndarray]:
    degree = 3
    interior = np.linspace(phi_min, phi_max, basis_count - 2, dtype=np.float64)[1:-1]
    knot_vector = np.concatenate(
        [np.repeat(phi_min, degree + 1), interior, np.repeat(phi_max, degree + 1)]
    )
    spline = BSpline(knot_vector, np.eye(basis_count), degree, extrapolate=False)
    return spline, knot_vector


def anchored_basis(spline: BSpline, phi: np.ndarray, phi_anchor: float, derivative: int = 0) -> np.ndarray:
    evaluator = spline.derivative(derivative) if derivative else spline
    values = np.asarray(evaluator(phi), dtype=np.float64)
    if derivative == 0:
        anchor = np.asarray(evaluator(phi_anchor), dtype=np.float64)
        values = values - anchor
    return values[:, :-1]


def roughness_penalty(spline: BSpline, knot_vector: np.ndarray) -> np.ndarray:
    nodes, weights = leggauss(8)
    unique = np.unique(knot_vector)
    size = spline.c.shape[0] - 1
    penalty = np.zeros((size, size), dtype=np.float64)
    second = spline.derivative(2)
    for left, right in zip(unique[:-1], unique[1:]):
        if right <= left:
            continue
        points = 0.5 * (right - left) * nodes + 0.5 * (right + left)
        local_weights = 0.5 * (right - left) * weights
        values = np.asarray(second(points), dtype=np.float64)[:, :-1]
        penalty += values.T @ (local_weights[:, None] * values)
    return 0.5 * (penalty + penalty.T)


def whiten_design(state: dict[str, np.ndarray | int | float], spline: BSpline) -> dict[str, np.ndarray]:
    phi_anchor = float(state["phi_min"])
    p_phi = np.asarray(state["p_phi"])
    d_phi = np.asarray(state["d_phi"])
    p_shape = anchored_basis(spline, p_phi, phi_anchor)
    d_shape = anchored_basis(spline, d_phi, phi_anchor)
    p_design = np.column_stack([np.ones(p_phi.size), np.zeros(p_phi.size), p_shape])
    d_design = np.column_stack([np.zeros(d_phi.size), np.ones(d_phi.size), d_shape])
    p_lower = np.linalg.cholesky(np.asarray(state["p_cov"]))
    d_lower = np.linalg.cholesky(np.asarray(state["d_cov"]))
    p_white_design = solve_triangular(p_lower, p_design, lower=True, check_finite=True)
    d_white_design = solve_triangular(d_lower, d_design, lower=True, check_finite=True)
    p_white_y = solve_triangular(p_lower, np.asarray(state["p_y"]), lower=True, check_finite=True)
    d_white_y = solve_triangular(d_lower, np.asarray(state["d_y"]), lower=True, check_finite=True)
    return {
        "design": np.vstack([p_white_design, d_white_design]),
        "observed": np.concatenate([p_white_y, d_white_y]),
        "p_design": p_white_design,
        "d_design": d_white_design,
        "p_observed": p_white_y,
        "d_observed": d_white_y,
    }


def analytic_penalty_nullspace(spline: BSpline) -> np.ndarray:
    """Return the two release offsets and exact anchored-affine spline mode."""
    basis_count = int(spline.c.shape[0])
    greville = np.asarray(
        [np.mean(spline.t[index + 1 : index + spline.k + 1]) for index in range(basis_count)],
        dtype=np.float64,
    )
    nullspace = np.zeros((basis_count + 1, 3), dtype=np.float64)
    nullspace[0, 0] = 1.0
    nullspace[1, 1] = 1.0
    nullspace[2:, 2] = greville[:-1] - greville[-1]
    return nullspace


def stable_penalty_coordinates(
    normal: np.ndarray, penalty: np.ndarray, rhs: np.ndarray, spline: BSpline
) -> dict[str, np.ndarray]:
    """Eliminate the exact penalty nullspace, then whiten the positive block."""
    nullspace = analytic_penalty_nullspace(spline)
    tolerance = 1.0e-10 * max(1.0, float(np.linalg.norm(penalty)))
    if float(np.linalg.norm(penalty @ nullspace)) > tolerance:
        raise RuntimeError("analytic affine mode is not in the roughness nullspace")
    orthogonal, _ = np.linalg.qr(nullspace, mode="complete")
    q_null = orthogonal[:, :3]
    q_penalized = orthogonal[:, 3:]
    a_zz = q_null.T @ normal @ q_null
    a_zr = q_null.T @ normal @ q_penalized
    a_rr = q_penalized.T @ normal @ q_penalized
    b_z = q_null.T @ rhs
    b_r = q_penalized.T @ rhs
    zz_factor = cho_factor(a_zz, lower=True, check_finite=True)
    zz_inverse_zr = cho_solve(zz_factor, a_zr, check_finite=True)
    zz_inverse_b = cho_solve(zz_factor, b_z, check_finite=True)
    reduced_normal = a_rr - a_zr.T @ zz_inverse_zr
    reduced_normal = 0.5 * (reduced_normal + reduced_normal.T)
    reduced_rhs = b_r - a_zr.T @ zz_inverse_b
    reduced_penalty = q_penalized.T @ penalty @ q_penalized
    reduced_penalty = 0.5 * (reduced_penalty + reduced_penalty.T)

    lower = np.linalg.cholesky(reduced_normal)
    left_whitened = solve_triangular(lower, reduced_penalty, lower=True, check_finite=True)
    whitened_penalty = solve_triangular(
        lower, left_whitened.T, lower=True, check_finite=True
    ).T
    whitened_penalty = 0.5 * (whitened_penalty + whitened_penalty.T)
    eigenvalues, eigenvectors = np.linalg.eigh(whitened_penalty)
    eigen_tolerance = 1000.0 * np.finfo(np.float64).eps * max(
        1.0, float(np.max(np.abs(eigenvalues)))
    )
    if float(np.min(eigenvalues)) < -eigen_tolerance:
        raise RuntimeError("roughness penalty lost positive semidefiniteness")
    eigenvalues = np.maximum(eigenvalues, 0.0)
    if not float(np.min(eigenvalues)) > 0.0:
        raise RuntimeError("reduced roughness penalty is not positive definite")
    transformed_rhs = solve_triangular(lower, reduced_rhs, lower=True, check_finite=True)
    projected_rhs = eigenvectors.T @ transformed_rhs
    return {
        "q_null": q_null,
        "q_penalized": q_penalized,
        "a_zz": a_zz,
        "a_zr": a_zr,
        "b_z": b_z,
        "lower": lower,
        "eigenvalues": eigenvalues,
        "eigenvectors": eigenvectors,
        "projected_rhs": projected_rhs,
    }


def spectral_coefficients(coordinates: dict[str, np.ndarray], regularization: float) -> tuple[np.ndarray, float]:
    inverse_weights = 1.0 / (1.0 + regularization * coordinates["eigenvalues"])
    whitened_penalized = coordinates["eigenvectors"] @ (
        inverse_weights * coordinates["projected_rhs"]
    )
    penalized = solve_triangular(
        coordinates["lower"].T, whitened_penalized, lower=False, check_finite=True
    )
    null = np.linalg.solve(
        coordinates["a_zz"], coordinates["b_z"] - coordinates["a_zr"] @ penalized
    )
    coefficients = coordinates["q_null"] @ null + coordinates["q_penalized"] @ penalized
    return coefficients, float(3.0 + np.sum(inverse_weights))


def evaluate_basis(state: dict[str, np.ndarray | int | float], basis_count: int) -> dict[str, object]:
    phi_min = float(state["phi_min"])
    phi_max = float(state["phi_max"])
    spline, knot_vector = spline_system(phi_min, phi_max, basis_count)
    white = whiten_design(state, spline)
    design = white["design"]
    observed = white["observed"]
    long_design = design.astype(np.longdouble)
    normal = np.asarray(long_design.T @ long_design, dtype=np.float64)
    rhs = np.asarray(long_design.T @ observed.astype(np.longdouble), dtype=np.float64)
    penalty_shape = roughness_penalty(spline, knot_vector)
    penalty = np.zeros_like(normal)
    penalty[2:, 2:] = penalty_shape
    scale = float(np.trace(normal[2:, 2:]) / np.trace(penalty_shape))
    coordinates = stable_penalty_coordinates(normal, penalty, rhs, spline)
    candidates: list[dict[str, object]] = []
    for index, log_alpha in enumerate(LOG10_ALPHA):
        alpha = float(10.0**log_alpha)
        regularization = alpha * scale
        coefficients, edf = spectral_coefficients(coordinates, regularization)
        residual = observed - design @ coefficients
        raw_chi2 = float(residual @ residual)
        denominator = observed.size - edf
        gcv = float(observed.size * raw_chi2 / (denominator * denominator))
        candidates.append(
            {
                "basis_count": basis_count,
                "alpha_index": index,
                "log10_alpha": float(log_alpha),
                "alpha": alpha,
                "lambda": float(regularization),
                "raw_chi2": raw_chi2,
                "edf": edf,
                "gcv": gcv,
                "coefficients": coefficients,
            }
        )
    best = min(candidates, key=lambda item: (float(item["gcv"]), int(item["alpha_index"])))
    coefficients = np.asarray(best["coefficients"])
    regularized = normal + float(best["lambda"]) * penalty
    factor = cho_factor(regularized, lower=True, check_finite=True)
    inverse_regularized = cho_solve(factor, np.eye(normal.shape[0]), check_finite=True)
    coefficient_covariance = inverse_regularized @ normal @ inverse_regularized
    p_residual = white["p_observed"] - white["p_design"] @ coefficients
    d_residual = white["d_observed"] - white["d_design"] @ coefficients
    return {
        "basis_count": basis_count,
        "spline": spline,
        "knot_vector": knot_vector,
        "normal": normal,
        "penalty": penalty,
        "scale": scale,
        "candidates": candidates,
        "best": best,
        "coefficient_covariance": coefficient_covariance,
        "condition_number": float(np.linalg.cond(regularized)),
        "pantheon_raw_chi2": float(p_residual @ p_residual),
        "des_raw_chi2": float(d_residual @ d_residual),
    }


def positive_intervals(grid: np.ndarray, derivative: np.ndarray) -> list[list[float]]:
    positive = derivative > 0.0
    intervals: list[list[float]] = []
    start: int | None = None
    for index, value in enumerate(positive):
        if value and start is None:
            start = index
        if start is not None and (not value or index == positive.size - 1):
            end = index if value and index == positive.size - 1 else index - 1
            intervals.append([float(grid[start]), float(grid[end])])
            start = None
    return intervals


def serial_candidate(candidate: dict[str, object]) -> dict[str, object]:
    return {key: value for key, value in candidate.items() if key != "coefficients"}


def evaluate() -> tuple[dict[str, object], dict[str, np.ndarray], list[dict[str, object]]]:
    manifest = verify_manifest()
    state = load_release_state()
    basis_results = [evaluate_basis(state, basis_count) for basis_count in BASIS_COUNTS]
    selected_result = min(
        basis_results,
        key=lambda item: (
            float(item["best"]["gcv"]),
            int(item["basis_count"]),
        ),
    )
    selected = selected_result["best"]
    selected_index = int(selected["alpha_index"])
    boundary = selected_index in (0, LOG10_ALPHA.size - 1)
    grid = np.linspace(float(state["phi_min"]), float(state["phi_max"]), 4097)
    spline = selected_result["spline"]
    shape_coefficients = np.asarray(selected["coefficients"])[2:]
    theta = anchored_basis(spline, grid, float(state["phi_min"])) @ shape_coefficients
    theta_prime = anchored_basis(spline, grid, float(state["phi_min"]), derivative=1) @ shape_coefficients
    theta_second = anchored_basis(spline, grid, float(state["phi_min"]), derivative=2) @ shape_coefficients
    conversion = math.log(10.0) / 5.0
    s_prime = conversion * theta_prime
    s_second = conversion * theta_second
    intervals = positive_intervals(grid, s_prime)
    globally_invertible = bool(np.min(s_prime) > 0.0)

    per_basis: list[dict[str, object]] = []
    sensitivity: dict[str, dict[str, float]] = {}
    for item in basis_results:
        best = item["best"]
        per_basis.append(
            {
                **serial_candidate(best),
                "condition_number": item["condition_number"],
                "pantheon_raw_chi2": item["pantheon_raw_chi2"],
                "des_raw_chi2": item["des_raw_chi2"],
                "alpha_boundary": int(best["alpha_index"]) in (0, LOG10_ALPHA.size - 1),
            }
        )
        other_coefficients = np.asarray(best["coefficients"])[2:]
        other_theta = anchored_basis(item["spline"], grid, float(state["phi_min"])) @ other_coefficients
        other_prime = anchored_basis(
            item["spline"], grid, float(state["phi_min"]), derivative=1
        ) @ other_coefficients
        sensitivity[str(item["basis_count"])] = {
            "maximum_abs_theta_difference_from_selected": float(np.max(np.abs(other_theta - theta))),
            "maximum_abs_theta_prime_difference_from_selected": float(np.max(np.abs(other_prime - theta_prime))),
        }

    if boundary:
        classification = "REGULARIZATION_MINIMUM_ON_REGISTERED_BOUNDARY__NO_FREEZE"
    elif globally_invertible:
        classification = "SNE_ONLY_SMOOTH_RADIAL_REPRESENTATION_FROZEN__GLOBALLY_INVERTIBLE"
    else:
        classification = "SNE_ONLY_SMOOTH_RADIAL_REPRESENTATION_FROZEN__TURNING_INTERVALS_RETAINED"

    summary = {
        "classification": classification,
        "method": "WHITENED_RELEASE_DESIGN__EXACT_NULLSPACE_SCHUR__SPECTRAL_POSITIVE_BLOCK",
        "epistemic_grade": "OBSERVED_PROCESSED_CONDITIONAL_OBSERVATIONAL_REPRESENTATION_ONLY",
        "redshift_role": "DIRECT_RECIPROCAL_DEPTH__NO_ANGULAR_INPUT",
        "angular_outcomes": "CLOSED_AND_UNUSED",
        "boss_outcomes": "CLOSED_AND_UNREAD",
        "manifest": manifest,
        "counts": {"pantheon": EXPECTED_P, "des": EXPECTED_D, "total": EXPECTED_P + EXPECTED_D},
        "phi_interval": [float(state["phi_min"]), float(state["phi_max"])],
        "basis_counts": list(BASIS_COUNTS),
        "log10_alpha_grid": [float(LOG10_ALPHA[0]), 0.25, float(LOG10_ALPHA[-1])],
        "selected": {
            **serial_candidate(selected),
            "condition_number": selected_result["condition_number"],
            "pantheon_raw_chi2": selected_result["pantheon_raw_chi2"],
            "des_raw_chi2": selected_result["des_raw_chi2"],
            "coefficients": np.asarray(selected["coefficients"]).tolist(),
            "coefficient_covariance_shape": list(np.asarray(selected_result["coefficient_covariance"]).shape),
            "coefficient_covariance_diagonal_minimum": float(
                np.min(np.diag(np.asarray(selected_result["coefficient_covariance"])))
            ),
            "coefficient_covariance_diagonal_maximum": float(
                np.max(np.diag(np.asarray(selected_result["coefficient_covariance"])))
            ),
            "knot_vector": np.asarray(selected_result["knot_vector"]).tolist(),
            "alpha_boundary": boundary,
            "minimum_s_prime": float(np.min(s_prime)),
            "maximum_s_prime": float(np.max(s_prime)),
            "positive_intervals": intervals,
            "globally_invertible": globally_invertible,
        },
        "per_basis_best": per_basis,
        "basis_sensitivity": sensitivity,
        "maximum_conclusion": (
            "SNE_ONLY_NUMERICAL_RADIAL_REPRESENTATION__NOT_PHYSICAL_HISTORY_TRANSFER_ANGULAR_"
            "PREDICTION_BAO_XMAX_OR_UDT_VALIDATION"
        ),
    }
    artifact = {
        "phi": grid,
        "theta": theta,
        "theta_prime": theta_prime,
        "theta_second": theta_second,
        "s_prime": s_prime,
        "s_second": s_second,
        "coefficients": np.asarray(selected["coefficients"]),
        "coefficient_covariance": np.asarray(selected_result["coefficient_covariance"]),
        "knot_vector": np.asarray(selected_result["knot_vector"]),
    }
    census = [
        serial_candidate(candidate)
        for item in basis_results
        for candidate in item["candidates"]
    ]
    return summary, artifact, census


def write_census(census: list[dict[str, object]]) -> None:
    fields = ("basis_count", "alpha_index", "log10_alpha", "alpha", "lambda", "raw_chi2", "edf", "gcv")
    with CENSUS_PATH.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(census)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    summary, artifact, census = evaluate()
    rendered = json.dumps(summary, indent=2, sort_keys=True)
    if not args.no_write:
        RESULT_PATH.write_text(rendered + "\n", encoding="utf-8")
        write_census(census)
        np.savez_compressed(REPRESENTATION_PATH, **artifact)
    print(rendered)


if __name__ == "__main__":
    main()
