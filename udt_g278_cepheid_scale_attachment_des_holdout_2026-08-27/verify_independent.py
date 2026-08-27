#!/usr/bin/env python3
"""Implementation-distinct G278 verification using direct NumPy solves."""

from __future__ import annotations

import csv
import json
import math
import os
from pathlib import Path

import numpy as np


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
DES_ROOT = Path(os.environ["G236_DES_ROOT"]).resolve()
K_VALUES = (8, 12, 16, 24)


def basis(phi: np.ndarray, knots: np.ndarray) -> np.ndarray:
    out = np.zeros((phi.size, knots.size))
    for i, value in enumerate(phi):
        j = min(max(int(np.searchsorted(knots, value, side="right") - 1), 0), knots.size - 2)
        t = (value - knots[j]) / (knots[j + 1] - knots[j])
        out[i, j] = 1.0 - t
        out[i, j + 1] = t
    return out


def linear_gls(y: np.ndarray, design: np.ndarray, covariance: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    cinv_design = np.linalg.solve(covariance, design)
    normal_inverse = np.linalg.inv(design.T @ cinv_design)
    operator = normal_inverse @ cinv_design.T
    return operator @ y, operator, normal_inverse


def read_des() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    names = None
    rows: list[list[str]] = []
    with (DES_ROOT / "DES-Dovekie_HD.csv").open() as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("VARNAMES:"):
                names = line.split()[1:]
            else:
                if names is None or not line.startswith("SN:"):
                    raise AssertionError("DES parse")
                rows.append(line.split()[1:])
    assert names is not None
    ix = {name: i for i, name in enumerate(names)}
    z = np.asarray([float(row[ix["zHD"]]) for row in rows])
    mu = np.asarray([float(row[ix["MU"]]) for row in rows])
    survey = np.asarray([int(float(row[ix["IDSURVEY"]])) for row in rows])
    with np.load(DES_ROOT / "STAT+SYS.npz", allow_pickle=False) as data:
        n = int(data["nsn"][0])
        packed = np.asarray(data["cov"])
    precision = np.zeros((n, n))
    tri = np.triu_indices(n)
    precision[tri] = packed
    precision[(tri[1], tri[0])] = packed
    precision = (precision + precision.T) / 2.0
    full_covariance = np.linalg.inv(precision)
    keep = np.flatnonzero(survey == 10)
    return z[keep], mu[keep], full_covariance[np.ix_(keep, keep)]


def scale_from_subset(
    table: np.ndarray,
    covariance: np.ndarray,
    cal: np.ndarray,
    flow: np.ndarray,
    lb: np.ndarray,
    flow_y: np.ndarray,
) -> tuple[float, np.ndarray, float, int]:
    m = np.asarray(table["m_b_corr"], float)
    cepheid = np.asarray(table["CEPH_DIST"], float)
    q = np.r_[m[cal] - cepheid[cal], lb @ flow_y]
    ccc = covariance[np.ix_(cal, cal)]
    cross = covariance[np.ix_(cal, flow)] @ lb
    vb = float(lb @ covariance[np.ix_(flow, flow)] @ lb)
    cq = np.block([[ccc, cross[:, None]], [cross[None, :], np.asarray([[vb]])]])
    design = np.zeros((q.size, 2))
    design[:, 0] = 1.0
    design[-1, 1] = 1.0
    parameter, op, _ = linear_gls(q, design, cq)
    qop = np.zeros((q.size, len(table)))
    qop[np.arange(cal.size), cal] = 1.0
    qop[-1, flow] = lb
    weight = (op @ qop)[1]
    residual = q - design @ parameter
    chi2 = float(residual @ np.linalg.solve(cq, residual))
    return float(parameter[1] - 25.0), weight, chi2, int(q.size - 2)


def main() -> None:
    table = np.genfromtxt(ROOT / "Data/Pantheon+SH0ES.dat", names=True, dtype=None, encoding="utf-8")
    with (ROOT / "Data/Pantheon+SH0ES_STAT+SYS.cov").open() as handle:
        n = int(handle.readline())
        raw = np.fromfile(handle, sep=" ").reshape(n, n)
    covariance = (raw + raw.T) / 2.0
    des_z, des_mu, des_covariance = read_des()

    z = np.asarray(table["zCMB"], float)
    m = np.asarray(table["m_b_corr"], float)
    calibrator_flag = np.asarray(table["IS_CALIBRATOR"], int)
    survey = np.asarray(table["IDSURVEY"], int)
    cids = np.asarray(table["CID"], str)
    phi_min = float(np.min(np.log1p(des_z)))
    phi_max = float(np.max(np.log1p(des_z)))
    flow = np.flatnonzero(
        (z > 0.023)
        & (calibrator_flag == 0)
        & (survey != 10)
        & (np.log1p(z) >= phi_min)
        & (np.log1p(z) <= phi_max)
    )
    cal_all = np.flatnonzero(calibrator_flag == 1)
    flow_phi = np.log1p(z[flow])
    flow_y = m[flow] - 10.0 * np.log10(1.0 + z[flow])
    cff = covariance[np.ix_(flow, flow)]

    result = json.load((PACKAGE / "DERIVATION_RESULT.json").open())
    scale_rows = list(csv.DictReader((PACKAGE / "SCALE_RESULTS.tsv").open(), delimiter="\t"))
    expected_scale = {
        int(row["K"]): float(row["a_mag"])
        for row in scale_rows
        if row["covariance_route"] == "symmetric_mean"
    }

    states: dict[int, dict[str, np.ndarray | float]] = {}
    scale_errors: list[float] = []
    for k in K_VALUES:
        knots = np.linspace(phi_min, phi_max, k)
        design = np.c_[np.ones(flow.size), basis(flow_phi, knots)[:, 1:]]
        coefficients, operator, coefficient_covariance = linear_gls(flow_y, design, cff)
        a, a_weight, chi2_cal, dof_cal = scale_from_subset(
            table, covariance, cal_all, flow, operator[0], flow_y
        )
        scale_errors.append(abs(a - expected_scale[k]))
        states[k] = {
            "knots": knots,
            "coefficients": coefficients,
            "operator": operator,
            "coefficient_covariance": coefficient_covariance,
            "a": a,
            "a_weight": a_weight,
            "chi2_cal": chi2_cal,
            "dof_cal": dof_cal,
        }

    # Independent common-data resolution statistic.
    diff = np.asarray([states[k]["a"] - states[12]["a"] for k in (8, 16, 24)])
    dw = np.vstack([states[k]["a_weight"] - states[12]["a_weight"] for k in (8, 16, 24)])
    vdiff = dw @ covariance @ dw.T
    resolution_chi2 = float(diff @ np.linalg.pinv(vdiff, rcond=1e-12) @ diff)

    # Independent primary subset maximum.
    unique = sorted(set(cids[cal_all]))
    specs = [set(unique[0::2]), set(unique[1::2])]
    specs.extend(set(unique) - {cid} for cid in unique)
    primary = states[12]
    subset_z: list[float] = []
    for included in specs:
        cal = cal_all[np.asarray([cids[i] in included for i in cal_all])]
        a, weight, _, _ = scale_from_subset(table, covariance, cal, flow, primary["operator"][0], flow_y)
        delta = float(a - primary["a"])
        dweight = weight - primary["a_weight"]
        variance = float(dweight @ covariance @ dweight)
        subset_z.append(abs(delta) / math.sqrt(variance))

    # Independent no-retuning DES primary score.
    k = 12
    theta = np.asarray(primary["coefficients"])[1:]
    des_b = basis(np.log1p(des_z), np.asarray(primary["knots"]))[:, 1:]
    prediction = 25.0 + float(primary["a"]) + 10.0 * np.log10(1.0 + des_z) + des_b @ theta
    theta_weight = np.zeros((k - 1, len(table)))
    theta_weight[:, flow] = np.asarray(primary["operator"])[1:]
    joint_weight = np.vstack([primary["a_weight"], theta_weight])
    joint_covariance = joint_weight @ covariance @ joint_weight.T
    pdesign = np.c_[np.ones(des_z.size), des_b]
    total_covariance = des_covariance + pdesign @ joint_covariance @ pdesign.T
    residual = des_mu - prediction
    des_chi2 = float(residual @ np.linalg.solve(total_covariance, residual))

    checks = {
        "counts_match": bool(len(table) == 1701 and flow.size == 768 and cal_all.size == 77 and des_z.size == 1623),
        "all_four_scale_values_match": bool(max(scale_errors) <= 2e-10),
        "resolution_chi2_matches": bool(abs(resolution_chi2 - result["gates"]["resolution_chi2"]) <= 2e-8),
        "resolution_failure_reproduced": bool(resolution_chi2 > result["gates"]["resolution_ceiling"]),
        "subset_max_z_matches": bool(
            abs(max(subset_z) - max(float(row["absolute_z"]) for row in csv.DictReader((PACKAGE / "CALIBRATOR_SUBSET_CONTROLS.tsv").open(), delimiter="\t"))) <= 2e-8
        ),
        "all_subsets_below_five_sigma": bool(max(subset_z) <= 5.0),
        "primary_DES_chi2_matches": bool(abs(des_chi2 - result["DES"]["12"]["chi2"]) <= 2e-7),
        "primary_DES_pass_reproduced": bool(des_chi2 <= result["DES"]["12"]["ceiling"]),
        "no_DES_fit_columns": bool(result["frozen"]["DES_parameters_fitted"] == 0),
        "no_kernel_or_P1_retuning": bool(
            not result["frozen"]["kernel_retuned"]
            and not result["frozen"]["P1_used"]
            and result["frozen"]["angular_coefficients_fitted"] == 0
        ),
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    output = {
        "audit": "G278_INDEPENDENT_DIRECT_SOLVE_VERIFICATION",
        "checks": checks,
        "max_scale_abs_error_mag": max(scale_errors),
        "resolution_chi2": resolution_chi2,
        "max_subset_absolute_z": max(subset_z),
        "primary_DES_chi2": des_chi2,
        "landing_reproduced": result["landing"],
    }
    with (PACKAGE / "INDEPENDENT_VERIFICATION.json").open("w") as handle:
        json.dump(output, handle, indent=2, sort_keys=True)
        handle.write("\n")
    rendered = json.dumps(output, indent=2, sort_keys=True)
    (PACKAGE / "INDEPENDENT_RUN_LOG.txt").write_text(
        "COMMAND: G236_DES_ROOT=<declared scratch data root> python3 verify_independent.py\n"
        + rendered
        + "\n"
    )
    print(rendered)


if __name__ == "__main__":
    main()
