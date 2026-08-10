#!/usr/bin/env python3
"""Exercise fail-closed semantic mutations for the joint-invariant audit."""

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
        "candidates": rows("JOINT_CANDIDATE_CLASSIFICATION.tsv"),
        "gauge": rows("GAUGE_INVARIANT_QUERY_ATLAS.tsv"),
        "characters": rows("CHARACTER_ATLAS.tsv"),
        "one_forms": rows("LOCAL_ONE_FORM_COCYCLE_ATLAS.tsv"),
    }


def valid(data: dict) -> bool:
    result = data["result"]
    candidates = data["candidates"]
    by_id = {row["candidate_id"]: row for row in candidates}
    return all((
        len(candidates) == len(by_id) == 12,
        set(by_id) == {f"J{i:02d}" for i in range(1, 13)},
        by_id["J01"]["composition"] == "EXACT",
        by_id["J03"]["selection_status"] == "VECTOR_w_MINUS_lambda__COVECTOR_w_PLUS_lambda",
        by_id["J04"]["classification"] == "NO_NONTRIVIAL_OPEN_PATH_ANGLE_SCALAR",
        by_id["J05"]["classification"] == "UNIQUE_NORMALIZED_CONTINUOUS_REAL_CHARACTER_IS_delta",
        by_id["J10"]["composition"] == "DIRECT_PRODUCT_ONLY",
        by_id["J11"]["classification"] == "CONDITIONAL_HIGHER_JET_LINE_INTEGRAL_FAMILY",
        result["continuous_real_character"] == "UNIQUE_NORMALIZED_CHARACTER_IS_delta_K",
        result["angular_real_character"] == "ZERO",
        result["continuous_semidirect_depth_action"] == "TRIVIAL",
        result["open_path_representative_free_angular_scalar"] == "NONE",
        result["complete_coframe_vector_weight"] == "w=-lambda",
        result["complete_coframe_covector_weight"] == "w=+lambda",
        result["joint_path_functor"] == "R_ADDITIVE_TIMES_ORIENTED_NORMAL_ISOMETRY_GROUPOID__LOCALLY_R_TIMES_SO2",
        result["higher_jet_scalar_path_cocycles"] == (
            "LINE_INTEGRALS_COMPOSE__GENERAL_NONEXACT_CONTROL_EXISTS__"
            "STATIONARY_R17_NONEXACT_REALIZATION_OPEN__NO_MEMBER_SELECTED"
        ),
        result["physical_path_or_arrow_selected"] is False,
        "F23=-4097/2048" in result["depth_does_not_determine_holonomy"],
        len(data["gauge"]) == 4,
        len(data["characters"]) == 3,
        len(data["one_forms"]) == 4,
    ))


def main() -> int:
    original = state()
    assert valid(original)
    mutations: list[dict[str, str]] = []

    def catch(name, mutate) -> None:
        item = copy.deepcopy(original)
        mutate(item)
        mutations.append({"catch_id": name, "mutation": name,
                          "result": "REJECTED" if not valid(item) else "MISSED"})

    catch("DROP_CANDIDATE", lambda s: s["candidates"].pop())
    catch("DUPLICATE_CANDIDATE", lambda s: s["candidates"].append(copy.deepcopy(s["candidates"][0])))
    catch("BREAK_JOINT_COMPOSITION", lambda s: s["candidates"][0].update(composition="FAIL"))
    catch("MISTYPE_GLOBAL_ARROW_AS_FIXED_SO2", lambda s: s["result"].update(
        joint_path_functor="R_TIMES_SO2_GLOBAL_GROUP"
    ))
    catch("MUTATE_COFRAME_WEIGHT", lambda s: s["candidates"][2].update(selection_status="w=0"))
    catch("PROMOTE_OPEN_PATH_ANGLE", lambda s: s["candidates"][3].update(classification="ANGLE_INVARIANT"))
    catch("ADD_REAL_ANGULAR_CHARACTER", lambda s: s["result"].update(angular_real_character="NONZERO"))
    catch("PROMOTE_SEMIDIRECT_ACTION", lambda s: s["result"].update(continuous_semidirect_depth_action="NONTRIVIAL"))
    catch("ERASE_HIGHER_JET_FAMILY", lambda s: s["candidates"][10].update(classification="NONE"))
    catch("OVERPROMOTE_STATIONARY_NONEXACTNESS", lambda s: s["result"].update(
        higher_jet_scalar_path_cocycles="STATIONARY_R17_NONEXACT_REALIZATION_DERIVED"
    ))
    catch("SELECT_PHYSICAL_PATH", lambda s: s["result"].update(physical_path_or_arrow_selected=True))
    catch("MUTATE_VECTOR_WEIGHT", lambda s: s["result"].update(complete_coframe_vector_weight="w=+lambda"))
    catch("MUTATE_COVECTOR_WEIGHT", lambda s: s["result"].update(complete_coframe_covector_weight="w=-lambda"))
    catch("ERASE_C08_INDEPENDENCE", lambda s: s["result"].update(depth_does_not_determine_holonomy="NONE"))
    catch("ERASE_GAUGE_QUERY", lambda s: s["gauge"].pop())
    catch("ERASE_CHARACTER_TARGET", lambda s: s["characters"].pop())
    catch("ERASE_ONE_FORM_FAMILY", lambda s: s["one_forms"].pop())

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
