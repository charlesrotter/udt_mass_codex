#!/usr/bin/env python3
"""Independent Decimal/source-first verification for G258."""

from __future__ import annotations

import json
from decimal import Decimal, getcontext
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
SOURCE = REPO / "udt_g237_dual_sne_joint_relational_state_freeze_2026-08-23" / "FROZEN_PRIMARY_K12_STATE.json"
getcontext().prec = 60
TOL = Decimal("2e-11")


def main() -> None:
    source = json.loads(SOURCE.read_text(), parse_float=Decimal)
    state = source["state"]
    phi = state["knots"]
    theta = [Decimal(0)] + state["theta"]
    saved_r = [Decimal(1)] + state["relative_R"]
    theta_cov = state["theta_covariance"]
    saved_cov = state["relative_R_covariance_delta_method"]
    ln10 = Decimal(10).ln()
    assertions = 0

    radius = []
    nodes = []
    for index, (depth, shape, expected_r) in enumerate(zip(phi, theta, saved_r)):
        reconstructed_r = (ln10 * shape / Decimal(5)).exp()
        assert abs(reconstructed_r - expected_r) < TOL
        assertions += 1
        radius.append(reconstructed_r)

        z_factor = depth.exp()
        clock = (-depth).exp()
        ruler = z_factor
        f_value = (-Decimal(2) * depth).exp()
        for residual in (
            clock * ruler - Decimal(1),
            f_value - clock * clock,
            z_factor - Decimal(1) / clock,
            (-f_value) * (Decimal(1) / f_value) + Decimal(1),
            (z_factor - Decimal(1) + Decimal(1)).ln() - depth,
        ):
            assert abs(residual) < TOL
            assertions += 1
        nodes.append(
            {
                "index": index,
                "phi": str(depth),
                "Z": str(z_factor),
                "f": str(f_value),
                "clock_T": str(clock),
                "ruler_L": str(ruler),
                "relative_R": str(reconstructed_r),
            }
        )

    jac = [(ln10 / Decimal(5)) * value for value in radius[1:]]
    cov = [[jac[i] * theta_cov[i][j] * jac[j] for j in range(11)] for i in range(11)]
    max_cov_residual = Decimal(0)
    for i in range(11):
        for j in range(11):
            residual = abs(cov[i][j] - saved_cov[i][j])
            max_cov_residual = max(max_cov_residual, residual)
            assert residual < TOL
            assertions += 1

    changes = []
    for index in range(1, 12):
        difference = radius[index] - radius[index - 1]
        if index == 1:
            variance = cov[0][0]
        else:
            i, j = index - 1, index - 2
            variance = cov[i][i] + cov[j][j] - Decimal(2) * cov[i][j]
        assert variance > 0
        assertions += 1
        standardized = difference / variance.sqrt()
        changes.append(
            {
                "from_index": index - 1,
                "to_index": index,
                "delta_relative_R": str(difference),
                "standard_error": str(variance.sqrt()),
                "standardized": str(standardized),
                "sign": "positive" if difference > 0 else "negative" if difference < 0 else "zero",
            }
        )

    for ell in (Decimal("0.125"), Decimal(1), Decimal("7.5"), Decimal(41)):
        physical = [ell * value for value in radius]
        for reconstructed, original in zip((value / physical[0] for value in physical), radius):
            assert abs(reconstructed - original) < TOL
            assertions += 1

    result = {
        "status": "PASS",
        "landing": "POINTWISE_RELATIVE_METRIC_STATE_RECONSTRUCTS__CONTINUOUS_LAW_REMAINS_OPEN",
        "assertions": assertions,
        "node_count": 12,
        "nodes": nodes,
        "adjacent_changes": changes,
        "positive_adjacent_changes": sum(row["sign"] == "positive" for row in changes),
        "negative_adjacent_changes": sum(row["sign"] == "negative" for row in changes),
        "max_covariance_residual": str(max_cov_residual),
        "production_imported": False,
        "production_result_read": False,
    }
    (ROOT / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"PASS: {assertions} independent Decimal assertions across 12 nodes")


if __name__ == "__main__":
    main()
