#!/usr/bin/env python3
"""Correctly scoped P01 resource replay verification."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np


SHELL_TAGS = ("0030", "0100", "0300", "1000", "2500")
TOLERANCE = 2.0e-10


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def shell_path(directory: Path, tag: str) -> Path:
    path = directory / f"ATLAS_shell_{tag}_N1024_T17_X33_MEXP64.npz"
    if not path.is_file():
        raise AssertionError(path)
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("primary", type=Path)
    parser.add_argument("replay", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    p_result = json.loads((args.primary / "ATLAS_RESULT.json").read_text())
    r_result = json.loads((args.replay / "ATLAS_RESULT.json").read_text())
    checks = {
        "coefficient_universe_hash_exact": p_result["coefficient_universe_sha256"] == r_result["coefficient_universe_sha256"],
        "feature_names_exact": p_result["feature_names"] == r_result["feature_names"],
        "replay_peak_below_6_gib": r_result["environment"]["peak_memory_bytes"] < 6 * 1024**3,
        "same_gpu": p_result["environment"]["device"] == r_result["environment"]["device"],
        "same_float64": p_result["environment"]["dtype"] == r_result["environment"]["dtype"] == "float64",
    }
    names = p_result["feature_names"]
    unresolved_index = names.index("transport_numerically_unresolved")
    nontrivial_index = names.index("holonomy_nontrivial")
    shell_records = []
    overall_max = 0.0
    for tag in SHELL_TAGS:
        ppath, rpath = shell_path(args.primary, tag), shell_path(args.replay, tag)
        with np.load(ppath, allow_pickle=False) as p, np.load(rpath, allow_pickle=False) as r:
            pf, rf = p["features"], r["features"]
            coefficients_exact = np.array_equal(p["coefficients"], r["coefficients"])
            local_exact = np.array_equal(pf[:, :14], rf[:, :14])
            masks_exact = np.array_equal(pf[:, unresolved_index], rf[:, unresolved_index])
            resolved = (pf[:, unresolved_index] == 0) & (rf[:, unresolved_index] == 0)
            transport_indices = list(range(14, unresolved_index))
            pa, ra = pf[resolved][:, transport_indices], rf[resolved][:, transport_indices]
            finite_exact = np.array_equal(np.isfinite(pa), np.isfinite(ra))
            with np.errstate(invalid="ignore", divide="ignore", over="ignore"):
                scaled = np.abs(pa - ra) / (1.0 + np.abs(pa))
            finite = np.isfinite(pa) & np.isfinite(ra)
            maximum = float(np.max(scaled[finite])) if np.any(finite) else 0.0
            overall_max = max(overall_max, maximum)
            nontrivial_exact = np.array_equal(pf[resolved, nontrivial_index], rf[resolved, nontrivial_index])
            record = {
                "shell_tag": tag,
                "coefficients_exact": bool(coefficients_exact),
                "local_features_exact": bool(local_exact),
                "transport_resolution_mask_exact": bool(masks_exact),
                "resolved_transport_rows": int(resolved.sum()),
                "unresolved_transport_rows": int((~resolved).sum()),
                "resolved_transport_finite_class_exact": bool(finite_exact),
                "resolved_nontrivial_class_exact": bool(nontrivial_exact),
                "resolved_transport_max_scaled_error": maximum,
                "primary_sha256": digest(ppath),
                "replay_sha256": digest(rpath),
            }
            shell_records.append(record)
            checks[f"shell_{tag}"] = bool(
                coefficients_exact and local_exact and masks_exact and finite_exact and nontrivial_exact and maximum <= TOLERANCE
            )
    result = {
        "schema": "udt-p01-resource-replay-scoped-verification-1.0",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "continuous_scaled_tolerance": TOLERANCE,
        "maximum_resolved_transport_scaled_error": overall_max,
        "checks": checks,
        "shells": shell_records,
        "primary_result_sha256": digest(args.primary / "ATLAS_RESULT.json"),
        "replay_result_sha256": digest(args.replay / "ATLAS_RESULT.json"),
        "primary_peak_memory_bytes": p_result["environment"]["peak_memory_bytes"],
        "replay_peak_memory_bytes": r_result["environment"]["peak_memory_bytes"],
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
