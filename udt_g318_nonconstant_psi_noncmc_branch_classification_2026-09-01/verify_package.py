#!/usr/bin/env python3
"""Aggregate dependency-free verifier for the externally accepted bounded G318 package."""

import ast
import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
LANDING = (
    "NONCONSTANT_PSI_FORCES_A_POWER_LAW_NONCMC_INTERLOCK__"
    "G317_DIRECT_FORM_IS_OBSTRUCTED__POSITIVE_PERIODIC_TIDAL_BRANCH_EXISTS__"
    "NO_PHYSICAL_DATA_SELECTION"
)

REQUIRED = (
    "MAP.md", "PREMISE_LEDGER.tsv", "COMPLETENESS_MAP.md", "PREREGISTRATION.md",
    "SOURCE_SCOPE.tsv", "REPLAY_COMMANDS.txt", "derive_nonconstant_psi_family.py",
    "verify_independent.py", "run_catch_proofs.py", "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json", "BRANCH_ATLAS.tsv",
    "EXACT_DERIVATION.md", "LAY_REPORT.md", "STATUS_LEDGER.tsv", "EVIDENCE_GATES.md",
    "AUDIT_REPORT.md", "RUN_RECORD.md", "EXTERNAL_REVIEW_REQUEST.md", "build_review_intake.py",
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
    need(production["assertion_count"] >= 14000, "production assertion floor")
    need(independent["assertion_count"] >= 4400, "independent assertion floor")
    need(production["center_witness_count"] == 4, "center witness count")
    need(production["atlas_rows"] == 16, "production atlas count")
    need(independent["production_imported"] is False, "independent imported production")
    need(independent["production_result_read"] is False, "independent read production result")
    need(independent["landing_upheld"] is True, "independent landing not upheld")
    need(hostile["status"] == "PASS", "hostile status")
    need(hostile["caught_count"] == hostile["mutation_count"] >= 40, "hostile catch failure")
    need(production["classification"]["G317_k_equals_1"].startswith("OBSTRUCTED"), "G317 obstruction")
    need(production["classification"]["n_minus2_strict_center"] == "POSITIVE_PERIODIC_LOCAL_FAMILY", "periodic family")
    need(production["classification"]["registered_periodic_tide"] == "NONZERO_WEYL", "tide class")
    need(not production["selected_history"], "history selected")
    need(not production["metric_changed"], "metric changed")
    need(not production["kernel_changed"], "kernel changed")

    with (HERE / "BRANCH_ATLAS.tsv").open(encoding="utf-8", newline="") as handle:
        atlas = list(csv.DictReader(handle, delimiter="\t"))
    need(len(atlas) == 16, "atlas row count")
    classes = {row["classification"] for row in atlas}
    need({
        "OBSTRUCTED_IN_REGISTERED_NONCONSTANT_PSI_BRANCH",
        "POWER_INTERLOCK",
        "NONLINEAR_AUTONOMOUS_ODE",
        "POSITIVE_PERIODIC_LOCAL_FAMILY",
        "NONZERO_ELECTRIC_TIDE",
        "NONZERO_MAGNETIC_TIDE_SOMEWHERE",
        "NOT_SELECTED",
    } <= classes, "atlas coverage")

    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = (HERE / "LAY_REPORT.md").read_text(encoding="utf-8")
    audit = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    request = (HERE / "EXTERNAL_REVIEW_REQUEST.md").read_text(encoding="utf-8")
    response = (HERE / "EXTERNAL_REVIEW_RESPONSE.md").read_text(encoding="utf-8")
    transcript = (HERE / "EXTERNAL_REVIEW_TRANSCRIPT.txt").read_text(encoding="utf-8")
    transmission = (HERE / "EXTERNAL_REVIEW_TRANSMISSION.md").read_text(encoding="utf-8")
    for label, body in (("prereg", prereg), ("exact", exact), ("audit", audit)):
        need(LANDING in body.replace("\n", ""), f"landing absent from {label}")
    for token in (
        "chosen diagnostic restrictions",
        "not a general non-CMC theorem",
        "standard one-dimensional autonomous phase portrait",
        "This does not prove that",
        "all nonconstant-`psi` data",
        "No physical initial data",
        "metric and reciprocal kernel are unchanged",
    ):
        need(token in exact, f"exact guard missing: {token}")
    for token in (
        "old G317 arrangement cannot simply be reused",
        "exact power relationship",
        "genuine tidal geometry",
        "does not choose which member Nature uses",
        "reciprocal kernel were not modified",
    ):
        need(token in lay, f"lay guard missing: {token}")
    for verdict in (
        "G318_ACCEPTED__NONCONSTANT_PSI_BRANCHING_AND_TIDAL_PERIODIC_FAMILY_UPHELD",
        "G318_REPAIRABLE_DEFECTS__BOUNDED_LANDING_RETAINED",
        "G318_SCIENTIFIC_LANDING_REFUTED",
        "G318_REVIEW_INCOMPLETE",
    ):
        need(verdict in request, f"external verdict absent: {verdict}")
    accepted = "G318_ACCEPTED__NONCONSTANT_PSI_BRANCHING_AND_TIDAL_PERIODIC_FAMILY_UPHELD"
    need(response.rstrip().endswith(accepted), "external response does not end with accepted verdict")
    need(accepted in transcript, "accepted verdict absent from transcript")
    need(accepted in transmission, "accepted verdict absent from transmission")
    need("All 33 manifest-listed payloads matched" in response,
         "external payload authentication absent")
    for artifact in (
        "DERIVATION_RESULT.json", "BRANCH_ATLAS.tsv", "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json", "PACKAGE_VERIFICATION_RESULT.json",
    ):
        need(f"`{artifact}`: byte-identical" in response,
             f"external replay identity absent: {artifact}")
    need("I found no scientific defect" in response,
         "external scientific finding absent")
    need("f31f9bf37b1d2d86fc3919466b2e19af05afabd86e4cc800c14453f28f8d6ef4" in transmission,
         "scope seal absent")
    need("226c20ae969c3f29c5fe9745db36191921cba7ac9030412fdd01e970d6142ee2" in transmission,
         "manifest seal absent")

    independent_source = (HERE / "verify_independent.py").read_text(encoding="utf-8")
    need("import derive_nonconstant_psi_family" not in independent_source, "independent imports production")
    need("DERIVATION_RESULT.json" not in independent_source, "independent reads production result")

    allowed_modules = {"ast", "csv", "fractions", "hashlib", "json", "pathlib", "shutil", "tempfile"}
    for script in (
        "derive_nonconstant_psi_family.py", "verify_independent.py", "run_catch_proofs.py",
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
        "center_witnesses": production["center_witness_count"],
        "weyl_instances": independent["weyl_instances"],
        "atlas_rows": len(atlas),
        "external_review": "ACCEPTED",
    }
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("G318 package verification PASS_EXTERNALLY_ACCEPTED")
    print(f"production assertions: {result['production_assertions']}")
    print(f"independent assertions: {result['independent_assertions']}")
    print(f"hostile mutations caught: {result['hostile_catches']}")
    print(LANDING)


if __name__ == "__main__":
    main()
