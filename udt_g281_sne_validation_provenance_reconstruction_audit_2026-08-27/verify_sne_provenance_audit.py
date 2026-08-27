#!/usr/bin/env python3
"""Fail-closed verifier for the bounded G281 SNe provenance audit."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    source_scope = rows("SOURCE_SCOPE.tsv")
    source_manifest = rows("SOURCE_MANIFEST.tsv")
    census = rows("HISTORICAL_CLAIM_CENSUS.tsv")
    routes = rows("ROUTE_PROVENANCE_MATRIX.tsv")
    stale = rows("STALE_CLAIM_SCAN.tsv")
    status = rows("STATUS_LEDGER.tsv")

    scope_paths = [row["path"] for row in source_scope]
    manifest = {row["path"]: row["sha256"] for row in source_manifest}
    protected_fragments = (
        "udt_native_onshell_timelive_reset_owner_audit_2026-08-10",
        "udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12",
        "udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12",
        "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02",
    )
    source_hashes = {
        path: (ROOT / path).is_file() and sha256(ROOT / path) == manifest.get(path)
        for path in scope_paths
    }

    allowed_classes = {
        "NATIVE_PREDICTION",
        "NATIVE_CONDITIONAL_EVALUATION",
        "EMPIRICAL_RECONSTRUCTION",
        "EMPIRICAL_CALIBRATION",
        "REGRESSION_OR_COMPATIBILITY_CONTROL",
        "IMPORTED_PHYSICS_COMPARISON",
        "SCAFFOLDED_OR_OVERCLAIMED",
        "SUPERSEDED_OR_REPAIRED",
    }
    census_ids = [row["id"] for row in census]
    route_names = [row["route"] for row in routes]
    history_gate = "history_metric_owned_or_physically_selected_and_fixed_before_SNe"
    g79_rows = [row for row in routes if row["route"] == "G79_same_geometry_control"]
    route_native_predictions = [
        row["route"] for row in routes if row["maximum_class"] == "NATIVE_PREDICTION"
    ]

    canonical = (ROOT / "udt_canonical_geometry.md").read_text()
    n2 = (ROOT / "luminosity_distance_n2_optics_results.md").read_text()
    g94 = (
        ROOT / "udt_native_flux_luminosity_law_ownership_audit_2026-08-15/AUDIT_REPORT.md"
    ).read_text()
    g236 = (
        ROOT / "udt_g236_dual_sne_relational_state_reconstruction_2026-08-23/AUDIT_REPORT.md"
    ).read_text()
    g279 = (
        ROOT / "udt_g279_native_kernel_observational_interface_provenance_audit_2026-08-27/AUDIT_REPORT.md"
    ).read_text()
    g280 = (
        ROOT / "udt_g280_projective_position_optical_area_bridge_audit_2026-08-27/AUDIT_REPORT.md"
    ).read_text()
    required_outputs = (
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "EVIDENCE_GATES.md",
        "STATUS_LEDGER.tsv",
        "HISTORICAL_CLAIM_CENSUS.tsv",
        "ROUTE_PROVENANCE_MATRIX.tsv",
        "STALE_CLAIM_SCAN.tsv",
        "VERIFICATION_RESULT.json",
        "COMMANDS.md",
        "PREREGISTRATION_EXECUTION_NOTE.md",
        "verify_sne_provenance_audit.py",
        "verify_sne_provenance_independent.py",
        "verify_saved_lineage_outputs.py",
        "build_review_intake.py",
        "EXTERNAL_REVIEW_REQUEST.md",
        "EXTERNAL_REVIEW.md",
        "EXTERNAL_REVIEW_TRANSMISSION.md",
        "EXTERNAL_REPAIR_PREREGISTRATION.md",
        "REPAIR_RESULT.md",
        "EXTERNAL_REPAIR_FOLLOWUP_REQUEST.md",
    )
    audit_report = (PACKAGE / "AUDIT_REPORT.md").read_text()
    recorded_result = json.loads((PACKAGE / "VERIFICATION_RESULT.json").read_text())

    checks = {
        "scope_count_32": len(source_scope) == 32,
        "sealed_source_count_32": len(source_manifest) == 32,
        "manifest_matches_scope_exactly": set(manifest) == set(scope_paths),
        "all_source_hashes_match": bool(source_hashes) and all(source_hashes.values()),
        "protected_paths_excluded": not any(
            fragment in path for fragment in protected_fragments for path in scope_paths
        ),
        "census_count_24": len(census) == 24,
        "census_ids_exact": census_ids == [f"H{i:02d}" for i in range(1, 25)],
        "census_classes_valid": all(row["current_class"] in allowed_classes for row in census),
        "all_census_rows_have_controllers": all(row["controlling_evidence"] for row in census),
        "route_count_15": len(routes) == 15,
        "route_names_unique": len(route_names) == len(set(route_names)),
        "history_ownership_is_explicit_gate_1": all(history_gate in row for row in routes),
        "g79_fails_history_ownership_gate": (
            len(g79_rows) == 1
            and g79_rows[0][history_gate] == "NO"
            and g79_rows[0]["maximum_class"] == "NATIVE_CONDITIONAL_EVALUATION"
        ),
        "no_route_upgraded_to_native_prediction": not route_native_predictions,
        "stale_scan_nonempty": len(stale) >= 10,
        "status_lands_prediction_not_found": any(
            row["id"] == "S11" and row["status"] == "NOT_FOUND" for row in status
        ),
        "all_required_outputs_present": all((PACKAGE / name).is_file() for name in required_outputs),
        "audit_report_landing_exact": (
            "NO_COMPLETE_NATIVE_SNE_PREDICTION_IN_AUDITED_NONPROTECTED_LINEAGE" in audit_report
        ),
        "recorded_result_landing_exact": (
            recorded_result["landing"]
            == "NO_COMPLETE_NATIVE_SNE_PREDICTION_IN_AUDITED_NONPROTECTED_LINEAGE"
        ),
        "canonical_old_overclaim_present": "Canonical UDT beats" in canonical,
        "canonical_old_one_factor_present": "D_L(z) = r(z) \\cdot (1+z)" in canonical,
        "july_n2_correction_present": "ERROR" in n2 and "should be `r·e^{2φ}`" in n2,
        "g94_transfer_is_conditional": "CONDITIONAL" in g94 and "epsilon" in g94,
        "g236_calls_it_reconstruction": "RELATIONAL_STATE_CONCORDANCE_LEAD" in g236,
        "g236_import_caveat_retained": "IMPORTED_TRANSFER_CAVEATS_RETAINED" in g236,
        "g279_native_core_intact": "NATIVE_CORE_INTACT" in g279,
        "g279_observational_path_downstream": "observational path begins only afterward" in g279,
        "g280_same_state_different_area": (
            "SAME_COMPLETE_PROJECTIVE_PAIR_STATE_ADMITS_DIFFERENT_NATIVE_JACOBI_AREA" in g280
        ),
        "g280_area_not_phi_function": "OPTICAL_AREA_IS_NOT_A_FUNCTION_OF_PHI_OR_W5_STATE_ALONE" in g280,
    }
    if not all(checks.values()):
        raise AssertionError(
            json.dumps(
                {
                    "checks": checks,
                    "failed": [name for name, passed in checks.items() if not passed],
                    "route_native_predictions": route_native_predictions,
                    "source_hashes": source_hashes,
                },
                indent=2,
                sort_keys=True,
            )
        )

    result = {
        "audit": "G281_SNE_PROVENANCE_VERIFICATION",
        "status": "PASS",
        "landing": "NO_COMPLETE_NATIVE_SNE_PREDICTION_IN_AUDITED_NONPROTECTED_LINEAGE",
        "checks": checks,
        "counts": {
            "source_files_inspected": len(source_scope),
            "immutable_source_files": len(source_manifest),
            "historical_tiles": len(census),
            "route_classes": len(routes),
            "native_prediction_witnesses": len(route_native_predictions),
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
