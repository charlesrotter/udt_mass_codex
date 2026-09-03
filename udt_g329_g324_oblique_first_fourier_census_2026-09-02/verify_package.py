#!/usr/bin/env python3
"""Dependency-light aggregate verifier for the bounded G329 package."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


LANDING = (
    "PRIMITIVE_OBLIQUE_FOURIER_SECTOR_CLOSES_MODULO_PERIODIC_GAUGE__"
    "TWO_PHYSICAL_AMPLITUDES__EXACT_COUPLING_CLASSIFICATION__"
    "EXACT_COMPACT_TIME_CENSUS__NO_FULL_STABILITY_CLAIM"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="PACKAGE_VERIFICATION_RESULT.json")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    checks: list[str] = []

    def gate(condition: bool, name: str) -> None:
        assert condition, name
        checks.append(name)

    required = [
        "MAP.md", "COMPLETENESS_MAP.md", "PREMISE_LEDGER.tsv", "SOURCE_SCOPE.tsv",
        "PREREGISTRATION.md", "PREREGISTRATION_REPAIR_NOTE.md",
        "PREREGISTRATION_COMMIT_OBJECT.txt", "PREREGISTRATION_TREE.tsv",
        "derive_oblique_modes.py", "verify_independent.py", "run_catch_proofs.py",
        "DERIVATION_RESULT.json", "RAW_RESIDUALS.json", "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json", "EXACT_DERIVATION.md", "LAY_REPORT.md",
        "STATUS_LEDGER.tsv", "EVIDENCE_GATES.md", "RUN_RECORD.md", "REPLAY_COMMANDS.txt",
        "SOURCE_MANIFEST.tsv",
        "AUDIT_REPORT.md", "ADVERSARIAL_REVIEW_REQUEST.md",
        "build_review_intake.py", "verify_review_intake.py",
    ]
    for name in required:
        gate((root / name).is_file(), f"required_{name}")

    production = json.loads((root / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((root / "INDEPENDENT_VERIFICATION.json").read_text())
    hostile = json.loads((root / "CATCH_PROOF_RESULT.json").read_text())
    raw = json.loads((root / "RAW_RESIDUALS.json").read_text())
    prereg = (root / "PREREGISTRATION.md").read_text()
    exact = (root / "EXACT_DERIVATION.md").read_text()
    lay = (root / "LAY_REPORT.md").read_text()
    ledger = (root / "PREMISE_LEDGER.tsv").read_text()
    replays = (root / "REPLAY_COMMANDS.txt").read_text().splitlines()
    source_manifest = (root / "SOURCE_MANIFEST.tsv").read_text()
    proof = (root / "PREREGISTRATION_COMMIT_OBJECT.txt").read_text()
    tree = (root / "PREREGISTRATION_TREE.tsv").read_text()

    gate(production["landing"] == LANDING, "production_landing")
    gate(independent["landing"] == LANDING, "independent_landing")
    gate(production["physical_dimension_real"] == 8, "production_dimension_eight")
    gate(independent["physical_dimension_real"] == 8, "independent_dimension_eight")
    gate(production["check_count"] == len(production["checks"]), "production_count_exact")
    gate(production["check_count"] >= 105, "production_at_least_105_checks")
    gate(independent["check_count"] == 28, "independent_28_checks")
    gate(independent["reads_production_output"] is False, "independent_no_result_read")
    gate(hostile["all_caught"] is True and hostile["catch_count"] == 11,
         "hostile_eleven_of_eleven")
    gate(hostile["production_output_read"] is False, "hostile_no_result_read")
    gate(raw["variables"]["odd"] == ["N", "H", "Q"], "raw_odd_three")
    gate(raw["variables"]["even"] == ["A", "B", "C", "U", "V", "W", "Z"],
         "raw_even_seven")
    gate(len(raw["odd_upper_triangle"]) == 10, "raw_odd_all_upper_components")
    gate(len(raw["even_upper_triangle"]) == 10, "raw_even_all_upper_components")
    gate(raw["odd_scalar"] == "0", "raw_odd_scalar_zero")
    gate("alpha" in production["masters"]["even"] and "beta" in production["masters"]["even"],
         "even_master_keeps_both_components")
    gate("alpha" in production["masters"]["odd_normalized"] and "beta" in production["masters"]["odd_normalized"],
         "odd_master_keeps_both_components")
    gate("ENDPOINT_ASYMPTOTICS_PARTIALLY_OPEN" not in production["landing"],
         "endpoint_classification_closed_without_filter")
    gate("NO_FULL_STABILITY_CLAIM" in prereg and "NO_FULL_STABILITY_CLAIM" in exact,
         "bounded_stability_language")
    gate("does **not** establish full stability" in lay, "lay_scope_guard")
    gate("OWNER_ADOPTED_PROVISIONAL_POSTULATE" in ledger, "equation_owner_stamp")
    gate("source action matter observation fit scale Xmax\tABSENT" in ledger,
         "forbidden_imports_absent_stamp")
    gate("67b06ba162d7311362684b275bda441c9a0f4d19" in proof,
         "initial_prereg_commit_recorded")
    gate("f606f50384ccc476ae7af94ec10bba14f2bc2c7b" in proof,
         "neutrality_repair_commit_recorded")
    gate(tree.count("\n") == 7, "prereg_tree_six_entries")
    gate(len(replays) == 4 and all("/tmp/G329_" in line for line in replays),
         "four_no_repository_output_replays")
    gate(all("python3 -S" in line for line in replays), "dependency_free_replay_mode")

    independent_source = (root / "verify_independent.py").read_text()
    hostile_source = (root / "run_catch_proofs.py").read_text()
    gate("DERIVATION_RESULT.json" not in independent_source, "independent_source_no_production_json")
    gate("DERIVATION_RESULT.json" not in hostile_source, "hostile_source_no_production_json")
    gate("subprocess" not in independent_source and "subprocess" not in hostile_source,
         "no_hidden_solver_dispatch")
    for source_name in ("derive_oblique_modes.py", "verify_independent.py", "run_catch_proofs.py"):
        digest = hashlib.sha256((root / source_name).read_bytes()).hexdigest()
        gate(f"{source_name}\t{digest}" in source_manifest, f"source_manifest_{source_name}")

    hashes = {}
    for name in required:
        hashes[name] = hashlib.sha256((root / name).read_bytes()).hexdigest()
    result = {
        "schema": "udt-g329-package-verification-v1",
        "landing": LANDING,
        "all_passed": True,
        "check_count": len(checks),
        "checks": checks,
        "required_sha256": hashes,
        "maximum_internal_grade": "DERIVED_CONDITIONAL__INTERNALLY_VERIFIED__EXTERNAL_REVIEW_PENDING",
    }
    (root / args.output).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
