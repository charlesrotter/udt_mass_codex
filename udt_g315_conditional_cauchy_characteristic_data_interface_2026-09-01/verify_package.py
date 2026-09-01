#!/usr/bin/env python3
"""Aggregate self-contained verifier for the bounded G315 package."""

import ast
import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
LANDING = (
    "ACTIVE_EQUATION_HAS_A_LAWFUL_CONDITIONAL_DATA_INTERFACE"
    "__CAUCHY_AND_CHARACTERISTIC_DATA_REMAIN_FREELY_SUPPLIED_WITH_DERIVED_CONSTRAINTS"
)

REQUIRED = [
    "MAP.md",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "SOURCE_SCOPE.tsv",
    "REPLAY_COMMANDS.txt",
    "derive_data_interface.py",
    "verify_independent.py",
    "run_catch_proofs.py",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "DATA_INTERFACE_ATLAS.tsv",
    "EXACT_DERIVATION.md",
    "LAY_REPORT.md",
    "STATUS_LEDGER.tsv",
    "EVIDENCE_GATES.md",
    "AUDIT_REPORT.md",
    "RUN_RECORD.md",
    "EXTERNAL_REVIEW_REQUEST.md",
    "EXTERNAL_REVIEW_RESPONSE.md",
    "EXTERNAL_REVIEW_TRANSCRIPT.txt",
    "EXTERNAL_REVIEW_TRANSMISSION.md",
    "build_review_intake.py",
]


def need(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    for name in REQUIRED:
        need((HERE / name).is_file(), f"missing {name}")

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    hostile = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    need(production["landing"] == LANDING, "production landing mismatch")
    need(independent["landing"] == LANDING, "independent landing mismatch")
    need(production["production_assertions"] >= 70, "production assertion floor")
    need(independent["implementation_distinct_assertions"] >= 85, "independent assertion floor")
    need(not independent["production_module_imported"], "independent imported production")
    need(not independent["production_result_read"], "independent read production result")
    need(hostile["all_caught"] and hostile["caught"] == hostile["hostile_mutations"] >= 17, "hostile catch failure")

    with (HERE / "DATA_INTERFACE_ATLAS.tsv").open(encoding="utf-8", newline="") as handle:
        atlas = list(csv.DictReader(handle, delimiter="\t"))
    need(len(atlas) == 15, "atlas row count")
    need({row["classification"] for row in atlas} >= {"FREE_GAUGE", "CONSTRAINED", "DOWNSTREAM_EVALUATOR"}, "atlas type coverage")

    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = (HERE / "LAY_REPORT.md").read_text(encoding="utf-8")
    audit = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    request = (HERE / "EXTERNAL_REVIEW_REQUEST.md").read_text(encoding="utf-8")
    response = (HERE / "EXTERNAL_REVIEW_RESPONSE.md").read_text(encoding="utf-8")
    transmission = (HERE / "EXTERNAL_REVIEW_TRANSMISSION.md").read_text(encoding="utf-8")
    for text_name, text in (("prereg", prereg), ("exact", exact), ("audit", audit)):
        need(LANDING in text.replace("\n", ""), f"landing absent from {text_name}")
    for token in (
        "does not select one universe",
        "owner-adopted provisionally",
        "lapse `N` and shift",
        "One isolated null",
        "Metric, reciprocal kernel, angular cancellation",
    ):
        need(token in exact, f"exact guard missing: {token}")
    for token in ("starting snapshot", "two genuine local shape", "reciprocal kernel remains downstream"):
        need(token in lay, f"lay guard missing: {token}")
    for verdict in (
        "G315_ACCEPTED__CONDITIONAL_DATA_INTERFACE_UPHELD",
        "G315_REPAIRABLE_DEFECTS__BOUNDED_LANDING_RETAINED",
        "G315_SCIENTIFIC_LANDING_REFUTED",
        "G315_REVIEW_INCOMPLETE",
    ):
        need(verdict in request, f"external verdict absent: {verdict}")
    accepted = "G315_ACCEPTED__CONDITIONAL_DATA_INTERFACE_UPHELD"
    need(accepted in response, "accepted external verdict absent from response")
    need(accepted in transmission, "accepted external verdict absent from transmission record")
    need("I found no equation-sign defect" in response, "external scientific finding absent")

    independent_source = (HERE / "verify_independent.py").read_text(encoding="utf-8")
    need("import derive_data_interface" not in independent_source, "independent imports production")
    need("DERIVATION_RESULT.json" not in independent_source, "independent reads production result")
    allowed_modules = {"ast", "copy", "csv", "fractions", "hashlib", "json", "pathlib", "shutil", "tempfile"}
    for script in ("derive_data_interface.py", "verify_independent.py", "run_catch_proofs.py", "verify_package.py", "build_review_intake.py"):
        source = (HERE / script).read_text(encoding="utf-8")
        tree = ast.parse(source, filename=script)
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        need(imported <= allowed_modules, f"unregistered dependency in {script}: {sorted(imported - allowed_modules)}")

    guards = production["guards"]
    need(not any(guards.values()), "production nonpromotion guard changed")
    need(production["generic_local_phase_space_functions"] == 4, "phase-space count")
    need(production["generic_local_configuration_modes"] == 2, "configuration-mode count")
    need("Lambda cancels" in production["characteristic"]["same_null"], "same-null Lambda guard")

    source_scope = (HERE / "SOURCE_SCOPE.tsv").read_text(encoding="utf-8")
    for forbidden in (
        "udt_native_onshell_timelive_reset_owner_audit_2026-08-10",
        "udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12",
        "udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12",
        "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02",
    ):
        need(forbidden not in source_scope, f"protected path in source scope: {forbidden}")

    result = {
        "status": "PASS",
        "landing": LANDING,
        "production_assertions": production["production_assertions"],
        "independent_assertions": independent["implementation_distinct_assertions"],
        "hostile_catches": f"{hostile['caught']}/{hostile['hostile_mutations']}",
        "atlas_rows": len(atlas),
        "external_review": "ACCEPTED",
    }
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("G315 package verification PASS")
    print(f"production assertions: {result['production_assertions']}")
    print(f"independent assertions: {result['independent_assertions']}")
    print(f"hostile semantic mutations caught: {result['hostile_catches']}")
    print(LANDING)


if __name__ == "__main__":
    main()
