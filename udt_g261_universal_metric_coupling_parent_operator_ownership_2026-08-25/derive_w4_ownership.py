#!/usr/bin/env python3
"""Replay the bounded G261 W4 ownership classification from frozen sources."""

from __future__ import annotations

import csv
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_source_gates() -> dict[str, object]:
    """Validate and read every frozen source before any classification is emitted."""
    manifest = list(
        csv.DictReader((ROOT / "SOURCE_MANIFEST.tsv").open(encoding="utf-8"), delimiter="\t")
    )
    assert len(manifest) == 10
    for row in manifest:
        path = REPO / row["path"]
        assert path.is_file(), row["path"]
        assert digest(path) == row["sha256"], row["path"]

    ledger_rows = list(
        csv.DictReader((ROOT / "PREMISE_LEDGER.tsv").open(encoding="utf-8"), delimiter="\t")
    )
    ledger = {row["item"]: row for row in ledger_rows}
    founding = (REPO / "founding.md").read_text(encoding="utf-8")
    founding_flat = " ".join(founding.split())
    g259 = json.loads(
        (
            REPO
            / "udt_g259_metric_only_parent_operator_fork_classification_2026-08-25"
            / "DERIVATION_RESULT.json"
        ).read_text(encoding="utf-8")
    )
    g260 = json.loads(
        (
            REPO
            / "udt_g260_gr_quiet_angular_nondiscard_audit_2026-08-25"
            / "DERIVATION_RESULT.json"
        ).read_text(encoding="utf-8")
    )

    gates = {
        "manifest_rows_verified": len(manifest),
        "w4_status_is_working_posit": (
            "### W4. Universal metric coupling" in founding_flat
            and "`WORKING/POSIT`" in founding_flat
            and ledger["W4"]["status"] == "WORKING_POSIT_NOT_CANON"
        ),
        "w4_one_metric_and_local_semantics": all(
            phrase in founding_flat
            for phrase in (
                "single local geometry used by clocks, rulers, freely falling test systems, and",
                "null propagation",
                "a freely falling frame has local special-relativistic",
            )
        ),
        "w4_primary_metric_unchanged": (
            "does not alter F1--F4's reciprocal algebra or the primary metric components"
            in founding_flat
        ),
        "w4_does_not_select_operator_or_history": all(
            phrase in founding_flat
            for phrase in (
                "does not, merely by being stated, select a field equation",
                "source/history law",
                "locality class",
                "differential order",
            )
        ),
        "g259_class_hypotheses_unowned": (
            g259["status"] == "PASS"
            and g259["lovelock_method"]["assumptions_owned_by_F1_F4_W1_W3"] is False
            and "ownership of locality second order rank2 and identity divergence freedom"
            in g259["open"]
        ),
        "g260_retains_angular_sector_without_parent_law": (
            g260["status"] == "PASS"
            and g260["landing"] == "FULL_METRIC_CANCELLATION_WITH_ACTIVE_ANGULAR_SECTOR"
            and "no UDT parent equation" in g260["maximum_conclusion"]
        ),
        "candidate_remains_not_adopted": (
            ledger["G259_classification"]["status"] == "DERIVED_CONDITIONAL"
            and ledger["vacuum_Einstein"]["status"] == "IMPORTED_COMPARISON_ONLY"
            and ledger["source_history"]["status"] == "OPEN"
        ),
    }
    assert all(value is True or key == "manifest_rows_verified" for key, value in gates.items()), gates
    return gates


def primary_metric_checks() -> dict[str, object]:
    checks = 0
    for index in range(1, 258):
        f = F(index + 1, index)
        c_e = F(index + 2, index + 1)
        r = F(index + 3, index + 2)
        diagonal = (-f * c_e * c_e, 1 / f, r * r, r * r)
        assert diagonal[0] < 0 and all(value > 0 for value in diagonal[1:])
        checks += 4
        determinant = diagonal[0] * diagonal[1] * diagonal[2] * diagonal[3]
        assert determinant == -(c_e * c_e * r**4)
        checks += 1
    return {
        "arbitrary_positive_profile_event_cases": 257,
        "exact_signature_and_determinant_assertions": checks,
        "equatorial_determinant": "-c_E^2*r^4",
        "determinant_depends_on_f_or_phi": False,
    }


def main() -> None:
    source_gates = load_source_gates()
    ownership = [
        ("one_universal_physical_metric", "DERIVED_FROM_W4", "stated directly by W4"),
        (
            "levi_civita_local_inertial_freefall_evaluator",
            "DERIVED_FROM_W4_PLUS_EXISTING_METRIC_GEOMETRY",
            "W4 plus the supplied Lorentz metric gives the unique torsion-free metric-compatible connection",
        ),
        (
            "diffeomorphism_naturality_of_future_law",
            "SUPPORTED_ACCEPTANCE_REQUIREMENT",
            "W4 is invariantly stated but generates no parent operator",
        ),
        (
            "metric_only_gravitational_state",
            "NOT_DERIVED_FROM_W4",
            "universal matter coupling does not exclude an auxiliary gravitational state",
        ),
        (
            "symmetric_rank_two_equation",
            "NOT_DERIVED_FROM_W4",
            "a scalar metric residual can coexist with W4",
        ),
        ("pointwise_locality", "NOT_DERIVED_FROM_W4", "a covariant nonlocal metric law can coexist with W4"),
        (
            "at_most_second_metric_order",
            "NOT_DERIVED_FROM_W4",
            "the G259 R-squared Euler tensor preserves universal metric coupling",
        ),
        (
            "identity_divergence_freedom",
            "NOT_DERIVED_FROM_W4",
            "Ricci_ab is natural and second order but not identity-divergence-free",
        ),
        ("nonidentity_parent_residual", "NOT_DERIVED_FROM_W4", "W4 supplies no residual"),
        ("source_history_values", "NOT_DERIVED_FROM_W4", "W4 evaluates every supplied regular metric"),
    ]

    witnesses = [
        {
            "id": "G259_R2_metric_action",
            "W4": True,
            "metric_only": True,
            "rank_two": True,
            "local": True,
            "second_order": False,
            "divergence_free": True,
            "nonidentity": True,
            "role": "logical_separator_not_UDT_candidate",
        },
        {
            "id": "covariant_nonlocal_metric_action",
            "W4": True,
            "metric_only": True,
            "rank_two": True,
            "local": False,
            "second_order": False,
            "divergence_free": True,
            "nonidentity": True,
            "role": "logical_separator_not_UDT_candidate",
        },
        {
            "id": "scalar_R_equals_zero",
            "W4": True,
            "metric_only": True,
            "rank_two": False,
            "local": True,
            "second_order": True,
            "divergence_free": False,
            "nonidentity": True,
            "role": "incomplete_equation_type_separator_only",
        },
        {
            "id": "Ricci_ab_equals_zero",
            "W4": True,
            "metric_only": True,
            "rank_two": True,
            "local": True,
            "second_order": True,
            "divergence_free": False,
            "nonidentity": True,
            "role": "identity_divergence_separator_only",
        },
        {
            "id": "universal_metric_plus_auxiliary_scalar",
            "W4": True,
            "metric_only": False,
            "rank_two": True,
            "local": True,
            "second_order": True,
            "divergence_free": True,
            "nonidentity": True,
            "role": "metric_only_separator_outside_UDT_program",
        },
        {
            "id": "zero_residual",
            "W4": True,
            "metric_only": True,
            "rank_two": True,
            "local": True,
            "second_order": True,
            "divergence_free": True,
            "nonidentity": False,
            "role": "predictivity_separator_only",
        },
    ]

    atlas_path = ROOT / "OWNERSHIP_ATLAS.tsv"
    with atlas_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("item", "classification", "reason"))
        writer.writerows(ownership)

    result = {
        "status": "PASS",
        "landing": (
            "W4_OWNS_UNIVERSAL_METRIC_COUPLING__PRIMARY_METRIC_UNCHANGED__"
            "G259_CLASS_STILL_UNOWNED__ONE_DYNAMICS_GENERATOR_PREMISE_REMAINS"
        ),
        "mode": "METRIC_LED_OBSERVING_PREMISE_OWNERSHIP",
        "W4_status": "WORKING_POSIT_NOT_CANON",
        "classification_method": "FROZEN_SOURCE_DRIVEN_RULES_PLUS_EXPLICIT_SEPARATORS",
        "source_gates": source_gates,
        "metric_effect": {
            "F1_F4_implication_changed": False,
            "coefficient_changes": 0,
            "new_metric_components": 0,
            "primary_metric_form": "UNCHANGED",
            "physical_interpretation": "ONE_UNIVERSALLY_COUPLED_LOCAL_GEOMETRY",
        },
        "ownership": [
            {"item": item, "classification": classification, "reason": reason}
            for item, classification, reason in ownership
        ],
        "counts": {
            "DERIVED_FROM_W4": sum(row[1] == "DERIVED_FROM_W4" for row in ownership),
            "DERIVED_FROM_W4_PLUS_EXISTING_METRIC_GEOMETRY": sum(
                row[1] == "DERIVED_FROM_W4_PLUS_EXISTING_METRIC_GEOMETRY" for row in ownership
            ),
            "SUPPORTED_ACCEPTANCE_REQUIREMENT": sum(
                row[1] == "SUPPORTED_ACCEPTANCE_REQUIREMENT" for row in ownership
            ),
            "NOT_DERIVED_FROM_W4": sum(row[1] == "NOT_DERIVED_FROM_W4" for row in ownership),
        },
        "separating_witnesses": witnesses,
        "primary_metric_checks": primary_metric_checks(),
        "remaining_premise_type": (
            "NONIDENTITY_DYNAMICS_GENERATOR_SELECTING_A_PROPER_SUBSPACE_OF_COMPLETE_METRICS"
        ),
        "remaining_premise_scope": "BROAD_FAMILY_NOT_UNIQUE_SPECIFIC_MECHANISM",
        "G259_specific_candidate_not_adopted": (
            "NOT_ADOPTED__DIFFEOMORPHISM_INVARIANT_LOCAL_METRIC_ONLY_VARIATIONAL_MINIMALITY_WITH_"
            "AT_MOST_SECOND_ORDER_NONIDENTITY_EULER_OPERATOR"
        ),
        "observational_values_used": 0,
        "fit_coefficients": 0,
        "gpu_used": False,
        "protected_inputs_used": 0,
        "maximum_conclusion": "bounded W4 premise-ownership theorem; no UDT field equation or source/history selected",
    }
    (ROOT / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
