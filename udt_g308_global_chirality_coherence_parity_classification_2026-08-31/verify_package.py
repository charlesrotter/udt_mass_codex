#!/usr/bin/env python3
"""No-write integrity and semantic verifier for G308."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LANDING = (
    "BOTH_G307_CHIRAL_MEMBERS_EXTEND_GLOBALLY_AND_CAUSALLY_ON_G305"
    "__CONNECTED_REGULAR_CARRY_FORBIDS_LOCAL_CHIRALITY_SWITCHING"
    "__TRANSVERSE_ORIENTATION_REVERSING_ISOMETRY_EXCHANGES_THE_TWO_SECTORS"
    "__METRIC_ONLY_PHYSICAL_SELECTION_REMAINS_OPEN"
)


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def resolve_source(root: Path, relative: Path) -> Path:
    candidates = (root / relative, root / "frozen_sources" / relative)
    matches = [path for path in candidates if path.is_file()]
    assert len(matches) == 1, (
        f"source resolution must be unique for {relative}: "
        f"found {[str(path) for path in matches]}"
    )
    return matches[0]


def main():
    required = (
        "MAP.md", "PONDER.md", "PREREGISTRATION.md", "PREREGISTRATION_ANCESTRY.md",
        "PREMISE_LEDGER.tsv", "PREMISE_AUDIT_RESULT.json", "COMPLETENESS_MAP.md",
        "SOURCE_SCOPE.tsv", "SOURCE_MANIFEST.tsv", "derive_global_chirality_coherence.py",
        "verify_global_chirality_independent.py", "run_catch_proofs.py", "verify_package.py",
        "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json",
        "COHERENCE_CENSUS.tsv", "STATUS_LEDGER.tsv", "VERIFICATION_RESULT.json",
        "EXACT_DERIVATION.md", "AUDIT_REPORT.md", "LAY_REPORT.md", "EVIDENCE_GATES.md",
        "RUN_RECORD.md", "COMMANDS.md", "EXTERNAL_REVIEW_RESPONSE.md",
        "EXTERNAL_REVIEW_TRANSCRIPT.txt", "REPAIR_PREREGISTRATION.md",
        "REPAIR_ANCESTRY.md", "REPAIR_REPORT.md",
        "verify_chirality_hodge_independent.py", "HODGE_INDEPENDENT_VERIFICATION.json",
        "verify_repair_portability.py", "PORTABILITY_VERIFICATION_RESULT.json",
        "EXTERNAL_REPAIR_FOLLOWUP_REQUEST.md",
    )
    for name in required:
        assert (HERE / name).is_file(), name

    derivation = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    catches = json.loads((HERE / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    hodge = json.loads((HERE / "HODGE_INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    portability = json.loads((HERE / "PORTABILITY_VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    verification = json.loads((HERE / "VERIFICATION_RESULT.json").read_text(encoding="utf-8"))
    premise = json.loads((HERE / "PREMISE_AUDIT_RESULT.json").read_text(encoding="utf-8"))

    assert derivation["status"] == "PASS"
    assert derivation["landing_candidate"] == "B"
    assert derivation["landing"] == LANDING
    assert derivation["production_assertions"] == 11526
    assert derivation["frame_cases"] == 36
    assert derivation["global_point_cases"] == 216
    assert derivation["both_global_smooth_nowhere_zero"] is True
    assert derivation["both_spatial_orbits_complete_closed"] is True
    assert derivation["normalized_fields_time_parallel"] is True
    assert derivation["spatial_hopf_fibers_automatically_spacetime_geodesic"] is False
    assert derivation["reflection_fixes_directed_route_plane"] is True
    assert derivation["reflection_reverses_transverse_orientation"] is True
    assert derivation["full_O4_exchanges_chirality"] is True
    assert derivation["SO4_exchanges_chirality"] is False
    assert derivation["pair_reversal_changes_chirality"] is False
    assert derivation["connected_regular_carry_allows_local_chirality_switch"] is False
    assert derivation["metric_or_causal_cone_changed"] is False
    assert derivation["physical_member_selected"] is False
    assert derivation["metric_and_kernel_changed"] is False

    assert independent["status"] == "PASS"
    assert independent["imports_production_code"] is False
    assert independent["independent_checks"] == 79200
    assert independent["maximum_error"] < 5e-13
    assert independent["both_global_fields_verified"] is True
    assert independent["det_minus_one_exchange_verified"] is True
    assert independent["det_plus_one_chirality_preservation_verified"] is True
    assert independent["pair_reversal_chirality_preservation_verified"] is True
    assert independent["connected_switch_degeneracy_verified"] is True
    assert independent["causal_quadratic_form_preserved"] is True

    assert hodge["status"] == "PASS"
    assert hodge["imports_production_code"] is False
    assert hodge["uses_outer_product_candidate_construction"] is False
    assert hodge["independent_checks"] == 121600
    assert hodge["maximum_error"] < 5e-13
    assert hodge["both_global_fields_verified"] is True
    assert hodge["hodge_chirality_split_verified"] is True
    assert hodge["O4_exchange_verified"] is True
    assert hodge["SO4_nonexchange_verified"] is True
    assert hodge["pair_reversal_preserves_chirality"] is True
    assert hodge["connected_regular_switch_excluded"] is True
    assert hodge["normalized_time_carry_verified"] is True
    assert hodge["slice_vs_spacetime_geodesic_distinguished"] is True
    assert hodge["causal_equivalence_verified"] is True
    assert hodge["metric_and_kernel_changed"] is False

    assert portability["status"] == "PASS"
    assert portability["repository_layout_verified"] is True
    assert portability["sealed_layout_verified"] is True
    assert portability["missing_layout_rejected"] is True
    assert portability["ambiguous_layout_rejected"] is True

    assert catches["status"] == "PASS"
    assert catches["hostile_cases"] == 22
    assert catches["direct_mathematical_mutations"] == 8
    assert catches["semantic_result_mutations"] == 14
    assert all(record["caught"] for record in catches["records"])
    assert verification["landing"] == LANDING
    assert verification["production_assertions"] == 11526
    assert verification["constructive_randomized_checks"] == 79200
    assert verification["hodge_independent_checks"] == 121600
    assert verification["external_review"] == "G308_REPAIRABLE_DEFECTS__NO_BOUNDED_SCIENTIFIC_DEFECT"
    assert verification["repair_status"] == "R1_R4_INTERNAL_PASS__EXTERNAL_FOLLOWUP_PENDING"
    assert verification["sealed_replay"] == "PASS__NO_SYMLINKS__NO_MANUAL_STAGING__6_OF_6_OUTCOMES_BYTE_IDENTICAL"
    assert verification["repository_regression"] == "PASS_POST_REPAIR__199_PASSED__1_EXPECTED_XFAIL__137_46_SECONDS"
    assert verification["status"] == "EXTERNALLY_REVIEWED__REPAIRS_INTERNAL_PASS__FOLLOWUP_PENDING"
    assert premise["status"] == "PASS"
    assert premise["registry_rows"] == 289

    expected_census = (
        ("round_G305_metric_only", "two_continuous_chiral_families", "no_member"),
        ("one_supplied_directed_germ", "two_global_members", "one_per_chirality"),
        ("connected_smooth_regular_Hopf_carry", "one_constant_chirality_label_per_component", "no_sign_preference"),
        ("unoriented_metric_full_O4_equivalence", "one_mirror_orbit_with_two_representatives", "orientation_blind_equivalence"),
        ("oriented_metric_SO4_equivalence", "two_chiral_sectors", "degenerate_not_selected"),
        ("supplied_signed_transverse_screen", "one_member", "conditional_reconstruction"),
        ("active_physical_population", "zero_selected", "open"),
    )
    with (HERE / "COHERENCE_CENSUS.tsv").open(encoding="utf-8", newline="") as handle:
        rows = tuple(
            (row["data_level"], row["global_geometric_status"], row["ownership"])
            for row in csv.DictReader(handle, delimiter="\t")
        )
    assert rows == expected_census

    source_rows = 0
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            relative = Path(row["path"])
            assert digest(resolve_source(ROOT, relative)) == row["sha256"], relative
            source_rows += 1
    assert source_rows == 9

    for name in ("EXACT_DERIVATION.md", "AUDIT_REPORT.md"):
        assert LANDING in (HERE / name).read_text(encoding="utf-8").replace("\n", "")

    print(json.dumps({
        "status": "PASS",
        "landing": LANDING,
        "required_files": len(required),
        "source_hashes_verified": source_rows,
        "production_assertions": derivation["production_assertions"],
        "independent_checks": independent["independent_checks"],
        "hodge_independent_checks": hodge["independent_checks"],
        "hostile_catches": catches["hostile_cases"],
        "portability": portability["status"],
        "metric_and_kernel_changed": derivation["metric_and_kernel_changed"],
        "external_review": "PENDING",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
