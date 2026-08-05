#!/usr/bin/env python3
"""Fail closed on current foundational premise and startup-precedence regressions."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    rows = read_tsv(ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv")
    require(len(rows) == 27, "premise registry must contain exactly 27 rows")
    by_id = {row["premise_id"]: row for row in rows}
    require(len(by_id) == 27, "duplicate premise id")
    require(
        by_id["G01"]["current_status"] == "DERIVED_RECIPROCAL_CHARACTER_ON_SUPPLIED_ORDERED_DEPTH",
        "founded relational character",
    )
    require(
        by_id["G02"]["current_status"]
        == "DERIVED_DELTA_MAPS_TO_DIAG_EXP_MINUS_DELTA_EXP_PLUS_DELTA",
        "founded relational character action",
    )
    require("general observer/event/path-to-depth law" in by_id["G01"]["open_scope"], "depth law promoted")
    require("universal pointwise physical scalar" in by_id["G01"]["forbidden_regression"], "pointwise owner guard absent")
    require(by_id["G03"]["active_use"] == "COMPARISON_ONLY_NOT_NATIVE", "independent phi promoted")
    require(by_id["G04"]["current_status"] == "CHALLENGED_OWNER_POSTULATE_NOT_DERIVED", "strong local CSN status")
    require(by_id["G04"]["active_use"] == "INACTIVE_UNLESS_CHARLES_EXPLICITLY_REAUTHORIZES", "strong local CSN activated")
    require(by_id["G05"]["active_use"] == "ALGEBRA_ONLY", "common cancellation promoted")
    require(by_id["G06"]["active_use"] == "ACTIVE_CALIBRATION", "c/G anchors dropped")
    require(by_id["G07"]["active_use"] == "GENERIC_ARENA_BASELINE_ONLY", "generic metric count promoted")
    require(by_id["G08"]["epistemic_label"] == "OPEN", "4D extension promoted")
    require(by_id["G09"]["epistemic_label"] == "POSIT", "carrier promoted")
    require(by_id["G10"]["active_use"] == "INACTIVE_WITHOUT_STRONG_CSN_PREMISE", "C2/Bach promoted")
    require(by_id["G11"]["active_use"] == "NOT_SELECTED", "EH promoted")
    require(
        by_id["G12"]["current_status"]
        == "WORKING_MUTUAL_ADMISSIBILITY_POSIT__PARTIAL_KINEMATIC_JOIN_DERIVED__SMOOTH_EXTENSION_CARTAN_NONSELECTION__FULL_FIRST_AND_SECOND_JET_CURVATURE_ATLASES_DERIVED__CONDITIONAL_LOCAL_SAME_SOLUTION_PHI_CURVATURE_COMPATIBILITY__GLOBAL_FACTORIZATION_GROUPOID_AND_OVERLAP_NONSELECTION_DERIVED__FOUNDING_RELATIONAL_CHARACTER_ON_SUPPLIED_DEPTH_DERIVED__POINTWISE_PHI_PRESENTATION_POTENTIAL_ON_SUPPLIED_FACTORIZATION__CONDITIONAL_STATIONARY_KILLING_DEPTH__TWO_OBSERVER_RELATIONAL_DEPTH_LAW_AND_COMPLETE_RETURN_OPEN",
        "bootstrap status regressed or promoted",
    )
    require(by_id["G12"]["active_use"] == "FALSIFIABLE_RELATIONAL_ARCHITECTURE_ONLY", "bootstrap use changed")
    require(by_id["G13"]["active_use"] == "TORIC_GEOMETRY_ONLY", "Maxwell promoted")
    require(
        by_id["G14"]["current_status"] == "WORKING_FOUNDATIONAL_POSITIONAL_DILATION_ASYMPTOTE",
        "Xmax limiting role reopened or promoted",
    )
    require(
        by_id["G14"]["active_use"] == "OWNER_RATIFIED_LIMIT_FRAME_AND_REQUIRED_DEPTH_LAW_GATE",
        "Xmax workflow gate mistyped",
    )
    require("numerical value" in by_id["G14"]["open_scope"], "numerical Xmax promoted")
    require("all-frame theorem" in by_id["G14"]["open_scope"], "Xmax frame theorem promoted")
    require("material wall" in by_id["G14"]["forbidden_regression"], "Xmax wall guard absent")
    require(by_id["G15"]["active_use"] == "STATIC_FINITE_BOX_AND_CARRIER_CONDITIONAL", "Hopfion promoted")
    require(by_id["G16"]["current_status"] == "OPEN", "complete physics promoted")
    require(
        by_id["G17"]["current_status"] == "KEPT_MULTIPLY_ANCHORED_SPLIT_FROM_MIRROR_CLAUSE",
        "finite-cell split reading changed",
    )
    require(by_id["G17"]["active_use"] == "ACTIVE_FOUNDATION_SPLIT_READING", "finite-cell split inactive")
    require(
        by_id["G18"]["current_status"] == "OWNER_RATIFIED_PROPOSAL_NOT_DERIVED_SPLIT_RULED_2026-07-30",
        "mirror closure promoted or dropped",
    )
    require(
        by_id["G18"]["active_use"] == "WORKING_PREMISE_ONLY_STAMPS_TRAVEL_VIA_CONSUMER_LEDGER",
        "mirror closure use changed",
    )
    require(by_id["G19"]["active_use"] == "CONFIGURATION_ARENA_ONLY", "coframe promoted")
    require(by_id["G20"]["active_use"] == "NO_UNIVERSAL_VARIATION_DOMAIN_SELECTED", "variation owner promoted")
    require("query varied as field" in by_id["G20"]["forbidden_regression"], "query variation guard absent")
    require(by_id["G21"]["current_status"] == "OPEN_RESPONSE_OR_CURRENT_ROLE_NOT_SUBSTANCE", "source mistyped")
    require(by_id["G22"]["active_use"] == "NO_UNCONDITIONAL_MASS_CLAIM", "mass promoted")
    require(by_id["G23"]["active_use"] == "SEMANTIC_FRAME_ONLY", "copresence promoted")
    require("instantaneous access" in by_id["G23"]["forbidden_regression"], "copresence signal guard absent")
    require(by_id["G24"]["active_use"] == "GEOMETRIC_REACHABILITY_ONLY", "causal access promoted")
    require(by_id["G25"]["active_use"] == "TYPE_GUARD_ONLY", "boundary type guard promoted")
    require("Xmax" in by_id["G25"]["forbidden_regression"], "Xmax/boundary guard absent")
    require(by_id["G26"]["active_use"] == "NO_CARRIER_EMERGENCE_CLAIM", "angular carrier promoted")
    require(by_id["G27"]["active_use"] == "NO_ORDER_SELECTED", "action/closure order selected")

    guard_rows = read_tsv(
        ROOT / "udt_foundational_semantic_regression_correction_2026-07-26/SEMANTIC_GUARD_UNIVERSE.tsv"
    )
    require(len(guard_rows) == 16, "guard universe must contain exactly 16 rows")
    guard_sources = {row["guard_id"]: row["controlling_source"] for row in guard_rows}
    for guard, source in guard_sources.items():
        if guard in {"G01", "G02", "G12", "G14"}:
            expected = {
                "G01": "udt_founding_phi_ownership_morphism_audit_2026-08-05/AUDIT_REPORT.md",
                "G02": "udt_founding_phi_ownership_morphism_audit_2026-08-05/EXACT_DERIVATION.md",
                "G12": "udt_founding_phi_ownership_morphism_audit_2026-08-05/AUDIT_REPORT.md",
                "G14": "udt_xmax_asymptotic_limit_frame_correction_2026-08-05/STATUS_AND_WORKFLOW.md",
            }[guard]
            require(
                by_id[guard]["controlling_source"] == expected,
                f"relational correction source priority changed: {guard}",
            )
        else:
            require(by_id[guard]["controlling_source"] == source, f"source priority changed: {guard}")

    expected_sources = {row["controlling_source"] for row in rows}
    for source in expected_sources:
        require((ROOT / source).is_file(), f"missing controlling source: {source}")

    controls = [
        "AGENTS.md",
        "LIVE.md",
        "HANDOFF.md",
        "INDEX.md",
        "README.md",
        "research/README.md",
        "research/_registry/README.md",
        "MEMORY.md",
        "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
    ]
    for control in controls:
        text = (ROOT / control).read_text(encoding="utf-8")
        require("CURRENT_SCIENTIFIC_PREMISES.tsv" in text, f"control lacks premise registry: {control}")

    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    for token in [
        "on **supplied ordered depth**",
        "presentation potential",
        "universal physical scalar",
        "CHOSE_COMPARISON_CONFIGURATION",
        "CHALLENGED_OWNER_POSTULATE_NOT_DERIVED",
        "generic configuration-arena count",
        "WORKING_FOUNDATIONAL_FRAME",
        "positional-dilation asymptote",
        "finite-cell seal",
    ]:
        require(token in agents, f"AGENTS guard absent: {token}")

    xmax_controls = [
        "LIVE.md",
        "HANDOFF.md",
        "INDEX.md",
        "README.md",
        "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
        "research/README.md",
    ]
    xmax_source = "udt_xmax_asymptotic_limit_frame_correction_2026-08-05/STATUS_AND_WORKFLOW.md"
    for control in xmax_controls:
        text = (ROOT / control).read_text(encoding="utf-8")
        require(xmax_source in text, f"control lacks Xmax correction: {control}")
        require("positional-dilation asymptote" in text, f"control lacks Xmax limiting meaning: {control}")

    adjudication = read_tsv(
        ROOT / "udt_foundational_semantic_regression_correction_2026-07-26/ACTIVE_SEMANTIC_ADJUDICATION.tsv"
    )
    require(len(adjudication) == 754, "semantic candidate adjudication must contain 754 rows")
    require(len({row["candidate_id"] for row in adjudication}) == 754, "duplicate semantic candidate id")
    require(len({row["path"] for row in adjudication}) == 754, "duplicate semantic candidate path")
    require(all(row["controlling_disposition"] for row in adjudication), "unadjudicated semantic candidate")

    dof = ROOT / "udt_global_functional_dof_constraint_rank_audit_2026-07-26"
    status = {row["id"]: row for row in read_tsv(dof / "STATUS_LEDGER.tsv")}
    presentation = {row["id"]: row for row in read_tsv(dof / "LOCAL_PRESENTATION_RANK.tsv")}
    require(status["S03"]["status"] == "CHOSE_COMPARISON_F4_7_TOTAL", "DOF independent phi still native")
    require(status["S04"]["status"] == "DERIVED_FOUNDED_PHI_ADDS_ZERO__COMPLETE_EXTENSION_OPEN", "DOF founded phi still conditional")
    require(presentation["P04"]["status"] == "CHOSE_COMPARISON_CONFIGURATION", "DOF comparison branch promotion")
    require(presentation["P05"]["status"] == "DERIVED_FOUNDED_SUBGROUP__FULL_EXTENSION_OPEN", "DOF founded branch regression")
    print("PASS: 27 premise guards, relational-depth and conceptual-type corrections, 9 startup controls, 754 historical candidate dispositions, corrected DOF semantics")


if __name__ == "__main__":
    main()
