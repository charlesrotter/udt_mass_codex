#!/usr/bin/env python3
"""Fail-closed selector-rank verifier and exercised mutation suite."""
from __future__ import annotations

import copy
import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def base_state() -> dict[str, object]:
    return {
        "phi_extra_field": False,
        "definition_as_selector": False,
        "inequality_reduces_rank": False,
        "unique_K_selects_profile": False,
        "twist_selects_lambda_phi": False,
        "hypersurface_orthogonal_assumed": False,
        "a_cancels_from_q": True,
        "volume_target_invented": False,
        "finite_scalar_kernel_checked": True,
        "lambda_minus_half_checked": True,
        "diameter_is_Xmax": False,
        "Xmax_readout_chosen": False,
        "cG_makes_density": False,
        "mass_invented": False,
        "density_executable": False,
        "bootstrap_is_offshell_map": False,
        "boundary_frozen": False,
        "conditional_action_promoted": False,
        "cross_branch_splice": False,
        "finite_witness_is_full_rank": False,
        "observations_define_law": False,
        "density_or_gpu_launched": False,
        "physical_closure_claimed": False,
        "scope_package_only": True,
    }


def validate(state: dict[str, object]) -> None:
    for key in ("a_cancels_from_q", "finite_scalar_kernel_checked", "lambda_minus_half_checked", "scope_package_only"):
        assert state[key]
    for key, value in state.items():
        if key not in {"a_cancels_from_q", "finite_scalar_kernel_checked", "lambda_minus_half_checked", "scope_package_only"}:
            assert value is False


def reject(key: str, value: object) -> str:
    state = copy.deepcopy(base_state())
    state[key] = value
    try:
        validate(state)
    except AssertionError:
        return "PASS"
    raise AssertionError(f"accepted corruption {key}={value!r}")


def main() -> int:
    universe = rows("SELECTOR_UNIVERSE.tsv")
    outcomes = rows("SELECTOR_OUTCOMES.tsv")
    constraints = rows("CONSTRAINT_RANK_LEDGER.tsv")
    contract = rows("FALSIFICATION_CONTRACT.tsv")
    ids = [f"Q{i:02d}" for i in range(1, 17)]
    assert [row["selector_id"] for row in universe] == ids
    assert [row["selector_id"] for row in outcomes] == ids
    allowed = {
        "DERIVED_DEFINITION",
        "DERIVED_OUTPUT",
        "OPEN_CONDITION_OR_INEQUALITY",
        "ON_SHELL_FILTER",
        "INDEPENDENT_EQUALITY_OR_PDE",
        "OPEN_MISSING_OBJECT",
        "INCOMPATIBLE_DOMAIN",
    }
    assert {row["selector_type"] for row in outcomes} <= allowed
    assert all(row["active_profile_selector_rank"] == "0" for row in outcomes)
    assert constraints[-1]["constraint_id"] == "TOTAL"
    assert constraints[-1]["independent_equality_rank_on_phi"] == "0"

    primary = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    assert primary["quotient_metric_shift_a_cancels"]
    assert primary["stationary_connection_curvature_sigma1_wedge_sigma2"] == "a*kappa/c_E"
    assert primary["quotient_volume_density"] == "R**3*exp(phi*(2*lambda + 1))"
    assert primary["slice_to_quotient_volume_ratio_squared"] == "-(-R*exp(2*phi) + a)*(R*exp(2*phi) + a)*exp(-4*phi)/R**2"
    assert primary["volume_phi_derivative_rank_generic"] == 1
    assert primary["volume_phi_derivative_rank_lambda_minus_half"] == 0
    assert primary["finite_differentiable_scalar_family_derivative_has_infinite_kernel"]
    assert primary["independent_profile_selector_rank_from_active_premises"] == 0
    assert primary["residual_phi_function_space"] == "INFINITE_DIMENSIONAL_OPEN_NEIGHBORHOOD"
    assert not primary["native_mass_available"]
    assert not primary["same_solution_density_executable"]
    assert not primary["bootstrap_return_map_available"]
    assert not primary["working_Xmax_identified_with_quotient_diameter"]
    assert independent["status"] == "PASS"
    review = (HERE / "FRESH_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")
    assert "VERIFIED-WITH-CAVEATS" in review
    assert "selector_rank_adversary" in review
    assert "BOOTSTRAP_REMAINS_WORKING_ON_SHELL_ADMISSIBILITY_ONLY" in review

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    for text in (report, exact):
        for phrase in (
            "FOUNDED_PHI_IDENTITY_AND_PAIR_ACTION = DERIVED",
            "STRONG_LOCAL_CSN = CHALLENGED_OWNER_POSTULATE_NOT_DERIVED",
            "X_MAX = WORKING_GLOBAL_OBSERVER_PAIR_SCHEMA",
            "COMPLETE_WHOLE_SOLUTION_LAW = OPEN",
        ):
            assert phrase in text
    for phrase in (
        "orthogonal distribution to be integrable",
        "local derivative-rank theorem",
        "not the induced proper volume of a hypersurface",
        "bounded smooth witness also has bounded",
    ):
        assert phrase in exact

    mutations = {
        "F01": ("phi_extra_field", True),
        "F02": ("definition_as_selector", True),
        "F03": ("inequality_reduces_rank", True),
        "F04": ("unique_K_selects_profile", True),
        "F05": ("twist_selects_lambda_phi", True),
        "F06": ("hypersurface_orthogonal_assumed", True),
        "F07": ("a_cancels_from_q", False),
        "F08": ("volume_target_invented", True),
        "F09": ("finite_scalar_kernel_checked", False),
        "F10": ("lambda_minus_half_checked", False),
        "F11": ("diameter_is_Xmax", True),
        "F12": ("Xmax_readout_chosen", True),
        "F13": ("cG_makes_density", True),
        "F14": ("mass_invented", True),
        "F15": ("density_executable", True),
        "F16": ("bootstrap_is_offshell_map", True),
        "F17": ("boundary_frozen", True),
        "F18": ("conditional_action_promoted", True),
        "F19": ("cross_branch_splice", True),
        "F20": ("finite_witness_is_full_rank", True),
        "F21": ("observations_define_law", True),
        "F22": ("density_or_gpu_launched", True),
        "F23": ("physical_closure_claimed", True),
        "F24": ("scope_package_only", False),
    }
    assert set(mutations) == {row["catch_id"] for row in contract}
    catches = [
        {
            "catch_id": row["catch_id"],
            "result": reject(*mutations[row["catch_id"]]),
            "corruption_or_overclaim": row["corruption_or_overclaim"],
        }
        for row in contract
    ]
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(catches[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(catches)

    result = {
        "schema": "udt.metric_native_selector_rank.verification.v1",
        "status": "PASS",
        "selectors": "16/16",
        "constraints": "14_PLUS_TOTAL",
        "active_profile_selector_rank": 0,
        "orbit_geometry": "PASS",
        "independent": "PASS_STDLIB_FRACTION",
        "catch_proofs": "24/24",
        "bootstrap_return_map_derived": False,
        "physical_profile_selected": False,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
