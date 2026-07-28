#!/usr/bin/env python3
"""Fail-closed verifier for the finite reciprocal quotient-lift audit."""

from __future__ import annotations

import copy
import csv
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def rows(name: str) -> list[dict[str, str]]:
    with (ROOT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def run_json(name: str):
    completed = subprocess.run(
        [sys.executable, str(ROOT / name)],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if completed.stderr:
        raise AssertionError(f"unexpected stderr from {name}: {completed.stderr}")
    return json.loads(completed.stdout)


def claims_valid(value: dict[str, object]) -> bool:
    return (
        value.get("exact_quotient_physical_status") == "OPEN_NOT_SELECTED"
        and value.get("complete_group_law_status") == "OPEN_CONDITIONAL_PREMISE"
        and value.get("quotient_group_parameters") == 8
        and value.get("first_response_rank") == 7
        and value.get("fixed_response_fiber") == 1
        and value.get("screen_flag_status") == "OPEN_NOT_SELECTED"
        and value.get("gauge_stratum") == "C=0_AND_S=lambda*I"
        and value.get("generic_rotation_status") == "INEQUIVALENT_FINITE_METRIC_DATA"
        and value.get("isotropic_unmixed_status") == "REPRESENTATIVE_FREEDOM"
        and value.get("self_adjoint_status") == "QUOTIENT_ONLY_IF_C_ZERO"
        and value.get("seal_selector_rank") == 0
        and value.get("global_status") == "OPEN"
    )


def main() -> None:
    checks: dict[str, str] = {}

    def check(name: str, condition: bool) -> None:
        if not condition:
            raise AssertionError(name)
        checks[name] = "PASS"

    candidates = rows("CANDIDATE_UNIVERSE.tsv")
    outcomes = rows("CANDIDATE_OUTCOMES.tsv")
    expected_ids = {f"Q{i:02d}" for i in range(1, 13)}
    check("candidate_universe_exact", {row["candidate_id"] for row in candidates} == expected_ids and len(candidates) == 12)
    check("candidate_outcomes_complete", {row["candidate_id"] for row in outcomes} == expected_ids and len(outcomes) == 12)
    check("candidate_names_stable", {row["candidate_id"]: row["candidate"] for row in candidates} == {row["candidate_id"]: row["candidate"] for row in outcomes})

    production = load("DERIVATION_RESULT.json")
    independent = load("INDEPENDENT_RESULT.json")
    check("production_pass", production["result"] == "PASS" and production["check_count"] == 42 and set(production["checks"].values()) == {"PASS"})
    check("independent_pass", independent["result"] == "PASS" and independent["check_count"] == 18 and set(independent["checks"].values()) == {"PASS"})
    check("independent_implementation_separate", independent["implementation"] == "stdlib_Fraction_no_sympy_no_production_import")
    check("rank_agreement", production["counts"]["complete_group_generator_parameters"] == independent["ranks"]["quotient_group_generators"] == 8 and production["counts"]["complete_group_first_metric_response_rank"] == independent["ranks"]["first_metric_response"] == 7 and production["counts"]["fixed_response_generator_fiber_dimension"] == independent["ranks"]["fixed_response_kernel"] == 1)

    replay_production = run_json("derive_finite_quotient_lifts.py")
    replay_independent = run_json("verify_finite_quotient_lifts_independent.py")
    check("production_replay_byte_semantics", replay_production == production)
    check("independent_replay_byte_semantics", replay_independent == independent)

    status = {row["object"]: row["status"] for row in rows("STATUS_LEDGER.tsv")}
    check("physical_quotient_remains_open", status["exact_complete_quotient_semantics"] == "OPEN")
    check("global_flag_remains_open", status["global_screen_flag"] == "OPEN")
    check("downstream_objects_remain_open", status["action_source_boundary_carrier_bootstrap_Xmax_mass_dynamics"] == "OPEN")
    check("triangular_chart_conditional", status["positive_triangular_seven_parameter_chart"] == "CONDITIONAL")

    completeness = rows("COMPLETENESS_MAP.tsv")
    check("completeness_one_row_per_candidate", len(completeness) == 12 and {row["candidate_id"] for row in completeness} == expected_ids)
    check("completeness_all_classified", all(row["classified"] == "YES" for row in completeness))
    check("source_scope_exists", all((REPO / row["path"]).is_file() for row in rows("SOURCE_SCOPE.tsv")))

    derivation_text = (ROOT / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    next_text = (ROOT / "NEXT_STEP.md").read_text(encoding="utf-8")
    for token in (
        "DERIVED_IF_EXACT_QUOTIENT",
        "DERIVED_IF_COMPLETE_GROUP_LAW",
        "CONDITIONAL_ON_SCREEN_FLAG",
        "C=0 and S=lambda I",
        "physical quotient semantics",
    ):
        check(f"derivation_token_{token}", token in derivation_text)
    check("next_step_fail_closed_on_quotient_semantics", "stop at that earlier gate" in next_text)

    base_claims: dict[str, object] = {
        "exact_quotient_physical_status": "OPEN_NOT_SELECTED",
        "complete_group_law_status": "OPEN_CONDITIONAL_PREMISE",
        "quotient_group_parameters": 8,
        "first_response_rank": 7,
        "fixed_response_fiber": 1,
        "screen_flag_status": "OPEN_NOT_SELECTED",
        "gauge_stratum": "C=0_AND_S=lambda*I",
        "generic_rotation_status": "INEQUIVALENT_FINITE_METRIC_DATA",
        "isotropic_unmixed_status": "REPRESENTATIVE_FREEDOM",
        "self_adjoint_status": "QUOTIENT_ONLY_IF_C_ZERO",
        "seal_selector_rank": 0,
        "global_status": "OPEN",
    }
    check("base_claim_contract", claims_valid(base_claims))
    mutations = {
        "promote_quotient_to_physical": ("exact_quotient_physical_status", "DERIVED_PHYSICAL"),
        "inherit_complete_group_law_silently": ("complete_group_law_status", "DERIVED_FROM_PAIR"),
        "drop_eighth_generator": ("quotient_group_parameters", 7),
        "claim_unique_fixed_response_lift": ("fixed_response_fiber", 0),
        "select_triangular_flag": ("screen_flag_status", "DERIVED_UPPER"),
        "call_rotation_always_gauge": ("generic_rotation_status", "REPRESENTATIVE_FREEDOM"),
        "call_rotation_always_physical": ("isotropic_unmixed_status", "INEQUIVALENT_FINITE_METRIC_DATA"),
        "broaden_gauge_stratum": ("gauge_stratum", "S=lambda*I"),
        "call_self_adjoint_general_quotient": ("self_adjoint_status", "GENERAL_QUOTIENT_SELECTOR"),
        "let_seal_select_extension": ("seal_selector_rank", 1),
        "promote_global_section": ("global_status", "DERIVED"),
    }
    catches: dict[str, str] = {}
    for name, (key, replacement) in mutations.items():
        mutated = copy.deepcopy(base_claims)
        mutated[key] = replacement
        if claims_valid(mutated):
            raise AssertionError(f"mutation escaped: {name}")
        catches[name] = "PASS"
    check("all_registered_mutations_caught", len(catches) == 11 and set(catches.values()) == {"PASS"})

    catch_rows = rows("CATCH_PROOFS.tsv")
    check("catch_table_matches_exercised_mutations", {row["catch_id"] for row in catch_rows} == set(catches) and all(row["result"] == "PASS" for row in catch_rows))

    expected_check_count = 26
    check("registered_verifier_check_count_before_count_check", len(checks) == expected_check_count - 1)
    if len(checks) != expected_check_count:
        raise AssertionError(f"unexpected verifier check count {len(checks)}")

    result = {
        "schema": "udt.finite_reciprocal_quotient_lift.verification.v1",
        "result": "PASS",
        "check_count": len(checks),
        "checks": checks,
        "catch_count": len(catches),
        "catch_proofs": catches,
        "candidate_count": len(candidates),
        "production_check_count": production["check_count"],
        "independent_check_count": independent["check_count"],
        "maximum_conclusion_enforced": production["maximum_conclusion"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
