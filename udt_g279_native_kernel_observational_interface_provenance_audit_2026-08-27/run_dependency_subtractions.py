#!/usr/bin/env python3
"""Graph-level subtraction audit for the G279 provenance chain."""

from __future__ import annotations

import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent


EDGES = {
    "E00": ("founding", "D_delta"),
    "E01": ("D_delta", "primary_metric"),
    "E02": ("primary_metric", "complete_pair_pullback_h"),
    "E03": ("complete_pair_pullback_h", "completed_Phi"),
    "E04": ("completed_Phi", "delta_AB"),
    "E05": ("delta_AB", "direct_redshift"),
    "E06": ("direct_redshift", "relative_areal_formula"),
    "E07": ("relative_areal_formula", "G236_state"),
    "E08": ("G236_state", "conditional_scale"),
    "E09": ("conditional_scale", "DES_holdout"),
    "S00": ("primary_metric", "angular_Jacobi_sibling"),
    "P00": ("completed_Phi", "projective_W5_sibling"),
}


def reachable(removed: set[str]) -> set[str]:
    nodes = {"founding"}
    changed = True
    while changed:
        changed = False
        for edge_id, (source, target) in EDGES.items():
            if edge_id in removed or source not in nodes or target in nodes:
                continue
            nodes.add(target)
            changed = True
    return nodes


def case(label: str, removed: set[str], must_survive: set[str], must_fail: set[str]) -> dict[str, object]:
    nodes = reachable(removed)
    assert must_survive <= nodes, (label, "missing survivors", sorted(must_survive - nodes))
    assert not (must_fail & nodes), (label, "unexpected survivors", sorted(must_fail & nodes))
    return {
        "case": label,
        "removed_edges": sorted(removed),
        "survives": sorted(nodes),
        "required_survivors_pass": True,
        "required_failures_pass": True,
    }


def main() -> None:
    native = {
        "D_delta",
        "primary_metric",
        "complete_pair_pullback_h",
        "completed_Phi",
        "delta_AB",
        "direct_redshift",
    }
    downstream = {"relative_areal_formula", "G236_state", "conditional_scale", "DES_holdout"}
    cases = [
        case("full_chain", set(), native | downstream, set()),
        case("subtract_transfer", {"E06"}, native, downstream),
        case(
            "subtract_G236_representation",
            {"E07"},
            native | {"relative_areal_formula"},
            {"G236_state", "conditional_scale", "DES_holdout"},
        ),
        case(
            "subtract_empirical_scale_attachment",
            {"E08"},
            native | {"relative_areal_formula", "G236_state"},
            {"conditional_scale", "DES_holdout"},
        ),
        case("subtract_DES_holdout", {"E09"}, native | (downstream - {"DES_holdout"}), {"DES_holdout"}),
        case(
            "subtract_W1_completed_pair_extension",
            {"E03"},
            {"D_delta", "primary_metric", "complete_pair_pullback_h", "angular_Jacobi_sibling"},
            {"completed_Phi", "delta_AB", "direct_redshift", "projective_W5_sibling"} | downstream,
        ),
        case(
            "subtract_founding_reciprocal_character",
            {"E00"},
            set(),
            native | downstream,
        ),
        case("subtract_W5_sibling", {"P00"}, native | downstream, {"projective_W5_sibling"}),
        case("subtract_angular_sibling", {"S00"}, native | downstream, {"angular_Jacobi_sibling"}),
    ]
    result = {
        "audit": "G279_DEPENDENCY_SUBTRACTIONS",
        "status": "PASS",
        "case_count": len(cases),
        "cases": cases,
        "landing": (
            "NATIVE_DIMENSIONLESS_CHAIN_SURVIVES_OBSERVATIONAL_IMPORT_SUBTRACTION"
            "__G278_OUTPUT_DOES_NOT_SURVIVE_TRANSFER_OR_EMPIRICAL_ATTACHMENT_SUBTRACTION"
            "__W5_AND_ANGULAR_SIBLINGS_NOT_EXECUTABLE_G278_DEPENDENCIES"
        ),
    }
    (PACKAGE / "SUBTRACTION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
