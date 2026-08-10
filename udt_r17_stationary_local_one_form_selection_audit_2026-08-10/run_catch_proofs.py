#!/usr/bin/env python3
"""Exercise fail-closed semantic mutations for the stationary one-form audit."""

from __future__ import annotations

import copy
import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def state() -> dict:
    return {
        "result": json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8")),
        "candidates": rows("ONE_FORM_CLASSIFICATION.tsv"),
        "invariants": rows("INVARIANT_COVECTOR_ATLAS.tsv"),
        "closedness": rows("CLOSEDNESS_ATLAS.tsv"),
        "owners": rows("SELECTION_OWNER_CENSUS.tsv"),
        "status": rows("STATUS_LEDGER.tsv"),
    }


def valid(data: dict) -> bool:
    try:
        result = data["result"]
        candidates = data["candidates"]
        by_id = {row["candidate_id"]: row for row in candidates}
        closed = {row["one_form"]: row for row in data["closedness"]}
        owners = {row["owner_id"]: row for row in data["owners"]}
        status = {row["claim_id"]: row for row in data["status"]}
        return all((
        len(candidates) == len(by_id) == 16,
        set(by_id) == {f"L{i:02d}" for i in range(1, 17)},
        by_id["L01"]["selection_status"] == "SELECTED_ONLY_FOR_ALREADY_OWNED_delta_K",
        by_id["L02"]["closedness"] == "NONCLOSED_FOR_a_POSITIVE",
        by_id["L03"]["metric_ownership"] == "OWNED_WITH_ORIENTATION_LOCAL_SYSTEM",
        by_id["L05"]["closedness"] == "SCALAR_MULTIPLE_OF_L03",
        by_id["L06"]["closedness"] == "E_MEAN_ZERO__H_MEAN_RULER_MULTIPLE",
        "dphi_PLUS_c*dJ_H" in by_id["L07"]["metric_ownership"],
        "ACTUAL_S3_R17_WITNESS" in by_id["L08"]["closedness"],
        by_id["L11"]["selection_status"] == "NOT_ENDPOINT_FRAME_INVARIANT_SCALAR_ONE_FORM",
        "dphi_PLUS_c_Hdphi" in by_id["L13"]["metric_ownership"],
        by_id["L13"]["selection_status"] == "PURE_PAIR_LEAF_REDUCTION_DOES_NOT_FIX_c",
        by_id["L14"]["metric_ownership"] == "SPAN_tau_nu",
        by_id["L16"]["selection_status"] == "NO_PHYSICAL_TRANSGRESSION_OWNER",
        len(data["invariants"]) == 4,
        data["invariants"][0]["rank"] == "2",
        data["invariants"][1]["rank"] == "4",
        len(closed) == 8,
        closed["tau=theta0"]["status"] == "NONCLOSED",
        closed["nu=theta1"]["status"] == "NONCLOSED",
        "NONCLOSED_R17_WITNESS_1_OVER_2" in closed["H*dphi"]["status"],
        "EXACT_FAMILY" in closed["dphi+c*dJ_H"]["status"],
        closed["A"]["status"] == "GAUGE_REPRESENTATIVE",
        len(owners) == 6,
        owners["O06"]["selection_effect"] == "OPEN",
        status["S08"]["status"] == "REFUTED",
        status["S09"]["status"] == "REFUTED",
        status["S12"]["status"] == "NOT_DERIVED",
        result["metric_owned_forms_beyond_dphi"] is True,
        result["distinguished_reciprocal_transgression_beyond_dphi"] is False,
        result["selection_owner"] is None,
        "ALL_REAL_c" in result["pure_pair_leaf_preserving_transgression_family"],
        "DIMENSIONLESS" in result["pure_reciprocal_preserving_exact_family"],
            result["required_new_owner_class"] == "ON_SHELL_EQUATION_OR_GLOBAL_COMPLETION_OR_EXPLICIT_QUERY_MEASUREMENT_PREMISE",
        ))
    except (KeyError, IndexError, StopIteration, TypeError):
        return False


def main() -> int:
    original = state()
    assert valid(original)
    mutations: list[dict[str, str]] = []

    def catch(name, mutate) -> None:
        item = copy.deepcopy(original)
        mutate(item)
        mutations.append({"catch_id": name, "mutation": name, "result": "REJECTED" if not valid(item) else "MISSED"})

    catch("DROP_CANDIDATE", lambda s: s["candidates"].pop())
    catch("DUPLICATE_CANDIDATE", lambda s: s["candidates"].append(copy.deepcopy(s["candidates"][0])))
    catch("DEMOTE_dphi_ENDPOINT_OWNER", lambda s: s["candidates"][0].update(selection_status="UNOWNED"))
    catch("MARK_CLOCK_CLOSED", lambda s: s["candidates"][1].update(closedness="CLOSED"))
    catch("ERASE_RULER_ORIENTATION", lambda s: s["candidates"][2].update(metric_ownership="OWNED_UNORIENTED_SCALAR"))
    catch("INVENT_THIRD_TWIST_DIRECTION", lambda s: s["candidates"][4].update(closedness="INDEPENDENT"))
    catch("INVENT_MEAN_CURVATURE_DIRECTION", lambda s: s["candidates"][5].update(closedness="FULL_NEW_DIRECTION"))
    catch("ERASE_EXACT_ENDPOINT_FAMILY", lambda s: s["candidates"][6].update(metric_ownership="ONLY_dphi"))
    catch("DEMOTE_R17_WITNESS_TO_GENERAL_RECTANGLE", lambda s: s["candidates"][7].update(closedness="GENERAL_CONTROL_ONLY"))
    catch("PROMOTE_CONNECTION_POTENTIAL_TO_SCALAR", lambda s: s["candidates"][10].update(selection_status="GAUGE_INVARIANT_SCALAR"))
    catch("SELECT_c_ZERO_BY_COMPOSITION", lambda s: s["candidates"][12].update(selection_status="c=0_SELECTED"))
    catch("CHANGE_ORDER_ZERO_RANK", lambda s: s["invariants"][0].update(rank="3"))
    catch("CHANGE_GENERIC_FIRST_JET_RANK", lambda s: s["invariants"][1].update(rank="3"))
    catch("MARK_Hdphi_CLOSED", lambda s: next(row for row in s["closedness"] if row["one_form"] == "H*dphi").update(status="CLOSED"))
    catch("ERASE_DIMENSIONLESS_EXACT_FAMILY", lambda s: next(row for row in s["closedness"] if row["one_form"] == "dphi+c*dJ_H").update(status="ABSENT"))
    catch("MARK_A_GAUGE_INVARIANT", lambda s: next(row for row in s["closedness"] if row["one_form"] == "A").update(status="SCALAR"))
    catch("FABRICATE_SELECTION_OWNER", lambda s: s["owners"][5].update(selection_effect="SELECTS_L07"))
    catch("PROMOTE_PHYSICAL_TRANSGRESSION", lambda s: s["result"].update(distinguished_reciprocal_transgression_beyond_dphi=True))
    catch("PROMOTE_SELECTION_OWNER", lambda s: s["result"].update(selection_owner="R17_LOCAL_METRIC"))
    catch("ERASE_REQUIRED_OWNER", lambda s: s["result"].update(required_new_owner_class="NONE"))

    failed = [row for row in mutations if row["result"] != "REJECTED"]
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=("catch_id", "mutation", "result"), lineterminator="\n")
        writer.writeheader()
        writer.writerows(mutations)
    result = {
        "total": len(mutations),
        "rejected": len(mutations) - len(failed),
        "failed": failed,
        "status": "PASS" if not failed else "FAIL",
    }
    (HERE / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
