#!/usr/bin/env python3
"""Aggregate dependency-free verifier for the externally accepted bounded G317 package."""

import ast
import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
LANDING = (
    "EXACT_NONCMC_COUPLED_TORUS_FAMILY_EXISTS_WITH_ZERO_TIDE_AND_TIDAL_SUBBRANCHES__"
    "CONSTANT_PSI_CLASSIFICATION_FORCES_LAMBDA_MINUS_Q_SQUARED__NO_PHYSICAL_DATA_SELECTION"
)

REQUIRED = (
    "MAP.md", "PREMISE_LEDGER.tsv", "PREREGISTRATION.md", "SOURCE_SCOPE.tsv",
    "REPLAY_COMMANDS.txt", "derive_exact_noncmc_family.py", "verify_independent.py",
    "run_catch_proofs.py", "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json", "NONCMC_FAMILY_ATLAS.tsv", "EXACT_DERIVATION.md",
    "LAY_REPORT.md", "STATUS_LEDGER.tsv", "EVIDENCE_GATES.md", "AUDIT_REPORT.md",
    "RUN_RECORD.md", "EXTERNAL_REVIEW_REQUEST.md", "build_review_intake.py",
    "EXTERNAL_REVIEW_RESPONSE.md", "EXTERNAL_REVIEW_TRANSCRIPT.txt",
    "EXTERNAL_REVIEW_TRANSMISSION.md",
)


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
    need(production["assertion_count"] >= 1600, "production assertion floor")
    need(independent["assertion_count"] >= 1100, "independent assertion floor")
    need(production["family_instances"] == 48, "family instance count")
    need(production["atlas_rows"] == 14, "production atlas count")
    need(independent["production_imported"] is False, "independent imported production")
    need(independent["production_result_read"] is False, "independent read production result")
    need(hostile["status"] == "PASS", "hostile status")
    need(hostile["caught_count"] == hostile["mutation_count"] >= 20, "hostile catch failure")
    need(production["classification"]["Lambda"] == "-q^2", "Lambda classification")
    need(production["subclasses"] == {"q=0": "ZERO_INITIAL_WEYL", "q!=0": "NONZERO_ELECTRIC_WEYL"}, "tide split")
    need(not production["selected_history"], "history selected")
    need(not production["metric_changed"], "metric changed")
    need(not production["kernel_changed"], "kernel changed")

    with (HERE / "NONCMC_FAMILY_ATLAS.tsv").open(encoding="utf-8", newline="") as handle:
        atlas = list(csv.DictReader(handle, delimiter="\t"))
    need(len(atlas) == 14, "atlas row count")
    classes = {row["classification"] for row in atlas}
    need({"FREE_SMOOTH_PERIODIC_NONCMC_FUNCTION", "LAWFUL_OUTPUT", "ZERO_INITIAL_WEYL", "NONZERO_ELECTRIC_WEYL", "NOT_SELECTED"} <= classes, "atlas coverage")

    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = (HERE / "LAY_REPORT.md").read_text(encoding="utf-8")
    audit = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    request = (HERE / "EXTERNAL_REVIEW_REQUEST.md").read_text(encoding="utf-8")
    response = (HERE / "EXTERNAL_REVIEW_RESPONSE.md").read_text(encoding="utf-8")
    transcript = (HERE / "EXTERNAL_REVIEW_TRANSCRIPT.txt").read_text(encoding="utf-8")
    transmission = (HERE / "EXTERNAL_REVIEW_TRANSMISSION.md").read_text(encoding="utf-8")
    for label, text in (("prereg", prereg), ("exact", exact), ("audit", audit)):
        need(LANDING in text.replace("\n", ""), f"landing absent from {label}")
    for token in (
        "CHOSE_BOUNDED_DIAGNOSTIC_SLICE",
        "CONDITIONAL_IMPORTED_MATHEMATICAL_METHOD",
        "arbitrary smooth periodic nonconstant function",
        "not a global UDT sign theorem",
        "No physical initial data",
        "metric, reciprocal kernel, angular",
    ):
        need(token in exact, f"exact guard missing: {token}")
    for token in (
        "varying profile",
        "Weyl tensor detects a real tidal field",
        "genuine interlocking, not physical selection",
        "reciprocal kernel were not modified",
    ):
        need(token in lay, f"lay guard missing: {token}")
    for verdict in (
        "G317_ACCEPTED__EXACT_NONCMC_INTERLOCK_AND_TIDE_SPLIT_UPHELD",
        "G317_REPAIRABLE_DEFECTS__BOUNDED_LANDING_RETAINED",
        "G317_SCIENTIFIC_LANDING_REFUTED",
        "G317_REVIEW_INCOMPLETE",
    ):
        need(verdict in request, f"external verdict absent: {verdict}")
    accepted = "G317_ACCEPTED__EXACT_NONCMC_INTERLOCK_AND_TIDE_SPLIT_UPHELD"
    need(response.rstrip().endswith(accepted), "external response does not end with accepted verdict")
    need(accepted in transcript, "accepted verdict absent from transcript")
    need(accepted in transmission, "accepted verdict absent from transmission")
    need("every manifest-listed payload" in response, "external payload authentication absent")
    need("matched the sealed package outputs byte-for-byte" in response,
         "external replay identity absent")
    need("No algebraic, geometric, completeness-within-scope, or provenance defect" in response,
         "external scientific finding absent")
    need("464adc40cf5ca2493a9e11a4208281997a09470b7ecb3a1b6ee48e0eb510a088" in transmission,
         "scope seal absent")
    need("ec07bc8e532e3a1eb6c0ff918aed3c607f0518d506d253a8edc5fc15e76c7125" in transmission,
         "manifest seal absent")

    independent_source = (HERE / "verify_independent.py").read_text(encoding="utf-8")
    need("import derive_exact_noncmc_family" not in independent_source, "independent imports production")
    need("DERIVATION_RESULT.json" not in independent_source, "independent reads production result")

    allowed_modules = {"ast", "csv", "fractions", "hashlib", "json", "pathlib", "shutil", "tempfile"}
    for script in (
        "derive_exact_noncmc_family.py", "verify_independent.py", "run_catch_proofs.py",
        "verify_package.py", "build_review_intake.py",
    ):
        source = (HERE / script).read_text(encoding="utf-8")
        tree = ast.parse(source, filename=script)
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        need(imported <= allowed_modules, f"unregistered dependency in {script}: {sorted(imported - allowed_modules)}")

    source_scope = (HERE / "SOURCE_SCOPE.tsv").read_text(encoding="utf-8")
    for protected in (
        "udt_native_onshell_timelive_reset_owner_audit_2026-08-10",
        "udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12",
        "udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12",
        "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02",
    ):
        need(protected not in source_scope, f"protected path in source scope: {protected}")

    result = {
        "status": "PASS_EXTERNALLY_ACCEPTED",
        "landing": LANDING,
        "production_assertions": production["assertion_count"],
        "independent_assertions": independent["assertion_count"],
        "hostile_catches": f"{hostile['caught_count']}/{hostile['mutation_count']}",
        "family_instances": production["family_instances"],
        "atlas_rows": len(atlas),
        "external_review": "ACCEPTED",
    }
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("G317 package verification PASS_EXTERNALLY_ACCEPTED")
    print(f"production assertions: {result['production_assertions']}")
    print(f"independent assertions: {result['independent_assertions']}")
    print(f"hostile mutations caught: {result['hostile_catches']}")
    print(LANDING)


if __name__ == "__main__":
    main()
