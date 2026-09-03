#!/usr/bin/env python3
"""Aggregate no-write verifier for the bounded pre-review G334 package."""

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
    "G333_FIRST_NORMAL_RESPONSE_HAS_EXACT_FINITE_BOOST_CONGRUENCE"
    "__ARBITRARY_PAIR_FIRST_JET_REMAINS_TRANSPORT_QUALIFIED"
    "__COMPLETE_MATRIX_EXCEEDS_TERMINAL_PHI_ON_INHERITED_GERMS"
    "__NO_NEW_CHANNEL_OR_OBSERVER_TIME_EVOLUTION"
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(script, output):
    result = subprocess.run(
        ["python3", "-B", "-S", str(ROOT / script), "--output", str(output)],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise AssertionError(f"{script} failed: {result.stderr or result.stdout}")
    return json.loads(output.read_text(encoding="utf-8")), result.stdout.strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()
    checks = []

    def require(condition, name):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    with tempfile.TemporaryDirectory(prefix="g334_package_") as temporary:
        temp = Path(temporary)
        production, production_stdout = run(
            "derive_boosted_pair_first_jet.py", temp / "production.json"
        )
        independent, independent_stdout = run(
            "verify_boosted_pair_first_jet_independent.py", temp / "independent.json"
        )
        catches, catches_stdout = run("run_catch_proofs.py", temp / "catches.json")

        require(production["landing"] == LANDING, "landing_exact")
        require(production["grade"] ==
                "DERIVED_CONDITIONAL_BOUNDED__EXTERNALLY_ACCEPTED_AFTER_PREREGISTERED_REPAIRS",
                "grade_exact")
        require(production["classifications"] == [
            "TRANSPORT_QUALIFIED_CONGRUENCE",
            "COMPLETE_MATRIX_STRONGER_ON_DECLARED_TRANSPORT",
        ], "classifications_exact")
        require(production["checks_passed"] == 43026, "production_43026_exact")
        require(production["sample_count"] == 2520, "production_2520_cases")
        require(len(production["checks_sha256"]) == 64, "production_check_digest")
        require(production["topology_inputs_used"] == [], "no_topology_inputs")
        require(production["scope"]["all_unit_directions"], "all_directions")
        require(production["scope"]["both_G332_branches"], "both_branches")
        require(production["scope"]["normal_derivative_only"], "normal_derivative_only")
        require(not production["scope"]["arbitrary_transport_unique_from_boost"],
                "transport_qualification")
        require(independent["verdict"] == "PASS", "independent_pass")
        require(independent["checks_passed"] == 580, "independent_580_exact")
        require(not independent["imports_production"], "independent_no_production_import")
        require(not independent["reads_production_result"], "independent_no_result_read")
        require(catches["verdict"] == "PASS", "catch_pass")
        require(catches["mutations_caught"] == 12, "twelve_mutations_caught")
        require("43026" in production_stdout and "2520" in production_stdout,
                "production_stdout")
        require("580" in independent_stdout, "independent_stdout")
        require("12" in catches_stdout, "catch_stdout")

        for filename, replay in (
            ("DERIVATION_RESULT.json", production),
            ("INDEPENDENT_VERIFICATION.json", independent),
            ("CATCH_PROOF_RESULT.json", catches),
        ):
            registered = ROOT / filename
            require(registered.is_file(), f"registered_{filename}_exists")
            expected = (json.dumps(replay, indent=2, sort_keys=True) + "\n").encode("utf-8")
            require(registered.read_bytes() == expected, f"registered_{filename}_byte_exact")

    required_files = (
        "MAP.md", "PREREGISTRATION.md", "PREMISE_LEDGER.tsv", "COMPLETENESS_MAP.md",
        "EXECUTION_NOTE.md", "EXACT_DERIVATION.md", "LAY_REPORT.md", "STATUS_LEDGER.tsv",
        "AUDIT_REPORT.md", "EVIDENCE_GATES.md", "COMMANDS.md", "RUN_RECORD.md",
        "SOURCE_SCOPE.tsv", "SOURCE_MANIFEST.tsv",
    )
    for filename in required_files:
        require((ROOT / filename).is_file(), f"document_{filename}")

    prereg = (ROOT / "PREREGISTRATION.md").read_text(encoding="utf-8")
    map_text = (ROOT / "MAP.md").read_text(encoding="utf-8")
    exact = (ROOT / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = (ROOT / "LAY_REPORT.md").read_text(encoding="utf-8")
    audit = (ROOT / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    ledger = (ROOT / "PREMISE_LEDGER.tsv").read_text(encoding="utf-8")
    completeness = (ROOT / "COMPLETENESS_MAP.md").read_text(encoding="utf-8")
    require("No candidate is privileged before execution" in map_text, "candidate_freeze")
    require("all finite boost signs and magnitudes" in prereg, "finite_boost_prereg")
    require("free-and-explored_GERM_DATA" in prereg, "transport_preregistered")
    require("D_general = D(z)+[[-2alpha, beta-gamma]" in exact,
            "general_transport_formula")
    require("pointwise boost value and `q` do not determine" in exact,
            "boost_insufficiency_stated")
    require("cannot be promoted into the time history" in exact,
            "observer_time_boundary")
    require("The full pair matrix does not have that blind spot" in lay,
            "lay_complete_matrix_boundary")
    require("how its measuring axes are carried" in lay, "lay_transport_boundary")
    require("EXTERNALLY_ACCEPTED_AFTER_PREREGISTERED_REPAIRS" in audit,
            "review_accepted_after_repairs")
    require("boost_rapidity_z\tfree-and-explored" in ledger, "boost_free")
    require("general_pair_transport\tfree-and-explored_GERM_DATA" in ledger,
            "general_transport_free")
    require("observer_time_derivative\tOMITTED_OPEN" in ledger, "observer_time_open")
    require("screen-mixed, null, accelerated" in completeness, "pair_space_incomplete")

    source_rows = list(csv.DictReader(
        (ROOT / "SOURCE_MANIFEST.tsv").open(encoding="utf-8"), delimiter="\t"
    ))
    require(len(source_rows) == 9, "nine_source_rows")
    source_root = SEALED_SOURCE_ROOT if SEALED_SOURCE_ROOT.is_dir() else REPO
    resolved_root = source_root.resolve()
    for row in source_rows:
        relative = Path(row["path"])
        require(not relative.is_absolute() and ".." not in relative.parts,
                f"source_{row['source_id']}_path_safe")
        source = (source_root / relative).resolve()
        require(source.is_relative_to(resolved_root), f"source_{row['source_id']}_contained")
        require(source.is_file(), f"source_{row['source_id']}_exists")
        require(source.stat().st_size == int(row["bytes"]), f"source_{row['source_id']}_bytes")
        require(digest(source) == row["sha256"], f"source_{row['source_id']}_sha256")

    for script in (
        "derive_boosted_pair_first_jet.py",
        "verify_boosted_pair_first_jet_independent.py",
        "run_catch_proofs.py",
    ):
        source = (ROOT / script).read_text(encoding="utf-8")
        require("import numpy" not in source and "import sympy" not in source,
                f"{script}_standard_library_only")
    independent_source = (ROOT / "verify_boosted_pair_first_jet_independent.py").read_text(
        encoding="utf-8"
    )
    require("derive_boosted_pair_first_jet" not in independent_source,
            "independent_source_separation")

    payload = {
        "package": "G334",
        "all_passed": True,
        "check_count": len(checks),
        "checks": checks,
        "landing": LANDING,
        "registered_outputs_replayed": True,
        "package_mutated": False,
        "external_review": "ACCEPTED_AFTER_PREREGISTERED_REPAIRS",
    }
    if args.output:
        Path(args.output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"G334 package PASS: {len(checks)} aggregate gates")


if __name__ == "__main__":
    main()
