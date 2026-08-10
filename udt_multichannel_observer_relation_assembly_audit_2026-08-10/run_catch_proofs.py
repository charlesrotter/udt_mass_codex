#!/usr/bin/env python3
"""Exercise semantic mutations against the multi-channel conclusion contract."""

from __future__ import annotations

import copy
import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


BASE = {
    "assembly_ids": {"A00", "A01", "A02", "A03", "A04", "A05"},
    "alpha": "UNSELECTED_PATH_SCALARIZATION_FAMILY",
    "beta_family": "UNSELECTED_ENDPOINT_SCALARIZATION_FAMILY",
    "strain": "DIAGNOSTIC_NOT_CHARACTER",
    "connection_potential": "QUOTIENT_GAUGE_REPRESENTATIVE",
    "physical_regime_map": None,
    "c_E": "ACTIVE_PAIR_TAPE_CALIBRATION_ONLY",
    "G_obs": "INACTIVE_WITHOUT_NATIVE_MASS_READOUT",
    "m_e": "UNAPPLIED_FUTURE_CALIBRATION_CANDIDATE",
    "hbar": "EXCLUDED",
    "conductor": None,
    "physical_arrow": None,
    "universal_c_eff": None,
    "strong_CSN": "INACTIVE",
    "downstream": None,
    "scope": "SUPPLIED_REGULAR_STATIONARY_R17_PAIR_QUERY",
}


def validate(state: dict[str, object]) -> None:
    assert state["assembly_ids"] == {"A00", "A01", "A02", "A03", "A04", "A05"}
    assert state["alpha"] == "UNSELECTED_PATH_SCALARIZATION_FAMILY"
    assert state["beta_family"] == "UNSELECTED_ENDPOINT_SCALARIZATION_FAMILY"
    assert state["strain"] == "DIAGNOSTIC_NOT_CHARACTER"
    assert state["connection_potential"] == "QUOTIENT_GAUGE_REPRESENTATIVE"
    assert state["physical_regime_map"] is None
    assert state["c_E"] == "ACTIVE_PAIR_TAPE_CALIBRATION_ONLY"
    assert state["G_obs"] == "INACTIVE_WITHOUT_NATIVE_MASS_READOUT"
    assert state["m_e"] == "UNAPPLIED_FUTURE_CALIBRATION_CANDIDATE"
    assert state["hbar"] == "EXCLUDED"
    assert state["conductor"] is None
    assert state["physical_arrow"] is None
    assert state["universal_c_eff"] is None
    assert state["strong_CSN"] == "INACTIVE"
    assert state["downstream"] is None
    assert state["scope"] == "SUPPLIED_REGULAR_STATIONARY_R17_PAIR_QUERY"


def main() -> int:
    mutations: list[tuple[str, str, object]] = [
        ("M01", "drop_pair_metric_parent", {"assembly_ids": {"A01", "A02", "A03", "A04", "A05"}}),
        ("M02", "drop_common_scale", {"assembly_ids": {"A00", "A02", "A03", "A04", "A05"}}),
        ("M03", "drop_reciprocal_depth", {"assembly_ids": {"A00", "A01", "A03", "A04", "A05"}}),
        ("M04", "drop_shift", {"assembly_ids": {"A00", "A01", "A02", "A04", "A05"}}),
        ("M05", "drop_angular_transport", {"assembly_ids": {"A00", "A01", "A02", "A03", "A05"}}),
        ("M06", "drop_object_typing", {"assembly_ids": {"A00", "A01", "A02", "A03", "A04"}}),
        ("M07", "promote_alpha_family", {"alpha": "PHYSICAL_CHANNEL"}),
        ("M08", "promote_beta_family", {"beta_family": "PHYSICAL_CHANNEL"}),
        ("M09", "promote_strain_character", {"strain": "ADDITIVE_CHARACTER"}),
        ("M10", "promote_connection_potential", {"connection_potential": "GLOBAL_SCALAR_ONE_FORM"}),
        ("M11", "assign_physical_regimes", {"physical_regime_map": "MICRO_ORDINARY_COSMO"}),
        ("M12", "use_cE_as_selector", {"c_E": "SELECTS_COMPLETE_ARCHITECTURE"}),
        ("M13", "activate_G_without_mass", {"G_obs": "ACTIVE_CHANNEL_SELECTOR"}),
        ("M14", "activate_electron_mass", {"m_e": "SELECTS_BRANCH"}),
        ("M15", "import_hbar", {"hbar": "ACTIVE"}),
        ("M16", "invent_conductor", {"conductor": "BOOTSTRAP"}),
        ("M17", "promote_physical_arrow", {"physical_arrow": "DERIVED"}),
        ("M18", "promote_universal_ceff", {"universal_c_eff": "DERIVED"}),
        ("M19", "restore_strong_CSN", {"strong_CSN": "ACTIVE"}),
        ("M20", "infer_downstream_physics", {"downstream": "ACTION_SOURCE_MATTER"}),
        ("M21", "widen_to_all_branches", {"scope": "ALL_UDT"}),
    ]
    rows = []
    rejected = 0
    for mutation_id, name, changes in mutations:
        state = copy.deepcopy(BASE)
        state.update(changes)
        caught = False
        try:
            validate(state)
        except AssertionError:
            caught = True
        if caught:
            rejected += 1
        rows.append({"mutation_id": mutation_id, "mutation": name, "expected": "REJECT", "result": "REJECTED" if caught else "ESCAPED", "status": "PASS" if caught else "FAIL"})

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
