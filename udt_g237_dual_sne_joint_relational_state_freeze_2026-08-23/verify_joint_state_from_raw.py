#!/usr/bin/env python3
"""Independent direct raw-release GLS replay for G237; never reads G237 output."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
from pathlib import Path

import numpy as np
from scipy.linalg import cho_factor, cho_solve


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
DES_ROOT = Path(os.environ["G237_DES_ROOT"]).resolve()
P_TABLE = ROOT / "Data/Pantheon+SH0ES.dat"
P_COV = ROOT / "Data/Pantheon+SH0ES_STAT+SYS.cov"
DES_TABLE = DES_ROOT / "DES-Dovekie_HD.csv"
DES_PRECISION = DES_ROOT / "STAT+SYS.npz"
G236_MANIFEST = ROOT / "udt_g236_dual_sne_relational_state_reconstruction_2026-08-23/SOURCE_MANIFEST.tsv"
OUT = PACKAGE / "INDEPENDENT_RAW_GLS.json"
K_VALUES = (8, 12, 16, 24)
PHI_MIN = 0.07077528204904217
PHI_MAX = 0.7627571949083936


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve(logical: str) -> Path:
    external = {
        "external_data/README.md": DES_ROOT / "README.md",
        "external_data/DES-Dovekie_HD.csv": DES_TABLE,
        "external_data/STAT+SYS.npz": DES_PRECISION,
    }
    return external.get(logical, ROOT / logical)


def source_checks() -> dict[str, str | bool]:
    checks: dict[str, str | bool] = {}
    with G236_MANIFEST.open(newline="") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            logical = row["path"]
            if logical == "CURRENT_SCIENTIFIC_PREMISES.tsv":
                checks[logical] = "FROZEN_AUTHORITY_HASHED_BY_G236_NOT_A_G237_NUMERIC_INPUT"
                continue
            path = resolve(logical)
            checks[logical] = path.is_file() and sha256(path) == row["sha256"]
    if any(value is False for value in checks.values()):
        raise AssertionError(f"underlying source hash failure: {checks}")
    return checks


def read_pantheon():
    table = np.genfromtxt(P_TABLE, names=True, dtype=None, encoding="utf-8")
    z = np.asarray(table["zCMB"], dtype=np.float64)
    magnitude = np.asarray(table["m_b_corr"], dtype=np.float64)
    calibrator = np.asarray(table["IS_CALIBRATOR"], dtype=np.int64)
    survey = np.asarray(table["IDSURVEY"], dtype=np.int64)
    with P_COV.open() as stream:
        dimension = int(stream.readline())
        values = np.fromfile(stream, sep=" ")
    covariance = values.reshape(dimension, dimension)
    keep = np.flatnonzero(
        (z > 0.023)
        & (calibrator == 0)
        & (survey != 10)
        & (np.log1p(z) >= PHI_MIN)
        & (np.log1p(z) <= PHI_MAX)
    )
    covariance = covariance[np.ix_(keep, keep)]
    factor = cho_factor(0.5 * (covariance + covariance.T), lower=True, check_finite=True)
    precision = cho_solve(factor, np.eye(keep.size), check_finite=True)
    return np.log1p(z[keep]), magnitude[keep] - 10.0 * np.log10(1.0 + z[keep]), precision


def read_des():
    names = None
    rows = []
    with DES_TABLE.open() as stream:
        for raw in stream:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("VARNAMES:"):
                names = line.split()[1:]
                continue
            if names is None or not line.startswith("SN:"):
                raise ValueError("unexpected DES table format")
            rows.append(line.split()[1:])
    index = {name: i for i, name in enumerate(names)}
    survey = np.asarray([int(float(row[index["IDSURVEY"]])) for row in rows])
    z = np.asarray([float(row[index["zHD"]]) for row in rows], dtype=np.float64)
    magnitude = np.asarray([float(row[index["MU"]]) for row in rows], dtype=np.float64)
    keep = np.flatnonzero(survey == 10)
    omit = np.flatnonzero(survey != 10)
    with np.load(DES_PRECISION, allow_pickle=False) as archive:
        dimension = int(archive["nsn"][0])
        packed = np.asarray(archive["cov"], dtype=np.float64)
    precision = np.zeros((dimension, dimension), dtype=np.float64)
    upper = np.triu_indices(dimension)
    precision[upper] = packed
    precision[(upper[1], upper[0])] = packed
    p_kk = precision[np.ix_(keep, keep)]
    p_ko = precision[np.ix_(keep, omit)]
    p_oo = precision[np.ix_(omit, omit)]
    omit_factor = cho_factor(0.5 * (p_oo + p_oo.T), lower=True, check_finite=True)
    marginal_precision = p_kk - p_ko @ cho_solve(omit_factor, p_ko.T, check_finite=True)
    marginal_precision = 0.5 * (marginal_precision + marginal_precision.T)
    return np.log1p(z[keep]), magnitude[keep] - 10.0 * np.log10(1.0 + z[keep]), marginal_precision


def basis(phi: np.ndarray, knots: np.ndarray) -> np.ndarray:
    answer = np.zeros((phi.size, knots.size), dtype=np.float64)
    segment = np.clip(np.searchsorted(knots, phi, side="right") - 1, 0, knots.size - 2)
    fraction = (phi - knots[segment]) / (knots[segment + 1] - knots[segment])
    answer[np.arange(phi.size), segment] = 1.0 - fraction
    answer[np.arange(phi.size), segment + 1] = fraction
    return answer


def fit_joint(phi_p, y_p, precision_p, phi_d, y_d, precision_d, k: int) -> dict:
    knots = np.linspace(PHI_MIN, PHI_MAX, k)
    b_p = basis(phi_p, knots)[:, 1:]
    b_d = basis(phi_d, knots)[:, 1:]
    x_p = np.column_stack([np.ones(phi_p.size), np.zeros(phi_p.size), b_p])
    x_d = np.column_stack([np.zeros(phi_d.size), np.ones(phi_d.size), b_d])
    normal = x_p.T @ precision_p @ x_p + x_d.T @ precision_d @ x_d
    rhs = x_p.T @ precision_p @ y_p + x_d.T @ precision_d @ y_d
    factor = cho_factor(0.5 * (normal + normal.T), lower=True, check_finite=True)
    coefficients = cho_solve(factor, rhs, check_finite=True)
    coefficient_covariance = cho_solve(factor, np.eye(normal.shape[0]), check_finite=True)
    residual_p = y_p - x_p @ coefficients
    residual_d = y_d - x_d @ coefficients
    chi2 = float(residual_p @ precision_p @ residual_p + residual_d @ precision_d @ residual_d)
    return {
        "knots": knots.tolist(),
        "offsets": coefficients[:2].tolist(),
        "theta": coefficients[2:].tolist(),
        "theta_covariance": coefficient_covariance[2:, 2:].tolist(),
        "joint_raw_chi2": chi2,
        "joint_raw_dof": int(phi_p.size + phi_d.size - (k + 1)),
    }


def main() -> None:
    sources = source_checks()
    phi_p, y_p, precision_p = read_pantheon()
    phi_d, y_d, precision_d = read_des()
    if phi_p.size != 768 or phi_d.size != 1623:
        raise AssertionError((phi_p.size, phi_d.size))
    result = {
        "audit": "G237_INDEPENDENT_DIRECT_RAW_GLS",
        "status": "PASS",
        "method": "DIRECT_PRECISION_NORMAL_EQUATIONS_WITH_DES_OMITTED_BLOCK_SCHUR_COMPLEMENT",
        "cross_release_covariance": (
            "CHOSE_ZERO_AFTER_EXACT_CID_DEOVERLAP__UNKNOWN_SHARED_SYSTEMATICS_OPEN"
        ),
        "samples": {"pantheon": int(phi_p.size), "des": int(phi_d.size)},
        "source_hashes": sources,
        "resolutions": {
            str(k): fit_joint(phi_p, y_p, precision_p, phi_d, y_d, precision_d, k)
            for k in K_VALUES
        },
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
