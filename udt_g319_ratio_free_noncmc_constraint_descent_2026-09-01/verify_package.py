#!/usr/bin/env python3
"""Aggregate dependency-free verifier for the externally accepted bounded G319 package."""

import ast
import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
LANDING = (
    "RATIO_FREE_REGULAR_STRATUM_HAS_EXACT_QUADRATURE_AND_ARBITRARY_"
    "POSITIVE_PERIODIC_PSI__B_ZERO_REMAINS_A_COMPATIBILITY_STRATUM__"
    "G318_POWER_OBSTRUCTIONS_ARE_ANSATZ_SCOPED__NO_PHYSICAL_DATA_SELECTION"
)

REQUIRED = (
    "MAP.md", "PREMISE_LEDGER.tsv", "COMPLETENESS_MAP.md", "PREREGISTRATION.md",
    "SOURCE_SCOPE.tsv", "REPLAY_COMMANDS.txt", "derive_ratio_free_family.py",
    "verify_independent.py", "run_catch_proofs.py", "verify_package.py",
    "build_review_intake.py", "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json", "PROFILE_ATLAS.tsv", "EXACT_DERIVATION.md",
    "LAY_REPORT.md", "STATUS_LEDGER.tsv", "EVIDENCE_GATES.md", "AUDIT_REPORT.md",
    "RUN_RECORD.md", "EXTERNAL_REVIEW_REQUEST.md", "EXTERNAL_REVIEW_RESPONSE.md",
    "EXTERNAL_REVIEW_CLI_FINAL.md", "EXTERNAL_REVIEW_TRANSCRIPT.txt",
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
    need(production["status"] == "PASS_PENDING_EXTERNAL_REVIEW", "production status")
    need(production["assertion_count"] >= 87000, "production assertion floor")
    need(production["exact_zero_stratum_instances"] >= 300, "zero-stratum coverage")
    need(production["periodic_profile_witnesses"] == 8, "profile witness count")
    need(independent["status"] == "PASS", "independent status")
    need(independent["assertion_count"] >= 35000, "independent assertion floor")
    need(independent["production_imported"] is False, "independent imported production")
    need(independent["production_result_read"] is False, "independent read production result")
    need(independent["landing_upheld"] is True, "independent landing not upheld")
    need(independent["periodic_variable_ratio_instances"] == 6, "independent profile count")
    need(independent["max_periodic_direct_residual"] < 1e-12, "direct residual too large")
    need(hostile["status"] == "PASS", "hostile status")
    need(hostile["caught_count"] == hostile["mutation_count"] >= 65, "hostile catch failure")

    classification = production["classification"]
    need(classification["regular_stratum"] == "EXACT_ONE_CONSTANT_QUADRATURE", "regular class")
    need(classification["positive_periodic_psi"] == "ARBITRARY_WITH_SUFFICIENTLY_LARGE_FREE_J0", "profile class")
    need(classification["B_zero"] == "COMPATIBILITY_GLUE_STRATUM_NOT_GLOBALLY_PARAMETERIZED", "zero class")
    need(classification["G318_power_family"] == "EXACT_EMBEDDED_SUBFAMILY", "G318 embedding")
    need(classification["G318_n_le_minus3_obstruction"] == "CONSTANT_RATIO_ANSATZ_SCOPED", "G318 scope")
    need(classification["G318_periodic_tidal_family"] == "SURVIVES_AS_EMBEDDED_SUBFAMILY", "G318 survival")
    for key in ("metric_changed", "kernel_changed", "selected_history", "selected_scale", "selected_Xmax"):
        need(production[key] is False, f"forbidden promotion: {key}")

    with (HERE / "PROFILE_ATLAS.tsv").open(encoding="utf-8", newline="") as handle:
        profiles = list(csv.DictReader(handle, delimiter="\t"))
    need(len(profiles) == 8, "profile atlas count")
    need({row["sign"] for row in profiles} == {"-1", "1"}, "profile signs")
    need({row["profile"] for row in profiles} == {"1", "2", "3", "4"}, "profile identities")
    need(all(float(row["min_psi"]) > 0 for row in profiles), "nonpositive psi")
    need(all(float(row["min_abs_tau"]) > 0 for row in profiles), "tau loses sign")
    need(all(float(row["ratio_range"]) > 1e-5 for row in profiles), "constant-ratio witness")
    need(max(float(row["max_hamiltonian"]) for row in profiles) < 1e-12, "profile Hamiltonian")
    need(max(float(row["max_momentum"]) for row in profiles) < 1e-12, "profile momentum")

    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = (HERE / "LAY_REPORT.md").read_text(encoding="utf-8")
    audit = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    request = (HERE / "EXTERNAL_REVIEW_REQUEST.md").read_text(encoding="utf-8")
    for label, body in (("exact", exact), ("audit", audit)):
        need(LANDING in body.replace("\n", ""), f"landing absent from {label}")
    for token in (
        "No division has occurred",
        "smooth positive periodic",
        "not the proof of the universal statement",
        "does not say that arbitrary constraint data are physical histories",
        "does not claim a global parameterization",
        "scope correction, not a refutation or deletion of G318",
        "metric, completed-pair pullback, and reciprocal kernel are unchanged",
    ):
        need(token in exact, f"exact guard missing: {token}")
    for token in (
        "restrictive behavior came from one simplifying assumption",
        "do not choose the shape",
        "G318 was not wrong",
        "unfinished edge case",
        "did not choose a universe",
    ):
        need(token in lay, f"lay guard missing: {token}")
    for token in (
        "sufficiently large `J_0`",
        "No claim of a full explicit",
        "G318 regression test",
        "No\nphysical data",
    ):
        need(token in prereg, f"prereg guard missing: {token}")
    for verdict in (
        "G319_ACCEPTED__RATIO_FREE_REGULAR_QUADRATURE_AND_ANSATZ_SCOPE_UPHELD",
        "G319_REPAIRABLE_DEFECTS__BOUNDED_LANDING_RETAINED",
        "G319_SCIENTIFIC_LANDING_REFUTED",
        "G319_REVIEW_INCOMPLETE",
    ):
        need(verdict in request, f"external verdict missing: {verdict}")

    response = (HERE / "EXTERNAL_REVIEW_RESPONSE.md").read_text(encoding="utf-8")
    cli_final = (HERE / "EXTERNAL_REVIEW_CLI_FINAL.md").read_text(encoding="utf-8")
    transcript = (HERE / "EXTERNAL_REVIEW_TRANSCRIPT.txt").read_text(encoding="utf-8")
    transmission = (HERE / "EXTERNAL_REVIEW_TRANSMISSION.md").read_text(encoding="utf-8")
    accepted = "G319_ACCEPTED__RATIO_FREE_REGULAR_QUADRATURE_AND_ANSATZ_SCOPE_UPHELD"
    need(response.rstrip().endswith(accepted), "external response does not end with acceptance")
    for label, body in (("CLI final", cli_final), ("transcript", transcript),
                        ("transmission", transmission)):
        need(accepted in body, f"external acceptance absent from {label}")
    need("All 33 listed payloads matched" in response, "external authentication absent")
    need("exact matches" in response and "This matters" in response,
         "external byte-identical replay finding absent")
    for artifact in (
        "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json",
        "PACKAGE_VERIFICATION_RESULT.json", "PROFILE_ATLAS.tsv",
    ):
        need(artifact in response, f"external replay artifact absent: {artifact}")
    need("I found no scientific defect" in response, "external scientific finding absent")
    need("global `B=0` crossing classification" in response,
         "external zero-stratum boundary absent")
    need("6b90239f7e62063541596ebd38d21a3ab67703b53ec32190cf95009a2ad500c7"
         in transmission, "scope seal absent")
    need("fe7976081493fc99e30a123616a4a6710674a83a3884ff048db51b3065e2d0fa"
         in transmission, "manifest seal absent")

    independent_source = (HERE / "verify_independent.py").read_text(encoding="utf-8")
    need("import derive_ratio_free_family" not in independent_source, "independent imports production")
    need("DERIVATION_RESULT.json" not in independent_source, "independent reads production output")

    allowed_modules = {
        "ast", "csv", "fractions", "hashlib", "json", "math", "pathlib", "shutil", "tempfile"
    }
    for script in (
        "derive_ratio_free_family.py", "verify_independent.py", "run_catch_proofs.py",
        "verify_package.py", "build_review_intake.py",
    ):
        tree = ast.parse((HERE / script).read_text(encoding="utf-8"), filename=script)
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
        "zero_stratum_instances": production["exact_zero_stratum_instances"],
        "production_profiles": len(profiles),
        "independent_profiles": independent["periodic_variable_ratio_instances"],
        "hostile_catches": f"{hostile['caught_count']}/{hostile['mutation_count']}",
        "external_review": "ACCEPTED",
    }
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("G319 package verification PASS_EXTERNALLY_ACCEPTED")
    print(f"production assertions: {result['production_assertions']}")
    print(f"independent assertions: {result['independent_assertions']}")
    print(f"hostile mutations caught: {result['hostile_catches']}")
    print(LANDING)


if __name__ == "__main__":
    main()
