#!/usr/bin/env python3
"""Fail-closed verifier for the finite-cell quotient-reduction audit."""

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


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_json(name: str, no_site: bool = False):
    command = [sys.executable]
    if no_site:
        command.append("-S")
    command.append(str(ROOT / name))
    completed = subprocess.run(
        command,
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if completed.stderr:
        raise AssertionError(f"unexpected stderr from {name}: {completed.stderr}")
    return json.loads(completed.stdout)


def claim_contract(value: dict[str, object]) -> bool:
    return (
        value.get("branch_count") == 16
        and value.get("completion_count") == 12
        and value.get("quotient_status") == "OPEN_CONDITIONAL"
        and value.get("global_screen_status") == "DERIVED_GIVEN_CONFIGURATION"
        and value.get("w_status") == "METRIC_GAUGE_ISOTROPIC_UNMIXED_ONLY"
        and value.get("flag_status") == "OPEN_NOT_SELECTED"
        and value.get("projected_connection_status") == "METRIC_CANONICAL_PHYSICAL_ROLE_OPEN"
        and value.get("ambient_connection_status") == "NOT_SCREEN_PRESERVING"
        and value.get("endpoint_status") == "PATH_LABELLED_ONLY"
        and value.get("reduced_survivor_status") == "NOT_FULL_FOUNDED_PAIR"
        and value.get("other_completions") == "STRUCTURAL_NO_CONCRETE_METRIC"
        and value.get("lambda_status") == "OPEN_NOT_SELECTED"
        and value.get("cross_branch_splice") is False
    )


def main() -> None:
    checks: dict[str, str] = {}

    def check(name: str, condition: bool) -> None:
        if not condition:
            raise AssertionError(name)
        checks[name] = "PASS"

    branch_universe = rows("BRANCH_UNIVERSE.tsv")
    branch_outcomes = rows("BRANCH_OUTCOMES.tsv")
    expected_branches = {f"B{i:02d}" for i in range(1, 17)}
    check("corrected_branch_universe_exact", len(branch_universe) == 16 and {row["branch_id"] for row in branch_universe} == expected_branches)
    check("branch_outcomes_complete", len(branch_outcomes) == 16 and {row["branch_id"] for row in branch_outcomes} == expected_branches)
    check("branch_names_stable", {row["branch_id"] for row in branch_universe} == {row["branch_id"] for row in branch_outcomes})
    check("distinct_B16_present", next(row for row in branch_universe if row["branch_id"] == "B16")["registered_branch_or_stratum"] == "TWISTED_S3_EXACT_UNIQUE_K_LAMBDA_TWO_THIRDS")

    completion_universe = rows("COMPLETION_UNIVERSE.tsv")
    completion_outcomes = rows("COMPLETION_OUTCOMES.tsv")
    completion_ids = {row["completion_id"] for row in completion_universe}
    check("completion_universe_exact", len(completion_universe) == 12 and len(completion_ids) == 12)
    check("completion_outcomes_complete", len(completion_outcomes) == 12 and {row["completion_id"] for row in completion_outcomes} == completion_ids)
    concrete = [row for row in completion_outcomes if row["concrete_all_gate_metric"].startswith("YES")]
    check("only_FC04_has_concrete_all_gate_metric", len(concrete) == 1 and concrete[0]["completion_id"] == "FC04_TWO_CAP_P1")

    production = load(ROOT / "DERIVATION_RESULT.json")
    independent = load(ROOT / "INDEPENDENT_RESULT.json")
    check("production_pass", production["result"] == "PASS" and production["check_count"] == 42 and set(production["checks"].values()) == {"PASS"})
    check("independent_pass", independent["result"] == "PASS" and independent["check_count"] == 21 and set(independent["checks"].values()) == {"PASS"})
    check("independent_separate", independent["implementation"] == "stdlib_Fraction_no_sympy_no_production_import")
    check("production_independent_core_agreement", production["counts"]["intrinsic_screen_rank"] == independent["controls"]["screen_rank"] == 2 and production["counts"]["full_Lorentz_centralizer_dimension"] == independent["controls"]["full_Lorentz_centralizer_dimension"] == 1)
    check("production_replay", run_json("derive_finite_cell_reduction.py") == production)
    check("independent_replay", run_json("verify_finite_cell_reduction_independent.py", no_site=True) == independent)

    # Independently check load-bearing frozen parent evidence rather than only
    # trusting prose in the new report.
    holonomy = load(REPO / "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27" / "DERIVATION_RESULT.json")
    screen_parent = load(REPO / "udt_twisted_s3_intrinsic_screen_cocycle_audit_2026-07-27" / "DERIVATION_RESULT.json")
    killing = load(REPO / "udt_twisted_s3_killing_algebra_audit_2026-07-27" / "DERIVATION_RESULT.json")
    check("parent_holonomy_rank_six", holonomy["curvature_span_ranks"] == [6] and holonomy["lie_closure_ranks"] == [6])
    check("parent_all_loops_nontrivial", holonomy["loop_transports"] == holonomy["loops_with_nonzero_ordinary_closure_residual"] == 36)
    check("parent_nabla_control", holonomy["exact_P00_nabla_E0_X_0_1"] == "-3/25")
    candidate_parent = {row["candidate"]: row for row in screen_parent["candidate_outcomes"]}
    check("parent_six_intrinsic_screens", all(candidate_parent[f"C{i:02d}"]["intrinsic_screen"] == "PASS_INTRINSIC_RANK_TWO" for i in range(1, 7)))
    check("parent_controls_fail_pair_gate", candidate_parent["C07"]["intrinsic_screen"].startswith("FAIL") and candidate_parent["C08"]["intrinsic_screen"].startswith("FAIL"))
    check("parent_exact_unique_K_witness", killing["invariant_gradient_determinant_nonzero"] is True and killing["stationary_norm_nonconstant"] is True and killing["twist_nonzero_for_nonzero_kappa"] is True)

    layers = {row["layer"]: row["status"] for row in rows("LAYER_OUTCOMES.tsv")}
    check("projected_connection_positive_layer", layers["PROJECTED_SCREEN_CONNECTION"] == "METRIC_CANONICAL_MATHEMATICS")
    check("ambient_restriction_negative_layer", layers["AMBIENT_SCREEN_RESTRICTION"] == "NOT_PARALLEL_ON_NONTRIVIAL_TWISTED_S3")
    check("flag_remains_open", layers["GLOBAL_SCREEN_FLAG"] == "OPEN_NOT_DERIVED")
    check("physical_selection_remains_open", layers["PHYSICAL_SELECTION"] == "OPEN")

    exact_text = (ROOT / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    next_text = (ROOT / "NEXT_STEP.md").read_text(encoding="utf-8")
    for token in (
        "D_X s = H(nabla_X s)",
        "A -> A+d alpha",
        "PATH_LABELLED_ONLY",
        "conditional branchwise construction",
        "no flag is required",
    ):
        check(f"exact_token_{token}", token in exact_text)
    check("next_step_is_variation_not_action", "variation-domain and bundle-stratification audit" in next_text and "not an action search" in next_text)

    base: dict[str, object] = {
        "branch_count": 16,
        "completion_count": 12,
        "quotient_status": "OPEN_CONDITIONAL",
        "global_screen_status": "DERIVED_GIVEN_CONFIGURATION",
        "w_status": "METRIC_GAUGE_ISOTROPIC_UNMIXED_ONLY",
        "flag_status": "OPEN_NOT_SELECTED",
        "projected_connection_status": "METRIC_CANONICAL_PHYSICAL_ROLE_OPEN",
        "ambient_connection_status": "NOT_SCREEN_PRESERVING",
        "endpoint_status": "PATH_LABELLED_ONLY",
        "reduced_survivor_status": "NOT_FULL_FOUNDED_PAIR",
        "other_completions": "STRUCTURAL_NO_CONCRETE_METRIC",
        "lambda_status": "OPEN_NOT_SELECTED",
        "cross_branch_splice": False,
    }
    check("base_claim_contract", claim_contract(base))
    mutations = {
        "promote_quotient_semantics": ("quotient_status", "DERIVED_PHYSICAL"),
        "drop_corrected_B16": ("branch_count", 15),
        "call_global_coframe_metric_flag": ("flag_status", "DERIVED_FROM_COFRAME"),
        "call_w_physical_on_isotropic": ("w_status", "ALWAYS_PHYSICAL"),
        "call_w_gauge_on_anisotropic": ("w_status", "ALWAYS_GAUGE"),
        "deny_global_screen_from_holonomy": ("global_screen_status", "ABSENT_FULL_HOLONOMY"),
        "call_ambient_connection_screen_closed": ("ambient_connection_status", "SCREEN_PRESERVING"),
        "deny_projected_screen_connection": ("projected_connection_status", "ABSENT"),
        "promote_projected_connection_physical": ("projected_connection_status", "DERIVED_PHYSICAL"),
        "promote_endpoint_descent": ("endpoint_status", "PATH_INDEPENDENT"),
        "promote_lambda_plus1_full_pair": ("reduced_survivor_status", "FULL_FOUNDED_PAIR"),
        "invent_other_completion_metrics": ("other_completions", "CONCRETE"),
        "splice_branches": ("cross_branch_splice", True),
        "select_lambda": ("lambda_status", "SELECTED_MINUS2"),
    }
    catches = {}
    for name, (key, replacement) in mutations.items():
        mutated = copy.deepcopy(base)
        mutated[key] = replacement
        if claim_contract(mutated):
            raise AssertionError(f"mutation escaped: {name}")
        catches[name] = "PASS"
    check("all_mutations_caught", len(catches) == 14 and set(catches.values()) == {"PASS"})
    catch_rows = rows("CATCH_PROOFS.tsv")
    check("catch_table_matches", {row["catch_id"] for row in catch_rows} == set(catches) and all(row["result"] == "PASS" for row in catch_rows))
    check("source_scope_exists", all((REPO / row["path"]).is_file() for row in rows("SOURCE_SCOPE.tsv")))

    expected_check_count = 34
    check("registered_verifier_check_count_before_count_check", len(checks) == expected_check_count - 1)
    if len(checks) != expected_check_count:
        raise AssertionError(f"unexpected verifier check count {len(checks)}")

    result = {
        "schema": "udt.finite_cell_reciprocal_quotient_reduction.verification.v1",
        "result": "PASS",
        "check_count": len(checks),
        "checks": checks,
        "catch_count": len(catches),
        "catch_proofs": catches,
        "branch_count": len(branch_universe),
        "completion_count": len(completion_universe),
        "production_check_count": production["check_count"],
        "independent_check_count": independent["check_count"],
        "maximum_conclusion_enforced": production["maximum_conclusion"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
