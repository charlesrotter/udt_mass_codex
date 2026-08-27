#!/usr/bin/env python3
"""In-memory hostile claim-schema catches for G284."""

from __future__ import annotations

import json


def accepted(claim: dict[str, object]) -> bool:
    return (
        claim["all_three_T_functions_live"] is True
        and claim["reconstruction_is_not_selection"] is True
        and claim["cE_is_not_absolute_scale"] is True
        and claim["screen_and_path_carry_retained"] is True
        and claim["endpoint_only_law_not_imported"] is True
        and claim["local_causal_regularity_not_global_selection"] is True
        and claim["homothety_blindness_retained"] is True
        and claim["infinite_c_not_signalling"] is True
        and claim["bounded_witness_not_universal_no_go"] is True
    )


def main() -> None:
    baseline = {
        "all_three_T_functions_live": True,
        "reconstruction_is_not_selection": True,
        "cE_is_not_absolute_scale": True,
        "screen_and_path_carry_retained": True,
        "endpoint_only_law_not_imported": True,
        "local_causal_regularity_not_global_selection": True,
        "homothety_blindness_retained": True,
        "infinite_c_not_signalling": True,
        "bounded_witness_not_universal_no_go": True,
    }
    mutations = {
        "freeze_tidal_functions": ("all_three_T_functions_live", False),
        "promote_cone_reconstruction_to_value_selection": ("reconstruction_is_not_selection", False),
        "promote_cE_to_absolute_tape_scale": ("cE_is_not_absolute_scale", False),
        "erase_screen_or_path_carry": ("screen_and_path_carry_retained", False),
        "import_endpoint_only_delay": ("endpoint_only_law_not_imported", False),
        "globalize_local_causal_tube": ("local_causal_regularity_not_global_selection", False),
        "erase_homothety_separator": ("homothety_blindness_retained", False),
        "promote_infinite_c_to_signalling": ("infinite_c_not_signalling", False),
        "globalize_bounded_nonselection": ("bounded_witness_not_universal_no_go", False),
    }
    caught: dict[str, bool] = {}
    assert accepted(baseline)
    for name, (key, value) in mutations.items():
        mutant = dict(baseline)
        mutant[key] = value
        caught[name] = not accepted(mutant)
    if not all(caught.values()):
        raise AssertionError({name: value for name, value in caught.items() if not value})
    print(
        json.dumps(
            {
                "audit": "G284_IN_MEMORY_CLAIM_SCHEMA_CATCHES",
                "status": "PASS",
                "baseline_accepted": True,
                "caught": caught,
                "caught_count": len(caught),
                "mutation_count": len(mutations),
                "certification_scope": (
                    "in_memory_boolean_claim_schema_only__not_artifact_level_mutation_replay"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
