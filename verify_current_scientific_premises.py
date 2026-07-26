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
    require(len(rows) == 16, "premise registry must contain exactly 16 rows")
    by_id = {row["premise_id"]: row for row in rows}
    require(len(by_id) == 16, "duplicate premise id")
    require(by_id["G01"]["current_status"] == "DERIVED_ADDITIVE_LOG_DEPTH_OF_RECIPROCAL_PAIR", "founded phi identity")
    require(by_id["G02"]["current_status"] == "DERIVED_PHI_MAPS_TO_DIAG_EXP_MINUS_PHI_EXP_PLUS_PHI", "founded phi action")
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
    require(by_id["G12"]["active_use"] == "ON_SHELL_ADMISSIBILITY_ONLY", "bootstrap promoted")
    require(by_id["G13"]["active_use"] == "TORIC_GEOMETRY_ONLY", "Maxwell promoted")
    require(by_id["G14"]["active_use"] == "GLOBAL_OBSERVER_PAIR_SCHEMA", "Xmax mistyped")
    require(by_id["G15"]["active_use"] == "STATIC_FINITE_BOX_AND_CARRIER_CONDITIONAL", "Hopfion promoted")
    require(by_id["G16"]["current_status"] == "OPEN", "complete physics promoted")

    guard_rows = read_tsv(
        ROOT / "udt_foundational_semantic_regression_correction_2026-07-26/SEMANTIC_GUARD_UNIVERSE.tsv"
    )
    require(len(guard_rows) == 16, "guard universe must contain exactly 16 rows")
    guard_sources = {row["guard_id"]: row["controlling_source"] for row in guard_rows}
    for guard, row in by_id.items():
        require(row["controlling_source"] == guard_sources[guard], f"source priority changed: {guard}")

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
        "derived additive logarithmic depth",
        "CHOSE_COMPARISON_CONFIGURATION",
        "CHALLENGED_OWNER_POSTULATE_NOT_DERIVED",
        "generic configuration-arena count",
    ]:
        require(token in agents, f"AGENTS guard absent: {token}")

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
    print("PASS: 16 premise guards, 9 startup controls, 754 candidate dispositions, corrected DOF semantics")


if __name__ == "__main__":
    main()
