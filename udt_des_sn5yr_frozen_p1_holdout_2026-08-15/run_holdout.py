#!/usr/bin/env python3
"""G100 frozen-G99 P1 versus DES-SN5YR/Dovekie.

Physics/data premises are frozen in PREREGISTRATION.md and TEST_CONTRACT.json.
This script never reads the release cosmology chains or metadata cosmology columns.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.linalg import cho_factor, cho_solve
from scipy.optimize import brentq, minimize_scalar
from scipy.stats import chi2 as chi2_dist

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
DATA_ROOT = Path(
    "/media/udt-admin/ScratchDisk/Data/UDT_DES_SN5YR_DOVEKIE_2026-08-15"
)
DIST = DATA_ROOT / "4_DISTANCES_COVMAT"
TABLE = DIST / "DES-Dovekie_HD.csv"
STAT_SYS = DIST / "STAT+SYS.npz"
STAT_ONLY = DIST / "STATONLY.npz"
N_G99 = 1.0559332414320268  # OBSERVED_CONDITIONAL:G99; fixed primary shape.
EXPECTED_ALL = 1820  # PINNED_BY_OFFICIAL_RELEASE.
EXPECTED_DES = 1623  # PINNED_BY_FROZEN_DOVEKIE_VECTOR_DRY_GATE.
S_BOUNDS = (1.0e-4, 40.0)  # CHOSE: inherited G99/M3 diagnostic bounds.


def dump_json(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def verify_manifest() -> list[dict]:
    rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST_PREREG.tsv").open(), delimiter="\t"))
    out = []
    for row in rows:
        p = Path(row["path"])
        if not p.is_absolute():
            p = REPO / p
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        out.append({"path": row["path"], "expected": row["sha256"],
                    "actual": actual, "pass": actual == row["sha256"]})
    if not all(r["pass"] for r in out):
        raise RuntimeError("source manifest mismatch")
    return out


def read_table(include_mu: bool) -> dict[str, np.ndarray]:
    names = None
    cols: dict[str, list] = {}
    with TABLE.open() as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("VARNAMES:"):
                names = line.split()[1:]
                cols = {name: [] for name in names}
                continue
            if not line.startswith("SN:") or names is None:
                raise ValueError(f"unexpected table line: {line[:80]}")
            values = line.split()[1:]
            if len(values) != len(names):
                raise ValueError("table field count mismatch")
            raw_row = dict(zip(names, values))
            for name in names:
                if name == "CID":
                    cols[name].append(raw_row[name])
                elif name == "MU" and not include_mu:
                    cols[name].append(np.nan)
                else:
                    cols[name].append(float(raw_row[name]))
    if names is None:
        raise ValueError("missing VARNAMES header")
    out = {"CID": np.asarray(cols["CID"], dtype=str)}
    for name in names:
        if name != "CID":
            out[name] = np.asarray(cols[name], dtype=float)
    return out


def unpack_precision(path: Path) -> np.ndarray:
    with np.load(path, allow_pickle=False) as data:
        n = int(data["nsn"][0])
        packed = np.asarray(data["cov"], dtype=np.float64)
    if packed.size != n * (n + 1) // 2:
        raise ValueError("packed precision length mismatch")
    precision = np.zeros((n, n), dtype=np.float64)
    iu = np.triu_indices(n)
    precision[iu] = packed
    precision[(iu[1], iu[0])] = packed
    return precision


def dry_run() -> dict:
    manifest = verify_manifest()
    tab = read_table(include_mu=False)
    w = unpack_precision(STAT_SYS)
    idx = np.flatnonzero(tab["IDSURVEY"] == 10)
    np.linalg.cholesky(w)
    result = {
        "status": "SCHEMA_AND_COVARIANCE_DRY_GATE_PASS",
        "manifest": manifest,
        "n_all": int(len(tab["CID"])),
        "n_des": int(idx.size),
        "zHD_all_range": [float(tab["zHD"].min()), float(tab["zHD"].max())],
        "zHD_des_range": [float(tab["zHD"][idx].min()), float(tab["zHD"][idx].max())],
        "precision_shape": list(w.shape),
        "precision_symmetry_max_abs": float(np.max(np.abs(w - w.T))),
        "precision_cholesky": "PASS",
        "mu_consumed": False,
    }
    if result["n_all"] != EXPECTED_ALL or result["n_des"] != EXPECTED_DES:
        raise RuntimeError("released row count differs from preregistration")
    dump_json(HERE / "DRY_RUN_RESULT.json", result)
    print(json.dumps(result, indent=2))
    return result


def mu_shape(z: np.ndarray, n: float = N_G99) -> np.ndarray:
    z = np.asarray(z, dtype=np.float64)
    if np.any(z <= 0.0) or n <= 0.0:
        raise ValueError("P1 magnitude shape requires z>0 and n>0")
    log_zp1 = np.log1p(z)
    log_d = np.log(n) + 2.0 * log_zp1 + np.log(-np.expm1(-2.0 * log_zp1 / n))
    return (5.0 / np.log(10.0)) * log_d


def marginal_covariance(full_precision: np.ndarray, keep: np.ndarray) -> np.ndarray:
    factor = cho_factor(full_precision, lower=True, check_finite=True)
    full_cov = cho_solve(factor, np.eye(full_precision.shape[0]), check_finite=True)
    cov = full_cov[np.ix_(keep, keep)]
    return 0.5 * (cov + cov.T)


def profile_from_cov(cov: np.ndarray, observed: np.ndarray,
                     model: np.ndarray) -> dict:
    factor = cho_factor(cov, lower=True, check_finite=True)
    one = np.ones(observed.size)
    resid0 = observed - model
    w1 = cho_solve(factor, one, check_finite=True)
    wr = cho_solve(factor, resid0, check_finite=True)
    s11 = float(one @ w1)
    s1r = float(one @ wr)
    offset = s1r / s11
    chi2 = float(resid0 @ wr - s1r * s1r / s11)
    return {"chi2": chi2, "offset_B": offset,
            "residual": resid0 - offset, "cov_factor": factor}


def profile_from_precision(precision: np.ndarray, observed: np.ndarray,
                           model: np.ndarray) -> dict:
    one = np.ones(observed.size)
    resid0 = observed - model
    w1 = precision @ one
    wr = precision @ resid0
    s11 = float(one @ w1)
    s1r = float(one @ wr)
    offset = s1r / s11
    chi2 = float(resid0 @ wr - s1r * s1r / s11)
    return {"chi2": chi2, "offset_B": offset, "residual": resid0 - offset}


def tail_record(chi2: float, dof: int) -> dict:
    upper = float(chi2_dist.sf(chi2, dof))
    lower = float(chi2_dist.cdf(chi2, dof))
    if upper < 0.01:
        status = "FIXED_P1_DES_TENSION"
    elif lower < 0.01:
        status = "LOW_CHI2_COVARIANCE_OR_EFFECTIVE_DOF_WARNING"
    else:
        status = "FIXED_P1_DES_COMPATIBLE"
    return {"status": status, "chi2": chi2, "dof": dof,
            "reduced_chi2": chi2 / dof, "upper_tail_p": upper,
            "lower_tail_p": lower}


def primary_run() -> dict:
    verify_manifest()
    dry = json.loads((HERE / "DRY_RUN_RESULT.json").read_text())
    if dry["status"] != "SCHEMA_AND_COVARIANCE_DRY_GATE_PASS":
        raise RuntimeError("dry gate did not pass")
    tab = read_table(include_mu=True)
    keep = np.flatnonzero(tab["IDSURVEY"] == 10)
    full_precision = unpack_precision(STAT_SYS)
    cov_des = marginal_covariance(full_precision, keep)
    np.linalg.cholesky(cov_des)
    fit = profile_from_cov(cov_des, tab["MU"][keep], mu_shape(tab["zHD"][keep]))
    tails = tail_record(fit["chi2"], keep.size - 1)
    result = {
        **tails,
        "program": "G100",
        "primary": True,
        "profile": "P1",
        "n_frozen": N_G99,
        "sample": "IDSURVEY==10",
        "n_data": int(keep.size),
        "redshift": "zHD",
        "observation": "MU",
        "covariance": "STAT+SYS marginal DES block",
        "offset_B": fit["offset_B"],
        "absolute_scale_inferred": False,
        "LambdaCDM_distance_used": False,
        "secondary_diagnostics_evaluated": False,
    }
    dump_json(HERE / "PRIMARY_RESULT.json", result)
    print(json.dumps(result, indent=2))
    return result


def profile_shape_diagnostic(cov: np.ndarray, z: np.ndarray,
                             observed: np.ndarray) -> dict:
    factor = cho_factor(cov, lower=True, check_finite=True)
    one = np.ones(observed.size)
    w1 = cho_solve(factor, one, check_finite=True)
    s11 = float(one @ w1)

    def objective(s: float) -> float:
        resid0 = observed - mu_shape(z, n=1.0 / float(s))
        wr = cho_solve(factor, resid0, check_finite=False)
        s1r = float(one @ wr)
        return float(resid0 @ wr - s1r * s1r / s11)

    grid = np.geomspace(S_BOUNDS[0], S_BOUNDS[1], 161)
    vals = np.asarray([objective(s) for s in grid])
    k = int(np.argmin(vals))
    lo = grid[max(0, k - 1)]
    hi = grid[min(grid.size - 1, k + 1)]
    opt = minimize_scalar(objective, bounds=(lo, hi), method="bounded",
                          options={"xatol": 1.0e-10})
    s_best = float(opt.x)
    c2_best = float(opt.fun)
    target = c2_best + 1.0
    lo_open = objective(S_BOUNDS[0]) < target
    hi_open = objective(S_BOUNDS[1]) < target
    s_lo = S_BOUNDS[0] if lo_open else brentq(
        lambda s: objective(s) - target, S_BOUNDS[0], s_best)
    s_hi = S_BOUNDS[1] if hi_open else brentq(
        lambda s: objective(s) - target, s_best, S_BOUNDS[1])
    frozen = objective(1.0 / N_G99)
    return {
        "s_best": s_best, "n_best": 1.0 / s_best,
        "s_delta_chi2_1": {"lo": float(s_lo), "hi": float(s_hi),
                             "lo_open": lo_open, "hi_open": hi_open},
        "n_delta_chi2_1": {"lo": 1.0 / float(s_hi), "hi": 1.0 / float(s_lo),
                             "lo_open": hi_open, "hi_open": lo_open},
        "chi2_best": c2_best, "chi2_frozen": frozen,
        "delta_chi2_frozen_minus_best": frozen - c2_best,
        "bounds_s": list(S_BOUNDS), "primary_repair_permitted": False,
    }


def residual_bins(z: np.ndarray, residual: np.ndarray) -> list[dict]:
    order = np.argsort(z, kind="stable")
    groups = np.array_split(order, 10)
    rows = []
    for i, idx in enumerate(groups):
        r = residual[idx]
        rows.append({"bin": i + 1, "n": int(idx.size),
                     "z_min": float(z[idx].min()), "z_max": float(z[idx].max()),
                     "mean_residual_mag": float(np.mean(r)),
                     "rms_residual_mag": float(np.sqrt(np.mean(r * r)))})
    return rows


def secondary_run() -> dict:
    primary = json.loads((HERE / "PRIMARY_RESULT.json").read_text())
    if not primary.get("primary"):
        raise RuntimeError("primary result must be written first")
    verify_manifest()
    tab = read_table(include_mu=True)
    keep = np.flatnonzero(tab["IDSURVEY"] == 10)
    w_all = unpack_precision(STAT_SYS)
    c_des = marginal_covariance(w_all, keep)

    full_fit = profile_from_precision(
        w_all, tab["MU"], mu_shape(tab["zHD"]))
    full_tail = tail_record(full_fit["chi2"], len(tab["MU"]) - 1)

    w_stat = unpack_precision(STAT_ONLY)
    c_des_stat = marginal_covariance(w_stat, keep)
    stat_fit = profile_from_cov(
        c_des_stat, tab["MU"][keep], mu_shape(tab["zHD"][keep]))
    stat_tail = tail_record(stat_fit["chi2"], keep.size - 1)

    hel_fit = profile_from_cov(
        c_des, tab["MU"][keep], mu_shape(tab["zHEL"][keep]))
    hel_tail = tail_record(hel_fit["chi2"], keep.size - 1)

    primary_fit = profile_from_cov(
        c_des, tab["MU"][keep], mu_shape(tab["zHD"][keep]))
    shape = profile_shape_diagnostic(
        c_des, tab["zHD"][keep], tab["MU"][keep])
    result = {
        "status": "SECONDARY_DIAGNOSTICS_COMPLETE",
        "primary_status_unchanged": primary["status"],
        "full_1820_STAT_SYS": {**full_tail, "offset_B": full_fit["offset_B"]},
        "DES_only_STATONLY": {**stat_tail, "offset_B": stat_fit["offset_B"]},
        "DES_only_zHEL_STAT_SYS": {**hel_tail, "offset_B": hel_fit["offset_B"]},
        "DES_only_shape_profile": shape,
        "DES_only_equal_count_residual_bins": residual_bins(
            tab["zHD"][keep], primary_fit["residual"]),
        "LambdaCDM_distance_used": False,
        "may_repair_primary": False,
    }
    dump_json(HERE / "SECONDARY_RESULT.json", result)
    print(json.dumps(result, indent=2))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--primary", action="store_true")
    mode.add_argument("--secondary", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        dry_run()
    elif args.primary:
        primary_run()
    else:
        secondary_run()


if __name__ == "__main__":
    main()
