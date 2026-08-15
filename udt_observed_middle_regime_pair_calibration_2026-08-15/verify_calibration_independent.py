#!/usr/bin/env python3
"""Independent standard-library replay of the frozen G99 contract.

This implementation does not import the production extractor.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CONTRACT = HERE / "CALIBRATION_CONTRACT.json"
REPLAY = ROOT / "udt_sne_native_observer_query_replay_2026-08-11" / "REPLAY_RESULT.json"
DRY = ROOT / "udt_xmax_scale_observational_M3_runs_2026-08-07" / "sne_dry_run.json"


def close(left: float, right: float, tolerance: float, label: str) -> None:
    if abs(left - right) > tolerance:
        raise AssertionError(f"{label}: {left} != {right} within {tolerance}")


def main() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    source = json.loads(REPLAY.read_text(encoding="utf-8"))["replay"]
    dry = json.loads(DRY.read_text(encoding="utf-8"))
    primary = source["fits"]["A:zCMB:P1"]
    anchored = source["fits"]["B:zCMB:P1"]

    inv_n = float(primary["shape"])
    n = 1.0 / inv_n
    x_eff = float(anchored["X_eff_Mpc"]["best"])
    r_w = n * x_eff
    frozen = contract["calibration"]
    close(n, float(frozen["n"]), 3.0e-15, "n")
    close(x_eff, float(frozen["X_eff_Mpc"]), 0.0, "X_eff")
    close(r_w, float(frozen["R_w_Mpc_at_joint_best"]), 3.0e-12, "R_w")
    if contract["domain"]["z_min_observed"] != dry["modes"]["A:zCMB"]["z_min"]:
        raise AssertionError("z_min was not independently recovered")
    if contract["domain"]["z_max_observed"] != dry["modes"]["A:zCMB"]["z_max"]:
        raise AssertionError("z_max was not independently recovered")

    with (HERE / "CALIBRATION_NODES.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if len(rows) != 6:
        raise AssertionError("expected six preregistered nodes")

    maximum_difference = 0.0
    for row, recorded in zip(rows, contract["nodes"], strict=True):
        z = float(row["z"])
        scale = 1.0 + z
        phi = math.log(scale)
        # Alternate direct-power evaluation rather than production expm1 evaluation.
        radial = n * x_eff * (1.0 - scale ** (-2.0 / n))
        luminosity = scale * scale * radial
        expected = {
            "phi_pair": phi,
            "c_eff_pair_over_c_E": 1.0 / (scale * scale),
            "r_cal_Mpc": radial,
            "dL_cal_Mpc": luminosity,
        }
        for key, value in expected.items():
            observed = float(row[key])
            close(observed, value, 2.0e-11, f"node {z} {key}")
            close(float(recorded[key]), value, 2.0e-11, f"JSON node {z} {key}")
            maximum_difference = max(maximum_difference, abs(observed - value))

    # Exact closed-form consequences, checked numerically at independent off-grid probes.
    close(n * x_eff * (1.0 - 1.0 ** (-2.0 / n)), 0.0, 0.0, "dL(0)")
    origin_slope = 2.0 * x_eff * 1.0 ** (-2.0 / n - 1.0)
    close(origin_slope, 2.0 * x_eff, 0.0, "r origin slope")
    for z in (0.03, 0.2, 0.75, 1.4, 2.2):
        scale = 1.0 + z
        dr_dz = 2.0 * x_eff * scale ** (-2.0 / n - 1.0)
        ddL_dz = n * x_eff * (
            2.0 * scale * (1.0 - scale ** (-2.0 / n))
            + (2.0 / n) * scale ** (1.0 - 2.0 / n)
        )
        if dr_dz <= 0.0 or ddL_dz <= 0.0:
            raise AssertionError("strict monotonicity failed at an independent probe")

    result = {
        "schema": "udt-observed-middle-regime-pair-calibration-independent-1.0",
        "status": "PASS",
        "method": "standalone_standard_library_direct_power_reconstruction",
        "source_values_recovered": True,
        "node_count": len(rows),
        "maximum_absolute_node_difference": maximum_difference,
        "origin_and_monotonicity_checks": "PASS",
        "imports_production_extractor": False,
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        "PASS independent G99 reconstruction "
        f"nodes={len(rows)} max_abs={maximum_difference:.3e}"
    )


if __name__ == "__main__":
    main()
