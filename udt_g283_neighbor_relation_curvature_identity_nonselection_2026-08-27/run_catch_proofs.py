#!/usr/bin/env python3
"""In-memory claim-schema catches for the bounded G283 landing."""

from __future__ import annotations

import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent


BASELINE = {
    "central_first_jet_equal": True,
    "three_arbitrary_tidal_functions": True,
    "two_tracefree_functions": True,
    "Bianchi_compatibility_passes": True,
    "Cartan_is_realization_not_composer": True,
    "Jacobi_areas_can_differ": True,
    "network_composes_for_arbitrary_T": True,
    "owned_value_selector_found": False,
    "field_equation_imported": False,
}


def accepted(claim: dict[str, bool]) -> bool:
    return (
        claim["central_first_jet_equal"]
        and claim["three_arbitrary_tidal_functions"]
        and claim["two_tracefree_functions"]
        and claim["Bianchi_compatibility_passes"]
        and claim["Cartan_is_realization_not_composer"]
        and claim["Jacobi_areas_can_differ"]
        and claim["network_composes_for_arbitrary_T"]
        and not claim["owned_value_selector_found"]
        and not claim["field_equation_imported"]
    )


def main() -> None:
    mutations = {
        "make_central_connection_depend_on_T": {"central_first_jet_equal": False},
        "make_Bianchi_select_T_values": {"Bianchi_compatibility_passes": False},
        "erase_tracefree_functional_freedom": {"two_tracefree_functions": False},
        "force_all_Jacobi_areas_equal": {"Jacobi_areas_can_differ": False},
        "promote_Cartan_to_composer": {"Cartan_is_realization_not_composer": False},
        "break_interval_network_composition": {"network_composes_for_arbitrary_T": False},
        "import_field_equation_as_owned": {"owned_value_selector_found": True, "field_equation_imported": True},
    }
    caught = {}
    for name, changes in mutations.items():
        claim = BASELINE | changes
        caught[name] = not accepted(claim)
    result = {
        "audit": "G283_IN_MEMORY_CLAIM_SCHEMA_CATCHES",
        "status": "PASS" if accepted(BASELINE) and all(caught.values()) else "FAIL",
        "baseline_accepted": accepted(BASELINE),
        "mutation_count": len(mutations),
        "caught_count": sum(caught.values()),
        "caught": caught,
        "certification_scope": "in_memory_boolean_claim_schema_only__not_artifact_level_mutation_replay",
    }
    if result["status"] != "PASS":
        raise AssertionError(result)
    (PACKAGE / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
