#!/usr/bin/env python3
"""G258 production reconstruction from the frozen G237 sampled state."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
SOURCE = REPO / "udt_g237_dual_sne_joint_relational_state_freeze_2026-08-23" / "FROZEN_PRIMARY_K12_STATE.json"
TOL = 2.0e-12


def main() -> None:
    source = json.loads(SOURCE.read_text())
    state = source["state"]
    phi = state["knots"]
    theta = [0.0] + state["theta"]
    saved_r = [1.0] + state["relative_R"]
    theta_cov = state["theta_covariance"]
    saved_r_cov = state["relative_R_covariance_delta_method"]

    assert len(phi) == len(theta) == len(saved_r) == 12
    reconstructed_r = [10.0 ** (value / 5.0) for value in theta]
    r_residual = max(abs(a - b) for a, b in zip(reconstructed_r, saved_r))
    assert r_residual < TOL

    nodes = []
    algebra_residual = 0.0
    for index, (depth, radius) in enumerate(zip(phi, reconstructed_r)):
        z_factor = math.exp(depth)
        redshift = z_factor - 1.0
        clock = 1.0 / z_factor
        ruler = z_factor
        f_value = math.exp(-2.0 * depth)
        residuals = (
            abs(clock * ruler - 1.0),
            abs(f_value - clock * clock),
            abs(z_factor - 1.0 / clock),
            abs(z_factor - ruler),
            abs((-f_value) * (1.0 / f_value) + 1.0),
            abs(math.log1p(redshift) - depth),
        )
        algebra_residual = max(algebra_residual, *residuals)
        nodes.append(
            {
                "index": index,
                "phi": depth,
                "z": redshift,
                "Z": z_factor,
                "f": f_value,
                "clock_T": clock,
                "ruler_L": ruler,
                "relative_R": radius,
                "g00_over_cE2": -f_value,
                "gRR": 1.0 / f_value,
                "angular_radius_over_ell": radius,
            }
        )
    assert algebra_residual < TOL

    jac = [(math.log(10.0) / 5.0) * value for value in reconstructed_r[1:]]
    reconstructed_cov = [
        [jac[i] * theta_cov[i][j] * jac[j] for j in range(11)]
        for i in range(11)
    ]
    covariance_residual = max(
        abs(reconstructed_cov[i][j] - saved_r_cov[i][j])
        for i in range(11)
        for j in range(11)
    )
    assert covariance_residual < TOL

    changes = []
    for index in range(1, 12):
        difference = reconstructed_r[index] - reconstructed_r[index - 1]
        if index == 1:
            variance = reconstructed_cov[0][0]
        else:
            i = index - 1
            j = index - 2
            variance = (
                reconstructed_cov[i][i]
                + reconstructed_cov[j][j]
                - 2.0 * reconstructed_cov[i][j]
            )
        assert variance > 0.0
        standard_error = math.sqrt(variance)
        changes.append(
            {
                "from_index": index - 1,
                "to_index": index,
                "delta_relative_R": difference,
                "standard_error": standard_error,
                "standardized": difference / standard_error,
                "sign": "positive" if difference > 0 else "negative" if difference < 0 else "zero",
            }
        )

    homothety_residual = 0.0
    for ell in (0.125, 1.0, 7.5, 41.0):
        physical = [ell * value for value in reconstructed_r]
        normalized = [value / physical[0] for value in physical]
        homothety_residual = max(
            homothety_residual,
            max(abs(a - b) for a, b in zip(normalized, reconstructed_r)),
        )
    assert homothety_residual < TOL

    landing = "POINTWISE_RELATIVE_METRIC_STATE_RECONSTRUCTS__CONTINUOUS_LAW_REMAINS_OPEN"
    result = {
        "status": "PASS",
        "landing": landing,
        "source_grade": source["epistemic_grade"],
        "source_query": source["query"],
        "node_count": len(nodes),
        "nodes": nodes,
        "adjacent_changes": changes,
        "positive_adjacent_changes": sum(row["sign"] == "positive" for row in changes),
        "negative_adjacent_changes": sum(row["sign"] == "negative" for row in changes),
        "maximum_residuals": {
            "saved_relative_R": r_residual,
            "algebra": algebra_residual,
            "delta_covariance": covariance_residual,
            "homothety": homothety_residual,
        },
        "absolute_scale": "one positive ell remains open",
        "continuous_history": "OPEN__no interpolation derivatives or field equation",
        "gr_use": "W3 comparison requirement only__static GR vacuum exterior not imposed on SNe branch",
        "fit_coefficients": 0,
    }
    (ROOT / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    with (ROOT / "NODE_ATLAS.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(nodes[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(nodes)
    with (ROOT / "ADJACENT_CHANGE_ATLAS.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(changes[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(changes)

    print(landing)
    print(f"nodes={len(nodes)} positive_changes={result['positive_adjacent_changes']} negative_changes={result['negative_adjacent_changes']}")
    print(f"max_algebra_residual={algebra_residual:.3e} max_covariance_residual={covariance_residual:.3e}")


if __name__ == "__main__":
    main()
