#!/usr/bin/env python3
"""Independent G100 replay: numpy table parser + precision Schur complement."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.linalg import cho_factor, cho_solve
from scipy.optimize import minimize_scalar

HERE = Path(__file__).resolve().parent
DEFAULT_DIST = (Path("/media/udt-admin/ScratchDisk/Data/") /
                "UDT_DES_SN5YR_DOVEKIE_2026-08-15/4_DISTANCES_COVMAT")
N_G99 = 1.0559332414320268
S_BOUNDS = (1.0e-4, 40.0)


def load_table(dist: Path) -> np.ndarray:
    names = ("tag", "CID", "IDSURVEY", "zHD", "zHEL", "MU", "MUERR",
             "MUERR_VPEC", "MUERR_SYS", "PROBIA_BEAMS")
    return np.genfromtxt(dist / "DES-Dovekie_HD.csv", comments="#", skip_header=9,
                         names=names, dtype=None, encoding="utf-8")


def load_precision(dist: Path, name: str) -> np.ndarray:
    with np.load(dist / name, allow_pickle=False) as data:
        n = int(np.asarray(data["nsn"])[0])
        values = np.asarray(data["cov"], dtype=np.float64)
    i, j = np.triu_indices(n)
    if values.size != i.size:
        raise AssertionError("packed precision count")
    out = np.zeros((n, n), dtype=np.float64)
    out[i, j] = values
    out[j, i] = values
    return out


def marginal_precision(full: np.ndarray, keep: np.ndarray) -> np.ndarray:
    drop = np.setdiff1d(np.arange(full.shape[0]), keep, assume_unique=True)
    a = full[np.ix_(keep, keep)]
    b = full[np.ix_(keep, drop)]
    d = full[np.ix_(drop, drop)]
    factor = cho_factor(d, lower=False, check_finite=True)
    answer = a - b @ cho_solve(factor, b.T, check_finite=True)
    return 0.5 * (answer + answer.T)


def direct_model(z: np.ndarray, n: float) -> np.ndarray:
    zp1 = 1.0 + np.asarray(z, dtype=np.float64)
    distance = n * zp1 * zp1 * (1.0 - zp1 ** (-2.0 / n))
    return 5.0 * np.log10(distance)


def profile(precision: np.ndarray, observed: np.ndarray, model: np.ndarray) -> tuple[float, float]:
    one = np.ones(observed.size)
    r = observed - model
    denom = float(one @ precision @ one)
    offset = float(one @ precision @ r) / denom
    residual = r - offset * one
    return float(residual @ precision @ residual), offset


def close(a: float, b: float, atol: float, label: str) -> float:
    delta = abs(float(a) - float(b))
    if delta > atol:
        raise AssertionError(f"{label}: {a} versus {b}; delta={delta}")
    return delta


def chi2_close(a: float, b: float, label: str) -> float:
    return close(a, b, max(1.0e-8, 1.0e-10 * abs(float(b))), label)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-dir", type=Path, default=DEFAULT_DIST,
        help="directory containing DES-Dovekie_HD.csv and the compact precision files")
    parser.add_argument(
        "--check-only", action="store_true",
        help="print the replay without writing INDEPENDENT_VERIFICATION.json")
    args = parser.parse_args()
    dist = args.data_dir.resolve()

    table = load_table(dist)
    keep = np.flatnonzero(table["IDSURVEY"] == 10)
    w_all = load_precision(dist, "STAT+SYS.npz")
    w_des = marginal_precision(w_all, keep)
    model = direct_model(table["zHD"][keep], N_G99)
    primary_chi2, primary_offset = profile(w_des, table["MU"][keep], model)
    primary = json.loads((HERE / "PRIMARY_RESULT.json").read_text())

    w_stat = marginal_precision(load_precision(dist, "STATONLY.npz"), keep)
    stat_chi2, stat_offset = profile(
        w_stat, table["MU"][keep], direct_model(table["zHD"][keep], N_G99))
    hel_chi2, hel_offset = profile(
        w_des, table["MU"][keep], direct_model(table["zHEL"][keep], N_G99))
    full_chi2, full_offset = profile(
        w_all, table["MU"], direct_model(table["zHD"], N_G99))
    secondary = json.loads((HERE / "SECONDARY_RESULT.json").read_text())

    def objective(s: float) -> float:
        return profile(w_des, table["MU"][keep],
                       direct_model(table["zHD"][keep], 1.0 / float(s)))[0]

    opt = minimize_scalar(objective, bounds=S_BOUNDS, method="bounded",
                          options={"xatol": 1.0e-11, "maxiter": 1000})
    n_best = 1.0 / float(opt.x)
    delta_chi2 = objective(1.0 / N_G99) - float(opt.fun)
    shape = secondary["DES_only_shape_profile"]

    deltas = {
        "primary_chi2": chi2_close(primary_chi2, primary["chi2"], "primary chi2"),
        "primary_offset": close(primary_offset, primary["offset_B"], 1.0e-10, "primary offset"),
        "full_chi2": chi2_close(full_chi2, secondary["full_1820_STAT_SYS"]["chi2"], "full chi2"),
        "stat_chi2": chi2_close(stat_chi2, secondary["DES_only_STATONLY"]["chi2"], "stat chi2"),
        "hel_chi2": chi2_close(hel_chi2, secondary["DES_only_zHEL_STAT_SYS"]["chi2"], "hel chi2"),
        "shape_n": close(n_best, shape["n_best"], 1.0e-6, "shape n"),
        "shape_delta_chi2": close(delta_chi2, shape["delta_chi2_frozen_minus_best"], 1.0e-7,
                                  "shape delta chi2"),
    }
    result = {
        "status": "PASS_INDEPENDENT_SCHUR_AND_DIRECT_POWER_REPLAY",
        "method_independence": [
            "numpy genfromtxt instead of production line parser",
            "precision Schur complement instead of full precision inversion and covariance subblock",
            "direct power P1 instead of log1p/expm1 P1",
            "single bounded shape minimizer instead of production grid plus local minimizer"
        ],
        "data_dir": str(dist),
        "n_all": int(table.size), "n_des": int(keep.size),
        "replayed": {"primary_chi2": primary_chi2, "primary_offset": primary_offset,
                     "full_chi2": full_chi2, "full_offset": full_offset,
                     "stat_chi2": stat_chi2, "stat_offset": stat_offset,
                     "hel_chi2": hel_chi2, "hel_offset": hel_offset,
                     "n_best": n_best, "shape_delta_chi2": delta_chi2},
        "absolute_differences": deltas,
    }
    if not args.check_only:
        (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
