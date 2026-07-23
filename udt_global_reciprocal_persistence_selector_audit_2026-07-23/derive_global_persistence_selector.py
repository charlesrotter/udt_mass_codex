#!/usr/bin/env python3
"""Deterministic audit of whether UDT premises force global reciprocal persistence."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "2f0853e070529925d38f5e8e9be99ce0c27684c8"

SOURCE_PATHS = [
    "LIVE.md",
    "HANDOFF.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
    "UDT_NATIVE_ACTION_COLD_PACKET.md",
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_MAP.md",
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md",
    "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md",
    "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md",
    "bootstrap_csn_phi_angular_selector_2026-07-19/AUDIT_REPORT.md",
    "bootstrap_csn_phi_angular_selector_2026-07-19/STATUS_LEDGER.tsv",
    "udt_complete_metric_realization_zoomout_2026-07-23/AUDIT_REPORT.md",
    "udt_complete_metric_realization_zoomout_2026-07-23/BOOTSTRAP_REALIZATION_MATRIX.tsv",
    "udt_complete_metric_intrinsic_object_audit_2026-07-23/AUDIT_REPORT.md",
    "udt_complete_metric_intrinsic_object_audit_2026-07-23/STATUS_LEDGER.tsv",
    "udt_finite_cell_reciprocal_survival_density_audit_2026-07-23/AUDIT_REPORT.md",
    "udt_finite_cell_reciprocal_survival_density_audit_2026-07-23/DERIVATION_RESULT.json",
]

SELECTORS = [
    {
        "selector_id": "S01",
        "premise": "RECIPROCAL_C_COEQUAL_CONVERSION",
        "level": "VALUE",
        "ruling": "VALUE_LEVEL_ONLY",
        "reason": "RELATES_TIME_LENGTH_CONVERSION_DIRECTIONS_NOT_DPHI",
    },
    {
        "selector_id": "S02",
        "premise": "DUAL_CONTRAGREDIENT_RECIPROCITY",
        "level": "VALUE",
        "ruling": "VALUE_LEVEL_ONLY",
        "reason": "FORCES_UV_EQUALS_ONE_FOR_COMPARISON_CHARACTER",
    },
    {
        "selector_id": "S03",
        "premise": "ADDITIVE_POSITIONAL_COMPOSITION",
        "level": "VALUE",
        "ruling": "VALUE_LEVEL_ONLY",
        "reason": "FORCES_EXPONENTIAL_CHARACTER_AFTER_REGULARITY_NOT_FIELD_JETS",
    },
    {
        "selector_id": "S04",
        "premise": "REALIZED_NONTRIVIAL_DILATION",
        "level": "GLOBAL_OBSERVATION",
        "ruling": "OBSERVED_NONTRIVIALITY_ONLY",
        "reason": "EXCLUDES_IDENTITY_AS_REALIZED_UNIVERSE_NOT_CRITICAL_POINTS",
    },
    {
        "selector_id": "S05",
        "premise": "TRIVIAL_PHI_ZERO_REPRESENTATION",
        "level": "VALUE",
        "ruling": "COMPATIBLE_BUT_NONSELECTING",
        "reason": "MATHEMATICALLY_ALLOWED_AND_HAS_NO_DERIVATIVE_SPLIT",
    },
    {
        "selector_id": "S06",
        "premise": "COMMON_SCALE_NEUTRALITY",
        "level": "EQUIVALENCE",
        "ruling": "COMPATIBLE_BUT_NONSELECTING",
        "reason": "PRESERVES_ZERO_NULL_NONNULL_STRATA_BUT_SELECTS_NONE",
    },
    {
        "selector_id": "S07",
        "premise": "STATIC_ODD_PHI_SEAL",
        "level": "BOUNDARY_VALUE",
        "ruling": "EXPLICITLY_LEAVES_DERIVATIVE_FREE",
        "reason": "PHI_ZERO_AT_SEAL_WITH_FREE_NORMAL_DERIVATIVE",
    },
    {
        "selector_id": "S08",
        "premise": "FINITE_CELL_STRUCTURE",
        "level": "GLOBAL_DOMAIN",
        "ruling": "COMPATIBLE_BUT_NONSELECTING",
        "reason": "SUPPLIES_DOMAIN_NOT_A_NONNULL_DPHI_EQUATION",
    },
    {
        "selector_id": "S09",
        "premise": "GLOBAL_BOOTSTRAP",
        "level": "GLOBAL_ADMISSIBILITY",
        "ruling": "ON_SHELL_ADMISSIBILITY_NO_OPERATION",
        "reason": "NO_TYPED_OPERATION_EXISTENCE_TEST_OR_RANKING_RULE",
    },
    {
        "selector_id": "S10",
        "premise": "GRADIENT_SLOT_IDENTIFICATION",
        "level": "LOCAL_REALIZATION",
        "ruling": "CONDITIONAL_FUTURE_ROUTE",
        "reason": "CURRENT_PACKET_LABELS_IDENTIFICATION_CONDITIONAL",
    },
    {
        "selector_id": "S11",
        "premise": "INTRINSIC_DPHI_TWO_FORM_REDUCTION",
        "level": "DERIVATIVE_GEOMETRY",
        "ruling": "CONDITIONAL_FUTURE_ROUTE",
        "reason": "EXACT_ON_NONNULL_STRATA_BUT_PHYSICAL_OWNER_AND_GLOBAL_EXTENSION_OPEN",
    },
    {
        "selector_id": "S12",
        "premise": "NATIVE_ACTION_OR_EIKONAL_EQUATION",
        "level": "DYNAMICS",
        "ruling": "CONDITIONAL_FUTURE_ROUTE",
        "reason": "COULD_EXCLUDE_CRITICAL_OR_NULL_STRATA_BUT IS CURRENTLY_OPEN",
    },
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def exact_algebra() -> tuple[dict[str, object], list[dict[str, object]]]:
    x, a, b, omega = sp.symbols("x a b omega", real=True)

    def character(phi: sp.Expr) -> sp.Matrix:
        return sp.diag(sp.exp(-phi), sp.exp(phi))

    group = {
        "determinant_one": sp.simplify(character(a).det()) == 1,
        "composition": sp.simplify(character(a) * character(b) - character(a + b))
        == sp.zeros(2),
        "reversal": sp.simplify(character(a).inv() - character(-a)) == sp.zeros(2),
    }
    profiles = [
        ("C01_LINEAR", x, "NONTRIVIAL"),
        ("C02_CUBIC_CRITICAL", x**3, "NONTRIVIAL"),
        ("C03_TRIVIAL", sp.Integer(0), "TRIVIAL_ALLOWED"),
    ]
    rows: list[dict[str, object]] = []
    for profile_id, phi, nontriviality in profiles:
        dphi = sp.diff(phi, x)
        d = character(phi)
        current = sp.simplify(d.inv() * d.diff(x))
        norm = sp.simplify(dphi**2)
        at_seal = sp.simplify(phi.subs(x, 0))
        derivative_at_seal = sp.simplify(dphi.subs(x, 0))
        rows.append(
            {
                "profile_id": profile_id,
                "phi": str(phi),
                "odd_at_seal": str(sp.simplify(phi.subs(x, -x) + phi) == 0),
                "phi_at_seal": str(at_seal),
                "dphi_dx": str(dphi),
                "dphi_at_seal": str(derivative_at_seal),
                "gradient_norm_control": str(norm),
                "D_at_seal": str(d.subs(x, 0).tolist()),
                "J_at_seal": str(current.subs(x, 0).tolist()),
                "det_D": str(sp.simplify(d.det())),
                "value_character_defined_at_seal": "True",
                "derivative_projector_defined_at_seal": str(
                    derivative_at_seal != 0
                ),
                "nontriviality": nontriviality,
                "implication_role": (
                    "POSITIVE_CONTROL"
                    if profile_id == "C01_LINEAR"
                    else (
                        "DECISIVE_FOUNDATION_LEVEL_COUNTERCONFIGURATION"
                        if profile_id == "C02_CUBIC_CRITICAL"
                        else "MATHEMATICALLY_ALLOWED_LIMIT_CONTROL"
                    )
                ),
                "scope_guard": "KINEMATIC_CONFIGURATION_NOT_COMPLETE_ON_SHELL_UNIVERSE",
            }
        )

    csn = {
        "norm_transform": str(sp.simplify(omega ** -2 * sp.Symbol("s"))),
        "positive_scale_preserves_zero": sp.simplify(
            (omega ** -2 * sp.Integer(0))
        )
        == 0,
        "positive_scale_cannot_select_nonzero": True,
    }
    if not all(group.values()) or not all(
        row["det_D"] == "1" and row["phi_at_seal"] == "0" for row in rows
    ):
        raise AssertionError("exact algebra control")
    if rows[1]["dphi_at_seal"] != "0" or rows[1][
        "value_character_defined_at_seal"
    ] != "True":
        raise AssertionError("critical counterconfiguration")
    return {"group": group, "csn": csn}, rows


def main() -> None:
    algebra, profiles = exact_algebra()
    classifications = Counter(row["ruling"] for row in SELECTORS)
    forced = classifications["FORCES_GLOBAL_PERSISTENCE"]

    write_tsv(
        HERE / "SELECTOR_LEDGER.tsv",
        ["selector_id", "premise", "level", "ruling", "reason"],
        SELECTORS,
    )
    write_tsv(
        HERE / "COUNTERCONFIGURATION_LEDGER.tsv",
        list(profiles[0]),
        profiles,
    )

    implication_rows = [
        {
            "edge_id": "I01",
            "from_object": "RECIPROCAL_C_PLUS_DUAL_RECIPROCITY",
            "to_object": "UV_EQUALS_ONE",
            "status": "DERIVED_WITH_FOUNDING_FORMALIZATION",
            "missing_join": "NONE",
        },
        {
            "edge_id": "I02",
            "from_object": "UV_EQUALS_ONE_PLUS_COMPOSITION_REGULARITY",
            "to_object": "D_PHI_EXPONENTIAL_CHARACTER",
            "status": "DERIVED_CONDITIONAL",
            "missing_join": "NONE",
        },
        {
            "edge_id": "I03",
            "from_object": "D_PHI_EXPONENTIAL_CHARACTER",
            "to_object": "J_EQUALS_DIAG_MINUS_DPHI_PLUS_DPHI",
            "status": "EXACT_DIFFERENTIATION_WHERE_PHI_IS_DIFFERENTIABLE",
            "missing_join": "NONE",
        },
        {
            "edge_id": "I04",
            "from_object": "J",
            "to_object": "NORMALIZED_DPHI_PROJECTOR",
            "status": "CONDITIONAL",
            "missing_join": "NONZERO_NONNULL_DPHI",
        },
        {
            "edge_id": "I05",
            "from_object": "NORMALIZED_DPHI_PROJECTOR",
            "to_object": "REAL_TWO_FORM_3PLUS3_REDUCTION",
            "status": "DERIVED_LOCAL_STRATUM_GEOMETRY",
            "missing_join": "GLOBAL_EXTENSION",
        },
        {
            "edge_id": "I06",
            "from_object": "REAL_TWO_FORM_3PLUS3_REDUCTION",
            "to_object": "PHYSICAL_RECIPROCAL_SECTOR_OWNER",
            "status": "OPEN",
            "missing_join": "NATIVE_SOLDERING_OR_SELECTION_RULE",
        },
        {
            "edge_id": "I07",
            "from_object": "REGISTERED_FOUNDATION",
            "to_object": "NONZERO_NONNULL_DPHI_EVERYWHERE",
            "status": "NOT_DERIVED",
            "missing_join": "NATIVE_EQUATION_OR_ADDITIONAL_PREMISE",
        },
        {
            "edge_id": "I08",
            "from_object": "GLOBAL_BOOTSTRAP",
            "to_object": "EXCLUSION_OF_CRITICAL_OR_NULL_STRATA",
            "status": "OPEN_NO_OPERATION",
            "missing_join": "TYPED_REALIZATION_OPERATION_AND_ACCEPTANCE_PREDICATE",
        },
    ]
    write_tsv(
        HERE / "IMPLICATION_GRAPH.tsv",
        ["edge_id", "from_object", "to_object", "status", "missing_join"],
        implication_rows,
    )

    lineage = []
    for relative in SOURCE_PATHS:
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(relative)
        lineage.append(
            {
                "path": relative,
                "sha256": sha256(path),
                "size": path.stat().st_size,
            }
        )
    write_tsv(HERE / "SOURCE_LINEAGE.tsv", ["path", "sha256", "size"], lineage)

    status_rows = [
        {
            "object": "reciprocal_exponential_character",
            "status": "DERIVED_CONDITIONAL",
            "scope": "dual_reciprocity_plus_composition_and_regularity",
        },
        {
            "object": "derivative_current",
            "status": "DERIVED_KINEMATIC_IDENTITY",
            "scope": "differentiable_phi",
        },
        {
            "object": "local_real_reciprocal_3plus3_reduction",
            "status": "DERIVED_LOCAL_STRATUM_GEOMETRY",
            "scope": "regular_metric_and_nonzero_nonnull_dphi",
        },
        {
            "object": "global_3plus3_persistence",
            "status": "OPEN_NOT_DERIVED",
            "scope": "registered_foundation_supplies_no_nowhere_critical_nonnull_equation",
        },
        {
            "object": "physical_reciprocal_sector_ownership",
            "status": "OPEN_NOT_DERIVED",
            "scope": "two_compatible_weight_assignments_and_no_native_soldering",
        },
        {
            "object": "bootstrap_exclusion_of_degenerate_strata",
            "status": "OPEN_NO_OPERATION",
            "scope": "working_on_shell_admissibility_only",
        },
        {
            "object": "additional_persistence_premise",
            "status": "NOT_ADOPTED",
            "scope": "would_be_required_unless_future_native_equation_derives_it",
        },
    ]
    write_tsv(
        HERE / "STATUS_LEDGER.tsv", ["object", "status", "scope"], status_rows
    )

    scope_rows = [
        {
            "item": "registered_foundation_source_audit",
            "coverage": "COMPLETE_FOR_PREREGISTERED_SOURCES",
            "not_covered": "future_or_unregistered_premises",
        },
        {
            "item": "exact_value_and_derivative_algebra",
            "coverage": "COMPLETE_FOR_THREE_PREREGISTERED_CONTROLS",
            "not_covered": "complete_field_solution_space",
        },
        {
            "item": "implication_counterconfiguration",
            "coverage": "COMPLETE_FOR_DIRECT_FOUNDATION_TO_PERSISTENCE_IMPLICATION",
            "not_covered": "on_shell_exclusion_by_future_dynamics",
        },
        {
            "item": "physical_universe",
            "coverage": "NOT_SOLVED",
            "not_covered": "action_source_carrier_boundary_density_and_scale",
        },
    ]
    write_tsv(
        HERE / "COMPLETENESS_SCOPE.tsv",
        ["item", "coverage", "not_covered"],
        scope_rows,
    )

    result = {
        "schema": "udt-global-reciprocal-persistence-selector-1.0",
        "base_commit": BASE,
        "sympy_version": sp.__version__,
        "algebra": algebra,
        "counts": {
            "selectors": len(SELECTORS),
            "forcing_selectors": forced,
            "counterconfigurations": len(profiles),
            "nontrivial_counterconfigurations_with_critical_seal": sum(
                row["nontriviality"] == "NONTRIVIAL"
                and row["dphi_at_seal"] == "0"
                for row in profiles
            ),
            "implication_edges": len(implication_rows),
            "sources": len(lineage),
        },
        "decisive_counterconfiguration": {
            "profile": "phi=x^3",
            "satisfies_value_level_reciprocal_character": True,
            "satisfies_static_odd_seal": True,
            "nontrivial": True,
            "dphi_zero_at_seal": True,
            "D_defined_at_seal": True,
            "on_shell_complete_universe_claimed": False,
            "logical_role": "DEFEATS_DIRECT_IMPLICATION_FROM_REGISTERED_FOUNDATION",
        },
        "selector_ruling": (
            "FOUNDING_RECIPROCITY_IS_VALUE_LEVEL_AND_DOES_NOT_FORCE_GLOBAL_"
            "DERIVATIVE_BASED_3PLUS3_PERSISTENCE__PERSISTENCE_REQUIRES_A_"
            "FUTURE_NATIVE_EQUATION_OR_AN_ADDITIONAL_PREMISE"
        ),
        "maximum_conclusion_respected": True,
    }
    (HERE / "RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
