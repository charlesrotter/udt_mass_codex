#!/usr/bin/env python3
"""Hostile mutation checks for G117."""

from __future__ import annotations

import json
import ast
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
N = 1.0559332414320268


def curve(z: np.ndarray, n: float = N) -> np.ndarray:
    scale = 1.0 + z
    return n * scale**2 * (1.0 - scale ** (-2.0 / n))


def main() -> None:
    z = np.array([0.03, 0.1, 0.5, 1.0, 2.0])
    base = curve(z)
    radius, v_rel, dot_v, optical = 0.01, 0.02, 1.0 / 70.0, 1.0 / 30.0
    zeta = np.log1p(z)
    correction = v_rel * radius + (dot_v - optical / 4.0) * radius**2
    phi_live = zeta - correction
    prereg_text = (HERE / "PREREGISTRATION.md").read_text()
    production_tree = ast.parse((HERE / "run_operational_sne_regrade.py").read_text())
    called_names = {
        node.func.id
        for node in ast.walk(production_tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    imported_modules = {
        alias.name
        for node in ast.walk(production_tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    executable_catches = {
        "universal_phi_equals_zeta_rejected_on_live_witness": bool(np.max(np.abs(phi_live - zeta)) > 1e-6),
        "universal_ceff_equals_Zminus2_rejected_on_live_witness": bool(np.max(np.abs(np.exp(-2.0 * phi_live) - np.exp(-2.0 * zeta))) > 1e-6),
        "moving_n_changes_curve": bool(np.max(np.abs(curve(z, N * 1.01) - base)) > 1e-4),
        "appending_orchestra_correction_changes_curve": bool(np.max(np.abs(base * np.exp(correction) - base)) > 1e-4),
        "using_terminal_phi_in_frequency_transfer_changes_curve": bool(np.max(np.abs(np.exp(2.0 * phi_live) / np.exp(2.0 * zeta) - 1.0)) > 1e-6),
    }
    semantic_guards = {
        "release_redshift_not_udt_distance_guard": "OBSERVED_RELEASE_REDSHIFT_COORDINATES" in prereg_text and "not metric-derived UDT distances" in prereg_text,
        "optimizer_absent_from_production": "scipy.optimize" not in imported_modules and not ({"minimize", "least_squares", "curve_fit"} & called_names),
        "conditional_transfer_guard": "conditional transfer" in prereg_text.lower(),
    }
    passed = all(executable_catches.values()) and all(semantic_guards.values())
    result = {
        "status": "PASS" if passed else "FAIL",
        "executable_catch_count": len(executable_catches),
        "semantic_guard_count": len(semantic_guards),
        "executable_catches": executable_catches,
        "semantic_guards_not_catch_proofs": semantic_guards,
    }
    (HERE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
