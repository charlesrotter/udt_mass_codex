#!/usr/bin/env python3
"""Deterministic descriptive census of the frozen P02-B atlas."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

import numpy as np


AXES = (
    "shell",
    "coordinate_time",
    "phi_gradient",
    "angular_shape",
    "shift_value_rank",
    "angular_first_rank",
    "shift_first_rank",
    "collective_Hessian_rank",
)


def numeric_rank(matrix: np.ndarray) -> int:
    singular = np.linalg.svd(matrix, compute_uv=False)
    return int(np.sum(singular > 1e-10 * max(1.0, singular[0])))


def distribution(values: np.ndarray) -> str:
    return ";".join(f"{key}:{value}" for key, value in sorted(Counter(map(int, values)).items()))


def finite_range(values: np.ndarray) -> tuple[float | str, float | str, float | str]:
    finite = values[np.isfinite(values)]
    if not len(finite):
        return "NA", "NA", "NA"
    return float(np.min(finite)), float(np.median(finite)), float(np.max(finite))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, required=True)
    args = parser.parse_args()
    package = args.package.resolve()
    with (package / "STRATUM_UNIVERSE.tsv").open(newline="") as handle:
        strata = list(csv.DictReader(handle, delimiter="\t"))
    stratum_by_id = {row["stratum_id"]: row for row in strata}
    with np.load(package / "JET_ATLAS.npz", allow_pickle=False) as source:
        source_status = source["status"]
        source_axes = source["requested_axes"]
        source_stratum_id = source["stratum_id"]
    with np.load(package / "REPEATED_TIDAL_ATLAS.npz", allow_pickle=False) as atlas:
        base_index = atlas["base_index"]
        target_code = atlas["target_code"]
        target_labels = atlas["target_labels"]
        target_lambda = atlas["target_lambda"]
        solved_ddq = atlas["solved_ddq"]
        response_rank = atlas["response_rank"]
        response_singular = atlas["response_singular_values"]
        hessian_norm = atlas["hessian_frobenius"]
        linear_residual = atlas["linear_residual"]
        reevaluated_residual = atlas["reevaluated_residual"]
        status = atlas["status"]
        features = atlas["features"]
        feature_names = atlas["feature_names"].tolist()
        tidal = atlas["tidal_components"]
    if len(strata) != 11520 or len(base_index) != 12594:
        raise AssertionError("frozen P02/P02-B universe size mismatch")
    if not np.all(source_status[base_index] == "CONSTRUCTED") or not np.all(source_axes[base_index, 7] == 0):
        raise AssertionError("P02-B base filter no longer matches the preregistration")
    actual_hessian_rank = np.array(
        [numeric_rank(value[:, np.triu_indices(4)[0], np.triu_indices(4)[1]]) for value in solved_ddq],
        dtype=np.int8,
    )
    feature = {name: features[:, column] for column, name in enumerate(feature_names)}
    repeated = feature["tidal_repeated"] > 0.5
    pair_screen_zero = feature["pair_screen_ricci_mixing"] <= 1e-10
    candidate_target = target_labels[target_code]
    base_rows = [stratum_by_id[str(source_stratum_id[index])] for index in base_index]
    ledger = []
    for candidate in range(len(base_index)):
        row = {
            "candidate_index": candidate,
            "base_attempt_index": int(base_index[candidate]),
            "stratum_id": str(source_stratum_id[base_index[candidate]]),
            "replicate": int(base_index[candidate] % 2),
            "target_label": candidate_target[candidate],
            "target_lambda": target_lambda[candidate],
        }
        row.update({axis: base_rows[candidate][axis] for axis in AXES})
        row.update(
            {
                "status": status[candidate],
                "response_rank": int(response_rank[candidate]),
                "response_singular_0": response_singular[candidate, 0],
                "response_singular_1": response_singular[candidate, 1],
                "response_singular_2": response_singular[candidate, 2],
                "solved_collective_Hessian_rank": int(actual_hessian_rank[candidate]),
                "Hessian_frobenius": hessian_norm[candidate],
                "linear_residual": linear_residual[candidate],
                "reevaluated_residual": reevaluated_residual[candidate],
                "T22": tidal[candidate, 0],
                "T23": tidal[candidate, 1],
                "T33": tidal[candidate, 2],
                "dphi_norm": feature["dphi_norm"][candidate],
                "scalar_curvature": feature["scalar_curvature"][candidate],
                "kretschmann": feature["kretschmann"][candidate],
                "pair_screen_ricci_mixing": feature["pair_screen_ricci_mixing"][candidate],
                "tidal_repeated": int(repeated[candidate]),
                "curvature_operator_rank": int(feature["curvature_operator_rank"][candidate]),
                "numerically_finite": int(feature["numerically_finite"][candidate]),
            }
        )
        ledger.append(row)
    with (package / "P02B_CANDIDATE_LEDGER.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(ledger[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(ledger)
    axis_rows = []
    for axis in AXES:
        axis_values = []
        for row in strata:
            if row[axis] not in axis_values:
                axis_values.append(row[axis])
        for value in axis_values:
            for label in target_labels:
                mask = np.array([row[axis] == value for row in base_rows]) & (candidate_target == label)
                minimum, median, maximum = finite_range(hessian_norm[mask])
                axis_rows.append(
                    {
                        "axis": axis,
                        "value": value,
                        "target_label": label,
                        "candidates": int(mask.sum()),
                        "constructed_repeated_tidal": int(np.sum(mask & (status == "CONSTRUCTED_REPEATED_TIDAL"))),
                        "response_rank_distribution": distribution(response_rank[mask]),
                        "solved_Hessian_rank_distribution": distribution(actual_hessian_rank[mask]),
                        "curvature_operator_rank_distribution": distribution(feature["curvature_operator_rank"][mask]),
                        "pair_screen_zero": int(np.sum(mask & pair_screen_zero)),
                        "Hessian_norm_minimum": minimum,
                        "Hessian_norm_median": median,
                        "Hessian_norm_maximum": maximum,
                        "max_reevaluated_residual": float(np.max(reevaluated_residual[mask])) if mask.any() else "NA",
                    }
                )
    with (package / "P02B_AXIS_CENSUS.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(axis_rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(axis_rows)
    causal_rows = []
    for time_mode in ("DYNAMIC_4D", "COORDINATE_STATIC"):
        for phi_class in ("ZERO", "TIMELIKE", "NULL", "SPACELIKE"):
            for label in target_labels:
                mask = np.array(
                    [row["coordinate_time"] == time_mode and row["phi_gradient"] == phi_class for row in base_rows]
                ) & (candidate_target == label)
                minimum, median, maximum = finite_range(hessian_norm[mask])
                causal_rows.append(
                    {
                        "coordinate_time": time_mode,
                        "phi_gradient": phi_class,
                        "target_label": label,
                        "candidates": int(mask.sum()),
                        "constructed_repeated_tidal": int(np.sum(mask & (status == "CONSTRUCTED_REPEATED_TIDAL"))),
                        "solved_Hessian_rank_distribution": distribution(actual_hessian_rank[mask]),
                        "Hessian_norm_minimum": minimum,
                        "Hessian_norm_median": median,
                        "Hessian_norm_maximum": maximum,
                        "max_reevaluated_residual": float(np.max(reevaluated_residual[mask])) if mask.any() else "NA",
                    }
                )
    with (package / "P02B_CAUSAL_TARGET_CENSUS.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(causal_rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(causal_rows)
    accepted = status == "CONSTRUCTED_REPEATED_TIDAL"
    bases = np.unique(base_index)
    summary = {
        "schema": "udt-p02b-repeated-tidal-census-1.0",
        "status": "OBSERVED_BOUNDED_LOCAL_OFF_SHELL_CONSTRUCTIBILITY_ATLAS",
        "bases": len(bases),
        "candidates": len(base_index),
        "status_counts": dict(sorted(Counter(status).items())),
        "target_counts": dict(sorted(Counter(candidate_target).items())),
        "response_rank_distribution": {str(key): value for key, value in sorted(Counter(map(int, response_rank)).items())},
        "solved_collective_Hessian_rank_distribution": {
            str(key): value for key, value in sorted(Counter(map(int, actual_hessian_rank)).items())
        },
        "curvature_operator_rank_distribution": {
            str(key): value for key, value in sorted(Counter(map(int, feature["curvature_operator_rank"])).items())
        },
        "phi_gradient_base_counts": dict(sorted(Counter(stratum_by_id[str(source_stratum_id[index])]["phi_gradient"] for index in bases).items())),
        "coordinate_time_base_counts": dict(sorted(Counter(stratum_by_id[str(source_stratum_id[index])]["coordinate_time"] for index in bases).items())),
        "null_candidates": int(np.sum(np.array([row["phi_gradient"] == "NULL" for row in base_rows]))),
        "null_constructed_repeated_tidal": int(np.sum(np.array([row["phi_gradient"] == "NULL" for row in base_rows]) & accepted)),
        "timelike_candidates": int(np.sum(np.array([row["phi_gradient"] == "TIMELIKE" for row in base_rows]))),
        "timelike_constructed_repeated_tidal": int(np.sum(np.array([row["phi_gradient"] == "TIMELIKE" for row in base_rows]) & accepted)),
        "tidal_repeated_by_registered_tolerance": int(np.sum(repeated)),
        "pair_screen_zero": int(np.sum(pair_screen_zero)),
        "numerically_finite": int(np.sum(feature["numerically_finite"] > 0.5)),
        "affine_linear_residual_maximum": float(np.max(linear_residual)),
        "reevaluated_residual_maximum": float(np.max(reevaluated_residual)),
        "Hessian_frobenius_range": {
            "minimum": float(np.min(hessian_norm)),
            "median": float(np.median(hessian_norm)),
            "maximum": float(np.max(hessian_norm)),
        },
        "scope_warning": "The exact frozen local two-jet chart admits the targets; no target, extension, global branch, equation, or physical role is selected.",
    }
    (package / "P02B_CENSUS.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
