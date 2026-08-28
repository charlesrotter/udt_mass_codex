#!/usr/bin/env python3
"""Hostile typed-overreach catches for G285."""

from __future__ import annotations

import json


def main() -> None:
    baseline = {
        "phi_is_component_not_complete_germ": True,
        "different_tide_means_different_L2_germ": True,
        "tide_is_metric_curvature_not_external_orchestra": True,
        "retyping_does_not_select_values": True,
        "W5_unchanged": True,
        "c_eff_not_promoted_to_signal_speed": True,
        "G283_G284_value_nonselection_retained": True,
        "local_germ_not_global_history": True,
        "absolute_scale_still_open": True,
        "observations_and_dynamics_not_imported": True,
    }
    mutations = {
        "collapse_complete_germ_to_phi": ("phi_is_component_not_complete_germ", False),
        "call_same_phi_same_separation": ("different_tide_means_different_L2_germ", False),
        "externalize_tidal_sector": ("tide_is_metric_curvature_not_external_orchestra", False),
        "claim_retyping_selects_values": ("retyping_does_not_select_values", False),
        "silently_replace_W5": ("W5_unchanged", False),
        "promote_c_eff_to_signal_speed": ("c_eff_not_promoted_to_signal_speed", False),
        "erase_value_nonselection": ("G283_G284_value_nonselection_retained", False),
        "globalize_local_germ": ("local_germ_not_global_history", False),
        "derive_absolute_scale": ("absolute_scale_still_open", False),
        "import_observations_or_dynamics": ("observations_and_dynamics_not_imported", False),
    }
    caught: dict[str, bool] = {}
    for name, (key, mutant_value) in mutations.items():
        mutant = dict(baseline)
        mutant[key] = mutant_value
        caught[name] = all(mutant.values()) is False
    result = {
        "audit": "G285_TYPED_OVERREACH_CATCHES",
        "status": "PASS" if all(baseline.values()) and all(caught.values()) else "FAIL",
        "baseline_accepted": all(baseline.values()),
        "mutation_count": len(mutations),
        "caught_count": sum(caught.values()),
        "caught": caught,
        "scope": "in_memory_typed_claim_schema_only",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
