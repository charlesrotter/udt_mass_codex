#!/usr/bin/env python3
"""Fail-closed no-write replay for the provisional G222 evidence package."""

from __future__ import annotations

import copy
import csv
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
    "FRESH_ADVERSARIAL_REVIEW.md",
    "REPAIR_PREREGISTRATION.md",
    "REPAIR_FOLLOWUP_REVIEW_REQUEST.md",
    "REPAIR_FOLLOWUP_REVIEW.md",
    "REPAIR_IMPLEMENTATION.md",
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


def source_paths() -> tuple[Path, ...]:
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    return tuple((HERE.parent / row["path"]).resolve() for row in rows)


def tree_snapshot() -> dict[str, str]:
    """Hash the complete package tree plus every frozen load-bearing source."""
    state: dict[str, str] = {}
    for path in sorted(HERE.rglob("*")):
        relative = path.relative_to(HERE).as_posix()
        if path.is_symlink():
            state[f"package:{relative}"] = f"symlink:{path.readlink()}"
        elif path.is_dir():
            state[f"package:{relative}"] = "directory"
        elif path.is_file():
            state[f"package:{relative}"] = "file:" + hashlib.sha256(path.read_bytes()).hexdigest()
        else:
            state[f"package:{relative}"] = "special"
    for path in source_paths():
        require(path.is_file(), f"missing frozen source during snapshot: {path}")
        relative = path.relative_to(HERE.parent).as_posix()
        state[f"frozen_source:{relative}"] = "file:" + hashlib.sha256(path.read_bytes()).hexdigest()
    return state


def production_contract(payload: dict[str, object]) -> bool:
    return bool(
        payload.get("status") == "PASS"
        and payload.get("landing") == LANDING
        and payload.get("source_count") == 10
        and payload.get("check_count") == 43
        and len(payload.get("checks", {})) == 43
        and all(payload.get("checks", {}).values())
        and payload.get("formulas", {}).get("pair_determinant") == "-a^2"
        and payload.get("formulas", {}).get("completed_ruler_density") == "m=a"
        and payload.get("formulas", {}).get("target_depth") == "Phi_AB=-log(r_AB)"
    )


def main() -> None:
    for name in REQUIRED:
        require((HERE / name).is_file(), f"missing evidence: {name}")
    before = tree_snapshot()
    synthetic_addition = dict(before)
    synthetic_addition["package:__synthetic_added_file__"] = "file:synthetic"
    require(before != synthetic_addition, "tree mutation guard failed to detect addition")
    synthetic_modification = dict(before)
    first_key = next(iter(synthetic_modification))
    synthetic_modification[first_key] = synthetic_modification[first_key] + ":modified"
    require(before != synthetic_modification, "tree mutation guard failed to detect modification")
    synthetic_deletion = dict(before)
    synthetic_deletion.pop(first_key)
    require(before != synthetic_deletion, "tree mutation guard failed to detect deletion")

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
        "symbolic_checks": 43,
        "full_pair_plane_constructed_conditionally": True,
        "completed_ruler_density": "a=-g(J,K)",
        "G221_boundary_chord_recovered": True,
        "G188_screen_joined_as_normal_channel": True,
        "G188_connection_tidal_intertwining_explicit": True,
        "global_ruler_coordinate_unconditional": False,
        "physical_protocol_selected": False,
        "physical_history_selected": False,
    }, "registered derivation result changed")

    expected_independent = {
        "classification": "independent_finite_algebra_replay_not_general_geometric_proof",
        "cases": 12000,
        "finite_algebra_assertions": 396000,
        "screen_isometry_cases": 12000,
        "connection_intertwining_cases": 12000,
        "tidal_intertwining_cases": 12000,
        "flat_ribbon_cases": 12000,
    }
    require(independent == expected_independent, "independent live replay changed")
    require(registered_independent == {
        "status": "PASS",
        "implementation": "independent_standard_library_fraction_finite_algebra_replay",
        **expected_independent,
    }, "registered independent result changed")
    require(catches["canonical_pass"] is True, "canonical catch payload failed")
    require(catches["payload_contract_mutations"] == 18, "live contract mutation count changed")
    require(all(catches["catches"].values()), "injected mutation escaped")
    require(registered_catches == {
        "status": "PASS",
        "canonical_pass": True,
        "payload_contract_mutations": 18,
        "all_contract_mutants_rejected": True,
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
        "symbolic_checks": 43,
        "independent_cases": 12000,
        "finite_algebra_assertions": 396000,
        "screen_isometry_cases": 12000,
        "connection_intertwining_cases": 12000,
        "tidal_intertwining_cases": 12000,
        "flat_ribbon_cases": 12000,
        "payload_contract_mutations": 18,
        "payload_contract_mutation_guard": True,
        "tree_mutation_guard": True,
        "optimized_mode_rejected": True,
        "no_write_scope": "complete_package_tree_plus_10_frozen_sources",
        "no_write_replay": True,
        "fresh_adversarial_review": "ACCEPT_WITH_REPAIRS",
        "repair_followup_review": "REPAIRS_ACCEPTED",
        "full_pair_plane_constructed_conditionally": True,
        "global_ruler_coordinate_unconditional": False,
        "screen_Jacobi_collapsed": False,
        "physical_protocol_selected": False,
        "physical_history_selected": False,
    }, "verification summary changed")

    after = tree_snapshot()
    require(before == after, "package replay changed the complete in-scope tree")
    print(
        "PASS: G222 repaired package; 10 sources; 43 symbolic/direct; 396,000 finite-algebra "
        "assertions; 18 payload-contract mutations; complete-tree no-write; repairs accepted"
    )


if __name__ == "__main__":
    main()
