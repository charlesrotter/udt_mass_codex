#!/usr/bin/env python3
"""Outcome-informed, non-regrading G278 resolution diagnostic."""

from __future__ import annotations

import csv
import json
import math

import numpy as np

from derive_scale_and_holdout import (
    K_VALUES,
    PACKAGE,
    hat_basis,
    read_des,
    read_pantheon,
    scale_fit,
    state_fit,
    verify_sources,
)


GRID_N = 4097
REFERENCE_K = 12


def write_tsv(rows: list[dict[str, object]]) -> None:
    with (PACKAGE / "RESOLUTION_CURVE_COMPARISON.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    verify_sources()
    table, routes = read_pantheon()
    des_z, _, _, _ = read_des()
    covariance = routes["symmetric_mean"]

    z = np.asarray(table["zCMB"], float)
    magnitude = np.asarray(table["m_b_corr"], float)
    calibrator = np.asarray(table["IS_CALIBRATOR"], int)
    survey = np.asarray(table["IDSURVEY"], int)
    phi_min = float(np.min(np.log1p(des_z)))
    phi_max = float(np.max(np.log1p(des_z)))
    flow = np.flatnonzero(
        (z > 0.023)
        & (calibrator == 0)
        & (survey != 10)
        & (np.log1p(z) >= phi_min)
        & (np.log1p(z) <= phi_max)
    )
    cal = np.flatnonzero(calibrator == 1)
    flow_phi = np.log1p(z[flow])
    flow_y = magnitude[flow] - 10.0 * np.log10(1.0 + z[flow])
    cff = covariance[np.ix_(flow, flow)]
    grid = np.linspace(phi_min, phi_max, GRID_N)
    midpoint_index = (GRID_N - 1) // 2
    drop = int(math.ceil(0.05 * GRID_N))
    interior = slice(drop, GRID_N - drop)

    models: dict[int, dict[str, np.ndarray | float]] = {}
    for k in K_VALUES:
        knots = np.linspace(phi_min, phi_max, k)
        state = state_fit(flow_phi, flow_y, cff, knots)
        scale = scale_fit(table, covariance, cal, flow, np.asarray(state["operator"])[0], flow_y)
        theta = np.asarray(state["coefficients"])[1:]
        theta_weight = np.zeros((k - 1, len(table)))
        theta_weight[:, flow] = np.asarray(state["operator"])[1:]
        parameter_weight = np.vstack([np.asarray(scale["a_weight"]), theta_weight])
        design_grid = np.column_stack([np.ones(GRID_N), hat_basis(grid, knots)[:, 1:]])
        value_grid = design_grid @ np.r_[float(scale["a_mag"]), theta]
        models[k] = {
            "knots": knots,
            "parameter_weight": parameter_weight,
            "design_grid": design_grid,
            "value_grid": value_grid,
        }

    rows: list[dict[str, object]] = []
    all_boundary_max = True
    all_interior_rms_smaller = True
    reference = models[REFERENCE_K]
    for k in (8, 16, 24):
        model = models[k]
        difference = np.asarray(model["value_grid"]) - np.asarray(reference["value_grid"])
        joint_weight = np.vstack([model["parameter_weight"], reference["parameter_weight"]])
        joint_covariance = joint_weight @ covariance @ joint_weight.T
        difference_design = np.column_stack([model["design_grid"], -np.asarray(reference["design_grid"])])
        variance = np.einsum("ij,jk,ik->i", difference_design, joint_covariance, difference_design)
        sigma = np.sqrt(np.maximum(variance, 0.0))
        standardized = np.divide(
            np.abs(difference), sigma, out=np.zeros_like(difference), where=sigma > 0.0
        )
        maximum_index = int(np.argmax(np.abs(difference)))
        maximum_in_boundary = bool(maximum_index < drop or maximum_index >= GRID_N - drop)
        full_rms = float(np.sqrt(np.mean(difference**2)))
        interior_rms = float(np.sqrt(np.mean(difference[interior] ** 2)))
        all_boundary_max = all_boundary_max and maximum_in_boundary
        all_interior_rms_smaller = all_interior_rms_smaller and interior_rms < full_rms
        rows.append(
            {
                "K": k,
                "reference_K": REFERENCE_K,
                "max_abs_difference_mag": float(np.max(np.abs(difference))),
                "full_rms_difference_mag": full_rms,
                "interior90_max_abs_difference_mag": float(np.max(np.abs(difference[interior]))),
                "interior90_rms_difference_mag": interior_rms,
                "max_location_phi": float(grid[maximum_index]),
                "max_location_fraction": float(maximum_index / (GRID_N - 1)),
                "max_in_boundary_band": maximum_in_boundary,
                "max_absolute_standardized_difference": float(np.max(standardized)),
                "midpoint_phi": float(grid[midpoint_index]),
                "midpoint_difference_mag": float(difference[midpoint_index]),
                "midpoint_sigma_mag": float(sigma[midpoint_index]),
                "midpoint_absolute_z": float(standardized[midpoint_index]),
            }
        )

    consecutive = {}
    for left, right in ((8, 12), (12, 16), (16, 24)):
        difference = np.asarray(models[left]["value_grid"]) - np.asarray(models[right]["value_grid"])
        consecutive[f"{left}_{right}"] = {
            "full_rms_difference_mag": float(np.sqrt(np.mean(difference**2))),
            "interior90_rms_difference_mag": float(np.sqrt(np.mean(difference[interior] ** 2))),
        }

    landing = (
        "BOUNDARY_COORDINATE_SENSITIVITY_DOMINATES"
        if all_boundary_max and all_interior_rms_smaller
        else "PHYSICAL_CURVE_RESOLUTION_SENSITIVITY_PERSISTS"
    )
    result = {
        "audit": "G278_OUTCOME_INFORMED_RESOLUTION_DIAGNOSTIC",
        "landing": landing,
        "cannot_regrade_original": True,
        "original_landing": "SCALE_ATTACHMENT_RESOLUTION_OR_SUBSET_SENSITIVE",
        "grid": {
            "nodes": GRID_N,
            "phi_min": phi_min,
            "phi_max": phi_max,
            "midpoint_phi": float(grid[midpoint_index]),
            "boundary_drop_nodes_each_side": drop,
        },
        "comparison_rows": rows,
        "consecutive": consecutive,
        "classification_checks": {
            "all_maxima_in_boundary_bands": all_boundary_max,
            "all_interior_rms_smaller_than_full": all_interior_rms_smaller,
        },
        "forbidden_actions": {
            "preferred_K_selected": False,
            "scales_averaged": False,
            "smoother_added": False,
            "profile_fitted": False,
            "DES_retuned": False,
            "metric_or_kernel_changed": False,
        },
    }
    with (PACKAGE / "RESOLUTION_FOLLOWUP_RESULT.json").open("w") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    write_tsv(rows)
    rendered = json.dumps(result, indent=2, sort_keys=True)
    (PACKAGE / "RESOLUTION_FOLLOWUP_RUN_LOG.txt").write_text(
        "COMMAND: G236_DES_ROOT=<declared scratch data root> python3 diagnose_resolution_sensitivity.py\n"
        + rendered
        + "\n"
    )
    print(rendered)


if __name__ == "__main__":
    main()
