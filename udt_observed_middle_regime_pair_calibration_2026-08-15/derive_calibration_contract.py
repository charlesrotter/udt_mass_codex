#!/usr/bin/env python3
"""Freeze the already banked P1 SNe result as a typed forward-use contract.

This script performs no fit. It verifies preregistered source bytes, extracts existing
results, evaluates the frozen closed form at preregistered nodes, and writes compact evidence.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MANIFEST = HERE / "SOURCE_MANIFEST_PREREG.tsv"
REPLAY = ROOT / "udt_sne_native_observer_query_replay_2026-08-11" / "REPLAY_RESULT.json"
INDEPENDENT = (
    ROOT
    / "udt_sne_native_observer_query_replay_2026-08-11"
    / "INDEPENDENT_PRIMARY.json"
)
DRY_RUN = ROOT / "udt_xmax_scale_observational_M3_runs_2026-08-07" / "sne_dry_run.json"
NODES = (0.02307, 0.1, 0.5, 1.0, 2.0, 2.2613)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_sources() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with MANIFEST.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            path = ROOT / row["path"]
            actual = sha256(path)
            if actual != row["sha256"]:
                raise AssertionError(f"source hash mismatch: {row['path']}")
            rows.append({"path": row["path"], "sha256": actual, "role": row["role"]})
    if len(rows) != 10:
        raise AssertionError(f"expected 10 preregistered sources, found {len(rows)}")
    return rows


def evaluate(z: float, n: float, x_eff: float) -> dict[str, float]:
    scale = 1.0 + z
    phi = math.log(scale)
    radial = n * x_eff * (-math.expm1(-2.0 * phi / n))
    luminosity = scale * scale * radial
    return {
        "z": z,
        "phi_pair": phi,
        "c_eff_pair_over_c_E": scale ** -2.0,
        "r_cal_Mpc": radial,
        "dL_cal_Mpc": luminosity,
    }


def main() -> None:
    sources = verify_sources()
    replay = json.loads(REPLAY.read_text(encoding="utf-8"))["replay"]
    independent = json.loads(INDEPENDENT.read_text(encoding="utf-8"))
    dry = json.loads(DRY_RUN.read_text(encoding="utf-8"))

    primary = replay["fits"]["A:zCMB:P1"]
    anchored = replay["fits"]["B:zCMB:P1"]
    inv_n = float(primary["shape"])
    n = float(primary["frozen_param_n"]["best"])
    x_eff = float(anchored["X_eff_Mpc"]["best"])
    r_w = float(anchored["R_w_Mpc_at_best_n"]["value"])
    anchor = replay["anchor"]

    if abs(inv_n * n - 1.0) > 2.0e-15:
        raise AssertionError("n and inv_n are not reciprocal")
    if abs(n * x_eff - r_w) > 2.0e-9:
        raise AssertionError("R_w does not equal n*X_eff at the joint best point")
    independent_best = independent["best"]
    if abs(float(independent_best["inv_n"]) - inv_n) > 2.0e-6:
        raise AssertionError("independent inv_n is outside preregistered tolerance")
    if abs(float(independent_best["chi2"]) - float(primary["chi2"])) > 2.0e-5:
        raise AssertionError("independent chi2 is outside preregistered tolerance")
    if abs(float(independent_best["X_eff_Mpc"]) - x_eff) > 5.0e-3:
        raise AssertionError("independent X_eff is outside preregistered tolerance")

    mode = dry["modes"]["A:zCMB"]
    if mode["n_after_cuts"] != primary["n_data"]:
        raise AssertionError("dry-run and fit row counts disagree")

    node_rows = [evaluate(z, n, x_eff) for z in NODES]
    if not all(row["r_cal_Mpc"] > 0.0 and row["dL_cal_Mpc"] > 0.0 for row in node_rows):
        raise AssertionError("positive-domain calibration is not positive")
    if not all(
        node_rows[index]["dL_cal_Mpc"] < node_rows[index + 1]["dL_cal_Mpc"]
        for index in range(len(node_rows) - 1)
    ):
        raise AssertionError("preregistered luminosity nodes are not strictly increasing")

    sensitivity = {
        "mode_C_inv_n": float(replay["fits"]["C:zCMB:P1"]["shape"]),
        "mode_D_zHD_inv_n": float(replay["fits"]["D:zHD:P1"]["shape"]),
        "mode_D_zHEL_inv_n": float(replay["fits"]["D:zHEL:P1"]["shape"]),
    }
    sensitivity["abs_C_minus_A_inv_n"] = abs(sensitivity["mode_C_inv_n"] - inv_n)
    sensitivity["abs_zHD_minus_zCMB_inv_n"] = abs(
        sensitivity["mode_D_zHD_inv_n"] - inv_n
    )
    sensitivity["abs_zHEL_minus_zCMB_inv_n"] = abs(
        sensitivity["mode_D_zHEL_inv_n"] - inv_n
    )

    contract = {
        "schema": "udt-observed-middle-regime-pair-calibration-1.0",
        "program": "G99",
        "status": "OBSERVED_CONDITIONAL_TERMINAL_CALIBRATION_FROZEN",
        "construction": {
            "optimizer_run": False,
            "known_banked_result_adopted_once": True,
            "holdout_data_read": False,
            "source_count": len(sources),
        },
        "object_type": "effective_terminal_observer_pair_luminosity_relation",
        "complete_metric_history_owned": False,
        "physical_pair_realization_owned": False,
        "orchestra_correction_appended": False,
        "transfer_law_derived": False,
        "c_eff_is_material_signal_speed": False,
        "absolute_scale_is_conditional": True,
        "R_w_is_marginal_measurement": False,
        "joint_n_X_eff_covariance_available": False,
        "marginal_intervals_form_independent_box": False,
        "calibration": {
            "profile": "P1",
            "inv_n": inv_n,
            "inv_n_interval": primary["shape_interval"],
            "n": n,
            "n_interval": primary["frozen_param_n"],
            "X_eff_Mpc": x_eff,
            "X_eff_interval_Mpc": anchored["X_eff_Mpc"],
            "R_w_Mpc_at_joint_best": r_w,
            "chi2": float(primary["chi2"]),
            "ndof": int(primary["ndof"]),
            "n_data": int(primary["n_data"]),
            "M_B": float(anchor["M_B"]),
            "M_B_error": float(anchor["err"]),
        },
        "domain": {
            "redshift_column": mode["zcol"],
            "z_cut": float(dry["frozen_z_cut"]),
            "z_min_observed": float(mode["z_min"]),
            "z_max_observed": float(mode["z_max"]),
            "calibrators_excluded": bool(mode["calibrators_excluded"]),
            "is_Xmax_interval": False,
        },
        "formulas": {
            "Z": "1+z",
            "phi_pair": "log(Z)",
            "c_eff_pair_over_c_E": "Z^(-2)",
            "r_cal_Mpc": "n*X_eff_Mpc*(1-Z^(-2/n))",
            "dL_cal_Mpc": "Z^2*r_cal_Mpc",
            "conditional_factorization": "d_A=r_cal; d_L=exp(2*phi_pair)*d_A",
            "radial_origin_slope": "dr_cal/dz at z=0 equals 2*X_eff_Mpc",
        },
        "sensitivity_diagnostics_not_fit_freedom": sensitivity,
        "nodes": node_rows,
        "holdouts": ["BAO", "CMB", "Xmax_endpoint", "micro_mass", "bootstrap"],
        "sources": sources,
        "explicit_nonclaims": [
            "complete_metric_history",
            "physical_pair_realization",
            "native_radiative_transfer",
            "time_live_regime_continuation",
            "Xmax_value_or_realization",
            "cosmology_action_source_matter_mass_or_bootstrap_closure",
            "rigorous_joint_n_X_eff_uncertainty_band",
        ],
    }

    (HERE / "CALIBRATION_CONTRACT.json").write_text(
        json.dumps(contract, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    with (HERE / "CALIBRATION_NODES.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, delimiter="\t", fieldnames=list(node_rows[0]), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(node_rows)
    print(
        "PASS G99 frozen terminal calibration "
        f"n={n:.15g} X_eff={x_eff:.15g} Mpc nodes={len(node_rows)} sources={len(sources)}"
    )


if __name__ == "__main__":
    main()
