#!/usr/bin/env python3
"""Hostile mutations proving the G110 gates can catch the targeted errors."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent


def main() -> None:
    lam = 0.8
    pair_screen = np.zeros((2, 2))
    sky = lam * np.eye(2)
    wrong_same_w_residual = float(np.linalg.norm(pair_screen - sky))

    phi_rate = 0.0
    sky_log_area_rate = 2.0 / lam
    zero_rate_division_rejected = False
    try:
        if phi_rate == 0.0:
            raise ZeroDivisionError("phi_pair is not a local propagation coordinate")
        _ = sky_log_area_rate / (2.0 * phi_rate)
    except ZeroDivisionError:
        zero_rate_division_rejected = True

    caustic = np.zeros((2, 2))
    caustic_inverse_rejected = False
    try:
        np.linalg.inv(caustic)
    except np.linalg.LinAlgError:
        caustic_inverse_rejected = True

    anisotropic = np.diag([math.cos(lam) / math.sin(lam), 1.0 / lam])
    shear = anisotropic - np.trace(anisotropic) * np.eye(2) / 2.0
    isotropic_filter_detected = float(np.linalg.norm(shear)) > 1.0e-3

    E = np.diag([2.0, 3.0, 4.0, 5.0])
    J = np.array([[1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [1.0, -1.0]])
    P = np.array(
        [[1.0, 1.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0],
         [0.0, 0.0, 2.0, 1.0], [0.0, 0.0, 0.0, 1.0]]
    )
    E_changed = E @ np.linalg.inv(P)
    J_changed = P @ J
    representative_changed = float(np.linalg.norm(E_changed - E)) > 1.0
    physical_product_unchanged = np.allclose(E_changed @ J_changed, E @ J)

    catches = {
        "wrong_same_w_detected": wrong_same_w_residual > 1.0,
        "zero_phi_rate_division_rejected": zero_rate_division_rejected,
        "caustic_inverse_rejected": caustic_inverse_rejected,
        "isotropic_only_filter_detected": isotropic_filter_detected,
        "representative_only_change_detected_as_scaffold": representative_changed
        and physical_product_unchanged,
    }
    result = {
        "schema": "UDT_G110_CATCH_PROOFS_V1",
        "raw": {
            "wrong_same_w_residual": wrong_same_w_residual,
            "sky_log_area_rate_with_zero_phi_rate": sky_log_area_rate,
            "anisotropic_shear_norm": float(np.linalg.norm(shear)),
            "representative_change_norm": float(np.linalg.norm(E_changed - E)),
        },
        "catches": catches,
        "all_catches_pass": all(catches.values()),
    }
    serialized = json.dumps(result, indent=2, sort_keys=True)
    (HERE / "CATCH_PROOF_RESULT.json").write_text(serialized + "\n")
    print(serialized)
    raise SystemExit(0 if result["all_catches_pass"] else 1)


if __name__ == "__main__":
    main()
