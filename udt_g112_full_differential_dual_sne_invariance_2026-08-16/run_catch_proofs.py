#!/usr/bin/env python3
"""Executable hostile mutations for the G112 frozen dual-SNe replay."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
N = 1.0559332414320268


def caught(condition: bool, label: str, checks: dict[str, bool]) -> None:
    checks[label] = bool(condition)
    if not condition:
        raise AssertionError(label)


def shape(z: np.ndarray, n: float) -> np.ndarray:
    scale = 1.0 + z
    return 5.0 * np.log10(n * scale**2 * (1.0 - scale ** (-2.0 / n)))


def main() -> None:
    result = json.loads((HERE / "PRODUCTION_RESULT.json").read_text())
    checks: dict[str, bool] = {}
    z = np.array([0.03, 0.1, 0.5, 1.0, 2.0])
    phi = np.log1p(z)
    screen_radius = N * (-np.expm1(-2.0 * phi / N))
    dsky = screen_radius[:, None, None] * np.eye(2)[None, :, :]
    caught(phi.shape != dsky.shape and dsky.shape == (5, 2, 2), "reject_pair_sky_identification", checks)
    caught(np.max(np.abs(shape(z, N * 1.01) - shape(z, N))) > 1.0e-6, "reject_moving_frozen_n", checks)
    altered_screen = screen_radius * (1.0 + 0.01 * np.sin(phi))
    altered = (5.0 / np.log(10.0)) * np.log(np.exp(2.0 * phi) * altered_screen)
    caught(np.max(np.abs(altered - shape(z, N))) > 1.0e-6, "reject_appended_orchestra_correction", checks)
    caught(result["des"]["hostile_precision_subblock_abs_difference"] > 1.0, "reject_precision_subblock", checks)
    production_source = (HERE / "run_dual_sne.py").read_text()
    forbidden_fields = ("MUMODEL", "MURES", "MUPULL")
    caught(not any(field in production_source for field in forbidden_fields), "reject_forbidden_cosmology_fields", checks)
    caught("minimize" not in production_source and not result["shape_optimizer_called"], "reject_shape_optimizer", checks)
    ledger = (HERE / "PREMISE_LEDGER.tsv").read_text()
    caught("CONDITIONAL_REPRESENTATIVE" in ledger and "physical complete SNe realization" in ledger,
           "reject_complete_history_promotion", checks)
    caught("CONDITIONAL" in result["typed_interface"]["transfer"], "reject_native_flux_promotion", checks)
    output = {"schema": "UDT_G112_CATCH_PROOFS_V1", "checks": checks,
              "all_checks_pass": all(checks.values())}
    (HERE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
