#!/usr/bin/env python3
"""No-write integrity and semantic verifier for the bounded G307 package."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LANDING = (
    "SUPPLIED_DIRECTED_GERM_SELECTS_ONE_MEMBER_PER_CHIRAL_FAMILY"
    "__SIGNED_TRANSVERSE_SCREEN_GERM_SELECTS_ONE_MEMBER_CONDITIONALLY"
    "__ACTIVE_PREMISES_POPULATE_NEITHER__PHYSICAL_MEMBER_REMAINS_OPEN"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_source(relative: Path) -> Path:
    candidates = (ROOT / relative, ROOT / "frozen_sources" / relative)
    matches = [path for path in candidates if path.is_file()]
    assert len(matches) == 1, (
        f"source resolution must be unique for {relative}: "
        f"found {[str(path) for path in matches]}"
    )
    return matches[0]


def main() -> None:
    required = (
        "MAP.md", "PREREGISTRATION.md", "PREREGISTRATION_ANCESTRY.md",
        "PREMISE_LEDGER.tsv", "SOURCE_SCOPE.tsv", "SOURCE_MANIFEST.tsv",
        "COMPLETENESS_MAP.md", "derive_directed_member_reconstruction.py",
        "verify_directed_member_independent.py", "run_catch_proofs.py",
        "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json",
        "CATCH_PROOF_RESULT.json", "MEMBER_CENSUS.tsv", "STATUS_LEDGER.tsv",
        "EXACT_DERIVATION.md", "AUDIT_REPORT.md", "LAY_REPORT.md",
        "EVIDENCE_GATES.md", "RUN_RECORD.md", "COMMANDS.md",
        "VERIFICATION_RESULT.json", "verify_package.py",
    )
    for name in required:
        assert (HERE / name).is_file(), name

    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8")
    )
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    verification = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))

    assert derivation["status"] == "PASS"
    assert derivation["landing_candidate"] == 2
    assert derivation["landing"] == LANDING
    assert derivation["production_assertions"] == 1806
    assert derivation["exact_cases"] == 36
    assert derivation["directed_germ_member_count"] == 2
    assert derivation["members_per_chirality"] == 1
    assert derivation["path_only_member_count"] == 2
    assert derivation["signed_transverse_screen_member_count"] == 1
    assert derivation["screen_twist_signs"] == [-1, 1]
    assert derivation["lawful_query_population_selected"] is False
    assert derivation["physical_member_selected"] is False
    assert derivation["metric_and_kernel_changed"] is False

    assert independent["status"] == "PASS"
    assert independent["implementation"] == "oriented_two_plane_outer_product_no_production_import"
    assert independent["imports_production_code"] is False
    assert independent["sample_cases"] == 1000
    assert independent["independent_checks"] == 17000
    assert independent["maximum_error"] < 2e-10
    assert independent["directed_germ_member_count"] == 2
    assert independent["signed_screen_member_count"] == 1
    assert independent["path_only_distinguishes_chirality"] is False

    assert catches["status"] == "PASS"
    assert catches["baseline_valid"] is True
    assert catches["hostile_cases"] == 14
    assert catches["direct_mutations"] == 14
    assert all(record["caught"] for record in catches["records"])
    assert verification["landing"] == LANDING
    assert verification["status"] == "INTERNAL_GATES_PASS_EXTERNAL_PENDING"
    assert verification["premise_audit"] == "PASS"
    assert verification["repository_regression"] == "199_passed_1_expected_xfail"

    expected_census = (
        ("round_metric_only", "two_S2_families", "no_member"),
        ("supplied_point", "two_S2_families", "no_direction"),
        ("supplied_point_and_ordered_unit_tangent", "two_members", "one_per_chirality"),
        ("complete_one_dimensional_route_and_metric_frame_carry", "two_members", "same_route"),
        ("supplied_oriented_signed_transverse_screen_first_jet", "one_member", "conditional_reconstruction"),
        ("active_premise_owned_lawful_query_population", "zero_selected", "open"),
    )
    with (HERE / "MEMBER_CENSUS.tsv").open(encoding="utf-8", newline="") as handle:
        rows = tuple(
            (row["data_level"], row["remaining_geometric_members"], row["ownership"])
            for row in csv.DictReader(handle, delimiter="\t")
        )
    assert rows == expected_census

    for name in ("EXACT_DERIVATION.md", "AUDIT_REPORT.md"):
        assert LANDING in (HERE / name).read_text(encoding="utf-8").replace("\n", "")

    forbidden = (
        "8_25", "udt_native_onshell_timelive_reset_owner_audit",
        "udt_pair_regime_flow_reciprocal_orchestra_amplification",
        "udt_sne_xmax_G88_am_radial_compatibility_atlas",
        "udt_kernel_plane_global_curvature_holonomy_atlas",
    )
    source_rows = 0
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            relative = Path(row["path"])
            assert not any(token in str(relative) for token in forbidden)
            assert sha256(resolve_source(relative)) == row["sha256"], relative
            source_rows += 1
    assert source_rows == 8

    print(json.dumps({
        "status": "PASS",
        "landing": LANDING,
        "required_files": len(required),
        "source_hashes_verified": source_rows,
        "production_assertions": derivation["production_assertions"],
        "independent_checks": independent["independent_checks"],
        "hostile_catches": catches["hostile_cases"],
        "metric_and_kernel_changed": derivation["metric_and_kernel_changed"],
        "external_review": "PENDING",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
