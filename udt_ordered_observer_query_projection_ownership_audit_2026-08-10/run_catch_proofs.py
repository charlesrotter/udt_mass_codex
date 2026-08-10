#!/usr/bin/env python3
"""Exercise semantic mutations against the projection-ownership contract."""

from __future__ import annotations

import copy
import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE = {
    "founding_output": "Delta_phi_CONDITIONAL_REALIZATION_WITHIN_DENSITY_CHARACTER_CLASS",
    "uniqueness_scope": "LIMITED_CHARACTER_CLASS",
    "kappa": "RETAINED_COMPLETE_STATE",
    "beta": "CONDITIONAL_QUERY_STATE_NOT_CHARACTER",
    "U": "CONDITIONAL_PATH_INSTRUMENT_NOT_REAL_SCALAR",
    "screen_weight": "DERIVED_REPRESENTATION",
    "endpoint_coboundaries": "MATHEMATICALLY_SURVIVE_BUT_UNOWNED",
    "G52": "UNSELECTED_MICROPHONE_FAMILIES",
    "phi_orchestra": "UPSTREAM_MODULATION_RETAINED",
    "physical_pair_map": None,
    "physical_path": None,
    "regime_map": None,
    "regime_switch": None,
    "c_E": "TERMINAL_RECIPROCAL_CALIBRATION_ONLY",
    "G_obs": "INACTIVE_WITHOUT_MASS_READOUT",
    "m_e": "UNAPPLIED_CANDIDATE",
    "hbar": "EXCLUDED",
    "conductor": None,
    "physical_arrow": None,
    "downstream": None,
    "scope": "SUPPLIED_REGULAR_CALIBRATED_STATIONARY_R17_PAIR_QUERY",
}


def validate(state: dict[str, object]) -> None:
    assert state == BASE


def main() -> int:
    mutations: list[tuple[str, str, dict[str, object]]] = [
        ("M01", "promote_full_panel_to_founding_output", {"founding_output": "FULL_PANEL"}),
        ("M02", "widen_uniqueness_to_all_coboundaries", {"uniqueness_scope": "ALL_COMPLETE_STATE_FUNCTIONS"}),
        ("M03", "delete_kappa_by_CSN", {"kappa": "GAUGE_DELETED"}),
        ("M04", "promote_beta_to_character", {"beta": "ADDITIVE_CHARACTER"}),
        ("M05", "scalarize_U", {"U": "REAL_SCALAR"}),
        ("M06", "double_count_screen_weight", {"screen_weight": "INDEPENDENT_CHANNEL"}),
        ("M07", "claim_endpoint_coboundaries_refuted", {"endpoint_coboundaries": "IMPOSSIBLE"}),
        ("M08", "promote_endpoint_coboundary", {"endpoint_coboundaries": "FOUNDING_OWNED"}),
        ("M09", "select_G52_microphone", {"G52": "PHYSICAL_PROJECTION"}),
        ("M10", "erase_phi_orchestra", {"phi_orchestra": "PURE_BLOCK_ONLY"}),
        ("M11", "invent_physical_pair_map", {"physical_pair_map": "DERIVED"}),
        ("M12", "invent_physical_path", {"physical_path": "DERIVED"}),
        ("M13", "assign_regime_map", {"regime_map": "MICRO_ORDINARY_COSMO"}),
        ("M14", "add_regime_switch", {"regime_switch": "HAND_THRESHOLD"}),
        ("M15", "use_cE_as_architecture_selector", {"c_E": "CHANNEL_SELECTOR"}),
        ("M16", "activate_G", {"G_obs": "CHANNEL_SELECTOR"}),
        ("M17", "activate_electron_mass", {"m_e": "CHANNEL_SELECTOR"}),
        ("M18", "import_hbar", {"hbar": "ACTIVE"}),
        ("M19", "invent_conductor", {"conductor": "BOOTSTRAP"}),
        ("M20", "promote_physical_arrow", {"physical_arrow": "DERIVED"}),
        ("M21", "infer_downstream_physics", {"downstream": "ACTION_SOURCE_MATTER"}),
        ("M22", "widen_to_all_branches", {"scope": "ALL_UDT"}),
        ("M23", "erase_conditional_realization_boundary", {"founding_output": "Delta_phi_BARE_ENDPOINT_DERIVED"}),
    ]
    rows = []
    rejected = 0
    for mutation_id, mutation, change in mutations:
        state = copy.deepcopy(BASE)
        state.update(change)
        caught = False
        try:
            validate(state)
        except AssertionError:
            caught = True
        rejected += int(caught)
        rows.append({
            "mutation_id": mutation_id,
            "mutation": mutation,
            "expected": "REJECT",
            "result": "REJECTED" if caught else "ESCAPED",
            "status": "PASS" if caught else "FAIL",
        })
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=["mutation_id", "mutation", "expected", "result", "status"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    result = {
        "status": "PASS" if rejected == len(mutations) else "FAIL",
        "rejected": rejected,
        "total": len(mutations),
        "failed": [row["mutation_id"] for row in rows if row["status"] != "PASS"],
    }
    (HERE / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
