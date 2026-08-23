#!/usr/bin/env python3
"""Independent precision-domain replay for G236; reads no production artifact."""

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
DES_ROOT = Path(os.environ["G236_DES_ROOT"]).resolve()
OUT = PACKAGE / "INDEPENDENT_VERIFICATION.json"
K_VALUES = (8, 12, 16, 24)
PHI_MIN = 0.07077528204904217
PHI_MAX = 0.7627571949083936


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def logical_path(name: str) -> Path:
    external = {
        "external_data/README.md": DES_ROOT / "README.md",
        "external_data/DES-Dovekie_HD.csv": DES_ROOT / "DES-Dovekie_HD.csv",
        "external_data/STAT+SYS.npz": DES_ROOT / "STAT+SYS.npz",
    }
    return external.get(name, ROOT / name)


def frozen_sources() -> dict[str, bool]:
    checks = {}
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            path = logical_path(row["path"])
            checks[row["path"]] = path.is_file() and digest(path) == row["sha256"]
    if not checks or not all(checks.values()):
        raise AssertionError(checks)
    return checks


def pantheon() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    table = np.genfromtxt(
        ROOT / "Data/Pantheon+SH0ES.dat", names=True, dtype=None, encoding="utf-8"
    )
    z = np.asarray(table["zCMB"], dtype=np.float64)
    magnitude = np.asarray(table["m_b_corr"], dtype=np.float64)
    keep = np.flatnonzero(
        (z > 0.023)
        & (np.asarray(table["IS_CALIBRATOR"], dtype=int) == 0)
        & (np.asarray(table["IDSURVEY"], dtype=int) != 10)
        & (np.log1p(z) >= PHI_MIN)
        & (np.log1p(z) <= PHI_MAX)
    )
    covariance_path = ROOT / "Data/Pantheon+SH0ES_STAT+SYS.cov"
    with covariance_path.open() as stream:
        dimension = int(stream.readline())
        flat = np.fromfile(stream, sep=" ")
    covariance = flat.reshape(dimension, dimension)
    covariance = 0.5 * (covariance + covariance.T)
    covariance = covariance[np.ix_(keep, keep)]
    factor = cho_factor(covariance, lower=False, check_finite=True)
    precision = cho_solve(factor, np.eye(keep.size), check_finite=True)
    return np.log1p(z[keep]), magnitude[keep] - 10.0 * np.log10(1.0 + z[keep]), precision


def des() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    names = None
    rows: list[list[str]] = []
    with (DES_ROOT / "DES-Dovekie_HD.csv").open() as stream:
        for raw in stream:
            fields = raw.strip().split()
            if not fields or fields[0] == "#":
                continue
            if fields[0] == "VARNAMES:":
                names = fields[1:]
                continue
            if fields[0] != "SN:" or names is None:
                raise AssertionError("bad DES release row")
            rows.append(fields[1:])
    assert names is not None
    col = {name: i for i, name in enumerate(names)}
    survey = np.array([int(float(row[col["IDSURVEY"]])) for row in rows])
    z = np.array([float(row[col["zHD"]]) for row in rows])
    magnitude = np.array([float(row[col["MU"]]) for row in rows])
    keep = np.flatnonzero(survey == 10)
    omit = np.flatnonzero(survey != 10)
    with np.load(DES_ROOT / "STAT+SYS.npz", allow_pickle=False) as archive:
        n = int(archive["nsn"][0])
        packed = np.asarray(archive["cov"], dtype=np.float64)
    precision = np.zeros((n, n), dtype=np.float64)
    iu = np.triu_indices(n)
    precision[iu] = packed
    precision[(iu[1], iu[0])] = packed
    precision = 0.5 * (precision + precision.T)
    # Independent route: marginal precision is the Schur complement of omitted rows.
    pkk = precision[np.ix_(keep, keep)]
    pko = precision[np.ix_(keep, omit)]
    poo = precision[np.ix_(omit, omit)]
    poo_factor = cho_factor(poo, lower=False, check_finite=True)
    marginal_precision = pkk - pko @ cho_solve(poo_factor, pko.T, check_finite=True)
    marginal_precision = 0.5 * (marginal_precision + marginal_precision.T)
    return (
        np.log1p(z[keep]),
        magnitude[keep] - 10.0 * np.log10(1.0 + z[keep]),
        marginal_precision,
    )


def basis(phi: np.ndarray, knots: np.ndarray) -> np.ndarray:
    answer = np.zeros((phi.size, knots.size))
    left = np.clip(np.searchsorted(knots, phi, side="right") - 1, 0, knots.size - 2)
    fraction = (phi - knots[left]) / (knots[left + 1] - knots[left])
    answer[np.arange(phi.size), left] = 1.0 - fraction
    answer[np.arange(phi.size), left + 1] = fraction
    return answer


def fit(phi: np.ndarray, observed: np.ndarray, precision: np.ndarray, knots: np.ndarray) -> dict:
    design = np.column_stack((np.ones(phi.size), basis(phi, knots)[:, 1:]))
    normal = design.T @ precision @ design
    rhs = design.T @ precision @ observed
    factor = cho_factor(normal, lower=False, check_finite=True)
    coefficient = cho_solve(factor, rhs, check_finite=True)
    parameter_covariance = cho_solve(factor, np.eye(normal.shape[0]), check_finite=True)
    residual = observed - design @ coefficient
    chi2 = float(residual @ precision @ residual)
    dof = phi.size - knots.size
    ceiling = float(dof + 5.0 * math.sqrt(2.0 * dof))
    return {
        "n": int(phi.size),
        "dof": int(dof),
        "chi2": chi2,
        "ceiling": ceiling,
        "adequate": bool(chi2 <= ceiling),
        "offset": float(coefficient[0]),
        "theta": coefficient[1:],
        "theta_covariance": parameter_covariance[1:, 1:],
    }


def contrast(a: dict, b: dict, k: int) -> dict:
    delta = a["theta"] - b["theta"]
    covariance = a["theta_covariance"] + b["theta_covariance"]
    factor = cho_factor(covariance, lower=False, check_finite=True)
    chi2 = float(delta @ cho_solve(factor, delta, check_finite=True))
    ceiling = float((k - 1) + 5.0 * math.sqrt(2.0 * (k - 1)))
    return {
        "difference": delta,
        "difference_covariance": covariance,
        "chi2": chi2,
        "dof": k - 1,
        "ceiling": ceiling,
        "concordant": bool(chi2 <= ceiling),
    }


def jsonify(item):
    if isinstance(item, np.ndarray):
        return item.tolist()
    if isinstance(item, dict):
        return {key: jsonify(value) for key, value in item.items()}
    return item


def main() -> None:
    hashes = frozen_sources()
    pp, py, pprec = pantheon()
    dp, dy, dprec = des()
    if pp.size != 768 or dp.size != 1623:
        raise AssertionError((pp.size, dp.size))
    resolutions = {}
    for k in K_VALUES:
        knots = np.linspace(PHI_MIN, PHI_MAX, k)
        pf = fit(pp, py, pprec, knots)
        df = fit(dp, dy, dprec, knots)
        cp = contrast(pf, df, k)
        resolutions[str(k)] = jsonify(
            {"knots": knots, "pantheon": pf, "des": df, "comparison": cp}
        )

    knots = np.linspace(PHI_MIN, PHI_MAX, 12)
    df = fit(dp, dy, dprec, knots)
    null = contrast(df, df, 12)
    ramp = (dp - PHI_MIN) / (PHI_MAX - PHI_MIN)
    shifted = fit(dp, dy + 0.5 * ramp, dprec, knots)
    slope = contrast(df, shifted, 12)
    order = np.argsort(dp)
    sorted_fit = fit(dp[order], dy[order], dprec[np.ix_(order, order)], knots)
    rolled_fit = fit(
        np.roll(dp[order], dp.size // 2),
        dy[order],
        dprec[np.ix_(order, order)],
        knots,
    )
    hostile = {
        "duplicate_shape_chi2": null["chi2"],
        "duplicate_pass": bool(null["chi2"] <= 1e-10),
        "slope_mutation_shape_chi2": slope["chi2"],
        "slope_mutation_ceiling": slope["ceiling"],
        "slope_mutation_pass": bool(slope["chi2"] > slope["ceiling"]),
        "roll_unmutated_chi2": sorted_fit["chi2"],
        "roll_mutated_chi2": rolled_fit["chi2"],
        "roll_ratio": float(rolled_fit["chi2"] / sorted_fit["chi2"]),
        "roll_mutation_pass": bool(rolled_fit["chi2"] > 2.0 * sorted_fit["chi2"]),
    }
    if not all(value for key, value in hostile.items() if key.endswith("_pass")):
        raise AssertionError(hostile)
    result = {
        "audit": "G236_INDEPENDENT",
        "status": "PASS",
        "method": "direct precision GLS; Pantheon precision solve; DES omitted-block Schur complement; no production artifact",
        "source_hashes": hashes,
        "resolutions": resolutions,
        "hostile_controls": hostile,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "hostile_controls": hostile}, indent=2))


if __name__ == "__main__":
    main()
