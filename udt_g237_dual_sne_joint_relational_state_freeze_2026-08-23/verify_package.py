#!/usr/bin/env python3
"""Fail-closed G237 package and cross-route verifier."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
PRODUCTION = PACKAGE / "JOINT_STATE_RESULT.json"
INDEPENDENT = PACKAGE / "INDEPENDENT_RAW_GLS.json"
OUT = PACKAGE / "VERIFICATION_RESULT.json"
K_VALUES = (8, 12, 16, 24)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_checks() -> dict[str, bool]:
    checks = {}
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            path = ROOT / row["path"]
            checks[row["path"]] = path.is_file() and sha256(path) == row["sha256"]
    return checks


def maximum_error(left, right) -> float:
    return float(np.max(np.abs(np.asarray(left, dtype=float) - np.asarray(right, dtype=float))))


def main() -> None:
    production = json.loads(PRODUCTION.read_text())
    independent = json.loads(INDEPENDENT.read_text())
    chronology_path = PACKAGE / "CHRONOLOGY_PROOF.json"
    chronology = json.loads(chronology_path.read_text()) if chronology_path.is_file() else {}
    bundle_verification_path = PACKAGE / "CHRONOLOGY_BUNDLE_VERIFICATION.json"
    bundle_verification = (
        json.loads(bundle_verification_path.read_text())
        if bundle_verification_path.is_file()
        else {}
    )
    hashes = source_checks()
    checks: dict[str, bool | float] = {
        "source_hashes": bool(hashes) and all(hashes.values()),
        "production_status": production.get("status") == "PASS",
        "independent_status": independent.get("status") == "PASS",
        "production_landing": production.get("landing")
        == "JOINT_DUAL_SNE_RELATIVE_STATE_FROZEN_WITH_CAVEATS",
        "primary_K12": production.get("primary_resolution") == 12,
        "state_rows": production.get("state_rows") == 56,
        "resolution_keys": set(production.get("resolutions", {})) == {str(k) for k in K_VALUES}
        and set(independent.get("resolutions", {})) == {str(k) for k in K_VALUES},
        "freeze_present": (PACKAGE / "FROZEN_PRIMARY_K12_STATE.json").is_file(),
        "chronology_status": chronology.get("status") == "PASS",
        "chronology_bundle_status": bundle_verification.get("status") == "PASS",
        "chronology_bundle_requires_no_git": bundle_verification.get("requires_live_git") is False,
        "preregistration_commit": chronology.get("commit", "").startswith("ad49b9c8"),
        "preregistration_unchanged": chronology.get("committed_equals_current") is True,
    }
    theta_error = 0.0
    covariance_error = 0.0
    raw_chi2_error = 0.0
    raw_identity_error = 0.0
    g236 = json.loads(
        (ROOT / "udt_g236_dual_sne_relational_state_reconstruction_2026-08-23/PRODUCTION_RESULT.json").read_text()
    )
    for k in K_VALUES:
        p = production["resolutions"][str(k)]
        i = independent["resolutions"][str(k)]
        theta_error = max(theta_error, maximum_error(p["theta"], i["theta"]))
        covariance_error = max(
            covariance_error, maximum_error(p["theta_covariance"], i["theta_covariance"])
        )
        raw_chi2_error = max(raw_chi2_error, abs(p["joint_raw_chi2"] - i["joint_raw_chi2"]))
        expected = (
            g236["resolutions"][str(k)]["pantheon"]["chi2"]
            + g236["resolutions"][str(k)]["des"]["chi2"]
            + g236["resolutions"][str(k)]["comparison"]["chi2"]
        )
        raw_identity_error = max(raw_identity_error, abs(p["joint_raw_chi2"] - expected))
        checks[f"K{k}_shape_identity"] = p["shape_identity_residual"] <= 1.0e-8
        checks[f"K{k}_joint_raw_adequate"] = p["joint_raw_adequate"] is True
    checks["max_theta_cross_error"] = theta_error
    checks["max_covariance_cross_error"] = covariance_error
    checks["max_raw_chi2_cross_error"] = raw_chi2_error
    checks["max_raw_identity_error"] = raw_identity_error
    checks["theta_cross_tolerance"] = theta_error <= 1.0e-8
    checks["covariance_cross_tolerance"] = covariance_error <= 1.0e-8
    checks["raw_chi2_cross_tolerance"] = raw_chi2_error <= 1.0e-7
    checks["raw_identity_tolerance"] = raw_identity_error <= 1.0e-7
    production_source = (PACKAGE / "derive_joint_state.py").read_text()
    independent_source = (PACKAGE / "verify_joint_state_from_raw.py").read_text()
    checks["independent_does_not_read_production"] = "JOINT_STATE_RESULT.json" not in independent_source
    checks["no_optimizer"] = "scipy.optimize" not in production_source + independent_source
    checks["no_tanh_profile"] = "tanh(" not in production_source + independent_source
    checks["no_p1_value"] = "1.0559332414320268" not in production_source + independent_source
    checks["covariance_caveat_retained"] = production.get("cross_release_covariance") == (
        "CHOSE_ZERO_AFTER_EXACT_CID_DEOVERLAP__UNKNOWN_SHARED_SYSTEMATICS_OPEN"
    )
    checks["independent_covariance_caveat_retained"] = independent.get(
        "cross_release_covariance"
    ) == "CHOSE_ZERO_AFTER_EXACT_CID_DEOVERLAP__UNKNOWN_SHARED_SYSTEMATICS_OPEN"
    booleans = [value for value in checks.values() if isinstance(value, bool)]
    result = {
        "audit": "G237_PACKAGE_VERIFICATION",
        "status": "PASS" if all(booleans) else "FAIL",
        "checks": checks,
        "source_hashes": hashes,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
