#!/usr/bin/env python3
"""Fail-closed adversarial claim-promotion checks."""

from __future__ import annotations

import copy
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def validate(state, claims):
    native_relational_matter = all(
        state[key]
        for key in (
            "metric_relational_clock_cocycle",
            "metric_transverse_path_cocycle",
            "metric_selected_global_angular_lift_and_caps",
            "metric_selected_carrier_or_configuration_space",
            "native_off_shell_matter_mass_response",
            "complete_finite_cell_boundary_variation",
            "same_solution_metric_matter_fixed_point",
        )
    )
    downstream_action = all(
        state[key]
        for key in (
            "native_off_shell_matter_mass_response",
            "complete_finite_cell_boundary_variation",
            "helmholtz_integrability_of_native_response",
            "global_action_periods_gauge_and_boundary_integrability",
        )
    )
    if claims["native_relational_matter"] and not native_relational_matter:
        raise AssertionError("matter promotion")
    if claims["downstream_native_action"] and not downstream_action:
        raise AssertionError("action promotion")
    if claims["clock_alone_supplies_hopf"]:
        raise AssertionError("contractible clock channel cannot supply angular winding alone")
    if claims["topology_alone_supplies_source"]:
        raise AssertionError("topological class is not an off-shell metric response")
    if claims["local_helmholtz_implies_global_action"] and not state[
        "global_action_periods_gauge_and_boundary_integrability"
    ]:
        raise AssertionError("global period/boundary obstruction")
    return {
        "native_relational_matter": native_relational_matter,
        "downstream_native_action": downstream_action,
    }


def rejected(state, mutation):
    claims = {
        "native_relational_matter": False,
        "downstream_native_action": False,
        "clock_alone_supplies_hopf": False,
        "topology_alone_supplies_source": False,
        "local_helmholtz_implies_global_action": False,
    }
    mutation(state, claims)
    try:
        validate(state, claims)
    except AssertionError:
        return "PASS_REJECTED"
    raise AssertionError("false promotion accepted")


def main():
    result = json.loads((HERE / "RESULT.json").read_text(encoding="utf-8"))
    base = result["details"]["dependency_arrows"]
    actual = validate(copy.deepcopy(base), {
        "native_relational_matter": False,
        "downstream_native_action": False,
        "clock_alone_supplies_hopf": False,
        "topology_alone_supplies_source": False,
        "local_helmholtz_implies_global_action": False,
    })
    catches = {
        "matter_from_conditional_hopf_only": rejected(
            copy.deepcopy(base),
            lambda state, claims: claims.update(native_relational_matter=True),
        ),
        "action_without_response": rejected(
            copy.deepcopy(base),
            lambda state, claims: claims.update(downstream_native_action=True),
        ),
        "clock_alone_as_hopf": rejected(
            copy.deepcopy(base),
            lambda state, claims: claims.update(clock_alone_supplies_hopf=True),
        ),
        "topology_as_source": rejected(
            copy.deepcopy(base),
            lambda state, claims: claims.update(topology_alone_supplies_source=True),
        ),
        "local_helmholtz_as_global_action": rejected(
            copy.deepcopy(base),
            lambda state, claims: (
                state.update(helmholtz_integrability_of_native_response=True),
                claims.update(local_helmholtz_implies_global_action=True),
            ),
        ),
        "response_without_boundary_as_action": rejected(
            copy.deepcopy(base),
            lambda state, claims: (
                state.update(
                    native_off_shell_matter_mass_response=True,
                    helmholtz_integrability_of_native_response=True,
                ),
                claims.update(downstream_native_action=True),
            ),
        ),
        "global_topology_without_local_response_as_matter": rejected(
            copy.deepcopy(base),
            lambda state, claims: (
                state.update(
                    metric_selected_global_angular_lift_and_caps=True,
                    metric_selected_carrier_or_configuration_space=True,
                ),
                claims.update(native_relational_matter=True),
            ),
        ),
    }
    assert all(value == "PASS_REJECTED" for value in catches.values())
    output = {
        "schema": "udt-sandbox-global-local-relational-closure-adversarial-1.0",
        "result": "PASS",
        "actual_derived_promotions": actual,
        "catch_proofs": catches,
        "catch_count": len(catches),
    }
    (HERE / "ADVERSARIAL.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
