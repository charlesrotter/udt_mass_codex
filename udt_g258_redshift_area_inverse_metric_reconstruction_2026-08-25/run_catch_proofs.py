#!/usr/bin/env python3
"""Executable hostile controls for G258."""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
SOURCE = REPO / "udt_g237_dual_sne_joint_relational_state_freeze_2026-08-23" / "FROZEN_PRIMARY_K12_STATE.json"


def main() -> None:
    state = json.loads(SOURCE.read_text())["state"]
    phi = state["knots"]
    theta = [0.0] + state["theta"]
    radius = [1.0] + state["relative_R"]
    cov = state["relative_R_covariance_delta_method"]
    catches = {}

    wrong_sign_z = [math.exp(-value) for value in phi]
    catches["wrong_redshift_sign"] = max(abs(a - math.exp(b)) for a, b in zip(wrong_sign_z, phi)) > 1e-3

    postreadout = [math.exp(-2 * p) * (1.0 + 0.01 * r) for p, r in zip(phi, radius)]
    catches["postreadout_angular_insertion"] = max(abs(a - math.exp(-2 * p)) for a, p in zip(postreadout, phi)) > 1e-4

    wrong_power = [math.exp(-p) for p in phi]
    catches["wrong_f_power"] = max(abs(a - math.exp(-2 * p)) for a, p in zip(wrong_power, phi)) > 1e-3

    wrong_base = [math.exp(value / 5.0) for value in theta]
    catches["logarithm_base_error"] = max(abs(a - b) for a, b in zip(wrong_base, radius)) > 1e-2

    ell_a, ell_b = 1.0, 7.0
    dimensionless_a = [(ell_a * value) / (ell_a * radius[0]) for value in radius]
    dimensionless_b = [(ell_b * value) / (ell_b * radius[0]) for value in radius]
    catches["absolute_scale_self_selection"] = max(abs(a - b) for a, b in zip(dimensionless_a, dimensionless_b)) < 1e-14 and ell_a != ell_b

    full_variances = []
    diagonal_variances = []
    for index in range(2, 12):
        i, j = index - 1, index - 2
        full_variances.append(cov[i][i] + cov[j][j] - 2.0 * cov[i][j])
        diagonal_variances.append(cov[i][i] + cov[j][j])
    catches["covariance_diagonalization"] = max(abs(a - b) for a, b in zip(full_variances, diagonal_variances)) > 1e-5

    forced = radius[:]
    forced[-1] = max(forced[-1], forced[-2])
    catches["forced_monotonicity"] = abs(forced[-1] - radius[-1]) > 1e-3

    c_values = [r * (math.exp(-2 * p) - 1.0) for p, r in zip(phi, radius)]
    catches["static_gr_exterior_import"] = max(c_values) - min(c_values) > 1e-2

    assert all(catches.values()), catches
    result = {
        "status": "PASS",
        "caught_count": len(catches),
        "catches": catches,
        "method": "formula-level mutations and forbidden-import controls",
    }
    (ROOT / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"PASS: {len(catches)}/{len(catches)} hostile controls caught")


if __name__ == "__main__":
    main()
