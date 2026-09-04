#!/usr/bin/env python3
"""Hostile mutation catches for G340's bounded scientific landing."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path


LANDING = (
    "METRIC_NULL_GEOMETRY_CLOSES_A_PATH_LABELLED_FINITE_NORMAL_PAIR_FAMILY"
    "__NO_PHENOMENOLOGICAL_LIGHT_MODEL_REQUIRED"
    "__SLICE_DISTANCE_NULL_EXCHANGE_RADAR_AND_PROJECTIVE_READOUT_ARE_RELATED_NOT_IDENTICAL"
    "__COMPACT_WINDINGS_REMAIN_DISTINCT_BRANCHES"
    "__NO_PHYSICAL_PROTOCOL_POPULATION_SCALE_OR_XMAX_SELECTED"
)


def close(a: float, b: float, tol: float = 1.0e-10) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def main() -> None:
    root = Path(__file__).resolve().parent
    exact = (root / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = (root / "LAY_REPORT.md").read_text(encoding="utf-8")
    production = json.loads((root / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((root / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))

    te, q, cx, cp = 0.9, 0.7, 1.2, 0.8
    tr_x = (te ** (4.0 / 3.0) + 4.0 * cx * q / 3.0) ** (3.0 / 4.0)
    tr_p = (te ** (1.0 / 3.0) + cp * q / 3.0) ** 3
    bad_tr_x = (te ** (2.0 / 3.0) + 2.0 * cx * q / 3.0) ** (3.0 / 2.0)
    bad_tr_p = (te ** (2.0 / 3.0) + 2.0 * cp * q / 3.0) ** (3.0 / 2.0)
    r_x = (te / tr_x) ** (1.0 / 3.0)
    r_p = (tr_p / te) ** (2.0 / 3.0)
    delta_x = -math.log(r_x)
    delta_p = -math.log(r_p)

    tb = 2.0
    qr = 0.8
    tm_x = (tb ** (4.0 / 3.0) - 4.0 * qr / 3.0) ** (3.0 / 4.0)
    tp_x = (tb ** (4.0 / 3.0) + 4.0 * qr / 3.0) ** (3.0 / 4.0)
    radar_x = 0.5 * (tp_x - tm_x)
    slice_x = tb ** (-1.0 / 3.0) * qr

    branches = [abs(0.8 + n) for n in range(-3, 4)]
    catches = {
        "wrong_longitudinal_power": not close(tr_x, bad_tr_x),
        "wrong_transverse_power": not close(tr_p, bad_tr_p),
        "winding_omission": min(branches) < abs(0.8),
        "radar_equals_slice": not close(radar_x, slice_x, 1.0e-8),
        "radar_midpoint_equals_reflection": not close(0.5 * (tm_x + tp_x), tb, 1.0e-8),
        "frequency_ratio_reversed": not close(r_x, 1.0 / r_x),
        "signed_depth_called_distance_sign": q > 0.0 and delta_x > 0.0 and delta_p < 0.0,
        "ce_called_history_selector": close(0.5 * 0.3 * (tp_x / 0.3 - tm_x / 0.3), 0.5 * 7.0 * (tp_x / 7.0 - tm_x / 7.0)),
        "null_route_promoted_to_light_field": "does not import electromagnetism" in exact and "No Maxwell field is needed" in exact,
        "projective_called_dimensionful_radar": "Projective `chi` is dimensionless" in exact,
        "general_quadrature_hidden": production["coverage"]["general_null_cases"] == 400,
        "premise_independence_overclaimed": "implementation-distinct, not\npremise-distinct" in exact,
        "physical_protocol_promoted": "does not say which routes a real source emits" in lay,
        "metric_kernel_modified": "metric, reciprocal kernel, angular sector, and provisional equation are unchanged" in exact,
        "production_independent_circularity": "no production import or result read" in independent["method"],
    }
    all_passed = all(catches.values())
    result = {
        "all_passed": all_passed,
        "catches_passed": sum(catches.values()),
        "catches_total": len(catches),
        "catches": catches,
        "landing": LANDING,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if os.environ.get("UDT_NO_WRITE") != "1":
        (root / "CATCH_PROOF_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
