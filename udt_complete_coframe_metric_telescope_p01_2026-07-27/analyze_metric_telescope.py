#!/usr/bin/env python3
"""Deterministic descriptive census for the frozen P01 primary atlas."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr


SHELLS = (("0030", 0.03), ("0100", 0.10), ("0300", 0.30), ("1000", 1.00), ("2500", 2.50))
AMPLITUDES = ("phi", "sigma", "alpha", "k", "S10", "S11", "S20", "S21")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def finite_stats(values: np.ndarray) -> dict[str, float | int]:
    finite = values[np.isfinite(values)]
    return {
        "finite_count": int(finite.size),
        "minimum": float(np.min(finite)) if finite.size else float("nan"),
        "median": float(np.median(finite)) if finite.size else float("nan"),
        "maximum": float(np.max(finite)) if finite.size else float("nan"),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("atlas", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    shell_records = []
    arrays = []
    names = None
    coefficients = None
    correlations = {}
    for tag, shell in SHELLS:
        path = args.atlas / f"ATLAS_shell_{tag}_N1024_T17_X33_MEXP64.npz"
        with np.load(path, allow_pickle=False) as data:
            current_names = data["feature_names"].tolist()
            current_coefficients = data["coefficients"]
            features = data["features"]
        if names is None:
            names = current_names
            coefficients = current_coefficients
        if current_names != names or not np.array_equal(current_coefficients, coefficients):
            raise AssertionError("shells do not share the frozen coefficient universe")
        arrays.append(features)
        index = {name: names.index(name) for name in names}
        timelike = features[:, index["dphi_timelike_fraction"]]
        null = features[:, index["dphi_null_fraction"]]
        spacelike = features[:, index["dphi_spacelike_fraction"]]
        zero = features[:, index["dphi_zero_fraction"]]
        repeated = features[:, index["tidal_repeated_fraction"]]
        unresolved = features[:, index["transport_numerically_unresolved"]] > 0.5
        nontrivial = features[:, index["holonomy_nontrivial"]] > 0.5
        resolved = ~unresolved
        record = {
            "shell": shell,
            "checkpoint_sha256": digest(path),
            "configurations": int(len(features)),
            "grid_points_per_configuration": 17 * 33,
            "local_point_evaluations": int(len(features) * 17 * 33),
            "grid_resolved_configurations": int(np.sum(features[:, index["grid_nonfinite_fraction"]] == 0)),
            "causal_presence": {
                "timelike_present": int(np.sum(timelike > 0)),
                "null_present": int(np.sum(null > 0)),
                "spacelike_present": int(np.sum(spacelike > 0)),
                "zero_gradient_present": int(np.sum(zero > 0)),
                "timelike_and_spacelike_present": int(np.sum((timelike > 0) & (spacelike > 0))),
            },
            "mean_grid_fractions": {
                "timelike": float(np.mean(timelike)),
                "null": float(np.mean(null)),
                "spacelike": float(np.mean(spacelike)),
                "zero_gradient": float(np.mean(zero)),
            },
            "repeated_screen_tidal": {
                "configurations_with_any_registered_repetition": int(np.sum(repeated > 0)),
                "registered_repeated_grid_points": int(round(float(np.sum(repeated) * 17 * 33))),
            },
            "local_feature_ranges": {
                name: finite_stats(features[:, index[name]])
                for name in (
                    "det_relative_error_max",
                    "scalar_rms",
                    "kretschmann_abs_max",
                    "pair_screen_ricci_mix_max",
                    "dphi_norm_min",
                    "dphi_norm_max",
                    "tidal_discriminant_min",
                )
            },
            "transport": {
                "resolved": int(np.sum(resolved)),
                "unresolved": int(np.sum(unresolved)),
                "nontrivial_among_resolved": int(np.sum(nontrivial & resolved)),
                "trivial_among_resolved": int(np.sum((~nontrivial) & resolved)),
                "pair_screen_mixing_among_resolved": finite_stats(features[resolved, index["holonomy_pair_screen_mixing"]]),
                "deviation_among_resolved": finite_stats(features[resolved, index["holonomy_deviation"]]),
            },
        }
        shell_records.append(record)
        amplitude_rms = np.sqrt(np.mean(current_coefficients**2, axis=2))
        response = np.column_stack(
            (
                np.log1p(features[:, index["scalar_rms"]]),
                np.log1p(features[:, index["kretschmann_abs_max"]]),
                np.log1p(features[:, index["pair_screen_ricci_mix_max"]]),
                np.log1p(np.maximum(0.0, features[:, index["dphi_norm_max"]] - features[:, index["dphi_norm_min"]])),
            )
        )
        response_names = ("log1p_scalar_rms", "log1p_kretschmann_max", "log1p_pair_screen_ricci_mix", "log1p_dphi_norm_span")
        matrix = np.empty((len(AMPLITUDES), len(response_names)))
        for i in range(len(AMPLITUDES)):
            for j in range(len(response_names)):
                matrix[i, j] = spearmanr(amplitude_rms[:, i], response[:, j]).statistic
        correlations[str(shell)] = {
            "row_amplitude_coefficient_rms": list(AMPLITUDES),
            "column_response": list(response_names),
            "spearman_matrix": matrix.tolist(),
            "scope": "DESCRIPTIVE_COEFFICIENT_NORM_ASSOCIATION_NOT_CAUSAL_SENSITIVITY",
        }
    stacked = np.stack(arrays, axis=0)
    index = {name: names.index(name) for name in names}
    monotonic = {}
    for name in ("scalar_rms", "kretschmann_abs_max", "pair_screen_ricci_mix_max"):
        values = stacked[:, :, index[name]]
        monotonic[name] = {
            "strictly_increasing_across_all_five_shells": int(np.sum(np.all(np.diff(values, axis=0) > 0, axis=0))),
            "not_strictly_increasing": int(np.sum(~np.all(np.diff(values, axis=0) > 0, axis=0))),
        }
    result = {
        "schema": "udt-p01-descriptive-structure-census-1.0",
        "status": "OBSERVED_BOUNDED_OFF_SHELL_ATLAS",
        "coefficient_universe_sha256": hashlib.sha256(coefficients.tobytes()).hexdigest(),
        "total_configurations": int(sum(record["configurations"] for record in shell_records)),
        "total_local_point_evaluations": int(sum(record["local_point_evaluations"] for record in shell_records)),
        "shells": shell_records,
        "same_configuration_shell_transitions": monotonic,
        "complete_amplitude_norm_correlation_tables": correlations,
        "scope_warning": "Sobol frequency and correlations are numerical coverage descriptions, not a physical measure, selector, dynamics, or prediction.",
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "total_configurations": result["total_configurations"], "total_local_point_evaluations": result["total_local_point_evaluations"], "same_configuration_shell_transitions": monotonic}, sort_keys=True))


if __name__ == "__main__":
    main()
