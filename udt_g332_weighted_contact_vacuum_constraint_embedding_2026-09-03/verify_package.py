#!/usr/bin/env python3
"""Aggregate no-write verifier for the bounded G332 package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
SEALED_SOURCE_ROOT = REPO / "sources"
LANDING = (
    "EXACT_IRREGULAR_WEIGHTED_CONTACT_VACUUM_CONSTRAINT_DATA_EXIST"
    "__INITIAL_CONSTRAINTS_DO_NOT_FORCE_HOPF_ORBIT_RIGIDITY"
    "__EXISTENCE_IS_NOT_A_FULL_K_CENSUS_OR_DYNAMIC_STABILITY"
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(script, output):
    result = subprocess.run(
        ["python3", "-S", str(ROOT / script), "--output", str(output)],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise AssertionError(f"{script} failed: {result.stderr or result.stdout}")
    return json.loads(output.read_text(encoding="utf-8")), result.stdout.strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="PACKAGE_VERIFICATION_RESULT.json")
    args = parser.parse_args()
    checks = []

    def require(condition, name):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    with tempfile.TemporaryDirectory(prefix="g332_package_") as temporary:
        temp = Path(temporary)
        production, production_stdout = run(
            "derive_weighted_constraint_embedding.py", temp / "production.json"
        )
        independent, independent_stdout = run(
            "verify_weighted_constraint_embedding_independent.py", temp / "independent.json"
        )
        catches, catches_stdout = run("run_catch_proofs.py", temp / "catches.json")

        require(production["landing"] == LANDING, "landing_exact")
        require(production["checks_passed"] == 642, "production_642_exact")
        require(production["sample_count"] == 80, "production_80_cases")
        require(independent["verdict"] == "PASS", "independent_pass")
        require(independent["checks_passed"] == 65, "independent_65_exact")
        require(not independent["imports_production"], "independent_no_production_import")
        require(not independent["reads_production_result"], "independent_no_result_read")
        require(catches["verdict"] == "PASS", "catch_proof_pass")
        require(catches["mutations_caught"] == 9, "nine_mutations_caught")
        require("642" in production_stdout and "80" in production_stdout, "production_stdout")
        require("65" in independent_stdout, "independent_stdout")
        require("9" in catches_stdout, "catch_stdout")

        registered = (
            ("DERIVATION_RESULT.json", production),
            ("INDEPENDENT_VERIFICATION.json", independent),
            ("CATCH_PROOF_RESULT.json", catches),
        )
        for filename, replay in registered:
            path = ROOT / filename
            require(path.is_file(), f"registered_{filename}_exists")
            require(path.read_bytes() == (
                json.dumps(replay, indent=2, sort_keys=True) + "\n"
            ).encode("utf-8"), f"registered_{filename}_byte_exact")

    required_files = (
        "MAP.md", "PREREGISTRATION.md", "PREMISE_LEDGER.tsv", "COMPLETENESS_MAP.md",
        "EXECUTION_NOTE.md", "EXACT_DERIVATION.md", "LAY_REPORT.md", "STATUS_LEDGER.tsv",
        "AUDIT_REPORT.md", "EVIDENCE_GATES.md", "COMMANDS.md", "RUN_RECORD.md",
        "SOURCE_SCOPE.tsv", "SOURCE_MANIFEST.tsv", "EXTERNAL_REVIEW_RESPONSE.md",
        "EXTERNAL_REVIEW_TRANSMISSION.md", "REPAIR_PREREGISTRATION.md",
        "REPAIR_FOLLOWUP_REQUEST.md", "EXTERNAL_REPAIR_FOLLOWUP.md",
        "REPAIR_FOLLOWUP_TRANSMISSION.md",
    )
    for filename in required_files:
        require((ROOT / filename).is_file(), f"document_{filename}")

    prereg = (ROOT / "PREREGISTRATION.md").read_text(encoding="utf-8")
    exact = (ROOT / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    audit = (ROOT / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    lay = (ROOT / "LAY_REPORT.md").read_text(encoding="utf-8")
    ledger = (ROOT / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    review = (ROOT / "EXTERNAL_REVIEW_RESPONSE.md").read_text(encoding="utf-8")
    repair = (ROOT / "REPAIR_PREREGISTRATION.md").read_text(encoding="utf-8")
    followup = (ROOT / "EXTERNAL_REPAIR_FOLLOWUP.md").read_text(encoding="utf-8")
    require("The question permits all six components of `K`" in prereg, "unrestricted_K_question")
    require("failure of the registered witness is insufficient" in prereg, "obstruction_burden")
    require("The derivative of `b` has not been discarded" in exact, "b_derivative_audited")
    require("for every smooth compact three-metric with a global unit Killing field" in exact,
            "analytic_family_scope")
    require("It does not classify all possible `K`" in exact, "no_full_K_census")
    require("physical-data selector or a theorem about later-time orbit closure" in exact,
            "no_dynamic_promotion")
    require("proof that Nature occupies one" in lay, "lay_occupancy_boundary")
    require("extrinsic_curvature\tfree-and-explored" in ledger, "K_provenance")
    require("Lambda\tfree-and-explored_CONDITIONAL" in ledger, "Lambda_provenance")
    require("historical_carrier_action\tOMITTED_OPEN" in ledger, "carrier_action_excluded")
    require("DERIVED_CONDITIONAL__EXTERNALLY_ACCEPTED_BOUNDED" in audit,
            "external_review_accepted")
    require("ACCEPT_WITH_REPAIRS__G332_SCIENTIFIC_LANDING_RETAINED" in review,
            "fresh_review_retained_landing")
    require("dependency-free sealed source resolution" in repair, "repair_R1_registered")
    require("explicit tensor index convention" in repair, "repair_R2_registered")
    require("REPAIRS_ACCEPTED__G332_BOUNDED_SCIENTIFIC_LANDING_RETAINED" in followup,
            "repair_followup_accepted")

    source_rows = list(csv.DictReader((ROOT / "SOURCE_MANIFEST.tsv").open(encoding="utf-8"), delimiter="\t"))
    require(len(source_rows) == 12, "twelve_source_rows")
    source_root = SEALED_SOURCE_ROOT if SEALED_SOURCE_ROOT.is_dir() else REPO
    resolved_source_root = source_root.resolve()
    for row in source_rows:
        relative = Path(row["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise AssertionError(f"source_{row['source_id']}_path_safe")
        source = (source_root / relative).resolve()
        if not source.is_relative_to(resolved_source_root):
            raise AssertionError(f"source_{row['source_id']}_contained")
        require(source.is_file(), f"source_{row['source_id']}_exists")
        require(source.stat().st_size == int(row["bytes"]), f"source_{row['source_id']}_bytes")
        require(digest(source) == row["sha256"], f"source_{row['source_id']}_sha256")

    for script in (
        "derive_weighted_constraint_embedding.py",
        "verify_weighted_constraint_embedding_independent.py",
        "run_catch_proofs.py",
    ):
        source = (ROOT / script).read_text(encoding="utf-8")
        require("import numpy" not in source and "import sympy" not in source,
                f"{script}_standard_library_only")
    independent_source = (ROOT / "verify_weighted_constraint_embedding_independent.py").read_text(
        encoding="utf-8"
    )
    require("derive_weighted_constraint_embedding" not in independent_source,
            "independent_source_separation")

    payload = {
        "package": "G332",
        "all_passed": True,
        "check_count": len(checks),
        "checks": checks,
        "landing": LANDING,
        "registered_outputs_replayed": True,
        "package_mutated": False,
        "external_review_accepted": True,
        "repair_followup_accepted": True,
    }
    Path(args.output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"G332 package PASS: {len(checks)} aggregate gates")


if __name__ == "__main__":
    main()
