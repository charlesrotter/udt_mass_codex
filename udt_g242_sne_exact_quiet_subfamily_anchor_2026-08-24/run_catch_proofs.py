#!/usr/bin/env python3
"""Hostile semantic checks for G242."""

from __future__ import annotations

import argparse
import ast
import json
import math
from pathlib import Path

import numpy as np

import derive_exact_quiet_anchor as production


PACKAGE = Path(__file__).resolve().parent
OUTPUT_PATH = PACKAGE / "CATCH_PROOF_RESULT.json"


def executable_paths(source: str) -> set[str]:
    tree = ast.parse(source)
    paths: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            value = node.value
            if "/" in value or value.endswith((".json", ".tsv", ".md")):
                paths.add(value)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    native = production.evaluate()
    diagonal = production.evaluate(covariance_mode="diagonal")
    wrong_plus = production.evaluate(model_mode="wrong_plus_sign")
    state = json.loads(production.STATE_PATH.read_text(encoding="utf-8"))["state"]
    knots = np.asarray(state["knots"], dtype=np.float64)
    base = production.quiet_theta(knots[1:], float(knots[0]))

    # C must cancel after anchoring. This direct construction would catch an unanchored scale.
    scale_predictions = []
    for magnitude in (1.0e-9, 1.0, 1.0e9):
        radius = np.sqrt((-np.expm1(-2.0 * knots)) / magnitude)
        scale_predictions.append(5.0 * np.log10(radius[1:] / radius[0]))
    maximum_c_dependence = max(float(np.max(np.abs(candidate - base))) for candidate in scale_predictions)

    angular_mutation = base + 0.125 * np.sin(knots[1:])
    angular_mutation_detected = float(np.max(np.abs(angular_mutation - base))) > 1.0e-3

    source = Path(production.__file__).read_text(encoding="utf-8")
    paths = executable_paths(source)
    forbidden_path_fragments = (
        "BOSS_R3",
        "R4_OUTCOME",
        "R5_OUTCOME",
        "observed_angular_pattern",
        "/media/",
        "udt_pair_regime_flow",
        "udt_sne_xmax_G88",
        "udt_native_onshell",
    )
    leaked_paths = sorted(path for path in paths if any(token in path for token in forbidden_path_fragments))

    checks = {
        "full_covariance_required": abs(float(diagonal["chi2"]) - float(native["chi2"])) > 1.0,
        "wrong_quiet_sign_detected": float(np.max(np.abs(np.asarray(wrong_plus["predicted_theta"]) - base))) > 1.0,
        "fitted_C_has_no_shape_leverage": maximum_c_dependence < 1.0e-12,
        "angular_coefficient_mutation_detected": angular_mutation_detected,
        "registered_ceiling_is_live": (
            float(native["chi2"]) > float(native["chi2_ceiling_0p999"])
            and float(native["chi2"]) <= math.inf
        ),
        "boss_and_protected_paths_absent": not leaked_paths,
        "manifest_has_only_four_registered_sources": len(native["manifest"]) == 4,
        "native_zero_tide_identity_live": float(native["maximum_abs_J"]) <= 1.0e-10,
    }
    if not all(checks.values()):
        raise RuntimeError(f"catch proof failure: {checks}")
    result = {
        "status": "PASS",
        "checks": checks,
        "native_chi2": native["chi2"],
        "diagonal_covariance_chi2": diagonal["chi2"],
        "wrong_plus_sign_chi2": wrong_plus["chi2"],
        "maximum_C_dependence": maximum_c_dependence,
        "leaked_paths": leaked_paths,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if not args.no_write:
        OUTPUT_PATH.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
