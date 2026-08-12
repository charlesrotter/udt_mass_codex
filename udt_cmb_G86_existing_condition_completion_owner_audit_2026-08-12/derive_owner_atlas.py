#!/usr/bin/env python3
"""Build the preregistered G86 existing-condition ownership atlas."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent

FAMILIES = (
    ("A03_RADIAL_SHIFT_TIMELIVE", "SHIFT_SUPPORTED_NONUNIFORM_SEAM"),
    ("A04_LAPSE_LIFT_TIMELIVE", "LAPSE_LIFTED_TIMELIKE_SEAM"),
    ("A05_MIXING_TAPER_BEFORE_SEAM", "TAPERED_UNIFORMLY_NULL_SEAM"),
)

CONDITIONS = (
    ("C01", "Lorentz regularity and nondegeneracy", "KINEMATIC_ADMISSIBILITY",
     "udt_cmb_G85_mixed_timelive_completion_atlas_2026-08-12/EXACT_DERIVATION.md",
     "Regularity classifies all three constructive families but supplies no history owner."),
    ("C02", "Exact G75 north-cell preservation", "KINEMATIC_ADMISSIBILITY",
     "udt_cmb_G85_mixed_timelive_completion_atlas_2026-08-12/PROFILE_ARCHETYPE_ATLAS.tsv",
     "Every regular family preserves the authoritative cell exactly."),
    ("C03", "Time orientation and local bidirectional causal admissibility", "KINEMATIC_ADMISSIBILITY",
     "udt_copresent_causal_pair_functor_selector_audit_2026-08-10/AUDIT_REPORT.md",
     "Causal admissibility evaluates a supplied family and does not choose the ambient family."),
    ("C04", "Observer reversal Reciprocity and matched carry", "QUERY_CONDITIONAL",
     "udt_founding_pair_relation_functor_ownership_audit_2026-08-09/AUDIT_REPORT.md",
     "Reciprocity constrains covariance reversal and matched composition; not existence or uniqueness."),
    ("C05", "Typed complete observer query", "QUERY_CONDITIONAL",
     "udt_common_query_pair_immersion_reconstruction_2026-08-11/AUDIT_REPORT.md",
     "A query types and evaluates supplied realizations; the physical query and branch remain open."),
    ("C06", "Co-presence as whole-solution membership", "NECESSARY_NOT_SUFFICIENT",
     "udt_copresent_causal_pair_functor_selector_audit_2026-08-10/AUDIT_REPORT.md",
     "Co-presence contributes no local selector or signalling rule."),
    ("C07", "Finite-domain and seam-type distinction", "NECESSARY_NOT_SUFFICIENT",
     "CURRENT_SCIENTIFIC_PREMISES.tsv",
     "The distinction prevents conflating asymptote seam boundary and variational data; it selects none."),
    ("C08", "Observer-pair X_max asymptote", "NECESSARY_NOT_SUFFICIENT",
     "udt_xmax_asymptotic_limit_frame_correction_2026-08-05/STATUS_AND_WORKFLOW.md",
     "The limit is required, but its law value angular completion and identification with this seam are open."),
    ("C09", "Observer re-centering and frame sharing", "OPEN_UNOWNED",
     "udt_cmb_G84_am_global_completion_pair_diameter_audit_2026-08-12/EXACT_DERIVATION.md",
     "Only the zero-mixing central-geodesic isometry orbit is proved; none of the mixed families is adjudicated."),
    ("C10", "Global topology and smooth complete-tensor candidate", "CONDITIONAL_CANDIDATE",
     "udt_cmb_G85_mixed_timelive_completion_atlas_2026-08-12/EXACT_DERIVATION.md",
     "All three have conditional smooth witnesses on the declared arena; physical topology is not selected."),
    ("C11", "Geodesic or global causal completeness", "OPEN_UNOWNED",
     "udt_cmb_G85_mixed_timelive_completion_atlas_2026-08-12/STATUS_LEDGER.tsv",
     "G85 complete-metric regularity is not geodesic completeness and no family has this proof."),
    ("C12", "Low-z SNe compatibility anchor", "NECESSARY_NOT_SUFFICIENT",
     "udt_sne_native_observer_query_replay_2026-08-11/AUDIT_REPORT.md",
     "All families are identical on the inherited cell and no complete SNe query owns a correction."),
    ("C13", "Cartan Maurer-Cartan and Bianchi compatibility", "IDENTITY_ONLY",
     "udt_complete_timelive_orchestra_compatibility_audit_2026-08-10/AUDIT_REPORT.md",
     "These identities hold for every smooth full-rank coframe movie and select no history."),
    ("C14", "Native history or global nonidentity restriction", "OPEN_UNOWNED",
     "udt_native_history_restriction_from_scratch_2026-08-10/AUDIT_REPORT.md",
     "No owned nonidentity history restriction was found in the controlling source census."),
)

EVALUATIONS = {
    "C01": {
        "A03_RADIAL_SHIFT_TIMELIVE": "PASS_CONDITIONAL_NONVANISHING_SHIFT",
        "A04_LAPSE_LIFT_TIMELIVE": "PASS_CONSTRUCTIVE_NEGATIVE_CLOCK_NORM",
        "A05_MIXING_TAPER_BEFORE_SEAM": "PASS_CONDITIONAL_REGULAR_CHART_TAPER",
    },
    "C02": {family: "PASS_EXACT_SAME_INHERITED_CELL" for family, _ in FAMILIES},
    "C03": {family: "ADMISSIBLE_ON_SUPPLIED_REGULAR_FAMILY__NO_FAMILY_TEST" for family, _ in FAMILIES},
    "C04": {family: "NOT_EVALUATED_DIFFERENTIALLY__QUERY_RULE_OPEN" for family, _ in FAMILIES},
    "C05": {family: "REALIZATION_CAN_BE_QUERY_SUPPLIED__NOT_QUERY_SELECTED" for family, _ in FAMILIES},
    "C06": {family: "WHOLE_SOLUTION_MEMBERSHIP_COMPATIBLE__NO_SELECTOR" for family, _ in FAMILIES},
    "C07": {
        "A03_RADIAL_SHIFT_TIMELIVE": "SEAM_TIMELIKE_OFF_AXIS_NULL_ON_AXIS",
        "A04_LAPSE_LIFT_TIMELIVE": "SEAM_TIMELIKE_EVERYWHERE",
        "A05_MIXING_TAPER_BEFORE_SEAM": "SEAM_UNIFORMLY_NULL",
    },
    "C08": {
        "A03_RADIAL_SHIFT_TIMELIVE": "CANDIDATE_LAPSE_DIVERGENCE_PRESENT__GLOBAL_JOIN_OPEN",
        "A04_LAPSE_LIFT_TIMELIVE": "DIVERGENCE_REMOVED_AT_THIS_SEAM__OTHER_REALIZATION_OPEN",
        "A05_MIXING_TAPER_BEFORE_SEAM": "CANDIDATE_LAPSE_DIVERGENCE_PRESENT__GLOBAL_JOIN_OPEN",
    },
    "C09": {family: "UNTESTED_FOR_MIXED_FAMILY" for family, _ in FAMILIES},
    "C10": {family: "CONDITIONAL_SMOOTH_WITNESS_ON_DECLARED_ARENA" for family, _ in FAMILIES},
    "C11": {family: "NOT_PROVED" for family, _ in FAMILIES},
    "C12": {family: "SAME_AUTHORITATIVE_CELL__NO_RANKING_POWER" for family, _ in FAMILIES},
    "C13": {family: "PASS_IDENTITY_FOR_SMOOTH_FULL_RANK_COFRAME" for family, _ in FAMILIES},
    "C14": {family: "NO_OWNED_HISTORY_RULE_TO_APPLY" for family, _ in FAMILIES},
}

PROPERTY_DISTINGUISHES = {"C07", "C08"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def read_manifest() -> list[dict[str, str]]:
    with (OUT / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    assert len(rows) == 21
    assert len({row["path"] for row in rows}) == 21
    for row in rows:
        assert sha256(ROOT / row["path"]) == row["sha256"]
    return rows


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    sources = read_manifest()
    source_paths = {row["path"] for row in sources}
    family_ids = {row[0] for row in FAMILIES}

    owner_rows = []
    for condition_id, condition, owner_class, source, finding in CONDITIONS:
        assert source in source_paths
        owner_rows.append({
            "condition_id": condition_id,
            "condition": condition,
            "owner_class": owner_class,
            "source_path": source,
            "property_distinguishes_families": str(condition_id in PROPERTY_DISTINGUISHES).lower(),
            "owned_selection_power": "false",
            "finding": finding,
        })

    matrix_rows = []
    for condition_id, *_ in CONDITIONS:
        assert set(EVALUATIONS[condition_id]) == family_ids
        for family_id, family_label in FAMILIES:
            matrix_rows.append({
                "condition_id": condition_id,
                "family_id": family_id,
                "family_label": family_label,
                "evaluation": EVALUATIONS[condition_id][family_id],
                "owned_exclusion": "false",
            })

    conditional_rows = [
        {
            "conditional_id": "S00",
            "extra_condition": "none__apply_only_frozen_owned_conditions",
            "surviving_families": ";".join(family for family, _ in FAMILIES),
            "premise_status": "CURRENT_OWNED_RESULT",
            "selection_status": "NO_SELECTION",
        },
        {
            "conditional_id": "S01",
            "extra_condition": "identify_this_seam_with_physical_Xmax_and_require_uniform_null_character",
            "surviving_families": "A05_MIXING_TAPER_BEFORE_SEAM",
            "premise_status": "NEW_COMPOSITE_UNOWNED",
            "selection_status": "CONDITIONAL_ONLY_NOT_AUTHORITY",
        },
        {
            "conditional_id": "S02",
            "extra_condition": "identify_this_seam_with_physical_Xmax_without_uniform_null_requirement",
            "surviving_families": "A03_RADIAL_SHIFT_TIMELIVE;A05_MIXING_TAPER_BEFORE_SEAM",
            "premise_status": "NEW_IDENTIFICATION_UNOWNED",
            "selection_status": "CONDITIONAL_ONLY_NOT_AUTHORITY",
        },
        {
            "conditional_id": "S03",
            "extra_condition": "preserve_nonzero_seam_mixing_and_lapse_zero_as_physical_history_data",
            "surviving_families": "A03_RADIAL_SHIFT_TIMELIVE",
            "premise_status": "NEW_HISTORY_PRESERVATION_UNOWNED",
            "selection_status": "CONDITIONAL_ONLY_NOT_AUTHORITY",
        },
    ]

    write_tsv(OUT / "CONDITION_OWNER_ATLAS.tsv", list(owner_rows[0]), owner_rows)
    write_tsv(OUT / "FAMILY_CONDITION_MATRIX.tsv", list(matrix_rows[0]), matrix_rows)
    write_tsv(OUT / "CONDITIONAL_SELECTOR_ATLAS.tsv", list(conditional_rows[0]), conditional_rows)

    owner_counts = Counter(row["owner_class"] for row in owner_rows)
    result = {
        "base_commit": "b8875ccffaaa422e3447c58895017e475202a804",
        "preregistration_commit": "2778b16e",
        "source_count": len(sources),
        "condition_count": len(owner_rows),
        "family_count": len(FAMILIES),
        "matrix_row_count": len(matrix_rows),
        "owned_nonidentity_selector_count": owner_counts["OWNED_NONIDENTITY_SELECTOR"],
        "owned_exclusion_count": sum(row["owned_exclusion"] == "true" for row in matrix_rows),
        "property_distinguishing_condition_count": sum(
            row["property_distinguishes_families"] == "true" for row in owner_rows
        ),
        "owner_class_counts": dict(sorted(owner_counts.items())),
        "primary_landing": "NO_EXISTING_OWNED_CONDITION_DISTINGUISHES_THE_THREE_G85_REGULAR_FAMILIES",
        "smallest_missing_selector": (
            "an_owned_native_history_or_global_relation rule deciding whether this candidate seam "
            "realizes the physical observer-pair asymptote and which complete-metric channels are "
            "permitted to change on approach"
        ),
        "physical_promotions": 0,
    }
    with (OUT / "DERIVATION_RESULT.json").open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, sort_keys=True)
        f.write("\n")


if __name__ == "__main__":
    main()
