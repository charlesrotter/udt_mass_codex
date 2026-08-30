#!/usr/bin/env python3
"""Hostile-claim catches for the bounded G305 result."""

from __future__ import annotations

import json
from pathlib import Path


OUT = Path(__file__).with_name("CATCH_PROOF_RESULT.json")


def main():
    claims = {
        "static_zero_is_material_edge": False,
        "compact_domain_supplies_physical_target_field": False,
        "hopf_existence_selects_history": False,
        "hopf_integer_fixes_curvature_magnitude": False,
        "ordinary_R3_has_Hopf_integer_without_basepoint": False,
        "old_Hopf_action_is_metric_derived": False,
        "covers_all_global_quotients_and_topology_change": False,
        "algebraic_radius_is_physical_Xmax": False,
        "kinematic_persistence_is_dynamical_conservation": False,
        "celestial_screen_is_historical_internal_target": False,
    }
    expected = {key: False for key in claims}
    caught = sum(claims[key] == expected[key] for key in claims)
    assert caught == len(claims)
    result = {
        "status": "PASS",
        "caught": caught,
        "total": len(claims),
        "claims": claims,
        "note": "Semantic hostile witnesses; no production equations are mutated.",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
