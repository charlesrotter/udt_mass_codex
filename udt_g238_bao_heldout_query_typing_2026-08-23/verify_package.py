#!/usr/bin/env python3
"""Fail-closed structural verifier for the G238 query-typing package."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path

import derive_query_typing


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_payload(
    state: dict[str, object],
    result: dict[str, object],
    ledger: list[dict[str, str]],
    source_hashes_valid: bool,
) -> None:
    state_values = state["state"]
    assert source_hashes_valid
    assert state["resolution"] == 12
    assert len(state_values["knots"]) == 12
    assert len(state_values["relative_R"]) == 11
    assert all(value > 0 for value in state_values["relative_R"])
    forbidden_fields = {"interpolation", "derivatives", "absolute_scale", "metric_history"}
    assert not forbidden_fields.intersection(state)
    assert not forbidden_fields.intersection(state_values)
    assert result["boss_outcomes_opened"] is False
    assert result["profile_or_feature_fit_performed"] is False
    assert result["source_hashes_verified"] == 15
    assert result["operator_ledger_rows"] == 15
    assert result["counterfamily"]["all_knot_values_zero"] is True
    for key in ("q", "q_prime", "q_second"):
        assert int(result["counterfamily"][key]["numerator"]) != 0
    expected_landing = (
        "QUERY_TYPING_INCOMPLETE__NO_OUTCOME_OPENING"
        "__FROZEN_SNE_STATE_DOES_NOT_DETERMINE_CONTINUOUS_METRIC_OR_SCREEN_HISTORY"
        "__COMPLETE_METRIC_EVALUATORS_REMAIN_LIVE_CONDITIONALLY"
        "__TWO_SOURCE_POPULATION_AND_REFERENCE_FORWARD_MAP_OPEN"
    )
    assert result["landing"] == expected_landing
    by_stage = {row["stage"]: row for row in ledger}
    assert len(ledger) == 15 and len(by_stage) == 15
    for stage in ("Q02", "Q03", "Q04", "Q09", "Q10", "Q11"):
        assert by_stage[stage]["status"] == "OPEN"
    assert by_stage["Q15"]["status"] == "QUERY_TYPING_INCOMPLETE"
    for stage in ("Q05", "Q06", "Q07"):
        assert "DERIVED_CONDITIONAL" in by_stage[stage]["status"]
    joined = json.dumps({"result": result, "ledger": ledger})
    for forbidden in ("OWNED_NO_REFIT_BAO_FORWARD_OPERATOR", "preferred_BOSS_feature", "P1_profile"):
        assert forbidden not in joined


def load_actual() -> tuple[dict[str, object], dict[str, object], list[dict[str, str]], bool]:
    state = json.loads(
        (
            ROOT
            / "udt_g237_dual_sne_joint_relational_state_freeze_2026-08-23"
            / "FROZEN_PRIMARY_K12_STATE.json"
        ).read_text()
    )
    result = json.loads((PACKAGE / "DERIVATION_RESULT.json").read_text())
    ledger = list(csv.DictReader((PACKAGE / "OPERATOR_TYPE_LEDGER.tsv").open(), delimiter="\t"))
    rows = list(csv.DictReader((PACKAGE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
    sources_valid = all((ROOT / row["path"]).is_file() and digest(ROOT / row["path"]) == row["sha256"] for row in rows)
    return state, result, ledger, sources_valid


def main() -> None:
    state, result, ledger, sources_valid = load_actual()
    validate_payload(state, result, ledger, sources_valid)
    recomputed = derive_query_typing.derive()
    assert recomputed == result
    output = {
        "audit": "G238_PACKAGE_VERIFICATION",
        "status": "PASS",
        "checks": {
            "source_hashes": True,
            "frozen_state_shape_and_scope": True,
            "exact_counterfamily": True,
            "fifteen_stage_operator_ledger": True,
            "conditional_metric_evaluators_retained": True,
            "open_continuation_two_source_population_and_reference_gates": True,
            "boss_outcomes_closed": True,
            "profile_and_feature_fit_absent": True,
            "saved_result_matches_fresh_recomputation": True,
        },
    }
    (PACKAGE / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
