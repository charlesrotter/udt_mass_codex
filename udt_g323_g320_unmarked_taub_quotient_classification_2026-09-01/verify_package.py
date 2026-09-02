#!/usr/bin/env python3
"""Aggregate no-write-input verifier for the internally verified G323 package."""

import ast
import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
LANDING = (
    "REGISTERED_G320_PROFILES_EMBED_AS_CAUCHY_GRAPHS_IN_ONE_LOCAL_RICCI_FLAT_"
    "TAUB_FORM__INTEGER_MODES_HAVE_STRICTLY_DISTINCT_COMPACT_LATTICE_MODULI_"
    "AND_THUS_DISTINCT_UNMARKED_QUOTIENTS__OPPOSITE_K_SIGNS_ARE_ONE_"
    "TIME_UNORIENTED_METRIC_WITH_OPPOSITE_TIME_ORIENTATIONS__NO_OCCUPANCY_SELECTION"
)
REQUIRED = (
    "MAP.md", "PREMISE_LEDGER.tsv", "COMPLETENESS_MAP.md", "PREREGISTRATION.md",
    "PREREGISTRATION_ANCESTRY.md", "SOURCE_SCOPE.tsv", "REPLAY_COMMANDS.txt",
    "derive_unmarked_quotients.py", "verify_independent.py", "run_catch_proofs.py",
    "verify_package.py", "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json", "QUOTIENT_ATLAS.tsv", "INDEPENDENT_FAILURE_AND_REPAIR.md",
    "EXACT_DERIVATION.md", "LAY_REPORT.md", "STATUS_LEDGER.tsv", "EVIDENCE_GATES.md",
    "AUDIT_REPORT.md", "RUN_RECORD.md",
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
    need(production["assertion_count"] >= 78, "production assertion floor")
    for key in (
        "ambient_ricci_flat_exact", "complete_data_embedding_pass",
        "profiles_are_local_refoliations", "primitive_period_formula_pass",
        "mode_period_strictly_increasing", "n1_n2_unmarked_compact_quotients_distinct",
        "opposite_K_same_time_unoriented_metric", "opposite_K_time_orientations_distinct",
    ):
        need(production[key] is True, f"production gate absent: {key}")
    for key in (
        "physical_occupancy_selected", "unique_universe_selected", "physical_scale_selected",
        "Xmax_selected", "metric_changed", "kernel_changed", "angular_cancellation_changed",
    ):
        need(production[key] is False, f"forbidden promotion: {key}")
    need(production["max_pullback_error"] < 2e-11, "production pullback")
    need(production["max_extrinsic_error"] < 2e-11, "production extrinsic")
    need(production["max_curvature_join_error"] < 2e-11, "production curvature join")

    need(independent["status"] == "PASS", "independent status")
    need(independent["assertion_count"] >= 33, "independent assertion floor")
    need(independent["production_imported"] is False, "independent production import")
    need(independent["production_result_read"] is False, "independent production read")
    need(independent["complete_embedding_upheld"] is True, "independent embedding")
    need(independent["strict_mode_modulus_upheld"] is True, "independent mode modulus")
    need(independent["local_isometry_and_global_modulus_upheld"] is True,
         "independent local/global split")
    need(independent["max_pullback_error"] < 5e-10, "independent pullback")
    need(independent["max_extrinsic_error"] < 5e-10, "independent extrinsic")
    need(hostile["status"] == "PASS", "hostile status")
    need(hostile["caught_count"] == hostile["mutation_count"] >= 13, "hostile catches")

    with (HERE / "QUOTIENT_ATLAS.tsv").open(encoding="utf-8", newline="") as handle:
        atlas = list(csv.DictReader(handle, delimiter="\t"))
    need(len(atlas) == 8, "atlas row count")
    need({row["mode"] for row in atlas} == {"1", "2", "3", "4"}, "atlas modes")
    need({row["sign"] for row in atlas} == {"-1", "1"}, "atlas signs")
    for sign in ("-1", "1"):
        rows = sorted((row for row in atlas if row["sign"] == sign), key=lambda row: int(row["mode"]))
        need(all(float(b["L_X"]) > float(a["L_X"]) for a, b in zip(rows, rows[1:])),
             f"period monotonic sign={sign}")
    for mode in ("1", "2", "3", "4"):
        rows = [row for row in atlas if row["mode"] == mode]
        need(abs(float(rows[0]["L_X"]) - float(rows[1]["L_X"])) < 2e-13,
             f"sign period mode={mode}")

    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    lay = " ".join((HERE / "LAY_REPORT.md").read_text(encoding="utf-8").split())
    prereg = (HERE / "PREREGISTRATION.md").read_text(encoding="utf-8")
    failure = (HERE / "INDEPENDENT_FAILURE_AND_REPAIR.md").read_text(encoding="utf-8")
    for token in (
        "The common local spacetime", "Exact embedding of the complete data",
        "The forced global quotient period", "L_X(n+1)>L_X(n)",
        "same unmarked metric spacetime", "G322's imported-theorem ownership",
        "metric/kernel/angular sector are\nunchanged",
    ):
        need(token in exact, f"exact guard missing: {token}")
    for token in (
        "same Ricci-flat spacetime geometry", "closure number is strictly different",
        "same underlying spacetime with its direction of time reversed",
        "does not choose which compact quotient Nature occupies",
        "does not alter the UDT metric, reciprocal kernel, angular cancellation",
    ):
        need(token in lay, f"lay guard missing: {token}")
    for token in (
        "PREREGISTERED_CONFIRMATION_AFTER_EXPLORATORY_WHITEBOARD",
        "Candidate common ambient metric", "primitive `X` period",
        "Possible landings", "may not select physical data",
    ):
        need(token.lower() in prereg.lower(), f"prereg guard missing: {token}")
    for token in (
        "first independent run failed closed", "1.274324063161e-06",
        "did not relax a tolerance", "No scientific landing",
    ):
        need(token in failure, f"repair record missing: {token}")

    independent_source = (HERE / "verify_independent.py").read_text(encoding="utf-8")
    need("import derive_unmarked_quotients" not in independent_source, "independent imports production")
    need("DERIVATION_RESULT.json" not in independent_source, "independent reads production")
    allowed = {"ast", "csv", "fractions", "json", "math", "pathlib"}
    for script in (
        "derive_unmarked_quotients.py", "verify_independent.py", "run_catch_proofs.py",
        "verify_package.py",
    ):
        tree = ast.parse((HERE / script).read_text(encoding="utf-8"), filename=script)
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        need(imported <= allowed, f"unregistered dependency {script}: {sorted(imported - allowed)}")

    source_scope = (HERE / "SOURCE_SCOPE.tsv").read_text(encoding="utf-8")
    for protected in (
        "udt_native_onshell_timelive_reset_owner_audit_2026-08-10",
        "udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12",
        "udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12",
        "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02",
    ):
        need(protected not in source_scope, f"protected source named: {protected}")

    result = {
        "schema": "udt-g323-package-verification-v1",
        "status": "PASS_INTERNALLY_VERIFIED_PENDING_EXTERNAL_REVIEW",
        "landing": LANDING,
        "production_assertions": production["assertion_count"],
        "independent_assertions": independent["assertion_count"],
        "hostile_catches": f"{hostile['caught_count']}/{hostile['mutation_count']}",
        "atlas_rows": len(atlas),
        "external_review": "PENDING",
    }
    (HERE / "PACKAGE_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("G323 package verification PASS_INTERNALLY_VERIFIED_PENDING_EXTERNAL_REVIEW")
    print(f"production assertions: {result['production_assertions']}")
    print(f"independent assertions: {result['independent_assertions']}")
    print(f"hostile mutations caught: {result['hostile_catches']}")
    print(LANDING)


if __name__ == "__main__":
    main()
