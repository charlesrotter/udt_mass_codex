#!/usr/bin/env python3
"""Hostile semantic and numerical catches for the G243 reconstruction."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

import numpy as np
from scipy.linalg import cho_factor, cho_solve


PACKAGE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("g243_production", PACKAGE / "derive_radial_spline_representation.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def one_offset_mutation(state: dict[str, object], basis_count: int, alpha: float) -> float:
    spline, knots = MODULE.spline_system(float(state["phi_min"]), float(state["phi_max"]), basis_count)
    white = MODULE.whiten_design(state, spline)
    # Collapse the two release offsets to one. Shape columns are unchanged.
    design = np.column_stack([white["design"][:, 0] + white["design"][:, 1], white["design"][:, 2:]])
    observed = white["observed"]
    normal = design.T @ design
    rhs = design.T @ observed
    penalty_shape = MODULE.roughness_penalty(spline, knots)
    penalty = np.zeros_like(normal)
    penalty[1:, 1:] = penalty_shape
    scale = float(np.trace(normal[1:, 1:]) / np.trace(penalty_shape))
    factor = cho_factor(normal + alpha * scale * penalty, lower=True, check_finite=True)
    coefficients = cho_solve(factor, rhs, check_finite=True)
    residual = observed - design @ coefficients
    return float(residual @ residual)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    checks: list[str] = []

    def catch(name: str, condition: bool) -> None:
        assert condition, name
        checks.append(name)

    state = MODULE.load_release_state()
    selected_basis = 48
    spline, _knots = MODULE.spline_system(float(state["phi_min"]), float(state["phi_max"]), selected_basis)
    white = MODULE.whiten_design(state, spline)
    production = json.loads((PACKAGE / "DERIVATION_RESULT.json").read_text())
    selected = production["selected"]

    catch("fixed_basis_census", tuple(MODULE.BASIS_COUNTS) == (16, 24, 32, 48, 64))
    catch("fixed_alpha_grid_size", MODULE.LOG10_ALPHA.size == 97)
    catch("fixed_alpha_grid_endpoints", MODULE.LOG10_ALPHA[0] == -12.0 and MODULE.LOG10_ALPHA[-1] == 12.0)
    catch("selected_alpha_interior", selected["alpha_index"] == 44 and selected["alpha_boundary"] is False)
    catch("two_release_offsets_present", white["design"].shape[1] == selected_basis + 1)
    catch("pantheon_second_offset_zero", np.max(np.abs(white["p_design"][:, 1])) == 0.0)
    catch("des_first_offset_zero", np.max(np.abs(white["d_design"][:, 0])) == 0.0)
    catch("release_offsets_numerically_distinct", abs(float(selected["coefficients"][0]) - float(selected["coefficients"][1])) > 1.0)

    one_offset_chi2 = one_offset_mutation(state, selected_basis, float(selected["alpha"]))
    catch("deleting_release_offset_changes_fit", abs(one_offset_chi2 - float(selected["raw_chi2"])) > 10.0)

    diagonal_state = dict(state)
    diagonal_state["p_cov"] = np.diag(np.diag(np.asarray(state["p_cov"])))
    diagonal_state["d_cov"] = np.diag(np.diag(np.asarray(state["d_cov"])))
    diagonal_best = MODULE.evaluate_basis(diagonal_state, selected_basis)["best"]
    catch("full_covariance_is_load_bearing", abs(float(diagonal_best["raw_chi2"]) - float(selected["raw_chi2"])) > 10.0)

    catch("monotonicity_not_imposed", float(selected["minimum_s_prime"]) < 0.0)
    catch("turning_landing_retained", production["classification"].endswith("TURNING_INTERVALS_RETAINED"))
    catch("direct_reciprocal_redshift", production["redshift_role"] == "DIRECT_RECIPROCAL_DEPTH__NO_ANGULAR_INPUT")
    catch("angular_outcomes_closed", production["angular_outcomes"] == "CLOSED_AND_UNUSED")
    catch("boss_outcomes_closed", production["boss_outcomes"] == "CLOSED_AND_UNREAD")
    catch("manifest_exactly_eight_sources", len(MODULE.verify_manifest()) == 8)

    source_text = (PACKAGE / "derive_radial_spline_representation.py").read_text()
    executable_prefix = source_text.split('"maximum_conclusion"', maxsplit=1)[0]
    forbidden_construction_tokens = ("G116", "G189", "P1_", "Lambda-CDM", "BOSS_R5", "protected package")
    catch("forbidden_construction_inputs_absent", not any(token in executable_prefix for token in forbidden_construction_tokens))

    output = {
        "status": "PASS",
        "count": len(checks),
        "catches": checks,
        "one_offset_mutation_raw_chi2": one_offset_chi2,
        "diagonal_covariance_selected_raw_chi2": float(diagonal_best["raw_chi2"]),
    }
    rendered = json.dumps(output, indent=2, sort_keys=True) + "\n"
    path = PACKAGE / "CATCH_PROOF_RESULT.json"
    if args.no_write:
        assert path.read_text() == rendered
    else:
        path.write_text(rendered)
    print(f"PASS: {len(checks)} G243 hostile catches")


if __name__ == "__main__":
    main()
