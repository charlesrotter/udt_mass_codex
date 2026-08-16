#!/usr/bin/env python3
"""Independent G120 precision-domain replay from the radius and transfer definitions."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.linalg import cho_factor, cho_solve


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
P_TABLE = ROOT / "Data/Pantheon+SH0ES.dat"
P_COV = ROOT / "Data/Pantheon+SH0ES_STAT+SYS.cov"
DES = Path("/media/udt-admin/ScratchDisk/Data/UDT_DES_SN5YR_DOVEKIE_2026-08-15/4_DISTANCES_COVMAT")
N_FROZEN = 1.0559332414320268


def model_from_radius_and_transfer(z: np.ndarray) -> np.ndarray:
    scale = 1.0 + np.asarray(z, dtype=float)
    radius = N_FROZEN * (1.0 - scale ** (-2.0 / N_FROZEN))
    transfer_product = scale ** -1.0
    distance = np.sqrt(scale**3 * radius**2 / transfer_product)
    return 5.0 * np.log10(distance)


def profile(precision: np.ndarray, observed: np.ndarray, predicted: np.ndarray) -> tuple[float, float]:
    one = np.ones(observed.size)
    residual = observed - predicted
    offset = float(one @ precision @ residual / (one @ precision @ one))
    final = residual - offset
    return float(final @ precision @ final), offset


def pantheon() -> tuple[float, float, int]:
    table = np.genfromtxt(P_TABLE, names=True, dtype=None, encoding="utf-8")
    z = np.asarray(table["zCMB"], dtype=float)
    observed = np.asarray(table["m_b_corr"], dtype=float)
    keep = np.flatnonzero((z > 0.023) & (np.asarray(table["IS_CALIBRATOR"], dtype=int) == 0))
    with P_COV.open() as handle:
        dimension = int(handle.readline())
        values = np.fromfile(handle, sep=" ")
    covariance = values.reshape(dimension, dimension)[np.ix_(keep, keep)]
    covariance = 0.5 * (covariance + covariance.T)
    factor = cho_factor(covariance, lower=False, check_finite=True)
    precision = cho_solve(factor, np.eye(keep.size), check_finite=True)
    chi2, offset = profile(precision, observed[keep], model_from_radius_and_transfer(z[keep]))
    return chi2, offset, keep.size


def des() -> tuple[float, float, int]:
    names = ("tag", "CID", "IDSURVEY", "zHD", "zHEL", "MU", "MUERR", "MUERR_VPEC", "MUERR_SYS", "PROBIA_BEAMS")
    table = np.genfromtxt(DES / "DES-Dovekie_HD.csv", comments="#", skip_header=9,
                          names=names, dtype=None, encoding="utf-8")
    keep = np.flatnonzero(table["IDSURVEY"] == 10)
    with np.load(DES / "STAT+SYS.npz", allow_pickle=False) as archive:
        dimension = int(archive["nsn"][0])
        packed = np.asarray(archive["cov"], dtype=float)
    full_precision = np.zeros((dimension, dimension))
    upper = np.triu_indices(dimension)
    full_precision[upper] = packed
    full_precision[(upper[1], upper[0])] = packed
    drop = np.setdiff1d(np.arange(dimension), keep, assume_unique=True)
    a = full_precision[np.ix_(keep, keep)]
    b = full_precision[np.ix_(keep, drop)]
    d = full_precision[np.ix_(drop, drop)]
    factor = cho_factor(d, lower=False, check_finite=True)
    marginal_precision = a - b @ cho_solve(factor, b.T, check_finite=True)
    marginal_precision = 0.5 * (marginal_precision + marginal_precision.T)
    chi2, offset = profile(marginal_precision, table["MU"][keep],
                           model_from_radius_and_transfer(table["zHD"][keep]))
    return chi2, offset, keep.size


def main() -> None:
    production = json.loads((HERE / "PRODUCTION_RESULT.json").read_text())
    p_chi2, p_offset, p_count = pantheon()
    d_chi2, d_offset, d_count = des()
    probe_z = np.array([0.01, 0.5, 2.0], dtype=float)
    probe_scale = 1.0 + probe_z
    probe_radius = N_FROZEN * (1.0 - probe_scale ** (-2.0 / N_FROZEN))
    probe_transfer = 1.0 / probe_scale
    transfer_residual = float(np.max(np.abs(
        np.sqrt(probe_scale**3 * probe_radius**2 / probe_transfer)
        - probe_scale**2 * probe_radius
    )))
    residuals = {
        "pantheon_chi2": abs(p_chi2 - production["pantheon"]["chi2"]),
        "pantheon_offset": abs(p_offset - production["pantheon"]["offset_B"]),
        "des_chi2": abs(d_chi2 - production["des"]["chi2"]),
        "des_offset": abs(d_offset - production["des"]["offset_B"]),
        "transfer_reduction": transfer_residual,
    }
    tolerances = {"pantheon_chi2": 3e-6, "pantheon_offset": 3e-9,
                  "des_chi2": 3e-6, "des_offset": 3e-9}
    checks = {
        "pantheon_count": p_count == 1367,
        "des_count": d_count == 1623,
        "pantheon_chi2": residuals["pantheon_chi2"] <= tolerances["pantheon_chi2"],
        "pantheon_offset": residuals["pantheon_offset"] <= tolerances["pantheon_offset"],
        "des_chi2": residuals["des_chi2"] <= tolerances["des_chi2"],
        "des_offset": residuals["des_offset"] <= tolerances["des_offset"],
        "transfer_reduces_to_Z2R": residuals["transfer_reduction"] <= 1e-12,
    }
    result = {
        "schema": "UDT_G120_INDEPENDENT_EXACT_SCREEN_TRANSFER_REPLAY_V1",
        "all_checks_pass": all(checks.values()),
        "checks": checks,
        "replayed": {"pantheon_chi2": p_chi2, "pantheon_offset": p_offset,
                     "des_chi2": d_chi2, "des_offset": d_offset},
        "absolute_residuals": residuals,
        "tolerances": tolerances,
        "method": "direct radius plus general Z3 transfer factorization; precision-domain Pantheon; DES precision Schur complement",
        "method_metadata": {
            "precision_domain_route": True,
            "des_schur_complement": True,
            "curve_rebuilt_from_general_Z3_factorization": True,
            "imported_transfer_is_one_over_Z": True,
            "shape_optimizer_called": False,
        },
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["all_checks_pass"] else 1)


if __name__ == "__main__":
    main()
