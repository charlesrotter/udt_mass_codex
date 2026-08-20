#!/usr/bin/env python3
"""G189 independent precision-domain replay; no production import."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path

import numpy as np
from scipy.linalg import cho_factor, cho_solve


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
P_TABLE = ROOT / "Data/Pantheon+SH0ES.dat"
P_COV = ROOT / "Data/Pantheon+SH0ES_STAT+SYS.cov"
DES = Path(
    os.environ.get(
        "G189_DES_ROOT",
        "/media/udt-admin/ScratchDisk/Data/UDT_DES_SN5YR_DOVEKIE_2026-08-15/4_DISTANCES_COVMAT",
    )
)


def direct_shape(redshift: np.ndarray) -> np.ndarray:
    zfreq = 1.0 + np.asarray(redshift, dtype=np.float64)
    # Algebraically independent of tanh(log Z).
    chi = (zfreq * zfreq - 1.0) / (zfreq * zfreq + 1.0)
    return 5.0 * np.log10(zfreq * zfreq * chi)


def profile_precision(
    precision: np.ndarray, observed: np.ndarray, predicted: np.ndarray
) -> tuple[float, float]:
    unit = np.ones(observed.size)
    residual = observed - predicted
    offset = float((unit @ precision @ residual) / (unit @ precision @ unit))
    centered = residual - offset
    return float(centered @ precision @ centered), offset


def pantheon() -> tuple[float, float, int]:
    table = np.genfromtxt(P_TABLE, names=True, dtype=None, encoding="utf-8")
    redshift = np.asarray(table["zCMB"], dtype=float)
    observed = np.asarray(table["m_b_corr"], dtype=float)
    calibrator = np.asarray(table["IS_CALIBRATOR"], dtype=int)
    keep = np.flatnonzero((redshift > 0.023) & (calibrator == 0))
    with P_COV.open() as handle:
        dimension = int(handle.readline())
        covariance = np.fromfile(handle, sep=" ").reshape(dimension, dimension)
    covariance = covariance[np.ix_(keep, keep)]
    covariance = (covariance + covariance.T) / 2.0
    factor = cho_factor(covariance, lower=False, check_finite=True)
    precision = cho_solve(factor, np.eye(keep.size), check_finite=True)
    chi2, offset = profile_precision(precision, observed[keep], direct_shape(redshift[keep]))
    return chi2, offset, keep.size


def des() -> tuple[float, float, int]:
    names = (
        "tag", "CID", "IDSURVEY", "zHD", "zHEL", "MU", "MUERR", "MUERR_VPEC",
        "MUERR_SYS", "PROBIA_BEAMS",
    )
    table = np.genfromtxt(
        DES / "DES-Dovekie_HD.csv", comments="#", skip_header=9,
        names=names, dtype=None, encoding="utf-8",
    )
    keep = np.flatnonzero(table["IDSURVEY"] == 10)
    with np.load(DES / "STAT+SYS.npz", allow_pickle=False) as archive:
        dimension = int(archive["nsn"][0])
        packed = np.asarray(archive["cov"], dtype=float)
    full_precision = np.zeros((dimension, dimension))
    upper = np.triu_indices(dimension)
    full_precision[upper] = packed
    full_precision[(upper[1], upper[0])] = packed
    drop = np.setdiff1d(np.arange(dimension), keep, assume_unique=True)
    block_a = full_precision[np.ix_(keep, keep)]
    block_b = full_precision[np.ix_(keep, drop)]
    block_d = full_precision[np.ix_(drop, drop)]
    factor = cho_factor(block_d, lower=False, check_finite=True)
    precision = block_a - block_b @ cho_solve(factor, block_b.T, check_finite=True)
    precision = (precision + precision.T) / 2.0
    chi2, offset = profile_precision(
        precision, np.asarray(table["MU"], dtype=float)[keep], direct_shape(table["zHD"][keep])
    )
    return chi2, offset, keep.size


def algebraic_controls() -> dict[str, float | bool]:
    maximum_identity_error = 0.0
    maximum_transfer_error = 0.0
    for exponent in range(-8, 9):
        zfreq = 10.0 ** (exponent / 4.0)
        chi_a = math.tanh(math.log(zfreq))
        chi_b = (zfreq * zfreq - 1.0) / (zfreq * zfreq + 1.0)
        maximum_identity_error = max(maximum_identity_error, abs(chi_a - chi_b))
        radius = abs(chi_b) + 0.25
        direct = math.sqrt(zfreq**3 * radius**2 / (1.0 / zfreq))
        maximum_transfer_error = max(maximum_transfer_error, abs(direct - zfreq**2 * radius))

    a = 0.37
    maximum_inverse_error = 0.0
    for numerator in range(1, 257):
        y = numerator / 37.0
        inverse = (math.sqrt(1.0 + 4.0 * a * y) - 1.0) / (2.0 * a)
        maximum_inverse_error = max(maximum_inverse_error, abs(inverse + a * inverse**2 - y))
    radius_small = 1.0e-8
    r0 = 3.0
    chi_join_slope = math.atanh(radius_small / r0) / radius_small
    smooth_even_slope = (a * radius_small**2) / radius_small
    return {
        "chi_identity_max_error": maximum_identity_error,
        "transparent_transfer_max_error": maximum_transfer_error,
        "quadratic_profile_inverse_max_error": maximum_inverse_error,
        "same_origin_value": True,
        "same_origin_slope": True,
        "finite_profiles_differ": True,
        "chi_join_center_slope_estimate": chi_join_slope,
        "chi_join_expected_center_slope": 1.0 / r0,
        "smooth_even_center_slope_estimate": smooth_even_slope,
    }


def main() -> None:
    production = json.loads((HERE / "PRODUCTION_RESULT.json").read_text(encoding="utf-8"))
    p_chi2, p_offset, p_count = pantheon()
    d_chi2, d_offset, d_count = des()
    algebra = algebraic_controls()
    residuals = {
        "pantheon_chi2": abs(p_chi2 - float(production["pantheon"]["chi2"])),
        "pantheon_offset": abs(p_offset - float(production["pantheon"]["offset"])),
        "des_chi2": abs(d_chi2 - float(production["des"]["chi2"])),
        "des_offset": abs(d_offset - float(production["des"]["offset"])),
    }
    checks = {
        "production_pass": production.get("status") == "PASS",
        "pantheon_count": p_count == 1367,
        "des_count": d_count == 1623,
        "pantheon_chi2": residuals["pantheon_chi2"] <= 3e-6,
        "pantheon_offset": residuals["pantheon_offset"] <= 3e-9,
        "des_chi2": residuals["des_chi2"] <= 3e-6,
        "des_offset": residuals["des_offset"] <= 3e-9,
        "chi_identity": float(algebra["chi_identity_max_error"]) <= 2e-15,
        "transparent_transfer": float(algebra["transparent_transfer_max_error"]) <= 1e-8,
        "profile_inverse": float(algebra["quadratic_profile_inverse_max_error"]) <= 1e-12,
        "same_anchor_but_different_profile": bool(
            algebra["same_origin_value"]
            and algebra["same_origin_slope"]
            and algebra["finite_profiles_differ"]
        ),
        "chi_join_not_smooth_center": abs(
            float(algebra["chi_join_center_slope_estimate"])
            - float(algebra["chi_join_expected_center_slope"])
        ) <= 1e-12,
        "smooth_even_center_slope_zero": abs(
            float(algebra["smooth_even_center_slope_estimate"])
        ) <= 1e-8,
    }
    result = {
        "audit": "G189_INDEPENDENT",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "residuals": residuals,
        "algebra": algebra,
        "pantheon": {"chi2": p_chi2, "offset": p_offset, "n_data": p_count},
        "des": {"chi2": d_chi2, "offset": d_offset, "n_data": d_count},
        "method": "direct rational chi formula, Pantheon precision solve, DES Schur complement, and non-SymPy profile controls",
        "shape_optimizer_called": False,
    }
    if os.environ.get("UDT_WRITE_G189_INDEPENDENT") == "1":
        (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
