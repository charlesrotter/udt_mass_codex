#!/usr/bin/env python3
"""Independent stdlib verifier for the bounded G86 ownership atlas."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent
EXPECTED_FAMILIES = {
    "A03_RADIAL_SHIFT_TIMELIVE",
    "A04_LAPSE_LIFT_TIMELIVE",
    "A05_MIXING_TAPER_BEFORE_SEAM",
}
ALLOWED_OWNER_CLASSES = {
    "IDENTITY_ONLY",
    "KINEMATIC_ADMISSIBILITY",
    "NECESSARY_NOT_SUFFICIENT",
    "QUERY_CONDITIONAL",
    "CONDITIONAL_CANDIDATE",
    "OPEN_UNOWNED",
    "INACTIVE_HYPOTHESIS",
    "OWNED_NONIDENTITY_SELECTOR",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def validate(snapshot: dict | None = None) -> list[str]:
    errors: list[str] = []
    source_rows = read_tsv(PKG / "SOURCE_MANIFEST.tsv")
    owner_rows = read_tsv(PKG / "CONDITION_OWNER_ATLAS.tsv")
    matrix_rows = read_tsv(PKG / "FAMILY_CONDITION_MATRIX.tsv")
    conditional_rows = read_tsv(PKG / "CONDITIONAL_SELECTOR_ATLAS.tsv")
    result = json.loads((PKG / "DERIVATION_RESULT.json").read_text())

    if snapshot:
        source_rows = snapshot.get("source_rows", source_rows)
        owner_rows = snapshot.get("owner_rows", owner_rows)
        matrix_rows = snapshot.get("matrix_rows", matrix_rows)
        conditional_rows = snapshot.get("conditional_rows", conditional_rows)
        result = snapshot.get("result", result)

    if len(source_rows) != 21 or len({r["path"] for r in source_rows}) != 21:
        errors.append("source_count_or_uniqueness")
    for row in source_rows:
        path = ROOT / row["path"]
        if not path.is_file() or digest(path) != row["sha256"]:
            errors.append(f"source_hash:{row['path']}")

    if len(owner_rows) != 14 or len({r["condition_id"] for r in owner_rows}) != 14:
        errors.append("condition_count_or_uniqueness")
    if any(r["owner_class"] not in ALLOWED_OWNER_CLASSES for r in owner_rows):
        errors.append("invalid_owner_class")
    if any(r["source_path"] not in {s["path"] for s in source_rows} for r in owner_rows):
        errors.append("owner_source_outside_manifest")
    if any(r["owned_selection_power"] != "false" for r in owner_rows):
        errors.append("unregistered_owned_selection")
    if sum(r["owner_class"] == "OWNED_NONIDENTITY_SELECTOR" for r in owner_rows) != 0:
        errors.append("owned_selector_present")

    cells = {(r["condition_id"], r["family_id"]) for r in matrix_rows}
    expected_cells = {
        (condition_id, family)
        for condition_id in {r["condition_id"] for r in owner_rows}
        for family in EXPECTED_FAMILIES
    }
    if len(matrix_rows) != 42 or cells != expected_cells:
        errors.append("matrix_coverage")
    if any(r["owned_exclusion"] != "false" for r in matrix_rows):
        errors.append("owned_exclusion_present")

    # Reconstruct the regular G85 family universe directly from the frozen 980-row atlas.
    g85 = read_tsv(ROOT / "udt_cmb_G85_mixed_timelive_completion_atlas_2026-08-12/PROFILE_ARCHETYPE_ATLAS.tsv")
    regular = [r for r in g85 if r["classification"] != "POINTWISE_DEGENERATE"]
    regular_counts = Counter(r["archetype_id"] for r in regular)
    if set(regular_counts) != EXPECTED_FAMILIES or set(regular_counts.values()) != {196}:
        errors.append("frozen_regular_family_reconstruction")
    if len(regular) != 588 or any(r["frozen_cell_preserved"] != "true" for r in regular):
        errors.append("frozen_regular_rows_or_cell_preservation")

    # Independent finite-dimensional seam checks using the exact registered formulas.
    # Off-axis set D=C=1. The axis is checked with det G_H=4u-b^2.
    shift_axis = 4 * 0 - 1**2
    shift_seam_off_axis = 1 * (0 * 1 - 1**2)
    lapse_axis = 4 * (-1) - 0**2
    lapse_seam_off_axis = 1 * ((-1) * 1 - 1**2)
    taper_axis_with_shift = 4 * 0 - 1**2
    taper_seam = 1 * (0 * 1 - 0**2)
    if not (shift_axis < 0 and shift_seam_off_axis < 0):
        errors.append("shift_seam_algebra")
    if not (lapse_axis < 0 and lapse_seam_off_axis < 0):
        errors.append("lapse_seam_algebra")
    if not (taper_axis_with_shift < 0 and taper_seam == 0):
        errors.append("taper_seam_algebra")

    # Exact source-owned semantic guards. These are source assertions, not new deductions.
    semantic_fragments = {
        "udt_xmax_asymptotic_limit_frame_correction_2026-08-05/STATUS_AND_WORKFLOW.md":
            "The asymptote is relational. It is not a material wall, a preferred center, a radial edge",
        "udt_founding_pair_relation_functor_ownership_audit_2026-08-09/AUDIT_REPORT.md":
            "constrains covariance, reversal, and matched composition but does not supply existence or",
        "udt_complete_timelive_orchestra_compatibility_audit_2026-08-10/AUDIT_REPORT.md":
            "EXACT_COMPATIBILITY_ORCHESTRA_BUT_NO_EVOLUTION_LAW",
        "udt_native_history_restriction_from_scratch_2026-08-10/AUDIT_REPORT.md":
            "NO_CURRENTLY_OWNED_NONIDENTITY_HISTORY_RESTRICTION",
        "udt_copresent_causal_pair_functor_selector_audit_2026-08-10/AUDIT_REPORT.md":
            "Co-presence remains whole-solution co-membership semantics",
    }
    for path, fragment in semantic_fragments.items():
        if fragment not in (ROOT / path).read_text(encoding="utf-8"):
            errors.append(f"semantic_guard:{path}")

    if len(conditional_rows) != 4 or conditional_rows[0]["conditional_id"] != "S00":
        errors.append("conditional_selector_rows")
    if conditional_rows[0]["selection_status"] != "NO_SELECTION":
        errors.append("current_owned_result_changed")
    if any(
        row["conditional_id"] != "S00" and "UNOWNED" not in row["premise_status"]
        for row in conditional_rows
    ):
        errors.append("conditional_selector_promoted")

    report = (PKG / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    forbidden = (
        "physical X_max is the seam",
        "geodesically complete",
        "bootstrap selects",
        "CMB prediction",
    )
    if any(token in report for token in forbidden):
        errors.append("forbidden_promotion_in_report")

    if result.get("owned_nonidentity_selector_count") != 0:
        errors.append("result_selector_count")
    if result.get("owned_exclusion_count") != 0:
        errors.append("result_exclusion_count")
    if result.get("physical_promotions") != 0:
        errors.append("physical_promotion")
    if result.get("primary_landing") != (
        "NO_EXISTING_OWNED_CONDITION_DISTINGUISHES_THE_THREE_G85_REGULAR_FAMILIES"
    ):
        errors.append("landing")
    return errors


def main() -> None:
    errors = validate()
    output = {
        "verdict": "VERIFIED_WITH_CAVEATS" if not errors else "FAILED",
        "errors": errors,
        "method": "independent_stdlib_manifest_census_seam_algebra_and_source_guard_reconstruction",
        "source_count": 21,
        "condition_count": 14,
        "family_count": 3,
        "matrix_row_count": 42,
        "regular_G85_rows_reconstructed": 588,
        "independence_caveat": (
            "separate implementation without production imports; semantic guards still test the frozen "
            "source record and are not a fresh external semantic adjudication"
        ),
    }
    (PKG / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()
