#!/usr/bin/env python3
"""Audit the pinned DESI DR2 Gaussian BAO release without fitting UDT."""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import subprocess
import sys
from pathlib import Path

import numpy as np


EXPECTED_DATA_COMMIT = "b7b8a36e9bccb063081f811f323cada21ab5fbdd"
EXPECTED_MEAN_SHA256 = "9ac154ab583ce759c0f7eef3c978c7c70a6ead2d18774caceadf1a350a640585"
EXPECTED_COV_SHA256 = "252a143274c8a07c78694c119617d36594f6d7965d00319ca611c6ffb886e509"

TABLE4 = {
    0.295: {"DV_over_rs": (7.942, 0.075)},
    0.510: {"DM_over_rs": (13.588, 0.167), "DH_over_rs": (21.863, 0.425)},
    0.706: {"DM_over_rs": (17.351, 0.177), "DH_over_rs": (19.455, 0.330)},
    0.934: {"DM_over_rs": (21.576, 0.152), "DH_over_rs": (17.641, 0.193)},
    1.321: {"DM_over_rs": (27.601, 0.318), "DH_over_rs": (14.176, 0.221)},
    1.484: {"DM_over_rs": (30.512, 0.760), "DH_over_rs": (12.817, 0.516)},
    2.330: {"DM_over_rs": (38.988, 0.531), "DH_over_rs": (8.632, 0.101)},
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def git_head(path: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(path), "rev-parse", "HEAD"], text=True
    ).strip()


def parse_measurements(path: Path):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        z, value, quantity = line.split()
        rows.append({"z": float(z), "value": float(value), "quantity": quantity})
    return rows


def released_logpdf(
    source: Path,
    dependency_path: Path,
    data_repo: Path,
    theory_vector: np.ndarray,
) -> float:
    sys.path.insert(0, str(dependency_path))
    sys.path.insert(0, str(source))
    from cobaya.likelihoods.base_classes.bao import BAO

    likelihood = object.__new__(BAO)
    likelihood.log = logging.getLogger("udt_bao_release_replay")
    likelihood.path = str(data_repo)
    likelihood.packages_path = None
    likelihood.measurements_file = (
        "desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_mean.txt"
    )
    likelihood.cov_file = "desi_bao_dr2/desi_gaussian_bao_ALL_GCcomb_cov.txt"
    likelihood.invcov_file = None
    likelihood.prob_dist = None
    likelihood.grid_file = None
    likelihood.rs_fid = 1
    likelihood.rs_rescale = None
    likelihood.initialize()
    return float(likelihood.logpdf(theory_vector))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-repo", type=Path, required=True)
    parser.add_argument("--cobaya-source", type=Path, required=True)
    parser.add_argument("--dependency-path", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ap-output", type=Path, required=True)
    args = parser.parse_args()

    data_dir = args.data_repo / "desi_bao_dr2"
    mean_path = data_dir / "desi_gaussian_bao_ALL_GCcomb_mean.txt"
    cov_path = data_dir / "desi_gaussian_bao_ALL_GCcomb_cov.txt"
    rows = parse_measurements(mean_path)
    values = np.array([row["value"] for row in rows], dtype=float)
    cov = np.loadtxt(cov_path)

    mean_hash = sha256(mean_path)
    cov_hash = sha256(cov_path)
    data_commit = git_head(args.data_repo)
    code_commit = git_head(args.cobaya_source)

    if data_commit != EXPECTED_DATA_COMMIT:
        raise AssertionError((data_commit, EXPECTED_DATA_COMMIT))
    if mean_hash != EXPECTED_MEAN_SHA256 or cov_hash != EXPECTED_COV_SHA256:
        raise AssertionError("official input hash changed")
    if len(rows) != 13 or cov.shape != (13, 13):
        raise AssertionError("unexpected DR2 vector shape")

    symmetry = float(np.max(np.abs(cov - cov.T)))
    eigenvalues = np.linalg.eigvalsh(cov)
    if symmetry != 0.0 or eigenvalues[0] <= 0.0:
        raise AssertionError("released covariance is not symmetric positive definite")

    allowed = np.zeros_like(cov, dtype=bool)
    allowed[0, 0] = True
    for i in range(1, 13, 2):
        allowed[i : i + 2, i : i + 2] = True
    off_block_max = float(np.max(np.abs(cov[~allowed])))
    if off_block_max != 0.0:
        raise AssertionError("unexpected cross-block covariance entry")

    table_checks = []
    max_mean_delta = 0.0
    max_sigma_delta = 0.0
    for i, row in enumerate(rows):
        expected_mean, expected_sigma = TABLE4[round(row["z"], 3)][row["quantity"]]
        sigma = float(np.sqrt(cov[i, i]))
        mean_delta = abs(row["value"] - expected_mean)
        sigma_delta = abs(sigma - expected_sigma)
        max_mean_delta = max(max_mean_delta, mean_delta)
        max_sigma_delta = max(max_sigma_delta, sigma_delta)
        table_checks.append(
            {
                **row,
                "sigma": sigma,
                "table4_mean": expected_mean,
                "table4_sigma": expected_sigma,
                "mean_abs_delta": mean_delta,
                "sigma_abs_delta": sigma_delta,
            }
        )
    # The release is a Gaussian distance-basis approximation.  Its central values should
    # reproduce Table 4, while sqrt(diag(cov)) need not equal the paper's separately
    # marginalized posterior widths after the nonlinear basis rotation.
    if max_mean_delta > 0.002:
        raise AssertionError("released Gaussian central values disagree with Table 4")
    if max_sigma_delta > 0.02:
        raise AssertionError("released Gaussian widths are unexpectedly far from Table 4")

    grouped = {}
    for index, row in enumerate(rows):
        grouped.setdefault(round(row["z"], 3), {})[row["quantity"]] = (index, row["value"])
    ap_rows = []
    for z, entries in sorted(grouped.items()):
        if "DM_over_rs" not in entries or "DH_over_rs" not in entries:
            continue
        i_dm, dm = entries["DM_over_rs"]
        i_dh, dh = entries["DH_over_rs"]
        gradient = np.array([1.0 / dh, -dm / dh**2])
        block = cov[np.ix_([i_dm, i_dh], [i_dm, i_dh])]
        sigma = float(np.sqrt(gradient @ block @ gradient))
        ap_rows.append({"z": z, "DM_over_DH": dm / dh, "delta_method_sigma": sigma})

    residual = np.linspace(-0.30, 0.30, len(values))
    theory = values + residual
    manual_logpdf = float(-0.5 * residual @ np.linalg.solve(cov, residual))
    package_logpdf = released_logpdf(
        args.cobaya_source, args.dependency_path, args.data_repo, theory
    )
    logpdf_abs_delta = abs(manual_logpdf - package_logpdf)
    if logpdf_abs_delta > 1e-12:
        raise AssertionError("independent Gaussian quadratic form disagrees with Cobaya")

    result = {
        "status": "PASS",
        "scope": "official DESI DR2 Gaussian data suitability; no UDT fit",
        "data_release": "CobayaSampler/bao_data v2.6",
        "data_commit": data_commit,
        "cobaya_commit": code_commit,
        "mean_sha256": mean_hash,
        "cov_sha256": cov_hash,
        "n_measurements": len(rows),
        "quantity_counts": {
            quantity: sum(row["quantity"] == quantity for row in rows)
            for quantity in sorted({row["quantity"] for row in rows})
        },
        "redshift_min": min(row["z"] for row in rows),
        "redshift_max": max(row["z"] for row in rows),
        "covariance": {
            "shape": list(cov.shape),
            "symmetry_max_abs": symmetry,
            "rank": int(np.linalg.matrix_rank(cov)),
            "eigenvalue_min": float(eigenvalues[0]),
            "eigenvalue_max": float(eigenvalues[-1]),
            "condition_2": float(np.linalg.cond(cov)),
            "off_registered_block_max_abs": off_block_max,
        },
        "table4_replay": {
            "interpretation": (
                "central values reproduce the paper; Gaussian covariance widths are an "
                "approximation and are not identical to separately marginalized Table 4 widths"
            ),
            "max_mean_abs_delta": max_mean_delta,
            "max_sigma_abs_delta": max_sigma_delta,
            "rows": table_checks,
        },
        "gaussian_replay": {
            "test_residual": residual.tolist(),
            "manual_logpdf": manual_logpdf,
            "cobaya_logpdf": package_logpdf,
            "abs_delta": logpdf_abs_delta,
        },
        "ap_shape_rows": ap_rows,
        "classification": {
            "full_vector_preregistered_label": "SCALE_READY_WITH_NUISANCE_RULER",
            "full_vector_operational_meaning": (
                "FULL_PATTERN_VECTOR_READY_ONLY_WITH_PUBLISHED_NORMALIZATION_NUISANCE"
            ),
            "anisotropic_shape_projection": "AP_READY_WITH_FIDUCIAL_MAP",
            "bgs": "ISOTROPIC_ONLY",
            "origin_interpretation": "NONE__OBSERVED_CORRELATION_PATTERN_ONLY",
        },
    }
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    lines = ["z\tDM_over_DH\tdelta_method_sigma"]
    for row in ap_rows:
        lines.append(
            f"{row['z']:.3f}\t{row['DM_over_DH']:.12g}\t{row['delta_method_sigma']:.12g}"
        )
    args.ap_output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "manual_logpdf": manual_logpdf,
                      "cobaya_logpdf": package_logpdf, "ap_rows": len(ap_rows)}))


if __name__ == "__main__":
    main()
