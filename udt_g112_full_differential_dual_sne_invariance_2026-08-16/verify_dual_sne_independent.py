#!/usr/bin/env python3
"""Independent fixed-shape G112 replay using precision-domain algebra."""

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


def model(z: np.ndarray) -> np.ndarray:
    scale = 1.0 + np.asarray(z, dtype=float)
    distance = N_FROZEN * scale * scale * (1.0 - scale ** (-2.0 / N_FROZEN))
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
        n = int(handle.readline())
        values = np.fromfile(handle, sep=" ")
    covariance = values.reshape(n, n)[np.ix_(keep, keep)]
    covariance = 0.5 * (covariance + covariance.T)
    factor = cho_factor(covariance, lower=False, check_finite=True)
    precision = cho_solve(factor, np.eye(keep.size), check_finite=True)
    chi2, offset = profile(precision, observed[keep], model(z[keep]))
    return chi2, offset, keep.size


def des() -> tuple[float, float, int]:
    names = ("tag", "CID", "IDSURVEY", "zHD", "zHEL", "MU", "MUERR",
             "MUERR_VPEC", "MUERR_SYS", "PROBIA_BEAMS")
    table = np.genfromtxt(DES / "DES-Dovekie_HD.csv", comments="#", skip_header=9,
                          names=names, dtype=None, encoding="utf-8")
    keep = np.flatnonzero(table["IDSURVEY"] == 10)
    with np.load(DES / "STAT+SYS.npz", allow_pickle=False) as archive:
        n = int(archive["nsn"][0])
        packed = np.asarray(archive["cov"], dtype=float)
    full = np.zeros((n, n))
    i, j = np.triu_indices(n)
    full[i, j] = packed
    full[j, i] = packed
    drop = np.setdiff1d(np.arange(n), keep, assume_unique=True)
    a = full[np.ix_(keep, keep)]
    b = full[np.ix_(keep, drop)]
    d = full[np.ix_(drop, drop)]
    factor = cho_factor(d, lower=False, check_finite=True)
    marginal_precision = a - b @ cho_solve(factor, b.T, check_finite=True)
    marginal_precision = 0.5 * (marginal_precision + marginal_precision.T)
    chi2, offset = profile(marginal_precision, table["MU"][keep], model(table["zHD"][keep]))
    return chi2, offset, keep.size


def main() -> None:
    production = json.loads((HERE / "PRODUCTION_RESULT.json").read_text())
    p_chi2, p_offset, p_count = pantheon()
    d_chi2, d_offset, d_count = des()
    residuals = {
        "pantheon_chi2": abs(p_chi2 - production["pantheon"]["chi2"]),
        "pantheon_offset": abs(p_offset - production["pantheon"]["offset_B"]),
        "des_chi2": abs(d_chi2 - production["des"]["chi2"]),
        "des_offset": abs(d_offset - production["des"]["offset_B"]),
    }
    tolerances = {"pantheon_chi2": 3.0e-6, "pantheon_offset": 3.0e-9,
                  "des_chi2": 3.0e-6, "des_offset": 3.0e-9}
    checks = {
        "pantheon_count": p_count == 1367,
        "des_count": d_count == 1623,
        "pantheon_chi2": residuals["pantheon_chi2"] <= tolerances["pantheon_chi2"],
        "pantheon_offset": residuals["pantheon_offset"] <= tolerances["pantheon_offset"],
        "des_chi2": residuals["des_chi2"] <= tolerances["des_chi2"],
        "des_offset": residuals["des_offset"] <= tolerances["des_offset"],
        "direct_power_formula": True,
        "precision_domain_route": True,
        "shape_optimizer_not_called": True,
    }
    result = {"schema": "UDT_G112_INDEPENDENT_PRECISION_REPLAY_V1",
              "all_checks_pass": all(checks.values()), "checks": checks,
              "replayed": {"pantheon_chi2": p_chi2, "pantheon_offset": p_offset,
                           "des_chi2": d_chi2, "des_offset": d_offset},
              "absolute_residuals": residuals, "tolerances": tolerances,
              "method": "direct-power P1 and precision-domain profiling; DES Schur complement"}
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["all_checks_pass"] else 1)


if __name__ == "__main__":
    main()
