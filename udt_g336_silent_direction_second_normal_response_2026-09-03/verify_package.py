#!/usr/bin/env python3
"""Aggregate dependency-free verifier for the repaired G336 package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent
PREREG_COMMIT = "eba7a42a"
LANDING = (
    "G336_INHERITED_SILENT_SECOND_JET_IS_EXACT_BUT_SIGN_INDEFINITE"
    "__INTERIOR_CLASSIFICATION_DEPENDS_ON_DIRECTION_CARRY"
    "__STRICT_HORIZONTAL_ENDPOINT_IS_POSITIVE_AND_CARRY_INDEPENDENT"
    "__VERTICAL_ENDPOINT_IS_BRANCH_MEETING_BOUNDARY"
    "__DOUBLE_SILENT_STRATUM_REQUIRES_HIGHER_JET"
)


def digest_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def run(script: str, output: Path) -> tuple[dict, str]:
    result = subprocess.run(
        ["python3", "-B", "-S", str(PACKAGE / script), "--output", str(output)],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise AssertionError(f"{script} failed: {result.stderr or result.stdout}")
    return json.loads(output.read_text(encoding="utf-8")), result.stdout.strip()


def frozen_source(relative: Path, expected_bytes: int, expected_digest: str) -> bytes:
    source_root = REPO / "sources" if (REPO / "sources").is_dir() else REPO
    candidate = (source_root / relative).resolve()
    if not candidate.is_relative_to(source_root.resolve()):
        raise AssertionError(f"source escaped root: {relative}")
    payload = candidate.read_bytes() if candidate.is_file() else b""
    if len(payload) == expected_bytes and digest_bytes(payload) == expected_digest:
        return payload
    replay = subprocess.run(
        ["git", "show", f"{PREREG_COMMIT}:{relative.as_posix()}"],
        cwd=REPO,
        capture_output=True,
        check=False,
    )
    if replay.returncode:
        raise AssertionError(f"frozen source unavailable: {relative}")
    return replay.stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    checks: list[str] = []

    def require(condition: bool, label: str) -> None:
        if not condition:
            raise AssertionError(label)
        checks.append(label)

    with tempfile.TemporaryDirectory(prefix="g336_package_") as temporary:
        temp = Path(temporary)
        production, production_stdout = run(
            "derive_silent_second_response.py", temp / "production.json"
        )
        independent, independent_stdout = run(
            "verify_silent_second_response_independent.py", temp / "independent.json"
        )
        catches, catches_stdout = run("run_catch_proofs.py", temp / "catches.json")

        require(production["landing"] == LANDING, "landing_exact")
        require(production["grade"] ==
                "DERIVED_CONDITIONAL_BOUNDED"
                "__EXTERNALLY_ACCEPTED_AFTER_PREREGISTERED_REPAIRS", "grade_accepted_exact")
        require(production["classifications"] == [
            "INHERITED_LIE_CARRY_SECOND_JET_EXACT",
            "SILENT_SET_SPLITS_POSITIVE_ZERO_NEGATIVE",
            "INTERIOR_SILENT_SECOND_RESPONSE_CARRY_DEPENDENT",
            "STRICT_HORIZONTAL_ENDPOINT_SECOND_RESPONSE_CARRY_INDEPENDENT_AT_THIS_ORDER",
            "VERTICAL_ENDPOINT_EXCLUDED_FROM_STRICT_FAMILY_AS_BRANCH_MEETING_BOUNDARY",
            "DOUBLE_SILENT_STRATUM_REQUIRES_THIRD_JET",
            "UNIVERSAL_SECOND_ORDER_TURN_ON_REFUTED",
        ], "classifications_exact")
        require(production["checks_passed"] == 48375, "production_48375_exact")
        require(production["strict_silent_case_count"] == 576,
                "production_576_strict_silent")
        require(production["vertical_boundary_case_count"] == 48,
                "production_48_vertical_boundary")
        require(production["strict_boost_case_count"] == 9792,
                "production_9792_strict_boost")
        require(production["boundary_boost_case_count"] == 816,
                "production_816_boundary_boost")
        require(production["interior_case_count"] == 528, "production_528_interior")
        require(production["horizontal_endpoint_case_count"] == 48,
                "production_48_horizontal_endpoint")
        require(production["double_silent_sample_count"] == 2,
                "production_double_silent")
        require({row["sign"] for row in production["sign_triplet"]} == {-1, 0, 1},
                "production_all_signs")
        require(production["scope"]["both_G332_branches"], "both_branches")
        require(production["scope"]["topology_inputs_used"] == [], "no_topology")
        require(production["scope"]["observational_inputs_used"] == [],
                "no_observations")
        require(independent["verdict"] == "PASS", "independent_pass")
        require(independent["checks_passed"] == 3860, "independent_3860_exact")
        require(not independent["imports_production"], "independent_no_import")
        require(not independent["reads_production_result"], "independent_no_result_read")
        require(independent["max_adm_error"] < 1e-10, "independent_adm_tolerance")
        require(catches["verdict"] == "PASS", "catch_pass")
        require(catches["mutations_caught"] == 14, "fourteen_mutations_caught")
        require("48375" in production_stdout and "9792" in production_stdout,
                "production_stdout")
        require("3860" in independent_stdout, "independent_stdout")
        require("14" in catches_stdout, "catch_stdout")

        for filename, replay in (
            ("DERIVATION_RESULT.json", production),
            ("INDEPENDENT_VERIFICATION.json", independent),
            ("CATCH_PROOF_RESULT.json", catches),
        ):
            registered = PACKAGE / filename
            require(registered.is_file(), f"registered_{filename}_exists")
            expected = (json.dumps(replay, indent=2, sort_keys=True) + "\n").encode()
            require(registered.read_bytes() == expected,
                    f"registered_{filename}_byte_exact")

    required_files = (
        "MAP.md", "EXPLORATORY_MAP_NOTE.md", "PREREGISTRATION.md",
        "PREREGISTRATION_SCOPE_REPAIR.md", "PREREGISTRATION_EXTERNAL_REPAIR.md",
        "PREMISE_LEDGER.tsv",
        "COMPLETENESS_MAP.md", "SOURCE_SCOPE.tsv", "SOURCE_MANIFEST.tsv",
        "EXECUTION_NOTE.md", "EXACT_DERIVATION.md", "LAY_REPORT.md", "STATUS_LEDGER.tsv",
        "AUDIT_REPORT.md", "EVIDENCE_GATES.md", "COMMANDS.md", "RUN_RECORD.md",
        "EXTERNAL_REVIEW_REQUEST.md", "EXTERNAL_REVIEW_RESPONSE.md",
        "EXTERNAL_REVIEW_TRANSMISSION.md", "EXTERNAL_REPAIR_FOLLOWUP.md",
        "REPAIR_IMPLEMENTATION.md",
        "REPAIR_FOLLOWUP_REQUEST.md", "build_review_intake.py",
        "build_repair_followup_intake.py", "verify_review_intake.py",
    )
    for filename in required_files:
        require((PACKAGE / filename).is_file(), f"document_{filename}")

    prereg = (PACKAGE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    disclosure = (PACKAGE / "EXPLORATORY_MAP_NOTE.md").read_text(encoding="utf-8")
    repair = (PACKAGE / "PREREGISTRATION_SCOPE_REPAIR.md").read_text(encoding="utf-8")
    external_repair = (PACKAGE / "PREREGISTRATION_EXTERNAL_REPAIR.md").read_text(
        encoding="utf-8"
    )
    exact = (PACKAGE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = (PACKAGE / "LAY_REPORT.md").read_text(encoding="utf-8")
    audit = (PACKAGE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    external = (PACKAGE / "EXTERNAL_REVIEW_RESPONSE.md").read_text(encoding="utf-8")
    followup = (PACKAGE / "EXTERNAL_REPAIR_FOLLOWUP.md").read_text(encoding="utf-8")
    ledger = (PACKAGE / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    require("EXPLORATORY_FORMULA_DISCLOSED" in prereg, "prereg_disclosure_status")
    require("not represented as a blind discovery" in disclosure,
            "not_blind_discovery")
    require("VERTICAL_ENDPOINT_IS_BRANCH_MEETING_BOUNDARY" not in prereg,
            "original_prereg_retained")
    require("SCIENTIFIC_SCOPE_REPAIR__STRICT_STRATUM_VERSUS_CLOSURE_BOUNDARY" in repair,
            "scope_repair_registered")
    require("radicand is positive exactly when `mu<1`" in repair,
            "scope_repair_math")
    require("= 1 + (R-6)mu/2 + b^2 mu^2" in exact,
            "reduced_formula_stated")
    require("For another unit-direction carry" in exact,
            "carry_category_boundary")
    require("branch-meeting closure boundary" in exact,
            "vertical_boundary_stated")
    require("For the strict interior `0<mu<1`" in exact,
            "external_R2_strict_domain_repaired")
    require("For `0<mu<=1`" not in exact,
            "external_R2_old_domain_absent")
    require("WORDING_SCOPE_REPAIR_ONLY__STRICT_INTERIOR_ZERO_SURFACE" in external_repair,
            "external_R2_preregistered")
    require("positive, zero, and negative" in lay,
            "lay_all_signs")
    require("not yet a complete evolving universe" in lay,
            "lay_not_complete_history")
    require("ACCEPT_WITH_REPAIRS__G336_BOUNDED_SILENT_SECOND_JET_RETAINED" in external,
            "external_math_retained")
    require("REPAIRS_ACCEPTED__G336_BOUNDED_SILENT_SECOND_JET_RETAINED" in followup,
            "external_R2_followup_accepted")
    require("follow-up independently accepted R2" in exact,
            "exact_R2_followup_accepted")
    require("EXTERNALLY_ACCEPTED_AFTER_PREREGISTERED_REPAIRS" in audit,
            "audit_external_accepted")
    require("Universal_Reciprocity_DDR\tOWNER_ADOPTED_PROVISIONAL_POSTULATE" in ledger,
            "DDR_owner_provisional")
    require("observations_scale_Xmax\tOMITTED_OPEN" in ledger,
            "scale_Xmax_open")

    rows = list(csv.DictReader(
        (PACKAGE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8"), delimiter="\t"
    ))
    require(len(rows) == 6, "six_source_rows")
    for row in rows:
        relative = Path(row["path"])
        require(not relative.is_absolute() and ".." not in relative.parts,
                f"source_{row['source_id']}_path_safe")
        payload = frozen_source(relative, int(row["bytes"]), row["sha256"])
        require(len(payload) == int(row["bytes"]), f"source_{row['source_id']}_bytes")
        require(digest_bytes(payload) == row["sha256"],
                f"source_{row['source_id']}_sha256")

    for script in (
        "derive_silent_second_response.py",
        "verify_silent_second_response_independent.py",
        "run_catch_proofs.py",
    ):
        source = (PACKAGE / script).read_text(encoding="utf-8")
        require("import numpy" not in source and "import sympy" not in source,
                f"{script}_standard_library_only")
    independent_source = (PACKAGE / "verify_silent_second_response_independent.py").read_text(
        encoding="utf-8"
    )
    require("derive_silent_second_response" not in independent_source,
            "independent_source_separation")

    payload = {
        "package": "G336",
        "all_passed": True,
        "check_count": len(checks),
        "checks": checks,
        "landing": LANDING,
        "registered_outputs_replayed": True,
        "package_mutated": False,
        "external_review": "ACCEPTED_AFTER_PREREGISTERED_REPAIRS",
    }
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(f"G336 package PASS: {len(checks)} aggregate gates")


if __name__ == "__main__":
    main()
