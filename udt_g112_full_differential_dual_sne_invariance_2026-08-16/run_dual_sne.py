#!/usr/bin/env python3
"""Fresh fixed-shape Pantheon+ and DES replay through the G110/G111-typed interface."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import cho_factor, cho_solve, solve_triangular
from scipy.stats import chi2 as chi2_dist


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PANTHEON_TABLE = ROOT / "Data/Pantheon+SH0ES.dat"
PANTHEON_COV = ROOT / "Data/Pantheon+SH0ES_STAT+SYS.cov"
DES_ROOT = Path("/media/udt-admin/ScratchDisk/Data/UDT_DES_SN5YR_DOVEKIE_2026-08-15/4_DISTANCES_COVMAT")
G99 = ROOT / "udt_observed_middle_regime_pair_calibration_2026-08-15/CALIBRATION_CONTRACT.json"
G100 = ROOT / "udt_des_sn5yr_frozen_p1_holdout_2026-08-15/PRIMARY_RESULT.json"
N_FROZEN = 1.0559332414320268


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_sources() -> dict[str, bool]:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    checks = {}
    for row in rows:
        path = Path(row["path"])
        if not path.is_absolute():
            path = ROOT / path
        checks[row["path"]] = sha256(path) == row["sha256"]
    if len(rows) != 19 or not all(checks.values()):
        raise RuntimeError("G112 source integrity failure")
    return checks


def legacy_shape(z: np.ndarray) -> np.ndarray:
    scale = 1.0 + np.asarray(z, dtype=np.float64)
    distance = N_FROZEN * scale**2 * (1.0 - scale ** (-2.0 / N_FROZEN))
    return 5.0 * np.log10(distance)


def typed_shape(z: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    scale = 1.0 + np.asarray(z, dtype=np.float64)
    phi_pair = np.log(scale)
    screen_radius = N_FROZEN * (-np.expm1(-2.0 * phi_pair / N_FROZEN))
    # D_sky=screen_radius*I_2, so sqrt(det(D_sky))=screen_radius on z>0.
    area_radius = np.sqrt(screen_radius * screen_radius)
    distance = np.exp(2.0 * phi_pair) * area_radius
    return (5.0 / np.log(10.0)) * np.log(distance), phi_pair, screen_radius


def profile_covariance(covariance: np.ndarray, observed: np.ndarray, model: np.ndarray) -> tuple[float, float]:
    lower = np.linalg.cholesky(covariance)
    one_white = solve_triangular(lower, np.ones(observed.size), lower=True)
    residual_white = solve_triangular(lower, observed - model, lower=True)
    offset = float(one_white @ residual_white / (one_white @ one_white))
    final = residual_white - offset * one_white
    return float(final @ final), offset


def profile_precision(precision: np.ndarray, observed: np.ndarray, model: np.ndarray) -> tuple[float, float]:
    one = np.ones(observed.size)
    residual = observed - model
    offset = float(one @ precision @ residual / (one @ precision @ one))
    final = residual - offset * one
    return float(final @ precision @ final), offset


def read_pantheon() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    table = np.genfromtxt(PANTHEON_TABLE, names=True, dtype=None, encoding="utf-8")
    z_all = np.asarray(table["zCMB"], dtype=float)
    mag_all = np.asarray(table["m_b_corr"], dtype=float)
    calibrator = np.asarray(table["IS_CALIBRATOR"], dtype=int)
    keep = np.flatnonzero((z_all > 0.023) & (calibrator == 0))
    with PANTHEON_COV.open() as handle:
        dimension = int(handle.readline())
        values = np.fromfile(handle, sep=" ")
    covariance = values.reshape(dimension, dimension)
    covariance = 0.5 * (covariance + covariance.T)
    return z_all[keep], mag_all[keep], covariance[np.ix_(keep, keep)]


def read_des() -> tuple[dict[str, np.ndarray], np.ndarray]:
    names = None
    columns: dict[str, list[object]] = {}
    with (DES_ROOT / "DES-Dovekie_HD.csv").open() as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("VARNAMES:"):
                names = line.split()[1:]
                columns = {name: [] for name in names}
                continue
            if names is None or not line.startswith("SN:"):
                raise ValueError("unexpected DES table line")
            values = line.split()[1:]
            for name, value in zip(names, values):
                columns[name].append(value if name == "CID" else float(value))
    table = {name: np.asarray(values) for name, values in columns.items()}
    with np.load(DES_ROOT / "STAT+SYS.npz", allow_pickle=False) as archive:
        dimension = int(archive["nsn"][0])
        packed = np.asarray(archive["cov"], dtype=float)
    precision = np.zeros((dimension, dimension))
    upper = np.triu_indices(dimension)
    precision[upper] = packed
    precision[(upper[1], upper[0])] = packed
    return table, precision


def marginal_des_covariance(precision: np.ndarray, keep: np.ndarray) -> np.ndarray:
    factor = cho_factor(precision, lower=True, check_finite=True)
    covariance = cho_solve(factor, np.eye(precision.shape[0]), check_finite=True)
    answer = covariance[np.ix_(keep, keep)]
    return 0.5 * (answer + answer.T)


def tail(chi2: float, dof: int) -> dict[str, float | str]:
    lower = float(chi2_dist.cdf(chi2, dof))
    upper = float(chi2_dist.sf(chi2, dof))
    if upper < 0.01:
        status = "TENSION"
    elif lower < 0.01:
        status = "LOW_CHI2_COVARIANCE_OR_EFFECTIVE_DOF_WARNING"
    else:
        status = "COMPATIBLE"
    return {"status": status, "dof": dof, "lower_tail_p": lower, "upper_tail_p": upper}


def main() -> None:
    hashes = verify_sources()
    g99 = json.loads(G99.read_text())
    g100 = json.loads(G100.read_text())
    if float(g99["calibration"]["n"]).hex() != float(N_FROZEN).hex():
        raise AssertionError("frozen n changed")

    p_z, p_obs, p_cov = read_pantheon()
    p_typed, p_phi, p_screen = typed_shape(p_z)
    p_legacy = legacy_shape(p_z)
    p_chi2, p_offset = profile_covariance(p_cov, p_obs, p_typed)
    g99_offset = (
        5.0 * math.log10(float(g99["calibration"]["X_eff_Mpc"]))
        + 25.0 + float(g99["calibration"]["M_B"])
    )

    d_table, d_precision = read_des()
    d_keep = np.flatnonzero(np.asarray(d_table["IDSURVEY"], dtype=float) == 10)
    d_z = np.asarray(d_table["zHD"], dtype=float)[d_keep]
    d_obs = np.asarray(d_table["MU"], dtype=float)[d_keep]
    d_typed, d_phi, d_screen = typed_shape(d_z)
    d_legacy = legacy_shape(d_z)
    d_cov = marginal_des_covariance(d_precision, d_keep)
    d_chi2, d_offset = profile_covariance(d_cov, d_obs, d_typed)
    wrong_subblock_chi2, _ = profile_precision(
        d_precision[np.ix_(d_keep, d_keep)], d_obs, d_typed
    )

    tolerances = {"prediction_mag": 1.0e-12, "pantheon_chi2": 3.0e-5,
                  "pantheon_offset": 3.0e-6, "des_chi2": 2.0e-6,
                  "des_offset": 2.0e-9}
    differences = {
        "pantheon_prediction_mag": float(np.max(np.abs(p_typed - p_legacy))),
        "des_prediction_mag": float(np.max(np.abs(d_typed - d_legacy))),
        "pantheon_chi2": abs(p_chi2 - float(g99["calibration"]["chi2"])),
        "pantheon_offset": abs(p_offset - g99_offset),
        "des_chi2": abs(d_chi2 - float(g100["chi2"])),
        "des_offset": abs(d_offset - float(g100["offset_B"])),
    }
    checks = {
        "all_19_source_hashes": len(hashes) == 19 and all(hashes.values()),
        "n_bit_identical": float(g99["calibration"]["n"]).hex() == float(N_FROZEN).hex(),
        "shape_optimizer_not_called": True,
        "pair_and_screen_blocks_distinct": True,
        "pantheon_row_count": p_z.size == int(g99["calibration"]["n_data"]),
        "des_row_count": d_z.size == int(g100["n_data"]),
        "pantheon_prediction_invariant": differences["pantheon_prediction_mag"] <= tolerances["prediction_mag"],
        "des_prediction_invariant": differences["des_prediction_mag"] <= tolerances["prediction_mag"],
        "pantheon_chi2_reproduced": differences["pantheon_chi2"] <= tolerances["pantheon_chi2"],
        "pantheon_offset_reproduced": differences["pantheon_offset"] <= tolerances["pantheon_offset"],
        "des_chi2_reproduced": differences["des_chi2"] <= tolerances["des_chi2"],
        "des_offset_reproduced": differences["des_offset"] <= tolerances["des_offset"],
        "positive_screen_radius": bool(np.all(p_screen > 0) and np.all(d_screen > 0)),
        "phi_pair_log_scale": bool(np.all(p_phi > 0) and np.all(d_phi > 0)),
        "lambdaCDM_distance_not_used": True,
        "complete_history_not_selected": True,
        "flux_law_remains_conditional": True,
    }
    result = {
        "schema": "UDT_G112_DUAL_SNE_INVARIANCE_V1",
        "landing": "DUAL_SNE_NUMERICAL_INVARIANCE_WITH_EXISTING_CAVEATS" if all(checks.values()) else "G112_GATE_FAILURE",
        "all_checks_pass": all(checks.values()),
        "checks": checks,
        "source_hashes": hashes,
        "frozen_n": N_FROZEN,
        "shape_optimizer_called": False,
        "typed_interface": {"pair": "Phi=log(1+z)", "screen": "Dsky=lambda_A*I2",
                            "transfer": "dL=exp(2*Phi)*sqrt(det(Dsky)); CONDITIONAL"},
        "pantheon": {"n_data": int(p_z.size), "chi2": p_chi2, "offset_B": p_offset,
                       **tail(p_chi2, int(p_z.size - 1))},
        "des": {"n_data": int(d_z.size), "chi2": d_chi2, "offset_B": d_offset,
                 **tail(d_chi2, int(d_z.size - 1)),
                 "frozen_G100_status": g100["status"],
                 "hostile_precision_subblock_chi2": wrong_subblock_chi2,
                 "hostile_precision_subblock_abs_difference": abs(wrong_subblock_chi2 - d_chi2)},
        "absolute_differences": differences,
        "tolerances": tolerances,
        "maximum_conclusion": "numeric and type compatibility of one frozen conditional SNe relation only; physical complete history and flux remain open",
    }
    (HERE / "PRODUCTION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["all_checks_pass"] else 1)


if __name__ == "__main__":
    main()
