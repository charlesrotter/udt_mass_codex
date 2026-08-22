#!/usr/bin/env python3
"""Fail-closed no-write replay for the provisional G220 evidence package."""

from __future__ import annotations

import csv
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import sympy as sp


if not __debug__:
    raise RuntimeError("G220 evidence must run with Python assertions enabled; -O is forbidden")

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REQUIRED = (
    "MAP.md",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "REPAIR_PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "derive_covariant_null_clock_arrow.py",
    "verify_null_clock_arrow_independent.py",
    "run_catch_proofs.py",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "CONTROL_ATLAS.tsv",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "EVIDENCE_GATES.md",
    "STATUS_LEDGER.tsv",
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "FRESH_ADVERSARIAL_REVIEW.md",
    "REPAIR_FOLLOWUP_REVIEW.md",
    "VERIFICATION_RESULT.json",
)


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def snapshot() -> dict[str, str]:
    return {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest() for name in REQUIRED}


def canonical_symbolic_contract() -> None:
    n, a, beta = sp.symbols("N A beta", positive=True, real=True)
    cp, cm = a - n * beta, a + n * beta
    metric = sp.Matrix([[-n**2, -n**2 * beta], [-n**2 * beta, a**2 - n**2 * beta**2]])
    right = sp.Matrix([1, n / cp])
    left = sp.Matrix([1, -n / cm])
    assert sp.factor(metric.det()) == -n**2 * a**2
    assert sp.factor((right.T * metric * right)[0]) == 0
    assert sp.factor((left.T * metric * left)[0]) == 0

    n_a, n_b, cp_a, cp_b = sp.symbols("N_A N_B Cp_A Cp_B", positive=True)
    dt_b_dt_a = n_a * cp_b / (cp_a * n_b)
    assert sp.simplify(-n_a / cp_a + n_b * dt_b_dt_a / cp_b) == 0
    r = sp.simplify(n_b * dt_b_dt_a / n_a)
    assert sp.simplify(r - cp_b / cp_a) == 0
    target_norm = sp.simplify(-n_b**2 * (dt_b_dt_a / n_a) ** 2)
    assert sp.simplify(target_norm + r**2) == 0


EXPECTED_CHECKS = {
    "implicit_null_incidence",
    "world_function_to_affine_tangent",
    "affine_frequency_ratio",
    "affine_rescaling_cancels",
    "pair_metric_determinant",
    "right_tangent_is_null",
    "left_tangent_is_null",
    "incidence_integral_first_jet",
    "proper_clock_slope",
    "lapse_cancels_after_proper_clock",
    "source_clock_is_unit",
    "target_pullback_norm",
    "completed_clock_equals_incidence_slope",
    "completed_depth_matches",
    "completed_reciprocal_product",
    "completed_q",
    "completed_chi",
    "G219_moving_flat_recovery",
    "primary_static_ratio",
    "primary_static_depth",
    "conformal_timelive_ratio",
    "affine_witness_Cplus",
    "affine_witness_endpoint_ratio",
    "affine_witness_map_slope",
    "affine_witness_incidence",
    "affine_witness_static_limit",
    "return_chord_is_Cminus",
    "return_not_symbolic_inverse",
}

EXPECTED_FORMULAS = {
    "covariant_clock_slope": "-(sigma_a*U_A^a)/(sigma_a_prime*U_B^a_prime)",
    "affine_frequency_slope": "(k_A.U_A)/(k_B.U_B)=omega_A/omega_B",
    "timelive_Cplus": "A-N*beta",
    "timelive_incidence": "L=integral(N/Cplus, t_A, t_B)",
    "timelive_clock_slope": "Cplus_B/Cplus_A",
    "completed_target_clock": "T_B=r_AB",
    "completed_depth": "-log(r_AB)",
    "future_return_chord": "Cminus=A+N*beta",
}


def production_payload_valid(production: dict[str, object]) -> bool:
    return (
        set(production["checks"]) == EXPECTED_CHECKS
        and production["formulas"] == EXPECTED_FORMULAS
        and production["landing"]
        == "COVARIANT_NULL_CLOCK_ARROW_DERIVED__COMPLETED_CLOCK_LEG_COMPATIBLE__NULL_REMAINS_QUERY_TYPED"
    )


def main() -> None:
    for name in REQUIRED:
        assert (HERE / name).is_file(), name
    before = snapshot()
    canonical_symbolic_contract()

    production = load("g220_production", "derive_covariant_null_clock_arrow.py").derive()
    independent = load("g220_independent", "verify_null_clock_arrow_independent.py").verify()
    caught = load("g220_catches", "run_catch_proofs.py").catches()
    registered = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    registered_independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
    )
    registered_catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    verification = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))

    assert production["manifest_files"] == registered["manifest_files"] == 11
    assert production["check_count"] == registered["symbolic_checks"] == 28
    assert all(production["checks"].values()) and registered["all_checks_pass"]
    assert production_payload_valid(production)
    assert production["landing"] == registered["landing"]
    assert registered["completed_clock_leg_compatible"]
    assert registered["genuinely_timelive_control"]
    assert not registered["null_protocol_universally_selected"]
    assert not registered["full_dynamic_orchestra_derived"]
    assert verification == {
        "status": "PASS",
        "landing": registered["landing"],
        "source_count": 11,
        "symbolic_checks": 28,
        "independent_cases": 11171,
        "independent_exact_checks": 111343,
        "direct_world_function_coordinate_cases": 5000,
        "affine_positive_d_cases": 500,
        "affine_negative_d_cases": 500,
        "injected_mutation_catches": 15,
        "payload_contract_mutation_guard": True,
        "optimized_mode_rejected": True,
        "no_write_replay": True,
        "fresh_adversarial_review": "ACCEPT_AFTER_PREREGISTERED_REPAIRS",
        "completed_clock_leg_compatibility_only": True,
        "physical_protocol_selected": False,
        "full_dynamic_orchestra_derived": False,
    }

    assert independent == {
        "exact_checks": registered_independent["exact_checks"],
        "endpoint_cases": registered_independent["endpoint_cases"],
        "world_function_coordinate_cases": registered_independent["world_function_coordinate_cases"],
        "affine_witness_cases": registered_independent["affine_witness_cases"],
        "moving_flat_cases": registered_independent["moving_flat_cases"],
        "return_diff_cases": registered_independent["return_diff_cases"],
        "affine_positive_d_cases": registered_independent["affine_positive_d_cases"],
        "affine_negative_d_cases": registered_independent["affine_negative_d_cases"],
        "implementation": registered_independent["implementation"],
        "all_checks_pass": registered_independent["all_checks_pass"],
    }
    assert registered_independent["cases"] == 11171
    assert registered_independent["exact_checks"] == 111343

    assert len(caught) == registered_catches["count"] == 15
    assert all(caught.values()) and registered_catches["all_caught"]
    assert set(caught) == set(registered_catches["mutations"])

    with (HERE / "CONTROL_ATLAS.tsv").open(newline="", encoding="utf-8") as handle:
        controls = {row["control"]: row for row in csv.DictReader(handle, delimiter="\t")}
    assert set(controls) == {
        "covariant_null_branch",
        "timelive_triangular_right",
        "completed_clock_leg",
        "moving_flat",
        "primary_static",
        "conformal_timelive",
        "affine_ruler_shift",
        "later_left_return",
    }
    assert controls["timelive_triangular_right"]["clock_slope_r"] == "Cplus_B/Cplus_A"
    assert controls["completed_clock_leg"]["clock_slope_r"] == "T_B=r"
    assert controls["primary_static"]["clock_slope_r"] == "exp(phi_A-phi_B)"
    assert controls["later_left_return"]["status"] == "DERIVED_CONDITIONAL"

    mutated_production = copy.deepcopy(production)
    mutated_production["formulas"]["timelive_clock_slope"] = "Cplus_A/Cplus_B"
    assert not production_payload_valid(mutated_production), "production formula mutation escaped"

    map_text = (HERE / "MAP.md").read_text(encoding="utf-8")
    report_text = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    status_text = (HERE / "STATUS_LEDGER.tsv").read_text(encoding="utf-8")
    assert "Null remains a declared causal query" in map_text
    assert "FRESHLY_ADVERSARIALLY_VERIFIED_AFTER_REPAIRS_WITH_CAVEATS" in report_text
    assert "protocol_ownership\tOPEN" in status_text
    assert snapshot() == before, "registered package mutated during replay"
    print(
        "PASS: G220 accepted package; 11 sources; 28 symbolic; 111,343 independent; "
        "15 injected catches; payload-contract mutation guard; optimized-mode rejection; no-write"
    )


if __name__ == "__main__":
    main()
