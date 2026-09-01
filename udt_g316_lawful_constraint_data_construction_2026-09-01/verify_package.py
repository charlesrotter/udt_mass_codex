#!/usr/bin/env python3
"""Aggregate self-contained verifier for the externally accepted bounded G316 package."""

import ast
import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
LANDING = (
    "CONFORMAL_CONSTRUCTION_MAPS_A_LAWFUL_SUBSET_WITH_NONTRIVIAL_SOLVABILITY_AND_"
    "CORNER_GAUGE_BOUNDS__NO_PHYSICAL_DATA_SELECTION"
)

REQUIRED = (
    "MAP.md", "PREMISE_LEDGER.tsv", "PREREGISTRATION.md", "SOURCE_SCOPE.tsv",
    "REPLAY_COMMANDS.txt", "derive_lawful_data_construction.py", "verify_independent.py",
    "run_catch_proofs.py", "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json", "DATA_CONSTRUCTION_ATLAS.tsv", "EXACT_DERIVATION.md",
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
    need(production["assertion_count"] >= 60, "production assertion floor")
    need(independent["assertion_count"] >= 130, "independent assertion floor")
    need(independent["production_imported"] is False, "independent imported production")
    need(independent["production_result_read"] is False, "independent read production result")
    need(hostile["status"] == "PASS", "hostile status")
    need(hostile["caught_count"] == hostile["mutation_count"] >= 16, "hostile catch failure")

    powers = production["conformal_powers"]
    need(powers == {"metric": 4, "A_up": -10, "A_norm": -12, "TT_scalar": -7, "scalar_source": 5, "momentum_source": 6}, "power ledger")
    need(production["formula"]["laplacian_coefficient"] == -8, "Laplacian coefficient")
    need(production["formula"]["tt_norm_coefficient"] == -1, "TT sign")
    need(production["formula"]["lambda_coefficient"] == -2, "Lambda sign")
    need(not production["selected_history"], "history selected")
    need(not production["metric_changed"], "metric changed")
    need(not production["kernel_changed"], "kernel changed")

    with (HERE / "DATA_CONSTRUCTION_ATLAS.tsv").open(encoding="utf-8", newline="") as handle:
        atlas = list(csv.DictReader(handle, delimiter="\t"))
    need(len(atlas) == 12, "atlas row count")
    classes = {row["classification"] for row in atlas}
    need({"SUPPLIED_SEED", "SOLVED_IF_SOLVABLE", "GAUGE_CONNECTION", "NOT_SELECTED"} <= classes, "atlas type coverage")

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
        "owner-adopted provisionally",
        "CONDITIONAL_IMPORTED_MATHEMATICAL_METHOD",
        "arbitrary seeds -> automatically physical universe",
        "No physical history",
        "Metric, reciprocal kernel, angular cancellation",
    ):
        need(token in exact, f"exact guard missing: {token}")
    for token in (
        "does **not** let us freely draw any starting geometry",
        "provably cannot be completed",
        "new physical tape measure",
        "does not choose which valid candidate Nature uses",
    ):
        need(token in lay, f"lay guard missing: {token}")
    for verdict in (
        "G316_ACCEPTED__LAWFUL_CONSTRUCTION_AND_BOUNDS_UPHELD",
        "G316_REPAIRABLE_DEFECTS__BOUNDED_LANDING_RETAINED",
        "G316_SCIENTIFIC_LANDING_REFUTED",
        "G316_REVIEW_INCOMPLETE",
    ):
        need(verdict in request, f"external verdict absent: {verdict}")
    accepted = "G316_ACCEPTED__LAWFUL_CONSTRUCTION_AND_BOUNDS_UPHELD"
    need(response.rstrip().endswith(accepted), "external response does not end with accepted verdict")
    need(accepted in transcript, "accepted verdict absent from transcript")
    need(accepted in transmission, "accepted verdict absent from transmission")
    need("all 31" in response, "external payload authentication count absent")
    need("byte-identical" in response, "external replay identity result absent")
    need(
        "do not find an algebraic, geometric, solvability, scope, or provenance defect" in response,
        "external scientific finding absent",
    )
    need("7c2d4b8431bb923741e41f9ac6c7f5291d8032be5777efc1fca87b4a1f81af29" in transmission, "scope seal absent")
    need("b4b6209ddee25ec1e41028883b0a52b0b37a2b6f9005ca5c0ffd5d5ff94569e4" in transmission, "manifest seal absent")

    independent_source = (HERE / "verify_independent.py").read_text(encoding="utf-8")
    need("import derive_lawful_data_construction" not in independent_source, "independent imports production")
    need("DERIVATION_RESULT.json" not in independent_source, "independent reads production result")

    allowed_modules = {"ast", "copy", "csv", "fractions", "hashlib", "json", "pathlib", "shutil", "tempfile"}
    for script in (
        "derive_lawful_data_construction.py", "verify_independent.py", "run_catch_proofs.py",
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
        "atlas_rows": len(atlas),
        "external_review": "ACCEPTED",
    }
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("G316 package verification PASS_EXTERNALLY_ACCEPTED")
    print(f"production assertions: {result['production_assertions']}")
    print(f"independent assertions: {result['independent_assertions']}")
    print(f"hostile mutations caught: {result['hostile_catches']}")
    print(LANDING)


if __name__ == "__main__":
    main()
