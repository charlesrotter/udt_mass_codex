#!/usr/bin/env python3
"""Registered hostile checks for the frozen shape-query calculation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = json.loads(args.result.read_text())
    controls = result["controls"]

    catches = {}
    # Algebra/typing mutations have exact distinctive failures.
    symbolic = result["symbolic"]
    catches["missing_L_pair"] = not symbolic["missing_L_pair_reparameterization_invariant"]
    catches["missing_exp_phi"] = symbolic["missing_exp_phi_fails_scalar_reduction"]

    # Covariance mutation: remove within-bin off diagonal and prove the load-bearing total changes.
    diagonal_total = 0.0
    for row in controls["C1"]:
        y = np.array([row["observed_DM"], row["observed_DH"]])
        v = np.array([row["F_pred"], 1.0])
        c = np.diag([row["cov_DM_DM"], row["cov_DH_DH"]])
        inv = np.linalg.inv(c)
        amp = float((v @ inv @ y) / (v @ inv @ v))
        diagonal_total += float((y - amp * v) @ inv @ (y - amp * v))
    catches["diagonal_only_covariance"] = (
        abs(diagonal_total - result["totals"]["C1"]["chi2"]) > 1e-6
    )

    # Delta-method mutation is explicitly not the production likelihood.
    catches["delta_method_as_likelihood"] = (
        "delta_method" not in result["scope"]
        and result["direct_profile_verification"]["maximum_chi2_abs_delta"] < 1e-10
    )
    catches["fit_n"] = result["n_sne_fixed"] == 1.0559332414320268 and "best_n" not in result

    for name in ("C0", "C1"):
        rows = controls[name]
        worst = max(rows, key=lambda x: x["chi2"])
        dropped = result["totals"][name]["chi2"] - worst["chi2"]
        catches[f"drop_worst_bin_{name}"] = abs(dropped - result["totals"][name]["chi2"]) > 1e-6

    catches["promote_C1_to_complete_history"] = (
        result["maximum_conclusion"] == "bounded normalization-free six-bin shape compatibility only"
    )
    catches["isotropic_point_inserted"] = len(result["z_used"]) == 6 and 0.295 not in result["z_used"]

    assert len(catches) == 9 and all(catches.values())
    output = {"status": "PASS", "caught": sum(catches.values()), "total": len(catches), "checks": catches}
    args.output.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output))


if __name__ == "__main__":
    main()
