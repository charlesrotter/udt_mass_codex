#!/usr/bin/env python3
"""Fail-closed comparison of the primary P01 atlas and batch-16 replay."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np


SHELL_TAGS = ("0030", "0100", "0300", "1000", "2500")
DISCRETE_FEATURES = (
    "dphi_timelike_fraction",
    "dphi_null_fraction",
    "dphi_spacelike_fraction",
    "dphi_zero_fraction",
    "tidal_repeated_fraction",
    "grid_nonfinite_fraction",
    "holonomy_nontrivial",
    "transport_numerically_unresolved",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def shell_file(directory: Path, tag: str) -> Path:
    matches = list(directory.glob(f"ATLAS_shell_{tag}_N1024_T17_X33_MEXP64.npz"))
    if len(matches) != 1:
        raise AssertionError(f"expected exactly one shell {tag} NPZ in {directory}, got {matches}")
    return matches[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("primary", type=Path)
    parser.add_argument("replay", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    primary_result = json.loads((args.primary / "ATLAS_RESULT.json").read_text())
    replay_result = json.loads((args.replay / "ATLAS_RESULT.json").read_text())
    checks: dict[str, bool] = {}
    checks["coefficient_universe_hash_equal"] = primary_result["coefficient_universe_sha256"] == replay_result["coefficient_universe_sha256"]
    checks["amplitudes_equal"] = primary_result["amplitudes"] == replay_result["amplitudes"]
    checks["feature_names_equal"] = primary_result["feature_names"] == replay_result["feature_names"]
    checks["totals_equal"] = primary_result["totals"] == replay_result["totals"]
    checks["replay_peak_below_6_gib"] = replay_result["environment"]["peak_memory_bytes"] < 6 * 1024**3
    checks["same_gpu"] = primary_result["environment"]["device"] == replay_result["environment"]["device"]
    checks["same_dtype"] = primary_result["environment"]["dtype"] == replay_result["environment"]["dtype"] == "float64"
    feature_names = primary_result["feature_names"]
    discrete_indices = [feature_names.index(name) for name in DISCRETE_FEATURES]
    continuous_indices = [index for index in range(len(feature_names)) if index not in discrete_indices]
    maximum_scaled_error = 0.0
    shell_records = []
    for tag in SHELL_TAGS:
        ppath = shell_file(args.primary, tag)
        rpath = shell_file(args.replay, tag)
        with np.load(ppath, allow_pickle=False) as p, np.load(rpath, allow_pickle=False) as r:
            coefficients_equal = np.array_equal(p["coefficients"], r["coefficients"])
            names_equal = np.array_equal(p["feature_names"], r["feature_names"])
            pf, rf = p["features"], r["features"]
            shape_equal = pf.shape == rf.shape == (1024, len(feature_names))
            discrete_equal = shape_equal and np.array_equal(pf[:, discrete_indices], rf[:, discrete_indices])
            finite_class_equal = shape_equal and np.array_equal(np.isfinite(pf), np.isfinite(rf))
            inf_sign_equal = shape_equal and np.array_equal(np.signbit(pf[~np.isfinite(pf)]), np.signbit(rf[~np.isfinite(rf)]))
            finite = np.isfinite(pf[:, continuous_indices]) & np.isfinite(rf[:, continuous_indices])
            scaled = np.abs(pf[:, continuous_indices] - rf[:, continuous_indices]) / (1.0 + np.abs(pf[:, continuous_indices]))
            shell_max = float(np.max(scaled[finite])) if np.any(finite) else 0.0
            maximum_scaled_error = max(maximum_scaled_error, shell_max)
            record = {
                "shell_tag": tag,
                "primary_sha256": digest(ppath),
                "replay_sha256": digest(rpath),
                "coefficients_exact": bool(coefficients_equal),
                "feature_names_exact": bool(names_equal),
                "shape_exact": bool(shape_equal),
                "discrete_features_exact": bool(discrete_equal),
                "finite_class_exact": bool(finite_class_equal),
                "infinite_sign_exact": bool(inf_sign_equal),
                "continuous_max_scaled_error": shell_max,
            }
            shell_records.append(record)
            checks[f"shell_{tag}_structural"] = all(
                record[key]
                for key in ("coefficients_exact", "feature_names_exact", "shape_exact", "discrete_features_exact", "finite_class_exact", "infinite_sign_exact")
            )
            checks[f"shell_{tag}_continuous_tolerance"] = shell_max <= 2.0e-10
    result = {
        "schema": "udt-p01-resource-replay-verification-1.0",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "continuous_scaled_tolerance": 2.0e-10,
        "maximum_continuous_scaled_error": maximum_scaled_error,
        "checks": checks,
        "shells": shell_records,
        "primary_result_sha256": digest(args.primary / "ATLAS_RESULT.json"),
        "replay_result_sha256": digest(args.replay / "ATLAS_RESULT.json"),
        "primary_peak_memory_bytes": primary_result["environment"]["peak_memory_bytes"],
        "replay_peak_memory_bytes": replay_result["environment"]["peak_memory_bytes"],
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
