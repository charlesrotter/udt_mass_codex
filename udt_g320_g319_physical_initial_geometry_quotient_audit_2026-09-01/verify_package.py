#!/usr/bin/env python3
"""Aggregate dependency-free verifier for the externally accepted bounded G320 package."""

import ast
import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
LANDING = (
    "G319_FREEDOM_NOT_PURE_REPRESENTATION__SCALE_FREE_INTRINSIC_CURVATURE_"
    "SEPARATES_LAWFUL_PROFILES__DECLARED_GAUGE_DUPLICATES_QUOTIENTED__"
    "NO_COMPLETE_MODULI_OR_PHYSICAL_DATA_SELECTION"
)
REQUIRED = (
    "MAP.md", "PREMISE_LEDGER.tsv", "COMPLETENESS_MAP.md", "PREREGISTRATION.md",
    "SOURCE_SCOPE.tsv", "REPLAY_COMMANDS.txt", "derive_physical_quotient.py",
    "verify_independent.py", "run_catch_proofs.py", "verify_package.py",
    "build_review_intake.py", "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json", "INVARIANT_ATLAS.tsv", "EXACT_DERIVATION.md",
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
    need(production["status"] == "PASS_PENDING_EXTERNAL_REVIEW", "production status")
    need(production["landing"] == LANDING, "production landing")
    need(production["assertion_count"] >= 290, "production assertion floor")
    need(production["Q_R_mode_scaling"] == "n^2", "mode scaling")
    need(production["intrinsic_physical_inequivalence"] is True, "inequivalence absent")
    need(production["countably_infinite_physical_directions_in_registered_family"] is True, "family breadth absent")
    need(production["every_distinct_profile_proven_inequivalent"] is False, "complete quotient overclaim")
    need(production["conformal_seed_full_data_duplicate_control_pass"] is True, "seed control")
    need(independent["status"] == "PASS", "independent status")
    need(independent["assertion_count"] >= 59, "independent assertion floor")
    need(independent["production_imported"] is False, "independent imported production")
    need(independent["production_result_read"] is False, "independent read production result")
    need(independent["intrinsic_inequivalence_upheld"] is True, "independent separator")
    need(hostile["status"] == "PASS", "hostile status")
    need(hostile["caught_count"] == hostile["mutation_count"] >= 26, "hostile catches")

    for key in (
        "complete_moduli_classification", "physical_data_selected", "history_selected",
        "scale_selected", "Xmax_selected", "metric_changed", "kernel_changed",
    ):
        need(production[key] is False, f"forbidden promotion: {key}")

    with (HERE / "INVARIANT_ATLAS.tsv").open(encoding="utf-8", newline="") as handle:
        atlas = list(csv.DictReader(handle, delimiter="\t"))
    need(len(atlas) == 8, "atlas count")
    need({row["mode"] for row in atlas} == {"1", "2", "3", "4"}, "atlas modes")
    need({row["sign"] for row in atlas} == {"-1", "1"}, "atlas signs")
    volumes = [float(row["volume"]) for row in atlas]
    need(max(volumes) - min(volumes) < 2e-11, "volume mismatch")
    for sign in ("-1", "1"):
        rows = {int(row["mode"]): row for row in atlas if row["sign"] == sign}
        base = float(rows[1]["Q_R"])
        for mode in (2, 3, 4):
            need(abs(float(rows[mode]["Q_R"]) / base - mode ** 2) < 2e-12, "Q ratio")
    need(max(float(row["max_hamiltonian"]) for row in atlas) < 4e-15, "Hamiltonian")
    need(max(float(row["max_momentum"]) for row in atlas) < 2e-15, "momentum")
    need(all(float(row["min_signed_tau"]) > 0 for row in atlas), "tau sign")

    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = (HERE / "LAY_REPORT.md").read_text(encoding="utf-8")
    lay_flat = " ".join(lay.split())
    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    request = (HERE / "EXTERNAL_REVIEW_REQUEST.md").read_text(encoding="utf-8")
    for token in (
        "compare physical data, not conformal coordinates",
        "Q_R[\\psi_n]=n^2Q_R[\\psi_1]",
        "at least a countably infinite set",
        "not a complete quotient",
        "same physical datum",
        "metric, reciprocal kernel, angular cancellation",
    ):
        need(token.lower() in exact.lower(), f"exact guard missing: {token}")
    for token in (
        "some of the freedom is definitely real",
        "1, 4, 9, 16",
        "choose one universe",
        "metric and reciprocal kernel were not changed",
    ):
        need(token.lower() in lay_flat.lower(), f"lay guard missing: {token}")
    for token in (
        "same physical initial datum",
        "homothety-neutral invariant",
        "does not prove\nthat every distinct profile",
        "fresh external adversarial review",
    ):
        need(token in prereg, f"prereg guard missing: {token}")
    for verdict in (
        "G320_ACCEPTED__GENUINE_INITIAL_GEOMETRY_FREEDOM_UPHELD",
        "G320_REPAIRABLE_DEFECTS__BOUNDED_LANDING_RETAINED",
        "G320_SCIENTIFIC_LANDING_REFUTED",
        "G320_REVIEW_INCOMPLETE",
    ):
        need(verdict in request, f"external verdict missing: {verdict}")

    response = (HERE / "EXTERNAL_REVIEW_RESPONSE.md").read_text(encoding="utf-8")
    cli_final = (HERE / "EXTERNAL_REVIEW_CLI_FINAL.md").read_text(encoding="utf-8")
    transcript = (HERE / "EXTERNAL_REVIEW_TRANSCRIPT.txt").read_text(encoding="utf-8")
    transmission = (HERE / "EXTERNAL_REVIEW_TRANSMISSION.md").read_text(encoding="utf-8")
    accepted = "G320_ACCEPTED__GENUINE_INITIAL_GEOMETRY_FREEDOM_UPHELD"
    need(response.rstrip().endswith(accepted), "external response does not end with acceptance")
    for label, body in (("CLI final", cli_final), ("transcript", transcript),
                        ("transmission", transmission)):
        need(accepted in body, f"external acceptance absent from {label}")
    need("Manifest payload rows checked: `32`" in response, "external authentication absent")
    need("matched the sealed package byte-for-byte" in response, "external replay identity absent")
    for artifact in (
        "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json",
        "PACKAGE_VERIFICATION_RESULT.json", "INVARIANT_ATLAS.tsv",
    ):
        need(artifact in response, f"external replay artifact absent: {artifact}")
    need("No scientific defect survived" in response, "external scientific finding absent")
    need("not claim a complete quotient" in response, "external scope boundary absent")
    need("260aac5813195eeaba3fefe10943313ed192e2dfc869d4cd6572ff991be39dfd"
         in transmission, "scope seal absent")
    need("db9e81c81fe1706c0ff7759367af15d5ee632c9bf41b018eab49d38d64e83c45"
         in transmission, "manifest seal absent")

    independent_source = (HERE / "verify_independent.py").read_text(encoding="utf-8")
    need("import derive_physical_quotient" not in independent_source, "independent import")
    need("DERIVATION_RESULT.json" not in independent_source, "independent output read")

    allowed_modules = {
        "ast", "csv", "fractions", "hashlib", "json", "math", "pathlib", "shutil", "tempfile"
    }
    for script in (
        "derive_physical_quotient.py", "verify_independent.py", "run_catch_proofs.py",
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
        need(protected not in source_scope, f"protected source: {protected}")

    result = {
        "status": "PASS_EXTERNALLY_ACCEPTED",
        "landing": LANDING,
        "production_assertions": production["assertion_count"],
        "independent_assertions": independent["assertion_count"],
        "hostile_catches": f"{hostile['caught_count']}/{hostile['mutation_count']}",
        "atlas_rows": len(atlas),
        "external_review": "ACCEPTED",
    }
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("G320 package verification PASS_EXTERNALLY_ACCEPTED")
    print(f"production assertions: {result['production_assertions']}")
    print(f"independent assertions: {result['independent_assertions']}")
    print(f"hostile mutations caught: {result['hostile_catches']}")
    print(LANDING)


if __name__ == "__main__":
    main()
