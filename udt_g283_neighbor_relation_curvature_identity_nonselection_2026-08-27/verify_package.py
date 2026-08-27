#!/usr/bin/env python3
"""Fail-closed package verifier for the bounded G283 result."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
LANDING = "ARBITRARY_SMOOTH_TIDAL_HISTORY_SURVIVES_OWNED_IDENTITIES__VALUE_LAW_STILL_MISSING"


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    scope = rows("SOURCE_SCOPE.tsv")
    manifest_rows = rows("SOURCE_MANIFEST.tsv")
    manifest = {row["path"]: row for row in manifest_rows}
    premises = rows("PREMISE_LEDGER.tsv")
    census = rows("IDENTITY_CENSUS.tsv")
    status = rows("STATUS_LEDGER.tsv")
    derivation = json.loads((PACKAGE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((PACKAGE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    verification = json.loads((PACKAGE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    report = (PACKAGE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (PACKAGE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    required = (
        "MAP.md",
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_SCOPE.tsv",
        "SOURCE_MANIFEST.tsv",
        "IDENTITY_CENSUS.tsv",
        "STATUS_LEDGER.tsv",
        "EXACT_DERIVATION.md",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "EVIDENCE_GATES.md",
        "COMMANDS.md",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "INDEPENDENT_CASES.tsv",
        "CATCH_PROOF_RESULT.json",
        "VERIFICATION_RESULT.json",
        "verify_preregistration.py",
        "derive_identity_nonselection.py",
        "verify_independent.py",
        "run_catch_proofs.py",
        "verify_package.py",
    )
    protected = (
        "udt_native_onshell_timelive_reset_owner_audit_2026-08-10",
        "udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12",
        "udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12",
        "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02",
    )
    checks = {
        "all_required_files_present": all((PACKAGE / name).is_file() for name in required),
        "source_count_12": len(scope) == len(manifest_rows) == 12,
        "source_scope_manifest_exact": set(row["path"] for row in scope) == set(manifest),
        "all_source_hashes_and_sizes_exact": all(
            (ROOT / path).is_file()
            and sha256(ROOT / path) == manifest[path]["sha256"]
            and str((ROOT / path).stat().st_size) == manifest[path]["bytes"]
            for path in manifest
        ),
        "protected_sources_excluded": not any(
            fragment in path for fragment in protected for path in manifest
        ),
        "premise_rows_17": len(premises) == 17,
        "identity_census_rows_11": len(census) == 11,
        "no_identity_selects_T_values": all(row["selects_T_values"] == "NO" for row in census),
        "no_registered_metric_rejected": all(row["rejects_registered_metric_family"] == "NO" for row in census),
        "derivation_12_of_12": (
            derivation["status"] == "PASS"
            and len(derivation["checks"]) == 12
            and all(derivation["checks"].values())
        ),
        "three_general_and_two_tracefree_functions": (
            len(derivation["arbitrary_functions_retained"]) == 3
            and len(derivation["tracefree_control_functions_retained"]) == 2
        ),
        "independent_128_cases_207360_assertions": (
            independent["status"] == "PASS"
            and independent["exact_cases"] == 128
            and independent["exact_assertions"] == 207360
            and independent["numerical_cases"] == 64
            and independent["different_area_cases"] == 64
            and all(independent["checks"].values())
        ),
        "claim_schema_catches_7_of_7": (
            catches["status"] == "PASS"
            and catches["caught_count"] == catches["mutation_count"] == 7
            and catches["certification_scope"]
            == "in_memory_boolean_claim_schema_only__not_artifact_level_mutation_replay"
            and all(catches["caught"].values())
        ),
        "landing_exact": (
            derivation["landing"] == verification["landing"] == LANDING
            and "ARBITRARY_SMOOTH_TIDAL_HISTORY_SURVIVES_OWNED_IDENTITIES" in report
            and "__VALUE_LAW_STILL_MISSING" in report
        ),
        "three_law_homes_retained": all(
            token in exact
            for token in (
                "metric two-jet",
                "first\ntransverse derivative of the connection",
                "Jacobi and relation-network home",
            )
        ),
        "no_imports_or_outcomes": (
            derivation["field_equations_adopted"] == 0
            and derivation["observational_outcomes_used"] == 0
            and derivation["fitted_coefficients"] == 0
            and not derivation["Xmax_used"]
            and not any(verification["premise_imports"].values())
        ),
        "external_review_pending": any(
            row["id"] == "S11" and row["status"] == "PENDING" for row in status
        ),
    }
    if not all(checks.values()):
        raise AssertionError({name: value for name, value in checks.items() if not value})
    print(
        json.dumps(
            {
                "audit": "G283_PACKAGE_VERIFICATION",
                "status": "PASS",
                "grade": verification["grade"],
                "landing": LANDING,
                "counts": verification["counts"],
                "checks": checks,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
