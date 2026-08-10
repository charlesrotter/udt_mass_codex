#!/usr/bin/env python3
"""Exercise fail-closed semantic mutations against the stationary classification."""

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
        "flat": rows("FLAT_SUBLOCUS_ATLAS.tsv"),
        "descent": rows("DESCENT_ATLAS.tsv"),
        "holonomy": rows("HOLONOMY_ATLAS.tsv"),
        "ownership": rows("R17_OWNERSHIP_ADJUDICATION.tsv"),
    }


def valid(data: dict) -> bool:
    flat = data["flat"]
    descent = data["descent"]
    holonomy = data["holonomy"]
    result = data["result"]
    ownership = data["ownership"]
    return all((
        [row["lambda"] for row in flat] == ["-2", "-1", "0", "1/2", "1", "2"],
        [row["regular_root_count_at_a_1_over_64"] for row in flat] == ["1", "1", "1", "1", "0", "2"],
        all(row["C01_C06_witness"] == "NONCONSTANT_NOT_FLAT_FULL_SO2" for row in flat),
        len(descent) == 8,
        all("IFF_PHI_CONSTANT" in row["global_curvature_horizontal_on_RxS3"] for row in descent[:6]),
        all(row["canonical_Hopf_tangent_descent"].startswith("NONE_REGULAR") for row in descent[:6]),
        next(row for row in descent if row["lambda"] == "1")["abstract_parallel_quotient_descent"] == "NONE",
        {row["complete_total_space_holonomy"] for row in holonomy[:-1]} == {"TRIVIAL", "FULL_SO2"},
        holonomy[-1]["curvature_status"] == "IMPOSSIBLE_IN_DECLARED_ARENA",
        result["manifest_backed_r17_source_selection"] is False,
        result["proper_nontrivial_reduced_holonomy"] is False,
        all(row["selection_consequence"] in {"NO_OWNER", "NOT_RELEVANT"} for row in ownership),
    ))


def main() -> int:
    original = state()
    assert valid(original)
    mutations = []

    def catch(name, mutate):
        item = copy.deepcopy(original)
        mutate(item)
        rejected = not valid(item)
        mutations.append({"catch_id": name, "mutation": name, "result": "REJECTED" if rejected else "MISSED"})

    catch("DROP_LAMBDA", lambda s: s["flat"].pop())
    catch("MUTATE_ROOT_COUNT", lambda s: s["flat"][0].update(regular_root_count_at_a_1_over_64="2"))
    catch("PROMOTE_C01_FLAT", lambda s: s["flat"][0].update(C01_C06_witness="FLAT"))
    catch("ALLOW_NONCONSTANT_HORIZONTAL", lambda s: s["descent"][0].update(global_curvature_horizontal_on_RxS3="GENERIC"))
    catch("ERASE_CONTROLS", lambda s: s["descent"].pop())
    catch("PROMOTE_LAMBDA1_DESCENT", lambda s: next(row for row in s["descent"] if row["lambda"] == "1").update(abstract_parallel_quotient_descent="YES"))
    catch("PROMOTE_CANONICAL_HOPF", lambda s: s["descent"][0].update(canonical_Hopf_tangent_descent="YES"))
    catch("INVENT_INTERMEDIATE_HOLONOMY", lambda s: s["holonomy"][1].update(complete_total_space_holonomy="U1_SUBGROUP"))
    catch("ALLOW_PROPER_REDUCTION", lambda s: s["holonomy"][-1].update(curvature_status="POSSIBLE"))
    catch("SELECT_MANIFEST_BACKED_R17_SOURCE", lambda s: s["result"].update(manifest_backed_r17_source_selection=True))
    catch("PROMOTE_REDUCED_HOLONOMY", lambda s: s["result"].update(proper_nontrivial_reduced_holonomy=True))
    catch("PROMOTE_OWNERSHIP_SOURCE", lambda s: s["ownership"][0].update(selection_consequence="SELECTS_FLAT"))

    failed = [row for row in mutations if row["result"] != "REJECTED"]
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=("catch_id", "mutation", "result"), lineterminator="\n")
        writer.writeheader()
        writer.writerows(mutations)
    result = {"total": len(mutations), "rejected": len(mutations) - len(failed), "failed": failed,
              "status": "PASS" if not failed else "FAIL"}
    (HERE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
