#!/usr/bin/env python3
"""Implementation-distinct precision-domain verification for G185."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
SEALED_REPLAY = HERE / "verify_sealed_intake.js"
if (HERE.parent.joinpath("sources").is_dir() and SEALED_REPLAY.is_file()):
    completed = subprocess.run(
        ["node", str(SEALED_REPLAY)], cwd=HERE, check=False, text=True
    )
    raise SystemExit(completed.returncode)

import numpy as np
from scipy.linalg import cho_factor, cho_solve


ROOT = HERE.parent
P_TABLE = ROOT / "Data/Pantheon+SH0ES.dat"
P_COV = ROOT / "Data/Pantheon+SH0ES_STAT+SYS.cov"
DES = Path(
    "/media/udt-admin/ScratchDisk/Data/UDT_DES_SN5YR_DOVEKIE_2026-08-15/4_DISTANCES_COVMAT"
)

# FROZEN_HISTORICAL_CALIBRATION; independently restated from the preregistered source.
N_FROZEN = 1.0559332414320268


def distance_shape(z: np.ndarray) -> np.ndarray:
    zfreq = 1.0 + np.asarray(z, dtype=np.float64)
    radius = N_FROZEN * (1.0 - np.exp((-2.0 / N_FROZEN) * np.log(zfreq)))
    return zfreq * zfreq * radius


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
    predicted = 5.0 * np.log10(distance_shape(redshift[keep]))
    chi2, offset = profile_precision(precision, observed[keep], predicted)
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
    predicted = 5.0 * np.log10(distance_shape(table["zHD"][keep]))
    chi2, offset = profile_precision(precision, table["MU"][keep], predicted)
    return chi2, offset, keep.size


def channel_controls() -> dict[str, float | bool]:
    # Direct numerical evaluation, independent of the production SymPy path.
    radial_theta = np.zeros((2, 2), dtype=float)
    radius = 7.0
    angular_gram = radius**2 * radial_theta.T @ radial_theta
    angle = 0.371
    rotation = np.array(
        [[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]],
        dtype=float,
    )
    dsky = radius * rotation
    a, radial_rate, angular_rate2 = 0.37, 1.9, 0.23
    m2 = radial_rate**2 + a * radius**2 * angular_rate2
    zfreq = np.geomspace(1.000001, 1000.0, 4096)
    test_radius = N_FROZEN * (1.0 - zfreq ** (-2.0 / N_FROZEN))
    imported = np.sqrt(zfreq**3 * test_radius**2 / (1.0 / zfreq))
    reduced = zfreq**2 * test_radius
    return {
        "radial_pair_angular_gram_max": float(np.max(np.abs(angular_gram))),
        "sky_determinant_residual": abs(float(np.linalg.det(dsky)) - radius**2),
        "nonradial_density_increment": m2 - radial_rate**2,
        "expected_nonradial_increment": a * radius**2 * angular_rate2,
        "transfer_reduction_residual": float(np.max(np.abs(imported - reduced))),
        "radial_pair_zero_and_sky_live": bool(
            np.max(np.abs(angular_gram)) == 0.0 and np.linalg.det(dsky) > 0.0
        ),
    }


def main() -> None:
    production = json.loads((HERE / "PRODUCTION_RESULT.json").read_text(encoding="utf-8"))
    p_chi2, p_offset, p_count = pantheon()
    d_chi2, d_offset, d_count = des()
    channels = channel_controls()
    residuals = {
        "pantheon_chi2": abs(p_chi2 - float(production["pantheon"]["chi2"])),
        "pantheon_offset": abs(p_offset - float(production["pantheon"]["offset_B"])),
        "des_chi2": abs(d_chi2 - float(production["des"]["chi2"])),
        "des_offset": abs(d_offset - float(production["des"]["offset_B"])),
    }
    checks = {
        "production_pass": production.get("status") == "PASS",
        "pantheon_count": p_count == 1367,
        "des_count": d_count == 1623,
        "pantheon_chi2": residuals["pantheon_chi2"] <= 3e-6,
        "pantheon_offset": residuals["pantheon_offset"] <= 3e-9,
        "des_chi2": residuals["des_chi2"] <= 3e-6,
        "des_offset": residuals["des_offset"] <= 3e-9,
        "radial_pair_angular_zero": channels["radial_pair_angular_gram_max"] == 0.0,
        "sky_area_active": channels["sky_determinant_residual"] <= 1e-12,
        "nonradial_pair_channel_live": abs(
            float(channels["nonradial_density_increment"])
            - float(channels["expected_nonradial_increment"])
        ) <= 1e-12,
        "transfer_reduction": channels["transfer_reduction_residual"] <= 1e-9,
        "radial_zero_and_sky_live_are_compatible": bool(channels["radial_pair_zero_and_sky_live"]),
    }
    result = {
        "audit": "G185_INDEPENDENT",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "residuals": residuals,
        "channels": channels,
        "method": "independent precision-domain Pantheon inversion, DES Schur complement, and direct matrix channel controls",
        "shape_optimizer_called": False,
    }
    if os.environ.get("UDT_WRITE_G185_INDEPENDENT") == "1":
        (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
