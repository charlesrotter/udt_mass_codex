#!/usr/bin/env python3
"""Package and cross-implementation verifier for G236."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import os
from pathlib import Path

import numpy as np


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
DES_ROOT = Path(os.environ["G236_DES_ROOT"]).resolve()
PRODUCTION = PACKAGE / "PRODUCTION_RESULT.json"
INDEPENDENT = PACKAGE / "INDEPENDENT_VERIFICATION.json"
RESULT = PACKAGE / "VERIFICATION_RESULT.json"
K_VALUES = (8, 12, 16, 24)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def manifest_path(name: str) -> Path:
    external = {
        "external_data/README.md": DES_ROOT / "README.md",
        "external_data/DES-Dovekie_HD.csv": DES_ROOT / "DES-Dovekie_HD.csv",
        "external_data/STAT+SYS.npz": DES_ROOT / "STAT+SYS.npz",
    }
    return external.get(name, ROOT / name)


def source_checks() -> dict[str, bool]:
    checks = {}
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            path = manifest_path(row["path"])
            checks[row["path"]] = path.is_file() and sha256(path) == row["sha256"]
    return checks


def max_abs(a, b) -> float:
    return float(np.max(np.abs(np.asarray(a, dtype=float) - np.asarray(b, dtype=float))))


def validate_payload(production: dict, independent: dict) -> dict[str, bool | float]:
    checks: dict[str, bool | float] = {
        "production_status": production.get("status") == "PASS",
        "production_landing": production.get("landing")
        == "DUAL_SNE_RELATIONAL_STATE_CONCORDANCE_LEAD",
        "independent_status": independent.get("status") == "PASS",
        "pantheon_count": production.get("samples", {}).get("pantheon_non_des_common_support") == 768,
        "des_count": production.get("samples", {}).get("des_only") == 1623,
        "excluded_pantheon_des_count": production.get("samples", {}).get("excluded_pantheon_survey10") == 203,
        "exact_overlap_count": production.get("samples", {}).get("exact_cid_overlap") == 148,
        "registered_resolutions": set(production.get("resolutions", {})) == {str(k) for k in K_VALUES}
        and set(independent.get("resolutions", {})) == {str(k) for k in K_VALUES},
        "all_production_source_hashes": bool(production.get("source_hashes"))
        and all(production.get("source_hashes", {}).values()),
        "all_independent_source_hashes": bool(independent.get("source_hashes"))
        and all(independent.get("source_hashes", {}).values()),
        "duplicate_hostile": production.get("hostile_controls", {}).get("duplicate_pass") is True
        and independent.get("hostile_controls", {}).get("duplicate_pass") is True,
        "slope_hostile": production.get("hostile_controls", {}).get("slope_mutation_pass") is True
        and independent.get("hostile_controls", {}).get("slope_mutation_pass") is True,
        "roll_hostile": production.get("hostile_controls", {}).get("roll_mutation_pass") is True
        and independent.get("hostile_controls", {}).get("roll_mutation_pass") is True,
        "processed_caveat": production.get("checks", {}).get("processed_release_caveat_retained") is True,
        "p1_absent": production.get("checks", {}).get("p1_not_used") is True,
        "xmax_absent": production.get("checks", {}).get("xmax_not_used") is True,
        "lcdm_distance_absent": production.get("checks", {}).get("lcdm_distance_not_used") is True,
        "optimizer_absent": production.get("checks", {}).get("no_profile_optimizer") is True,
    }
    theta_max = 0.0
    covariance_max = 0.0
    residual_chi_max = 0.0
    shape_chi_max = 0.0
    for k in K_VALUES:
        pk = production["resolutions"][str(k)]
        ik = independent["resolutions"][str(k)]
        checks[f"K{k}_adequate"] = bool(pk["pantheon"]["adequate"] and pk["des"]["adequate"])
        checks[f"K{k}_concordant"] = bool(pk["comparison"]["concordant"])
        checks[f"K{k}_classification"] = (
            pk["classification"] == f"PROCESSED_RELEASE_SHAPES_CONCORDANT_AT_RESOLUTION_{k}"
        )
        for catalog in ("pantheon", "des"):
            theta_max = max(theta_max, max_abs(pk[catalog]["theta"], ik[catalog]["theta"]))
            covariance_max = max(
                covariance_max,
                max_abs(pk[catalog]["theta_covariance"], ik[catalog]["theta_covariance"]),
            )
            residual_chi_max = max(
                residual_chi_max, abs(pk[catalog]["chi2"] - ik[catalog]["chi2"])
            )
        shape_chi_max = max(
            shape_chi_max, abs(pk["comparison"]["chi2"] - ik["comparison"]["chi2"])
        )
    checks["max_theta_cross_residual"] = theta_max
    checks["max_covariance_cross_residual"] = covariance_max
    checks["max_raw_chi2_cross_residual"] = residual_chi_max
    checks["max_shape_chi2_cross_residual"] = shape_chi_max
    checks["theta_cross_tolerance"] = theta_max <= 1e-8
    checks["covariance_cross_tolerance"] = covariance_max <= 1e-8
    checks["raw_chi2_cross_tolerance"] = residual_chi_max <= 1e-7
    checks["shape_chi2_cross_tolerance"] = shape_chi_max <= 1e-7
    return checks


def main() -> None:
    production = json.loads(PRODUCTION.read_text())
    independent = json.loads(INDEPENDENT.read_text())
    checks = validate_payload(production, independent)
    hashes = source_checks()
    checks["manifest_hashes_current"] = bool(hashes) and all(hashes.values())
    independent_source = (PACKAGE / "verify_dual_sne_relational_state_independent.py").read_text()
    production_source = (PACKAGE / "derive_dual_sne_relational_state.py").read_text()
    checks["independent_reads_no_production_artifact"] = "PRODUCTION_RESULT.json" not in independent_source
    checks["no_scipy_optimizer_import"] = "scipy.optimize" not in production_source
    checks["no_frozen_p1_number"] = "1.0559332414320268" not in production_source
    checks["no_tanh_profile"] = "tanh(" not in production_source
    with (PACKAGE / "STATE_RECONSTRUCTION.tsv").open() as stream:
        row_count = sum(1 for _ in stream) - 1
    checks["state_table_row_count"] = row_count == sum(k - 1 for k in K_VALUES)
    booleans = [value for value in checks.values() if isinstance(value, bool)]
    result = {
        "audit": "G236_PACKAGE_VERIFICATION",
        "status": "PASS" if all(booleans) else "FAIL",
        "checks": checks,
        "source_hashes": hashes,
    }
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
