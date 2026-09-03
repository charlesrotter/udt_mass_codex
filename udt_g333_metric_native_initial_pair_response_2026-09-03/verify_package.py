#!/usr/bin/env python3
"""Aggregate no-write verifier for the bounded G333 package."""

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
    "G332_METRIC_NATIVE_FIRST_RESPONSE_IS_COMMON_PLUS_DIRECTIONAL"
    "__COMPLETE_NORMAL_SPATIAL_PAIR_PULLBACK_EXCEEDS_ITS_TERMINAL_SCALAR"
    "__FIRST_JET_ONLY_NO_HOPF_SELECTION_OR_STABILITY"
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
    parser.add_argument("--output")
    args = parser.parse_args()
    checks = []

    def require(condition, name):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    with tempfile.TemporaryDirectory(prefix="g333_package_") as temporary:
        temp = Path(temporary)
        production, production_stdout = run(
            "derive_initial_pair_response.py", temp / "production.json"
        )
        independent, independent_stdout = run(
            "verify_initial_pair_response_independent.py", temp / "independent.json"
        )
        catches, catches_stdout = run("run_catch_proofs.py", temp / "catches.json")

        require(production["landing"] == LANDING, "landing_exact")
        require(production["grade"] == "DERIVED_CONDITIONAL_BOUNDED_PENDING_EXTERNAL_REVIEW",
                "production_result_preserves_pre_review_grade")
        require(production["classifications"] == [
            "METRIC_2_PLUS_1", "COMPLETE_PULLBACK_STRONGER"
        ], "classifications_exact")
        require(production["checks_passed"] == 6882, "production_6882_exact")
        require(production["sample_count"] == 360, "production_360_cases")
        require(production["topology_inputs_used"] == [], "no_topology_inputs")
        require(production["scope"]["all_unit_directions"], "all_directions_analytic")
        require(production["scope"]["both_G332_branches"], "both_branches")
        require(not production["scope"]["Hopf_selection"], "no_Hopf_selection")
        require(independent["verdict"] == "PASS", "independent_pass")
        require(independent["checks_passed"] == 146, "independent_146_exact")
        require(not independent["imports_production"], "independent_no_production_import")
        require(not independent["reads_production_result"], "independent_no_result_read")
        require(catches["verdict"] == "PASS", "catch_proof_pass")
        require(catches["mutations_caught"] == 9, "nine_mutations_caught")
        require("6882" in production_stdout and "360" in production_stdout,
                "production_stdout")
        require("146" in independent_stdout, "independent_stdout")
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
        "SOURCE_SCOPE.tsv", "SOURCE_MANIFEST.tsv", "EXTERNAL_REVIEW_REQUEST.md",
        "EXTERNAL_REVIEW_RESPONSE.md", "EXTERNAL_REVIEW_TRANSMISSION.md",
        "REPAIR_PREREGISTRATION.md", "REPAIR_IMPLEMENTATION.md", "REPAIR_FOLLOWUP_REQUEST.md",
        "EXTERNAL_REPAIR_FOLLOWUP.md", "REPAIR_FOLLOWUP_TRANSMISSION.md",
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
    review = (ROOT / "EXTERNAL_REVIEW_RESPONSE.md").read_text(encoding="utf-8")
    transmission = (ROOT / "EXTERNAL_REVIEW_TRANSMISSION.md").read_text(encoding="utf-8")
    repair = (ROOT / "REPAIR_PREREGISTRATION.md").read_text(encoding="utf-8")
    implementation = (ROOT / "REPAIR_IMPLEMENTATION.md").read_text(encoding="utf-8")
    followup_path = ROOT / "EXTERNAL_REPAIR_FOLLOWUP.md"
    followup = followup_path.read_text(encoding="utf-8")
    followup_transmission = (ROOT / "REPAIR_FOLLOWUP_TRANSMISSION.md").read_text(
        encoding="utf-8"
    )
    require("No candidate is privileged before execution" in map_text, "candidate_freeze")
    require("every unit separation direction" in prereg, "all_direction_prereg")
    require("Other timelike, oblique, null, accelerated" in exact, "pair_scope_boundary")
    require("does not use whether an integral curve" in exact, "topology_independence_proof")
    require("This is a curvature-to-first-response statement" in exact,
            "no_history_selection_promotion")
    require("may still" in lay and "matter later" in lay and "not needed for this result" in lay,
            "lay_Hopf_boundary")
    require("other observer-pair directions" in lay, "lay_pair_boundary")
    require("EXTERNALLY_ACCEPTED_AFTER_PREREGISTERED_REPAIRS" in audit,
            "external_repair_acceptance_grade")
    require("Gaussian_normal_presentation\tCHOSE_GAUGE_PRESENTATION_CONTROL" in ledger,
            "gauge_provenance")
    require("Hopf_topology\tOMITTED_OPEN" in ledger, "Hopf_omitted")
    require("physical_occupancy\tOMITTED_OPEN" in ledger, "occupancy_open")
    require("v_normal_extension\tCHOSE_TRANSPORT_PRESENTATION_CONTROL" in ledger,
            "transport_provenance")
    require("arbitrary timelike/mixed/null germs" in completeness, "pair_space_incomplete")
    require("ACCEPT_WITH_REPAIRS__G333_BOUNDED_FIRST_RESPONSE_RETAINED" in review,
            "fresh_review_retained")
    require("gamma(Hv,v) = (1/2)L_n gamma(v,v)" in review,
            "review_R1_requested")
    require("n(h11) = (L_n gamma)(v,v) + 2 gamma(L_n v, v)" in review,
            "review_R2_requested")
    require("representative directions rather than a second continuum symbolic proof" in review,
            "review_R3_requested")
    require("internal payload integrity and replay consistency" in transmission
            and "does not establish third-party authorship" in transmission,
            "repair_R4_implemented")
    require("H(v,v) := gamma(Hv,v)" in exact, "repair_R1_implemented")
    require("n[gamma(v,v)] = (L_n gamma)(v,v) + 2 gamma(L_n v,v)" in exact
            and "[n,v]=L_n v=0" in exact, "repair_R2_implemented")
    require("not a second continuum symbolic proof" in exact
            and "representative directions" in exact, "repair_R3_implemented")
    require("## R1 — contraction typing" in repair and "## R4 — seal meaning" in repair,
            "repairs_preregistered")
    require("All four externally requested repairs were implemented" in implementation,
            "repairs_implemented")
    require(digest(followup_path)
            == "52d7d293f55ce3284ef0e777151b43bfd64e217d2725cff5717577ef185b4a95",
            "repair_followup_sha256")
    require(followup.rstrip().endswith(
        "REPAIRS_ACCEPTED__G333_BOUNDED_FIRST_RESPONSE_RETAINED"
    ), "repair_followup_verdict")
    require("all `41` manifest payloads" in followup
            and "byte-identical to the sealed intake payloads" in followup,
            "repair_followup_authenticated_replay")
    require("e6a315d404e30524e9692ee455f59e26515d71bf82f30889f199951c17cfbb35"
            in followup_transmission
            and "2c2e91b5d5bcb28f1350acfba7a58a15f8b049e50329d4027db21906767b3c7c"
            in followup_transmission,
            "repair_followup_transmission_authenticated")

    source_rows = list(csv.DictReader(
        (ROOT / "SOURCE_MANIFEST.tsv").open(encoding="utf-8"), delimiter="\t"
    ))
    require(len(source_rows) == 9, "nine_source_rows")
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
        "derive_initial_pair_response.py",
        "verify_initial_pair_response_independent.py",
        "run_catch_proofs.py",
    ):
        source = (ROOT / script).read_text(encoding="utf-8")
        require("import numpy" not in source and "import sympy" not in source,
                f"{script}_standard_library_only")
    independent_source = (ROOT / "verify_initial_pair_response_independent.py").read_text(
        encoding="utf-8"
    )
    require("derive_initial_pair_response" not in independent_source,
            "independent_source_separation")

    payload = {
        "package": "G333",
        "all_passed": True,
        "check_count": len(checks),
        "checks": checks,
        "landing": LANDING,
        "registered_outputs_replayed": True,
        "package_mutated": False,
        "external_review": "ACCEPT_WITH_REPAIRS__G333_BOUNDED_FIRST_RESPONSE_RETAINED",
        "repair_followup": "REPAIRS_ACCEPTED__G333_BOUNDED_FIRST_RESPONSE_RETAINED",
    }
    if args.output:
        Path(args.output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"G333 package PASS: {len(checks)} aggregate gates")


if __name__ == "__main__":
    main()
