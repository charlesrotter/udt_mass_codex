#!/usr/bin/env python3
"""Fail-closed semantic and mutation verifier for the neighborhood audit."""

from __future__ import annotations

import copy
import csv
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load() -> dict[str, object]:
    return {
        "result": json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8")),
        "independent": json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8")),
        "centers": rows("CENTER_NEIGHBORHOOD_ATLAS.tsv"),
        "candidates": rows("CANDIDATE_UNIVERSE.tsv"),
        "subfamilies": rows("EXACT_SUBFAMILY_ATLAS.tsv"),
        "walls": rows("DEGENERACY_WALL_ATLAS.tsv"),
        "openness": rows("FUNCTIONAL_OPENNESS_GATES.tsv"),
        "premises": rows("PREMISE_LEDGER.tsv"),
        "status": rows("STATUS_LEDGER.tsv"),
        "local": rows("LOCAL_RESPONSE_FORMULAS.tsv"),
        "sources": rows("SOURCE_MANIFEST.tsv"),
    }


def validate(state: dict[str, object]) -> None:
    result = state["result"]
    independent = state["independent"]
    centers = state["centers"]
    candidates = state["candidates"]
    subfamilies = state["subfamilies"]
    walls = state["walls"]
    openness = state["openness"]
    premises = state["premises"]
    status = state["status"]
    local = state["local"]
    sources = state["sources"]
    assert isinstance(result, dict) and result["status"] == "PASS", "derivation status"
    assert isinstance(independent, dict) and independent["status"] == "PASS", "independent status"
    assert independent["implementation"].startswith("stdlib_Fraction_full_exterior"), "independence"
    assert independent["check_count"] == 49, "independent check count"

    assert isinstance(centers, list)
    center_ids = [row["center"] for row in centers]
    assert center_ids == [f"C{index:02d}" for index in range(1, 7)], "center identity/order"
    assert len(center_ids) == len(set(center_ids)) == 6, "center uniqueness"
    for row in centers:
        assert F(row["clock_certificate_determinant"]) != 0, "zero clock certificate"
        assert F(row["relative_curvature_W23"]) != 0, "zero center response"
        assert row["functional_neighborhood"].startswith("OPEN_IN_C3"), "not functional-open"
        assert "OFFSHELL" in row["maximum_status"], "center promoted on shell"
    assert result["center_count"] == result["functional_open_neighborhood_count"] == 6, "result counts"
    assert result["equal_screen_W23"] == "(9*lambda**2 + 2500)/2500", "equal formula"
    assert result["equal_screen_global_minimum"] == "1", "equal minimum"
    assert result["all_centers_clock_certificate_nonzero"] is True, "clock flag"
    assert result["all_centers_relative_curvature_nonzero"] is True, "response flag"
    for forbidden in ("action_used", "carrier_used", "bootstrap_used", "on_shell_claimed"):
        assert result[forbidden] is False, f"forbidden promotion {forbidden}"
    assert result["external_semantic_review"] == "OPEN_NOT_AUTHORIZED", "external review promotion"
    maximum = result["maximum_conclusion"]
    assert "OFFSHELL" in maximum and "UNIVERSAL" not in maximum and "STABLE" not in maximum, "scope wording"

    assert isinstance(candidates, list) and len(candidates) == 18, "candidate universe count"
    candidate_ids = [row["candidate_id"] for row in candidates]
    assert len(candidate_ids) == len(set(candidate_ids)), "duplicate candidate"
    assert {f"N{index:02d}" for index in range(1, 7)} <= set(candidate_ids), "missing neighborhood"
    by_candidate = {row["candidate_id"]: row for row in candidates}
    assert "full_GL2" in by_candidate["N01"]["free_data"], "full screen omitted"
    assert "mu;nu" in by_candidate["E04"]["free_data"], "two shear omitted"
    assert by_candidate["C07"]["question"] == "metric_results_gauge_invariant", "gauge typing"

    assert isinstance(openness, list) and len(openness) == 5, "openness gate count"
    gate_names = {row["gate"] for row in openness}
    assert gate_names == {
        "CLOCK_CERTIFICATE",
        "TWIST_SELECTED_RULER",
        "RANK1_PROJECTOR_AND_RANK2_COMPLEMENT",
        "GLOBAL_CONFIGURATION_AND_POSITIVE_SLICE",
        "NONZERO_RELATIVE_CURVATURE_SOMEWHERE",
    }, "openness gate identity"

    assert isinstance(subfamilies, list) and len(subfamilies) == 4, "subfamily count"
    by_family = {row["family"]: row for row in subfamilies}
    assert by_family["E01_EQUAL_SCREEN"]["north_event_zero_locus"] == "EMPTY_BECAUSE_W23_GE_1", "equal zero"
    assert by_family["E02_ONE_SHEAR_S1"]["north_event_zero_locus"] == "lambda=25/2;mu=-125/6", "S1 wall"
    assert by_family["E03_ONE_SHEAR_S2"]["north_event_zero_locus"] == "lambda=-200/9;nu=-250/9", "S2 wall"
    assert by_family["E04_TWO_SHEAR_SYMMETRIC"]["north_event_zero_locus"] == "lambda=5nu/4+25/2;mu=-3nu/4-125/6", "two shear wall"
    assert by_family["E02_ONE_SHEAR_S1"]["classification"].startswith("ONE_ISOLATED"), "S1 zero erased"
    assert by_family["E03_ONE_SHEAR_S2"]["classification"].startswith("ONE_ISOLATED"), "S2 zero erased"

    assert isinstance(walls, list)
    wall_names = {row["wall"] for row in walls}
    assert wall_names == {
        "SCREEN_RANK",
        "DISPLAYED_SLICE",
        "TWIST_RULER",
        "CLOCK_CERTIFICATE",
        "LOCAL_RESPONSE_CERTIFICATE",
        "SYMMETRIC_TWO_SHEAR_P00",
        "POLAR_SHEAR_AXIS",
    }, "wall census"
    by_wall = {row["wall"]: row for row in walls}
    assert by_wall["CLOCK_CERTIFICATE"]["overclaim_guard"] == "INTRINSIC_CLOCK_MAY_STILL_EXIST", "certificate conflation"
    assert by_wall["LOCAL_RESPONSE_CERTIFICATE"]["overclaim_guard"] == "MAY_BE_NONZERO_ELSEWHERE", "local/global conflation"

    assert isinstance(local, list)
    assert {row["object"] for row in local} == {"W01", "W02", "W03", "W12", "W13", "W23"}, "local formula set"
    assert all(row["complete_gate"] == "W12=W13=W23=0_AT_EVENT" for row in local), "complete response gate"

    assert isinstance(premises, list) and len(premises) == 19, "premise count"
    by_premise = {row["premise_id"]: row for row in premises}
    assert by_premise["P06"]["status"] == "free-and-explored", "screen not free"
    assert by_premise["P15"]["status"] == "POSIT_EXCLUDED", "carrier imported"
    assert by_premise["P16"]["status"] == "CONDITIONAL_EXCLUDED", "action imported"
    assert "EXCLUDED_FROM_MAP" in by_premise["P17"]["status"], "bootstrap imported"

    assert isinstance(status, list) and len(status) == 15, "status count"
    by_status = {row["claim_id"]: row for row in status}
    assert by_status["S13"]["status"] == "OPEN_NOT_RUN", "bootstrap run claimed"
    assert by_status["S14"]["status"] == "OPEN", "stability promoted"
    assert by_status["S15"]["status"] == "OPEN_NOT_AUTHORIZED", "review promoted"

    assert isinstance(sources, list) and len(sources) == 15, "source count"
    assert len({row["path"] for row in sources}) == 15, "source duplicate"
    assert all(row["unchanged_at_freeze"] == "YES" for row in sources), "source drift at freeze"


def main() -> int:
    baseline = load()
    validate(baseline)
    catches: list[dict[str, str]] = []

    def catch(name: str, mutate) -> None:
        state = copy.deepcopy(baseline)
        mutate(state)
        try:
            validate(state)
        except (AssertionError, KeyError, ValueError) as error:
            catches.append({"catch_id": f"M{len(catches) + 1:02d}", "mutation": name, "result": "CAUGHT", "reason": str(error)})
            return
        raise AssertionError(f"mutation escaped: {name}")

    catch("missing_center", lambda s: s["centers"].pop())
    catch("duplicate_center", lambda s: s["centers"].__setitem__(5, copy.deepcopy(s["centers"][4])))
    catch("zero_clock_determinant", lambda s: s["centers"][0].__setitem__("clock_certificate_determinant", "0"))
    catch("zero_center_response", lambda s: s["centers"][0].__setitem__("relative_curvature_W23", "0"))
    catch("functional_neighborhood_removed", lambda s: s["centers"][0].__setitem__("functional_neighborhood", "POINT_ONLY"))
    catch("full_screen_candidate_removed", lambda s: next(row for row in s["candidates"] if row["candidate_id"] == "N01").__setitem__("free_data", "delta_phi_C3;trace_screen_only"))
    catch("two_shear_omitted", lambda s: next(row for row in s["candidates"] if row["candidate_id"] == "E04").__setitem__("free_data", "lambda;mu"))
    catch("gauge_called_metric_mode", lambda s: next(row for row in s["candidates"] if row["candidate_id"] == "C07").__setitem__("question", "extra_metric_mode"))
    catch("wall_removed", lambda s: s["walls"].pop())
    catch("certificate_wall_called_no_clock", lambda s: next(row for row in s["walls"] if row["wall"] == "CLOCK_CERTIFICATE").__setitem__("overclaim_guard", "NO_INTRINSIC_CLOCK"))
    catch("local_wall_called_global", lambda s: next(row for row in s["walls"] if row["wall"] == "LOCAL_RESPONSE_CERTIFICATE").__setitem__("overclaim_guard", "ZERO_EVERYWHERE"))
    catch("action_injected", lambda s: s["result"].__setitem__("action_used", True))
    catch("carrier_injected", lambda s: s["result"].__setitem__("carrier_used", True))
    catch("bootstrap_injected", lambda s: s["result"].__setitem__("bootstrap_used", True))
    catch("on_shell_promoted", lambda s: s["result"].__setitem__("on_shell_claimed", True))
    catch("universal_wording", lambda s: s["result"].__setitem__("maximum_conclusion", "UNIVERSAL_STABLE_PROJECTOR"))
    catch("equal_screen_formula_changed", lambda s: s["result"].__setitem__("equal_screen_W23", "1"))
    catch("S1_zero_erased", lambda s: next(row for row in s["subfamilies"] if row["family"] == "E02_ONE_SHEAR_S1").__setitem__("classification", "NONZERO_EVERYWHERE"))
    catch("S2_zero_erased", lambda s: next(row for row in s["subfamilies"] if row["family"] == "E03_ONE_SHEAR_S2").__setitem__("north_event_zero_locus", "EMPTY"))
    catch("two_shear_line_changed", lambda s: next(row for row in s["subfamilies"] if row["family"] == "E04_TWO_SHEAR_SYMMETRIC").__setitem__("north_event_zero_locus", "mu=nu=0"))
    catch("W23_formula_removed", lambda s: s["local"].pop())
    catch("component_used_as_complete_gate", lambda s: s["local"][0].__setitem__("complete_gate", "W23=0"))
    catch("independent_replay_failed", lambda s: s["independent"].__setitem__("status", "FAIL"))
    catch("external_review_falsely_closed", lambda s: s["result"].__setitem__("external_semantic_review", "PASS"))

    assert len(catches) == 24 and all(row["result"] == "CAUGHT" for row in catches)
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(catches[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(catches)
    result = {
        "schema": "udt.projector_deformation_neighborhood.verification.v1",
        "status": "PASS",
        "semantic_checks": "FAIL_CLOSED",
        "mutation_catches": len(catches),
        "independent_checks": baseline["independent"]["check_count"],
        "centers": len(baseline["centers"]),
        "functional_openness_gates": len(baseline["openness"]),
        "walls": len(baseline["walls"]),
        "fresh_external_semantic_review": "OPEN_NOT_AUTHORIZED",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
