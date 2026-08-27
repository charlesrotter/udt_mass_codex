#!/usr/bin/env python3
"""Fail-closed verifier for the bounded G282 package."""

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
    premises = rows("PREMISE_LEDGER.tsv")
    ownership = rows("OWNERSHIP_CENSUS.tsv")
    status = rows("STATUS_LEDGER.tsv")
    manifest = {row["path"]: row for row in source_manifest}
    scope_paths = [row["path"] for row in source_scope]
    source_hashes = {
        path: (
            (ROOT / path).is_file()
            and sha256(ROOT / path) == manifest[path]["sha256"]
            and str((ROOT / path).stat().st_size) == manifest[path]["bytes"]
        )
        for path in scope_paths
        if path in manifest
    }
    protected_fragments = (
        "udt_native_onshell_timelive_reset_owner_audit_2026-08-10",
        "udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12",
        "udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12",
        "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02",
    )
    derivation = json.loads((PACKAGE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((PACKAGE / "INDEPENDENT_VERIFICATION.json").read_text())
    catches = json.loads((PACKAGE / "CATCH_PROOF_RESULT.json").read_text())
    verification = json.loads((PACKAGE / "VERIFICATION_RESULT.json").read_text())
    report = (PACKAGE / "AUDIT_REPORT.md").read_text()
    exact = (PACKAGE / "EXACT_DERIVATION.md").read_text()
    required = (
        "MAP.md",
        "PREREGISTRATION.md",
        "PREMISE_LEDGER.tsv",
        "SOURCE_SCOPE.tsv",
        "SOURCE_MANIFEST.tsv",
        "OWNERSHIP_CENSUS.tsv",
        "STATUS_LEDGER.tsv",
        "EXACT_DERIVATION.md",
        "AUDIT_REPORT.md",
        "LAY_REPORT.md",
        "EVIDENCE_GATES.md",
        "DERIVATION_RESULT.json",
        "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json",
        "VERIFICATION_RESULT.json",
        "derive_minimal_law_type.py",
        "verify_independent.py",
        "run_catch_proofs.py",
        "verify_preregistration.py",
        "verify_package.py",
        "COMMANDS.md",
    )
    checks = {
        "source_count_18": len(source_scope) == 18 and len(source_manifest) == 18,
        "manifest_matches_scope_exactly": set(manifest) == set(scope_paths),
        "all_source_hashes_and_sizes_match": len(source_hashes) == 18 and all(source_hashes.values()),
        "protected_paths_excluded": not any(
            fragment in path for fragment in protected_fragments for path in scope_paths
        ),
        "premise_count_17": len(premises) == 17,
        "ownership_count_14": len(ownership) == 14,
        "no_owned_joint_law_in_census": all(row["joint_history_law"] == "NO" for row in ownership),
        "status_owned_law_not_found": any(
            row["id"] == "S07" and row["status"] == "NOT_FOUND" for row in status
        ),
        "derivation_passed_11_checks": (
            derivation["status"] == "PASS"
            and len(derivation["checks"]) == 11
            and all(derivation["checks"].values())
        ),
        "independent_passed_3584_assertions": (
            independent["status"] == "PASS"
            and independent["cases"] == 512
            and independent["assertions"] == 3584
            and all(independent["checks"].values())
        ),
        "hostile_catches_7_of_7": (
            catches["status"] == "PASS"
            and catches["caught_count"] == catches["mutation_count"] == 7
            and all(catches["caught"].values())
        ),
        "minimum_information_types_retained": len(
            derivation["minimum_missing_information_types"]
        ) == 3,
        "no_unique_PDE_promotion": (
            "second_order_metric_PDE" in derivation["not_uniquely_implied"]
            and "DIFFERENTIAL_REPRESENTATION_NOT_UNIQUELY_SELECTED" in report
            and "does not derive\nthat representation uniquely" in exact
        ),
        "no_imports_or_observations": (
            derivation["field_equations_adopted"] == 0
            and derivation["fitted_coefficients"] == 0
            and derivation["observational_outcomes_used"] == 0
            and not derivation["Xmax_used"]
            and not any(verification["premise_imports"].values())
        ),
        "all_required_files_present": all((PACKAGE / name).is_file() for name in required),
        "landing_exact": (
            derivation["landing"]
            == verification["landing"]
            == "NO_OWNED_JOINT_HISTORY_LAW__NEIGHBOR_RELATION_CURVATURE_CONSTRAINT_REQUIRED"
        ),
    }
    if not all(checks.values()):
        raise AssertionError(
            json.dumps(
                {
                    "checks": checks,
                    "failed": [name for name, passed in checks.items() if not passed],
                    "source_hashes": source_hashes,
                },
                indent=2,
                sort_keys=True,
            )
        )
    print(
        json.dumps(
            {
                "audit": "G282_PACKAGE_VERIFICATION",
                "status": "PASS",
                "landing": derivation["landing"],
                "checks": checks,
                "counts": verification["counts"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
