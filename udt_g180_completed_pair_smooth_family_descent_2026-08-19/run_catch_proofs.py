#!/usr/bin/env python3
"""Semantic and algebraic mutation catches for G180."""

from __future__ import annotations

import ast
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def main() -> None:
    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text())
    exact_text = (HERE / "EXACT_DERIVATION.md").read_text()
    prereg_text = (HERE / "PREREGISTRATION.md").read_text()

    trees = [
        ast.parse((HERE / "derive_completed_pair_family.py").read_text()),
        ast.parse((HERE / "verify_family_descent_independent.py").read_text()),
    ]
    names = {
        node.id
        for tree in trees
        for node in ast.walk(tree)
        if isinstance(node, ast.Name)
    }

    primary = derivation["primary_full_witness"]
    h = sp.diag(sp.Rational(-1, 4), sp.Rational(89, 4))
    arbitrary_phi = sp.log((-h.det()) / h[0, 0] ** 2) / 4
    completed_phi = -sp.log(-h[0, 0]) / 2

    forbidden_executable = {
        "X_max",
        "score",
        "torsor",
        "carry_rule",
        "fit_parameter",
        "luminosity",
        "source_term",
        "bootstrap",
        "action_density",
    }
    checks = derivation["checks"]
    catches = {
        "production_and_independent_pass": derivation["status"] == "PASS"
        and independent["status"] == "PASS",
        "registered_landing_retained": derivation["landing"]
        == "COMPLETED_PAIR_SMOOTH_FAMILY_DESCENT__ORCHESTRA_ENTERS_THE_PHYSICAL_TAPE_MAP",
        "independent_target_reached": independent["exact_fraction_regular_trials"] >= 20_000,
        "independent_assertion_floor": independent["exact_assertions"] >= 300_000,
        "turning_population_present": independent["turning_trials"] > 0,
        "pure_angular_population_present": independent["pure_angular_trials"] > 0,
        "radial_population_present": independent["radial_trials"] > 0,
        "generic_density_and_determinant": checks["generic_density"]
        and checks["generic_calibrated_determinant"],
        "generic_shift_retained": checks["generic_shift_retained"]
        and checks["generic_shift_witness"],
        "reparameterization_covariant": checks["positive_reparameterization_density"]
        and checks["positive_reparameterization_invariant"],
        "common_scale_not_canceled": checks["common_scale_density_retained"]
        and checks["common_scale_changes_completed_depth"],
        "primary_orchestra_changes_tape": checks["angular_channel_changes_tape"]
        and primary["m_squared"] == "89/16",
        "primary_orchestra_not_bolted_onto_depth": checks[
            "angular_channel_not_direct_depth"
        ],
        "arbitrary_control_not_completed_depth": sp.simplify(
            arbitrary_phi - completed_phi
        ) != 0,
        "primary_calibrated_metric_reciprocal": checks["primary_calibrated_metric"]
        and checks["primary_calibrated_determinant"],
        "radial_recovery": checks["radial_recovery"],
        "turning_regular": checks["turning_witness_positive"]
        and checks["turning_witness_calibrated"],
        "center_control_bounded": checks["center_monotone_limit"],
        "time_live_is_chain_rule_only": checks["depth_derivative_identity"]
        and checks["primary_density_derivative_exact"]
        and "not an equation of motion" in exact_text,
        "same_family_only_guard": "No closure is imposed between independently supplied pair"
        in exact_text,
        "zero_tangent_excluded": "zero-tangent case" in exact_text,
        "physical_family_selection_open": "physical_event_germ_and_family_realization"
        in derivation["open"],
        "global_completion_open": "cross_family_matching_and_global_completion"
        in derivation["open"],
        "non_scalar_transport_open": "non_scalar_transport" in derivation["open"],
        "no_forbidden_executable_dependency": not (forbidden_executable & names),
        "scaffold_exclusion_preregistered": "G142--G160" in prereg_text,
        "Xmax_exclusion_preregistered": "`X_max`" in prereg_text,
        "observation_exclusion_preregistered": "observations" in prereg_text,
    }
    failed = [name for name, passed in catches.items() if not passed]
    result = {
        "audit": "G180",
        "status": "PASS" if not failed and len(catches) >= 20 else "FAIL",
        "catch_count": len(catches),
        "failed": failed,
        "catches": catches,
    }
    (HERE / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    if result["status"] != "PASS":
        raise SystemExit(f"FAIL: {failed}")
    print(f"PASS: {len(catches)} semantic and algebraic mutation catches")


if __name__ == "__main__":
    main()
