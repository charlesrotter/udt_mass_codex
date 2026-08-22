#!/usr/bin/env python3
"""Fail-closed no-write replay for the provisional G222 evidence package."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path


if not __debug__:
    raise RuntimeError("G222 evidence requires Python assertions; optimized mode is forbidden")

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
LANDING = (
    "SUPPLIED_NULL_FAMILY_OWNS_FULL_RANK_TWO_PAIR_PLANE_CONDITIONALLY"
    "__CONSERVED_NULL_AREA_DENSITY_COMPLETES_RECIPROCAL_RULER"
    "__G188_SCREEN_IS_CANONICAL_NORMAL_CHANNEL"
    "__GLOBAL_RULER_COORDINATE_AND_PHYSICAL_PROTOCOL_REMAIN_OPEN"
)
REQUIRED = (
    "MAP.md",
    "OBSERVATION.md",
    "PONDER.md",
    "PREREGISTRATION.md",
    "PREMISE_LEDGER.tsv",
    "SOURCE_MANIFEST.tsv",
    "derive_null_pair_plane_screen_join.py",
    "verify_null_pair_plane_independent.py",
    "run_catch_proofs.py",
    "build_review_intake.py",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "EXACT_DERIVATION.md",
    "CONTROL_ATLAS.tsv",
    "STATUS_LEDGER.tsv",
    "AUDIT_REPORT.md",
    "EVIDENCE_GATES.md",
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "VERIFICATION_RESULT.json",
)


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
    return bool(
        payload.get("status") == "PASS"
        and payload.get("landing") == LANDING
        and payload.get("source_count") == 10
        and payload.get("check_count") == 38
        and len(payload.get("checks", {})) == 38
        and all(payload.get("checks", {}).values())
        and payload.get("formulas", {}).get("pair_determinant") == "-a^2"
        and payload.get("formulas", {}).get("completed_ruler_density") == "m=a"
        and payload.get("formulas", {}).get("target_depth") == "Phi_AB=-log(r_AB)"
    )


def main() -> None:
    for name in REQUIRED:
        require((HERE / name).is_file(), f"missing evidence: {name}")
    before = snapshot()

    production = load("g222_production", "derive_null_pair_plane_screen_join.py").derive()
    independent = load("g222_independent", "verify_null_pair_plane_independent.py").verify()
    catches = load("g222_catches", "run_catch_proofs.py").catches()

    registered = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    registered_independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
    )
    registered_catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    verification = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))

    require(production_contract(production), "production payload contract failed")
    mutant = copy.deepcopy(production)
    mutant["formulas"]["completed_ruler_density"] = "m=T"
    require(not production_contract(mutant), "production payload mutation escaped")

    require(registered == {
        "status": "PASS",
        "landing": LANDING,
        "source_count": 10,
        "symbolic_checks": 38,
        "full_pair_plane_constructed_conditionally": True,
        "completed_ruler_density": "a=-g(J,K)",
        "G221_boundary_chord_recovered": True,
        "G188_screen_joined_as_normal_channel": True,
        "global_ruler_coordinate_unconditional": False,
        "physical_protocol_selected": False,
        "physical_history_selected": False,
    }, "registered derivation result changed")

    expected_independent = {
        "cases": 12000,
        "exact_checks": 276000,
        "screen_isometry_cases": 12000,
        "affine_reparameterization_cases": 12000,
        "integrability_boundary_cases": 12000,
    }
    require(independent == expected_independent, "independent live replay changed")
    require(registered_independent == {
        "status": "PASS",
        "implementation": "independent_standard_library_fraction_replay",
        **expected_independent,
    }, "registered independent result changed")
    require(catches["canonical_pass"] is True, "canonical catch payload failed")
    require(catches["injected_mutation_catches"] == 18, "live catch count changed")
    require(all(catches["catches"].values()), "injected mutation escaped")
    require(registered_catches == {
        "status": "PASS",
        "canonical_pass": True,
        "injected_mutation_catches": 18,
        "all_mutants_rejected": True,
    }, "registered catch result changed")

    optimized = subprocess.run(
        [sys.executable, "-O", str(HERE / "derive_null_pair_plane_screen_join.py")],
        cwd=HERE,
        text=True,
        capture_output=True,
        check=False,
    )
    require(optimized.returncode != 0, "optimized mode was not rejected")
    require("optimized mode is forbidden" in optimized.stderr, "optimized rejection message changed")

    require(verification == {
        "status": "PASS",
        "landing": LANDING,
        "source_count": 10,
        "symbolic_checks": 38,
        "independent_cases": 12000,
        "independent_exact_checks": 276000,
        "screen_isometry_cases": 12000,
        "affine_reparameterization_cases": 12000,
        "integrability_boundary_cases": 12000,
        "injected_mutation_catches": 18,
        "payload_contract_mutation_guard": True,
        "optimized_mode_rejected": True,
        "no_write_replay": True,
        "fresh_adversarial_review": "PENDING",
        "full_pair_plane_constructed_conditionally": True,
        "global_ruler_coordinate_unconditional": False,
        "screen_Jacobi_collapsed": False,
        "physical_protocol_selected": False,
        "physical_history_selected": False,
    }, "verification summary changed")

    after = snapshot()
    require(before == after, "package replay wrote to evidence files")
    print(
        "PASS: G222 provisional package; 10 sources; 38 symbolic; 276,000 independent exact; "
        "18 injected catches; payload guard; optimized-mode rejection; no-write; fresh review pending"
    )


if __name__ == "__main__":
    main()
