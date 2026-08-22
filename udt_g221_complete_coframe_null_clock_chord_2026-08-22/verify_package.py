#!/usr/bin/env python3
"""Fail-closed no-write replay for the provisional G221 evidence package."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path


if not __debug__:
    raise RuntimeError("G221 evidence must run with Python assertions enabled; -O is forbidden")

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent

REQUIRED = (
    "MAP.md",
    "PREREGISTRATION.md",
    "PREMISE_LEDGER.tsv",
    "SOURCE_MANIFEST.tsv",
    "derive_complete_coframe_null_chord.py",
    "verify_complete_coframe_null_chord_independent.py",
    "run_catch_proofs.py",
    "build_review_intake.py",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "CONTROL_ATLAS.tsv",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "EVIDENCE_GATES.md",
    "STATUS_LEDGER.tsv",
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "VERIFICATION_RESULT.json",
)

LANDING = (
    "COMPLETE_COFRAME_NULL_CLOCK_CHORD_DERIVED_CONDITIONALLY"
    "__SCREEN_AND_MIXING_ENTER_UPSTREAM__G220_RECOVERED"
    "__NULL_AND_FULL_PAIR_REMAIN_QUERY_TYPED"
)

EXPECTED_CHECKS = {
    "future_root_null",
    "past_root_null",
    "root_separation",
    "strict_root_sign_margin",
    "complete_coframe_determinant",
    "observer_norm_includes_time_mixing",
    "direct_inverse_metric_null",
    "future_frequency_positive_witness",
    "past_frequency_negative_witness",
    "Hamilton_Jacobi_longitudinal_velocity",
    "Hamilton_Jacobi_screen_velocity_1",
    "Hamilton_Jacobi_screen_velocity_2",
    "screen_covariance_P2",
    "screen_covariance_Pi",
    "screen_covariance_q2",
    "screen_covariance_coordinate_energy",
    "positive_affine_homogeneity",
    "G220_single_endpoint_recovery",
    "G220_endpoint_ratio_recovery",
    "same_correspondence_clock_leg",
    "completed_depth_compatibility",
}

EXPECTED_FORMULAS = {
    "future_coframe_root": "(-N*beta*Pi-A*sqrt(Pi^2+D*q2))/D",
    "coordinate_energy": "s_t^T*p_z-N*(A*R+N*beta*Pi)/D",
    "observer_lapse_squared": "N^2-s_t^T*H*s_t",
    "measured_frequency": "-p_t/P",
    "clock_slope": "W_A/W_B",
    "incidence_velocity": "d_xi^i/dt=-partial(p_t^-)/partial(p_i)",
    "completed_clock_leg": "T_B=r_AB",
    "G220_reduction": "W=p_x/(A-N*beta)",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    require(spec is not None and spec.loader is not None, f"cannot load {filename}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def snapshot() -> dict[str, str]:
    return {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest() for name in REQUIRED}


def production_contract(payload: dict[str, object]) -> bool:
    return (
        payload.get("manifest_files") == 12
        and payload.get("check_count") == 21
        and set(payload.get("checks", {})) == EXPECTED_CHECKS
        and all(payload.get("checks", {}).values())
        and payload.get("formulas") == EXPECTED_FORMULAS
        and payload.get("landing") == LANDING
    )


def main() -> None:
    for name in REQUIRED:
        require((HERE / name).is_file(), f"missing evidence: {name}")
    before = snapshot()

    production = load("g221_production", "derive_complete_coframe_null_chord.py").derive()
    independent = load("g221_independent", "verify_complete_coframe_null_chord_independent.py").verify()
    catches = load("g221_catches", "run_catch_proofs.py").catches()

    registered = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    registered_independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
    )
    registered_catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    verification = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))

    require(production_contract(production), "production payload contract failed")
    mutant = copy.deepcopy(production)
    mutant["formulas"]["clock_slope"] = "W_B/W_A"
    require(not production_contract(mutant), "payload contract mutation escaped")

    require(registered == {
        "status": "PASS",
        "landing": LANDING,
        "manifest_files": 12,
        "symbolic_checks": 21,
        "all_checks_pass": True,
        "future_branch_unique_on_declared_stratum": True,
        "screen_and_mixing_upstream": True,
        "G220_recovered": True,
        "completed_clock_leg_compatibility_only": True,
        "null_protocol_universally_selected": False,
        "full_pair_plane_constructed": False,
        "screen_Jacobi_collapsed_into_scalar": False,
    }, "registered derivation contract changed")
    require(production["landing"] == registered["landing"], "landing mismatch")

    expected_independent = {
        "cases": 12000,
        "full_sector_cases": 10000,
        "screen_covariance_cases": 10000,
        "future_past_branch_cases": 10000,
        "G220_reduction_pairs": 2000,
        "exact_checks": 154000,
    }
    require(independent == expected_independent, "independent live replay changed")
    require(registered_independent == {
        "status": "PASS",
        **expected_independent,
        "implementation": "independent_standard_library_fraction_and_quadratic_surd_replay",
    }, "registered independent evidence changed")
    require(catches["canonical_pass"] is True, "canonical catch payload failed")
    require(catches["injected_mutation_catches"] == 18, "live catch count changed")
    require(all(catches["catches"].values()), "injected mutation escaped")
    require(registered_catches == {
        "status": "PASS",
        "canonical_pass": True,
        "injected_mutation_catches": 18,
        "all_mutants_rejected": True,
        "algebraic_mutants": 12,
        "semantic_and_boundary_mutants": 6,
    }, "registered catch evidence changed")

    require(verification == {
        "status": "PASS",
        "landing": LANDING,
        "source_count": 12,
        "symbolic_checks": 21,
        "independent_cases": 12000,
        "independent_exact_checks": 154000,
        "full_sector_cases": 10000,
        "screen_covariance_cases": 10000,
        "future_past_branch_cases": 10000,
        "G220_reduction_pairs": 2000,
        "injected_mutation_catches": 18,
        "payload_contract_mutation_guard": True,
        "optimized_mode_rejected": True,
        "no_write_replay": True,
        "fresh_adversarial_review": "PENDING",
        "completed_clock_leg_compatibility_only": True,
        "physical_protocol_selected": False,
        "full_pair_plane_constructed": False,
        "screen_Jacobi_collapsed": False,
    }, "verification summary changed")

    after = snapshot()
    require(before == after, "package replay wrote to evidence files")
    print(
        "PASS: G221 provisional package; 12 sources; 21 symbolic; "
        "154,000 independent exact; 18 injected catches; payload guard; "
        "optimized-mode rejection; no-write; fresh review pending"
    )


if __name__ == "__main__":
    main()
