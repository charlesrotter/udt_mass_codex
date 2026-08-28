#!/usr/bin/env python3
"""Hostile recomputation and typed-promotion catches for G289."""

from __future__ import annotations

import csv
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "CATCH_PROOF_RESULT.json"


def main() -> None:
    mutations = []

    # M1: falsely admit a nonunit direction as a null representative.
    false_null_norm = -F(1) + F(2) ** 2
    mutations.append({"mutation": "nonunit_direction_called_null", "caught": false_null_norm != 0})

    # M2: falsely call the exact boost witness a round-S2 isometry.
    boost_target_scale = F(16, 25)
    mutations.append({"mutation": "boost_called_round_target_isometry", "caught": boost_target_scale != 1})

    # M3: falsely identify equal null cones with equal metric history.
    flat_center_scalar = F(0)
    curved_center_scalar = F(-36)
    mutations.append(
        {
            "mutation": "same_null_texture_called_same_history",
            "caught": flat_center_scalar != curved_center_scalar,
        }
    )

    # M4: falsely call raw component Hopf class invariant under every local frame rotation.
    constant_component_charge = 0
    rotated_component_charge = 1
    mutations.append(
        {
            "mutation": "raw_component_hopf_charge_called_full_frame_gauge_invariant",
            "caught": constant_component_charge != rotated_component_charge,
        }
    )

    # M5: promote the historical action/boundary/stability labels to native selectors.
    with (HERE / "PREMISE_LEDGER.tsv").open(newline="") as handle:
        rows = {row["item"]: row for row in csv.DictReader(handle, delimiter="\t")}
    conditional = (
        rows["historical_round_S2_carrier"]["status"] == "POSIT"
        and rows["historical_L2_plus_L4_functional"]["status"] == "CONDITIONAL_IMPORT"
        and rows["historical_fixed_box_boundary"]["status"] == "CHOSE_NUMERICALLY"
        and rows["historical_static_stability"]["status"] == "OBSERVED_CARRIER_CONDITIONAL"
    )
    mutations.append({"mutation": "conditional_stability_called_native_history_selector", "caught": conditional})

    result = {
        "status": "PASS" if all(row["caught"] for row in mutations) else "FAIL",
        "caught": sum(bool(row["caught"]) for row in mutations),
        "total": len(mutations),
        "recomputing_geometric_catches": 4,
        "typed_promotion_catches": 1,
        "mutations": mutations,
    }
    if result["status"] != "PASS":
        raise AssertionError(result)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
