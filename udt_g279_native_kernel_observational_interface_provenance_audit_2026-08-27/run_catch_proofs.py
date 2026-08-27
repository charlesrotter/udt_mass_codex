#!/usr/bin/env python3
"""Hostile mutation checks for G279 provenance guards."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from derive_native_provenance import EDGES, G236, G278, audit_executables, validate_edges


PACKAGE = Path(__file__).resolve().parent


def must_fail(label: str, operation) -> dict[str, object]:
    try:
        operation()
    except (AssertionError, SyntaxError):
        return {"mutation": label, "caught": True}
    raise AssertionError(f"hostile mutation escaped: {label}")


def validate_required_fragments(g236_text: str, g278_text: str) -> None:
    assert "K_VALUES = (8, 12, 16, 24)" in g236_text
    assert "IMPORTED_CONDITIONAL_eta_1_epsilon_1_over_Z" in g236_text
    assert "K_VALUES = (8, 12, 16, 24)" in g278_text
    assert "elif not (resolution_pass and subset_pass and serialization_pass)" in g278_text
    assert '"transparent_transfer_imported": True' in g278_text
    assert '"P1_used": False' in g278_text
    assert '"Xmax_used": False' in g278_text
    assert '"lcdm_distance_used": False' in g278_text


def main() -> None:
    audit_executables()
    validate_edges(EDGES)
    g236 = G236.read_text()
    g278 = G278.read_text()
    validate_required_fragments(g236, g278)

    catches: list[dict[str, object]] = []
    mutations = [
        ("hide_transfer_import", g236.replace("IMPORTED_CONDITIONAL_eta_1_epsilon_1_over_Z", "DERIVED_NATIVE"), g278),
        ("drop_G236_resolution_family", g236.replace("K_VALUES = (8, 12, 16, 24)", "K_VALUES = (12,)"), g278),
        ("drop_G278_resolution_family", g236, g278.replace("K_VALUES = (8, 12, 16, 24)", "K_VALUES = (12,)")),
        ("bypass_resolution_landing", g236, g278.replace("elif not (resolution_pass and subset_pass and serialization_pass)", "elif not (subset_pass and serialization_pass)")),
        ("claim_no_transfer", g236, g278.replace('"transparent_transfer_imported": True', '"transparent_transfer_imported": False')),
        ("activate_P1", g236, g278.replace('"P1_used": False', '"P1_used": True')),
        ("activate_Xmax", g236, g278.replace('"Xmax_used": False', '"Xmax_used": True')),
        ("activate_LCDM_distance", g236, g278.replace('"lcdm_distance_used": False', '"lcdm_distance_used": True')),
    ]
    for label, left, right in mutations:
        catches.append(must_fail(label, lambda l=left, r=right: validate_required_fragments(l, r)))

    edge_mutations = [
        ("promote_W1_to_derived", "E03", "status", "DERIVED"),
        ("promote_transfer_to_native", "E06", "status", "DERIVED"),
        ("hide_numerical_representation", "E07", "class", "NATIVE_KERNEL"),
        ("hide_empirical_attachment", "E08", "class", "NATIVE_KERNEL"),
        ("make_W5_load_bearing_G278", "P00", "load_bearing_G278", "yes"),
        ("make_angular_postreadout_load_bearing", "S00", "load_bearing_G278", "yes"),
    ]
    for label, edge_id, key, value in edge_mutations:
        trial = copy.deepcopy(EDGES)
        for edge in trial:
            if edge["edge"] == edge_id:
                edge[key] = value
        catches.append(must_fail(label, lambda t=trial: validate_edges(t)))

    result = {
        "audit": "G279_HOSTILE_CATCH_PROOFS",
        "status": "PASS",
        "catches": catches,
        "caught": sum(int(item["caught"]) for item in catches),
        "expected": len(catches),
    }
    assert result["caught"] == result["expected"]
    (PACKAGE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
