#!/usr/bin/env python3
"""Independent precision-domain G243 radial spline census."""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.interpolate import BSpline
from scipy.linalg import cho_factor, cho_solve, eigh


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
DES_ROOT = Path(os.environ["G243_DES_ROOT"]).resolve()
P_TABLE = ROOT / "Data/Pantheon+SH0ES.dat"
P_COV = ROOT / "Data/Pantheon+SH0ES_STAT+SYS.cov"
DES_TABLE = DES_ROOT / "DES-Dovekie_HD.csv"
DES_PRECISION = DES_ROOT / "STAT+SYS.npz"
OUTPUT_PATH = PACKAGE / "INDEPENDENT_VERIFICATION.json"
CENSUS_PATH = PACKAGE / "INDEPENDENT_CENSUS.tsv"

BASIS_COUNTS = (16, 24, 32, 48, 64)
LOG10_ALPHA = np.arange(-12.0, 12.0000001, 0.25, dtype=np.float64)
PHI_MIN = 0.07077528204904217
PHI_MAX = 0.7627571949083936


def pantheon_precision() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    table = np.genfromtxt(P_TABLE, names=True, dtype=None, encoding="utf-8")
    z = np.asarray(table["zCMB"], dtype=np.float64)
    magnitude = np.asarray(table["m_b_corr"], dtype=np.float64)
    keep = np.flatnonzero(
        (z > 0.023)
        & (np.asarray(table["IS_CALIBRATOR"], dtype=np.int64) == 0)
        & (np.asarray(table["IDSURVEY"], dtype=np.int64) != 10)
        & (np.log1p(z) >= PHI_MIN)
        & (np.log1p(z) <= PHI_MAX)
    )
    with P_COV.open() as handle:
        dimension = int(handle.readline())
        values = np.fromfile(handle, sep=" ")
    covariance = values.reshape(dimension, dimension)
    covariance = 0.5 * (covariance + covariance.T)
    retained = covariance[np.ix_(keep, keep)]
    factor = cho_factor(retained, lower=False, check_finite=True)
    precision = cho_solve(factor, np.eye(keep.size), check_finite=True)
    return (
        np.log1p(z[keep]),
        magnitude[keep] - 10.0 * np.log10(1.0 + z[keep]),
        0.5 * (precision + precision.T),
        retained,
    )


def des_marginal_precision() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    names: list[str] | None = None
    rows: list[list[str]] = []
    with DES_TABLE.open() as handle:
        for raw in handle:
            fields = raw.strip().split()
            if not fields or fields[0] == "#":
                continue
            if fields[0] == "VARNAMES:":
                names = fields[1:]
                continue
            if fields[0] != "SN:" or names is None:
                raise RuntimeError("bad DES release row")
            rows.append(fields[1:])
    if names is None:
        raise RuntimeError("missing DES VARNAMES")
    columns = {name: i for i, name in enumerate(names)}
    survey = np.asarray([int(float(row[columns["IDSURVEY"]])) for row in rows], dtype=np.int64)
    z = np.asarray([float(row[columns["zHD"]]) for row in rows], dtype=np.float64)
    magnitude = np.asarray([float(row[columns["MU"]]) for row in rows], dtype=np.float64)
    keep = np.flatnonzero(survey == 10)
    omit = np.flatnonzero(survey != 10)
    with np.load(DES_PRECISION, allow_pickle=False) as archive:
        dimension = int(archive["nsn"][0])
        packed = np.asarray(archive["cov"], dtype=np.float64)
    precision = np.zeros((dimension, dimension), dtype=np.float64)
    upper = np.triu_indices(dimension)
    precision[upper] = packed
    precision[(upper[1], upper[0])] = packed
    precision = 0.5 * (precision + precision.T)
    pkk = precision[np.ix_(keep, keep)]
    pko = precision[np.ix_(keep, omit)]
    poo = precision[np.ix_(omit, omit)]
    factor = cho_factor(poo, lower=False, check_finite=True)
    marginal = pkk - pko @ cho_solve(factor, pko.T, check_finite=True)
    marginal = 0.5 * (marginal + marginal.T)
    # A separately assembled covariance-domain evaluator certifies raw chi-square without changing
    # the direct Schur-precision normal equations that determine the independent coefficients.
    full_factor = cho_factor(precision, lower=False, check_finite=True)
    selectors = np.zeros((dimension, keep.size), dtype=np.float64)
    selectors[keep, np.arange(keep.size)] = 1.0
    selected_columns = cho_solve(full_factor, selectors, check_finite=True)
    retained_covariance = selected_columns[keep, :]
    retained_covariance = 0.5 * (retained_covariance + retained_covariance.T)
    return (
        np.log1p(z[keep]),
        magnitude[keep] - 10.0 * np.log10(1.0 + z[keep]),
        marginal,
        retained_covariance,
    )


def spline_basis(basis_count: int) -> tuple[BSpline, np.ndarray]:
    degree = 3
    interior = np.linspace(PHI_MIN, PHI_MAX, basis_count - 2, dtype=np.float64)[1:-1]
    knot_vector = np.concatenate(
        [np.repeat(PHI_MIN, degree + 1), interior, np.repeat(PHI_MAX, degree + 1)]
    )
    return BSpline(knot_vector, np.eye(basis_count), degree, extrapolate=False), knot_vector


def shape_design(spline: BSpline, phi: np.ndarray, derivative: int = 0) -> np.ndarray:
    evaluator = spline.derivative(derivative) if derivative else spline
    values = np.asarray(evaluator(phi), dtype=np.float64)
    if derivative == 0:
        values = values - np.asarray(evaluator(PHI_MIN), dtype=np.float64)
    return values[:, :-1]


def penalty_matrix(spline: BSpline, knots: np.ndarray) -> np.ndarray:
    # Five-point quadrature is independent of production's eight-point route and exact here.
    nodes, weights = leggauss(5)
    size = spline.c.shape[0] - 1
    penalty = np.zeros((size, size), dtype=np.float64)
    derivative = spline.derivative(2)
    unique = np.unique(knots)
    for left, right in zip(unique[:-1], unique[1:]):
        points = (right - left) * nodes / 2.0 + (right + left) / 2.0
        values = np.asarray(derivative(points), dtype=np.float64)[:, :-1]
        penalty += values.T @ (((right - left) * weights / 2.0)[:, None] * values)
    return 0.5 * (penalty + penalty.T)


def release_design(phi: np.ndarray, spline: BSpline, first: bool) -> np.ndarray:
    if first:
        return np.column_stack([np.ones(phi.size), np.zeros(phi.size), shape_design(spline, phi)])
    return np.column_stack([np.zeros(phi.size), np.ones(phi.size), shape_design(spline, phi)])


def analytic_nullspace(spline: BSpline) -> np.ndarray:
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


def evaluate() -> tuple[dict[str, object], list[dict[str, float | int]], np.ndarray]:
    p_phi, p_y, p_precision, p_covariance = pantheon_precision()
    d_phi, d_y, d_precision, d_covariance = des_marginal_precision()
    if p_phi.size != 768 or d_phi.size != 1623:
        raise RuntimeError("release count mismatch")
    census: list[dict[str, float | int]] = []
    basis_best: list[dict[str, object]] = []
    basis_payload: dict[int, tuple[BSpline, np.ndarray, np.ndarray]] = {}
    p_covariance_factor = cho_factor(p_covariance, lower=False, check_finite=True)
    d_covariance_factor = cho_factor(d_covariance, lower=False, check_finite=True)

    for basis_count in BASIS_COUNTS:
        spline, knots = spline_basis(basis_count)
        p_design = release_design(p_phi, spline, True)
        d_design = release_design(d_phi, spline, False)
        long_p_design = p_design.astype(np.longdouble)
        long_d_design = d_design.astype(np.longdouble)
        long_p_precision = p_precision.astype(np.longdouble)
        long_d_precision = d_precision.astype(np.longdouble)
        normal = np.asarray(
            long_p_design.T @ long_p_precision @ long_p_design
            + long_d_design.T @ long_d_precision @ long_d_design,
            dtype=np.float64,
        )
        rhs = np.asarray(
            long_p_design.T @ long_p_precision @ p_y.astype(np.longdouble)
            + long_d_design.T @ long_d_precision @ d_y.astype(np.longdouble),
            dtype=np.float64,
        )
        penalty_shape = penalty_matrix(spline, knots)
        penalty = np.zeros_like(normal)
        penalty[2:, 2:] = penalty_shape
        scale = float(np.trace(normal[2:, 2:]) / np.trace(penalty_shape))
        nullspace = analytic_nullspace(spline)
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
        zz_factor = cho_factor(a_zz, lower=False, check_finite=True)
        zz_inverse_zr = cho_solve(zz_factor, a_zr, check_finite=True)
        zz_inverse_b = cho_solve(zz_factor, b_z, check_finite=True)
        reduced_normal = a_rr - a_zr.T @ zz_inverse_zr
        reduced_normal = 0.5 * (reduced_normal + reduced_normal.T)
        reduced_rhs = b_r - a_zr.T @ zz_inverse_b
        reduced_penalty = q_penalized.T @ penalty @ q_penalized
        reduced_penalty = 0.5 * (reduced_penalty + reduced_penalty.T)
        eigenvalues, eigenvectors = eigh(reduced_penalty, reduced_normal, check_finite=True)
        tolerance = 1000.0 * np.finfo(np.float64).eps * max(
            1.0, float(np.max(np.abs(eigenvalues)))
        )
        if float(np.min(eigenvalues)) < -tolerance:
            raise RuntimeError("roughness penalty lost positive semidefiniteness")
        eigenvalues = np.maximum(eigenvalues, 0.0)
        if not float(np.min(eigenvalues)) > 0.0:
            raise RuntimeError("reduced roughness penalty is not positive definite")
        projected_rhs = eigenvectors.T @ reduced_rhs
        candidates: list[dict[str, object]] = []
        for alpha_index, log_alpha in enumerate(LOG10_ALPHA):
            alpha = float(10.0**log_alpha)
            lam = alpha * scale
            inverse_weights = 1.0 / (1.0 + lam * eigenvalues)
            penalized = eigenvectors @ (inverse_weights * projected_rhs)
            null = cho_solve(zz_factor, b_z - a_zr @ penalized, check_finite=True)
            coefficient = q_null @ null + q_penalized @ penalized
            p_residual = p_y - p_design @ coefficient
            d_residual = d_y - d_design @ coefficient
            raw_chi2 = float(
                p_residual @ cho_solve(p_covariance_factor, p_residual, check_finite=True)
                + d_residual @ cho_solve(d_covariance_factor, d_residual, check_finite=True)
            )
            edf = float(3.0 + np.sum(inverse_weights))
            gcv = float((p_phi.size + d_phi.size) * raw_chi2 / (p_phi.size + d_phi.size - edf) ** 2)
            row = {
                "basis_count": basis_count,
                "alpha_index": alpha_index,
                "log10_alpha": float(log_alpha),
                "alpha": alpha,
                "lambda": float(lam),
                "raw_chi2": raw_chi2,
                "edf": edf,
                "gcv": gcv,
            }
            census.append(row)
            candidates.append({**row, "coefficient": coefficient})
        best = min(candidates, key=lambda item: (float(item["gcv"]), int(item["alpha_index"])))
        basis_best.append({key: value for key, value in best.items() if key != "coefficient"})
        basis_payload[basis_count] = (spline, knots, np.asarray(best["coefficient"]))

    selected = min(basis_best, key=lambda item: (float(item["gcv"]), int(item["basis_count"])))
    basis_count = int(selected["basis_count"])
    spline, knots, coefficient = basis_payload[basis_count]
    grid = np.linspace(PHI_MIN, PHI_MAX, 4097)
    theta = shape_design(spline, grid) @ coefficient[2:]
    theta_prime = shape_design(spline, grid, derivative=1) @ coefficient[2:]
    s_prime = (math.log(10.0) / 5.0) * theta_prime
    boundary = int(selected["alpha_index"]) in (0, LOG10_ALPHA.size - 1)
    globally_invertible = bool(np.min(s_prime) > 0.0)
    if boundary:
        classification = "REGULARIZATION_MINIMUM_ON_REGISTERED_BOUNDARY__NO_FREEZE"
    elif globally_invertible:
        classification = "SNE_ONLY_SMOOTH_RADIAL_REPRESENTATION_FROZEN__GLOBALLY_INVERTIBLE"
    else:
        classification = "SNE_ONLY_SMOOTH_RADIAL_REPRESENTATION_FROZEN__TURNING_INTERVALS_RETAINED"
    summary = {
        "status": "PASS",
        "method": (
            "DIRECT_PRECISION_NORMALS__PANTHEON_SOLVE__DES_SCHUR__EXACT_NULLSPACE_SCHUR__"
            "GENERALIZED_EIGEN_POSITIVE_BLOCK__COVARIANCE_DOMAIN_RAW_CHI2"
        ),
        "classification": classification,
        "selected": {
            **selected,
            "coefficients": coefficient.tolist(),
            "knot_vector": knots.tolist(),
            "minimum_s_prime": float(np.min(s_prime)),
            "maximum_s_prime": float(np.max(s_prime)),
            "globally_invertible": globally_invertible,
            "alpha_boundary": boundary,
        },
        "per_basis_best": basis_best,
        "counts": {"pantheon": int(p_phi.size), "des": int(d_phi.size)},
        "boss_outcomes": "CLOSED_AND_UNREAD",
        "angular_outcomes": "CLOSED_AND_UNUSED",
    }
    return summary, census, theta


def write_census(census: list[dict[str, float | int]]) -> None:
    fields = ("basis_count", "alpha_index", "log10_alpha", "alpha", "lambda", "raw_chi2", "edf", "gcv")
    with CENSUS_PATH.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(census)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    summary, census, _theta = evaluate()
    rendered = json.dumps(summary, indent=2, sort_keys=True)
    if not args.no_write:
        OUTPUT_PATH.write_text(rendered + "\n", encoding="utf-8")
        write_census(census)
    print(rendered)


if __name__ == "__main__":
    main()
